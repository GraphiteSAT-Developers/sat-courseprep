"""The signed-in student's own account."""
from flask import Blueprint, jsonify

from ..db import execute, query
from ..security import (ApiError, body, clean_date, clean_email, clean_grade, clean_name, clean_target,
                        current_user, login_required, public_user)

bp = Blueprint("account", __name__, url_prefix="/api")


@bp.get("/me")
@login_required
def me():
    return jsonify({"user": public_user(current_user())})


@bp.patch("/me")
@login_required
def update_me():
    data = body()
    user = current_user()
    fields = {}
    if "name" in data:
        fields["name"] = clean_name(data["name"])
    if "grade" in data:
        fields["grade"] = clean_grade(data["grade"])
    if "test_date" in data:
        fields["test_date"] = clean_date(data["test_date"])
    if "target_score" in data:
        fields["target_score"] = clean_target(data["target_score"])
    if "parent_email" in data:
        fields["parent_email"] = clean_email(data["parent_email"], "parent_email", required=False)
    if "weekly_goal_hours" in data:
        try:
            hours = int(data["weekly_goal_hours"])
        except (TypeError, ValueError):
            hours = 0
        if not 1 <= hours <= 20:
            raise ApiError(400, "Weekly goals run from 1 to 20 hours.", "weekly_goal_hours")
        fields["weekly_goal_hours"] = hours
    if not fields:
        raise ApiError(400, "Nothing to update.")
    sets = ", ".join(f"{k} = ?" for k in fields)  # keys come from the fixed list above, never from the request
    execute(f"UPDATE users SET {sets} WHERE id = ?", (*fields.values(), user["id"]))
    fresh = query("SELECT * FROM users WHERE id = ?", (user["id"],), one=True)
    return jsonify({"user": public_user(fresh)})
