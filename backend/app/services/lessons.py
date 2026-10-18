"""Active recall lessons: short lessons where every step asks the student to do something before it explains.

Lessons live in app/content/lessons/ as JSON, one file each. Step types:
  recall   a question to answer from memory, then reveal the answer and rate yourself
  predict  pick an answer before being told; the explanation comes after
  fill     a worked solution with one blank to type
  order    put the steps of a solution in order
  spot     tap the line with the mistake
Any step can carry a "table" (caption, head, rows) and "desmos" (lines to type into the Desmos calculator). "keys" are the takeaways shown at the end, and "recall"
holds the questions for the spaced recall checks.

Hands-on step types (each lesson leans on a different one, so no two lessons play alike):
  slider   drag a constant until the graph does something (answer: the value)
  plot     tap a point on a graph, like a vertex or an intersection (answer: [x, y])
  graph    type an equation; it's drawn live, Desmos style (answer: the expression, checked by value)
  sort     put cards into buckets (answer: the bucket for each card)
  match    pair each item on the left with one on the right (answer: the right-hand index for each)
  line     mark an inequality on a number line: endpoint, open or closed, direction
  build    tap tiles to build an equation (answer: the tile order)
  grid     fill in several cells of a table (answer: one value per blank)
  flash    a list shows for a few seconds, then hides, then you're asked about it
Each lesson also has a "format" (FORMATS below) that changes how it plays: hearts, a clock, a cold open with a
rematch, a story, a case file, a shortcut path, grading a student's work, a race between Desmos and by hand, an
experiment, or the classic flow. tests/test_lesson_formats.py checks that no two lessons share a format and step order.

After a lesson, a recall check is due in RECALL_DAYS[0] days, then RECALL_DAYS[1], then RECALL_DAYS[2].
Passing all three marks the lesson mastered. A missed check comes back the next day.
"""
import json
import math
import re
from datetime import date, timedelta
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

from ..db import execute, now_iso, parse_iso, query
from . import bank, game

FOLDER = Path(__file__).resolve().parent.parent / "content" / "lessons"
# Lessons that aren't one SAT skill: how to remember, and the Desmos course (reports/AI Desmos SAT math course plan.md).
# The SAT Math lessons use the question bank's domains and skills, and "Practice this skill" opens a set on that skill.
GROUPS = {
    "memory": {"name": "How to remember", "skills": {
        "active-recall": "Active recall", "spacing": "Spacing", "memory-palace": "Memory palace", "storytelling": "Story method"}},
    "desmos": {"name": "The Desmos course", "skills": {
        "hacks": "Desmos hacks", "basics": "Desmos basics", "equations": "Solve by graphing", "systems": "Systems", "sliders": "Sliders",
        "regression": "Regression", "tilde": "Find the constants", "statistics": "Lists and statistics",
        "inequalities": "Inequalities", "functions": "Functions", "circles": "Circles", "exact": "Exact answers",
        "trig": "Trig", "choices": "Answer choices", "strategy": "Desmos or by hand"}},
}
GROUP_ORDER = {"memory": 0, "algebra": 1, "advanced-math": 2, "psda": 3, "geometry-trig": 4, "desmos": 5}
STEP_TYPES = {"recall", "predict", "fill", "order", "spot", "slider", "plot", "graph", "sort", "match", "line", "build",
              "grid", "flash"}
FORMATS = {
    "classic": "Answer first, then see why.",
    "lives": "Three hearts. A wrong answer costs one.",
    "timed": "Every step has a clock. Beat it if you can.",
    "cold-open": "Try the hardest question before the lesson, then get a rematch at the end.",
    "story": "One story runs through the whole lesson.",
    "case": "A case file: every step is a clue.",
    "path": "Get the first question right and you skip ahead.",
    "teach": "A student solved these. You check the work.",
    "race": "The same kind of question two ways: by hand and in Desmos.",
    "lab": "Experiment first, then name the rule you found.",
}
START_LESSON = "desmos-hacks"  # everyone does this one first; the rest of the list opens after it
RECALL_DAYS = (1, 3, 7)
RECALL_PASS = 2 / 3  # share of recall questions to get right


@lru_cache(maxsize=1)
def all_lessons():
    out = []
    skills = {d["key"]: {s["key"] for s in d["skills"]} for d in bank.topics()}
    for f in sorted(FOLDER.glob("*.json")):
        lesson = json.loads(f.read_text(encoding="utf-8"))
        for step in lesson["steps"] + lesson["recall"]:
            if step["type"] not in STEP_TYPES:
                raise ValueError(f"{f.name}: unknown step type {step['type']}")
        lesson.setdefault("format", "classic")
        if lesson["format"] not in FORMATS:
            raise ValueError(f"{f.name}: unknown format {lesson['format']}")
        d, s = lesson["domain"], lesson["skill"]
        if d in GROUPS:
            if s not in GROUPS[d]["skills"]:
                raise ValueError(f"{f.name}: unknown {d} skill {s}")
            lesson.setdefault("practice", None)
        else:
            if s not in skills.get(d, ()):
                raise ValueError(f"{f.name}: {d}/{s} isn't a skill in the question bank")
            lesson.setdefault("practice", {"domain": d, "skill": s})
        p = lesson["practice"]
        if p and p["skill"] not in skills.get(p["domain"], ()):
            raise ValueError(f"{f.name}: practice skill {p} isn't in the question bank")
        out.append(lesson)
    return sorted(out, key=lambda l: (GROUP_ORDER.get(l["domain"], 9), l["order"]))


def lesson(lesson_id):
    return next((l for l in all_lessons() if l["id"] == lesson_id), None)


def topic_names():
    names = {}
    for key, g in GROUPS.items():
        names[key] = g["name"]
        for k, v in g["skills"].items():
            names[f"{key}/{k}"] = v
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
    for i in items:
        i["format"] = lesson(i["id"]).get("format", "classic")
    started = rows.get(START_LESSON) is not None or lesson(START_LESSON) is None
    return {"lessons": items, "recall_days": list(RECALL_DAYS), "start_with": None if started else START_LESSON,
            "formats": FORMATS,
            "due": [i["id"] for i in items if i["progress"]["due"]],
            "done": sum(1 for i in items if i["progress"]["done"]),
            "mastered": sum(1 for i in items if i["progress"]["mastered"])}


def must_start_first(user_id, lesson_id):
    """The Desmos hacks lesson opens first for everyone. Until it's finished, other lessons stay locked."""
    if lesson_id == START_LESSON or lesson(START_LESSON) is None:
        return False
    return query("SELECT 1 FROM lesson_progress WHERE user_id = ? AND lesson_id = ?", (user_id, START_LESSON), one=True) is None


def public(l, row=None, today=None):
    names = topic_names()
    return dict(l, domain_name=names.get(l["domain"], l["domain"]), format_rule=FORMATS[l.get("format", "classic")],
                skill_name=names.get(f"{l['domain']}/{l['skill']}", l["skill"]),
                progress=status(row, today or date.today()), recall_days=list(RECALL_DAYS))


def _norm(v):
    return re.sub(r"[\s,]", "", str(v or "")).replace("\u2212", "-").replace("\u2013", "-").rstrip("%").lower()


def _number(v):
    v = _norm(v)
    m = re.match(r"^(-?\d+)/(\d+)$", v)
    if m and int(m.group(2)):
        return Fraction(int(m.group(1)), int(m.group(2)))
    try:
        return Fraction(v) if re.match(r"^-?(\d+\.?\d*|\.\d+)$", v) else None
    except (ValueError, ZeroDivisionError):
        return None


def _num(v):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def _fill_ok(accept, answer):
    if not isinstance(answer, str) or len(answer) > 40:
        return False
    n = _number(answer)
    for a in accept:
        x = _number(a)
        if (n is not None and x is not None and n == x) or _norm(a) == _norm(answer):
            return True
    return False


def key(step):
    """The right answer for a step, in the shape the browser sends."""
    t = step["type"]
    return {"recall": lambda: True, "predict": lambda: step["answer"], "flash": lambda: step["answer"],
            "spot": lambda: step["wrong"], "order": lambda: list(range(len(step["items"]))),
            "fill": lambda: step["accept"][0], "slider": lambda: step["answer"], "plot": lambda: list(step["answer"]),
            "graph": lambda: step["accept"][0], "sort": lambda: [c["bucket"] for c in step["cards"]],
            "match": lambda: list(range(len(step["left"]))), "line": lambda: dict(step["answer"]),
            "build": lambda: list(step["answers"][0]), "grid": lambda: [a[0] for a in step["accept"]]}[t]()


def right(step, answer):
    """Grades one first-try answer on the server, so a score can't be made up in the browser.
    Recall steps are rated by the student (True for "Got it")."""
    t = step["type"]
    if t == "recall":
        return answer is True
    if t in ("predict", "flash"):
        return isinstance(answer, int) and not isinstance(answer, bool) and answer == step["answer"]
    if t == "spot":
        return isinstance(answer, int) and not isinstance(answer, bool) and answer == step["wrong"]
    if t == "order":
        return isinstance(answer, list) and answer == list(range(len(step["items"])))
    if t == "fill":
        return _fill_ok(step["accept"], answer)
    if t == "slider":
        v = _num(answer)
        return v is not None and abs(v - step["answer"]) <= step.get("tol", 0) + 1e-9
    if t == "plot":
        if not (isinstance(answer, list) and len(answer) == 2 and all(_num(v) is not None for v in answer)):
            return False
        tol = step.get("tol", 0) + 1e-9
        return abs(answer[0] - step["answer"][0]) <= tol and abs(answer[1] - step["answer"][1]) <= tol
    if t == "graph":
        from . import mathexpr
        return (isinstance(answer, str) and len(answer) <= mathexpr.MAX_LEN
                and not any(f in answer for f in step.get("forbid", [])) and any(mathexpr.same(answer, a) for a in step["accept"]))
    if t == "sort":
        return isinstance(answer, list) and answer == [c["bucket"] for c in step["cards"]]
    if t == "match":
        return isinstance(answer, list) and answer == list(range(len(step["left"])))
    if t == "line":
        want = step["answer"]
        return (isinstance(answer, dict) and _num(answer.get("at")) is not None and abs(answer["at"] - want["at"]) < 1e-9
                and answer.get("closed") is want["closed"] and answer.get("dir") == want["dir"])
    if t == "build":
        return isinstance(answer, list) and answer in step["answers"]
    if t == "grid":
        return (isinstance(answer, list) and len(answer) == len(step["accept"])
                and all(_fill_ok(acc, a) for acc, a in zip(step["accept"], answer)))
    return False


def grade(steps, answers):
    """How many steps were right the first time, from the student's answers (one per step).
    In a "path" lesson, a step marked skip_if (the index of its gate step) may be answered "skip"; that counts as
    right only when the gate was answered right."""
    if not isinstance(answers, list) or len(answers) != len(steps):
        raise ValueError("Send one answer for each step.")
    n = 0
    for step, a in zip(steps, answers):
        gate = step.get("skip_if")
        if a == "skip" and isinstance(gate, int) and 0 <= gate < len(steps) and steps[gate].get("skip_if") is None:
            n += 1 if right(steps[gate], answers[gate]) else 0
        elif right(step, a):
            n += 1
    return n


def complete(user_id, lesson_id, kind, answers, today=None):
    """A finished lesson or recall check, graded here from the answers.
    Returns the rewards report plus the lesson's new progress."""
    today = today or date.today()
    l = lesson(lesson_id)
    steps = l["steps"] if kind == "lesson" else l["recall"]
    total = len(steps)
    score = grade(steps, answers)
    from . import history
    for i, (step, a) in enumerate(zip(steps, answers)):
        history.question(user_id, f"lesson:{lesson_id}:{kind}:{i + 1}", "lesson" if kind == "lesson" else "recall",
                         lesson_id, a if isinstance(a, str) else json.dumps(a), a != "skip" and right(step, a))
    row = _rows(user_id).get(lesson_id)
    xp_before, _ = game.totals(user_id)
    badges = []
    passed = None
    if kind == "lesson":
        if row:
            # Stamps are UTC; compare in the server's own day so late-evening replays still count as today.
            replayed_today = parse_iso(row["last_recall_at"] or row["completed_at"]).astimezone().date() == today
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
