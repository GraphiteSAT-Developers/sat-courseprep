"""The daily warm-up: 3 questions, about 5 minutes, meant to be done every day.

1. A missed question that's due in the review queue (a right answer counts toward clearing it).
2. A question from the student's weakest topic: recent practice accuracy, or the diagnostic.
3. A question where Desmos is the fastest route, to keep the calculator moves fresh.

Any slot that can't be filled (no review due, no data yet) takes a new question from anywhere.
"""
import json
import random
from datetime import date, timedelta

from ..db import query
from . import bank, practice

SIZE = 3
TITLE = "Daily warm-up"


def weakest_skill(user_id):
    """(domain key, skill key) with the lowest accuracy over the last 30 days of practice, or from the diagnostic."""
    items = bank.all_items()
    since = (date.today() - timedelta(days=30)).isoformat()
    tally = {}
    for r in query("SELECT item_ids, checked, results FROM practice_sessions WHERE user_id = ? AND created_at >= ?", (user_id, since)):
        ids = json.loads(r["item_ids"])
        graded = ([(q["id"], q["correct"]) for q in json.loads(r["results"])["questions"] if q["answered"]] if r["results"]
                  else [(ids[int(k)], bank.graded_question(items[ids[int(k)]], int(k), v)["correct"])
                        for k, v in json.loads(r["checked"] or "{}").items()])
        for item_id, ok in graded:
            q = items.get(item_id)
            if q:
                t = tally.setdefault((q["domain_key"], q["skill_key"]), [0, 0])
                t[0] += ok
                t[1] += 1
    scored = [(right / n, key) for key, (right, n) in tally.items() if n >= 2]
    if scored:
        return min(scored)[1]
    diag = query("SELECT results FROM diagnostics WHERE user_id = ? AND results IS NOT NULL ORDER BY id DESC LIMIT 1", (user_id,), one=True)
    if diag:
        skills = json.loads(diag["results"]).get("skills") or {}
        if skills:
            key = min(skills, key=lambda k: skills[k])
            for d in bank.topics():
                if any(s["key"] == key for s in d["skills"]):
                    return d["key"], key
    return None


def pick(user_id, today=None, rng=random):
    """The warm-up's question ids, and the review item behind the first one (or None)."""
    today = today or date.today()
    items = bank.all_items()
    seen = practice.seen_ids(user_id)
    picks, review_id = [], None

    for r in query("SELECT id, test_id FROM review_items WHERE user_id = ? AND cleared_at IS NULL AND due_on <= ? "
                   "AND test_id LIKE 'bank:%' ORDER BY due_on, id", (user_id, today.isoformat())):
        if r["test_id"][5:] in items:
            picks.append(r["test_id"][5:])
            review_id = r["id"]
            break

    def take(pool):
        pool = [i for i in pool if i not in picks]
        fresh = [i for i in pool if i not in seen]
        if fresh or pool:
            picks.append(rng.choice(sorted(fresh or pool)))
            return True
        return False

    weak = weakest_skill(user_id)
    if weak:
        take(bank.pool(*weak))
    weak_skill = weak[1] if weak else None
    take([i for i, q in items.items() if q["route"] == "desmos-primary" and q["skill_key"] != weak_skill and q["difficulty"] != "easy"])
    while len(picks) < SIZE and take(list(items)):
        pass
    return picks[:SIZE], review_id


def start(user_id, today=None, rng=random):
    ids, review_id = pick(user_id, today, rng)
    return practice.save_session(user_id, "warmup", TITLE, ids, 0, plan_task=f"warmup:{review_id}" if review_id else "warmup")


def status(user_id, today):
    """For the dashboard: today's warm-up (done or in progress) and how many days this week had one finished."""
    monday = today - timedelta(days=today.weekday())
    rows = query("SELECT id, item_ids, checked, submitted_at, created_at FROM practice_sessions WHERE user_id = ? AND mode = 'warmup' "
                 "AND created_at >= ? ORDER BY id", (user_id, monday.isoformat()))
    done_days, today_row = set(), None
    for r in rows:
        finished = bool(r["submitted_at"]) or len(json.loads(r["checked"] or "{}")) >= len(json.loads(r["item_ids"]))
        day = r["created_at"][:10]
        if finished:
            done_days.add(day)
        if day == today.isoformat():
            today_row = {"id": r["id"], "done": finished}
    return {"done_today": today.isoformat() in done_days, "days_this_week": len(done_days),
            "session_id": today_row["id"] if today_row and not today_row["done"] else None, "questions": SIZE, "minutes": 5}
