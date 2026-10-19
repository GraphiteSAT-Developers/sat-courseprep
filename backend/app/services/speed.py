"""Speed round: the same 10 quick questions for everyone each day, timed by the server.

The first round a student starts each day is their ranked run; later rounds that day are for practice.
Time runs on the server from the moment the questions are sent until the last answer arrives, and each
miss adds PENALTY_MS. Leaderboards show today's runs and the best run of each student this week, for
the student's state or the whole country.

Only students who turn on the leaderboard in Settings appear on it, and only by a nickname built from the
word lists below (no free text, so there's nothing to moderate). Everyone can still see where they'd place.
"""
import hashlib
import json
import random
import re
import time
from datetime import date, timedelta

from ..db import execute, now_iso, query
from . import bank, game, prefs

SIZE = 10
PENALTY_MS = 15_000         # each miss or skipped question
MAX_MS = 10 * 60 * 1000     # a run can't take longer than this
LIGHTNING_MS = 3 * 60 * 1000
BOARD_SIZE = 25

STATES = [
    ("AL", "Alabama"), ("AK", "Alaska"), ("AZ", "Arizona"), ("AR", "Arkansas"), ("CA", "California"), ("CO", "Colorado"),
    ("CT", "Connecticut"), ("DE", "Delaware"), ("DC", "District of Columbia"), ("FL", "Florida"), ("GA", "Georgia"),
    ("HI", "Hawaii"), ("ID", "Idaho"), ("IL", "Illinois"), ("IN", "Indiana"), ("IA", "Iowa"), ("KS", "Kansas"),
    ("KY", "Kentucky"), ("LA", "Louisiana"), ("ME", "Maine"), ("MD", "Maryland"), ("MA", "Massachusetts"),
    ("MI", "Michigan"), ("MN", "Minnesota"), ("MS", "Mississippi"), ("MO", "Missouri"), ("MT", "Montana"),
    ("NE", "Nebraska"), ("NV", "Nevada"), ("NH", "New Hampshire"), ("NJ", "New Jersey"), ("NM", "New Mexico"),
    ("NY", "New York"), ("NC", "North Carolina"), ("ND", "North Dakota"), ("OH", "Ohio"), ("OK", "Oklahoma"),
    ("OR", "Oregon"), ("PA", "Pennsylvania"), ("RI", "Rhode Island"), ("SC", "South Carolina"), ("SD", "South Dakota"),
    ("TN", "Tennessee"), ("TX", "Texas"), ("UT", "Utah"), ("VT", "Vermont"), ("VA", "Virginia"), ("WA", "Washington"),
    ("WV", "West Virginia"), ("WI", "Wisconsin"), ("WY", "Wyoming"),
]
STATE_NAMES = dict(STATES)

ADJECTIVES = ["Swift", "Quiet", "Bright", "Steady", "Clever", "Bold", "Calm", "Keen", "Lucky", "Nimble", "Sharp", "Sunny",
              "Brave", "Cosmic", "Crisp", "Daring", "Electric", "Golden", "Mighty", "Rapid", "Stellar", "Witty", "Zesty", "Silver"]
NOUNS = ["Parabola", "Vertex", "Tangent", "Radius", "Integer", "Fraction", "Slope", "Prism", "Vector", "Median", "Sigma",
         "Cosine", "Hexagon", "Axis", "Decimal", "Quotient", "Matrix", "Theorem", "Circle", "Ratio", "Pencil", "Compass",
         "Protractor", "Graph"]


# ---------- nicknames ----------
def roll_nicknames(n=3, rng=random):
    """Suggestions that always pass clean_nickname: a few word pairs, like "Electric Protractor", are too long."""
    out = []
    while len(out) < n:
        nick = f"{rng.choice(ADJECTIVES)} {rng.choice(NOUNS)} {rng.randint(10, 99)}"
        if len(nick) <= NICK_MAX:
            out.append(nick)
    return out


NICK_MIN, NICK_MAX = 3, 20
NICK_CHARS = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 ._'-]*$")


def valid_nickname(name):
    """A suggested nickname from the word lists (always allowed)."""
    parts = (name or "").split(" ")
    return (len(parts) == 3 and parts[0] in ADJECTIVES and parts[1] in NOUNS
            and parts[2].isdigit() and 10 <= int(parts[2]) <= 99)


def clean_nickname(name, user):
    """A nickname the student typed: 3 to 20 letters, numbers, spaces and . _ ' -, no curse words, not their
    real name or email, and not already taken. Returns it tidied up, or raises ValueError with the reason."""
    from . import wordfilter
    nick = " ".join(str(name or "").split())
    if not NICK_MIN <= len(nick) <= NICK_MAX:
        raise ValueError(f"Nicknames are {NICK_MIN} to {NICK_MAX} characters.")
    if not NICK_CHARS.match(nick):
        raise ValueError("Use letters, numbers, spaces and . _ ' - only.")
    if not wordfilter.is_clean(nick):
        raise ValueError(wordfilter.MESSAGE)
    squash = lambda t: re.sub(r"[^a-z0-9]", "", t.lower())
    real = squash(user["name"] or "")
    local = squash((user["email"] or "").split("@")[0])
    last = squash((user["name"] or "").split(" ")[-1]) if " " in (user["name"] or "").strip() else ""
    n = squash(nick)
    if (real and n == real) or (len(local) >= 4 and local in n) or (len(last) >= 3 and last in n):
        raise ValueError("Leaderboards are public, so pick a nickname that isn't your real name or email.")
    taken = query("SELECT 1 FROM users WHERE LOWER(nickname) = ? AND id != ?", (nick.lower(), user["id"]), one=True)
    if taken:
        raise ValueError("Someone already has that nickname. Try adding a number.")
    return nick


# ---------- the day's questions ----------
def _salt():
    from flask import current_app
    key = current_app.config.get("SECRET_KEY") or "graphite"
    return hashlib.sha256(f"speed:{key}".encode()).hexdigest()[:16]


def day_items(day):
    """Today's 10 questions: quick multiple choice, easy and medium, picked the same way for everyone."""
    pool = sorted(q["id"] for q in bank.all_items().values()
                  if q["type"] == "mc" and q["difficulty"] in ("easy", "medium") and q["domain_key"] in DOMAINS)
    rng = random.Random(f"{day}:{_salt()}")
    return rng.sample(pool, SIZE)


DOMAINS = {"algebra", "advanced-math", "psda", "geometry-trig"}


def now_ms():
    return int(time.time() * 1000)


# ---------- a run ----------
def get(user_id, run_id):
    return query("SELECT * FROM speed_runs WHERE id = ? AND user_id = ?", (run_id, user_id), one=True)


def public(run, now=None):
    items = bank.all_items()
    ids = json.loads(run["item_ids"])
    answers = {int(k): v for k, v in json.loads(run["answers"]).items()}
    out = {"id": run["id"], "day": run["day"], "ranked": bool(run["ranked"]), "total": run["total"],
           "questions": [bank.public_question(items[i]) for i in ids],
           "answered": {str(i): {"answer": a, "correct": bank.graded_question(items[ids[i]], i, a)["correct"],
                                 "answer_index": bank.graded_question(items[ids[i]], i, a)["answer_index"]}
                        for i, a in answers.items()},
           "elapsed_ms": min(MAX_MS, (now or now_ms()) - run["started_ms"]),
           "finished": run["finished_ms"] is not None, "penalty_ms": PENALTY_MS, "max_ms": MAX_MS}
    if run["finished_ms"] is not None:
        out["result"] = result_of(run)
    return out


def result_of(run):
    raw = run["finished_ms"] - run["started_ms"]
    return {"correct": run["correct"], "total": run["total"], "raw_ms": raw, "misses": run["total"] - run["correct"],
            "score_ms": run["score_ms"], "ranked": bool(run["ranked"])}


def start(user, today=None):
    """Picks up today's unfinished run if there is one, else starts a new one."""
    day = (today or date.today()).isoformat()
    t = now_ms()
    open_run = query("SELECT * FROM speed_runs WHERE user_id = ? AND day = ? AND finished_ms IS NULL ORDER BY id DESC LIMIT 1",
                     (user["id"], day), one=True)
    if open_run and t - open_run["started_ms"] < MAX_MS:
        return open_run
    if open_run:
        finish(user["id"], open_run, open_run["started_ms"] + MAX_MS)
    ranked = not query("SELECT 1 FROM speed_runs WHERE user_id = ? AND day = ? AND ranked = 1", (user["id"], day), one=True)
    row = execute("INSERT INTO speed_runs (user_id, day, item_ids, answers, started_ms, total, ranked, state, created_at) "
                  "VALUES (?, ?, ?, '{}', ?, ?, ?, ?, ?) RETURNING id",
                  (user["id"], day, json.dumps(day_items(day)), t, SIZE, 1 if ranked else 0, user["state"], now_iso()))
    return get(user["id"], row["id"])


def answer(user_id, run, index, value):
    """Records one answer (each question once). Returns (graded, run, report-or-None when this finished the run)."""
    items = bank.all_items()
    ids = json.loads(run["item_ids"])
    q = items[ids[index]]
    answers = json.loads(run["answers"])
    key = str(index)
    t = now_ms()
    fresh = key not in answers and t - run["started_ms"] <= MAX_MS
    if fresh:
        answers[key] = value
        execute("UPDATE speed_runs SET answers = ? WHERE id = ?", (json.dumps(answers), run["id"]))
        run = get(user_id, run["id"])
    g = bank.graded_question(q, index, answers.get(key, value))
    if fresh:
        from . import history
        history.question(user_id, ids[index], "speed", f"speed-{run['id']}", value, g["correct"])
    report = None
    if len(answers) >= len(ids) or t - run["started_ms"] > MAX_MS:
        run, report = finish(user_id, run, t)
    return {"index": index, "correct": g["correct"], "answer_index": g["answer_index"]}, run, report


def finish(user_id, run, t=None):
    """Ends a run: time on the server's clock, plus PENALTY_MS for each miss or skip."""
    if run["finished_ms"] is not None:
        return run, None
    t = min(t or now_ms(), run["started_ms"] + MAX_MS)
    items = bank.all_items()
    ids = json.loads(run["item_ids"])
    answers = json.loads(run["answers"])
    correct = sum(1 for k, v in answers.items() if bank.graded_question(items[ids[int(k)]], int(k), v)["correct"])
    raw = t - run["started_ms"]
    score = raw + PENALTY_MS * (len(ids) - correct)
    execute("UPDATE speed_runs SET finished_ms = ?, correct = ?, score_ms = ? WHERE id = ?", (t, correct, score, run["id"]))
    execute("INSERT INTO activity (user_id, kind, seconds, detail, at) VALUES (?, 'speed_round', ?, ?, ?)",
            (user_id, raw // 1000, f"speed-{run['id']}", now_iso()))
    run = get(user_id, run["id"])
    xp_before, _ = game.totals(user_id)
    xp = game.XP_SPEED_DONE + game.XP_SPEED_RIGHT * correct
    coins = game.COINS_SPEED_DONE if run["ranked"] else 0
    s = game.award(user_id, "speed", xp, coins, f"speed-{run['id']}")
    badges = [game.earn_badge(user_id, "off_the_line")]
    if correct == len(ids) and raw <= LIGHTNING_MS:
        badges.append(game.earn_badge(user_id, "lightning"))
    return run, game.report(user_id, xp_before, xp, coins, badges, s)


# ---------- leaderboards ----------
def _week_start(day):
    return day - timedelta(days=day.weekday())


def board(viewer, scope="state", period="today", today=None):
    """Top runs, best per student. scope: state or nation. period: today or week (Monday to now)."""
    today = today or date.today()
    since = today if period == "today" else _week_start(today)
    state = viewer["state"] if scope == "state" else None
    if scope == "state" and not state:
        return {"scope": scope, "period": period, "needs_state": True, "rows": [], "you": None}
    sql = ("SELECT r.user_id, MIN(r.score_ms) AS score_ms FROM speed_runs r JOIN users u ON u.id = r.user_id "
           "WHERE r.ranked = 1 AND r.finished_ms IS NOT NULL AND r.day >= ? AND r.day <= ?")
    params = [since.isoformat(), today.isoformat()]
    if state:
        sql += " AND u.state = ?"
        params.append(state)
    best = query(sql + " GROUP BY r.user_id", tuple(params))
    best_by_user = {r["user_id"]: r["score_ms"] for r in best}
    users = {}
    if best_by_user:
        marks = ",".join("?" for _ in best_by_user)
        for u in query(f"SELECT id, nickname, board_opt_in, title, frame, state, prefs FROM users WHERE id IN ({marks})",
                       tuple(best_by_user)):
            users[u["id"]] = u
    shown = sorted((uid for uid, u in users.items() if u["board_opt_in"] and u["nickname"]),
                   key=lambda uid: (best_by_user[uid], uid))
    detail = _run_details(best_by_user, since, today)
    rows = []
    for i, uid in enumerate(shown[:BOARD_SIZE]):
        u = users[uid]
        rows.append(dict(detail[uid], rank=i + 1, nickname=u["nickname"], title=u["title"], frame=u["frame"],
                         state=u["state"], you=uid == viewer["id"], avatar=prefs.drawn_avatar(u)))
    you = None
    mine = best_by_user.get(viewer["id"])
    if mine is not None:
        visible = bool(viewer["board_opt_in"] and viewer["nickname"])
        place = (shown.index(viewer["id"]) + 1) if visible else 1 + sum(1 for uid in shown if best_by_user[uid] < mine)
        you = dict(detail[viewer["id"]], rank=place, visible=visible, of=len(shown) + (0 if visible else 1))
    return {"scope": scope, "period": period, "state": state, "state_name": STATE_NAMES.get(state) if state else None,
            "rows": rows, "you": you, "players": len(shown)}


def _run_details(best_by_user, since, today):
    """The run behind each student's best score: correct answers and raw time."""
    out = {}
    for uid, score in best_by_user.items():
        r = query("SELECT correct, total, started_ms, finished_ms, score_ms, day FROM speed_runs WHERE user_id = ? "
                  "AND ranked = 1 AND score_ms = ? AND day >= ? AND day <= ? ORDER BY id LIMIT 1",
                  (uid, score, since.isoformat(), today.isoformat()), one=True)
        out[uid] = {"score_ms": r["score_ms"], "raw_ms": r["finished_ms"] - r["started_ms"], "correct": r["correct"],
                    "total": r["total"], "day": r["day"]}
    return out


def overview(user, today=None):
    today = today or date.today()
    day = today.isoformat()
    ranked = query("SELECT * FROM speed_runs WHERE user_id = ? AND day = ? AND ranked = 1", (user["id"], day), one=True)
    best = query("SELECT MIN(score_ms) AS s FROM speed_runs WHERE user_id = ? AND ranked = 1 AND finished_ms IS NOT NULL",
                 (user["id"],), one=True)["s"]
    runs = query("SELECT * FROM speed_runs WHERE user_id = ? AND finished_ms IS NOT NULL ORDER BY id DESC LIMIT 5", (user["id"],))
    return {"day": day, "size": SIZE, "penalty_ms": PENALTY_MS, "max_ms": MAX_MS,
            "ranked_today": None if not ranked else (result_of(ranked) if ranked["finished_ms"] is not None else {"open": True}),
            "personal_best_ms": best,
            "recent": [dict(result_of(r), day=r["day"]) for r in runs],
            "board_profile": {"opt_in": bool(user["board_opt_in"]), "nickname": user["nickname"], "state": user["state"],
                              "state_name": STATE_NAMES.get(user["state"]) if user["state"] else None}}
