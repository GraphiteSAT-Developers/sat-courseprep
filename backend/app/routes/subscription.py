"""A student's own subscription, on its own page, subscription.html. Every locked feature links there.

GET  /api/me/subscription              the plan, its status, what's locked, billing history and the plans
POST /api/me/subscription/plan         switch plans: {plan, interval}. Paid plans go through checkout once payments are live.
POST /api/me/subscription/<action>     pause, cancel, resume, or trial (the one free trial, no card)
POST /api/me/subscription/portal       Stripe's page for the card on file, receipts and paying a failed bill
POST /api/me/subscription/test         test account only: {plan, status} takes effect at once, no checkout or card

A parent can manage the same subscription from the parent dashboard. Whoever paid last is the payer on file.
"""
from datetime import date, timedelta

from flask import Blueprint, jsonify

from ..db import query
from ..security import ApiError, body, current_user, login_required
from .. import admins
from ..services import access, billing, parent as service, stripe_api
from ..services.plans import INTERVALS, PLANS, public_plans

bp = Blueprint("subscription", __name__, url_prefix="/api/me/subscription")


def _student():
    me = current_user()
    if me["role"] == "parent":
        raise ApiError(403, "Parents manage plans on the parent dashboard.", code="parent_account")
    return me


def _payer(student_id):
    """Who's paying: the account that last bought a paid plan."""
    sub = service.subscription(student_id)
    if sub["plan"] == "free":
        return None
    row = query("SELECT parent_id FROM billing_events WHERE student_id = ? AND kind = 'change' AND parent_id IS NOT NULL "
                "ORDER BY id DESC LIMIT 1", (student_id,), one=True)
    if not row:
        return None
    return query("SELECT id, name, role, email, stripe_customer_id FROM users WHERE id = ?", (row["parent_id"],), one=True)


def _out(me):
    sub = service.subscription(me["id"])
    payer = _payer(me["id"])
    return {
        "subscription": sub,
        "billing": service.billing_history(me["id"]),
        "access": access.summary(me["id"]),
        "plans": public_plans(),
        "payments_live": stripe_api.is_live(),
        "pause_days": service.PAUSE_DAYS,
        "trial": {"plan": service.TRIAL_PLAN, "plan_name": PLANS[service.TRIAL_PLAN]["name"], "days": service.TRIAL_DAYS},
        "payer": None if not payer else {"you": payer["id"] == me["id"], "role": payer["role"],
                                          "name": payer["name"] if payer["id"] != me["id"] else "You"},
        "has_card": bool(payer and payer["stripe_customer_id"]),
        "test_account": _is_test(me),
    }


def _is_test(me):
    return admins.is_test_student(me)


TEST_STATUSES = ("active", "past_due", "paused", "canceled")


@bp.post("/test")
@login_required
def test_switch():
    """The test account switches plans instantly, to try every plan and lock without checkout or a card."""
    me = _student()
    if not _is_test(me):
        raise ApiError(403, "Only the test account can switch plans instantly.", code="not_test_account")
    data = body()
    plan, status = data.get("plan"), data.get("status", "active")
    if plan not in PLANS:
        raise ApiError(400, "Pick a plan.", "plan")
    if status not in TEST_STATUSES or (plan == "free" and status != "active"):
        raise ApiError(400, "Pick active, past due, paused or canceled for a paid plan.", "status")
    sub = service.subscription(me["id"])
    interval = None if plan == "free" else (sub["interval"] or "month")
    renews = None if plan == "free" else service.next_renewal(date.today(), interval, service.add_months).isoformat()
    paused = (date.today() + timedelta(days=service.PAUSE_DAYS)).isoformat() if status == "paused" else None
    service._save(me["id"], {"plan": plan, "billing_interval": interval, "status": status, "renews_on": renews, "paused_until": paused}, me["id"])
    service._event(me["id"], me["id"], "test", f"Test account: switched to {PLANS[plan]['name']}" + ("" if status == "active" else f" ({status.replace('_', ' ')})") + ".")
    return jsonify(_out(me))


@bp.get("")
@login_required
def overview():
    return jsonify(_out(_student()))


@bp.post("/plan")
@login_required
def change_plan():
    me = _student()
    data = body()
    plan, interval = data.get("plan"), data.get("interval")
    if plan not in PLANS:
        raise ApiError(400, "Pick a plan.", "plan")
    if plan == "free":
        sub = service.subscription(me["id"])
        if sub["plan"] != "free" and not stripe_api.is_live():
            # Nothing was charged, so there's no paid time to run out: the free plan starts now.
            service.change_plan(me["id"], me["id"], "free", None)
        elif sub["plan"] != "free" and sub["status"] != "canceled":
            # A paid plan runs to the end of the time paid for, then switches to free.
            _stripe(me["id"], "cancel")
            service.cancel(me["id"], me["id"])
        return jsonify(_out(me))
    if interval not in INTERVALS:
        raise ApiError(400, "Pick weekly, monthly or yearly billing.", "interval")
    if data.get("agree") is not True:
        raise ApiError(400, "Check the box to agree to the terms and automatic renewal.", "agree")
    if stripe_api.payments_off():
        raise ApiError(503, "Paid plans aren't open yet, so nothing was charged. Try again soon.", code="payments_off")
    if stripe_api.is_live():
        # Paying happens on Stripe's page; the plan starts when Stripe confirms it.
        out = billing.start(me, me, plan, interval)
        return jsonify(dict(_out(me), checkout_url=out.get("url")))
    service.change_plan(me["id"], me["id"], plan, interval)
    return jsonify(_out(me)), 201


def _stripe(student_id, action, paused_until=None):
    try:
        billing.sync_action(student_id, action, paused_until)
    except stripe_api.StripeError:
        raise ApiError(502, "We couldn't reach the payment service, so nothing changed. Try again in a minute.") from None


@bp.post("/<action>")
@login_required
def plan_action(action):
    me = _student()
    if action == "portal":
        return portal()
    sub = service.subscription(me["id"])
    allowed = {"pause": sub["plan"] != "free" and sub["status"] == "active",
               "cancel": sub["plan"] != "free" and sub["status"] in ("active", "paused", "past_due", "trial"),
               "resume": sub["status"] in ("paused", "canceled"),
               "trial": sub["trial_available"]}
    if action not in allowed:
        raise ApiError(404, "Unknown plan action.")
    if not allowed[action]:
        raise ApiError(409, {"pause": "Only an active paid plan can be paused.", "cancel": "There's no paid plan to cancel.",
                             "resume": "The plan is already active.",
                             "trial": "The free trial is for the free plan, once per student."}[action])
    if action == "trial":
        service.start_trial(me["id"], me["id"])
        return jsonify(_out(me)), 201
    _stripe(me["id"], action, (date.today() + timedelta(days=service.PAUSE_DAYS)).isoformat())
    getattr(service, action)(me["id"], me["id"])
    return jsonify(_out(me))


def portal():
    me = _student()
    payer = _payer(me["id"])
    if payer and payer["id"] != me["id"]:
        raise ApiError(409, f"{payer['name']} pays for this plan, so the card is on their parent dashboard.", code="parent_pays")
    try:
        url = billing.portal_url(me)
    except stripe_api.StripeError:
        raise ApiError(502, "We couldn't open the billing page. Try again in a minute.") from None
    if not url:
        raise ApiError(409, "There's no card on file yet. It's added when you buy a plan." if stripe_api.is_live()
                       else "Payments aren't connected on this site yet, so there's no card to manage.")
    return jsonify({"url": url})
