"""Active recall lessons: short lessons where every step asks the student to do something before it explains.

Lessons live in app/content/lessons/ as JSON, one file each. Step types:
  recall   a question to answer from memory, then reveal the answer and rate yourself
  predict  pick an answer before being told; the explanation comes after
  fill     a worked solution with one blank to type
  order    put the steps of a solution in order
  spot     tap the line with the mistake
Any step can carry a "table" (caption, head, rows). "keys" are the takeaways shown at the end, and "recall"
holds the questions for the spaced recall checks.

After a lesson, a recall check is due in RECALL_DAYS[0] days, then RECALL_DAYS[1], then RECALL_DAYS[2].
Passing all three marks the lesson mastered. A missed check comes back the next day.
"""
import json
import math
from datetime import date, timedelta
from functools import lru_cache
from pathlib import Path

from ..db import execute, now_iso, query
from . import bank, game

FOLDER = Path(__file__).resolve().parent.parent / "content" / "lessons"
STEP_TYPES = {"recall", "predict", "fill", "order", "spot"}
RECALL_DAYS = (1, 3, 7)
RECALL_PASS = 2 / 3  # share of recall questions to get right


@lru_cache(maxsize=1)
def all_lessons():
    out = []
    for f in sorted(FOLDER.glob("*.json")):
        lesson = json.loads(f.read_text(encoding="utf-8"))
        for step in lesson["steps"] + lesson["recall"]:
            if step["type"] not in STEP_TYPES:
                raise ValueError(f"{f.name}: unknown step type {step['type']}")
        out.append(lesson)
    return sorted(out, key=lambda l: l["order"])


def lesson(lesson_id):
    return next((l for l in all_lessons() if l["id"] == lesson_id), None)


def topic_names():
    names = {}
    for d in bank.topics():
        names[d["key"]] = d["name"]
        for s in d["skills"]:
            names[f"{d['key']}/{s['key']}"] = s["name"]
    return names


def _rows(user_id):
    return {r["lesson_id"]: r for r in query("SELECT * FROM lesson_progress WHERE user_id = ?", (user_id,))}


def status(row, today):
    if not row:
        return {"done": False, "stage": 0, "mastered": False, "due": False, "due_on": None, "best": None, "total": None}
    mastered = row["stage"] >= len(RECALL_DAYS)
    return {"done": True, "stage": row["stage"], "mastered": mastered, "best": row["best"], "total": row["total"],
            "due_on": row["due_on"], "due": bool(row["due_on"]) and not mastered and row["due_on"] <= today.isoformat()}


def overview(user_id, today=None):
    today = today or date.today()
    rows = _rows(user_id)
    names = topic_names()
    items = []
    for l in all_lessons():
        items.append({"id": l["id"], "title": l["title"], "hook": l["hook"], "minutes": l["minutes"], "domain": l["domain"],
                      "domain_name": names.get(l["domain"], l["domain"]), "skill": l["skill"],
                      "skill_name": names.get(f"{l['domain']}/{l['skill']}", l["skill"]), "steps": len(l["steps"]),
                      "progress": status(rows.get(l["id"]), today)})
    return {"lessons": items, "recall_days": list(RECALL_DAYS),
            "due": [i["id"] for i in items if i["progress"]["due"]],
            "done": sum(1 for i in items if i["progress"]["done"]),
            "mastered": sum(1 for i in items if i["progress"]["mastered"])}


def public(l, row=None, today=None):
    names = topic_names()
    return dict(l, domain_name=names.get(l["domain"], l["domain"]),
                skill_name=names.get(f"{l['domain']}/{l['skill']}", l["skill"]),
                progress=status(row, today or date.today()), recall_days=list(RECALL_DAYS))


def complete(user_id, lesson_id, kind, score, today=None):
    """A finished lesson or recall check. score is how many steps were right the first time.
    Returns the rewards report plus the lesson's new progress."""
    today = today or date.today()
    l = lesson(lesson_id)
    total = len(l["steps"] if kind == "lesson" else l["recall"])
    score = max(0, min(total, score))
    row = _rows(user_id).get(lesson_id)
    xp_before, _ = game.totals(user_id)
    badges = []
    passed = None
    if kind == "lesson":
        if row:
            replayed_today = (row["last_recall_at"] or row["completed_at"])[:10] == today.isoformat()
            xp, coins = (0 if replayed_today else game.XP_LESSON_REPLAY), 0
            execute("UPDATE lesson_progress SET best = ?, last_recall_at = ? WHERE id = ?",
                    (max(row["best"], score), now_iso(), row["id"]))
        else:
            xp, coins = game.XP_LESSON_FIRST, game.COINS_LESSON_FIRST
            execute("INSERT INTO lesson_progress (user_id, lesson_id, completed_at, best, total, stage, due_on) VALUES (?, ?, ?, ?, ?, 0, ?)",
                    (user_id, lesson_id, now_iso(), score, total, (today + timedelta(days=RECALL_DAYS[0])).isoformat()))
            badges.append(game.earn_badge(user_id, "recall_rookie"))
    else:
        if not row:
            raise ValueError("Finish the lesson before its recall check.")
        st = status(row, today)
        passed = score >= math.ceil(total * RECALL_PASS)
        if not st["due"]:
            xp, coins = 0, 0  # an early recall check is good practice but doesn't move the schedule
        elif passed:
            stage = row["stage"] + 1
            due = None if stage >= len(RECALL_DAYS) else (today + timedelta(days=RECALL_DAYS[stage])).isoformat()
            execute("UPDATE lesson_progress SET stage = ?, due_on = ?, last_recall_at = ? WHERE id = ?",
                    (stage, due, now_iso(), row["id"]))
            xp, coins = game.XP_RECALL_PASS, game.COINS_RECALL_PASS
        else:
            execute("UPDATE lesson_progress SET due_on = ?, last_recall_at = ? WHERE id = ?",
                    ((today + timedelta(days=1)).isoformat(), now_iso(), row["id"]))
            xp, coins = game.XP_RECALL_TRY, 0
    rows = _rows(user_id)
    if sum(1 for r in rows.values() if r["stage"] >= len(RECALL_DAYS)) >= 3:
        badges.append(game.earn_badge(user_id, "memory_palace"))
    if len(rows) == len(all_lessons()):
        badges.append(game.earn_badge(user_id, "total_recall"))
    s = game.award(user_id, "lesson" if kind == "lesson" else "recall", xp, coins, f"lesson:{lesson_id}") if xp or coins else None
    rep = game.report(user_id, xp_before, xp, coins, badges, s)
    return dict(rep, score=score, total=total, passed=passed, progress=status(rows.get(lesson_id), today))
