"""Practice from the question bank: random practice tests and topic practice, with no repeats."""
import json
import random

from flask import Blueprint, jsonify

from ..security import ApiError, body, current_user, login_required
from ..services import bank
from ..services import practice as service

bp = Blueprint("practice", __name__, url_prefix="/api/practice")

MAX_SECONDS_SLACK = 120  # allow for network delay past the time limit
TOPIC_SECONDS_PER_QUESTION = 600  # the most time one untimed question can log


def _session_or_404(session_id):
    session = service.get(current_user()["id"], session_id)
    if not session:
        raise ApiError(404, "That practice set doesn't exist.")
    return session


@bp.get("")
@login_required
def overview():
    return jsonify(service.overview(current_user()["id"]))


@bp.post("/sessions")
@login_required
def create():
    data = body()
    mode = data.get("mode")
    user_id = current_user()["id"]
    if mode == "test":
        session = service.create(user_id, "test")
    elif mode == "topic":
        domain, skill = data.get("domain"), data.get("skill") or None
        if not isinstance(domain, str) or not service.topic_title(domain, skill if isinstance(skill, str) else None):
            raise ApiError(400, "Pick a topic to practice.", "topic")
        count = data.get("count", 10)
        if count not in service.TOPIC_COUNTS:
            raise ApiError(400, "Pick how many questions you want.", "count")
        session = service.create(user_id, "topic", domain, skill, count)
    else:
        raise ApiError(400, "Choose a practice test or a topic.", "mode")
    return jsonify({"session": service.public(session)}), 201


@bp.get("/sessions/<int:session_id>")
@login_required
def get_one(session_id):
    return jsonify({"session": service.public(_session_or_404(session_id))})


def _index(session, value):
    try:
        i = int(value)
    except (TypeError, ValueError):
        raise ApiError(400, "That question isn't in this set.")
    if not 0 <= i < len(json.loads(session["item_ids"])):
        raise ApiError(400, "That question isn't in this set.")
    return i


@bp.post("/sessions/<int:session_id>/check")
@login_required
def check(session_id):
    session = _session_or_404(session_id)
    if session["mode"] not in ("topic", "quiz", "review"):
        raise ApiError(400, "Answers on a practice test are checked when you submit it.")
    if session["submitted_at"]:
        raise ApiError(409, "This set is already finished.")
    data = body()
    i = _index(session, data.get("index"))
    q = bank.all_items()[json.loads(session["item_ids"])[i]]
    answer = bank.clean_answer(q, data.get("answer"))
    if answer is None:
        raise ApiError(400, "Choose or type an answer first.", "answer")
    graded, finished = service.check(current_user()["id"], session, i, answer)
    return jsonify({"question": graded, "finished": finished})


@bp.post("/sessions/<int:session_id>/submit")
@login_required
def submit(session_id):
    session = _session_or_404(session_id)
    if session["submitted_at"]:
        return jsonify({"result": json.loads(session["results"])})
    data = body()
    ids = json.loads(session["item_ids"])
    items = bank.all_items()
    answers = {}
    raw = data.get("answers")
    if isinstance(raw, dict):
        for key, value in raw.items():
            try:
                i = int(key)
            except (TypeError, ValueError):
                continue
            if 0 <= i < len(ids):
                cleaned = bank.clean_answer(items[ids[i]], value)
                if cleaned is not None:
                    answers[i] = cleaned
    try:
        seconds = int(data.get("seconds_used") or 0)
    except (TypeError, ValueError):
        seconds = 0
    limit = session["minutes"] * 60 + MAX_SECONDS_SLACK if session["minutes"] else len(ids) * TOPIC_SECONDS_PER_QUESTION
    seconds = max(0, min(seconds, limit))
    result = service.submit(current_user()["id"], session, answers, seconds)
    return jsonify({"result": result}), 201


# ---------- the home page's sample question (no sign-in) ----------

sample_bp = Blueprint("sample", __name__, url_prefix="/api/sample")
SAMPLE_DIFFICULTIES = ("easy", "medium")


@sample_bp.get("")
def sample():
    """A random easy or medium multiple-choice question from the bank, without its answer."""
    pool = [q for q in bank.all_items().values() if q["type"] == "mc" and q["difficulty"] in SAMPLE_DIFFICULTIES]
    return jsonify({"question": bank.public_question(random.choice(pool))})


@sample_bp.post("/check")
def sample_check():
    data = body()
    q = bank.all_items().get(str(data.get("id") or ""))
    if not q or q["type"] != "mc" or q["difficulty"] not in SAMPLE_DIFFICULTIES:
        raise ApiError(404, "That question isn't available.")
    answer = bank.clean_answer(q, data.get("answer"))
    if answer is None:
        raise ApiError(400, "Choose an answer first.", "answer")
    g = bank.graded_question(q, 0, answer)
    return jsonify({"correct": g["correct"], "answer": g["answer"], "answer_index": g["answer_index"], "explain_html": g["explain_html"]})
