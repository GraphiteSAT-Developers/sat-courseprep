"""History: what each person has done on the site and every question they've answered (services/history.py)."""
import re

from flask import Blueprint, jsonify, request

from ..security import ApiError, body, current_user, login_required
from ..services import history

bp = Blueprint("history", __name__, url_prefix="/api/me/history")
PAGE = re.compile(r"^/[a-z0-9-]{0,40}(\.html)?$")


def _before():
    raw = request.args.get("before")
    if raw is None:
        return None
    if not raw.isdigit():
        raise ApiError(400, "That isn't a page of history.")
    return int(raw)


@bp.get("")
@login_required
def summary():
    return jsonify({"stats": history.stats(current_user()["id"])})


@bp.get("/events")
@login_required
def events():
    return jsonify(history.events(current_user()["id"], _before()))


@bp.get("/questions")
@login_required
def questions():
    return jsonify(history.questions(current_user()["id"], _before()))


@bp.post("/view")
@login_required
def page_view():
    """A page opened while signed in. The request hook saves it (as 'Opened a page'); nothing else to do."""
    page = body().get("page")
    if not isinstance(page, str) or not PAGE.match(page):
        raise ApiError(400, "That isn't a page on the site.", "page")
    return "", 204
