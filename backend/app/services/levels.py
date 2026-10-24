"""Practice Sets: practice sets that get harder one level at a time.

Each track (all of Math, one Math domain, all of Reading and Writing, or one Reading and Writing
domain) has LEVELS levels of SIZE questions. Level 1 is
mostly easy and the last level is mostly hard. Getting PASS right unlocks the next level, and
any unlocked level can be replayed with new questions.

A level is an ordinary check-as-you-go practice set (mode "quiz") tagged ladder:<track>:<level>
in practice_sessions.plan_task, so explanations, the no-repeat list and the review queue all
work the same as everywhere else.
"""
import json
import random

from . import bank, studyplan

# The database and practice sets load on first use, so the site build can import this module for its numbers.

LEVELS = 10
SIZE = 10
PASS = 7
TIERS = [(2, "Warm-up"), (4, "Building"), (6, "On target"), (8, "Challenge"), (LEVELS, "Top score")]
ALL = "mixed"
RW_ALL = "rw-mixed"
MIXED = {ALL: ("math", "All of Math"), RW_ALL: ("rw", "All of Reading and Writing")}


def tracks():
    """[{key, name, section, skills: [{domain, skill, name}]}]: all of Math, the Math domains, then the same for Reading and Writing."""
    out = []
    for key, (section, name) in MIXED.items():
        per = []
        for d in bank.topics(section):
            per.append({"key": d["key"], "name": d["name"], "section": section,
                        "skills": [{"domain": d["key"], "skill": s["key"], "name": s["name"]} for s in d["skills"]]})
        out += [{"key": key, "name": name, "section": section, "skills": [s for t in per for s in t["skills"]]}] + per
    return out


def track(key):
    return next((t for t in tracks() if t["key"] == key), None)


def tier(level):
    return next(name for top, name in TIERS if level <= top)


def difficulty(level):
    """0.05 at level 1 up to 0.95 at the top level."""
    return round(0.05 + 0.9 * (level - 1) / (LEVELS - 1), 2)


def mix(level):
    return studyplan.mix_for(difficulty(level), SIZE)


def tag(track_key, level):
    return f"ladder:{track_key}:{level}"


def parse_tag(task):
    """(track, level) for a level set's plan_task, else None."""
    parts = (task or "").split(":")
    if len(parts) != 3 or parts[0] != "ladder" or not parts[2].isdigit():
        return None
    return parts[1], int(parts[2])


def _sessions(user_id, track_key):
    from ..db import query
    return query("SELECT id, plan_task, submitted_at, correct FROM practice_sessions "
                 "WHERE user_id = ? AND plan_task LIKE ? ORDER BY id", (user_id, f"ladder:{track_key}:%"))


def progress(user_id, track_key):
    """{level: {best, passed, open_id}} for the levels this student has tried, and the highest unlocked level."""
    out = {}
    for r in _sessions(user_id, track_key):
        parsed = parse_tag(r["plan_task"])
        if not parsed:
            continue
        lv = out.setdefault(parsed[1], {"best": None, "passed": False, "open_id": None})
        if r["submitted_at"]:
            lv["best"] = max(lv["best"] or 0, r["correct"] or 0)
            lv["passed"] = lv["passed"] or (r["correct"] or 0) >= PASS
            lv["open_id"] = None
        else:
            lv["open_id"] = r["id"]
    passed = [n for n, lv in out.items() if lv["passed"]]
    unlocked = min(LEVELS, max(passed) + 1) if passed else 1
    return out, unlocked


def overview(user_id):
    out = []
    for t in tracks():
        prog, unlocked = progress(user_id, t["key"])
        levels = []
        for n in range(1, LEVELS + 1):
            p = prog.get(n, {})
            status = "passed" if p.get("passed") else ("open" if n <= unlocked else "locked")
            m = mix(n)
            levels.append({"n": n, "tier": tier(n), "mix": m, "mix_label": studyplan.mix_label(m), "status": status,
                           "best": p.get("best"), "resume_id": p.get("open_id")})
        out.append({"key": t["key"], "name": t["name"], "section": t["section"], "unlocked": unlocked, "levels": levels,
                    "all_passed": all(lv["status"] == "passed" for lv in levels)})
    return {"tracks": out, "size": SIZE, "pass": PASS, "levels": LEVELS}


HARDNESS = {"easy": 0, "medium": 1, "hard": 2}


def boss_last(ids):
    """Moves the hardest question to the end: it's the level's boss question, worth bonus XP and coins."""
    if not ids:
        return ids
    items = bank.all_items()
    boss = max(range(len(ids)), key=lambda i: (HARDNESS.get(items[ids[i]]["difficulty"], 0), i))
    return ids[:boss] + ids[boss + 1:] + [ids[boss]]


def start(user_id, track_key, level, rng=random):
    """The set for one level: the unfinished one if there is one, else a new one. None if the level is locked."""
    from . import practice
    t = track(track_key)
    prog, unlocked = progress(user_id, track_key)
    if level > unlocked:
        return None
    open_id = prog.get(level, {}).get("open_id")
    if open_id:
        return practice.get(user_id, open_id)
    ids = boss_last(practice.draw_mix(user_id, t["skills"], mix(level), rng))
    title = f"{t['name']} · Level {level}"
    domain = None if track_key in MIXED else track_key
    return practice.save_session(user_id, "quiz", title, ids, 0, domain=domain, plan_task=tag(track_key, level))


def result(user_id, session, correct):
    """What a finished level set means for the ladder, for the results page. Runs before the set is saved."""
    track_key, level = parse_tag(session.get("plan_task"))
    _, unlocked = progress(user_id, track_key)
    passed = correct >= PASS
    if passed:
        unlocked = max(unlocked, min(LEVELS, level + 1))
    t = track(track_key)
    return {"track": track_key, "track_name": t["name"] if t else track_key, "level": level, "pass": PASS,
            "total": len(json.loads(session["item_ids"])), "passed": passed,
            "next": level + 1 if passed and level < LEVELS else None, "unlocked": unlocked, "top": LEVELS}
