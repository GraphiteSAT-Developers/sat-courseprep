"""The AI tutor: whether it's connected, and asking it a question. Answers come from Qwen (services/qwen.py)."""
from flask import Blueprint, jsonify

from ..security import ApiError, body, current_user, login_required, rate_limited, record_event
from ..services import access, qwen, tutor

bp = Blueprint("tutor", __name__, url_prefix="/api/tutor")


def _student():
    user = current_user()
    if user["role"] == "parent":
        raise ApiError(403, "The tutor is for student accounts.")
    return user


@bp.get("")
@login_required
def status():
    user = _student()
    return jsonify({"connected": qwen.is_live(), "lock": access.public_state(access.state(user["id"], "tutor"))})


@bp.post("/chat")
@login_required
def chat():
    user = _student()
    if not qwen.is_live():
        raise ApiError(503, "The tutor isn't connected yet.", code="tutor_offline")
    data = body()
    messages = tutor.conversation(data.get("messages"), data.get("context"))  # checks the request before any limit
    access.require(user, "tutor")
    bucket = f"tutor:{user['id']}"
    if rate_limited(bucket, tutor.PER_MINUTE, 1):
        raise ApiError(429, "That's a lot of questions at once. Give it a minute.", code="rate_limited")
    try:
        reply = qwen.chat(messages)
    except qwen.QwenError as err:
        raise ApiError(502, str(err), code="tutor_error") from err
    record_event(bucket)  # only answered questions count toward the day's limit
    return jsonify({"reply": reply, "lock": access.public_state(access.state(user["id"], "tutor"))})
