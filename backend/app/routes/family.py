"""Students and parents: the student's Parent access card, and everything on the parent dashboard."""
from datetime import date

from flask import Blueprint, current_app, jsonify

from ..db import execute, query
from ..security import (ApiError, body, clean_date, clean_target, current_user, login_required, rate_limited,
                        record_event)
from ..services import family, mailer, parent as service

# ---------- the student's side: make a code, see and remove parents ----------

student_bp = Blueprint("family", __name__, url_prefix="/api/family")


@student_bp.get("")
@login_required
def parents():
    me = current_user()
    return jsonify({"parents": [{"id": p["id"], "name": p["name"], "email": p["email"], "since": p["created_at"]}
                                for p in family.parents_of(me["id"])],
                    "code_expires_at": family.pending_code(me["id"])})


@student_bp.post("/code")
@login_required
def make_code():
    me = current_user()
    bucket = f"family-code:{me['id']}"
    if rate_limited(bucket, 10, 60):
        raise ApiError(429, "That's a lot of codes. Try again in an hour.")
    record_event(bucket)
    return jsonify(family.new_code(me["id"])), 201


@student_bp.delete("/parents/<int:parent_id>")
@login_required
def remove_parent(parent_id):
    family.unlink(parent_id, current_user()["id"])
    return jsonify({"ok": True})


# ---------- the parent dashboard ----------

bp = Blueprint("parent", __name__, url_prefix="/api/parent")


def _student_or_404(student_id):
    link = family.link(current_user()["id"], student_id)
    if not link:
        raise ApiError(404, "That student isn't connected to your account.")
    return query("SELECT * FROM users WHERE id = ?", (student_id,), one=True), link


def _plans():
    from ..services.plans import public_plans
    return public_plans()


@bp.get("")
@login_required
def home():
    me = current_user()
    return jsonify({"parent": {"name": me["name"], "email": me["email"]},
                    "students": [{"id": s["id"], "name": s["name"]} for s in family.students_of(me["id"])],
                    "plans": _plans(), "payments_live": service.PAYMENTS_LIVE, "alert_days": list(service.ALERT_DAYS)})


@bp.post("/link")
@login_required
def link_student():
    me = current_user()
    bucket = f"family-link:{me['id']}"
    if rate_limited(bucket, 10, 60):
        raise ApiError(429, "Too many tries. Wait an hour, or ask your student for a new code.")
    code = family.clean_code(body().get("code"))
    if not code:
        raise ApiError(400, "Codes are 8 letters and numbers, like K7QM-4ZTR.", "code")
    record_event(bucket)
    student = family.redeem(me["id"], code)
    if not student:
        raise ApiError(400, "That code didn't work. It may have expired or already been used. Ask your student for a new one.", "code")
    return jsonify({"student": {"id": student["id"], "name": student["name"]}}), 201


@bp.delete("/students/<int:student_id>")
@login_required
def unlink_student(student_id):
    _student_or_404(student_id)
    family.unlink(current_user()["id"], student_id)
    return jsonify({"ok": True})


@bp.get("/students/<int:student_id>")
@login_required
def student_summary(student_id):
    student, link = _student_or_404(student_id)
    return jsonify(service.summary(student, link))


@bp.patch("/students/<int:student_id>/settings")
@login_required
def update_settings(student_id):
    student, link = _student_or_404(student_id)
    data = body()
    fields, link_fields = {}, {}
    if "weekly_goal_hours" in data:
        try:
            hours = int(data["weekly_goal_hours"])
        except (TypeError, ValueError):
            hours = 0
        if not 1 <= hours <= 20:
            raise ApiError(400, "Weekly goals run from 1 to 20 hours.", "weekly_goal_hours")
        fields["weekly_goal_hours"] = hours
    if "test_date" in data:
        fields["test_date"] = clean_date(data["test_date"])
    if "target_score" in data:
        fields["target_score"] = clean_target(data["target_score"])
    if "weekly_report" in data:
        link_fields["weekly_report"] = 1 if data["weekly_report"] is True else 0
    if "alert_days" in data:
        if data["alert_days"] not in service.ALERT_DAYS:
            raise ApiError(400, "Pick how many quiet days before an alert.", "alert_days")
        link_fields["alert_days"] = data["alert_days"]
    if not fields and not link_fields:
        raise ApiError(400, "Nothing to update.")
    if fields:  # keys come from the fixed lists above, never from the request
        execute(f"UPDATE users SET {', '.join(k + ' = ?' for k in fields)} WHERE id = ?", (*fields.values(), student_id))
    if link_fields:
        execute(f"UPDATE family_links SET {', '.join(k + ' = ?' for k in link_fields)} WHERE id = ?", (*link_fields.values(), link["id"]))
    student, link = _student_or_404(student_id)
    return jsonify(service.summary(student, link))


@bp.post("/students/<int:student_id>/plan")
@login_required
def change_plan(student_id):
    _student_or_404(student_id)
    data = body()
    plan, interval = data.get("plan"), data.get("interval")
    if plan not in service.PLANS:
        raise ApiError(400, "Pick a plan.", "plan")
    if plan != "free" and interval not in service.INTERVALS:
        raise ApiError(400, "Pick weekly, monthly or yearly billing.", "interval")
    return jsonify({"subscription": service.change_plan(current_user()["id"], student_id, plan, interval),
                    "billing": service.billing_history(student_id)})


@bp.post("/students/<int:student_id>/plan/<action>")
@login_required
def plan_action(student_id, action):
    _student_or_404(student_id)
    sub = service.subscription(student_id)
    allowed = {"pause": sub["plan"] != "free" and sub["status"] == "active",
               "cancel": sub["plan"] != "free" and sub["status"] in ("active", "paused"),
               "resume": sub["status"] in ("paused", "canceled")}
    if action not in allowed:
        raise ApiError(404, "Unknown plan action.")
    if not allowed[action]:
        raise ApiError(409, {"pause": "Only an active paid plan can be paused.", "cancel": "There's no paid plan to cancel.",
                             "resume": "The plan is already active."}[action])
    sub = getattr(service, action)(current_user()["id"], student_id)
    return jsonify({"subscription": sub, "billing": service.billing_history(student_id)})


@bp.post("/students/<int:student_id>/report")
@login_required
def send_report(student_id):
    student, link = _student_or_404(student_id)
    me = current_user()
    bucket = f"family-report:{me['id']}"
    if rate_limited(bucket, 5, 60):
        raise ApiError(429, "Reports are limited to five an hour.")
    record_event(bucket)
    s = service.summary(student, link)
    mailer.send(me["email"], f"{s['student']['first_name']}'s week on Graphite", service.report_text(me, s))
    return jsonify({"ok": True, "to": me["email"]})


def send_weekly_reports():
    """Emails every parent who has weekly reports on. Run once a week: flask --app wsgi send-weekly-reports"""
    sent = 0
    for link in query("SELECT * FROM family_links WHERE weekly_report = 1"):
        p = query("SELECT * FROM users WHERE id = ?", (link["parent_id"],), one=True)
        st = query("SELECT * FROM users WHERE id = ?", (link["student_id"],), one=True)
        s = service.summary(st, link, date.today())
        mailer.send(p["email"], f"{s['student']['first_name']}'s week on Graphite", service.report_text(p, s))
        sent += 1
    current_app.logger.info("Sent %d weekly parent reports", sent)
    return sent
