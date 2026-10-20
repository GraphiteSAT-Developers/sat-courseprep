"""The score check: 20 questions anyone can take without an account, scored like the SAT.

10 Reading and Writing questions, then 10 Math (2 of them typed-in answers), in the real test's order and
domain mix, with easy, medium and hard questions in roughly Module 1's proportions. Each section is
projected to a 200 to 800 score by services/scoring.py; 10 questions is a small sample, so its range is
wider than a practice test's.

The result also says where the points are: for each skill, about how many points the student would gain
by getting its misses right (and by being sure of its lucky guesses, which count half). That ranks what to
study first.

No database access here, so the static preview (score-check.js) can mirror it.
"""
import random

from . import bank, scoring

DIFFICULTY_CYCLE = ["easy", "medium", "hard", "medium", "easy", "hard", "medium", "hard", "easy", "medium"]
SECTIONS = [
    # (section, domain keys and question counts, the slots with typed-in answers)
    ("rw", [("information-ideas", 3), ("craft-structure", 3), ("expression-ideas", 2), ("conventions", 2)], ()),
    ("math", [("algebra", 3), ("advanced-math", 3), ("psda", 2), ("geometry-trig", 2)], (2, 5)),
]
SECTION_NAMES = {"rw": "Reading and Writing", "math": "Math"}
QUESTIONS = 20
GUESS_WEIGHT = 0.5  # a right answer the student wasn't sure of: half its points count as still at risk
TOP_SKILLS = 3


def pick(rng=random):
    """The 20 question ids: Reading and Writing first, as on test day, then Math easiest first."""
    items = bank.all_items()
    ids = []
    for section, domains, typed in SECTIONS:
        slots = [d for d, n in domains for _ in range(n)]
        picked = []
        for i, domain in enumerate(slots):
            want = DIFFICULTY_CYCLE[i % len(DIFFICULTY_CYCLE)]
            kind = "spr" if i in typed else "mc"  # one hard Algebra and one hard Advanced Math typed-in answer
            pool = [q for q in items.values() if q["section"] == section and q["domain_key"] == domain
                    and q["type"] == kind and q["id"] not in picked]
            pool = [q for q in pool if q["difficulty"] == want] or [q for q in pool if q["difficulty"] != "easy"] or pool
            picked.append(rng.choice(sorted(pool, key=lambda q: q["id"]))["id"])
        if section == "rw":
            picked.sort(key=lambda i: bank.rw_sort_key(items[i]))
        else:
            picked.sort(key=lambda i: bank.DIFFICULTY_ORDER[items[i]["difficulty"]])
        ids += picked
    return ids


def questions(ids):
    return [bank.public_question(bank.all_items()[i]) for i in ids]


def grade(ids, answers, sure):
    """Grades the score check. answers and sure are keyed by question index. Returns the total and
    section estimates, the skills worth the most points, and every question with its explanation."""
    items = bank.all_items()
    graded = []
    for i, item_id in enumerate(ids):
        g = bank.graded_question(items[item_id], i, answers.get(i))
        g["sure"] = bool(sure.get(i))
        g["skill_key"] = items[item_id]["skill_key"]
        graded.append(g)

    sections, skills = [], {}
    for key, *_ in SECTIONS:
        qs = [g for g in graded if g["section"] == key]
        est = scoring.project(key, qs, "check")
        sections.append(dict(est, name=SECTION_NAMES[key], right=sum(g["correct"] for g in qs), total=len(qs)))
        for n, g in enumerate(qs):
            if g["correct"] and g["sure"]:
                continue
            # What this one question is worth: the section score with it right, minus the score with it wrong.
            flipped = [dict(x, correct=(k == n) or x["correct"]) for k, x in enumerate(qs)]
            missed = [dict(x, correct=(k != n) and x["correct"]) for k, x in enumerate(qs)]
            worth = scoring.project(key, flipped, "check")["score"] - scoring.project(key, missed, "check")["score"]
            s = skills.setdefault(g["skill"], {"skill": g["skill"], "section": SECTION_NAMES[key], "domain": g["domain"],
                                               "points": 0.0, "missed": 0, "guessed": 0})
            if g["correct"]:
                s["points"] += worth * GUESS_WEIGHT
                s["guessed"] += 1
            else:
                s["points"] += worth
                s["missed"] += 1

    score = sum(s["score"] for s in sections)
    spread = scoring.SPREAD["check_total"]
    ranked = sorted((dict(s, points=int(round(s["points"] / 10.0) * 10)) for s in skills.values()),
                    key=lambda s: (-s["points"], -s["missed"], s["skill"]))
    top = [s for s in ranked if s["points"] > 0][:TOP_SKILLS]
    # The estimate with every question in those skills right: what fixing them is worth, all together.
    fix = {s["skill"] for s in top}
    potential = sum(scoring.project(key, [dict(g, correct=g["correct"] or g["skill"] in fix) for g in graded if g["section"] == key],
                                    "check")["score"] for key, *_ in SECTIONS)
    return {
        "total": {"score": score, "low": max(400, score - spread), "high": min(1600, score + spread)},
        "sections": sections,
        "skills": top,
        "potential": potential,
        "correct": sum(g["correct"] for g in graded), "count": len(graded),
        "skipped": sum(not g["answered"] for g in graded),
        "questions": graded,
    }
