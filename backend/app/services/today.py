"""Today's set on the dashboard, from the study plan when there is one."""
import json

from ..db import query
from . import bank, practice, studyplan

MINUTES = {"drill": 15, "quiz": 15, "test": 35}


def latest_plan(user_id):
    row = query("SELECT * FROM study_plans WHERE user_id = ? ORDER BY id DESC LIMIT 1", (user_id,), one=True)
    return (row, json.loads(row["plan"])) if row else (None, None)


def week_tasks(user_id, today):
    """This week's plan tasks with their state, then any work carried over from the last two weeks
    (studyplan.catch_up), or None without a plan. Each task has its week index, so it can be started."""
    row, plan = latest_plan(user_id)
    if not row:
        return None
    index = studyplan.current_week(plan, today)
    week = plan["weeks"][index]
    states = practice.plan_task_states(user_id, row["id"])
    tasks = [dict(t, done=states.get(t["key"], {}).get("done", False), week=index) for t in week["tasks"]]
    tasks += [dict(c["task"], done=False, week=c["week"], carried=c["week_n"]) for c in studyplan.catch_up(plan, index, states)]
    return row, plan, index, week, tasks


def summary(user_id, today):
    """The dashboard's Today's set panel. None without a plan, so the dashboard falls back to its domain picks."""
    found = week_tasks(user_id, today)
    if not found:
        return None
    _, plan, index, week, tasks = found
    why = f"Week {week['n']} of {len(plan['weeks'])} · {week['phase_label']} · {week['difficulty_label']}"
    items = [{"domain": ("Drill: " if t["kind"] == "drill" else "") + t["title"], "count": t.get("count", sum(bank.MODULE_MIX.values())),
              "why": f"Carried over from week {t['carried']}" if t.get("carried") else why, "done": t["done"]} for t in tasks]
    left = [t for t in tasks if not t["done"]]
    return {"items": items, "questions": sum(i["count"] for i, t in zip(items, tasks) if not t["done"]),
            "minutes": sum(MINUTES[t["kind"]] for t in left), "source": "plan", "all_done": not left}


def start(user, today):
    """Starts today's set and returns its session, or None when the student should take the diagnostic first."""
    found = week_tasks(user["id"], today)
    if found:
        row, plan, index, week, tasks = found
        task = next((t for t in tasks if not t["done"]), None)  # this week's first, then carried-over work
        if not task:  # the week is done: another round of the week's quiz
            task = next(t for t in tasks if t["kind"] == "quiz" and t["week"] == index)
        return practice.create_plan_task(user["id"], row["id"], plan, task["week"], task["key"])
    attempt = query("SELECT results FROM test_attempts WHERE user_id = ? ORDER BY submitted_at DESC, id DESC LIMIT 1",
                    (user["id"],), one=True)
    if not attempt:
        return None
    keys = {t["name"]: t["key"] for t in bank.topics("math") + bank.topics("rw")}
    domains = [d for d in json.loads(attempt["results"])["by_domain"] if d["domain"] in keys]
    if not domains:
        return None
    weakest = min(domains, key=lambda d: d["right"] / d["total"])
    return practice.create(user["id"], "topic", keys[weakest["domain"]], None, 10)
