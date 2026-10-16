"""Practice sets drawn from the question bank, without repeats.

Every question a student answers goes on their done list (practice_seen).
New sets draw only from questions not on that list. When a pool runs out
(the whole bank for a practice test's domain, or one topic), the questions
in that pool come off the list and the student starts the pool again.

When the last question of a skill or a domain goes on the list, the student
has finished that topic: it's recorded once per round (practice_completions)
and returned so the page can congratulate them.
"""
import json
import random

from ..db import days_from_today, execute, now_iso, query
from . import bank, review, studyplan

TOPIC_COUNTS = (5, 10, 15, 20)


def seen_ids(user_id):
    return {r["item_id"] for r in query("SELECT item_id FROM practice_seen WHERE user_id = ?", (user_id,))}


def draw(user_id, pool, n, seen, rng=random, fill=False):
    """Up to n random questions from pool that the student hasn't done.

    When fewer than n are left, the set is just those, so the student can finish the topic,
    unless fill is set (a practice test needs its full count): then it tops up with questions
    already done. Once every question in the pool is done, its list starts again.
    """
    unseen = [i for i in pool if i not in seen]
    if not unseen:
        # Every question in this pool is done: start its list again.
        for topic in topics_of(pool):
            execute("DELETE FROM practice_completions WHERE user_id = ? AND topic = ?", (user_id, topic))
        for item_id in pool:
            execute("DELETE FROM practice_seen WHERE user_id = ? AND item_id = ?", (user_id, item_id))
            seen.discard(item_id)
        unseen = list(pool)
    if len(unseen) >= n or not fill:
        return rng.sample(unseen, min(n, len(unseen)))
    done = [i for i in pool if i not in unseen]
    return rng.sample(unseen, len(unseen)) + rng.sample(done, min(n - len(unseen), len(done)))


def build_test(user_id, rng=random):
    """A 22-question module in the real test's domain mix, easiest first, like the real module."""
    seen = seen_ids(user_id)
    items = bank.all_items()
    picked = []
    for domain, n in bank.MODULE_MIX.items():
        picked += draw(user_id, bank.pool(domain=domain), n, seen, rng, fill=True)
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
    return save_session(user_id, mode, title, ids, minutes, domain, skill)


def save_session(user_id, mode, title, ids, minutes, domain=None, skill=None, plan_id=None, plan_task=None):
    row = execute(
        "INSERT INTO practice_sessions (user_id, mode, domain, skill, title, item_ids, minutes, created_at, plan_id, plan_task) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) RETURNING id",
        (user_id, mode, domain, skill, title, json.dumps(ids), minutes, now_iso(), plan_id, plan_task))
    return get(user_id, row["id"])


# ---------- study plan sets ----------

NEIGHBORS = {"easy": ["medium", "hard"], "medium": ["easy", "hard"], "hard": ["medium", "easy"]}


def draw_mix(user_id, skills, mix, rng=random):
    """Questions from these skills in the given difficulty mix ({easy: n, medium: n, hard: n}).

    Takes questions the student hasn't done first. A difficulty that runs short borrows from the
    nearest other difficulty; if the skills run out altogether, it falls back to draw(), which
    starts the pool over.
    """
    items = bank.all_items()
    seen = seen_ids(user_id)
    pool = [i for s in skills for i in bank.pool(s["domain"], s["skill"])]
    unseen = {d: [i for i in pool if i not in seen and items[i]["difficulty"] == d] for d in ("easy", "medium", "hard")}
    for d in unseen:
        rng.shuffle(unseen[d])
    picked = []
    for d, n in mix.items():
        for source in [d] + NEIGHBORS[d]:
            while n and unseen[source]:
                picked.append(unseen[source].pop())
                n -= 1
        if n:
            rest = [i for i in pool if i not in picked]
            more = draw(user_id, rest, n, seen, rng, fill=True)
            picked += [i for i in more if i not in picked]
    picked.sort(key=lambda i: bank.DIFFICULTY_ORDER[items[i]["difficulty"]])
    return picked


def adjusted_mix(user_id, plan_id, difficulty, n):
    """The week's difficulty, nudged by the student's last two plan quiz scores: up after 80% or better, down at 50% or worse."""
    rows = query("SELECT correct, item_ids FROM practice_sessions WHERE user_id = ? AND plan_id = ? AND mode = 'quiz' "
                 "AND submitted_at IS NOT NULL ORDER BY submitted_at DESC, id DESC LIMIT 2", (user_id, plan_id))
    if rows:
        pct = sum(r["correct"] for r in rows) / sum(len(json.loads(r["item_ids"])) for r in rows)
        if pct >= 0.8:
            difficulty += 0.1
        elif pct <= 0.5:
            difficulty -= 0.1
    return studyplan.mix_for(min(0.95, max(0.05, difficulty)), n)


def plan_task_states(user_id, plan_id):
    """Each plan task's latest set: {task key: {session_id, submitted, done, correct, total}}."""
    rows = query("SELECT id, plan_task, submitted_at, correct, item_ids FROM practice_sessions "
                 "WHERE user_id = ? AND plan_id = ? ORDER BY id", (user_id, plan_id))
    out = {}
    for r in rows:
        done = out.get(r["plan_task"], {}).get("done", False) or bool(r["submitted_at"])
        out[r["plan_task"]] = {"session_id": r["id"], "submitted": bool(r["submitted_at"]), "done": done,
                               "correct": r["correct"], "total": len(json.loads(r["item_ids"]))}
    return out


def create_plan_task(user_id, plan_id, plan, week_index, task_key, rng=random):
    """Starts (or resumes) the practice set for one task in the student's plan."""
    week = plan["weeks"][week_index]
    task = next((t for t in week["tasks"] if t["key"] == task_key), None)
    if not task:
        return None
    open_row = query("SELECT id FROM practice_sessions WHERE user_id = ? AND plan_id = ? AND plan_task = ? AND submitted_at IS NULL "
                     "ORDER BY id DESC LIMIT 1", (user_id, plan_id, task_key), one=True)
    if open_row:
        return get(user_id, open_row["id"])
    if task["kind"] == "test":
        return save_session(user_id, "test", "Math practice test", build_test(user_id, rng), bank.MODULE_MINUTES,
                            plan_id=plan_id, plan_task=task_key)
    if task["kind"] == "drill":
        skills = [task["skill"]]
        title = f"Week {week['n']}: {task['skill']['name']}"
    else:
        skills = week["focus"] + ([week["review"]] if week.get("review") else [])
        title = task["title"]
    if week["phase"] == "test":
        mix = week["mix"]
    else:
        mix = adjusted_mix(user_id, plan_id, week["difficulty"], task["count"])
    ids = draw_mix(user_id, skills, mix, rng)
    return save_session(user_id, "quiz", title, ids, 0, plan_id=plan_id, plan_task=task_key)


def get(user_id, session_id):
    return query("SELECT * FROM practice_sessions WHERE id = ? AND user_id = ?", (session_id, user_id), one=True)


def topics_of(item_ids):
    """The skill and domain topics these questions belong to, as keys like skill:algebra/linear-functions."""
    items = bank.all_items()
    keys = set()
    for item_id in item_ids:
        q = items[item_id]
        keys.add(f"skill:{q['domain_key']}/{q['skill_key']}")
        keys.add(f"domain:{q['domain_key']}")
    return keys


def topic_pool(topic):
    kind, _, rest = topic.partition(":")
    domain, _, skill = rest.partition("/")
    return bank.pool(domain, skill or None)


def topic_name(topic):
    kind, _, rest = topic.partition(":")
    domain, _, skill = rest.partition("/")
    return topic_title(domain, skill or None)


def mark_seen(user_id, item_ids):
    """Adds questions to the done list. Returns the topics this finished, skills first: [{kind, name}]."""
    stamp = now_iso()
    for item_id in item_ids:
        execute("INSERT INTO practice_seen (user_id, item_id, seen_at) VALUES (?, ?, ?) "
                "ON CONFLICT (user_id, item_id) DO NOTHING", (user_id, item_id, stamp))
    if not item_ids:
        return []
    seen = seen_ids(user_id)
    finished = []
    for topic in sorted(topics_of(item_ids), key=lambda t: (not t.startswith("skill:"), t)):
        if not all(i in seen for i in topic_pool(topic)):
            continue
        if query("SELECT 1 FROM practice_completions WHERE user_id = ? AND topic = ?", (user_id, topic), one=True):
            continue
        execute("INSERT INTO practice_completions (user_id, topic, completed_at) VALUES (?, ?, ?)", (user_id, topic, stamp))
        finished.append({"kind": topic.partition(":")[0], "name": topic_name(topic)})
    return finished


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
        "id": session["id"], "mode": session["mode"], "title": session["title"], "plan_task": session.get("plan_task"),
        "domain": session["domain"], "skill": session["skill"], "minutes": session["minutes"],
        "created_at": session["created_at"], "submitted": bool(session["submitted_at"]),
        "questions": [bank.public_question(items[i]) for i in ids],
        "checked": {k: bank.graded_question(items[ids[int(k)]], int(k), v) for k, v in checked.items()},
    }
    if session["results"]:
        out["result"] = json.loads(session["results"])
    if (session.get("plan_task") or "").startswith("ladder:"):
        from . import levels
        tag = levels.parse_tag(session["plan_task"])
        if tag:
            out["level"] = {"track": tag[0], "n": tag[1], "tier": levels.tier(tag[1]), "pass": levels.PASS, "top": levels.LEVELS}
    return out


def check(user_id, session, index, answer):
    """Grades one question in topic practice and locks it. Returns the graded question and any topics it finished."""
    items = bank.all_items()
    ids = json.loads(session["item_ids"])
    checked = json.loads(session["checked"] or "{}")
    key = str(index)
    if key not in checked:
        checked[key] = answer
        execute("UPDATE practice_sessions SET checked = ? WHERE id = ?", (json.dumps(checked), session["id"]))
        graded = bank.graded_question(items[ids[index]], index, answer)
        finished = mark_seen(user_id, [ids[index]])
        task = session.get("plan_task") or ""
        if task.startswith("review:"):
            # Reopened from the review queue: a right answer counts toward clearing it, a miss resets it.
            if graded["correct"]:
                graded["review"] = review.mark_right(user_id, int(task.split(":")[1]))
            else:
                add_to_review(user_id, [graded])
        else:
            add_to_review(user_id, [graded])
        return graded, finished
    return bank.graded_question(items[ids[index]], index, checked[key]), []


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
    result["finished"] = mark_seen(user_id, answered)
    unchecked = [q for q in result["questions"] if q["answered"] and q["index"] not in checked]
    task = session.get("plan_task") or ""
    if task.startswith("review:"):
        for q in unchecked:
            if q["correct"]:
                review.mark_right(user_id, int(task.split(":")[1]))
            else:
                add_to_review(user_id, [q])
    else:
        add_to_review(user_id, unchecked)

    if session["mode"] == "test":
        # Practice tests count toward the dashboard's score history, like the fixed tests.
        row = execute(
            "INSERT INTO test_attempts (user_id, test_id, seconds_used, correct, total, answers, results, submitted_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?) RETURNING id",
            (user_id, f"practice-{session['id']}", seconds, result["correct"], result["total"],
             json.dumps({str(k): v for k, v in answers.items()}), json.dumps(result), stamp))
        result["attempt_id"] = row["id"]
    if task.startswith("ladder:"):
        from . import levels  # levels builds on this module
        if levels.parse_tag(task):
            result["level"] = levels.result(user_id, session, result["correct"])
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
