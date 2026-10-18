"""Pets: hatch an egg by studying, then raise the pet.

- Every student gets a first egg. It hatches after they earn EGG_XP more XP anywhere on the site.
- Hatching picks a species at random (rarer ones are less likely). The new pet becomes the active pet.
- The active pet grows with every XP the student earns. Treats (bought with coins, a few a day) add a bit more.
- Levels get a little further apart as they go; stages (baby, young, teen, grown, legend) change how it looks.
- More eggs come from the shop. Only one egg can wait to hatch at a time.
Nothing bad happens if a student takes a break: the pet just naps until they're back.
"""
import random

from ..db import execute, now_iso, query, today
from . import game

EGG_XP = 150
EGG_PRICE = 600
TREAT_PRICE = 20
TREAT_XP = 40
TREATS_PER_DAY = 5
MAX_PETS = 8
MAX_LEVEL = 30
SPECIES = [
    # key, name, rarity, weight, about
    ("sketch", "Sketch", "common", 26, "A little pencil dragon. Its tail tip is pure graphite."),
    ("inky", "Inky", "common", 26, "An octopus who writes with all eight arms."),
    ("hoot", "Hoot", "common", 26, "An owl with compass-point eyes. Up late studying."),
    ("foxel", "Foxel", "rare", 9, "A fox whose tail curls into a π."),
    ("axel", "Axel", "rare", 9, "An axolotl that regrows wrong answers into right ones."),
    ("nova", "Nova", "legendary", 4, "A tiny star spirit. Almost nobody hatches one."),
]
SPECIES_BY_KEY = {s[0]: s for s in SPECIES}
STAGES = [(1, "baby"), (5, "young"), (10, "teen"), (18, "grown"), (30, "legend")]


class PetError(ValueError):
    pass


def level_for(xp):
    """(level, xp into this level, xp needed for the next). Level n needs 40 + 20n more XP to reach n + 1."""
    level, need = 1, 60
    while level < MAX_LEVEL and xp >= need:
        xp -= need
        level += 1
        need = 40 + 20 * level
    return level, xp, (None if level >= MAX_LEVEL else need)


def stage_for(level):
    return [name for at, name in STAGES if level >= at][-1]


def _rows(user_id):
    return query("SELECT * FROM pets WHERE user_id = ? ORDER BY id", (user_id,))


def _total_xp(user_id):
    return game.totals(user_id)[0]


def ensure_egg(user_id):
    """Everyone starts with one egg."""
    if not _rows(user_id):
        execute("INSERT INTO pets (user_id, egg_base, xp_base, banked, active, created_at) VALUES (?, ?, 0, 0, 0, ?)",
                (user_id, _total_xp(user_id), now_iso()))


def _xp(row, total):
    if not row["hatched_at"]:
        return 0
    return int(row["banked"]) + (total - int(row["xp_base"]) if row["active"] else 0)


def public(row, total):
    if not row["hatched_at"]:
        got = max(0, total - int(row["egg_base"]))
        return {"id": row["id"], "egg": True, "progress": min(got, EGG_XP), "need": EGG_XP, "ready": got >= EGG_XP}
    sp = SPECIES_BY_KEY.get(row["species"], SPECIES[0])
    xp = _xp(row, total)
    level, into, need = level_for(xp)
    return {"id": row["id"], "egg": False, "species": sp[0], "species_name": sp[1], "rarity": sp[2], "about": sp[4],
            "name": row["name"] or sp[1], "xp": xp, "level": level, "into": into, "need": need, "stage": stage_for(level),
            "active": bool(row["active"]), "gear": row["gear"], "hatched_at": row["hatched_at"]}


def overview(user):
    uid = user["id"]
    ensure_egg(uid)
    total = _total_xp(uid)
    pets = [public(r, total) for r in _rows(uid)]
    treats = query("SELECT COUNT(*) AS n FROM xp_events WHERE user_id = ? AND kind = 'pet_treat' AND day = ?",
                   (uid, today().isoformat()), one=True)["n"]
    studied = query("SELECT 1 FROM xp_events WHERE user_id = ? AND day = ? AND xp > 0", (uid, today().isoformat()), one=True)
    owned = game.owned(uid)
    return {"pets": pets, "active": next((p for p in pets if not p["egg"] and p["active"]), None),
            "egg": next((p for p in pets if p["egg"]), None), "mood": "happy" if studied else "sleepy",
            "treats_left": max(0, TREATS_PER_DAY - treats), "rules": rules(),
            "gear": [dict(s, owned=s["key"] in owned) for s in game.SHOP if s["kind"] == "petgear"]}


def rules():
    return {"egg_xp": EGG_XP, "egg_price": EGG_PRICE, "treat_price": TREAT_PRICE, "treat_xp": TREAT_XP,
            "treats_per_day": TREATS_PER_DAY, "max_pets": MAX_PETS, "max_level": MAX_LEVEL,
            "species": [{"key": k, "name": n, "rarity": r, "about": a} for k, n, r, _w, a in SPECIES],
            "stages": [{"at": at, "name": name} for at, name in STAGES]}


def _get(user_id, pet_id):
    row = query("SELECT * FROM pets WHERE id = ? AND user_id = ?", (pet_id, user_id), one=True)
    if not row:
        raise PetError("That pet isn't yours.")
    return row


def hatch(user_id, pet_id, pick=None):
    """Hatches a ready egg. pick is for tests; normally the species is random."""
    row = _get(user_id, pet_id)
    if row["hatched_at"]:
        raise PetError("That egg already hatched.")
    total = _total_xp(user_id)
    if total - int(row["egg_base"]) < EGG_XP:
        raise PetError(f"Earn {EGG_XP - (total - int(row['egg_base']))} more XP to hatch it.")
    species = pick or random.choices([s[0] for s in SPECIES], weights=[s[3] for s in SPECIES])[0]
    has_active = any(r["active"] and r["hatched_at"] for r in _rows(user_id))
    execute("UPDATE pets SET species = ?, hatched_at = ?, xp_base = ?, banked = 0, active = ? WHERE id = ?",
            (species, now_iso(), total, 0 if has_active else 1, row["id"]))
    xp, _ = game.totals(user_id)
    badges = [game.earn_badge(user_id, "first_hatch")]
    if sum(1 for r in _rows(user_id) if r["hatched_at"]) >= 3:
        badges.append(game.earn_badge(user_id, "pet_parent"))
    return {"pet": public(_get(user_id, pet_id), total), "reward": game.report(user_id, xp, 0, 0, badges)}


def set_active(user_id, pet_id):
    row = _get(user_id, pet_id)
    if not row["hatched_at"]:
        raise PetError("Hatch it first.")
    total = _total_xp(user_id)
    for r in _rows(user_id):
        if r["active"] and r["id"] != row["id"]:
            execute("UPDATE pets SET banked = ?, active = 0 WHERE id = ?", (_xp(r, total), r["id"]))
    if not row["active"]:
        execute("UPDATE pets SET active = 1, xp_base = ? WHERE id = ?", (total, row["id"]))


def rename(user_id, pet_id, name):
    from . import wordfilter
    import re
    _get(user_id, pet_id)
    name = re.sub(r"\s+", " ", str(name or "")).strip()
    if not 1 <= len(name) <= 16 or not re.match(r"^[A-Za-z0-9][A-Za-z0-9 '\-]*$", name):
        raise PetError("Use 1 to 16 letters, numbers or spaces.")
    if not wordfilter.is_clean(name):
        raise PetError("Pick a different name.")
    execute("UPDATE pets SET name = ? WHERE id = ?", (name, pet_id))
    return name


def treat(user_id):
    """Feeds the active pet a treat: costs coins, adds pet XP."""
    total = _total_xp(user_id)
    act = next((r for r in _rows(user_id) if r["active"] and r["hatched_at"]), None)
    if not act:
        raise PetError("Hatch a pet first.")
    used = query("SELECT COUNT(*) AS n FROM xp_events WHERE user_id = ? AND kind = 'pet_treat' AND day = ?",
                 (user_id, today().isoformat()), one=True)["n"]
    if used >= TREATS_PER_DAY:
        raise PetError(f"That's {TREATS_PER_DAY} treats today. Your pet is full.")
    xp, coins = game.totals(user_id)
    if coins < TREAT_PRICE:
        raise PetError(f"You need {TREAT_PRICE - coins} more coins.")
    before = level_for(_xp(act, total))[0]
    execute("UPDATE pets SET banked = banked + ? WHERE id = ?", (TREAT_XP, act["id"]))
    execute("INSERT INTO xp_events (user_id, kind, xp, coins, detail, day, at) VALUES (?, 'pet_treat', 0, ?, ?, ?, ?)",
            (user_id, -TREAT_PRICE, str(act["id"]), today().isoformat(), now_iso()))
    pet = public(_get(user_id, act["id"]), total)
    badges = [game.earn_badge(user_id, "best_friends")] if pet["level"] >= 10 else []
    return {"pet": pet, "level_up": pet["level"] > before, "reward": game.report(user_id, xp, 0, -TREAT_PRICE, badges)}


def buy_egg(user_id):
    rows = _rows(user_id)
    if any(not r["hatched_at"] for r in rows):
        raise PetError("Hatch the egg you have first.")
    if len(rows) >= MAX_PETS:
        raise PetError(f"You can have up to {MAX_PETS} pets.")
    xp, coins = game.totals(user_id)
    if coins < EGG_PRICE:
        raise PetError(f"You need {EGG_PRICE - coins} more coins.")
    execute("INSERT INTO pets (user_id, egg_base, xp_base, banked, active, created_at) VALUES (?, ?, 0, 0, 0, ?)",
            (user_id, xp, now_iso()))
    execute("INSERT INTO xp_events (user_id, kind, xp, coins, detail, day, at) VALUES (?, 'shop', 0, ?, 'pet:egg', ?, ?)",
            (user_id, -EGG_PRICE, today().isoformat(), now_iso()))
    return game.report(user_id, xp, 0, -EGG_PRICE)


def wear(user_id, gear):
    """Puts gear on the active pet (None takes it off)."""
    act = next((r for r in _rows(user_id) if r["active"] and r["hatched_at"]), None)
    if not act:
        raise PetError("Hatch a pet first.")
    if gear is not None and f"petgear:{gear}" not in game.owned(user_id):
        raise PetError("Buy that in the shop first.")
    execute("UPDATE pets SET gear = ? WHERE id = ?", (gear, act["id"]))


def check_level_badge(user_id):
    """Called after earning XP elsewhere: the Best Friends badge at pet level 10."""
    total = _total_xp(user_id)
    act = next((r for r in _rows(user_id) if r["active"] and r["hatched_at"]), None)
    if act and level_for(_xp(act, total))[0] >= 10:
        return game.earn_badge(user_id, "best_friends")
    return None
