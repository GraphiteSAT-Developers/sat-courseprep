"""Everything a signed-in person does on the site, saved to their account.

Two logs:
- user_events: every change made through the API (sign-ins, profile and settings changes, practice, rewards,
  market trades, pages opened), with what was sent and which account fields changed. One row per request,
  written by the request hooks in app/__init__.py, so a new route is logged without extra code.
- question_log: every question answered anywhere (practice, Level up, practice tests, the diagnostic,
  speed rounds, lessons and recall checks), with the answer and whether it was right.

Privacy
- Passwords, tokens, codes and photos are never logged (REDACT), and secret account columns are never
  compared (NEVER_DIFF).
- The details are encrypted at rest (crypto.seal), like the other sensitive fields.
- Both logs belong to the account: they're in the data export (Settings > Your data), the student can read them
  in Settings > History, and they're deleted with the account.
"""
import json
import re

from flask import g, request, session

from .. import crypto
from ..db import execute, get_db, now_iso, query, today

REDACT = re.compile(r"pass|token|secret|code|turnstile|card|photo|image|file|signature", re.I)
NEVER_DIFF = {"password_hash", "session_version", "stripe_customer_id", "photo", "avatar", "market_seq",
              "reminder_sent_on", "diagnostic_prompted_at"}
SKIP = {"settings.delete_account", "stripe_webhook.webhook", "sample.sample_check", "leads.create_lead", "auth.forgot"}
MAX_TEXT = 300
MAX_DETAIL = 8000
PAGE = 40

LABELS = {
    "auth.register": "Created the account", "auth.login": "Signed in", "auth.logout": "Signed out",
    "auth.reset": "Reset the password", "account.update_me": "Updated the profile",
    "tests.submit": "Finished a practice test", "practice.create": "Started a practice set",
    "practice.check": "Checked an answer", "practice.submit": "Finished a practice set",
    "plan.start_diagnostic": "Started the diagnostic", "plan.submit_diagnostic": "Finished the diagnostic",
    "plan.rebuild": "Rebuilt the study plan", "plan.start_task": "Started a plan task",
    "levels.levels_start": "Started a Level up set", "dashboard.start_today": "Started today's practice",
    "dashboard.review_practice": "Practiced a review question", "dashboard.review_right": "Cleared a review question",
    "dashboard.log_activity": "Logged study time", "family.make_code": "Made a parent link code",
    "family.remove_parent": "Removed a parent", "parent.link_student": "Linked a student",
    "parent.unlink_student": "Unlinked a student", "parent.update_settings": "Changed a student's settings",
    "parent.change_plan": "Changed a student's plan", "parent.plan_action": "Changed a subscription",
    "parent.billing_portal": "Opened billing", "parent.send_report": "Sent a progress report",
    "settings.appearance": "Changed the look", "settings.patch_prefs": "Changed preferences",
    "settings.upload_avatar": "Uploaded a profile picture", "settings.remove_avatar": "Removed the profile picture",
    "settings.change_email": "Changed the email", "settings.change_password": "Changed the password",
    "settings.sign_out_others": "Signed out other devices", "settings.reset_test_account": "Reset the test account",
    "checkout.start": "Started checkout", "game.game_buy": "Bought from the shop", "game.game_equip": "Changed what's worn",
    "speed.speed_start": "Started a speed round", "speed.speed_answer": "Answered in a speed round",
    "speed.speed_finish": "Finished a speed round", "speed.speed_profile": "Changed leaderboard settings",
    "focus.focus_start": "Started a focus session", "focus.focus_finish": "Finished a focus session",
    "lessons.lessons_complete": "Finished a lesson", "market.market_trade": "Traded on the market",
    "history.page_view": "Opened a page",
}


# ---------- request hooks ----------
def _snapshot(user):
    if not user:
        return None
    return {k: v for k, v in dict(user).items() if k not in NEVER_DIFF}


def before(user):
    """Remembers who is making a change and what their account looked like (call for API writes)."""
    g.history_uid = user["id"] if user else None
    g.history_before = _snapshot(user)


def _clean(value, key="", depth=0):
    if key and REDACT.search(key):
        return "[not saved]"
    if depth > 4:
        return "…"
    if isinstance(value, dict):
        return {str(k)[:60]: _clean(v, str(k), depth + 1) for k, v in list(value.items())[:60]}
    if isinstance(value, list):
        return [_clean(v, key, depth + 1) for v in value[:60]]
    if isinstance(value, str):
        return value if len(value) <= MAX_TEXT else value[:MAX_TEXT] + "…"
    return value


def _value(v):
    v = crypto.unseal(v)
    if isinstance(v, str) and v[:1] in "[{":
        try:
            return json.loads(v)
        except ValueError:
            return v
    return v


def _diff(before_row, after_row):
    if not before_row or not after_row:
        return {}
    out = {}
    for k, old in before_row.items():
        if k in NEVER_DIFF or k not in after_row:
            continue
        new = after_row[k]
        if old != new:
            a, b = _value(old), _value(new)
            if isinstance(a, dict) and isinstance(b, dict):  # prefs: only the parts that changed
                changed = {s: {"from": a.get(s), "to": b.get(s)} for s in set(a) | set(b) if a.get(s) != b.get(s)}
                out[k] = _clean(changed)
            else:
                out[k] = {"from": _clean(a, k), "to": _clean(b, k)}
    return out


def after(resp):
    """Saves one user_events row for an API write. Never breaks the response."""
    endpoint = request.endpoint or ""
    if endpoint in SKIP or not endpoint:
        return
    try:
        uid = g.get("history_uid") or session.get("uid")
        if not uid:
            return
        row = query("SELECT * FROM users WHERE id = ?", (uid,), one=True)
        if not row:
            return  # the account is gone
        sent = request.get_json(silent=True)
        detail = {"sent": _clean(sent) if isinstance(sent, dict) else {}, "changes": _diff(g.get("history_before"), row)}
        if request.view_args:
            detail["ids"] = _clean(request.view_args)
        if resp.status_code >= 400:
            try:
                detail["error"] = (resp.get_json(silent=True) or {}).get("error")
            except Exception:
                pass
        text = json.dumps(detail, separators=(",", ":"), default=str)
        if len(text) > MAX_DETAIL:
            detail.pop("sent", None)
            detail["trimmed"] = True
            text = json.dumps(detail, separators=(",", ":"), default=str)[:MAX_DETAIL]
        execute("INSERT INTO user_events (user_id, kind, action, status, detail, day, at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (uid, endpoint, f"{request.method} {request.url_rule.rule if request.url_rule else request.path}",
                 resp.status_code, crypto.seal(text), today().isoformat(), now_iso()))
    except Exception as err:  # logging must never cost the student their change
        try:
            get_db().rollback()
        except Exception:
            pass
        from flask import current_app
        current_app.logger.warning("History not saved for %s: %s", endpoint, err)


# ---------- questions ----------
def question(user_id, item_id, source, ref, answer, correct):
    """One answered question. answer is what the student gave (as sent); correct is True, False or None."""
    if answer is None or answer == "":
        return
    execute("INSERT INTO question_log (user_id, item_id, source, ref, answer, correct, day, at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (user_id, str(item_id)[:120], source, str(ref)[:80] if ref is not None else None, str(answer)[:MAX_TEXT],
             None if correct is None else (1 if correct else 0), today().isoformat(), now_iso()))


SOURCES = {"practice": "Topic practice", "level": "Level up", "practice_test": "Practice test", "test": "Practice test",
           "diagnostic": "Diagnostic", "speed": "Speed round", "lesson": "Lesson", "recall": "Recall check",
           "review": "Review"}


# ---------- reading it back ----------
def _event_out(r):
    try:
        detail = json.loads(crypto.unseal(r["detail"]) or "{}")
    except (ValueError, TypeError):
        detail = {}
    return {"id": r["id"], "kind": r["kind"], "label": LABELS.get(r["kind"], r["kind"]), "action": r["action"],
            "ok": r["status"] < 400, "status": r["status"], "at": r["at"], "detail": detail}


def events(user_id, before_id=None, limit=PAGE):
    rows = query("SELECT * FROM user_events WHERE user_id = ? AND (? IS NULL OR id < ?) ORDER BY id DESC LIMIT ?",
                 (user_id, before_id, before_id, limit + 1))
    return {"items": [_event_out(r) for r in rows[:limit]], "more": len(rows) > limit}


def questions(user_id, before_id=None, limit=PAGE):
    from . import bank
    items = bank.all_items()
    rows = query("SELECT * FROM question_log WHERE user_id = ? AND (? IS NULL OR id < ?) ORDER BY id DESC LIMIT ?",
                 (user_id, before_id, before_id, limit + 1))
    out = []
    for r in rows[:limit]:
        q = items.get(r["item_id"])
        out.append({"id": r["id"], "item_id": r["item_id"], "source": r["source"], "source_name": SOURCES.get(r["source"], r["source"]),
                    "answer": r["answer"], "correct": None if r["correct"] is None else bool(r["correct"]), "at": r["at"],
                    "skill": q["skill"] if q else None, "domain": q["domain"] if q else None})
    return {"items": out, "more": len(rows) > limit}


def stats(user_id):
    rows = query("SELECT source, COUNT(*) AS n, COALESCE(SUM(correct), 0) AS r FROM question_log WHERE user_id = ? GROUP BY source",
                 (user_id,))
    distinct = query("SELECT COUNT(DISTINCT item_id) AS n FROM question_log WHERE user_id = ?", (user_id,), one=True)["n"]
    ev = query("SELECT COUNT(*) AS n, MIN(at) AS first FROM user_events WHERE user_id = ?", (user_id,), one=True)
    total = sum(int(r["n"]) for r in rows)
    right = sum(int(r["r"]) for r in rows)
    return {"answered": total, "right": right, "different_questions": distinct, "events": ev["n"], "since": ev["first"],
            "by_source": [{"source": r["source"], "name": SOURCES.get(r["source"], r["source"]), "answered": int(r["n"]),
                           "right": int(r["r"])} for r in rows]}
