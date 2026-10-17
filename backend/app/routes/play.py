"""Rewards, speed rounds and leaderboards, the focus timer, and active recall lessons."""
from flask import Blueprint, jsonify, request

from ..security import ApiError, body, current_user, login_required
from ..services import focus, game, lessons, speed


def _student():
    user = current_user()
    if user["role"] == "parent":
        raise ApiError(403, "This is for student accounts.")
    return user


def _fresh_user():
    from ..db import query
    return query("SELECT * FROM users WHERE id = ?", (current_user()["id"],), one=True)


def _int(value, field, message):
    if not isinstance(value, int) or isinstance(value, bool):
        raise ApiError(400, message, field)
    return value


# ---------- rewards: XP, coins, badges, shop ----------
game_bp = Blueprint("game", __name__, url_prefix="/api/game")


@game_bp.get("")
@login_required
def game_profile():
    return jsonify(game.profile(_student()))


@game_bp.get("/summary")
@login_required
def game_summary():
    return jsonify(game.summary(_student()["id"]))


@game_bp.post("/buy")
@login_required
def game_buy():
    user = _student()
    key = body().get("item")
    try:
        rep = game.buy(user["id"], key if isinstance(key, str) else "")
    except ValueError as err:
        raise ApiError(400, str(err), "item")
    return jsonify({"reward": rep, "profile": game.profile(_fresh_user())})


@game_bp.post("/equip")
@login_required
def game_equip():
    user = _student()
    data = body()
    kind, value = data.get("kind"), data.get("value")
    if value is not None and not isinstance(value, str):
        raise ApiError(400, "Pick something to wear.", "value")
    try:
        game.equip(user["id"], kind, value)
    except ValueError as err:
        raise ApiError(400, str(err), "value")
    return jsonify({"profile": game.profile(_fresh_user())})


# ---------- speed rounds and leaderboards ----------
speed_bp = Blueprint("speed", __name__, url_prefix="/api/speed")


@speed_bp.get("")
@login_required
def speed_overview():
    return jsonify(speed.overview(_student()))


@speed_bp.post("/start")
@login_required
def speed_start():
    user = _student()
    return jsonify({"run": speed.public(speed.start(user))}), 201


def _run(run_id):
    run = speed.get(current_user()["id"], run_id)
    if not run:
        raise ApiError(404, "That speed round doesn't exist.")
    return run


@speed_bp.get("/runs/<int:run_id>")
@login_required
def speed_get(run_id):
    return jsonify({"run": speed.public(_run(run_id))})


@speed_bp.post("/runs/<int:run_id>/answer")
@login_required
def speed_answer(run_id):
    run = _run(run_id)
    if run["finished_ms"] is not None:
        raise ApiError(409, "This round is already over.")
    data = body()
    from ..services import bank
    import json
    ids = json.loads(run["item_ids"])
    i = data.get("index")
    if not isinstance(i, int) or isinstance(i, bool) or not 0 <= i < len(ids):
        raise ApiError(400, "That question isn't in this round.")
    value = bank.clean_answer(bank.all_items()[ids[i]], data.get("answer"))
    if value is None:
        raise ApiError(400, "Choose an answer.", "answer")
    graded, run, rep = speed.answer(current_user()["id"], run, i, value)
    out = {"answer": graded, "finished": run["finished_ms"] is not None}
    if out["finished"]:
        out["result"] = speed.result_of(run)
        out["reward"] = rep
    return jsonify(out)


@speed_bp.post("/runs/<int:run_id>/finish")
@login_required
def speed_finish(run_id):
    run, rep = speed.finish(current_user()["id"], _run(run_id))
    return jsonify({"result": speed.result_of(run), "reward": rep})


@speed_bp.get("/board")
@login_required
def speed_board():
    scope = request.args.get("scope", "state")
    period = request.args.get("period", "today")
    if scope not in ("state", "nation") or period not in ("today", "week"):
        raise ApiError(400, "Pick a leaderboard.")
    return jsonify(speed.board(_student(), scope, period))


@speed_bp.get("/nicknames")
@login_required
def speed_nicknames():
    return jsonify({"nicknames": speed.roll_nicknames(4)})


@speed_bp.patch("/profile")
@login_required
def speed_profile():
    """Leaderboard settings: on or off, the nickname (from the word lists) and the state."""
    from ..db import execute, query, set_clause
    user = _student()
    data = body()
    fields = {}
    if "state" in data:
        if data["state"] is not None and data["state"] not in speed.STATE_NAMES:
            raise ApiError(400, "Pick your state.", "state")
        fields["state"] = data["state"]
    if "nickname" in data:
        try:
            fields["nickname"] = speed.clean_nickname(data["nickname"], user)
        except ValueError as err:
            raise ApiError(400, str(err), "nickname")
    if "opt_in" in data:
        fields["board_opt_in"] = 1 if data["opt_in"] else 0
    if not fields:
        raise ApiError(400, "Nothing to update.")
    nickname = fields.get("nickname", user["nickname"])
    if fields.get("board_opt_in") and not nickname:
        raise ApiError(400, "Pick a nickname to show on the leaderboard.", "nickname")
    sets = set_clause(fields)  # keys come from the fixed names above
    execute(f"UPDATE users SET {sets} WHERE id = ?", (*fields.values(), user["id"]))
    fresh = query("SELECT * FROM users WHERE id = ?", (user["id"],), one=True)
    return jsonify({"board_profile": speed.overview(fresh)["board_profile"]})


@speed_bp.get("/states")
def speed_states():
    return jsonify({"states": [{"code": c, "name": n} for c, n in speed.STATES]})


# ---------- focus timer ----------
focus_bp = Blueprint("focus", __name__, url_prefix="/api/focus")


@focus_bp.get("")
@login_required
def focus_overview():
    return jsonify(focus.overview(_student()))


@focus_bp.post("/start")
@login_required
def focus_start():
    user = _student()
    data = body()
    minutes = data.get("minutes")
    if minutes not in focus.LENGTHS or isinstance(minutes, bool):
        raise ApiError(400, "Pick how long to focus.", "minutes")
    label = data.get("label")
    if label not in focus.LABELS:
        raise ApiError(400, "Pick what you're working on.", "label")
    return jsonify({"session": focus.public(focus.start(user["id"], minutes, label))}), 201


@focus_bp.post("/<int:sid>/finish")
@login_required
def focus_finish(sid):
    user = _student()
    row = focus.get(user["id"], sid)
    if not row:
        raise ApiError(404, "That focus session doesn't exist.")
    row, rep = focus.finish(user["id"], row, completed=bool(body().get("completed")))
    return jsonify({"session": focus.public(row), "reward": rep, "overview": focus.overview(current_user())})


# ---------- lessons ----------
lessons_bp = Blueprint("lessons", __name__, url_prefix="/api/lessons")


@lessons_bp.get("")
@login_required
def lessons_overview():
    return jsonify(lessons.overview(_student()["id"]))


@lessons_bp.get("/<lesson_id>")
@login_required
def lessons_get(lesson_id):
    user = _student()
    l = lessons.lesson(lesson_id)
    if not l:
        raise ApiError(404, "That lesson doesn't exist.")
    from ..db import query
    row = query("SELECT * FROM lesson_progress WHERE user_id = ? AND lesson_id = ?", (user["id"], lesson_id), one=True)
    return jsonify({"lesson": lessons.public(l, row)})


@lessons_bp.post("/<lesson_id>/complete")
@login_required
def lessons_complete(lesson_id):
    user = _student()
    if not lessons.lesson(lesson_id):
        raise ApiError(404, "That lesson doesn't exist.")
    data = body()
    kind = data.get("kind", "lesson")
    if kind not in ("lesson", "recall"):
        raise ApiError(400, "Finish a lesson or a recall check.", "kind")
    try:
        out = lessons.complete(user["id"], lesson_id, kind, data.get("answers"))
    except ValueError as err:
        raise ApiError(400, str(err))
    return jsonify(out)
