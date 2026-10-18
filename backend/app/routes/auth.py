"""Create account, sign in, sign out, forgot password and reset password."""
import secrets
from datetime import timedelta

from flask import Blueprint, current_app, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from .. import botcheck, testaccount
from ..db import execute, iso, now, now_iso, parse_iso, query
from ..security import (ApiError, body, clean_date, clean_email, clean_grade, clean_name, clean_password,
                        clean_target, clear_events, client_ip, hash_text, login_user, logout_user, public_user,
                        rate_limited, record_event)
from ..services import mailer

bp = Blueprint("auth", __name__, url_prefix="/api/auth")

# Compared against when an email has no account, so a wrong email takes as long as a wrong password.
_DUMMY_HASH = generate_password_hash("not-a-real-password")
RESET_MINUTES = 30


@bp.get("/form-token")
def form_token():
    """A signed, timestamped token for the sign-up, reset and home page forms (bot protection, app/botcheck.py)."""
    return jsonify({"token": botcheck.new_token(), "turnstile_site_key": current_app.config.get("TURNSTILE_SITE_KEY") or None})


@bp.post("/register")
def register():
    data = body()
    botcheck.check(data)
    ip_bucket = "register-ip:" + client_ip()
    if rate_limited(ip_bucket, 10, 60):
        raise ApiError(429, "Too many new accounts from this network. Try again in an hour.")
    role = data.get("role") or "student"
    if role not in ("student", "parent"):
        raise ApiError(400, "Choose a student or parent account.", "role")
    name = clean_name(data.get("name"))
    email = clean_email(data.get("email"))
    password = clean_password(data.get("password"))
    student = role == "student"  # parent accounts don't have a grade, test date or target
    grade = clean_grade(data.get("grade")) if student else None
    test_date = clean_date(data.get("test_date")) if student else None
    target = clean_target(data.get("target_score")) if student else None
    if query("SELECT id FROM users WHERE email = ?", (email,), one=True):
        raise ApiError(409, "An account with this email already exists. Sign in instead.", "email", "email_taken")
    record_event(ip_bucket)
    row = execute(
        "INSERT INTO users (email, password_hash, name, grade, test_date, target_score, role, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?) RETURNING id",
        (email, generate_password_hash(password), name, grade, test_date, target, role, now_iso()))
    user = query("SELECT * FROM users WHERE id = ?", (row["id"],), one=True)
    login_user(user, remember=True)
    if not student:
        mailer.send(email, "Welcome to Graphite SAT",
                    f"Hi {user['name'].split(' ')[0]},\n\nYour parent account is ready. To see your student's progress, "
                    f"ask them to open Account, then Parent access, on their Graphite SAT dashboard and send you the code. "
                    f"Enter it here:\n{current_app.config['BASE_URL']}/parent.html\n\nGraphite SAT")
        return jsonify({"user": public_user(user)}), 201
    mailer.send(email, "Welcome to Graphite SAT",
                f"Hi {user['name'].split(' ')[0]},\n\nYour Graphite SAT account is ready. Start with the 10-question diagnostic "
                f"to build your study plan:\n{current_app.config['BASE_URL']}/plan.html\n\nGraphite SAT")
    return jsonify({"user": public_user(user)}), 201


@bp.post("/login")
def login():
    data = body()
    if testaccount.is_test_login(current_app, data.get("email")):
        email = str(data.get("email")).strip().lower()
    else:
        email = clean_email(data.get("email"), new=False)
    password = data.get("password") or ""
    email_bucket, ip_bucket = "login:" + email, "login-ip:" + client_ip()
    if rate_limited(email_bucket, 5, 15) or rate_limited(ip_bucket, 30, 15):
        raise ApiError(429, "Too many sign-in attempts. Wait 15 minutes, or reset your password.", code="rate_limited")
    user = query("SELECT * FROM users WHERE email = ?", (email,), one=True)
    ok = check_password_hash(user["password_hash"] if user else _DUMMY_HASH, password)
    if not user or not ok:
        record_event(email_bucket)
        record_event(ip_bucket)
        raise ApiError(401, "That email and password don't match.", code="bad_credentials")
    clear_events(email_bucket)
    # "I'm a student" / "I'm a parent" on the sign-in page has to match the account.
    role = data.get("role")
    if role in ("student", "parent") and role != user["role"]:
        if user["role"] == "parent":
            raise ApiError(403, "That's a parent account. Choose \"I'm a parent\" above to sign in.", code="wrong_role")
        raise ApiError(403, "That's a student account. Choose \"I'm a student\" to sign in, or create a parent account "
                            "to follow a student's progress.", code="wrong_role")
    if email == testaccount.USERNAME and current_app.config.get("TEST_ACCOUNT") and not testaccount.was_set_up(user["id"]):
        # The first sign-in sets the test account up. After that its progress is saved like any account's;
        # Settings > Your data has a button to start it over.
        testaccount.reset(user["id"])
        user = query("SELECT * FROM users WHERE id = ?", (user["id"],), one=True)
    login_user(user, remember=bool(data.get("remember")))
    return jsonify({"user": public_user(user)})


@bp.post("/logout")
def logout():
    logout_user()
    return jsonify({"ok": True})


@bp.post("/forgot")
def forgot():
    data = body()
    botcheck.check(data)
    email = clean_email(data.get("email"), new=False)
    bucket = "reset:" + email
    if rate_limited(bucket, 3, 15):
        raise ApiError(429, "Reset links are limited to three every 15 minutes. Check your inbox and spam folder.")
    record_event(bucket)
    user = query("SELECT id, name FROM users WHERE email = ?", (email,), one=True)
    if user:
        token = secrets.token_urlsafe(32)
        execute("INSERT INTO password_resets (user_id, token_hash, expires_at) VALUES (?, ?, ?)",
                (user["id"], hash_text(token), iso(now() + timedelta(minutes=RESET_MINUTES))))
        link = f"{current_app.config['BASE_URL']}/signin.html?reset={token}"
        mailer.send(email, "Reset your Graphite SAT password",
                    f"Hi {user['name'].split(' ')[0]},\n\nChoose a new password here. The link works for "
                    f"{RESET_MINUTES} minutes:\n{link}\n\nIf you didn't ask for this, you can ignore this email.")
    # Same answer whether or not the account exists, so this can't be used to look up emails.
    return jsonify({"ok": True})


@bp.post("/reset")
def reset():
    data = body()
    token = str(data.get("token") or "")
    password = clean_password(data.get("password"))
    row = query("SELECT * FROM password_resets WHERE token_hash = ?", (hash_text(token),), one=True)
    if not row or row["used_at"] or parse_iso(row["expires_at"]) < now():
        raise ApiError(400, "This reset link has expired or was already used. Ask for a new one.", code="bad_token")
    execute("UPDATE users SET password_hash = ?, session_version = session_version + 1 WHERE id = ?",
            (generate_password_hash(password), row["user_id"]))
    execute("UPDATE password_resets SET used_at = ? WHERE user_id = ? AND used_at IS NULL", (now_iso(), row["user_id"]))
    user = query("SELECT * FROM users WHERE id = ?", (row["user_id"],), one=True)
    clear_events("login:" + user["email"])
    login_user(user)
    return jsonify({"user": public_user(user)})
