"""Practice tests: list them, load questions without answers, and submit for grading."""
import json

from flask import Blueprint, jsonify

from ..db import days_from_today, execute, now_iso, query
from ..security import ApiError, body, current_user, login_required
from ..services.content import all_tests, get_test, public_test, summary
from ..services.grading import clean_answers, grade

bp = Blueprint("tests", __name__, url_prefix="/api/tests")

MAX_SECONDS_SLACK = 120  # allow for network delay past the time limit


def _test_or_404(test_id):
    test = get_test(test_id)
    if not test:
        raise ApiError(404, "That practice test doesn't exist.")
    return test


@bp.get("")
@login_required
def list_tests():
    return jsonify({"tests": [summary(t) for t in all_tests().values()]})


@bp.get("/<test_id>")
@login_required
def get_one(test_id):
    return jsonify({"test": public_test(_test_or_404(test_id))})


@bp.post("/<test_id>/attempts")
@login_required
def submit(test_id):
    test = _test_or_404(test_id)
    data = body()
    user = current_user()
    answers = clean_answers(data.get("answers"), test)
    try:
        seconds = int(data.get("seconds_used") or 0)
    except (TypeError, ValueError):
        seconds = 0
    seconds = max(0, min(seconds, test["minutes"] * 60 + MAX_SECONDS_SLACK))
    result = grade(test, answers)
    result["seconds_used"] = seconds
    stamp = now_iso()
    row = execute(
        "INSERT INTO test_attempts (user_id, test_id, seconds_used, correct, total, answers, results, submitted_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?) RETURNING id",
        (user["id"], test_id, seconds, result["correct"], result["total"], json.dumps(answers), json.dumps(result), stamp))
    result["attempt_id"] = row["id"]
    result["submitted_at"] = stamp

    # Every miss goes into the review queue (or back into it, if it was cleared before).
    for q in result["questions"]:
        if q["correct"]:
            continue
        execute(
            "INSERT INTO review_items (user_id, test_id, question_index, domain, skill, right_count, due_on, created_at) "
            "VALUES (?, ?, ?, ?, ?, 0, ?, ?) "
            "ON CONFLICT (user_id, test_id, question_index) DO UPDATE SET right_count = 0, cleared_at = NULL, due_on = excluded.due_on",
            (user["id"], test_id, q["index"], q["domain"], q.get("skill") or q["domain"], days_from_today(0), stamp))
    execute("INSERT INTO activity (user_id, kind, seconds, detail, at) VALUES (?, 'practice_test', ?, ?, ?)",
            (user["id"], seconds, test_id, stamp))
    return jsonify({"result": result}), 201


@bp.get("/<test_id>/attempts")
@login_required
def attempts(test_id):
    _test_or_404(test_id)
    rows = query("SELECT id, seconds_used, correct, total, submitted_at FROM test_attempts "
                 "WHERE user_id = ? AND test_id = ? ORDER BY submitted_at DESC", (current_user()["id"], test_id))
    return jsonify({"attempts": rows})


@bp.get("/<test_id>/attempts/<int:attempt_id>")
@login_required
def attempt_detail(test_id, attempt_id):
    row = query("SELECT results FROM test_attempts WHERE id = ? AND user_id = ? AND test_id = ?",
                (attempt_id, current_user()["id"], test_id), one=True)
    if not row:
        raise ApiError(404, "That attempt doesn't exist.")
    return jsonify({"result": json.loads(row["results"])})
