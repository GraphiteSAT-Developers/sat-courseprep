"""The home page's "Get your free diagnostic link" form."""
from flask import Blueprint, current_app, jsonify

from ..db import execute, now_iso
from ..security import (ApiError, body, clean_date, clean_email, clean_grade, clean_name, clean_target, clean_text,
                        client_ip, rate_limited, record_event)
from ..services import mailer

bp = Blueprint("leads", __name__, url_prefix="/api")


@bp.post("/leads")
def create_lead():
    data = body()
    if data.get("company"):  # hidden honeypot field: people never fill it, bots do
        return jsonify({"ok": True})
    bucket = "lead-ip:" + client_ip()
    if rate_limited(bucket, 5, 10):
        raise ApiError(429, "You've sent this form several times in ten minutes. Wait a bit, or email us directly.")
    name = clean_name(data.get("name"))
    email = clean_email(data.get("email"))
    grade = clean_grade(data.get("grade"))
    if grade is None:
        raise ApiError(400, "Choose a grade.", "grade")
    if not data.get("agree"):
        raise ApiError(400, "Check the box to agree to the terms.", "agree")
    test_date = clean_date(data.get("test_date"))
    target = clean_target(data.get("target"), "target")
    message = clean_text(data.get("message"))
    record_event(bucket)
    execute("INSERT INTO leads (name, email, grade, test_date, target_score, message, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name, email, grade, test_date, target, message, now_iso()))
    base = current_app.config["BASE_URL"]
    mailer.send(email, "Your free Graphite diagnostic",
                f"Hi {name.split(' ')[0]},\n\nCreate your free account here, then take the 10-question diagnostic. "
                f"It takes about 15 minutes and builds your study plan:\n{base}/signin.html#create\n\nGraphite")
    admin = current_app.config["ADMIN_EMAIL"]
    if admin:
        mailer.send(admin, f"New diagnostic signup: {name}",
                    f"{name} <{email}>, grade {grade}, test date {test_date or 'not set'}, target {target or 'not set'}.\n\n{message or ''}")
    return jsonify({"ok": True}), 201
