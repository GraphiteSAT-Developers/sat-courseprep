"""Practice from the question bank: random practice tests and topic practice, with no repeats."""
import json
import random

from flask import Blueprint, jsonify, request

from ..security import ApiError, body, current_user, login_required
from ..services import access, bank, levels
from ..services.plans import FREE_LEVELS
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
    section = request.args.get("section", "math")
    if section not in bank.SECTIONS:
        raise ApiError(400, "Pick Math or Reading and Writing.", "section")
    out = service.overview(current_user()["id"], section)
    out["access"] = access.public_state(access.state(current_user()["id"], "practice_set"))
    return jsonify(out)


@bp.post("/sessions")
@login_required
def create():
    data = body()
    mode = data.get("mode")
    user_id = current_user()["id"]
    if mode == "test":
        section = data.get("section", "math")
        if section not in bank.SECTIONS:
            raise ApiError(400, "Pick Math or Reading and Writing.", "section")
        access.require(current_user(), "mock_test")
        session = service.create(user_id, "test", section=section)
    elif mode == "topic":
        domain, skill = data.get("domain"), data.get("skill") or None
        if not isinstance(domain, str) or not service.topic_title(domain, skill if isinstance(skill, str) else None):
            raise ApiError(400, "Pick a topic to practice.", "topic")
        count = data.get("count", 10)
        if count not in service.TOPIC_COUNTS:
            raise ApiError(400, "Pick how many questions you want.", "count")
        access.require(current_user(), "practice_set")
        session = service.create(user_id, "topic", domain, skill, count)
    else:
        raise ApiError(400, "Choose a practice test or a topic.", "mode")
    return jsonify({"session": public(session)}), 201


def public(session):
    """The set for the browser, with explanations swapped for a note when the plan doesn't include them."""
    out = service.public(session)
    uid = current_user()["id"]
    access.redact(uid, list(out["checked"].values()))
    if out.get("result"):
        access.redact(uid, out["result"].get("questions", []))
        _level_lock(out["result"])
    return out


@bp.get("/sessions/<int:session_id>")
@login_required
def get_one(session_id):
    return jsonify({"session": public(_session_or_404(session_id))})


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
    access.redact(current_user()["id"], [graded])
    return jsonify({"question": graded, "finished": finished})


@bp.post("/sessions/<int:session_id>/submit")
@login_required
def submit(session_id):
    session = _session_or_404(session_id)
    if session["submitted_at"]:
        done = json.loads(session["results"])
        access.redact(current_user()["id"], done.get("questions", []))
        return jsonify({"result": _level_lock(done)})
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
    from ..services import mock
    result = mock.after_module(current_user()["id"], session, result)
    access.redact(current_user()["id"], result.get("questions", []))
    return jsonify({"result": _level_lock(result)}), 201


def _level_lock(result):
    """A passed Level up set whose next level the plan doesn't open: the lock to show instead of "unlocked"."""
    lv = result.get("level")
    if lv and lv.get("next") and lv["next"] > FREE_LEVELS:
        st = access.state(current_user()["id"], "level_up")
        if not st["ok"]:
            lv["next_lock"] = dict(access.public_state(st), free_levels=FREE_LEVELS)
    return result


# ---------- the home page's sample question (no sign-in) ----------

sample_bp = Blueprint("sample", __name__, url_prefix="/api/sample")
SAMPLE_DIFFICULTIES = ("easy", "medium")


SAMPLE_LONG = {"cross-text-connections", "command-of-evidence-quantitative"}  # two texts or a table: too long for the home page card


def sample_ok(q):
    return q["type"] == "mc" and q["difficulty"] in SAMPLE_DIFFICULTIES and q["skill_key"] not in SAMPLE_LONG


@sample_bp.get("")
def sample():
    """A random easy or medium multiple-choice question from the bank, without its answer: Math or
    Reading and Writing, half the time each."""
    section = random.choice(list(bank.SECTIONS))
    pool = [q for q in bank.all_items().values() if q["section"] == section and sample_ok(q)]
    return jsonify({"question": bank.public_question(random.choice(pool))})


@sample_bp.post("/check")
def sample_check():
    data = body()
    q = bank.all_items().get(str(data.get("id") or ""))
    if not q or not sample_ok(q):
        raise ApiError(404, "That question isn't available.")
    answer = bank.clean_answer(q, data.get("answer"))
    if answer is None:
        raise ApiError(400, "Choose an answer first.", "answer")
    g = bank.graded_question(q, 0, answer)
    return jsonify({"correct": g["correct"], "answer": g["answer"], "answer_index": g["answer_index"], "explain_html": g["explain_html"]})


# ---------- Level up: sets that get harder one level at a time ----------

levels_bp = Blueprint("levels", __name__, url_prefix="/api/levels")


@levels_bp.get("")
@login_required
def levels_overview():
    out = levels.overview(current_user()["id"])
    out["access"] = access.public_state(access.state(current_user()["id"], "level_up"))
    out["free_levels"] = FREE_LEVELS  # open on every plan; the levels above need level_up
    return jsonify(out)


@levels_bp.post("/start")
@login_required
def levels_start():
    data = body()
    track = data.get("track")
    level = data.get("level")
    if not isinstance(track, str) or not levels.track(track):
        raise ApiError(400, "Pick a track to practice.", "track")
    if not isinstance(level, int) or isinstance(level, bool) or not 1 <= level <= levels.LEVELS:
        raise ApiError(400, "Pick a level.", "level")
    if level > FREE_LEVELS:
        access.require(current_user(), "level_up")
    session = levels.start(current_user()["id"], track, level)
    if not session:
        raise ApiError(403, f"Pass level {level - 1} first to unlock level {level}.", "level")
    return jsonify({"session": public(session)}), 201
