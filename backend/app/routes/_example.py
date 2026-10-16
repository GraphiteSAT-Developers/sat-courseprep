"""Copy this file to start a new feature. It is not switched on.

1. Copy it to app/routes/<feature>.py and rename the blueprint.
2. Add the blueprint to BLUEPRINTS in app/routes/__init__.py.
3. If it needs new tables, add a migration to the end of MIGRATIONS in app/schema.py.
4. Put the logic in app/services/<feature>.py so routes stay short.
5. Add tests in backend/tests/.

Example: a list of flashcard decks for the signed-in student.
"""
from flask import Blueprint, jsonify

from ..db import execute, now_iso, query
from ..security import ApiError, body, clean_text, current_user, login_required

bp = Blueprint("example", __name__, url_prefix="/api/example")


@bp.get("")
@login_required
def list_items():
    # rows = query("SELECT id, title FROM decks WHERE user_id = ?", (current_user()["id"],))
    return jsonify({"items": []})


@bp.post("")
@login_required
def create_item():
    data = body()
    title = clean_text(data.get("title"), 120)
    if not title:
        raise ApiError(400, "Give it a title.", "title")
    # row = execute("INSERT INTO decks (user_id, title, created_at) VALUES (?, ?, ?) RETURNING id",
    #               (current_user()["id"], title, now_iso()))
    return jsonify({"title": title}), 201
