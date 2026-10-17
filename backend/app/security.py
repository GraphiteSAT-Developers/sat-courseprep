"""Sign-in sessions, request checks, rate limits and input validation."""
import hashlib
import re
from datetime import timedelta
from functools import wraps
from urllib.parse import urlparse

from flask import current_app, g, jsonify, request, session

from .db import execute, iso, now, query

EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]{2,}$")


class ApiError(Exception):
    """Raise anywhere in a route to send a JSON error: raise ApiError(400, "Message", field="email")."""

    def __init__(self, status, message, field=None, code=None):
        super().__init__(message)
        self.status, self.message, self.field, self.code = status, message, field, code


def error_response(err):
    body = {"error": err.message}
    if err.field:
        body["field"] = err.field
    if err.code:
        body["code"] = err.code
    return jsonify(body), err.status


# ---------- sessions ----------
def login_user(user, remember=False):
    session.clear()
    session["uid"] = user["id"]
    session["sv"] = user["session_version"]
    session.permanent = bool(remember)
    execute("UPDATE users SET last_login_at = ? WHERE id = ?", (iso(now()), user["id"]))


def logout_user():
    session.clear()


def current_user():
    if "user" in g:
        return g.user
    g.user = None
    uid = session.get("uid")
    if uid:
        user = query("SELECT * FROM users WHERE id = ?", (uid,), one=True)
        if user and user["session_version"] == session.get("sv"):
            g.user = user
        else:
            session.clear()
    return g.user


def login_required(view):
    """For API routes. Returns 401 JSON when nobody is signed in."""
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not current_user():
            raise ApiError(401, "Please sign in to continue.", code="signed_out")
        return view(*args, **kwargs)
    return wrapper


def public_user(user):
    """The account fields that are safe to send to the browser."""
    return {
        "id": user["id"], "email": user["email"], "name": user["name"],
        "first_name": (user["name"] or "").split(" ")[0],
        "grade": user["grade"], "test_date": user["test_date"], "target_score": user["target_score"],
        "plan": user["plan"], "weekly_goal_hours": user["weekly_goal_hours"], "parent_email": user["parent_email"],
        "role": user["role"] if "role" in user.keys() else "student",
        "created_at": user["created_at"],
    }


# ---------- request checks ----------
def check_same_origin():
    """Blocks cross-site form posts (CSRF). Writes must come from this site, as JSON."""
    if request.method in ("GET", "HEAD", "OPTIONS"):
        return
    if not request.is_json:
        raise ApiError(415, "Send this request as JSON.")
    source = request.headers.get("Origin") or request.headers.get("Referer")
    if not source:
        raise ApiError(403, "This request is missing its origin.")
    src, here = urlparse(source), urlparse(request.host_url)
    if (src.scheme, src.netloc) != (here.scheme, here.netloc):
        raise ApiError(403, "Requests must come from this site.")


def client_ip():
    return request.access_route[0] if request.access_route else (request.remote_addr or "unknown")


def hash_text(text):
    return hashlib.sha256(text.encode()).hexdigest()


def rate_limited(bucket, limit, window_minutes):
    """True when this bucket already has `limit` events inside the window."""
    since = iso(now() - timedelta(minutes=window_minutes))
    row = query("SELECT COUNT(*) AS n FROM rate_events WHERE bucket = ? AND at > ?", (bucket, since), one=True)
    return row["n"] >= limit


def record_event(bucket):
    execute("INSERT INTO rate_events (bucket, at) VALUES (?, ?)", (bucket, iso(now())))


def clear_events(bucket):
    execute("DELETE FROM rate_events WHERE bucket = ?", (bucket,))


def prune_events():
    """Delete rate-limit records older than a day. Called now and then."""
    execute("DELETE FROM rate_events WHERE at < ?", (iso(now() - timedelta(days=1)),))


# ---------- validation ----------
def body():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ApiError(400, "Send a JSON object.")
    return data


def clean_email(value, field="email", required=True):
    value = (value or "").strip().lower()
    if not value:
        if required:
            raise ApiError(400, "Enter an email address.", field)
        return None
    if len(value) > 254 or not EMAIL_RE.match(value):
        raise ApiError(400, "Enter an email like name@school.org.", field)
    return value


def clean_name(value, field="name"):
    value = " ".join((value or "").split())
    if not value:
        raise ApiError(400, "Enter a name.", field)
    if len(value) > 80:
        raise ApiError(400, "Names can be up to 80 characters.", field)
    return value


def clean_password(value, field="password"):
    value = value or ""
    if len(value) < 8:
        raise ApiError(400, "Passwords need at least 8 characters.", field)
    if len(value) > 200:
        raise ApiError(400, "Passwords can be up to 200 characters.", field)
    return value


def clean_grade(value, field="grade"):
    if value in (None, ""):
        return None
    try:
        grade = int(value)
    except (TypeError, ValueError):
        raise ApiError(400, "Choose a grade from 9 to 12.", field)
    if grade not in (9, 10, 11, 12):
        raise ApiError(400, "Choose a grade from 9 to 12.", field)
    return grade


def clean_target(value, field="target_score"):
    if value in (None, ""):
        return None
    try:
        score = int(value)
    except (TypeError, ValueError):
        raise ApiError(400, "Target scores are whole numbers from 400 to 1600.", field)
    if not 400 <= score <= 1600:
        raise ApiError(400, "Target scores run from 400 to 1600.", field)
    if score % 10:
        raise ApiError(400, "SAT totals move in steps of 10.", field)
    return score


def clean_date(value, field="test_date"):
    """Accepts YYYY-MM-DD or YYYY-MM (the signup form's month picker). Returns YYYY-MM-DD or None."""
    value = (value or "").strip()
    if not value or value == "not-registered":
        return None
    if re.match(r"^\d{4}-\d{2}$", value):
        value += "-01"
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", value):
        raise ApiError(400, "Use a date like 2026-12-05.", field)
    return value


def clean_text(value, limit=2000):
    value = (value or "").strip()
    return value[:limit] or None
