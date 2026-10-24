"""Copy warnings: copying a question, or pasting into one, is noticed.

The first time a student copies text from a question (or pastes into an answer), the page warns them:
doing it again emails their parent. From then on each time is recorded, and every parent linked to the
account gets an email, at most once every EMAIL_GAP_MINUTES so a burst of copies sends one email.
Students without a linked parent see that it was recorded on their account.

Every event is saved (integrity_events), shown to linked parents as an alert, and included in the
student's data export. The terms and privacy policy say so.
"""
from datetime import datetime, timedelta, timezone

from flask import current_app

from ..db import execute, now_iso, query
from . import family, mailer

KINDS = ("copy", "cut", "paste")
PAGES = {"practice-test": "a practice set", "mock-test": "a practice test", "speed": "the speed round", "plan": "the diagnostic or a study plan quiz",
         "dashboard": "today's set", "lessons": "a lesson", "levels": "Practice Sets"}
EMAIL_GAP_MINUTES = 30


def count(user_id):
    return query("SELECT COUNT(*) AS n FROM integrity_events WHERE user_id = ?", (user_id,), one=True)["n"]


def _recent_email(user_id):
    since = (datetime.now(timezone.utc) - timedelta(minutes=EMAIL_GAP_MINUTES)).strftime("%Y-%m-%dT%H:%M:%SZ")
    return query("SELECT 1 FROM integrity_events WHERE user_id = ? AND action = 'parent_emailed' AND at >= ? LIMIT 1",
                 (user_id, since), one=True) is not None


def record(student, kind, page, item_id, chars):
    """Saves one event and does what it calls for. Returns {action, parents, count}."""
    first = count(student["id"]) == 0
    parents = family.parents_of(student["id"])
    if first:
        action = "warned"
    elif parents and not _recent_email(student["id"]):
        action = "parent_emailed"
    else:
        action = "recorded"
    execute("INSERT INTO integrity_events (user_id, kind, page, item_id, chars, action, at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (student["id"], kind, page, item_id, chars, action, now_iso()))
    if action == "parent_emailed":
        name = student["name"].split(" ")[0]
        where = PAGES.get(page, "a practice question")
        did = {"copy": "copied text from", "cut": "copied text from", "paste": "pasted text into"}[kind]
        for p in parents:
            mailer.send(p["email"], f"{name} copied a question on Graphite SAT",
                        f"Hi {p['name'].split(' ')[0]},\n\n"
                        f"{name} {did} a question in {where} on Graphite SAT. The first time it happened, the page warned "
                        f"{name} that doing it again would email you, so we're letting you know.\n\n"
                        "Copying a question usually means pasting it into another app, such as an AI chatbot, instead of "
                        "working it out. It may be worth a quick conversation. You can see every time it happened on your "
                        f"parent dashboard:\n{current_app.config['BASE_URL']}/parent.html\n\nGraphite SAT")
    return {"action": action, "parents": len(parents), "count": count(student["id"])}


def recent(user_id, days=7):
    since = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    return query("SELECT kind, page, action, at FROM integrity_events WHERE user_id = ? AND at >= ? ORDER BY at DESC",
                 (user_id, since))
