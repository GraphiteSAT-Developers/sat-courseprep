"""The settings page: appearance, profile picture, email, password, devices, data download and account deletion.

Everything is under /api/me so parent accounts can use it too. Changes to email, password and deleting the
account need the current password. The local test accounts (beta, beta2) can't change those or be deleted.
"""
import base64
import binascii
import io
import json
import re
from datetime import datetime, timezone

from flask import Blueprint, Response, current_app, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from .. import testaccount
from ..db import execute, now_iso, query
from ..security import (ApiError, body, clean_email, clean_password, clear_events, current_user, login_required,
                        login_user, logout_user, public_user, rate_limited, record_event)
from ..services import game, mailer

bp = Blueprint("settings", __name__, url_prefix="/api/me")

THEMES = ("dark", "light", "system")
ACCENTS = ("pencil", "sky", "mint", "coral", "lilac")
AVATAR_SIZE = 256              # px, square
AVATAR_MAX_UPLOAD = 6_000_000  # bytes after decoding
AVATAR_MAX_PIXELS = 40_000_000
DATA_URL = re.compile(r"^data:image/(png|jpeg|jpg|webp|gif);base64,([A-Za-z0-9+/=\s]+)$")

# What "Download my data" includes, beyond the account itself. Each is (table, column that holds the user's id).
EXPORT_TABLES = [("test_attempts", "user_id"), ("review_items", "user_id"), ("activity", "user_id"),
                 ("practice_sessions", "user_id"), ("practice_seen", "user_id"), ("practice_completions", "user_id"),
                 ("diagnostics", "user_id"), ("study_plans", "user_id"), ("subscriptions", "student_id"),
                 ("billing_events", "student_id"), ("xp_events", "user_id"), ("badges", "user_id"), ("inventory", "user_id"),
                 ("speed_runs", "user_id"), ("focus_sessions", "user_id"), ("lesson_progress", "user_id")]
NEVER_EXPORTED = {"password_hash", "session_version", "token_hash", "code_hash"}


def _fresh(user_id):
    return query("SELECT * FROM users WHERE id = ?", (user_id,), one=True)


def _block_test_account(user, what):
    if user["email"] in (testaccount.USERNAME, testaccount.PARENT_USERNAME) and current_app.config.get("TEST_ACCOUNT"):
        raise ApiError(403, f"Test accounts can't {what}. Create your own account to try it.", code="test_account")


def _check_password(user, password, field="password"):
    """Confirms the current password, with a limit on wrong guesses."""
    bucket = f"settings-pw:{user['id']}"
    if rate_limited(bucket, 5, 15):
        raise ApiError(429, "Too many wrong passwords. Wait 15 minutes and try again.", field)
    if not password or not check_password_hash(user["password_hash"], password):
        record_event(bucket)
        raise ApiError(400, "That's not your current password.", field, "wrong_password")
    clear_events(bucket)


# ---------- appearance ----------
@bp.patch("/appearance")
@login_required
def appearance():
    data = body()
    fields = {}
    if "theme" in data:
        if data["theme"] not in THEMES:
            raise ApiError(400, "Choose dark, light or match my device.", "theme")
        fields["theme"] = data["theme"]
    if "accent" in data:
        if data["accent"] not in ACCENTS and data["accent"] not in game.SHOP_ACCENTS:
            raise ApiError(400, "Choose one of the accent colors.", "accent")
        if not game.accent_allowed(current_user()["id"], data["accent"]):
            raise ApiError(403, "Buy that color in the shop first.", "accent")
        fields["accent"] = data["accent"]
    if "ripple" in data:
        fields["ripple"] = 1 if data["ripple"] else 0
    if not fields:
        raise ApiError(400, "Nothing to update.")
    user = current_user()
    sets = ", ".join(f"{k} = ?" for k in fields)  # keys come from the fixed list above
    execute(f"UPDATE users SET {sets} WHERE id = ?", (*fields.values(), user["id"]))
    return jsonify({"user": public_user(_fresh(user["id"]))})


# ---------- profile picture ----------
def _process_avatar(data_url):
    """Checks the upload is a real image, then makes a 256px square WebP (JPEG if WebP isn't available)."""
    from PIL import Image, ImageOps, UnidentifiedImageError
    m = DATA_URL.match(data_url or "")
    if not m:
        raise ApiError(400, "Upload a PNG, JPEG, WebP or GIF image.", "image")
    try:
        raw = base64.b64decode(re.sub(r"\s+", "", m.group(2)), validate=True)
    except (binascii.Error, ValueError):
        raise ApiError(400, "That image couldn't be read. Try another file.", "image")
    if len(raw) > AVATAR_MAX_UPLOAD:
        raise ApiError(400, "That image is too large. Use one under 6 MB.", "image")
    Image.MAX_IMAGE_PIXELS = AVATAR_MAX_PIXELS
    try:
        img = Image.open(io.BytesIO(raw))
        if img.format not in ("PNG", "JPEG", "WEBP", "GIF"):
            raise ApiError(400, "Upload a PNG, JPEG, WebP or GIF image.", "image")
        img.seek(0)
        img = ImageOps.exif_transpose(img)
        img = img.convert("RGBA") if img.mode in ("RGBA", "LA", "P") else img.convert("RGB")
    except ApiError:
        raise
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError, ValueError):
        raise ApiError(400, "That image couldn't be read. Try another file.", "image")
    w, h = img.size
    side = min(w, h)
    img = img.crop(((w - side) // 2, (h - side) // 2, (w - side) // 2 + side, (h - side) // 2 + side))
    img = img.resize((AVATAR_SIZE, AVATAR_SIZE), Image.LANCZOS)
    out = io.BytesIO()
    try:
        img.save(out, "WEBP", quality=84, method=4)
        mime = "image/webp"
    except (OSError, KeyError):
        out = io.BytesIO()
        img.convert("RGB").save(out, "JPEG", quality=86, optimize=True)
        mime = "image/jpeg"
    return mime, base64.b64encode(out.getvalue()).decode()


@bp.post("/avatar")
@login_required
def upload_avatar():
    user = current_user()
    bucket = f"avatar:{user['id']}"
    if rate_limited(bucket, 20, 60):
        raise ApiError(429, "You've changed your photo a lot this hour. Try again later.")
    mime, data = _process_avatar(body().get("image"))
    record_event(bucket)
    if query("SELECT 1 FROM avatars WHERE user_id = ?", (user["id"],), one=True):
        execute("UPDATE avatars SET mime = ?, data = ?, updated_at = ? WHERE user_id = ?", (mime, data, now_iso(), user["id"]))
    else:
        execute("INSERT INTO avatars (user_id, mime, data, updated_at) VALUES (?, ?, ?, ?)", (user["id"], mime, data, now_iso()))
    execute("UPDATE users SET avatar_version = avatar_version + 1 WHERE id = ?", (user["id"],))
    return jsonify({"user": public_user(_fresh(user["id"]))}), 201


@bp.delete("/avatar")
@login_required
def remove_avatar():
    user = current_user()
    execute("DELETE FROM avatars WHERE user_id = ?", (user["id"],))
    execute("UPDATE users SET avatar_version = 0 WHERE id = ?", (user["id"],))
    return jsonify({"user": public_user(_fresh(user["id"]))})


@bp.get("/avatar")
@login_required
def get_avatar():
    row = query("SELECT mime, data FROM avatars WHERE user_id = ?", (current_user()["id"],), one=True)
    if not row:
        raise ApiError(404, "No profile picture.")
    return Response(base64.b64decode(row["data"]), mimetype=row["mime"],
                    headers={"Cache-Control": "private, max-age=86400"})


# ---------- sign-in and security ----------
@bp.post("/email")
@login_required
def change_email():
    user = current_user()
    _block_test_account(user, "change their email")
    data = body()
    email = clean_email(data.get("email"))
    if email == user["email"]:
        raise ApiError(400, "That's already your email.", "email")
    _check_password(user, data.get("password"))
    if query("SELECT 1 FROM users WHERE email = ?", (email,), one=True):
        raise ApiError(409, "Another account already uses that email.", "email", "email_taken")
    old = user["email"]
    execute("UPDATE users SET email = ? WHERE id = ?", (email, user["id"]))
    mailer.send(old, "Your Graphite email was changed",
                f"Hi {user['name'].split(' ')[0]},\n\nThe email on your Graphite account was changed to {email}. "
                "If you didn't do this, reply to this email right away.\n\nGraphite")
    mailer.send(email, "Your Graphite email is updated",
                f"Hi {user['name'].split(' ')[0]},\n\nYou'll sign in to Graphite with this email from now on.\n\nGraphite")
    return jsonify({"user": public_user(_fresh(user["id"]))})


@bp.post("/password")
@login_required
def change_password():
    user = current_user()
    _block_test_account(user, "change their password")
    data = body()
    _check_password(user, data.get("current_password"), "current_password")
    new = clean_password(data.get("new_password"), "new_password")
    if check_password_hash(user["password_hash"], new):
        raise ApiError(400, "Choose a password you haven't been using.", "new_password")
    execute("UPDATE users SET password_hash = ?, session_version = session_version + 1 WHERE id = ?",
            (generate_password_hash(new), user["id"]))
    login_user(_fresh(user["id"]), remember=True)  # stay signed in here; other devices are signed out
    mailer.send(user["email"], "Your Graphite password was changed",
                f"Hi {user['name'].split(' ')[0]},\n\nYour Graphite password was just changed, and other devices were "
                "signed out. If you didn't do this, reset your password from the sign-in page.\n\nGraphite")
    return jsonify({"user": public_user(_fresh(user["id"]))})


@bp.post("/sign-out-others")
@login_required
def sign_out_others():
    user = current_user()
    execute("UPDATE users SET session_version = session_version + 1 WHERE id = ?", (user["id"],))
    login_user(_fresh(user["id"]), remember=True)
    return jsonify({"ok": True})


# ---------- your data ----------
def _rows(table, column, user_id):
    rows = query(f"SELECT * FROM {table} WHERE {column} = ?", (user_id,))  # names come from EXPORT_TABLES
    out = []
    for r in rows:
        clean = {}
        for k, v in r.items():
            if k in NEVER_EXPORTED:
                continue
            if isinstance(v, str) and v[:1] in "[{":
                try:
                    v = json.loads(v)
                except ValueError:
                    pass
            clean[k] = v
        out.append(clean)
    return out


@bp.get("/export")
@login_required
def export():
    user = current_user()
    links = query("SELECT u.name, u.email, u.role FROM family_links f JOIN users u "
                  "ON u.id = CASE WHEN f.parent_id = ? THEN f.student_id ELSE f.parent_id END "
                  "WHERE f.parent_id = ? OR f.student_id = ?", (user["id"], user["id"], user["id"]))
    data = {"exported_at": now_iso(), "account": public_user(user), "connected_accounts": links}
    for table, column in EXPORT_TABLES:
        data[table] = _rows(table, column, user["id"])
    data["account"].pop("avatar_url", None)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return Response(json.dumps(data, indent=2, default=str), mimetype="application/json",
                    headers={"Content-Disposition": f'attachment; filename="graphite-data-{stamp}.json"'})


@bp.post("/delete")
@login_required
def delete_account():
    user = current_user()
    _block_test_account(user, "be deleted")
    data = body()
    if str(data.get("confirm") or "").strip().upper() != "DELETE":
        raise ApiError(400, 'Type DELETE to confirm.', "confirm")
    _check_password(user, data.get("password"))
    email, first = user["email"], user["name"].split(" ")[0]
    # study_plans points at diagnostics, so it goes first; everything else is removed with the account.
    execute("DELETE FROM study_plans WHERE user_id = ?", (user["id"],))
    execute("DELETE FROM users WHERE id = ?", (user["id"],))
    logout_user()
    mailer.send(email, "Your Graphite account was deleted",
                f"Hi {first},\n\nYour Graphite account and its practice history were deleted. "
                "Thanks for studying with us.\n\nGraphite")
    return jsonify({"ok": True})
