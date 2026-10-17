"""Daily study reminders: an email at the hour each student picked in Settings, in their own time zone.

Run send_due() once an hour (backend/remind.py does, from a cron job on the host). A student gets at most one
reminder a day, and none on a day they've already studied.
"""
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from flask import current_app

from ..db import execute, query
from . import game, mailer, prefs


def studied_since(user_id, since_utc):
    stamp = since_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    for sql in ("SELECT 1 FROM activity WHERE user_id = ? AND at >= ? LIMIT 1",
                "SELECT 1 FROM practice_seen WHERE user_id = ? AND seen_at >= ? LIMIT 1",
                "SELECT 1 FROM xp_events WHERE user_id = ? AND at >= ? AND xp > 0 LIMIT 1"):
        if query(sql, (user_id, stamp), one=True):
            return True
    return False


def send_due(now=None):
    """Sends the reminders due this hour. Returns how many went out."""
    now = now or datetime.now(timezone.utc)
    sent = 0
    for u in query("SELECT * FROM users WHERE role = 'student' AND prefs LIKE '%\"reminder\": true%'"):
        study = prefs.load(u)["study"]
        if not study["reminder"]:
            continue
        local = now.astimezone(ZoneInfo(study["tz"]))
        if local.hour != study["reminder_hour"] or u["reminder_sent_on"] == local.date().isoformat():
            continue
        midnight = local.replace(hour=0, minute=0, second=0, microsecond=0).astimezone(timezone.utc)
        if studied_since(u["id"], midnight):
            continue
        st = game.streak(u["id"], local.date())
        base = current_app.config["BASE_URL"]
        first = (u["name"] or "").split(" ")[0] or "there"
        keep = (f"You're on a {st['days']}-day streak. Earn any XP today to keep it going.\n\n" if st["days"] else "")
        mailer.send(u["email"], "Your SAT practice for today",
                    f"Hi {first},\n\n{keep}A quick idea: today's speed round takes about two minutes, or pick up where you "
                    f"left off in Level up.\n\n{base}/dashboard.html\n\n"
                    f"You asked for this reminder. Turn it off or change the time in Settings: {base}/settings.html#study\n\nGraphite")
        execute("UPDATE users SET reminder_sent_on = ? WHERE id = ?", (local.date().isoformat(), u["id"]))
        sent += 1
    return sent
