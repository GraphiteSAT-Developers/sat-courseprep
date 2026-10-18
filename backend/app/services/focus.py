"""Focus timer: timed study sessions that count toward the weekly study goal and the daily streak.

The server keeps the clock. A session is credited with the time that really passed, up to its length, and
counts as finished when nearly all of it ran. Time spent on practice sets and the review queue already
counts from those sets, so focus sessions labeled that way earn XP but don't add study time a second time.
"""
import time
from datetime import date, datetime, timedelta, timezone

from ..db import execute, local_day, now_iso, query
from . import game

LENGTHS = (15, 25, 50)
BREAKS = {15: 3, 25: 5, 50: 10}
LABELS = {"practice": "Practice sets", "review": "Review queue", "lesson": "A lesson", "notes": "My own notes",
          "reading": "Reading and Writing", "other": "Something else"}
COUNTED_ELSEWHERE = {"practice", "review"}  # those sets already log their own time
FINISH_SHARE = 0.95   # this much of the session has to have passed for it to count as finished
MIN_CREDIT = 60       # seconds; shorter sessions aren't logged


def now_ms():
    return int(time.time() * 1000)


def _open(user_id):
    return query("SELECT * FROM focus_sessions WHERE user_id = ? AND finished_at IS NULL ORDER BY id DESC LIMIT 1",
                 (user_id,), one=True)


def public(row, t=None):
    t = t or now_ms()
    return {"id": row["id"], "minutes": row["minutes"], "label": row["label"], "label_name": LABELS.get(row["label"], row["label"]),
            "elapsed_ms": t - row["started_ms"], "finished": row["finished_at"] is not None,
            "completed": bool(row["completed"]), "seconds": row["seconds"], "break_minutes": BREAKS.get(row["minutes"], 5)}


def start(user_id, minutes, label):
    """Starts a session. An unfinished one is ended first (with the time it really ran)."""
    old = _open(user_id)
    if old:
        finish(user_id, old, completed=False)
    row = execute("INSERT INTO focus_sessions (user_id, minutes, label, started_ms, created_at) VALUES (?, ?, ?, ?, ?) RETURNING id",
                  (user_id, minutes, label, now_ms(), now_iso()))
    return query("SELECT * FROM focus_sessions WHERE id = ?", (row["id"],), one=True)


def get(user_id, sid):
    return query("SELECT * FROM focus_sessions WHERE id = ? AND user_id = ?", (sid, user_id), one=True)


def finish(user_id, row, completed=True):
    """Ends a session. Returns (row, rewards report or None)."""
    if row["finished_at"]:
        return row, None
    planned = row["minutes"] * 60 * 1000
    elapsed = now_ms() - row["started_ms"]
    done = bool(completed) and elapsed >= planned * FINISH_SHARE
    seconds = int(min(elapsed, planned) // 1000)
    execute("UPDATE focus_sessions SET finished_at = ?, seconds = ?, completed = ? WHERE id = ?",
            (now_iso(), seconds, 1 if done else 0, row["id"]))
    if seconds >= MIN_CREDIT and row["label"] not in COUNTED_ELSEWHERE:
        execute("INSERT INTO activity (user_id, kind, seconds, detail, at) VALUES (?, 'focus', ?, ?, ?)",
                (user_id, seconds, f"focus-{row['id']}", now_iso()))
    row = get(user_id, row["id"])
    if seconds < MIN_CREDIT:
        return row, None
    xp_before, _ = game.totals(user_id)
    minutes = seconds // 60
    xp = game.XP_FOCUS_MINUTE * minutes if done else game.XP_FOCUS_MINUTE * minutes // 2
    coins = game.COINS_FOCUS_DONE if done else 0
    s = game.award(user_id, "focus", xp, coins, f"focus-{row['id']}")
    badges = []
    if done:
        badges.append(game.earn_badge(user_id, "deep_focus"))
        n = query("SELECT COUNT(*) AS n FROM focus_sessions WHERE user_id = ? AND completed = 1", (user_id,), one=True)["n"]
        if n >= 10:
            badges.append(game.earn_badge(user_id, "in_the_zone"))
    return row, game.report(user_id, xp_before, xp, coins, badges, s, {"completed": done, "seconds": seconds})


def overview(user, today=None):
    today = today or date.today()
    uid = user["id"]
    monday = today - timedelta(days=today.weekday())
    since = datetime.combine(monday, datetime.min.time(), tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    week_all = query("SELECT COALESCE(SUM(seconds), 0) AS s FROM activity WHERE user_id = ? AND at >= ?", (uid, since), one=True)["s"]
    rows = query("SELECT * FROM focus_sessions WHERE user_id = ? AND finished_at IS NOT NULL AND created_at >= ? ORDER BY id DESC",
                 (uid, since))
    days = [0] * 7
    for r in rows:
        i = (local_day(r["created_at"]) - monday).days
        if 0 <= i < 7:
            days[i] += r["seconds"] or 0
    open_row = _open(uid)
    if open_row and now_ms() - open_row["started_ms"] > open_row["minutes"] * 60 * 1000 * 3:
        finish(uid, open_row, completed=False)  # left running for hours: close it with the time it was planned for
        open_row = None
    total_done = query("SELECT COUNT(*) AS n FROM focus_sessions WHERE user_id = ? AND completed = 1", (uid,), one=True)["n"]
    return {
        "lengths": [{"minutes": m, "break": BREAKS[m]} for m in LENGTHS],
        "labels": [{"key": k, "name": v} for k, v in LABELS.items()],
        "counted_elsewhere": sorted(COUNTED_ELSEWHERE),
        "goal_hours": user["weekly_goal_hours"], "week_seconds": int(week_all),
        "week_focus_seconds": sum(days), "week_days": days, "today_focus_seconds": days[today.weekday()],
        "sessions_done": total_done,
        "recent": [public(r) for r in rows if (r["seconds"] or 0) >= MIN_CREDIT][:6],
        "open": public(open_row) if open_row else None,
        "streak": game.streak(uid),
    }
