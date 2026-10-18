"""The market: collectibles whose prices move with what every student buys and sells.

How a price is set
- Each collectible has a base price and a "demand" number shared by everyone.
- Every buy adds 1 to demand and every sell takes 1 away. The price is base × growth^demand, so buying pushes
  the price up for everyone and selling pushes it down.
- Demand fades by half every HALF_LIFE_HOURS, so an item nobody is trading drifts back to its base price.
- Selling pays SPREAD less than the buy price. Buying and then selling right away always loses coins, so
  nobody can pump a price and cash out on their own.

Limits that keep it fair
- Rare and legendary collectibles have a fixed supply. When they're all owned, they're sold out until
  someone sells one back.
- Each student can hold only so many of each collectible (MAX_HOLD) and make TRADES_PER_DAY trades a day.
- The page sends the price it showed. If the price moved since (someone else traded), the trade stops and
  the new price comes back, so nobody pays a price they didn't see.
- Two trades by the same student at once can't both spend the same coins (users.market_seq), and two trades
  of the same item at once can't both use the same price (market_items.version).

Students never deal with each other directly and nobody's name is shown in the market activity feed.
"""
import math
import time

from ..db import changed, execute, query, today
from . import game

HALF_LIFE_HOURS = 12
SPREAD = 0.10              # selling pays 10% less than buying
TRADES_PER_DAY = 60
FLOOR, CEILING = 0.5, 4.0  # a price stays between half and four times its base
HISTORY_POINTS = 32        # points on a price chart

RARITIES = {
    # growth per trade, how many one student can hold, total supply (None = unlimited)
    "common": {"name": "Common", "growth": 1.05, "max_hold": 25, "supply": None},
    "uncommon": {"name": "Uncommon", "growth": 1.05, "max_hold": 15, "supply": None},
    "rare": {"name": "Rare", "growth": 1.06, "max_hold": 5, "supply": 1000},
    "legendary": {"name": "Legendary", "growth": 1.07, "max_hold": 2, "supply": 250},
}

SETS = [
    {"key": "symbols", "name": "Math Symbols", "about": "The symbols you'll see all over the Math section."},
    {"key": "pencils", "name": "Pencil Case", "about": "Every great test starts with a sharp pencil."},
    {"key": "numbers", "name": "Famous Numbers", "about": "Numbers with a story behind them."},
    {"key": "shapes", "name": "Shape Shifters", "about": "The shapes behind every geometry question."},
    {"key": "tools", "name": "Calculator Crew", "about": "Every tool that ever crunched a number."},
]
# Finishing a set earns its title (an exclusive one; it can't be bought).
SET_TITLES = {"symbols": "Symbol Collector", "pencils": "Pencil Pusher", "numbers": "Number Theorist",
              "shapes": "Shape Shifter", "tools": "Calculator Crew"}

# art: "glyph" draws the text on a tile; "pencil" draws a pencil in that color.
ITEMS = [
    {"key": "pi", "set": "symbols", "name": "Pi", "rarity": "common", "base": 20, "art": "glyph", "glyph": "π",
     "about": "A circle's circumference divided by its diameter. Every SAT circle question leans on it."},
    {"key": "sigma", "set": "symbols", "name": "Sigma", "rarity": "common", "base": 20, "art": "glyph", "glyph": "Σ",
     "about": "The Greek capital S, used to mean \"add these all up.\""},
    {"key": "root", "set": "symbols", "name": "Square Root", "rarity": "common", "base": 25, "art": "glyph", "glyph": "√",
     "about": "The number that times itself gives what's inside."},
    {"key": "infinity", "set": "symbols", "name": "Infinity", "rarity": "uncommon", "base": 60, "art": "glyph", "glyph": "∞",
     "about": "What you get when a system of equations has the same line twice."},
    {"key": "delta", "set": "symbols", "name": "Delta", "rarity": "uncommon", "base": 55, "art": "glyph", "glyph": "Δ",
     "about": "Change in something. Slope is Δy over Δx."},
    {"key": "theta", "set": "symbols", "name": "Theta", "rarity": "uncommon", "base": 65, "art": "glyph", "glyph": "θ",
     "about": "The usual name for an angle in trig questions."},
    {"key": "classic", "set": "pencils", "name": "Classic No. 2", "rarity": "common", "base": 30, "art": "pencil", "color": "#f2c14e",
     "about": "The one they tell you to bring on test day."},
    {"key": "carpenter", "set": "pencils", "name": "Carpenter's Pencil", "rarity": "uncommon", "base": 70, "art": "pencil", "color": "#d9534f",
     "about": "Flat so it never rolls off the desk."},
    {"key": "midnight", "set": "pencils", "name": "Midnight Pencil", "rarity": "rare", "base": 160, "art": "pencil", "color": "#2b2f36",
     "about": "Matte black, for late-night study sessions."},
    {"key": "golden", "set": "pencils", "name": "Golden Pencil", "rarity": "legendary", "base": 600, "art": "pencil", "color": "#d4a017",
     "about": "Only 250 exist. Never been sharpened."},
    {"key": "euler", "set": "numbers", "name": "e", "rarity": "rare", "base": 180, "art": "glyph", "glyph": "e",
     "about": "About 2.718. The base of natural growth and compound interest."},
    {"key": "imaginary", "set": "numbers", "name": "i", "rarity": "rare", "base": 200, "art": "glyph", "glyph": "i",
     "about": "The square root of −1. It shows up in SAT complex-number questions."},
    {"key": "phi", "set": "numbers", "name": "Golden Ratio", "rarity": "legendary", "base": 650, "art": "glyph", "glyph": "φ",
     "about": "About 1.618. Only 250 exist."},
    {"key": "taxicab", "set": "numbers", "name": "1729", "rarity": "legendary", "base": 700, "art": "glyph", "glyph": "1729",
     "about": "The smallest number that's a sum of two cubes in two ways. Only 250 exist."},
    {"key": "triangle", "set": "shapes", "name": "Triangle", "rarity": "common", "base": 20, "art": "shape", "shape": "triangle",
     "about": "Three sides, 180 degrees, endless SAT questions."},
    {"key": "circle", "set": "shapes", "name": "Circle", "rarity": "common", "base": 22, "art": "shape", "shape": "circle",
     "about": "Every point the same distance from the center."},
    {"key": "hexagon", "set": "shapes", "name": "Hexagon", "rarity": "uncommon", "base": 55, "art": "shape", "shape": "hexagon",
     "about": "Bees figured out this one first."},
    {"key": "star", "set": "shapes", "name": "Star", "rarity": "uncommon", "base": 60, "art": "shape", "shape": "star",
     "about": "Five points, and every angle at a tip is 36 degrees."},
    {"key": "cube", "set": "shapes", "name": "Cube", "rarity": "rare", "base": 170, "art": "shape", "shape": "cube",
     "about": "Six faces. Double the side and the volume grows eight times."},
    {"key": "spiral", "set": "shapes", "name": "Golden Spiral", "rarity": "legendary", "base": 680, "art": "shape", "shape": "spiral",
     "about": "Grows by the golden ratio every quarter turn. Only 250 exist."},
    {"key": "abacus", "set": "tools", "name": "Abacus", "rarity": "uncommon", "base": 65, "art": "tool", "tool": "abacus",
     "about": "The calculator before batteries."},
    {"key": "protractor", "set": "tools", "name": "Protractor", "rarity": "common", "base": 25, "art": "tool", "tool": "protractor",
     "about": "Measures angles from 0 to 180."},
    {"key": "sliderule", "set": "tools", "name": "Slide Rule", "rarity": "rare", "base": 190, "art": "tool", "tool": "sliderule",
     "about": "Took people to the moon."},
    {"key": "goldcalc", "set": "tools", "name": "Golden Calculator", "rarity": "legendary", "base": 720, "art": "tool", "tool": "calculator",
     "about": "Graphs in pure gold. Only 250 exist."},
]
BY_KEY = {i["key"]: i for i in ITEMS}

HALF_LIFE_MS = HALF_LIFE_HOURS * 3600 * 1000


class MarketError(ValueError):
    def __init__(self, message, status=400, extra=None):
        super().__init__(message)
        self.status = status
        self.extra = extra or {}


def now_ms():
    return int(time.time() * 1000)


# ---------- prices ----------
def _limits(item):
    """The demand range where the price stops moving (so demand can't run off where it takes days to come back)."""
    g = math.log(RARITIES[item["rarity"]]["growth"])
    return math.log(FLOOR) / g, math.log(CEILING) / g


def decayed(demand, since_ms, at_ms):
    if not demand:
        return 0.0
    return demand * 0.5 ** (max(0, at_ms - since_ms) / HALF_LIFE_MS)


def price_for(item, demand):
    lo, hi = _limits(item)
    d = min(hi, max(lo, demand))
    return max(1, round(item["base"] * RARITIES[item["rarity"]]["growth"] ** d))


def sell_price(buy):
    return max(1, math.floor(buy * (1 - SPREAD)))


def _row(key):
    row = query("SELECT * FROM market_items WHERE item = ?", (key,), one=True)
    if row:
        return row
    execute("INSERT INTO market_items (item, demand, demand_ms, version) VALUES (?, 0, 0, 0) ON CONFLICT (item) DO NOTHING", (key,))
    return query("SELECT * FROM market_items WHERE item = ?", (key,), one=True)


def _rows():
    have = {r["item"]: r for r in query("SELECT * FROM market_items")}
    return {k: have.get(k) or _row(k) for k in BY_KEY}


def demand_now(row, at_ms=None):
    return decayed(float(row["demand"]), int(row["demand_ms"]), now_ms() if at_ms is None else at_ms)


def circulation():
    return {r["item"]: int(r["n"]) for r in query("SELECT item, COALESCE(SUM(qty), 0) AS n FROM market_holdings GROUP BY item")}


def holdings(user_id):
    return {r["item"]: r for r in query("SELECT item, qty, cost FROM market_holdings WHERE user_id = ? AND qty > 0", (user_id,))}


def trades_today(user_id):
    return query("SELECT COUNT(*) AS n FROM market_trades WHERE user_id = ? AND day = ?",
                 (user_id, today().isoformat()), one=True)["n"]


# ---------- history ----------
def history(key, hours=24, at_ms=None):
    """[{at_ms, price}] sampled evenly over the last `hours`, rebuilt from the trades (demand fades between them)."""
    item = BY_KEY[key]
    end = now_ms() if at_ms is None else at_ms
    start = end - hours * 3600 * 1000
    before = query("SELECT demand_after, at_ms FROM market_trades WHERE item = ? AND at_ms <= ? ORDER BY at_ms DESC, id DESC LIMIT 1",
                   (key, start), one=True)
    trades = query("SELECT demand_after, at_ms FROM market_trades WHERE item = ? AND at_ms > ? AND at_ms <= ? ORDER BY at_ms, id",
                   (key, start, end))
    d, since = (float(before["demand_after"]), int(before["at_ms"])) if before else (0.0, start)
    out, i = [], 0
    for n in range(HISTORY_POINTS):
        t = start + (end - start) * n // (HISTORY_POINTS - 1)
        while i < len(trades) and int(trades[i]["at_ms"]) <= t:
            d, since = float(trades[i]["demand_after"]), int(trades[i]["at_ms"])
            i += 1
        out.append({"at_ms": t, "price": price_for(item, decayed(d, since, t))})
    return out


def change_24h(key, price_now, at_ms=None):
    then = history(key, 24, at_ms)[0]["price"]
    return round((price_now - then) / then * 100, 1) if then else 0.0


# ---------- what the page shows ----------
def _public_item(item, row, mine, circ, at_ms):
    d = demand_now(row, at_ms)
    buy = price_for(item, d)
    r = RARITIES[item["rarity"]]
    h = mine.get(item["key"])
    supply = r["supply"]
    return {
        "key": item["key"], "set": item["set"], "name": item["name"], "about": item["about"],
        "rarity": item["rarity"], "rarity_name": r["name"], "art": item["art"],
        "glyph": item.get("glyph"), "color": item.get("color"), "shape": item.get("shape"), "tool": item.get("tool"), "base": item["base"],
        "price": buy, "sell_price": sell_price(buy), "change_24h": change_24h(item["key"], buy, at_ms),
        "supply": supply, "left": None if supply is None else max(0, supply - circ.get(item["key"], 0)),
        "max_hold": r["max_hold"], "owned": int(h["qty"]) if h else 0,
        "avg_cost": round(int(h["cost"]) / int(h["qty"])) if h and int(h["qty"]) else None,
    }


def overview(user):
    uid = user["id"]
    at = now_ms()
    rows, mine, circ = _rows(), holdings(uid), circulation()
    items = [_public_item(i, rows[i["key"]], mine, circ, at) for i in ITEMS]
    value = sum(i["owned"] * i["sell_price"] for i in items)
    paid = sum(int(h["cost"]) for h in mine.values())
    owned_keys = {k for k, h in mine.items() if int(h["qty"]) > 0}
    sets = [dict(s, have=sum(1 for i in ITEMS if i["set"] == s["key"] and i["key"] in owned_keys),
                 of=sum(1 for i in ITEMS if i["set"] == s["key"])) for s in SETS]
    _, coins = game.totals(uid)
    return {
        "items": items, "sets": sets, "coins": coins, "value": value, "paid": paid,
        "trades_left": max(0, TRADES_PER_DAY - trades_today(uid)), "trades_per_day": TRADES_PER_DAY,
        "activity": activity(), "rules": rules(), "mine": my_trades(uid),
        "set_titles": [{"set": k, "title": v, "owned": f"title:set-{k}" in game.owned(uid)} for k, v in SET_TITLES.items()],
    }


def activity(limit=12):
    """The latest trades across the whole market. No names: just what moved and when."""
    rows = query("SELECT item, side, price, at_ms FROM market_trades ORDER BY id DESC LIMIT ?", (limit,))
    return [{"item": r["item"], "name": BY_KEY[r["item"]]["name"] if r["item"] in BY_KEY else r["item"],
             "side": r["side"], "price": int(r["price"]), "at_ms": int(r["at_ms"])} for r in rows]


def rules():
    return {"half_life_hours": HALF_LIFE_HOURS, "spread": SPREAD, "trades_per_day": TRADES_PER_DAY,
            "floor": FLOOR, "ceiling": CEILING, "rarities": RARITIES, "sets": SETS, "items": ITEMS, "set_titles": SET_TITLES,
            "history_points": HISTORY_POINTS}


# ---------- trading ----------
def _claim_user(user_id):
    """Takes this student's trade turn. If another of their trades got in first, this one stops."""
    seq = query("SELECT market_seq FROM users WHERE id = ?", (user_id,), one=True)["market_seq"] or 0
    return seq


def _commit_user(user_id, seq):
    if not changed("UPDATE users SET market_seq = ? WHERE id = ? AND market_seq = ?", (seq + 1, user_id, seq)):
        raise MarketError("Another trade is going through. Try again.", 409)


def _move(item, row, new_demand, at):
    """Saves the item's new demand, unless someone else traded it first."""
    if not changed("UPDATE market_items SET demand = ?, demand_ms = ?, version = version + 1 WHERE item = ? AND version = ?",
                   (new_demand, at, item["key"], row["version"])):
        raise MarketError("Someone else just traded this. Check the new price.", 409)


def _quote_check(expected, actual):
    if expected is not None and expected != actual:
        raise MarketError("The price changed since you looked.", 409, {"price": actual})


def trade(user_id, key, side, expected_price=None):
    """One buy or sell of one collectible. Returns {report, item, price}."""
    item = BY_KEY.get(key)
    if not item:
        raise MarketError("That isn't in the market.")
    if side not in ("buy", "sell"):
        raise MarketError("Buy or sell.")
    if trades_today(user_id) >= TRADES_PER_DAY:
        raise MarketError(f"That's {TRADES_PER_DAY} trades today. The market opens again for you tomorrow.", 429)
    seq = _claim_user(user_id)
    at = now_ms()
    row = _row(key)
    d = demand_now(row, at)
    buy = price_for(item, d)
    r = RARITIES[item["rarity"]]
    h = holdings(user_id).get(key)
    qty = int(h["qty"]) if h else 0
    cost = int(h["cost"]) if h else 0
    xp_before, coins = game.totals(user_id)
    badges = []
    unlocked = None
    if side == "buy":
        _quote_check(expected_price, buy)
        if qty >= r["max_hold"]:
            raise MarketError(f"You can hold up to {r['max_hold']} of this one.")
        if r["supply"] is not None and circulation().get(key, 0) >= r["supply"]:
            raise MarketError("Sold out. One comes back when someone sells.", 409)
        if coins < buy:
            raise MarketError(f"You need {buy - coins} more coins for that.")
        price, new_d, coins_delta = buy, d + 1, -buy
    else:
        price = sell_price(buy)
        _quote_check(expected_price, price)
        if qty < 1:
            raise MarketError("You don't have one to sell.")
        new_d, coins_delta = d - 1, price
    lo, hi = _limits(item)
    new_d = min(hi, max(lo, new_d))
    _commit_user(user_id, seq)
    _move(item, row, new_d, at)

    if side == "buy":
        execute("INSERT INTO market_holdings (user_id, item, qty, cost) VALUES (?, ?, 1, ?) "
                "ON CONFLICT (user_id, item) DO UPDATE SET qty = market_holdings.qty + 1, cost = market_holdings.cost + ?",
                (user_id, key, price, price))
    else:
        avg = round(cost / qty) if qty else 0
        execute("UPDATE market_holdings SET qty = qty - 1, cost = ? WHERE user_id = ? AND item = ? AND qty >= 1",
                (max(0, cost - avg), user_id, key))
        if price > avg:
            badges.append(game.earn_badge(user_id, "buy_low"))
    execute("INSERT INTO market_trades (user_id, item, side, price, demand_after, at_ms, day) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_id, key, side, price, new_d, at, today().isoformat()))
    execute("INSERT INTO xp_events (user_id, kind, xp, coins, detail, day, at) VALUES (?, ?, 0, ?, ?, ?, ?)",
            (user_id, "market_" + side, coins_delta, key, today().isoformat(), _iso(at)))
    badges.append(game.earn_badge(user_id, "market_debut"))
    if side == "buy":
        mine = {k for k, v in holdings(user_id).items() if int(v["qty"]) > 0}
        for s in SETS:
            if all(i["key"] in mine for i in ITEMS if i["set"] == s["key"]):
                badges.append(game.earn_badge(user_id, "collector"))
                if s["key"] == item["set"]:
                    title = _grant_set_title(user_id, s["key"])
                    if title:
                        unlocked = title
    rep = game.report(user_id, xp_before, 0, coins_delta, badges)
    circ, mine = circulation(), holdings(user_id)
    fresh = _public_item(item, _row(key), mine, circ, now_ms())
    return {"reward": rep, "item": fresh, "price": price, "side": side, "unlocked_title": unlocked}


def _grant_set_title(user_id, set_key):
    """Gives the set's title once. Returns its name if it's new."""
    key = "title:set-" + set_key
    if query("SELECT 1 FROM inventory WHERE user_id = ? AND item = ?", (user_id, key), one=True):
        return None
    execute("INSERT INTO inventory (user_id, item, bought_at) VALUES (?, ?, ?) ON CONFLICT (user_id, item) DO NOTHING",
            (user_id, key, _iso(now_ms())))
    return SET_TITLES[set_key]


def my_trades(user_id, limit=15):
    rows = query("SELECT item, side, price, at_ms FROM market_trades WHERE user_id = ? ORDER BY id DESC LIMIT ?", (user_id, limit))
    return [{"item": r["item"], "name": BY_KEY[r["item"]]["name"] if r["item"] in BY_KEY else r["item"], "side": r["side"],
             "price": int(r["price"]), "at_ms": int(r["at_ms"])} for r in rows]


def _iso(at_ms):
    from datetime import datetime, timezone
    return datetime.fromtimestamp(at_ms / 1000, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def item_history(key, hours):
    if key not in BY_KEY:
        raise MarketError("That isn't in the market.", 404)
    pts = history(key, hours)
    return {"key": key, "hours": hours, "points": pts}
