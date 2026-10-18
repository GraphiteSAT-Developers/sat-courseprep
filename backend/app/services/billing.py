"""Checkout and Stripe: buying a plan, and keeping plans in step with Stripe.

Without STRIPE_SECRET_KEY, checkout starts the plan straight away and records it in the billing history
with "No card was charged". With it, checkout sends the parent to Stripe's payment page, and the plan
starts when Stripe confirms the payment (on the way back to checkout.html, and through the webhook).

Prices come from plans.py. The first checkout for each plan, billing option and amount creates the
matching Stripe price (found again later by its lookup key), so there's nothing to set up in Stripe by hand.
"""
from datetime import date, datetime, timezone

from flask import current_app

from ..db import execute, now_iso, query
from . import parent as parent_svc, stripe_api
from .plans import PLANS, interval_words, key_for, money, next_renewal

_price_ids = {}  # lookup key -> Stripe price id, so each price is looked up once per server start


def lookup_key(plan, interval):
    return f"graphite_{plan}_{interval}_{PLANS[plan]['prices'][interval]}"


def price_id(plan, interval):
    """The Stripe price for this plan and billing option, created the first time it's needed."""
    key = lookup_key(plan, interval)
    if key in _price_ids:
        return _price_ids[key]
    found = stripe_api.request("GET", "/prices", {"lookup_keys": [key], "active": True, "limit": 1})
    if found.get("data"):
        _price_ids[key] = found["data"][0]["id"]
        return _price_ids[key]
    p = PLANS[plan]
    made = stripe_api.request("POST", "/prices", {
        "currency": "usd", "unit_amount": p["prices"][interval], "recurring": {"interval": interval},
        "lookup_key": key, "product_data": {"name": f"Graphite SAT {p['name']}", "metadata": {"plan": plan}},
        "metadata": {"plan": plan, "interval": interval}})
    _price_ids[key] = made["id"]
    return made["id"]


def start(payer, student, plan, interval):
    """Begins checkout. Returns {"url": Stripe's payment page} when payments are live, or the started plan."""
    if not stripe_api.is_live():
        sub = parent_svc.change_plan(payer["id"], student["id"], plan, interval)
        return {"done": True, "subscription": sub}
    base = current_app.config["BASE_URL"]
    meta = {"student_id": student["id"], "plan": plan, "interval": interval, "payer_id": payer["id"]}
    params = {
        "mode": "subscription",
        "line_items": [{"price": price_id(plan, interval), "quantity": 1}],
        "client_reference_id": student["id"],
        "metadata": meta,
        "subscription_data": {"metadata": meta, "description": f"Graphite SAT {PLANS[plan]['name']} for {student['name']}"},
        "allow_promotion_codes": True,
        "success_url": f"{base}/checkout.html?session_id={{CHECKOUT_SESSION_ID}}",
        "cancel_url": f"{base}/checkout.html?plan={plan}&interval={interval}&student={student['id']}&canceled=1",
    }
    if payer["stripe_customer_id"]:
        params["customer"] = payer["stripe_customer_id"]
    else:
        params["customer_email"] = payer["email"]
    session = stripe_api.request("POST", "/checkout/sessions", params)
    return {"url": session["url"]}


def confirm(session_id, payer):
    """After Stripe sends the parent back: starts the plan if the payment went through (the webhook may already have)."""
    s = stripe_api.request("GET", f"/checkout/sessions/{session_id}", {"expand": ["subscription"]})
    meta = s.get("metadata") or {}
    if str(meta.get("payer_id")) != str(payer["id"]):
        return None
    paid = s.get("status") == "complete" and s.get("payment_status") in ("paid", "no_payment_required")
    if paid:
        _activate(meta, s.get("customer"), s.get("subscription"), s.get("amount_total"))
    return {"paid": paid, "status": s.get("status"), "student_id": int(meta["student_id"]),
            "subscription": parent_svc.subscription(int(meta["student_id"]))}


def _sub_row(student_id):
    row = query("SELECT * FROM subscriptions WHERE student_id = ?", (student_id,), one=True)
    return dict(row) if row else None


def _period_end(sub):
    """When a Stripe subscription renews, as an ISO date."""
    stamp = sub.get("current_period_end") or ((sub.get("items") or {}).get("data") or [{}])[0].get("current_period_end")
    return datetime.fromtimestamp(stamp, tz=timezone.utc).date().isoformat() if stamp else None


def _activate(meta, customer_id, subscription, amount=None):
    """Starts a paid plan from a completed checkout. Safe to call twice for the same checkout."""
    student_id, plan, interval = int(meta["student_id"]), key_for(meta.get("plan")), meta.get("interval")
    payer_id = int(meta["payer_id"]) if meta.get("payer_id") else None
    if isinstance(subscription, str):
        subscription = stripe_api.request("GET", f"/subscriptions/{subscription}")
    sub_id = subscription["id"] if subscription else None
    current = _sub_row(student_id)
    if current and sub_id and current.get("stripe_subscription_id") == sub_id:
        return  # already started (the webhook and the return to checkout both land here)
    old = current.get("stripe_subscription_id") if current else None
    if old and old != sub_id:
        # Switching plans: end the old subscription now. Stripe credits the unused time to the customer.
        try:
            stripe_api.request("DELETE", f"/subscriptions/{old}", {"prorate": True, "invoice_now": True})
        except stripe_api.StripeError:
            current_app.logger.warning("Couldn't end the old Stripe subscription %s; end it in the Stripe dashboard.", old)
    renews = (subscription and _period_end(subscription)) or next_renewal(date.today(), interval, parent_svc.add_months).isoformat()
    parent_svc._save(student_id, {"plan": plan, "billing_interval": interval, "status": "active", "renews_on": renews,
                                  "paused_until": None}, payer_id)
    execute("UPDATE subscriptions SET stripe_subscription_id = ? WHERE student_id = ?", (sub_id, student_id))
    if customer_id and payer_id:
        execute("UPDATE users SET stripe_customer_id = ? WHERE id = ?", (customer_id, payer_id))
    paid = amount if amount is not None else PLANS[plan]["prices"][interval]
    parent_svc._event(student_id, payer_id, "change",
                      f"{PLANS[plan]['name']}, billed {interval_words(interval)}. Paid {money(paid)}. Renews {parent_svc.nice_date(renews)}.", paid)


# ---------- keeping Stripe in step with the parent dashboard ----------

def sync_action(student_id, action, paused_until=None):
    """Pause, cancel and resume on the parent dashboard also change the Stripe subscription."""
    row = _sub_row(student_id)
    if not stripe_api.is_live() or not row or not row.get("stripe_subscription_id"):
        return
    sid = row["stripe_subscription_id"]
    if action == "cancel":
        stripe_api.request("POST", f"/subscriptions/{sid}", {"cancel_at_period_end": True})
    elif action == "resume":
        stripe_api.request("POST", f"/subscriptions/{sid}", {"cancel_at_period_end": False, "pause_collection": ""})
    elif action == "pause":
        until = datetime.fromisoformat(paused_until).replace(tzinfo=timezone.utc)
        stripe_api.request("POST", f"/subscriptions/{sid}", {"pause_collection": {"behavior": "void", "resumes_at": int(until.timestamp())}})


def portal_url(payer):
    """Stripe's billing page, where a parent updates their card and downloads receipts."""
    if not stripe_api.is_live() or not payer["stripe_customer_id"]:
        return None
    s = stripe_api.request("POST", "/billing_portal/sessions", {"customer": payer["stripe_customer_id"],
                                                                "return_url": current_app.config["BASE_URL"] + "/parent.html"})
    return s["url"]


# ---------- webhook ----------

def handle_event(event):
    """Applies one Stripe webhook event. Each event is handled once, however many times Stripe sends it."""
    if query("SELECT id FROM stripe_events WHERE id = ?", (event["id"],), one=True):
        return "duplicate"
    kind, obj = event["type"], event["data"]["object"]
    if kind == "checkout.session.completed" and obj.get("mode") == "subscription":
        if obj.get("payment_status") in ("paid", "no_payment_required") and (obj.get("metadata") or {}).get("student_id"):
            _activate(obj["metadata"], obj.get("customer"), obj.get("subscription"), obj.get("amount_total"))
    elif kind in ("customer.subscription.updated", "customer.subscription.deleted"):
        row = query("SELECT * FROM subscriptions WHERE stripe_subscription_id = ?", (obj["id"],), one=True)
        if row:
            row = dict(row)
            if kind == "customer.subscription.deleted" or obj.get("status") in ("canceled", "incomplete_expired"):
                parent_svc._save(row["student_id"], {"plan": "free", "billing_interval": None, "status": "active",
                                                     "renews_on": None, "paused_until": None}, None)
                execute("UPDATE subscriptions SET stripe_subscription_id = NULL WHERE student_id = ?", (row["student_id"],))
                parent_svc._event(row["student_id"], None, "change", f"The paid plan ended. Back on the free {PLANS['free']['name']} plan.")
            else:
                status = ("paused" if obj.get("pause_collection") else "canceled" if obj.get("cancel_at_period_end") else "active")
                row.update(status=status, renews_on=_period_end(obj) or row["renews_on"])
                if status != "paused":
                    row["paused_until"] = None
                parent_svc._save(row["student_id"], row, row["updated_by"])
    elif kind in ("invoice.paid", "invoice.payment_failed") and obj.get("subscription"):
        row = query("SELECT * FROM subscriptions WHERE stripe_subscription_id = ?", (obj["subscription"],), one=True)
        if row and kind == "invoice.payment_failed":
            parent_svc._event(row["student_id"], None, "payment_failed",
                              "A payment didn't go through. Stripe will try again; update the card under Manage billing.")
        elif row and obj.get("billing_reason") == "subscription_cycle":
            parent_svc._event(row["student_id"], None, "renewal", f"Renewed. Paid {money(obj.get('amount_paid') or 0)}.", obj.get("amount_paid") or 0)
    execute("INSERT INTO stripe_events (id, kind, received_at) VALUES (?, ?, ?)", (event["id"], kind, now_iso()))
    return "ok"
