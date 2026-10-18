"""Mock tests: a full SAT section in two adaptive modules, like the digital SAT.

Math: Module 1 has 22 questions in 35 minutes with a broad mix of easy, medium and hard questions.
How Module 1 goes decides Module 2 (22 questions, 35 minutes): a harder module after a strong
Module 1, an easier one otherwise. Both modules use questions the student has never seen, and
Module 2 never repeats Module 1. Every question in a mock goes on the done list, answered or not,
so the next mock test is all new questions too.

On test day the 10-minute break comes between Reading and Writing and Math. A Math mock can start
with that break (the student can end it early), so the timing feels the same as the real thing.
Reading and Writing mocks are listed as coming soon.

Each module is an ordinary practice session (services/practice.py) tagged mock:<mock id>:<module>.
The mock counts as one practice test in the score history, with an estimated section score.
"""
import json
import random
from datetime import datetime, timezone

from ..db import execute, now_iso, query
from . import bank, practice

SECTIONS = {
    "math": {"name": "Math", "questions": 22, "minutes": 35, "modules": 2, "ready": True},
    "rw": {"name": "Reading and Writing", "questions": 27, "minutes": 32, "modules": 2, "ready": False},
}
BREAK_SECONDS = 10 * 60
ROUTE_AT = 14  # right answers in Module 1 (of 22) for the harder Module 2
MIX = {
    "m1": {"easy": 7, "medium": 8, "hard": 7},
    "harder": {"easy": 3, "medium": 8, "hard": 11},
    "easier": {"easy": 10, "medium": 9, "hard": 3},
}
NEIGHBORS = {"easy": ["medium", "hard"], "medium": ["easy", "hard"], "hard": ["medium", "easy"]}


def _stamp():
    return datetime.now(timezone.utc)


def _parse(iso):
    return datetime.strptime(iso, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def _split(n, mix):
    """n questions split in the proportions of mix, summing exactly to n."""
    total = sum(mix.values())
    raw = {d: n * c / total for d, c in mix.items()}
    out = {d: int(v) for d, v in raw.items()}
    for d in sorted(raw, key=lambda d: raw[d] - out[d], reverse=True)[:n - sum(out.values())]:
        out[d] += 1
    return out


def build_module(user_id, mix, exclude=(), rng=random):
    """22 questions in the real domain mix and the given difficulty mix, new to the student, easiest first."""
    items = bank.all_items()
    seen = practice.seen_ids(user_id) | set(exclude)
    picked = []
    # Each domain gets its share of each difficulty; the domain mix comes first, like the real test.
    domains = list(bank.MODULE_MIX.items())
    per_domain = {d: _split(n, mix) for d, n in domains}
    for domain, n in domains:
        pool = bank.pool(domain=domain)
        fresh = {lv: [i for i in pool if i not in seen and i not in picked and items[i]["difficulty"] == lv] for lv in ("easy", "medium", "hard")}
        for lv in fresh:
            rng.shuffle(fresh[lv])
        for lv, want in per_domain[domain].items():
            for source in [lv] + NEIGHBORS[lv]:
                while want and fresh[source]:
                    picked.append(fresh[source].pop())
                    want -= 1
            if want:
                # Every question in this domain is done: reuse done ones, never the ones in this mock.
                rest = [i for i in pool if i not in picked and i not in set(exclude)]
                rng.shuffle(rest)
                picked += rest[:want]
    picked.sort(key=lambda i: bank.DIFFICULTY_ORDER[items[i]["difficulty"]])
    return picked


def tag(mock_id, module):
    return f"mock:{mock_id}:{module}"


def parse_tag(task):
    parts = (task or "").split(":")
    if len(parts) == 3 and parts[0] == "mock" and parts[1].isdigit() and parts[2] in ("1", "2"):
        return int(parts[1]), int(parts[2])
    return None


def get(user_id, mock_id):
    return query("SELECT * FROM mock_tests WHERE id = ? AND user_id = ?", (mock_id, user_id), one=True)


def create(user_id, section="math", with_break=True, rng=random):
    stamp = now_iso()
    row = execute("INSERT INTO mock_tests (user_id, section, status, with_break, created_at) VALUES (?, ?, ?, ?, ?) RETURNING id",
                  (user_id, section, "break" if with_break else "module1", 1 if with_break else 0, stamp))
    mock_id = row["id"]
    ids = build_module(user_id, MIX["m1"], rng=rng)
    s = practice.save_session(user_id, "test", "Math: Module 1", ids, SECTIONS[section]["minutes"], plan_task=tag(mock_id, 1))
    execute("UPDATE mock_tests SET m1_session = ? WHERE id = ?", (s["id"], mock_id))
    return get(user_id, mock_id)


def break_left(m, now=None):
    if not m["with_break"] or m["break_ended_at"]:
        return 0
    if not m["break_started_at"]:
        return BREAK_SECONDS
    used = ((now or _stamp()) - _parse(m["break_started_at"])).total_seconds()
    return max(0, int(BREAK_SECONDS - used))


def on_break(m):
    return m["status"] == "break" and break_left(m) > 0


def break_action(user_id, m, action):
    """Starts the break clock (once), or ends the break early. A break that runs out ends by itself."""
    if m["status"] != "break":
        return get(user_id, m["id"])
    if action == "start" and not m["break_started_at"]:
        execute("UPDATE mock_tests SET break_started_at = ? WHERE id = ?", (now_iso(), m["id"]))
    elif action == "end" or break_left(m) == 0:
        execute("UPDATE mock_tests SET break_ended_at = ?, status = 'module1' WHERE id = ?", (now_iso(), m["id"]))
    return get(user_id, m["id"])


def estimate(route, raw):
    """An estimated section score, 200 to 800, from the right answers in both modules (44 in all).

    The harder Module 2 opens the top of the scale; the easier one tops out lower, as on the real test.
    This is an estimate from our own question bank, not an official College Board score.
    """
    if route == "harder":
        score = 400 + 400 * max(0, raw - ROUTE_AT) / (44 - ROUTE_AT)
    else:
        top = ROUTE_AT - 1 + 22
        score = 200 + 410 * min(raw, top) / top
    return int(round(score / 10.0) * 10)


def _answers_from(result):
    """The raw answers in a graded result: choice index for multiple choice, the typed text otherwise."""
    out = {}
    for q in result.get("questions", []):
        if not q.get("answered"):
            continue
        if q["type"] == "mc":
            out[q["index"]] = bank.LETTERS.index(q["your_answer"])
        else:
            out[q["index"]] = q["your_answer"]
    return out


def after_module(user_id, session, result, rng=random):
    """Called after a module is submitted. Module 1 builds Module 2; Module 2 finishes the mock."""
    found = parse_tag(session.get("plan_task") if hasattr(session, "get") else session["plan_task"])
    if not found:
        return result
    mock_id, module = found
    m = get(user_id, mock_id)
    if not m:
        return result
    ids = json.loads(session["item_ids"])
    practice.mark_seen(user_id, ids)  # the whole module is used up, answered or not
    if module == 1:
        if m["m2_session"]:
            return dict(result, mock={"id": mock_id, "module": 1, "next_session": m["m2_session"]})
        route = "harder" if result["correct"] >= ROUTE_AT else "easier"
        ids2 = build_module(user_id, MIX[route], exclude=ids, rng=rng)
        s2 = practice.save_session(user_id, "test", "Math: Module 2", ids2, SECTIONS[m["section"]]["minutes"], plan_task=tag(mock_id, 2))
        execute("UPDATE mock_tests SET m2_session = ?, route = ?, m1_correct = ?, status = 'module2' WHERE id = ?",
                (s2["id"], route, result["correct"], mock_id))
        return dict(result, mock={"id": mock_id, "module": 1, "next_session": s2["id"]})
    # Module 2: grade the whole section together and save it as one practice test.
    s1 = practice.get(user_id, m["m1_session"])
    r1 = json.loads(s1["results"]) if s1 and s1["results"] else {"questions": [], "seconds_used": 0}
    ids1 = json.loads(s1["item_ids"]) if s1 else []
    answers = _answers_from(r1)
    answers.update({len(ids1) + k: v for k, v in _answers_from(result).items()})
    combined = bank.grade(ids1 + ids, answers)
    for q in combined["questions"]:
        q["module"] = 1 if q["index"] < len(ids1) else 2
    score = estimate(m["route"], combined["correct"])
    stamp = now_iso()
    combined.update({"seconds_used": (r1.get("seconds_used") or 0) + (result.get("seconds_used") or 0), "mode": "mock",
                     "title": "Math mock test", "submitted_at": stamp, "finished": result.get("finished", []),
                     "score": score, "route": m["route"],
                     "modules": [{"n": 1, "correct": m["m1_correct"], "total": len(ids1)},
                                 {"n": 2, "correct": result["correct"], "total": len(ids), "route": m["route"]}]})
    attempt = execute(
        "INSERT INTO test_attempts (user_id, test_id, seconds_used, correct, total, answers, results, submitted_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?) RETURNING id",
        (user_id, f"mock-{mock_id}", combined["seconds_used"], combined["correct"], combined["total"],
         json.dumps({str(k): v for k, v in answers.items()}), json.dumps(combined), stamp))
    execute("UPDATE mock_tests SET m2_correct = ?, score = ?, status = 'done', finished_at = ? WHERE id = ?",
            (result["correct"], score, stamp, mock_id))
    combined["attempt_id"] = attempt["id"]
    combined["mock"] = {"id": mock_id, "module": 2, "done": True}
    # Module 2's page shows the whole section from now on, including after a reload.
    execute("UPDATE practice_sessions SET results = ? WHERE id = ?", (json.dumps(combined), session["id"]))
    return combined


def public(m):
    return {"id": m["id"], "section": m["section"], "section_name": SECTIONS[m["section"]]["name"], "status": m["status"],
            "with_break": bool(m["with_break"]), "break_seconds": BREAK_SECONDS, "break_left": break_left(m),
            "break_started": bool(m["break_started_at"]), "m1_session": m["m1_session"], "m2_session": m["m2_session"],
            "score": m["score"], "route": m["route"] if m["status"] == "done" else None,
            "correct": (m["m1_correct"] or 0) + (m["m2_correct"] or 0) if m["status"] == "done" else None,
            "created_at": m["created_at"], "finished_at": m["finished_at"]}


def for_session(user_id, session):
    """The mock a module belongs to, for the test page: which module, and the break."""
    found = parse_tag(session["plan_task"])
    if not found:
        return None
    m = get(user_id, found[0])
    if not m:
        return None
    if m["status"] == "break" and break_left(m) == 0 and m["break_started_at"]:
        m = break_action(user_id, m, "end")
    return dict(public(m), module=found[1], modules=SECTIONS[m["section"]]["modules"])


def overview(user_id):
    rows = query("SELECT * FROM mock_tests WHERE user_id = ? ORDER BY id DESC LIMIT 10", (user_id,))
    return {"sections": [dict(v, key=k) for k, v in SECTIONS.items()], "break_minutes": BREAK_SECONDS // 60,
            "recent": [public(r) for r in rows]}
