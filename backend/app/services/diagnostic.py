"""The 10-question diagnostic: 6 Math questions from the question bank and 4 Reading and Writing questions.

Math slots cover all four domains at medium and hard difficulty, so the result says both
where a student is weak and how hard their practice should start. Reading and Writing draws
one medium question per domain from the same question bank, from questions the student hasn't
done when possible. Each answer also carries the student's confidence: a lucky guess shouldn't
count as a strength.

content/diagnostic/rw.json holds the questions the diagnostic used before Reading and Writing
joined the bank. It's only read to grade diagnostics that were started with them.

No database access here, so website/build.py can reuse it for the offline preview.
"""
import html
import json
from functools import lru_cache
from pathlib import Path

from . import bank

RW_FILE = Path(__file__).resolve().parent.parent / "content" / "diagnostic" / "rw.json"

MATH_SLOTS = [("algebra", "medium"), ("algebra", "hard"), ("advanced-math", "medium"), ("advanced-math", "hard"),
              ("psda", "medium"), ("geometry-trig", "medium")]
RW_DOMAINS = ["Information and Ideas", "Craft and Structure", "Expression of Ideas", "Standard English Conventions"]
DIFFICULTY_WEIGHT = {"easy": 0.8, "medium": 1.0, "hard": 1.3}
SURE, GUESS = 1.0, 0.7  # credit for a right answer, by confidence. A wrong answer earns 0.
STRONG, WEAK = 0.75, 0.45


@lru_cache(maxsize=None)
def legacy_rw_items():
    """The old diagnostic-only Reading and Writing questions, for diagnostics started before the bank had them."""
    items = {}
    for raw in json.loads(RW_FILE.read_text())["items"]:
        q = dict(raw, type="mc", section="Reading and Writing", difficulty="medium")
        key = raw["answer"]
        q["explain_html"] = (
            '<div class="xp"><p class="xp-answer"><span class="label">Answer</span> '
            f"<strong>{bank.LETTERS[key]}. {html.escape(raw['choices'][key])}</strong></p>"
            f'<section class="xp-sec"><h4>Why</h4><p>{html.escape(raw["explain"])}</p></section>'
            f'<section class="xp-sec xp-desmos"><h4>Strategy</h4><p>{html.escape(raw["tip"])}</p></section></div>')
        items[q["id"]] = q
    return items


def item(item_id):
    return bank.all_items().get(item_id) or legacy_rw_items()[item_id]


def is_rw(q):
    return q.get("section") in ("rw", "Reading and Writing")


def pick(seen, rng):
    """The 10 question ids: Math first (questions the student hasn't done when possible), then Reading and Writing."""
    items = bank.all_items()
    ids, used_skills = [], set()
    for domain, difficulty in MATH_SLOTS:
        pool = [q for q in items.values() if q["domain_key"] == domain and q["difficulty"] == difficulty
                and q["skill_key"] not in used_skills]
        fresh = [q for q in pool if q["id"] not in seen] or pool
        q = rng.choice(sorted(fresh, key=lambda x: x["id"]))
        used_skills.add(q["skill_key"])
        ids.append(q["id"])
    for domain in RW_DOMAINS:
        pool = [q["id"] for q in items.values() if q["section"] == "rw" and q["domain"] == domain and q["difficulty"] == "medium"]
        fresh = [i for i in pool if i not in seen] or pool
        ids.append(rng.choice(sorted(fresh)))
    return ids


def public_question(item_id):
    q = item(item_id)
    section = "Reading and Writing" if is_rw(q) else "Math"
    out = {"id": q["id"], "section": section, "domain": q["domain"], "skill": q["skill"],
           "type": q["type"], "stem": q["stem"]}
    if q.get("passage"):
        out["passage"], out["prompt"] = q["passage"], q["prompt"]
    if q["type"] == "mc":
        out["choices"] = q["choices"]
    return out


def clean_answer(item_id, value):
    q = item(item_id)
    if is_rw(q):
        return value if isinstance(value, int) and not isinstance(value, bool) and 0 <= value < len(q["choices"]) else None
    return bank.clean_answer(q, value)


def grade(item_ids, answers, sure):
    """Grades the diagnostic and scores every domain. answers and sure are keyed by question index."""
    questions, by_domain = [], {}
    math_points = math_weight = 0.0
    for i, item_id in enumerate(item_ids):
        q = item(item_id)
        rw = is_rw(q)
        answer = answers.get(i)
        if rw and q["section"] == "Reading and Writing":  # an old diagnostic-only question
            ok = answer is not None and answer == q["answer"]
            g = {"index": i, "id": item_id, "type": "mc", "domain": q["domain"], "skill": q["skill"], "stem": q["stem"],
                 "choices": q["choices"], "answer_index": q["answer"], "answer": bank.LETTERS[q["answer"]],
                 "answered": answer is not None, "correct": ok,
                 "your_answer": bank.LETTERS[answer] if answer is not None else None, "explain_html": q["explain_html"]}
        else:
            g = bank.graded_question(q, i, answer)
            ok = g["correct"]
        g["section"] = "Reading and Writing" if rw else "Math"
        g["sure"] = bool(sure.get(i))
        g["score"] = (SURE if g["sure"] else GUESS) if ok else 0.0
        if not rw:
            g["skill_key"] = q["skill_key"]
            g["domain_key"] = q["domain_key"]
            w = DIFFICULTY_WEIGHT[q["difficulty"]]
            math_points += g["score"] * w
            math_weight += w
        d = by_domain.setdefault(q["domain"], {"section": g["section"], "domain": q["domain"],
                                               "domain_key": q.get("domain_key"), "points": 0.0, "count": 0})
        d["points"] += g["score"]
        d["count"] += 1
        questions.append(g)

    domains = []
    for d in by_domain.values():
        score = round(d["points"] / d["count"], 2)
        domains.append({"section": d["section"], "domain": d["domain"], "domain_key": d["domain_key"], "score": score,
                        "label": "Strength" if score >= STRONG else ("Focus" if score < WEAK else "Building")})
    order = {name: i for i, name in enumerate([t["name"] for t in bank.topics()] + RW_DOMAINS)}
    domains.sort(key=lambda d: order.get(d["domain"], 99))
    return {
        "questions": questions,
        "correct": sum(q["correct"] for q in questions), "total": len(questions),
        "domains": domains,
        "skills": {q["skill_key"]: q["score"] for q in questions if q["section"] == "Math"},
        "level": round(math_points / math_weight, 2) if math_weight else 0.5,
        "strengths": [d["domain"] for d in sorted(domains, key=lambda d: -d["score"]) if d["score"] >= STRONG],
        "focus": [d["domain"] for d in sorted(domains, key=lambda d: d["score"]) if d["score"] < WEAK],
    }
