"""Practice sets drawn from the question bank, without repeats.

Every question a student answers goes on their done list (practice_seen).
New sets draw only from questions not on that list. When a pool runs out
(the whole bank for a practice test's domain, or one topic), the questions
in that pool come off the list and the student starts the pool again.
"""
import json
import random

from ..db import days_from_today, execute, now_iso, query
from . import bank

TOPIC_COUNTS = (5, 10, 15, 20)


def seen_ids(user_id):
    return {r["item_id"] for r in query("SELECT item_id FROM practice_seen WHERE user_id = ?", (user_id,))}


def draw(user_id, pool, n, seen, rng=random):
    """n random questions from pool, unseen first. Starts the pool over when it runs out."""
    unseen = [i for i in pool if i not in seen]
    if len(unseen) >= n:
        return rng.sample(unseen, n)
    picked = list(unseen)
    rng.shuffle(picked)
    # Every question in this pool is done (or about to be): start its list again.
    for item_id in pool:
        if item_id in seen:
            execute("DELETE FROM practice_seen WHERE user_id = ? AND item_id = ?", (user_id, item_id))
            seen.discard(item_id)
    rest = [i for i in pool if i not in picked]
    picked += rng.sample(rest, min(n - len(picked), len(rest)))
    return picked


def build_test(user_id, rng=random):
    """A 22-question module in the real test's domain mix, easiest first, like the real module."""
    seen = seen_ids(user_id)
    items = bank.all_items()
    picked = []
    for domain, n in bank.MODULE_MIX.items():
        picked += draw(user_id, bank.pool(domain=domain), n, seen, rng)
    rng.shuffle(picked)
    picked.sort(key=lambda i: bank.DIFFICULTY_ORDER[items[i]["difficulty"]])
    return picked


def topic_title(domain, skill):
    for d in bank.topics():
        if d["key"] != domain:
            continue
        if not skill:
            return d["name"]
        for s in d["skills"]:
            if s["key"] == skill:
                return s["name"]
    return None


def create(user_id, mode, domain=None, skill=None, count=10, rng=random):
    if mode == "test":
        ids, title, minutes = build_test(user_id, rng), "Math practice test", bank.MODULE_MINUTES
        domain = skill = None
    else:
        title = topic_title(domain, skill)
        ids = draw(user_id, bank.pool(domain, skill), count, seen_ids(user_id), rng)
        minutes = 0  # topic practice is untimed
    row = execute(
        "INSERT INTO practice_sessions (user_id, mode, domain, skill, title, item_ids, minutes, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?) RETURNING id",
        (user_id, mode, domain, skill, title, json.dumps(ids), minutes, now_iso()))
    return get(user_id, row["id"])


def get(user_id, session_id):
    return query("SELECT * FROM practice_sessions WHERE id = ? AND user_id = ?", (session_id, user_id), one=True)


def mark_seen(user_id, item_ids):
    stamp = now_iso()
    for item_id in item_ids:
        execute("INSERT INTO practice_seen (user_id, item_id, seen_at) VALUES (?, ?, ?) "
                "ON CONFLICT (user_id, item_id) DO NOTHING", (user_id, item_id, stamp))


def add_to_review(user_id, graded):
    """Every miss goes into the review queue, as it does for the fixed practice tests."""
    for q in graded:
        if q["correct"]:
            continue
        execute(
            "INSERT INTO review_items (user_id, test_id, question_index, domain, skill, right_count, due_on, created_at) "
            "VALUES (?, ?, 0, ?, ?, 0, ?, ?) "
            "ON CONFLICT (user_id, test_id, question_index) DO UPDATE SET right_count = 0, cleared_at = NULL, due_on = excluded.due_on",
            (user_id, "bank:" + q["id"], q["domain"], q["skill"], days_from_today(0), now_iso()))


def public(session):
    """The set as the browser sees it: questions without keys, plus feedback already given."""
    items = bank.all_items()
    ids = json.loads(session["item_ids"])
    checked = json.loads(session["checked"] or "{}")
    out = {
        "id": session["id"], "mode": session["mode"], "title": session["title"],
        "domain": session["domain"], "skill": session["skill"], "minutes": session["minutes"],
        "created_at": session["created_at"], "submitted": bool(session["submitted_at"]),
        "questions": [bank.public_question(items[i]) for i in ids],
        "checked": {k: bank.graded_question(items[ids[int(k)]], int(k), v) for k, v in checked.items()},
    }
    if session["results"]:
        out["result"] = json.loads(session["results"])
    return out


def check(user_id, session, index, answer):
    """Grades one question in topic practice and locks it. Returns the graded question."""
    items = bank.all_items()
    ids = json.loads(session["item_ids"])
    checked = json.loads(session["checked"] or "{}")
    key = str(index)
    if key not in checked:
        checked[key] = answer
        execute("UPDATE practice_sessions SET checked = ? WHERE id = ?", (json.dumps(checked), session["id"]))
        graded = bank.graded_question(items[ids[index]], index, answer)
        mark_seen(user_id, [ids[index]])
        add_to_review(user_id, [graded])
        return graded
    return bank.graded_question(items[ids[index]], index, checked[key])


def submit(user_id, session, answers, seconds):
    """Grades the whole set, saves it, and adds every answered question to the done list."""
    ids = json.loads(session["item_ids"])
    checked = {int(k): v for k, v in json.loads(session["checked"] or "{}").items()}
    answers = dict(answers)
    answers.update(checked)  # an answer that was checked can't change afterward
    result = bank.grade(ids, answers)
    result.update({"seconds_used": seconds, "practice_id": session["id"], "mode": session["mode"], "title": session["title"]})
    stamp = now_iso()
    answered = [ids[i] for i in answers if answers[i] is not None and answers[i] != ""]
    mark_seen(user_id, answered)
    add_to_review(user_id, [q for q in result["questions"] if q["answered"] and q["index"] not in checked])

    if session["mode"] == "test":
        # Practice tests count toward the dashboard's score history, like the fixed tests.
        row = execute(
            "INSERT INTO test_attempts (user_id, test_id, seconds_used, correct, total, answers, results, submitted_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?) RETURNING id",
            (user_id, f"practice-{session['id']}", seconds, result["correct"], result["total"],
             json.dumps({str(k): v for k, v in answers.items()}), json.dumps(result), stamp))
        result["attempt_id"] = row["id"]
    result["submitted_at"] = stamp
    execute("UPDATE practice_sessions SET submitted_at = ?, seconds_used = ?, correct = ?, results = ? WHERE id = ?",
            (stamp, seconds, result["correct"], json.dumps(result), session["id"]))
    execute("INSERT INTO activity (user_id, kind, seconds, detail, at) VALUES (?, ?, ?, ?, ?)",
            (user_id, "practice_test" if session["mode"] == "test" else "topic_practice", seconds,
             f"practice-{session['id']}", stamp))
    return result


def overview(user_id):
    """Topics with each one's progress through the current round, plus sets left unfinished."""
    seen = seen_ids(user_id)
    items = bank.all_items()
    done_by_skill = {}
    for item_id in seen:
        q = items.get(item_id)
        if q:
            k = (q["domain_key"], q["skill_key"])
            done_by_skill[k] = done_by_skill.get(k, 0) + 1
    domains = []
    for d in bank.topics():
        skills = [dict(s, done=done_by_skill.get((d["key"], s["key"]), 0)) for s in d["skills"]]
        domains.append({"key": d["key"], "name": d["name"], "skills": skills,
                        "total": sum(s["total"] for s in skills), "done": sum(s["done"] for s in skills)})
    open_rows = query("SELECT id, mode, title, item_ids, checked, created_at FROM practice_sessions "
                      "WHERE user_id = ? AND submitted_at IS NULL ORDER BY created_at DESC, id DESC LIMIT 5", (user_id,))
    unfinished = [{"id": r["id"], "mode": r["mode"], "title": r["title"], "created_at": r["created_at"],
                   "questions": len(json.loads(r["item_ids"])), "checked": len(json.loads(r["checked"] or "{}"))}
                  for r in open_rows]
    return {
        "total": len(items), "done": sum(d["done"] for d in domains), "domains": domains,
        "test": {"questions": sum(bank.MODULE_MIX.values()), "minutes": bank.MODULE_MINUTES},
        "topic_counts": list(TOPIC_COUNTS), "unfinished": unfinished,
    }
