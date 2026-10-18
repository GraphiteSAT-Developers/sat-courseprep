"""What a student's plan lets them use right now, and the locks on everything else.

The plan's LIMITS (services/plans.py) decide what's included. A paid plan only counts while it's paid:
when a payment fails (status past_due) or the plan is paused, the student is treated as being on the free
plan until it's paid again. A canceled plan keeps working until the end of the period that was paid for.

Routes call require(user, feature) before starting something, and summary(user) tells the pages what to
show as locked. PLAN_LIMITS=false in the environment turns every lock off.
"""
from datetime import date, datetime, timedelta, timezone

from flask import current_app

from ..db import query
from .plans import LIMITS, ORDER, PLANS, key_for

UNPAID = {"past_due": "A payment didn't go through", "paused": "Your plan is paused"}

# feature: (limit key, what the student is trying to use, how it's counted)
FEATURES = {
    "practice_set": ("practice_sets_per_week", "Practice sets", "week"),
    "mock_test": ("practice_tests_per_month", "Mock tests", "month"),
    "level_up": ("level_up", "Level up", None),
    "study_plan": ("study_plan", "Your study plan", None),
    "review_queue": ("review_queue", "The review queue", None),
    "explanations": ("explanations", "Step-by-step explanations", None),
    "score_history": ("score_history", "Score history and skill breakdown", None),
    "parent_dashboard": ("parent_dashboard", "The parent dashboard", None),
}


def enforced():
    return bool(current_app.config.get("PLAN_LIMITS", True))


def subscription(student_id):
    from . import parent as parent_svc
    return parent_svc.subscription(student_id)


def standing(student_id):
    """(the plan that counts for limits, the subscription, why a paid plan isn't counting or None)."""
    sub = subscription(student_id)
    reason = UNPAID.get(sub["status"]) if sub["plan"] != "free" else None
    return ("free" if reason else key_for(sub["plan"])), sub, reason


def _since(period, today=None):
    today = today or datetime.now(timezone.utc).date()
    start = today - timedelta(days=today.weekday()) if period == "week" else today.replace(day=1)
    return datetime(start.year, start.month, start.day, tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def used(student_id, feature, today=None):
    """How many of a counted feature the student has started this week or month."""
    period = FEATURES[feature][2]
    since = _since(period, today)
    if feature == "practice_set":
        # Practice sets the student starts: topics and today's sets. Plan tasks, Level up and review count elsewhere.
        row = query("SELECT COUNT(*) AS n FROM practice_sessions WHERE user_id = ? AND mode = 'topic' AND created_at >= ?",
                    (student_id, since), one=True)
        return row["n"]
    row = query("SELECT COUNT(*) AS n FROM mock_tests WHERE user_id = ? AND created_at >= ?", (student_id, since), one=True)
    single = query("SELECT COUNT(*) AS n FROM practice_sessions WHERE user_id = ? AND mode = 'test' AND plan_task IS NULL "
                   "AND created_at >= ?", (student_id, since), one=True)
    return row["n"] + single["n"]


def cheapest_with(feature):
    """The lowest plan that includes a feature (or more of it)."""
    key = FEATURES[feature][0]
    for plan in ORDER:
        v = LIMITS[plan][key]
        if v is True or v is None or (isinstance(v, int) and not isinstance(v, bool) and v > 0 and plan != "free"):
            return plan
    return ORDER[-1]


def state(student_id, feature, today=None):
    """{ok, left, limit, used, need, need_name, reason} for one feature."""
    plan, sub, reason = standing(student_id)
    key, name, period = FEATURES[feature]
    limit = LIMITS[plan][key]
    out = {"feature": feature, "name": name, "plan": plan, "reason": reason, "period": period}
    if not enforced():
        return dict(out, ok=True, left=None, limit=None, used=None, need=None, need_name=None)
    if period:
        n = used(student_id, feature, today)
        left = None if limit is None else max(0, limit - n)
        ok = left is None or left > 0
        out.update(ok=ok, left=left, limit=limit, used=n)
    else:
        out.update(ok=bool(limit), left=None, limit=None, used=None)
    need = None
    if not out["ok"]:
        # A paid plan that isn't paid needs paying, not an upgrade (unless even the paid plan doesn't include it).
        paid_plan = key_for(sub["plan"])
        paid_limit = LIMITS[paid_plan][key]
        if reason and (paid_limit is True or paid_limit is None or (period and paid_limit and paid_limit > (out.get("used") or 0))):
            need = paid_plan
        else:
            need = next((p for p in ORDER[ORDER.index(plan) + 1:] if LIMITS[p][key] is True or LIMITS[p][key] is None
                         or (period and LIMITS[p][key] and LIMITS[p][key] > (out.get("used") or 0))), ORDER[-1])
    out["need"] = need
    out["need_name"] = PLANS[need]["name"] if need else None
    return out


def message(st):
    if st["reason"]:
        return f"{st['reason']}, so {st['name'].lower()} {'are' if st['name'].endswith('s') else 'is'} locked until it's paid. Open Settings, then Subscription."
    if st["period"] and st["limit"]:
        each = "this week" if st["period"] == "week" else "this month"
        return (f"You've used all {st['limit']} of your {st['name'].lower()} {each}. "
                f"{st['need_name']} includes more.")
    return f"{st['name']} {'come' if st['name'].endswith('s') else 'comes'} with the {st['need_name']} plan and up."


def require(user, feature, today=None):
    """Raises 402 with code plan_required when the student's plan doesn't include this right now."""
    from ..security import ApiError  # here, so the site build can read this module without Flask's request helpers
    st = state(user["id"], feature, today)
    if not st["ok"]:
        raise ApiError(402, message(st), code="plan_required", extra={"lock": public_state(st)})
    return st


def allowed(user_id, feature):
    return state(user_id, feature)["ok"]


def public_state(st):
    return {k: st[k] for k in ("feature", "name", "ok", "left", "limit", "used", "need", "need_name", "reason", "period")}


def summary(student_id, today=None):
    """Everything the pages need to show locks: the plan, whether it's paid, and each feature's state."""
    plan, sub, reason = standing(student_id)
    return {"plan": key_for(sub["plan"]), "plan_name": sub["plan_name"], "status": sub["status"], "counts_as": plan,
            "unpaid": reason, "enforced": enforced(),
            "features": {f: public_state(state(student_id, f, today)) for f in FEATURES}}


LOCKED_EXPLANATION = (
    '<div class="xp-locked"><p><strong>Step-by-step explanations come with the No. 2 plan and up.</strong> '
    'You can see the right answer here. <a href="settings.html#subscription">See plans</a></p></div>')


def redact(user_id, questions):
    """Swaps each explanation for a short note when the plan doesn't include explanations."""
    if allowed(user_id, "explanations"):
        return questions
    for q in questions:
        if isinstance(q, dict) and "explain_html" in q:
            q["explain_html"] = LOCKED_EXPLANATION
    return questions


def today_iso():
    return date.today().isoformat()
