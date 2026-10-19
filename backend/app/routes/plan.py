"""The diagnostic and the study plan built from it."""
import json
import random
from datetime import date, datetime, timezone

from flask import Blueprint, jsonify, request

from ..db import execute, now_iso, query, set_clause
from ..security import ApiError, body, clean_date, current_user, login_required, public_user
from ..services import access, bank, diagnostic, practice, studyplan

bp = Blueprint("plan", __name__, url_prefix="/api/plan")


def _today():
    """The student's date (?today=YYYY-MM-DD), accepted within a day of the server's, as the dashboard does."""
    server = datetime.now(timezone.utc).date()
    try:
        local = date.fromisoformat(request.args.get("today", ""))
    except ValueError:
        return server
    return local if abs((local - server).days) <= 1 else server


def _latest_plan(user_id):
    return query("SELECT * FROM study_plans WHERE user_id = ? ORDER BY id DESC LIMIT 1", (user_id,), one=True)


def _update_profile(user, data):
    fields = {}
    if data.get("test_date") not in (None, ""):
        fields["test_date"] = clean_date(data["test_date"])
    if data.get("weekly_goal_hours") not in (None, ""):
        try:
            hours = int(data["weekly_goal_hours"])
        except (TypeError, ValueError):
            hours = 0
        if not 1 <= hours <= 20:
            raise ApiError(400, "Weekly study time runs from 1 to 20 hours.", "weekly_goal_hours")
        fields["weekly_goal_hours"] = hours
    if fields:
        sets = set_clause(fields)  # keys from the fixed list above
        execute(f"UPDATE users SET {sets} WHERE id = ?", (*fields.values(), user["id"]))
    return query("SELECT * FROM users WHERE id = ?", (user["id"],), one=True)


def _save_plan(user, diagnostic_id, results, today):
    plan = studyplan.build(results, user["test_date"], user["weekly_goal_hours"], today)
    row = execute("INSERT INTO study_plans (user_id, diagnostic_id, plan, created_at) VALUES (?, ?, ?, ?) RETURNING id",
                  (user["id"], diagnostic_id, json.dumps(plan), now_iso()))
    return row["id"], plan


@bp.get("")
@login_required
def overview():
    user = current_user()
    if not user["diagnostic_prompted_at"]:
        execute("UPDATE users SET diagnostic_prompted_at = ? WHERE id = ?", (now_iso(), user["id"]))
    diag = query("SELECT * FROM diagnostics WHERE user_id = ? ORDER BY id DESC LIMIT 1", (user["id"],), one=True)
    out = {"user": public_user(user), "diagnostic": None, "plan": None}
    if diag:
        out["diagnostic"] = {"id": diag["id"], "submitted": bool(diag["submitted_at"]),
                             "questions": [diagnostic.public_question(i) for i in json.loads(diag["item_ids"])]}
        if diag["results"]:
            out["diagnostic"]["results"] = json.loads(diag["results"])
    row = _latest_plan(user["id"])
    if row:
        plan = json.loads(row["plan"])
        source = query("SELECT results FROM diagnostics WHERE id = ?", (row["diagnostic_id"],), one=True)
        out["plan"] = dict(plan, id=row["id"], current_week=studyplan.current_week(plan, _today()), tasks=practice.plan_task_states(user["id"], row["id"]),
                           results=json.loads(source["results"]))
    out["access"] = access.public_state(access.state(user["id"], "study_plan"))
    return jsonify(out)


@bp.post("/diagnostic")
@login_required
def start_diagnostic():
    user = _update_profile(current_user(), body())
    diag = query("SELECT * FROM diagnostics WHERE user_id = ? AND submitted_at IS NULL ORDER BY id DESC LIMIT 1", (user["id"],), one=True)
    if not diag:
        ids = diagnostic.pick(practice.taken_ids(user["id"]), random)
        diag = execute("INSERT INTO diagnostics (user_id, item_ids, created_at) VALUES (?, ?, ?) RETURNING id",
                       (user["id"], json.dumps(ids), now_iso()))
        diag = query("SELECT * FROM diagnostics WHERE id = ?", (diag["id"],), one=True)
    return jsonify({"diagnostic": {"id": diag["id"], "submitted": False,
                                   "questions": [diagnostic.public_question(i) for i in json.loads(diag["item_ids"])]}}), 201


@bp.post("/diagnostic/<int:diag_id>/submit")
@login_required
def submit_diagnostic(diag_id):
    user = current_user()
    diag = query("SELECT * FROM diagnostics WHERE id = ? AND user_id = ?", (diag_id, user["id"]), one=True)
    if not diag:
        raise ApiError(404, "That diagnostic doesn't exist.")
    if diag["submitted_at"]:
        raise ApiError(409, "This diagnostic is already finished.")
    data = body()
    ids = json.loads(diag["item_ids"])
    answers, sure = {}, {}
    raw_answers = data.get("answers") if isinstance(data.get("answers"), dict) else {}
    raw_sure = data.get("sure") if isinstance(data.get("sure"), dict) else {}
    for key, value in raw_answers.items():
        try:
            i = int(key)
        except (TypeError, ValueError):
            continue
        if 0 <= i < len(ids):
            cleaned = diagnostic.clean_answer(ids[i], value)
            if cleaned is not None:
                answers[i] = cleaned
                sure[i] = raw_sure.get(key) is True
    results = diagnostic.grade(ids, answers, sure)
    stamp = now_iso()
    from ..services import history
    graded = {q.get("index"): q.get("correct") for q in results.get("questions", []) if isinstance(q, dict)}
    for i, a in answers.items():
        history.question(user["id"], ids[i], "diagnostic", f"diagnostic-{diag_id}", a, graded.get(i))
    execute("UPDATE diagnostics SET submitted_at = ?, answers = ?, results = ? WHERE id = ?",
            (stamp, json.dumps({"answers": answers, "sure": sure}), json.dumps(results), diag_id))
    # Math questions answered here count as done, like any practice question.
    # Bank questions (Math and Reading and Writing) go on the done list; the old diagnostic-only ones aren't in the bank.
    items = bank.all_items()
    practice.mark_seen(user["id"], [ids[i] for i in answers if ids[i] in items])
    plan_id, plan = _save_plan(user, diag_id, results, _today())
    return jsonify({"results": results, "plan": dict(plan, id=plan_id, current_week=studyplan.current_week(plan, _today()), tasks={}),
                    "access": access.public_state(access.state(user["id"], "study_plan"))}), 201


@bp.post("/rebuild")
@login_required
def rebuild():
    """New test date or weekly hours: rebuild the plan from the latest diagnostic."""
    access.require(current_user(), "study_plan")
    user = _update_profile(current_user(), body())
    diag = query("SELECT * FROM diagnostics WHERE user_id = ? AND submitted_at IS NOT NULL ORDER BY id DESC LIMIT 1", (user["id"],), one=True)
    if not diag:
        raise ApiError(400, "Take the diagnostic first.")
    plan_id, plan = _save_plan(user, diag["id"], json.loads(diag["results"]), _today())
    return jsonify({"plan": dict(plan, id=plan_id, current_week=studyplan.current_week(plan, _today()), tasks={})}), 201


@bp.post("/tasks")
@login_required
def start_task():
    user = current_user()
    data = body()
    row = _latest_plan(user["id"])
    if not row:
        raise ApiError(400, "Take the diagnostic first.")
    access.require(user, "study_plan")
    plan = json.loads(row["plan"])
    try:
        week = int(data.get("week"))
    except (TypeError, ValueError):
        raise ApiError(400, "That week isn't in your plan.")
    if not 0 <= week < len(plan["weeks"]):
        raise ApiError(400, "That week isn't in your plan.")
    session = practice.create_plan_task(user["id"], row["id"], plan, week, str(data.get("task") or ""))
    if not session:
        raise ApiError(400, "That task isn't in your plan.")
    out = practice.public(session)
    access.redact(user["id"], list(out["checked"].values()))
    return jsonify({"session": out}), 201
