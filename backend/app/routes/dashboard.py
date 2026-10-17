"""Dashboard data, the review queue and practice time."""
from datetime import date, datetime, timezone

from flask import Blueprint, jsonify, request

from ..db import execute, now_iso, query
from ..security import ApiError, body, current_user, login_required, rate_limited, record_event
from ..services import bank, practice, review, today as today_service
from ..services import dashboard as dashboard_service

bp = Blueprint("dashboard", __name__, url_prefix="/api")
ACTIVITY_KINDS = {"practice_question": 300}  # kind: most seconds one entry can log
ACTIVITY_PER_HOUR = 30


@bp.get("/dashboard")
@login_required
def dashboard():
    user = current_user()
    data = dashboard_service.build(user, _local_today())
    # The first visit after a student's first sign-in goes to the diagnostic, once. Skipping it is fine:
    # they aren't sent back, and Today's set offers it until they take it.
    data["start_with_diagnostic"] = False
    if not user["diagnostic_prompted_at"]:
        execute("UPDATE users SET diagnostic_prompted_at = ? WHERE id = ?", (now_iso(), user["id"]))
        started = query("SELECT 1 FROM diagnostics WHERE user_id = ? LIMIT 1", (user["id"],), one=True)
        data["start_with_diagnostic"] = not started
    return jsonify(data)


def _local_today():
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
    return local


@bp.post("/today")
@login_required
def start_today():
    """Today's set: the next task in this week of the study plan, or the weakest domain, or the diagnostic."""
    session = today_service.start(current_user(), _local_today())
    if not session:
        return jsonify({"redirect": "plan.html"})
    return jsonify({"session": practice.public(session)}), 201


@bp.post("/review/<int:item_id>/practice")
@login_required
def review_practice(item_id):
    """Opens a missed question from the question bank again, as a one-question set."""
    user = current_user()
    item = query("SELECT * FROM review_items WHERE id = ? AND user_id = ? AND cleared_at IS NULL", (item_id, user["id"]), one=True)
    if not item:
        raise ApiError(404, "That review question is already cleared.")
    bank_id = item["test_id"][len("bank:"):] if item["test_id"].startswith("bank:") else None
    if not bank_id or bank_id not in bank.all_items():
        raise ApiError(400, "This question can't be reopened. Mark it when you've reworked it.")
    session = practice.save_session(user["id"], "review", f"Review: {item['skill']}", [bank_id], 0, plan_task=f"review:{item_id}")
    return jsonify({"session": practice.public(session)}), 201


@bp.post("/review/<int:item_id>/right")
@login_required
def review_right(item_id):
    state = review.mark_right(current_user()["id"], item_id)
    if not state:
        raise ApiError(404, "That review question is already cleared.")
    return jsonify(state)


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
    bucket = f"activity:{current_user()['id']}"
    if rate_limited(bucket, ACTIVITY_PER_HOUR, 60):  # so practice time can't be padded by sending this over and over
        raise ApiError(429, "That's more practice time than an hour holds. It wasn't logged.")
    record_event(bucket)
    execute("INSERT INTO activity (user_id, kind, seconds, detail, at) VALUES (?, ?, ?, ?, ?)",
            (current_user()["id"], kind, seconds, str(data.get("detail") or "")[:100], now_iso()))
    return jsonify({"ok": True}), 201
