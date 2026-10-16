"""Engagement: which days each student studied, retention across all students, and the weekly progress email.

A study day is any day with practice: an answered question, a finished set or test, the diagnostic,
or a step in a lesson. Everything here reads tables the rest of the app already writes.

The weekly email goes to the student (on unless they turn it off) and to a parent, only when the
student adds a parent email and turns the parent copy on. Every email has a one-click link to stop it.
Students who haven't studied in four weeks stop getting it: the email is a nudge, not a nag.
"""
import json
from datetime import date, timedelta

from flask import current_app
from itsdangerous import BadSignature, URLSafeSerializer

from ..db import execute, now_iso, query
from . import bank, mailer, masterclass
from .practice import topic_name

INACTIVE_STOP_DAYS = 28   # no weekly email after this long without studying
MIN_ACCOUNT_DAYS = 3      # skip accounts too new to have a week to report
RESEND_GAP_DAYS = 6       # running the sender twice in a week sends once


# ---------- study days ----------

ACTIVE_SOURCES = [
    "SELECT user_id, at AS t FROM activity",
    "SELECT user_id, seen_at AS t FROM practice_seen",
    "SELECT user_id, submitted_at AS t FROM test_attempts",
    "SELECT user_id, submitted_at AS t FROM diagnostics WHERE submitted_at IS NOT NULL",
]


def active_days(user_id=None, since=None):
    """{user_id: set of 'YYYY-MM-DD' days with any practice}. Optionally for one student, or from a date on."""
    sql = " UNION ALL ".join(ACTIVE_SOURCES)
    rows = query(f"SELECT user_id, t FROM ({sql}) AS a")
    out = {}
    for r in rows:
        if user_id is not None and r["user_id"] != user_id:
            continue
        day = r["t"][:10]
        if since and day < since:
            continue
        out.setdefault(r["user_id"], set()).add(day)
    return out


# ---------- retention ----------

WINDOWS = [  # (column, label, first day after signup, last day after signup)
    ("day1", "Came back the next day", 1, 1),
    ("week1", "Came back in the first week", 1, 7),
    ("week4", "Still studying in week 4", 22, 28),
]


def retention(today=None):
    """Per student: signup day, study days, and whether they came back in each window.

    A window counts only once it has fully passed for that student, so new accounts don't drag
    the numbers down. Returns (rows, summary).
    """
    today = today or date.today()
    days = active_days()
    users = query("SELECT id, email, name, created_at FROM users ORDER BY id")
    rows = []
    for u in users:
        signup = date.fromisoformat(u["created_at"][:10])
        mine = sorted(days.get(u["id"], set()))
        offsets = {(date.fromisoformat(d) - signup).days for d in mine}
        row = {"user_id": u["id"], "email": u["email"], "signup_date": signup.isoformat(), "study_days": len(mine),
               "last_active": mine[-1] if mine else "", "signup_week": (signup - timedelta(days=signup.weekday())).isoformat()}
        for col, _, lo, hi in WINDOWS:
            if (today - signup).days < hi + 1:
                row[col] = ""  # not over yet
            else:
                row[col] = "yes" if any(lo <= o <= hi for o in offsets) else "no"
        rows.append(row)
    summary = []
    for col, label, _, hi in WINDOWS:
        counted = [r for r in rows if r[col] != ""]
        kept = sum(r[col] == "yes" for r in counted)
        summary.append({"window": label, "students": len(counted), "returned": kept,
                        "percent": round(100 * kept / len(counted)) if counted else None})
    weekly = []
    monday = today - timedelta(days=today.weekday())
    for w in range(7, -1, -1):
        start = monday - timedelta(weeks=w)
        end = start + timedelta(days=6)
        active = sum(any(start.isoformat() <= d <= end.isoformat() for d in s) for s in days.values())
        weekly.append({"week_of": start.isoformat(), "active_students": active})
    return rows, summary, weekly


# ---------- the weekly report ----------

def _answered(user_id, start, end):
    """(answered, right) over the week, from practice sets: graded results, or checked answers in topic practice."""
    rows = query("SELECT item_ids, checked, results, created_at, submitted_at FROM practice_sessions WHERE user_id = ? "
                 "AND ((submitted_at >= ? AND submitted_at < ?) OR (submitted_at IS NULL AND created_at >= ? AND created_at < ?))",
                 (user_id, start, end, start, end))
    items = bank.all_items()
    answered = right = 0
    for r in rows:
        if r["results"]:
            qs = [q for q in json.loads(r["results"])["questions"] if q["answered"]]
            answered += len(qs)
            right += sum(q["correct"] for q in qs)
        else:
            ids = json.loads(r["item_ids"])
            for k, v in json.loads(r["checked"] or "{}").items():
                g = bank.graded_question(items[ids[int(k)]], int(k), v)
                answered += 1
                right += g["correct"]
    for a in query("SELECT correct, total FROM test_attempts WHERE user_id = ? AND submitted_at >= ? AND submitted_at < ? "
                   "AND test_id NOT LIKE 'practice-%'", (user_id, start, end)):
        answered += a["total"]
        right += a["correct"]
    return answered, right


def weekly_report(user, today=None):
    """What the student did in the last 7 days (today included), and what's next."""
    today = today or date.today()
    first = today - timedelta(days=6)
    start, end = first.isoformat(), (today + timedelta(days=1)).isoformat()
    days = active_days(user["id"], since=start).get(user["id"], set())
    answered, right = _answered(user["id"], start, end)
    minutes = round((query("SELECT COALESCE(SUM(seconds), 0) AS s FROM activity WHERE user_id = ? AND at >= ? AND at < ?",
                           (user["id"], start, end), one=True)["s"] or 0) / 60)
    lessons = masterclass.lessons()
    finished_lessons = [lessons[r["lesson_id"]]["title"] for r in query(
        "SELECT lesson_id FROM masterclass_progress WHERE user_id = ? AND completed_at >= ? AND completed_at < ? ORDER BY completed_at",
        (user["id"], start, end)) if r["lesson_id"] in lessons]
    topics = [r["topic"] for r in query("SELECT topic FROM practice_completions WHERE user_id = ? AND completed_at >= ? AND completed_at < ?",
                                        (user["id"], start, end))]
    due = query("SELECT COUNT(*) AS n FROM review_items WHERE user_id = ? AND cleared_at IS NULL AND due_on <= ?",
                (user["id"], today.isoformat()), one=True)["n"]
    days_to_test = None
    if user["test_date"]:
        d = (date.fromisoformat(user["test_date"]) - today).days
        days_to_test = d if d >= 0 else None
    return {
        "first_name": (user["name"] or "").split(" ")[0] or "there", "week_from": first, "week_to": today,
        "study_days": len(days), "answered": answered, "right": right, "minutes": minutes,
        "lessons": finished_lessons, "topics": [topic_name(t) for t in topics if topic_name(t)],
        "review_due": due, "days_to_test": days_to_test, "test_date": user["test_date"],
    }


def _when(d):
    return d.strftime("%b ") + str(d.day)


def email_text(report, base_url, unsubscribe_url, for_parent=False):
    """(subject, body) for the student, or for a parent when for_parent is set."""
    r, name = report, report["first_name"]
    span = f"{_when(r['week_from'])} to {_when(r['week_to'])}"
    who = name if for_parent else "You"
    if r["study_days"]:
        subject = (f"{name}'s week on Graphite: " if for_parent else "Your Graphite week: ") + \
                  f"{r['study_days']} study day{'s' if r['study_days'] != 1 else ''}, {r['answered']} questions"
    else:
        subject = f"{name}'s week on Graphite" if for_parent else "A 5-minute way back in"
    lines = [f"Hi {'there' if for_parent else name},", ""]
    if for_parent:
        lines.append(f"Here's {name}'s SAT practice on Graphite for {span}.")
    else:
        lines.append(f"Here's your week on Graphite, {span}.")
    lines.append("")
    if r["study_days"]:
        lines.append(f"- Studied on {r['study_days']} of 7 days" + (f", about {r['minutes']} minutes" if r["minutes"] else ""))
        if r["answered"]:
            pct = round(100 * r["right"] / r["answered"])
            lines.append(f"- Answered {r['answered']} questions, {r['right']} right ({pct}%)")
        for t in r["lessons"]:
            lines.append(f"- Finished the lesson \"{t}\"")
        for t in r["topics"]:
            lines.append(f"- Finished every question in {t}")
    else:
        lines.append(f"- No practice this week{'.' if for_parent else '. That happens.'}")
    if r["review_due"]:
        lines.append(f"- {r['review_due']} missed question{'s are' if r['review_due'] != 1 else ' is'} due for review")
    if r["days_to_test"] is not None:
        lines.append(f"- {r['days_to_test']} day{'s' if r['days_to_test'] != 1 else ''} until the SAT")
    lines.append("")
    if for_parent:
        lines.append(f"{who} can pick up with a 5-minute daily warm-up on the dashboard. A few short sessions a week "
                     "do more than one long one.")
    elif r["study_days"]:
        lines.append(f"Keep it going with today's 5-minute warm-up: {base_url}/dashboard.html")
    else:
        lines.append(f"The daily warm-up is 3 questions, about 5 minutes: one review question, one from your weakest topic "
                     f"and one Desmos move. {base_url}/dashboard.html")
    lines += ["", "Graphite", "", "---",
              ("You're getting this because " + name + " added your email for weekly progress updates."
               if for_parent else "You're getting this because weekly progress emails are on in your account."),
              f"Stop these emails: {unsubscribe_url}"]
    return subject, "\n".join(lines)


# ---------- sending ----------

def _serializer():
    return URLSafeSerializer(current_app.config["SECRET_KEY"], salt="weekly-email")


def unsubscribe_token(user_id, who):
    return _serializer().dumps({"u": user_id, "w": who})


def unsubscribe(token):
    """Turns off the weekly email a link was for. Returns 'student' or 'parent', or None for a bad link."""
    try:
        data = _serializer().loads(token)
    except BadSignature:
        return None
    if data.get("w") == "parent":
        execute("UPDATE users SET parent_weekly = 0 WHERE id = ?", (data["u"],))
    elif data.get("w") == "student":
        execute("UPDATE users SET weekly_email = 0 WHERE id = ?", (data["u"],))
    else:
        return None
    return data["w"]


def due_for_weekly(user, today):
    """Whether this student gets this week's email, and why not if they don't."""
    if "@" not in (user["email"] or ""):
        return False, "no email address"
    if (today - date.fromisoformat(user["created_at"][:10])).days < MIN_ACCOUNT_DAYS:
        return False, "new account"
    if user["weekly_sent_at"] and (today - date.fromisoformat(user["weekly_sent_at"][:10])).days < RESEND_GAP_DAYS:
        return False, "already sent this week"
    days = active_days(user["id"]).get(user["id"], set())
    if not days or (today - date.fromisoformat(max(days))).days > INACTIVE_STOP_DAYS:
        return False, "inactive"
    if not user["weekly_email"] and not (user["parent_weekly"] and user["parent_email"]):
        return False, "turned off"
    return True, ""


def send_weekly(today=None, dry_run=False):
    """Sends this week's progress emails. Returns counts, and the list of what was (or would be) sent."""
    today = today or date.today()
    base = current_app.config["BASE_URL"]
    sent, skipped = [], {}
    for user in query("SELECT * FROM users ORDER BY id"):
        ok, why = due_for_weekly(user, today)
        if not ok:
            skipped[why] = skipped.get(why, 0) + 1
            continue
        report = weekly_report(user, today)
        targets = []
        if user["weekly_email"]:
            targets.append((user["email"], "student", False))
        if user["parent_weekly"] and user["parent_email"]:
            targets.append((user["parent_email"], "parent", True))
        for to, who, parent in targets:
            link = f"{base}/api/email/unsubscribe?t={unsubscribe_token(user['id'], who)}"
            subject, text = email_text(report, base, link, for_parent=parent)
            if not dry_run:
                mailer.send(to, subject, text)
            sent.append({"user_id": user["id"], "to": to, "who": who, "subject": subject})
        if not dry_run:
            execute("UPDATE users SET weekly_sent_at = ? WHERE id = ?", (now_iso(), user["id"]))
    return {"sent": len(sent), "skipped": skipped, "emails": sent}

