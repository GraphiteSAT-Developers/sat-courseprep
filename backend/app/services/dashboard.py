"""Everything the dashboard shows, computed from one student's own records."""
import json
from datetime import date, datetime, timedelta, timezone

from ..db import query
from ..security import public_user
from .content import MATH_DOMAINS, RW_DOMAINS, all_tests, summary
from .planner import build_plan
from .studyplan import current_week
from .today import summary as today_summary

SET_SIZES = [5, 4, 3]
SHORT = {"Algebra": "Math", "Advanced Math": "Math", "Problem-Solving and Data Analysis": "Math",
         "Geometry and Trigonometry": "Math"}


def _due_label(due_on, today):
    due = date.fromisoformat(due_on)
    delta = (due - today).days
    if delta <= 0:
        return "Due today", True
    if delta == 1:
        return "Due tomorrow", False
    if delta < 7:
        return "Due " + due.strftime("%A"), False
    return f"Due {due.strftime('%b')} {due.day}", False


def study_plan_weeks(user, today):
    """The student's study plan from the diagnostic, in the dashboard's week list shape. None before the diagnostic."""
    row = query("SELECT plan FROM study_plans WHERE user_id = ? ORDER BY id DESC LIMIT 1", (user["id"],), one=True)
    if not row:
        return None
    plan = json.loads(row["plan"])
    now = current_week(plan, today)
    weeks = []
    for i, w in enumerate(plan["weeks"]):
        if i < now:
            continue
        if w["phase"] == "test":
            focus = "Test week: warm-up quiz, rest and test-day prep"
        else:
            focus = f"{w['phase_label']}: " + " and ".join(f["name"] for f in w["focus"]) + f". {w['difficulty_label']}"
        weeks.append({"week_of": w["week_of"], "focus": focus, "is_now": i == now})
    return {"weeks": weeks, "fits_test_date": bool(plan.get("test_date")), "study_plan": True}


def study_days(user_id, monday, since):
    """Which days this week (Monday first) the student practiced: a finished set or any answered question."""
    rows = query("SELECT at AS t FROM activity WHERE user_id = ? AND at >= ? "
                 "UNION ALL SELECT seen_at AS t FROM practice_seen WHERE user_id = ? AND seen_at >= ?",
                 (user_id, since, user_id, since))
    days = [False] * 7
    for r in rows:
        i = (date.fromisoformat(r["t"][:10]) - monday).days
        if 0 <= i < 7:
            days[i] = True
    return days


def build(user, today=None):
    today = today or date.today()
    attempts = query("SELECT id, test_id, seconds_used, correct, total, results, submitted_at FROM test_attempts "
                     "WHERE user_id = ? ORDER BY submitted_at", (user["id"],))
    history = []
    for a in attempts:
        when = datetime.strptime(a["submitted_at"], "%Y-%m-%dT%H:%M:%SZ")
        history.append({"id": a["id"], "test_id": a["test_id"], "date": when.date().isoformat(), "submitted_at": a["submitted_at"],
                        "label": f"{when.strftime('%b')} {when.day}", "correct": a["correct"], "total": a["total"],
                        "pct": round(a["correct"] / a["total"] * 100), "seconds_used": a["seconds_used"]})

    latest = json.loads(attempts[-1]["results"]) if attempts else None
    domain_pct = {}
    missed_skill = {}
    if latest:
        for d in latest["by_domain"]:
            domain_pct[d["domain"]] = round(d["right"] / d["total"] * 100)
        for q in latest["questions"]:
            if not q["correct"]:
                missed_skill.setdefault(q["domain"], q.get("skill"))

    measured = sorted((d for d in MATH_DOMAINS if d in domain_pct and domain_pct[d] < 100), key=lambda d: domain_pct[d])
    focus = set(measured[:3])
    domains = [{"name": d, "section": "Math", "pct": domain_pct.get(d), "focus": d in focus} for d in MATH_DOMAINS]
    domains += [{"name": d, "section": "Reading and Writing", "pct": None, "focus": False} for d in RW_DOMAINS]

    today_items = []
    for d, n in zip(measured[:3], SET_SIZES):
        why = f"{domain_pct[d]}% on your last practice test"
        if missed_skill.get(d):
            why = f"{missed_skill[d]}. {why}"
        today_items.append({"domain": d, "count": n, "why": why})

    monday = today - timedelta(days=today.weekday())
    since = datetime(monday.year, monday.month, monday.day, tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    week = query("SELECT COALESCE(SUM(seconds), 0) AS s FROM activity WHERE user_id = ? AND at >= ?", (user["id"], since), one=True)
    minutes_week = int(week["s"]) // 60

    items = query("SELECT id, test_id, question_index, domain, skill, right_count, due_on FROM review_items "
                  "WHERE user_id = ? AND cleared_at IS NULL ORDER BY due_on, id", (user["id"],))
    review = []
    for it in items:
        label, now_due = _due_label(it["due_on"], today)
        review.append({"id": it["id"], "section": SHORT.get(it["domain"], "R&W"), "skill": it["skill"],
                       "practice": it["test_id"].startswith("bank:"),
                       "domain": it["domain"], "right_count": it["right_count"], "due_label": label, "due_now": now_due})

    days_to_test = None
    if user["test_date"]:
        days_to_test = max(0, (date.fromisoformat(user["test_date"]) - today).days)

    taken = {a["test_id"] for a in attempts}
    tests = [dict(summary(t), taken=t["id"] in taken) for t in all_tests().values()]

    first = history[0] if history else None
    last = history[-1] if history else None
    return {
        "user": public_user(user),
        "summary": {
            "latest": last,
            "change_pct_points": (last["pct"] - first["pct"]) if len(history) > 1 else None,
            "attempts": len(history),
            "practice_minutes_week": minutes_week,
            "study_days_week": study_days(user["id"], monday, since),
            "weekly_goal_hours": user["weekly_goal_hours"],
            "days_to_test": days_to_test,
            "test_date": user["test_date"],
            "target_score": user["target_score"],
        },
        "history": history,
        "domains": domains,
        "today": today_summary(user["id"], today) or {
            "items": today_items, "questions": sum(i["count"] for i in today_items),
            "minutes": 25 if today_items else 0, "source": "domains" if today_items else "none"},
        "review": review,
        "plan": study_plan_weeks(user, today) or build_plan(user["test_date"], domain_pct, today),
        "tests": tests,
    }
