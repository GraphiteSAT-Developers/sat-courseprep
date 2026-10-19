"""The checkout page (checkout.html) and Stripe's webhook.

GET  /api/checkout                 plans, today's date, and who's signed in (with a parent's students)
POST /api/checkout                 buy a plan for a student: Stripe's payment page, or the started plan
GET  /api/checkout/session/<id>    after paying: did it go through?
POST /api/stripe/webhook           Stripe tells us about payments, renewals and cancellations
"""
from datetime import date

from flask import Blueprint, current_app, jsonify, request

from ..security import ApiError, body, current_user, login_required, rate_limited, record_event
from ..services import billing, family, parent as parent_svc, stripe_api
from ..services.plans import INTERVALS, PLANS, public_plans

bp = Blueprint("checkout", __name__, url_prefix="/api/checkout")
webhook_bp = Blueprint("stripe_webhook", __name__, url_prefix="/api/stripe")


@bp.get("")
def overview():
    me = current_user()
    account = None
    if me:
        account = {"name": me["name"], "role": me["role"]}
        if me["role"] == "parent":
            account["students"] = [{"id": s["id"], "name": s["name"], "subscription": parent_svc.subscription(s["id"])}
                                   for s in family.students_of(me["id"])]
        else:
            # A student can buy a plan for themselves.
            account["students"] = [{"id": me["id"], "name": me["name"], "self": True, "subscription": parent_svc.subscription(me["id"])}]
    return jsonify({"plans": public_plans(), "today": date.today().isoformat(),
                    "payments_live": stripe_api.is_live(), "account": account})


@bp.post("")
@login_required
def start():
    me = current_user()
    data = body()
    plan, interval = data.get("plan"), data.get("interval")
    if plan not in PLANS or plan == "free":
        raise ApiError(400, "Pick a paid plan.", "plan")
    if interval not in INTERVALS:
        raise ApiError(400, "Pick weekly, monthly or yearly billing.", "interval")
    if data.get("agree") is not True:
        raise ApiError(400, "Check the box to agree to the terms and automatic renewal.", "agree")
    try:
        student_id = int(data.get("student_id"))
    except (TypeError, ValueError):
        raise ApiError(400, "Pick which student the plan is for.", "student_id") from None
    students = family.students_of(me["id"]) if me["role"] == "parent" else [me]
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        raise ApiError(404, "That student isn't connected to your account.", "student_id")
    if stripe_api.payments_off():
        raise ApiError(503, "Paid plans aren't open yet, so nothing was charged. Try again soon.", code="payments_off")
    bucket = f"checkout:{me['id']}"
    if rate_limited(bucket, 20, 60):
        raise ApiError(429, "That's a lot of checkouts in an hour. Try again later.")
    record_event(bucket)
    try:
        out = billing.start(me, student, plan, interval)
    except stripe_api.StripeError:
        raise ApiError(502, "We couldn't reach the payment service. Nothing was charged. Try again in a minute.") from None
    out["student"] = {"id": student["id"], "name": student["name"]}
    return jsonify(out), 201 if out.get("done") else 200


@bp.get("/session/<session_id>")
@login_required
def session_status(session_id):
    if not stripe_api.is_live():
        raise ApiError(404, "Payments aren't connected.")
    if not session_id.startswith("cs_") or len(session_id) > 200:
        raise ApiError(404, "That checkout wasn't found.")
    try:
        out = billing.confirm(session_id, current_user())
    except stripe_api.StripeError:
        raise ApiError(502, "We couldn't check the payment just now. Refresh in a minute.") from None
    if not out:
        raise ApiError(404, "That checkout wasn't found.")
    me = current_user()
    students = family.students_of(me["id"]) if me["role"] == "parent" else [me]
    student = next((s for s in students if s["id"] == out["student_id"]), None)
    out["student"] = {"id": out["student_id"], "name": student["name"] if student else ""}
    return jsonify(out)


@webhook_bp.post("/webhook")
def webhook():
    """Add this address in Stripe (Developers > Webhooks): https://your-site/api/stripe/webhook"""
    try:
        event = stripe_api.verify_webhook(request.get_data(), request.headers.get("Stripe-Signature"),
                                          current_app.config.get("STRIPE_WEBHOOK_SECRET"))
    except stripe_api.StripeError as err:
        current_app.logger.warning("Rejected a Stripe webhook: %s", err)
        return jsonify({"error": "Bad signature."}), 400
    billing.handle_event(event)
    return jsonify({"received": True})
