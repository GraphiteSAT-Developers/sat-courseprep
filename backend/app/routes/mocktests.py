"""Mock tests: a full SAT section in two adaptive modules, with the test-day break (services/mock.py).

GET  /api/mock-tests                the sections, this month's allowance, and recent mock tests
POST /api/mock-tests                start one: {section: "math", with_break: true}
GET  /api/mock-tests/<id>           one mock test
POST /api/mock-tests/<id>/break     {action: "start" | "end"}: the 10-minute break before Math
"""
from flask import Blueprint, jsonify

from ..security import ApiError, body, current_user, login_required
from ..services import access, mock

bp = Blueprint("mocktests", __name__, url_prefix="/api/mock-tests")


def _mock_or_404(mock_id):
    m = mock.get(current_user()["id"], mock_id)
    if not m:
        raise ApiError(404, "That mock test doesn't exist.")
    return m


@bp.get("")
@login_required
def overview():
    user = current_user()
    out = mock.overview(user["id"])
    out["access"] = access.public_state(access.state(user["id"], "mock_test"))
    return jsonify(out)


@bp.post("")
@login_required
def create():
    user = current_user()
    data = body()
    section = data.get("section", "math")
    if section not in mock.SECTIONS:
        raise ApiError(400, "Pick Math or Reading and Writing.", "section")
    if not mock.SECTIONS[section]["ready"]:
        raise ApiError(409, f"{mock.SECTIONS[section]['name']} mock tests are coming soon.", code="coming_soon")
    access.require(user, "mock_test")
    m = mock.create(user["id"], section, data.get("with_break", True) is not False)
    return jsonify({"mock": mock.public(m)}), 201


@bp.get("/<int:mock_id>")
@login_required
def get_one(mock_id):
    return jsonify({"mock": mock.public(_mock_or_404(mock_id))})


@bp.post("/<int:mock_id>/break")
@login_required
def take_break(mock_id):
    m = _mock_or_404(mock_id)
    action = body().get("action")
    if action not in ("start", "end"):
        raise ApiError(400, "Start or end the break.", "action")
    return jsonify({"mock": mock.public(mock.break_action(current_user()["id"], m, action))})
