"""Saved preferences: look and reading, dashboard layout, study and test defaults, and the drawn avatar.

They live in users.prefs as JSON. Theme, accent color and the ripple background keep their own columns
(they came first). Everything here has a default, every change is checked against the lists below, and
options sold in the shop (game.SHOP) need to be owned first.

The browser draws the avatar from these part names (website/src/theme.js holds the colors and shapes), so
add a part in both places.
"""
import json
import re
from copy import deepcopy

from . import cosmetics

# ---------- look and reading ----------
SHOP_THEME_KEYS = ("chalkboard", "nightowl", "sunrise", "sakura", "graph", "deepsea", "espresso", "plum")
THEMES = ("dark", "light", "system", "paper", "midnight", "contrast") + SHOP_THEME_KEYS
SHOP_THEMES = {t: f"theme:{t}" for t in SHOP_THEME_KEYS}
BASE_ACCENTS = ("pencil", "sky", "mint", "coral", "lilac")
TEXT_SIZES = ("s", "m", "l", "xl")
FONTS = ("default", "readable", "rounded", "mono")
CORNERS = ("round", "soft", "sharp")
MOTION = ("system", "reduce", "full")
DENSITY = ("comfortable", "compact")
HEX = re.compile(r"^#[0-9a-fA-F]{6}$")

# ---------- dashboard ----------
SECTIONS = ("kpis", "play", "today", "scores", "domains", "review", "plan", "account")
PINS = ("levels", "speed", "focus", "lessons", "practice_test", "practice", "review", "plan", "rewards", "calculator")
MAX_PINS = 4

# ---------- study and test defaults ----------
SET_SIZES = (5, 10, 15, 20)
TIMER = ("show", "hide")
CALCULATOR = ("closed", "open")
COLORS = ("graphite", "testday")

# ---------- drawn avatar ----------
AVATAR = {
    "bg": ("sky", "mint", "sun", "rose", "lilac", "slate", "peach", "teal"),
    "skin": ("s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8"),
    "hair": ("none", "short", "curly", "long", "bun", "buzz", "waves", "ponytail"),
    "hair_color": ("black", "brown", "auburn", "blonde", "gray", "blue", "pink", "green"),
    "eyes": ("dots", "happy", "wide", "sleepy"),
    "mouth": ("smile", "grin", "flat", "open"),
    "acc": ("none", "glasses", "beanie", "headphones", "sunglasses", "pencil", "gradcap", "crown"),
    "shirt": ("pencil", "sky", "mint", "coral", "lilac", "slate", "white", "black"),
}
# Item slots from the cosmetics catalog. "acc" is the old single accessory slot, kept so saved avatars still load.
for _slot, _items in cosmetics.AVATAR.items():
    AVATAR[_slot] = ("none",) * (_slot in ("hat", "face")) + tuple(v for v, *_ in _items)
# value -> shop key, for each slot (free items aren't in the shop)
SHOP_AVATAR = {v: f"avatar:{v}" for _items in cosmetics.AVATAR.values() for v, _n, price, *_ in _items if price}
EFFECTS = tuple(v for v, *_ in cosmetics.EFFECTS)
AVATAR_MODES = ("photo", "drawn")

DEFAULTS = {
    "look": {"text": "m", "font": "default", "motion": "system", "density": "comfortable", "custom_accent": "#f2c14e",
             "effect": "none", "corners": "round"},  # a plain background until one is bought in the shop
    "dashboard": {"order": list(SECTIONS), "hidden": [], "pins": []},
    "study": {"set_size": 10, "timer": "show", "calculator": "closed", "colors": "graphite", "sounds": True,
              "reminder": False, "reminder_hour": 16, "tz": "America/New_York"},
    "avatar": {"mode": "photo", "parts": {"bg": "sky", "skin": "s3", "hair": "short", "hair_color": "brown",
                                          "eyes": "dots", "mouth": "smile", "acc": "none", "shirt": "pencil",
                                          "hat": "none", "face": "none", "outfit": "tee", "backdrop": "solid"}},
}


class PrefsError(ValueError):
    def __init__(self, message, field=None):
        super().__init__(message)
        self.field = field


def load(user):
    """The user's preferences with defaults filled in."""
    raw = {}
    try:
        raw = json.loads(user["prefs"] or "{}") if "prefs" in user.keys() else {}
    except (TypeError, ValueError):
        raw = {}
    out = deepcopy(DEFAULTS)
    for section, values in out.items():
        saved = raw.get(section)
        if isinstance(saved, dict):
            for k in values:
                if k in saved:
                    values[k] = saved[k]
    saved = (raw.get("avatar") or {}).get("parts") or {}
    parts = dict(DEFAULTS["avatar"]["parts"], **saved)
    # Avatars saved before slots existed had one accessory; move it to its slot.
    if parts.get("acc", "none") != "none" and "hat" not in saved and "face" not in saved:
        slot = cosmetics.slot_of(parts["acc"])
        if slot in ("hat", "face"):
            parts[slot] = parts["acc"]
        parts["acc"] = "none"
    out["avatar"]["parts"] = parts
    # A background that has to be bought shows only once it's owned (Ripples used to be free).
    eff = out["look"]["effect"]
    if eff not in cosmetics.FREE_EFFECTS and "id" in user.keys():
        from ..db import query
        if not query("SELECT 1 FROM inventory WHERE user_id = ? AND item = ?", (user["id"], f"effect:{eff}"), one=True):
            out["look"]["effect"] = "none"
    return out


def _one_of(value, allowed, field, message):
    if value not in allowed:
        raise PrefsError(message, field)
    return value


def clean(section, data, current, owned):
    """Checks a partial update to one section and returns the merged section. owned: shop keys the user has."""
    if not isinstance(data, dict):
        raise PrefsError("Send the settings to change.")
    out = deepcopy(current[section])
    if section == "look":
        for k, allowed, msg in (("text", TEXT_SIZES, "Pick a text size."), ("font", FONTS, "Pick a font."),
                                ("motion", MOTION, "Pick a motion setting."), ("density", DENSITY, "Pick a spacing."),
                                ("corners", CORNERS, "Pick a corner style.")):
            if k in data:
                out[k] = _one_of(data[k], allowed, k, msg)
        if "effect" in data:
            out["effect"] = _one_of(data["effect"], EFFECTS, "effect", "Pick a background.")
            if out["effect"] not in cosmetics.FREE_EFFECTS and f"effect:{out['effect']}" not in owned:
                raise PrefsError("Buy that background in the shop first.", "effect")
        if "custom_accent" in data:
            if not isinstance(data["custom_accent"], str) or not HEX.match(data["custom_accent"]):
                raise PrefsError("Pick a color.", "custom_accent")
            if "accent:custom" not in owned:
                raise PrefsError("Buy Any color in the shop first.", "custom_accent")
            out["custom_accent"] = data["custom_accent"].lower()
    elif section == "dashboard":
        if "order" in data:
            order = data["order"]
            if not isinstance(order, list) or sorted(order) != sorted(SECTIONS):
                raise PrefsError("That layout is missing a section.", "order")
            out["order"] = order
        if "hidden" in data:
            hidden = data["hidden"]
            if not isinstance(hidden, list) or any(h not in SECTIONS for h in hidden) or len(set(hidden)) != len(hidden):
                raise PrefsError("Pick sections to hide.", "hidden")
            out["hidden"] = hidden
        if "pins" in data:
            pins = data["pins"]
            if not isinstance(pins, list) or any(p not in PINS for p in pins) or len(set(pins)) != len(pins):
                raise PrefsError("Pick shortcuts to pin.", "pins")
            if len(pins) > MAX_PINS:
                raise PrefsError(f"Pin up to {MAX_PINS} shortcuts.", "pins")
            out["pins"] = pins
    elif section == "study":
        if "set_size" in data:
            out["set_size"] = _one_of(data["set_size"], SET_SIZES, "set_size", "Pick a set size.")
        for k, allowed, msg in (("timer", TIMER, "Show or hide the timer."), ("calculator", CALCULATOR, "Pick open or closed."),
                                ("colors", COLORS, "Pick test colors.")):
            if k in data:
                out[k] = _one_of(data[k], allowed, k, msg)
        for k in ("sounds", "reminder"):
            if k in data:
                if not isinstance(data[k], bool):
                    raise PrefsError("Turn it on or off.", k)
                out[k] = data[k]
        if "reminder_hour" in data:
            h = data["reminder_hour"]
            if not isinstance(h, int) or isinstance(h, bool) or not 0 <= h <= 23:
                raise PrefsError("Pick a time for the reminder.", "reminder_hour")
            out["reminder_hour"] = h
        if "tz" in data:
            out["tz"] = valid_tz(data["tz"])
    elif section == "avatar":
        if "mode" in data:
            out["mode"] = _one_of(data["mode"], AVATAR_MODES, "mode", "Pick photo or drawn avatar.")
        if "parts" in data:
            parts = data["parts"]
            if not isinstance(parts, dict):
                raise PrefsError("Pick avatar parts.", "parts")
            merged = dict(out["parts"])
            for k, v in parts.items():
                if k not in AVATAR:
                    raise PrefsError("That isn't an avatar part.", "parts")
                merged[k] = _one_of(v, AVATAR[k], "parts", "Pick one of the options.")
            for slot in ("acc", "hat", "face", "outfit", "backdrop"):
                item = SHOP_AVATAR.get(merged[slot])
                if item and item not in owned:
                    raise PrefsError("Buy that in the shop first.", "parts")
            out["parts"] = merged
    else:
        raise PrefsError("That isn't a settings section.")
    return out


def valid_tz(tz):
    from zoneinfo import ZoneInfo
    try:
        ZoneInfo(str(tz))
    except Exception:
        raise PrefsError("That time zone isn't recognized.", "tz")
    return str(tz)


def save(user_id, prefs):
    from ..db import execute
    execute("UPDATE users SET prefs = ? WHERE id = ?", (json.dumps(prefs), user_id))


def drawn_avatar(user):
    """The avatar parts when the student uses a drawn avatar, else None. Safe to show anyone (it isn't a photo)."""
    a = load(user)["avatar"]
    return a["parts"] if a["mode"] == "drawn" else None


def options():
    """Every choice, for the Settings page and the preview."""
    return {"themes": list(THEMES), "shop_themes": SHOP_THEMES, "text_sizes": list(TEXT_SIZES), "fonts": list(FONTS),
            "motion": list(MOTION), "density": list(DENSITY), "sections": list(SECTIONS), "pins": list(PINS),
            "max_pins": MAX_PINS, "set_sizes": list(SET_SIZES), "avatar": {k: list(v) for k, v in AVATAR.items()},
            "shop_avatar": SHOP_AVATAR, "effects": list(EFFECTS), "corners": list(CORNERS), "defaults": DEFAULTS}
