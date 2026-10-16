"""The Desmos masterclass: each student's progress through the lessons."""
from flask import Blueprint, jsonify

from ..security import ApiError, body, current_user, login_required
from ..services import masterclass

bp = Blueprint("masterclass", __name__, url_prefix="/api/masterclass")


@bp.get("")
@login_required
def overview():
    user_id = current_user()["id"]
    return jsonify({"progress": masterclass.progress(user_id), "summary": masterclass.summary(user_id)})


@bp.post("/progress")
@login_required
def save_progress():
    data = body()
    lesson_id = data.get("lesson")
    if not isinstance(lesson_id, str) or lesson_id not in masterclass.lessons():
        raise ApiError(404, "That lesson doesn't exist.")
    step = data.get("step")
    if not isinstance(step, int) or isinstance(step, bool):
        raise ApiError(400, "Send the step as a whole number.", "step")
    return jsonify({"lesson": lesson_id, "progress": masterclass.save(current_user()["id"], lesson_id, step)})


@bp.post("/quiz")
@login_required
def save_quiz():
    data = body()
    lesson = masterclass.lessons().get(data.get("lesson")) if isinstance(data.get("lesson"), str) else None
    if not lesson or not masterclass.quiz_total(lesson):
        raise ApiError(404, "That lesson doesn't have a quiz.")
    correct = data.get("correct")
    if not isinstance(correct, int) or isinstance(correct, bool) or not 0 <= correct <= masterclass.quiz_total(lesson):
        raise ApiError(400, "Send the number of right answers.", "correct")
    return jsonify({"lesson": lesson["id"], "progress": masterclass.save_quiz(current_user()["id"], lesson["id"], correct)})
