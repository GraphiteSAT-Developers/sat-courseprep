"""The /admin page's data: home page signups and accounts. Only for ADMIN_ACCOUNTS (app/admins.py)."""
from flask import Blueprint, abort, jsonify

from .. import admins, crypto
from ..db import query
from ..security import current_user, login_required
from ..services.plans import PLANS, key_for

bp = Blueprint("admin", __name__, url_prefix="/api/admin")
LIMIT = 500  # newest first; the counts cover everything


@bp.get("")
@login_required
def overview():
    if not admins.is_admin(current_user()):
        abort(404)  # the same answer as a page that doesn't exist
    leads = [dict(r, message=crypto.unseal(r["message"])) for r in query(
        "SELECT id, name, email, grade, test_date, target_score, message, created_at FROM leads ORDER BY id DESC LIMIT ?", (LIMIT,))]
    students = query(
        "SELECT u.id, u.name, u.email, u.grade, u.test_date, u.target_score, u.created_at, "
        "COALESCE(s.plan, 'free') AS plan, COALESCE(s.status, 'active') AS status "
        "FROM users u LEFT JOIN subscriptions s ON s.student_id = u.id WHERE u.role = 'student' ORDER BY u.id DESC LIMIT ?", (LIMIT,))
    parents = query("SELECT id, name, email, created_at FROM users WHERE role = 'parent' ORDER BY id DESC LIMIT ?", (LIMIT,))
    for s in students:
        s["plan_name"] = PLANS.get(key_for(s["plan"]), {}).get("name", s["plan"])
    count = lambda sql: query(sql, one=True)["n"]
    return jsonify({
        "counts": {"leads": count("SELECT COUNT(*) AS n FROM leads"),
                   "students": count("SELECT COUNT(*) AS n FROM users WHERE role = 'student'"),
                   "parents": count("SELECT COUNT(*) AS n FROM users WHERE role = 'parent'")},
        "leads": leads, "students": students, "parents": parents, "limit": LIMIT,
    })
