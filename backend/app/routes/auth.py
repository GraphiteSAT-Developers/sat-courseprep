"""Create account, sign in, sign out, forgot password and reset password."""
import secrets
from datetime import timedelta

from flask import Blueprint, current_app, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from ..db import execute, iso, now, now_iso, parse_iso, query
from ..security import (ApiError, body, clean_date, clean_email, clean_grade, clean_name, clean_password,
                        clean_target, clear_events, client_ip, hash_text, login_user, logout_user, public_user,
                        rate_limited, record_event)
from ..services import mailer

bp = Blueprint("auth", __name__, url_prefix="/api/auth")

# Compared against when an email has no account, so a wrong email takes as long as a wrong password.
_DUMMY_HASH = generate_password_hash("not-a-real-password")
RESET_MINUTES = 30


@bp.post("/register")
def register():
    data = body()
    ip_bucket = "register-ip:" + client_ip()
    if rate_limited(ip_bucket, 10, 60):
        raise ApiError(429, "Too many new accounts from this network. Try again in an hour.")
    name = clean_name(data.get("name"))
    email = clean_email(data.get("email"))
    password = clean_password(data.get("password"))
    grade = clean_grade(data.get("grade"))
    test_date = clean_date(data.get("test_date"))
    target = clean_target(data.get("target_score"))
    if query("SELECT id FROM users WHERE email = ?", (email,), one=True):
        raise ApiError(409, "An account with this email already exists. Sign in instead.", "email", "email_taken")
    record_event(ip_bucket)
    row = execute(
        "INSERT INTO users (email, password_hash, name, grade, test_date, target_score, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?) RETURNING id",
        (email, generate_password_hash(password), name, grade, test_date, target, now_iso()))
    user = query("SELECT * FROM users WHERE id = ?", (row["id"],), one=True)
    login_user(user, remember=True)
    mailer.send(email, "Welcome to Graphite",
                f"Hi {user['name'].split(' ')[0]},\n\nYour Graphite account is ready. Start with practice test 4 "
                f"to build your study plan:\n{current_app.config['BASE_URL']}/practice-test.html\n\nGraphite")
    return jsonify({"user": public_user(user)}), 201


@bp.post("/login")
def login():
    data = body()
    email = clean_email(data.get("email"))
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
    login_user(user, remember=bool(data.get("remember")))
    return jsonify({"user": public_user(user)})


@bp.post("/logout")
def logout():
    logout_user()
    return jsonify({"ok": True})


@bp.post("/forgot")
def forgot():
    data = body()
    email = clean_email(data.get("email"))
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
        mailer.send(email, "Reset your Graphite password",
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
