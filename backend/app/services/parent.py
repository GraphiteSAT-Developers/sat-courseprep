"""The parent dashboard: one linked student's progress, alerts, settings, plan and billing.

Everything here is read from the student's own records (the same ones the student's dashboard uses).
Parents can change a few of the student's settings (weekly goal, test date, target score) and the
student's plan. Paid plans are bought on the checkout page (services/billing.py). Until Stripe is connected,
plan changes take effect and are recorded in the billing history, but no card is charged.
"""
import json
from calendar import monthrange
from datetime import date, datetime, timedelta, timezone

from ..db import execute, local_day, now_iso, query
from . import dashboard, levels, stripe_api, today as today_svc
from .plans import ALERT_DAYS, INTERVALS, PAUSE_DAYS, PLANS, interval_words, key_for, next_renewal, price_label  # noqa: F401

def payments_live():
    """True once Stripe is connected (STRIPE_SECRET_KEY is set)."""
    return stripe_api.is_live()


def money(cents):
    return f"${cents / 100:,.2f}".replace(".00", "")


def add_months(d, n):
    m = d.month - 1 + n
    y, m = d.year + m // 12, m % 12 + 1
    return date(y, m, min(d.day, monthrange(y, m)[1]))


def nice_date(iso_date):
    d = date.fromisoformat(iso_date)
    return f"{d.strftime('%b')} {d.day}, {d.year}"


# ---------- subscription ----------

def subscription(student_id, today=None):
    today = today or date.today()
    row = query("SELECT * FROM subscriptions WHERE student_id = ?", (student_id,), one=True)
    sub = dict(row) if row else {"plan": "free", "billing_interval": None, "status": "active", "renews_on": None, "paused_until": None}
    # A canceled plan runs to the end of its paid period; a pause ends by itself.
    if sub["status"] == "canceled" and sub["renews_on"] and sub["renews_on"] < today.isoformat():
        sub.update(plan="free", billing_interval=None, status="active", renews_on=None)
        _save(student_id, sub, None)
    elif sub["status"] == "paused" and sub["paused_until"] and sub["paused_until"] < today.isoformat():
        sub.update(status="active", paused_until=None)
        _save(student_id, sub, None)
    key = key_for(sub["plan"])
    plan = PLANS[key]
    interval = sub["billing_interval"] if sub["billing_interval"] in INTERVALS else None
    price = plan["prices"][interval] if interval else 0
    return {"plan": key, "plan_name": plan["name"], "interval": interval, "status": sub["status"],
            "renews_on": sub["renews_on"], "paused_until": sub["paused_until"], "price_cents": price,
            "price_label": price_label(key, interval)}


def _save(student_id, sub, parent_id):
    stamp = now_iso()
    execute("INSERT INTO subscriptions (student_id, plan, billing_interval, status, renews_on, paused_until, updated_by, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT (student_id) DO UPDATE SET plan = excluded.plan, "
            "billing_interval = excluded.billing_interval, status = excluded.status, renews_on = excluded.renews_on, "
            "paused_until = excluded.paused_until, updated_by = excluded.updated_by, updated_at = excluded.updated_at",
            (student_id, sub["plan"], sub["billing_interval"], sub["status"], sub["renews_on"], sub["paused_until"], parent_id, stamp))
    execute("UPDATE users SET plan = ? WHERE id = ?", (sub["plan"], student_id))


def _event(student_id, parent_id, kind, detail, amount=0):
    if not payments_live() and amount:
        detail += " No card was charged: payments aren't connected yet."
    execute("INSERT INTO billing_events (student_id, parent_id, kind, detail, amount_cents, at) VALUES (?, ?, ?, ?, ?, ?)",
            (student_id, parent_id, kind, detail, amount, now_iso()))


def change_plan(parent_id, student_id, plan, interval, today=None):
    today = today or date.today()
    if plan == "free":
        cur = subscription(student_id, today)
        _save(student_id, {"plan": "free", "billing_interval": None, "status": "active", "renews_on": None, "paused_until": None}, parent_id)
        if cur["plan"] != "free":
            _event(student_id, parent_id, "change", f"Switched from {cur['plan_name']} to the free {PLANS['free']['name']} plan.")
        return subscription(student_id, today)
    renews = next_renewal(today, interval, add_months).isoformat()
    _save(student_id, {"plan": plan, "billing_interval": interval, "status": "active", "renews_on": renews, "paused_until": None}, parent_id)
    price = PLANS[plan]["prices"][interval]
    _event(student_id, parent_id, "change",
           f"{PLANS[plan]['name']}, billed {interval_words(interval)} at {money(price)}. Renews {nice_date(renews)}.", price)
    return subscription(student_id, today)


def pause(parent_id, student_id, today=None):
    today = today or date.today()
    row = dict(query("SELECT * FROM subscriptions WHERE student_id = ?", (student_id,), one=True))
    until = (today + timedelta(days=PAUSE_DAYS)).isoformat()
    renews = (date.fromisoformat(row["renews_on"]) + timedelta(days=PAUSE_DAYS)).isoformat()
    row.update(status="paused", paused_until=until, renews_on=renews)
    _save(student_id, row, parent_id)
    _event(student_id, parent_id, "pause", f"Paused until {nice_date(until)}. The next bill moves to {nice_date(renews)}.")
    return subscription(student_id, today)


def resume(parent_id, student_id, today=None):
    today = today or date.today()
    row = dict(query("SELECT * FROM subscriptions WHERE student_id = ?", (student_id,), one=True))
    was = row["status"]
    row.update(status="active", paused_until=None)
    _save(student_id, row, parent_id)
    _event(student_id, parent_id, "resume", "Resumed." if was == "paused" else f"Cancellation undone. Renews {nice_date(row['renews_on'])}.")
    return subscription(student_id, today)


def cancel(parent_id, student_id, today=None):
    today = today or date.today()
    row = dict(query("SELECT * FROM subscriptions WHERE student_id = ?", (student_id,), one=True))
    row.update(status="canceled", paused_until=None)
    _save(student_id, row, parent_id)
    _event(student_id, parent_id, "cancel",
           f"Canceled. {PLANS[key_for(row['plan'])]['name']} stays on until {nice_date(row['renews_on'])}, then the plan returns to the free {PLANS['free']['name']} plan.")
    return subscription(student_id, today)


def billing_history(student_id):
    return [{"at": r["at"], "kind": r["kind"], "detail": r["detail"], "amount_cents": r["amount_cents"]}
            for r in query("SELECT * FROM billing_events WHERE student_id = ? ORDER BY at DESC, id DESC LIMIT 20", (student_id,))]


# ---------- progress ----------

def _study_dates(student_id, since):
    rows = query("SELECT at AS t FROM activity WHERE user_id = ? AND at >= ? "
                 "UNION ALL SELECT seen_at AS t FROM practice_seen WHERE user_id = ? AND seen_at >= ? "
                 "UNION ALL SELECT created_at AS t FROM practice_sessions WHERE user_id = ? AND created_at >= ?",
                 (student_id, since, student_id, since, student_id, since))
    return {local_day(r["t"]).isoformat() for r in rows}


def _activity(student_id):
    """Finished practice, newest first: sets, practice tests and the diagnostic."""
    out = []
    for r in query("SELECT id, mode, title, item_ids, correct, seconds_used, submitted_at, plan_task FROM practice_sessions "
                   "WHERE user_id = ? AND submitted_at IS NOT NULL ORDER BY submitted_at DESC LIMIT 20", (student_id,)):
        task = r["plan_task"] or ""
        kind = ("Practice test" if r["mode"] == "test" else "Level up" if task.startswith("ladder:")
                else "Study plan" if r["mode"] == "quiz" else "Review" if r["mode"] == "review" else "Topic practice")
        out.append({"title": r["title"], "kind": kind, "at": r["submitted_at"], "correct": r["correct"],
                    "total": len(json.loads(r["item_ids"])), "minutes": round((r["seconds_used"] or 0) / 60)})
    for r in query("SELECT test_id, correct, total, seconds_used, submitted_at FROM test_attempts "
                   "WHERE user_id = ? AND test_id NOT LIKE 'practice-%' ORDER BY submitted_at DESC LIMIT 10", (student_id,)):
        out.append({"title": "Full practice test", "kind": "Practice test", "at": r["submitted_at"], "correct": r["correct"],
                    "total": r["total"], "minutes": round(r["seconds_used"] / 60)})
    for r in query("SELECT results, submitted_at FROM diagnostics WHERE user_id = ? AND submitted_at IS NOT NULL "
                   "ORDER BY submitted_at DESC LIMIT 3", (student_id,)):
        res = json.loads(r["results"])
        out.append({"title": "10-question diagnostic", "kind": "Diagnostic", "at": r["submitted_at"], "correct": res["correct"],
                    "total": res["total"], "minutes": None})
    out.sort(key=lambda a: a["at"], reverse=True)
    return out[:15]


def _alerts(student, link, s, scores, diagnostic, today):
    first, out = student["name"].split(" ")[0], []
    if link["alert_days"]:
        if not s["last_active"]:
            out.append({"level": "warn", "text": f"{first} hasn't started practicing yet."})
        else:
            idle = (today - local_day(s["last_active"])).days
            if idle >= link["alert_days"]:
                out.append({"level": "warn", "text": f"{first} hasn't practiced in {idle} days."})
    if s["days_to_test"] is not None and s["days_to_test"] <= 21 and not diagnostic:
        out.append({"level": "warn", "text": f"The SAT is {s['days_to_test']} days away and the diagnostic isn't done yet."})
    if len(scores) >= 2:
        change = scores[-1]["pct"] - scores[-2]["pct"]
        if change <= -10:
            out.append({"level": "warn", "text": f"The latest practice test was {abs(change)} points lower than the one before."})
        elif change >= 10:
            out.append({"level": "good", "text": f"Up {change} points on the latest practice test."})
    goal = s["goal_minutes"]
    if today.weekday() >= 3 and goal and s["minutes_week"] < goal / 2:
        out.append({"level": "info", "text": f"{s['minutes_week']} of {goal} minutes studied this week so far."})
    if s["streak_days"] >= 5:
        out.append({"level": "good", "text": f"{first} has practiced {s['streak_days']} days in a row."})
    return out


def summary(student, link, today=None):
    today = today or date.today()
    dash = dashboard.build(student, today)
    d = dash["summary"]
    monday = today - timedelta(days=today.weekday())
    since_week = datetime(monday.year, monday.month, monday.day, tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    since_60 = (datetime.now(timezone.utc) - timedelta(days=60)).strftime("%Y-%m-%dT%H:%M:%SZ")
    days = _study_dates(student["id"], since_60)
    streak, day = 0, today if today.isoformat() in days else today - timedelta(days=1)
    while day.isoformat() in days:
        streak += 1
        day -= timedelta(days=1)
    last = query("SELECT MAX(t) AS t FROM (SELECT MAX(at) AS t FROM activity WHERE user_id = ? "
                 "UNION ALL SELECT MAX(seen_at) FROM practice_seen WHERE user_id = ? "
                 "UNION ALL SELECT MAX(created_at) FROM practice_sessions WHERE user_id = ?) x",
                 (student["id"], student["id"], student["id"]), one=True)["t"]
    week = query("SELECT COALESCE(SUM(correct), 0) AS c, COUNT(*) AS n FROM practice_sessions WHERE user_id = ? AND submitted_at >= ?",
                 (student["id"], since_week), one=True)
    asked = sum(len(json.loads(r["item_ids"])) for r in query(
        "SELECT item_ids FROM practice_sessions WHERE user_id = ? AND submitted_at >= ?", (student["id"], since_week)))
    answered = query("SELECT COUNT(*) AS n FROM practice_seen WHERE user_id = ? AND seen_at >= ?", (student["id"], since_week), one=True)["n"]
    stats = {
        "last_active": last, "streak_days": streak, "minutes_week": d["practice_minutes_week"],
        "goal_minutes": d["weekly_goal_hours"] * 60, "study_days_week": d["study_days_week"],
        "days_to_test": d["days_to_test"], "questions_week": answered,
        "accuracy_week": round(week["c"] / asked * 100) if asked else None,
    }
    scores = [{"label": h["label"], "date": h["date"], "pct": h["pct"], "correct": h["correct"], "total": h["total"]} for h in dash["history"]]
    drow = query("SELECT results, submitted_at FROM diagnostics WHERE user_id = ? AND submitted_at IS NOT NULL ORDER BY submitted_at DESC LIMIT 1",
                 (student["id"],), one=True)
    diagnostic = None
    if drow:
        res = json.loads(drow["results"])
        diagnostic = {"at": drow["submitted_at"], "correct": res["correct"], "total": res["total"],
                      "strengths": res.get("strengths", []), "focus": res.get("focus", [])}
    plan = None
    found = today_svc.week_tasks(student["id"], today)
    if found:
        _, p, index, w, tasks = found
        plan = {"week": w["n"], "weeks": len(p["weeks"]), "phase": w["phase_label"], "difficulty": w.get("difficulty_label"),
                "focus": [f["name"] for f in w.get("focus", [])], "done": sum(1 for t in tasks if t["done"]), "tasks": len(tasks)}
    ladder = [{"name": t["name"], "unlocked": t["unlocked"], "passed": sum(1 for lv in t["levels"] if lv["status"] == "passed"),
               "levels": len(t["levels"])} for t in levels.overview(student["id"])["tracks"]]
    return {
        "student": {"id": student["id"], "name": student["name"], "first_name": student["name"].split(" ")[0],
                    "email": student["email"], "grade": student["grade"], "test_date": student["test_date"],
                    "target_score": student["target_score"], "weekly_goal_hours": student["weekly_goal_hours"]},
        "settings": {"weekly_report": bool(link["weekly_report"]), "alert_days": link["alert_days"]},
        "overview": stats,
        "alerts": _alerts(student, link, stats, scores, diagnostic, today),
        "scores": scores,
        "domains": [{"name": x["name"], "pct": x["pct"], "focus": x["focus"]} for x in dash["domains"] if x["section"] == "Math"],
        "diagnostic": diagnostic,
        "plan": plan,
        "levels": ladder,
        "review": {"total": len(dash["review"]), "due": sum(1 for r in dash["review"] if r["due_now"])},
        "activity": _activity(student["id"]),
        "subscription": subscription(student["id"], today),
        "billing": billing_history(student["id"]),
    }


# ---------- the weekly email ----------

def report_text(parent, s):
    st, o = s["student"], s["overview"]
    lines = [f"Hi {parent['name'].split(' ')[0]},", "", f"Here's {st['first_name']}'s week on Graphite.", ""]
    lines.append(f"- Study time: {o['minutes_week']} of {o['goal_minutes']} minutes")
    lines.append(f"- Days practiced this week: {sum(1 for x in o['study_days_week'] if x)} of 7")
    lines.append(f"- Questions answered: {o['questions_week']}" + (f" ({o['accuracy_week']}% right)" if o["accuracy_week"] is not None else ""))
    if s["scores"]:
        lines.append(f"- Latest practice test: {s['scores'][-1]['pct']}% ({s['scores'][-1]['label']})")
    if o["days_to_test"] is not None:
        lines.append(f"- SAT in {o['days_to_test']} days")
    if s["plan"]:
        lines.append(f"- Study plan: week {s['plan']['week']} of {s['plan']['weeks']}, {s['plan']['done']} of {s['plan']['tasks']} tasks done")
    if s["alerts"]:
        lines += ["", "Worth a look:"] + [f"- {a['text']}" for a in s["alerts"]]
    lines += ["", "See the full picture on your parent dashboard.", "", "Graphite"]
    return "\n".join(lines)
