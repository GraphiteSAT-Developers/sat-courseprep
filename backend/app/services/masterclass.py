"""The Desmos masterclass: lessons from content/masterclass/lessons.json and each student's progress.

A lesson is a series of checkpoints: its calculator steps, then its questions about the graph, then
one SAT-style question (a strategy drill's checkpoints are its items). Progress is how many checkpoints
the student has passed, and it only goes up: going back over a finished lesson never undoes it.

The page checks each step against the student's calculator in the browser, so the server only
stores how far each student got.
"""
import json
from functools import lru_cache
from pathlib import Path

from ..db import execute, now_iso, query

LESSONS_FILE = Path(__file__).resolve().parent.parent / "content" / "masterclass" / "lessons.json"


@lru_cache(maxsize=None)
def content():
    return json.loads(LESSONS_FILE.read_text())


def lessons():
    return {lesson["id"]: lesson for lesson in content()["lessons"]}


def total(lesson):
    if lesson.get("kind") == "drill":
        return len(lesson["items"])
    return len(lesson["steps"]) + len(lesson.get("reads", [])) + (1 if lesson.get("try") else 0)


def progress(user_id):
    rows = query("SELECT lesson_id, step, completed_at FROM masterclass_progress WHERE user_id = ?", (user_id,))
    known = lessons()
    return {r["lesson_id"]: {"step": r["step"], "total": total(known[r["lesson_id"]]), "completed": bool(r["completed_at"])}
            for r in rows if r["lesson_id"] in known}


def save(user_id, lesson_id, step):
    """Records that the student reached checkpoint `step` of a lesson. Returns that lesson's progress."""
    lesson = lessons()[lesson_id]
    n = total(lesson)
    step = max(0, min(n, step))
    stamp = now_iso()
    # Steps can pass in quick succession, so saves may arrive together: each write here is safe to race.
    execute("INSERT INTO masterclass_progress (user_id, lesson_id, step, updated_at) VALUES (?, ?, 0, ?) "
            "ON CONFLICT (user_id, lesson_id) DO NOTHING", (user_id, lesson_id, stamp))
    execute("UPDATE masterclass_progress SET step = ?, updated_at = ? WHERE user_id = ? AND lesson_id = ? AND step < ?",
            (step, stamp, user_id, lesson_id, step))
    if step == n:
        execute("UPDATE masterclass_progress SET completed_at = ? WHERE user_id = ? AND lesson_id = ? AND completed_at IS NULL",
                (stamp, user_id, lesson_id))
    row = query("SELECT step FROM masterclass_progress WHERE user_id = ? AND lesson_id = ?", (user_id, lesson_id), one=True)
    return {"step": row["step"], "total": n, "completed": row["step"] == n}


def summary(user_id):
    """For the dashboard: lessons finished, and the next lesson to take."""
    done = progress(user_id)
    order = content()["lessons"]
    finished = sum(1 for lesson in order if done.get(lesson["id"], {}).get("completed"))
    nxt = next((lesson for lesson in order if not done.get(lesson["id"], {}).get("completed")), None)
    return {
        "completed": finished, "lessons": len(order),
        "next": {"id": nxt["id"], "title": nxt["title"], "minutes": nxt["minutes"],
                 "started": nxt["id"] in done} if nxt else None,
    }
