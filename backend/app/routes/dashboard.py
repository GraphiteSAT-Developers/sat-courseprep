"""Dashboard data, the review queue and practice time."""
from datetime import date, datetime, timezone

from flask import Blueprint, jsonify, request

from ..db import days_from_today, execute, now_iso, query
from ..security import ApiError, body, current_user, login_required
from ..services import dashboard as dashboard_service

bp = Blueprint("dashboard", __name__, url_prefix="/api")

REVIEW_GAP_DAYS = 3
ACTIVITY_KINDS = {"practice_question": 300}  # kind: most seconds one entry can log


@bp.get("/dashboard")
@login_required
def dashboard():
    # The browser sends its own date (?today=YYYY-MM-DD) so due dates and countdowns follow the
    # student's time zone, not the server's. Accepted only within a day of the server's date.
    local = None
    try:
        local = date.fromisoformat(request.args.get("today", ""))
    except ValueError:
        pass
    server_today = datetime.now(timezone.utc).date()
    if local is None or abs((local - server_today).days) > 1:
        local = server_today
    return jsonify(dashboard_service.build(current_user(), local))


@bp.post("/review/<int:item_id>/right")
@login_required
def review_right(item_id):
    user = current_user()
    item = query("SELECT * FROM review_items WHERE id = ? AND user_id = ? AND cleared_at IS NULL", (item_id, user["id"]), one=True)
    if not item:
        raise ApiError(404, "That review question is already cleared.")
    count = item["right_count"] + 1
    if count >= 2:
        execute("UPDATE review_items SET right_count = ?, cleared_at = ? WHERE id = ?", (count, now_iso(), item_id))
        return jsonify({"id": item_id, "right_count": count, "cleared": True})
    due = days_from_today(REVIEW_GAP_DAYS)
    execute("UPDATE review_items SET right_count = ?, due_on = ? WHERE id = ?", (count, due, item_id))
    return jsonify({"id": item_id, "right_count": count, "cleared": False, "due_on": due})


@bp.post("/activity")
@login_required
def log_activity():
    data = body()
    kind = data.get("kind")
    if kind not in ACTIVITY_KINDS:
        raise ApiError(400, "Unknown activity.")
    try:
        seconds = int(data.get("seconds") or 0)
    except (TypeError, ValueError):
        seconds = 0
    seconds = max(0, min(seconds, ACTIVITY_KINDS[kind]))
    execute("INSERT INTO activity (user_id, kind, seconds, detail, at) VALUES (?, ?, ?, ?, ?)",
            (current_user()["id"], kind, seconds, str(data.get("detail") or "")[:100], now_iso()))
    return jsonify({"ok": True}), 201
