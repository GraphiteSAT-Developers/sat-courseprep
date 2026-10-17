"""Rewards: XP, ranks, coins, a daily streak, badges, and items to buy with coins.

Every reward is a row in xp_events, so totals are sums and can't drift. Spending coins is a row with
negative coins. A day counts toward the streak when the student earns any XP that day (Level up, a speed
round, a focus session or a lesson).

All the numbers live here. The site build copies RANKS, BADGES and SHOP into the preview, and
website/src/play-local.js applies the same rules there, so change both together.
"""
from datetime import date, timedelta

from ..db import execute, now_iso, query

# ---------- Level up ----------
XP_RIGHT = 10          # a right answer
XP_MISS = 2            # a miss still counts for something
COMBO_STEP = 2         # each right answer in a row adds this much...
COMBO_CAP = 10         # ...up to this
XP_BOSS = 40           # extra for the boss question (the last, hardest question of a level)
COINS_RIGHT = 1
COINS_BOSS = 10
XP_LEVEL_DONE = 20     # finishing a level set
XP_LEVEL_PASS = 50     # passing it
XP_FIRST_CLEAR = 50    # passing a level for the first time
COINS_FIRST_CLEAR = 5  # times the level number
XP_PERFECT = 50        # every question right

# ---------- the other activities ----------
XP_SPEED_RIGHT = 3
XP_SPEED_DONE = 10
COINS_SPEED_DONE = 5
XP_FOCUS_MINUTE = 1
COINS_FOCUS_DONE = 5
XP_LESSON_FIRST = 40
COINS_LESSON_FIRST = 10
XP_LESSON_REPLAY = 10
XP_RECALL_PASS = 20
COINS_RECALL_PASS = 5
XP_RECALL_TRY = 5

# Coins for reaching a streak length (once per streak).
STREAK_COINS = {3: 20, 7: 50, 14: 100, 30: 250, 60: 400, 100: 750}

RANKS = [
    (0, "Blank Page"), (150, "Doodler"), (400, "Sketcher"), (800, "Drafter"), (1500, "Outliner"),
    (2500, "Sharp Point"), (4000, "Fine Liner"), (6000, "Ink Master"), (9000, "Graphite Legend"),
]

BADGES = [
    {"key": "first_steps", "name": "First Steps", "how": "Finish your first Level up set."},
    {"key": "on_a_roll", "name": "On a Roll", "how": "Get 5 Level up questions right in a row."},
    {"key": "boss_slayer", "name": "Boss Slayer", "how": "Beat a boss question."},
    {"key": "boss_hunter", "name": "Boss Hunter", "how": "Beat 10 boss questions."},
    {"key": "flawless", "name": "Flawless", "how": "Get every question right on a level."},
    {"key": "top_score", "name": "Top Score", "how": "Pass level 9 or 10 in any track."},
    {"key": "track_cleared", "name": "Track Cleared", "how": "Pass all 10 levels in a track."},
    {"key": "streak_3", "name": "Warmed Up", "how": "Earn XP 3 days in a row."},
    {"key": "streak_7", "name": "Week Streak", "how": "Earn XP 7 days in a row."},
    {"key": "streak_30", "name": "Month Streak", "how": "Earn XP 30 days in a row."},
    {"key": "off_the_line", "name": "Off the Line", "how": "Finish a speed round."},
    {"key": "lightning", "name": "Lightning", "how": "Finish a speed round with no misses in under 3 minutes."},
    {"key": "deep_focus", "name": "Deep Focus", "how": "Finish a focus session."},
    {"key": "in_the_zone", "name": "In the Zone", "how": "Finish 10 focus sessions."},
    {"key": "recall_rookie", "name": "Recall Rookie", "how": "Finish a lesson."},
    {"key": "memory_palace", "name": "Memory Palace", "how": "Master 3 lessons with recall checks."},
    {"key": "total_recall", "name": "Total Recall", "how": "Finish every lesson."},
    {"key": "fresh_look", "name": "Fresh Look", "how": "Buy something in the shop."},
]
BADGE_KEYS = {b["key"] for b in BADGES}

# What coins buy. Accents show up in Settings > Appearance once bought; frames go around your profile
# picture; titles show under your nickname on the leaderboard and on your rewards card.
SHOP = [
    {"key": "accent:rose", "kind": "accent", "value": "rose", "name": "Rose Quartz", "price": 150, "about": "A soft pink accent color."},
    {"key": "accent:blueprint", "kind": "accent", "value": "blueprint", "name": "Blueprint", "price": 150, "about": "A bright drafting-table cyan."},
    {"key": "accent:ember", "kind": "accent", "value": "ember", "name": "Ember", "price": 200, "about": "A glowing orange-red."},
    {"key": "frame:sharpened", "kind": "frame", "value": "sharpened", "name": "Sharpened ring", "price": 60, "about": "A solid ring in your accent color."},
    {"key": "frame:graph", "kind": "frame", "value": "graph", "name": "Graph paper ring", "price": 100, "about": "A dashed ring, like graph paper."},
    {"key": "frame:double", "kind": "frame", "value": "double", "name": "Double line", "price": 120, "about": "Two thin rings."},
    {"key": "frame:gold", "kind": "frame", "value": "gold", "name": "Gold ring", "price": 300, "about": "A gold ring. Show it off."},
    {"key": "title:calculator", "kind": "title", "value": "Calculator Whisperer", "name": "Calculator Whisperer", "price": 80, "about": "A title for your leaderboard name."},
    {"key": "title:parabola", "kind": "title", "value": "Parabola Tamer", "name": "Parabola Tamer", "price": 80, "about": "A title for your leaderboard name."},
    {"key": "title:ratio", "kind": "title", "value": "Ratio Wrangler", "name": "Ratio Wrangler", "price": 80, "about": "A title for your leaderboard name."},
    {"key": "title:triangle", "kind": "title", "value": "Triangle Tactician", "name": "Triangle Tactician", "price": 120, "about": "A title for your leaderboard name."},
    {"key": "title:boss", "kind": "title", "value": "Boss Breaker", "name": "Boss Breaker", "price": 200, "about": "A title for your leaderboard name."},
    {"key": "title:legend", "kind": "title", "value": "Unhurried Legend", "name": "Unhurried Legend", "price": 400, "about": "A title for your leaderboard name."},
]
SHOP_BY_KEY = {s["key"]: s for s in SHOP}
FRAMES = {s["value"] for s in SHOP if s["kind"] == "frame"}
TITLES = {s["value"] for s in SHOP if s["kind"] == "title"}
SHOP_ACCENTS = {s["value"]: s["key"] for s in SHOP if s["kind"] == "accent"}


def today():
    return date.today()


# ---------- totals ----------
def totals(user_id):
    row = query("SELECT COALESCE(SUM(xp), 0) AS xp, COALESCE(SUM(coins), 0) AS coins FROM xp_events WHERE user_id = ?",
                (user_id,), one=True)
    return int(row["xp"]), int(row["coins"])


def rank_for(xp):
    """The rank for this much XP, and how far it is to the next one."""
    i = max(n for n, (floor, _) in enumerate(RANKS) if xp >= floor)
    floor, name = RANKS[i]
    out = {"n": i + 1, "name": name, "floor": floor, "of": len(RANKS)}
    if i + 1 < len(RANKS):
        nxt, nxt_name = RANKS[i + 1]
        out.update({"next_at": nxt, "next_name": nxt_name, "progress": round((xp - floor) / (nxt - floor), 3)})
    else:
        out.update({"next_at": None, "next_name": None, "progress": 1})
    return out


def streak(user_id, on=None):
    """{days, today}: days in a row with XP, counting today if earned, else ending yesterday."""
    on = on or today()
    rows = query("SELECT DISTINCT day FROM xp_events WHERE user_id = ? AND day >= ? AND xp > 0",
                 (user_id, (on - timedelta(days=400)).isoformat()))
    days = {r["day"] for r in rows}
    earned_today = on.isoformat() in days
    d = on if earned_today else on - timedelta(days=1)
    n = 0
    while d.isoformat() in days:
        n += 1
        d -= timedelta(days=1)
    return {"days": n, "today": earned_today}


# ---------- earning ----------
def award(user_id, kind, xp=0, coins=0, detail=None):
    """Records a reward. Returns any streak reward it set off: {days, coins, badges}."""
    on = today()
    before = streak(user_id, on)
    execute("INSERT INTO xp_events (user_id, kind, xp, coins, detail, day, at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_id, kind, xp, coins, detail, on.isoformat(), now_iso()))
    if xp <= 0 or before["today"]:
        return None
    days = before["days"] + 1  # the first XP of the day extends the streak
    out = {"days": days, "coins": 0, "badges": []}
    if days in STREAK_COINS:
        execute("INSERT INTO xp_events (user_id, kind, xp, coins, detail, day, at) VALUES (?, 'streak', 0, ?, ?, ?, ?)",
                (user_id, STREAK_COINS[days], f"{days}-day streak", on.isoformat(), now_iso()))
        out["coins"] = STREAK_COINS[days]
    for need, key in ((3, "streak_3"), (7, "streak_7"), (30, "streak_30")):
        if days >= need:
            b = earn_badge(user_id, key)
            if b:
                out["badges"].append(b)
    return out


def earn_badge(user_id, key):
    """Gives a badge once. Returns it if it's new, else None."""
    if key not in BADGE_KEYS or query("SELECT 1 FROM badges WHERE user_id = ? AND badge = ?", (user_id, key), one=True):
        return None
    execute("INSERT INTO badges (user_id, badge, earned_at) VALUES (?, ?, ?) ON CONFLICT (user_id, badge) DO NOTHING",
            (user_id, key, now_iso()))
    return next(b for b in BADGES if b["key"] == key)


def count(user_id, kind):
    return query("SELECT COUNT(*) AS n FROM xp_events WHERE user_id = ? AND kind = ?", (user_id, kind), one=True)["n"]


def report(user_id, xp_before, gained_xp, gained_coins, badges=(), streak_info=None, extra=None):
    """What the page shows after earning something: what was gained, new totals, and any rank-up."""
    xp, coins = totals(user_id)
    rank = rank_for(xp)
    out = {"xp": gained_xp, "coins": gained_coins, "total_xp": xp, "total_coins": coins, "rank": rank,
           "rank_up": rank["n"] > rank_for(xp_before)["n"], "badges": [b for b in badges if b],
           "streak": streak_info}
    if streak_info:
        out["badges"] += streak_info["badges"]
        out["coins"] += streak_info["coins"]
    out.update(extra or {})
    return out


# ---------- Level up hooks ----------
def level_check(user_id, session, index, correct, checked_correct, total):
    """One checked Level up answer. checked_correct is {index: right?} for every checked question so far.
    The combo is the run of right answers ending at this question; the last question is the boss."""
    xp_before, _ = totals(user_id)
    boss = index == total - 1
    combo = 0
    i = index
    while i >= 0 and checked_correct.get(i):
        combo += 1
        i -= 1
    badges = []
    if correct:
        xp = XP_RIGHT + min(COMBO_CAP, COMBO_STEP * (combo - 1))
        coins = COINS_RIGHT
        if boss:
            xp += XP_BOSS
            coins += COINS_BOSS
        if combo >= 5:
            badges.append(earn_badge(user_id, "on_a_roll"))
    else:
        xp, coins = XP_MISS, 0
    s = award(user_id, "boss" if boss and correct else "level_q", xp, coins, f"practice-{session['id']}:{index}")
    if boss and correct:
        badges.append(earn_badge(user_id, "boss_slayer"))
        if count(user_id, "boss") >= 10:
            badges.append(earn_badge(user_id, "boss_hunter"))
    return report(user_id, xp_before, xp, coins, badges, s, {"combo": combo if correct else 0, "boss": boss, "correct": correct})


def level_finish(user_id, session, level, correct, total, passed, first_clear, top):
    """A finished Level up set: finishing, passing, a first clear and a perfect score each pay out."""
    xp_before, _ = totals(user_id)
    xp, coins = XP_LEVEL_DONE, 0
    lines = [("Finished the set", XP_LEVEL_DONE, 0)]
    badges = [earn_badge(user_id, "first_steps")]
    if passed:
        xp += XP_LEVEL_PASS
        lines.append(("Passed level " + str(level), XP_LEVEL_PASS, 0))
        if first_clear:
            xp += XP_FIRST_CLEAR
            coins += COINS_FIRST_CLEAR * level
            lines.append(("First clear", XP_FIRST_CLEAR, COINS_FIRST_CLEAR * level))
        if level >= 9:
            badges.append(earn_badge(user_id, "top_score"))
        if level == top:
            badges.append(earn_badge(user_id, "track_cleared"))
    if correct == total:
        xp += XP_PERFECT
        lines.append(("Perfect set", XP_PERFECT, 0))
        badges.append(earn_badge(user_id, "flawless"))
    s = award(user_id, "level_done", xp, coins, f"practice-{session['id']}")
    session_xp = query("SELECT COALESCE(SUM(xp), 0) AS xp, COALESCE(SUM(coins), 0) AS c FROM xp_events "
                       "WHERE user_id = ? AND detail LIKE ? AND kind IN ('level_q', 'boss')",
                       (user_id, f"practice-{session['id']}:%"), one=True)
    lines.insert(0, ("Answers, combos and the boss", int(session_xp["xp"]), int(session_xp["c"])))
    return report(user_id, xp_before, xp, coins, badges, s,
                  {"lines": [{"label": l, "xp": x, "coins": c} for l, x, c in lines],
                   "set_xp": int(session_xp["xp"]) + xp, "set_coins": int(session_xp["c"]) + coins})


# ---------- shop ----------
def owned(user_id):
    return {r["item"] for r in query("SELECT item FROM inventory WHERE user_id = ?", (user_id,))}


def buy(user_id, key):
    """Buys an item. Returns the report, or raises ValueError with a message for the student."""
    item = SHOP_BY_KEY.get(key)
    if not item:
        raise ValueError("That item isn't in the shop.")
    if key in owned(user_id):
        raise ValueError("You already have that.")
    xp, coins = totals(user_id)
    if coins < item["price"]:
        raise ValueError(f"You need {item['price'] - coins} more coins for that.")
    execute("INSERT INTO inventory (user_id, item, bought_at) VALUES (?, ?, ?)", (user_id, key, now_iso()))
    execute("INSERT INTO xp_events (user_id, kind, xp, coins, detail, day, at) VALUES (?, 'shop', 0, ?, ?, ?, ?)",
            (user_id, -item["price"], key, today().isoformat(), now_iso()))
    badge = earn_badge(user_id, "fresh_look")
    return report(user_id, xp, 0, -item["price"], [badge])


def equip(user_id, kind, value):
    """Wears a frame or title (None takes it off). Raises ValueError if it isn't owned."""
    if kind not in ("frame", "title"):
        raise ValueError("You can only wear frames and titles.")
    if value is not None:
        item = next((s for s in SHOP if s["kind"] == kind and s["value"] == value), None)
        if not item or item["key"] not in owned(user_id):
            raise ValueError("Buy that in the shop first.")
    execute(f"UPDATE users SET {kind} = ? WHERE id = ?", (value, user_id))  # kind is one of two fixed names


def accent_allowed(user_id, accent):
    key = SHOP_ACCENTS.get(accent)
    return key is None or key in owned(user_id)


# ---------- what the pages show ----------
def summary(user_id):
    xp, coins = totals(user_id)
    return {"xp": xp, "coins": coins, "rank": rank_for(xp), "streak": streak(user_id)}


def profile(user):
    """Everything the rewards page shows."""
    uid = user["id"]
    out = summary(uid)
    earned = {r["badge"]: r["earned_at"] for r in query("SELECT badge, earned_at FROM badges WHERE user_id = ?", (uid,))}
    mine = owned(uid)
    keys = user.keys()
    worn = {"frame": user["frame"] if "frame" in keys else None, "title": user["title"] if "title" in keys else None,
            "accent": user["accent"] if "accent" in keys else None}
    out["badges"] = [dict(b, earned_at=earned.get(b["key"])) for b in BADGES]
    out["shop"] = [dict(s, owned=s["key"] in mine, worn=worn.get(s["kind"]) == s["value"]) for s in SHOP]
    out["frame"], out["title"] = worn["frame"], worn["title"]
    out["ranks"] = [{"at": a, "name": n} for a, n in RANKS]
    out["streak_coins"] = [{"days": d, "coins": c} for d, c in sorted(STREAK_COINS.items())]
    out["earn"] = earn_table()
    out["recent"] = [dict(r) for r in query(
        "SELECT kind, xp, coins, detail, at FROM xp_events WHERE user_id = ? ORDER BY id DESC LIMIT 12", (uid,))]
    return out


def earn_table():
    """How to earn, for the rewards page: [{what, xp, coins}] (xp and coins are display text)."""
    return [
        {"what": "Level up: a right answer", "xp": f"{XP_RIGHT}", "coins": f"{COINS_RIGHT}"},
        {"what": "Level up: answers in a row (combo)", "xp": f"+{COMBO_STEP} each, up to +{COMBO_CAP}", "coins": ""},
        {"what": "Level up: the boss question", "xp": f"+{XP_BOSS}", "coins": f"+{COINS_BOSS}"},
        {"what": "Level up: pass a level for the first time", "xp": f"{XP_LEVEL_DONE + XP_LEVEL_PASS + XP_FIRST_CLEAR}", "coins": f"{COINS_FIRST_CLEAR} × the level"},
        {"what": "Level up: a perfect set", "xp": f"+{XP_PERFECT}", "coins": ""},
        {"what": "Speed round", "xp": f"{XP_SPEED_DONE} + {XP_SPEED_RIGHT} per right answer", "coins": f"{COINS_SPEED_DONE} (first round of the day)"},
        {"what": "Focus session, finished", "xp": f"{XP_FOCUS_MINUTE} per minute", "coins": f"{COINS_FOCUS_DONE}"},
        {"what": "Lesson, first time", "xp": f"{XP_LESSON_FIRST}", "coins": f"{COINS_LESSON_FIRST}"},
        {"what": "Recall check, passed on its day", "xp": f"{XP_RECALL_PASS}", "coins": f"{COINS_RECALL_PASS}"},
    ]


def rules():
    """The numbers the preview needs to follow the same rules."""
    return {
        "xp_right": XP_RIGHT, "xp_miss": XP_MISS, "combo_step": COMBO_STEP, "combo_cap": COMBO_CAP, "xp_boss": XP_BOSS,
        "coins_right": COINS_RIGHT, "coins_boss": COINS_BOSS, "xp_level_done": XP_LEVEL_DONE, "xp_level_pass": XP_LEVEL_PASS,
        "xp_first_clear": XP_FIRST_CLEAR, "coins_first_clear": COINS_FIRST_CLEAR, "xp_perfect": XP_PERFECT,
        "xp_speed_right": XP_SPEED_RIGHT, "xp_speed_done": XP_SPEED_DONE, "coins_speed_done": COINS_SPEED_DONE,
        "xp_focus_minute": XP_FOCUS_MINUTE, "coins_focus_done": COINS_FOCUS_DONE,
        "xp_lesson_first": XP_LESSON_FIRST, "coins_lesson_first": COINS_LESSON_FIRST, "xp_lesson_replay": XP_LESSON_REPLAY,
        "xp_recall_pass": XP_RECALL_PASS, "coins_recall_pass": COINS_RECALL_PASS, "xp_recall_try": XP_RECALL_TRY,
        "streak_coins": {str(k): v for k, v in STREAK_COINS.items()},
        "ranks": [{"at": a, "name": n} for a, n in RANKS], "badges": BADGES, "shop": SHOP, "earn": earn_table(),
    }
