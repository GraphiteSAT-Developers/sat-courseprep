"""The AI tutor (services/tutor.py). Students only; parents are kept out by the request hook in app/__init__.py.

GET  /api/tutor                       whether the tutor is on, the student's credits, and recent conversations
                                      (?item_id= also returns the latest conversation about that question)
POST /api/tutor/message               {conversation_id?, item_id?, message, hint_request?: "nudge"|"method"|"solution",
                                       calculator?: [LaTeX lines], answer?}: the reply, the hint level reached, the
                                      model that answered and the credits left
GET  /api/tutor/conversations/<id>    one conversation, to pick it up again
"""
from flask import Blueprint, jsonify, request

from ..security import ApiError, body, current_user, login_required
from ..services import tutor

bp = Blueprint("tutor", __name__, url_prefix="/api/tutor")


def _student():
    user = current_user()
    if user["role"] == "parent":
        raise ApiError(403, "The tutor is for student accounts.", code="parent_account")
    return user


@bp.get("")
@login_required
def status():
    user = _student()
    out = {"enabled": tutor.enabled(), "credits": tutor.credits(user["id"]) if tutor.enabled() else None,
           "levels": ["nudge", "method", "solution"], "conversations": [], "conversation": None}
    if not out["enabled"]:
        return jsonify(out)
    out["conversations"] = tutor.recent(user["id"])
    item_id = (request.args.get("item_id") or "").strip()
    if item_id:
        conv = tutor.latest_for_item(user["id"], item_id)
        if conv:
            out["conversation"] = tutor.public_conversation(user["id"], conv)
    return jsonify(out)


@bp.post("/message")
@login_required
def message():
    user = _student()
    if not tutor.enabled():
        raise ApiError(503, "The tutor is coming soon.", code="tutor_off")
    try:
        return jsonify(tutor.reply(user, body()))
    except tutor.TutorError as err:
        raise ApiError(err.status, err.message, code=err.code, extra=err.extra)


@bp.get("/conversations/<int:conv_id>")
@login_required
def conversation(conv_id):
    user = _student()
    conv = tutor.get_conversation(user["id"], conv_id)
    if not conv:
        raise ApiError(404, "That conversation isn't there anymore.")
    return jsonify({"conversation": tutor.public_conversation(user["id"], conv), "credits": tutor.credits(user["id"])})
