#!/usr/bin/env python3
"""Style lint for web/content/items.ts against docs/item-style-guide.md.

How to run (from the repo root; Python 3, stdlib only):

    python3 web/scripts/lint_items.py            # table + counts, exit 1 on any error
    python3 web/scripts/lint_items.py --rules    # print the rule list and exit
    python3 web/scripts/lint_items.py --quiet    # counts only

verify_items.py checks that keys are right; this script checks that items are
written the way the College Board framework writes them. Every rule has an id,
a severity and a one-line message that cites the style-guide section ("SG §4")
or, for process rules, docs/item-writing.md ("IW §7"). Error-level rules block
an item from the database; warn-level rules are reported for a human to judge.

Rules are listed in RULES below and documented in docs/item-writing.md.
"""

from __future__ import annotations

import argparse
import math
import re
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from itembank import DIFFICULTIES, DOMAINS, ROUTES, load_items, load_skills  # noqa: E402

MAX_POSITIVE_LENGTH = 5
MAX_NEGATIVE_LENGTH = 6
CONTEXT_WORD_LIMIT = 50  # standardized 6-character words (SG §1, §3)
KEY_POSITION_MAX_SHARE = 0.40
DOMAIN_TARGET = {"algebra": 0.35, "advanced-math": 0.35, "psda": 0.15, "geometry-trig": 0.15}
DOMAIN_TOLERANCE = 0.10
SPR_TARGET, SPR_TOLERANCE = 0.25, 0.10
CONTEXT_TARGET, CONTEXT_TOLERANCE = 0.30, 0.10
WINDOW_WORDS = 10
# Question frames the framework itself repeats; they break a window rather than count toward one (SG §3).
STOCK_PHRASES = [
    "which of the following is the best interpretation of",
    "which of the following could be",
    "which of the following must be true",
    "which of the following",
    "what is the value of",
    "in the xy plane",
    "is a positive constant",
    "is a constant",
    "are constants",
    "are positive constants",
    "if the equation has",
    "if the system has",
    "to the nearest",
]

# id -> (severity, message). Keep in step with docs/item-writing.md.
RULES: dict[str, tuple[str, str]] = {
    "ID01": ("error", "item ids are unique slugs (IW §2)"),
    "SK01": ("error", "skill is one of the 19 exact framework skill names in skills.ts (SG §2)"),
    "SK02": ("error", "skill belongs to the item's domain (SG §2)"),
    "DF01": ("error", "difficulty is easy, medium or hard and route/domain/format are valid (SG §6)"),
    "CH01": ("error", "MC item has exactly four choices and a key index 0-3 (SG §4)"),
    "CH02": ("error", "choices are parallel in form: all numeric, all equations, all expressions or all sentences (SG §4)"),
    "CH03": ("error", "numeric choices are strictly ascending or strictly descending, never mixed (SG §4)"),
    "CH04": ("error", "no two choices are the same value or text (SG §4, §10)"),
    "CH05": ("warn", f"bank: no key position holds more than {int(KEY_POSITION_MAX_SHARE*100)}% of MC items (SG §4)"),
    "SP01": ("error", "SPR key fits the entry box: 5 characters positive, 6 negative, as a fraction or a full-width decimal (SG §5)"),
    "SP02": ("warn", "bank: SPR items exist in PSDA and in Geometry and Trigonometry, not only Algebra and Advanced Math (SG §1)"),
    "ST01": ("warn", "a single-letter constant appears but the stem never declares it ('where k is a constant' / 'k is a constant') (SG §3)"),
    "ST02": ("warn", "constants are declared in a trailing 'where ... is a (positive) constant' clause (SG §3)"),
    "ST03": ("error", "a graph, intercept, intersection, slope or parabola is referenced without 'in the xy-plane' (SG §3)"),
    "ST04": ("error", "'which of the following' is not used when the choices are plain numbers (SG §3)"),
    "ST05": ("warn", f"in-context stem is at most {CONTEXT_WORD_LIMIT} standardized words (characters / 6) (SG §1, §3)"),
    "ST06": ("error", "stem ends with a question mark (a trailing parenthetical note or I/II/III list may follow it) (SG §3)"),
    "ST07": ("error", "no first or second person (I, we, you, your ...) and no names of people (SG §3)"),
    "ST08": ("error", "no dollar sign used as money inside $...$ and no '\\$': write 'dollars' in prose (IW §4, MathText limitation)"),
    "ST09": ("warn", "quantities carry their unit in the stem; units and rounding go inside the question sentence (SG §3)"),
    "PR01": ("error", "provenance.author is present and non-empty (IW §2)"),
    "PR02": ("error", "provenance.created is an ISO date YYYY-MM-DD (IW §2)"),
    "PR03": ("error", "byHand is non-empty (SG §8, IW §7)"),
    "PR04": ("warn", "MC byHand names the mistake behind each distractor (SG §4, §8)"),
    "DS01": ("error", "desmos is present exactly when techniques is non-empty (IW §7)"),
    "DS02": ("error", "desmos.verified is a boolean literal and desmos.lines/read are present (IW §3, §7)"),
    "OR01": ("error", f"bank: no two stems share a {WINDOW_WORDS}-word window (SG §9)"),
    "OR02": ("error", "stem does not mention College Board or Khan (SG §9)"),
    "BK01": ("warn", "bank: domain shares are within 10 points of 35/35/15/15 (SG §1)"),
    "BK02": ("warn", "bank: SPR share is within 10 points of 25% (SG §1)"),
    "BK03": ("warn", "bank: in-context share is within 10 points of 30% (SG §1)"),
    "BK04": ("warn", "bank: every difficulty level and every route is represented (SG §6, design notes §1, §3)"),
}


class Report:
    def __init__(self) -> None:
        self.rows: list[tuple[str, str, str, str]] = []  # (item id, rule, severity, detail)

    def add(self, item_id: str, rule: str, detail: str = "") -> None:
        sev = RULES[rule][0]
        self.rows.append((item_id, rule, sev, detail))

    @property
    def errors(self) -> int:
        return sum(1 for r in self.rows if r[2] == "error")


# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------

MATH_SPAN_RE = re.compile(r"\$([^$]+)\$")


def math_spans(text: str) -> list[str]:
    return MATH_SPAN_RE.findall(text)


def strip_math_markup(text: str) -> str:
    """Remove $ delimiters and LaTeX commands, keeping letters and numbers."""
    s = text.replace("$", " ")
    s = re.sub(r"\\frac\{([^}]*)\}\{([^}]*)\}", r" \1 / \2 ", s)
    s = re.sub(r"\\[A-Za-z]+", " ", s)
    s = re.sub(r"[{}^_]", " ", s)
    return s


def words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", strip_math_markup(text).lower())


def window_words(text: str) -> list[str]:
    """Words for the originality window; a stock phrase becomes a break token so it never joins two windows."""
    joined = " ".join(words(text))
    for phrase in STOCK_PHRASES:
        joined = joined.replace(phrase, " | ")
    return joined.split()


def standardized_words(text: str) -> int:
    return math.ceil(len(text) / 6)


NUMERIC_RE = re.compile(r"^-?(\d+(\.\d+)?|\d*π|\d+/\d+|\d*π/\d+|\d+(\.\d+)?%)$")


def normalize_number(choice: str) -> str | None:
    """'$-\\frac{4}{5}$' -> '-4/5', '$2304\\pi$' -> '2304π', '$8,640$' -> '8640'; None if not a number."""
    s = choice.strip()
    if not (s.startswith("$") and s.endswith("$")):
        return None
    s = s.strip("$").replace(" ", "").replace(",", "")
    s = s.replace("\\left", "").replace("\\right", "").replace("\\%", "%")
    s = re.sub(r"\\frac\{([^}]*)\}\{([^}]*)\}", r"\1/\2", s)
    s = s.replace("\\pi", "π").replace("{", "").replace("}", "")
    return s if NUMERIC_RE.match(s) else None


def numeric_value(norm: str) -> float:
    s = norm.rstrip("%")
    sign = -1.0 if s.startswith("-") else 1.0
    s = s.lstrip("-")
    num, _, den = s.partition("/")
    factor = 1.0
    if "π" in num:
        factor = math.pi
        num = num.replace("π", "") or "1"
    value = float(num) * factor
    if den:
        value /= float(den)
    return sign * value


def choice_class(choice: str) -> str:
    if normalize_number(choice) is not None:
        return "numeric"
    s = choice.strip()
    if s.startswith("$") and s.endswith("$"):
        inner = s.strip("$")
        if re.search(r"=|<|>|\\(?:le|leq|ge|geq)(?![a-z])|\\neq", inner):
            return "equation"
        return "expression"
    return "sentence"


STOPWORDS = {"the", "a", "an", "of", "is", "are", "and", "or", "set", "data", "only", "each", "by", "in", "to"}


def math_form(text: str) -> str:
    """Whitespace-free comparison form of a math string: '$f(x) = 12 \\cdot 4^{x - 2}$' -> '12·4^(x-2)'."""
    s = text.replace("$", "")
    s = re.sub(r"\\(left|right)", "", s)
    s = s.replace("\\cdot", "·").replace("\\pi", "π").replace("\\le", "<=").replace("\\ge", ">=")
    s = re.sub(r"\\frac\{([^}]*)\}\{([^}]*)\}", r"(\1)/(\2)", s)
    s = re.sub(r"\\[A-Za-z]+", "", s)
    s = s.replace("{", "(").replace("}", ")")
    s = re.sub(r"\s+", "", s)
    s = re.sub(r"\^\(([a-z0-9])\)", r"^\1", s)  # 4^{x} -> 4^x
    # Drop a leading "f(x) =" or "y =" so the right-hand side alone can match.
    s = re.sub(r"^([a-zA-Z]\([a-z]\)|y)=", "", s)
    return s


def loose_form(text: str) -> str:
    """Looser comparison form for PR04: renders \\frac and \\sqrt the way prose writes them
    (a/b, sqrt(x)), then drops grouping, spacing and multiplication marks, so a byHand that writes
    "sqrt(d)/4.9" matches the choice "$t = \\frac{\\sqrt{d}}{4.9}$"."""
    s = text.replace("$", "")
    s = re.sub(r"\\(left|right)", "", s)
    s = s.replace("\\cdot", "").replace("\\times", "").replace("\\pi", "pi").replace("π", "pi")
    s = s.replace("\\pm", "±").replace("+/-", "±").replace("\\neq", "!=").replace("≠", "!=")
    s = s.replace("√", "sqrt").replace("\\%", "%").replace("{,}", ",")
    s = re.sub(r"\\geq?(?![a-z])", ">=", s)
    s = re.sub(r"\\leq?(?![a-z])", "<=", s)
    s = s.replace("≥", ">=").replace("≤", "<=")
    # innermost-first rewrites so nesting resolves
    for _ in range(6):
        s2 = re.sub(r"\\sqrt\[([^\[\]{}]*)\]\{([^{}]*)\}", r"root\1(\2)", s)
        s2 = re.sub(r"\\sqrt\{([^{}]*)\}", r"sqrt(\1)", s2)
        s2 = re.sub(r"\\[dt]?frac\{([^{}]*)\}\{([^{}]*)\}", r"(\1)/(\2)", s2)
        if s2 == s:
            break
        s = s2
    s = re.sub(r"\\[A-Za-z]+", "", s)
    s = s.lower()
    s = re.sub(r"^\s*([a-z](\([a-z]\))?)\s*=", "", s)  # drop a leading "t =" / "f(x) ="
    s = re.sub(r"[\s(){}\[\]*·]", "", s)
    s = s.replace("−", "-")
    return s


def spr_fits_bluebook(value: Fraction) -> bool:
    limit = MAX_NEGATIVE_LENGTH if value < 0 else MAX_POSITIVE_LENGTH
    frac = f"{value.numerator}" if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    if len(frac) <= limit:
        return True
    whole = str(abs(value.numerator) // value.denominator)
    return (1 if value < 0 else 0) + len(whole) + 2 <= limit


CONTEXT_WORDS = re.compile(
    r"\b(dollars?|cents?|price|cost|costs|fee|charges?|meters?|centimeters?|kilometers?|millimeters?|"
    r"grams?|kilograms?|milliliters?|liters?|feet|foot|inches|inch|yards?|miles?|hours?|minutes?|seconds|"
    r"days?|weeks?|months?|years?|students?|people|adults?|members?|population|survey|sample[sd]?|"
    r"store|shop|town|city|chemist|club|plants?|per|ohms?|volts?|watts?|degrees Fahrenheit|degrees Celsius)\b",
    re.I,
)


def is_in_context(stem: str) -> bool:
    return bool(CONTEXT_WORDS.search(stem))


XY_TRIGGER = re.compile(
    r"\bgraphs?\b|[xy]\$?-intercept|\bslope\b|\bparabola\b|\bline with equation\b",
    re.I,
)
# "intersect" alone also covers arcs and transversals; it needs the xy-plane only with an equation in y.
XY_INTERSECT = re.compile(r"\bintersect", re.I)
EQUATION_IN_Y = re.compile(r"\$[^$]*\by\s*=")
XY_PLANE = re.compile(r"xy\$?-plane", re.I)
WHERE_CONSTANT = re.compile(r"\bwhere\b[^.?]*\bconstants?\b", re.I)
PERSON = re.compile(r"\b(we|our|us|my|me|you|your|yours)\b|\bI\b(?![.,])", re.I)
PERSON_STRICT_I = re.compile(r"\bI\b(?![.,]|\s+(?:and|only)\b)")
FORBIDDEN_SOURCES = re.compile(r"college board|khan", re.I)
SINGLE_LETTER = re.compile(r"(?<![A-Za-z\\])([a-z])(?![A-Za-z(])")
FUNCTION_LETTER = re.compile(r"(?<![A-Za-z\\])([a-z])\(")


DECL_LIST = re.compile(
    r"(?:\b(?:where|let)\s+)?\$[a-z]\$(?:\s*,\s*\$[a-z]\$)*(?:\s*,?\s*and\s+\$[a-z]\$)?\s+(?:is|are)\b"
)


def undeclared_letters(stem: str) -> set[str]:
    """Lower-case single letters in math spans that are neither x/y, a function name, nor declared."""
    letters: set[str] = set()
    functions: set[str] = set()
    for span in math_spans(stem):
        cleaned = re.sub(r"\\[A-Za-z]+", " ", span)
        functions |= set(FUNCTION_LETTER.findall(cleaned))
        letters |= set(SINGLE_LETTER.findall(cleaned))
    letters -= {"x", "y"} | functions
    prose = stem.lower()
    declared = set()
    # Lists such as "$a$, $b$, and $c$ are constants" or "where $p$ and $q$ are ..." declare every
    # letter in the list (with or without the serial comma).
    for m in DECL_LIST.finditer(prose):
        declared |= set(re.findall(r"\$([a-z])\$", m.group(0)))
    for letter in letters:
        patterns = [
            rf"\${letter}\$\s*(is|are|and \$[a-z]\$ are|, \$[a-z]\$,? and \$[a-z]\$ are)\b",
            rf"\b(where|let|for every real number|for an angle measure|for a quantity)\s+\${letter}\$",
            rf"\bvalue of \${letter}\$",  # asked-for unknown
            rf"\${letter}\$\s*(weeks|days|hours|years|minutes|seconds|sides|atmospheres|kelvins)\b",
            rf"\${letter}\\%\$",
        ]
        if any(re.search(p, prose) for p in patterns):
            declared.add(letter)
    return letters - declared


# ---------------------------------------------------------------------------
# Item-level rules
# ---------------------------------------------------------------------------


def lint_item(item: dict, skills: dict[str, str], rep: Report) -> None:
    iid = item["id"]
    stem = item["stem"] or ""

    # Schema-ish
    if item["skill"] not in skills:
        rep.add(iid, "SK01", f"skill {item['skill']!r}")
    elif skills[item["skill"]] != item["domain"]:
        rep.add(iid, "SK02", f"{item['skill']!r} is a {skills[item['skill']]} skill, item is {item['domain']}")
    if item["difficulty"] not in DIFFICULTIES:
        rep.add(iid, "DF01", f"difficulty {item['difficulty']!r}")
    if item["domain"] not in DOMAINS:
        rep.add(iid, "DF01", f"domain {item['domain']!r}")
    if item["route"] not in ROUTES:
        rep.add(iid, "DF01", f"route {item['route']!r}")
    if item["format"] not in ("mc", "spr"):
        rep.add(iid, "DF01", f"format {item['format']!r}")

    # Choices
    if item["format"] == "mc":
        choices = item["choices"]
        if len(choices) != 4 or item["answerIndex"] not in (0, 1, 2, 3):
            rep.add(iid, "CH01", f"{len(choices)} choices, key {item['answerIndex']}")
        classes = [choice_class(c) for c in choices]
        if len(set(classes)) > 1:
            rep.add(iid, "CH02", ", ".join(f"{c!r}={k}" for c, k in zip(choices, classes)))
        if classes and classes[0] == "sentence" and len(set(c.strip().endswith(".") for c in choices)) > 1:
            rep.add(iid, "CH02", "some sentence choices end with a period and some do not")
        if classes and all(k == "numeric" for k in classes):
            vals = [numeric_value(normalize_number(c)) for c in choices]
            asc = all(a < b for a, b in zip(vals, vals[1:]))
            desc = all(a > b for a, b in zip(vals, vals[1:]))
            if not (asc or desc):
                rep.add(iid, "CH03", "values " + ", ".join(f"{v:g}" for v in vals))
        norm = [normalize_number(c) or c.strip().lower() for c in choices]
        if len(set(norm)) != len(norm):
            rep.add(iid, "CH04", str([c for c in norm if norm.count(c) > 1]))
        if classes and all(k == "numeric" for k in classes) and re.search(r"which of the following", stem, re.I):
            rep.add(iid, "ST04", "numeric choices; ask 'What is the value of ...?' instead")
        # Distractor coverage in byHand
        by = (item["byHand"] or "")
        by_flat = re.sub(r"\s+", " ", by.replace("\\", "")).lower()
        missing = []
        for i, c in enumerate(choices):
            if i == item["answerIndex"]:
                continue
            n = normalize_number(c)
            if n is not None:
                forms = {n, n.replace("π", "\\pi"), n.replace("π", "pi"), n.replace("π", "π")}
                if "/" in n and "π" not in n:
                    a, b = n.lstrip("-").split("/")
                    forms |= {f"{a}/{b}", f"-{a}/{b}"}
                if re.match(r"^-?\d{4,}$", n):
                    v = int(n)
                    forms.add(f"{v:,}")
                found = any(re.search(r"(?<![\d./])" + re.escape(f) + r"(?![\d/])", by_flat) for f in forms)
                if not found and c.strip().startswith("$"):
                    lc = loose_form(c)
                    found = bool(re.search(r"(?<![\d./])" + re.escape(lc) + r"(?![\d/])", loose_form(by)))
            elif c.strip().startswith("$"):
                found = math_form(c) in math_form(by) or loose_form(c) in loose_form(by)
            else:
                text = re.sub(r"[^a-z0-9 ]", " ", strip_math_markup(c).lower())
                toks = text.split()
                bigrams = [" ".join(toks[j:j + 2]) for j in range(len(toks) - 1)]
                content = [t for t in toks if t not in STOPWORDS]
                found = any(bg in by_flat for bg in bigrams) or (
                    len(toks) <= 3 and any(re.search(rf"\b{re.escape(t)}\b", by_flat) for t in content))
            if not found:
                missing.append(c)
        if missing:
            rep.add(iid, "PR04", "not mentioned: " + ", ".join(repr(m) for m in missing))
    else:
        for ans in item["answers"]:
            if not spr_fits_bluebook(ans):
                rep.add(iid, "SP01", f"{ans} does not fit")
        if not item["answers"]:
            rep.add(iid, "SP01", "no answers")

    # Stem conventions
    xy_hit = XY_TRIGGER.search(stem) or (XY_INTERSECT.search(stem) if EQUATION_IN_Y.search(stem) else None)
    if xy_hit and not XY_PLANE.search(stem):
        rep.add(iid, "ST03", "trigger: " + xy_hit.group(0))
    letters = undeclared_letters(stem)
    if letters:
        rep.add(iid, "ST01", "letters " + ", ".join(sorted(letters)))
    if re.search(r"\bconstants?\b", stem, re.I) and not WHERE_CONSTANT.search(stem):
        rep.add(iid, "ST02", "declared without a 'where' clause")
    if is_in_context(stem):
        n = standardized_words(stem)
        if n > CONTEXT_WORD_LIMIT:
            rep.add(iid, "ST05", f"{n} standardized words ({len(stem)} characters)")
    tail = stem.strip()
    tail = re.sub(r"\s*\([^()]*\)\s*$", "", tail)  # trailing note such as (1 kilometer = 1,000 meters)
    tail = re.sub(r"\s*I\.\s.*?\bII\.\s.*?\bIII\.\s.*$", "", tail, flags=re.S)  # trailing I/II/III list
    if not tail.endswith("?"):
        rep.add(iid, "ST06", f"ends with {tail[-25:]!r}")
    prose_only = MATH_SPAN_RE.sub(" ", stem)
    m = PERSON.search(prose_only) or PERSON_STRICT_I.search(prose_only)
    if m:
        rep.add(iid, "ST07", f"found {m.group(0)!r}")
    if FORBIDDEN_SOURCES.search(stem):
        rep.add(iid, "OR02", FORBIDDEN_SOURCES.search(stem).group(0))
    # Dollar signs: odd count, escaped \$, or prose leaked into a math span (money written as $5.50)
    if stem.count("$") % 2:
        rep.add(iid, "ST08", "odd number of $ delimiters")
    if "\\$" in stem or any("\\$" in c for c in item.get("choices", [])):
        rep.add(iid, "ST08", "escaped \\$ is not rendered by MathText")
    for span in math_spans(stem):
        if re.search(r"[A-Za-z]{3,}\s+[A-Za-z]{3,}\s+[A-Za-z]{3,}", re.sub(r"\\[A-Za-z]+", "", span)):
            rep.add(iid, "ST08", f"prose inside a math span: {span[:40]!r}")
            break
    if re.search(r"\$\d+(\.\d+)?\s", stem) and not re.search(r"\$\d+(\.\d+)?\s*(\\|[-+=<>])", stem):
        rep.add(iid, "ST08", "'$<number> ' looks like a price; write 'dollars'")
    if is_in_context(stem):
        q = re.search(r"what is the (cost|price|height|length|width|mass|volume|area|speed|distance|temperature|"
                      r"perimeter|circumference|weight)\b([^?]*)\?", stem, re.I)
        if q and not re.search(r",\s*in\s+[a-z ]+[,?]?", q.group(2) + "?", re.I):
            rep.add(iid, "ST09", f"'what is the {q.group(1)}' without ', in <unit>,'")

    # Provenance / process
    prov = item["provenance"] or {}
    if not prov.get("author"):
        rep.add(iid, "PR01")
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", prov.get("created") or ""):
        rep.add(iid, "PR02", f"created {prov.get('created')!r}")
    if not (item["byHand"] or "").strip():
        rep.add(iid, "PR03")
    has_tech = bool(item["techniques"])
    has_desmos = item["desmos"] is not None
    if has_tech != has_desmos:
        rep.add(iid, "DS01", f"techniques={item['techniques']}, desmos={'present' if has_desmos else 'absent'}")
    if has_desmos:
        d = item["desmos"]
        if d["verified"] is None:
            rep.add(iid, "DS02", f"verified is {d['verified_raw']!r}")
        if not d["lines"] or not d["read"]:
            rep.add(iid, "DS02", "lines or read missing")


# ---------------------------------------------------------------------------
# Bank-level rules
# ---------------------------------------------------------------------------


def lint_bank(items: list[dict], rep: Report) -> dict:
    n = len(items)
    ids = Counter(i["id"] for i in items)
    for iid, c in ids.items():
        if c > 1:
            rep.add(iid, "ID01", f"appears {c} times")

    mc = [i for i in items if i["format"] == "mc"]
    key_pos = Counter(i["answerIndex"] for i in mc)
    for pos, c in sorted(key_pos.items()):
        if mc and c / len(mc) > KEY_POSITION_MAX_SHARE:
            rep.add("(bank)", "CH05", f"key index {pos} ('{'ABCD'[pos]}') holds {c}/{len(mc)} = {c/len(mc):.0%}")

    spr_domains = {i["domain"] for i in items if i["format"] == "spr"}
    for dom in ("psda", "geometry-trig"):
        if dom not in spr_domains:
            rep.add("(bank)", "SP02", f"no SPR item in {dom}")

    # Originality: shared 10-word windows across stems
    seen: dict[tuple, str] = {}
    reported: set[tuple[str, str]] = set()
    for it in items:
        toks = window_words(it["stem"] or "")
        for j in range(len(toks) - WINDOW_WORDS + 1):
            win = tuple(toks[j:j + WINDOW_WORDS])
            if "|" in win:
                continue
            other = seen.get(win)
            if other and other != it["id"] and (other, it["id"]) not in reported:
                reported.add((other, it["id"]))
                rep.add(it["id"], "OR01", f"shares with {other}: '{' '.join(win)}'")
            seen.setdefault(win, it["id"])

    # Distribution
    stats = {
        "n": n,
        "domain": Counter(i["domain"] for i in items),
        "format": Counter(i["format"] for i in items),
        "difficulty": Counter(i["difficulty"] for i in items),
        "route": Counter(i["route"] for i in items),
        "context": sum(1 for i in items if is_in_context(i["stem"] or "")),
        "key_pos": key_pos,
        "mc": len(mc),
    }
    if n:
        for dom, target in DOMAIN_TARGET.items():
            share = stats["domain"][dom] / n
            if abs(share - target) > DOMAIN_TOLERANCE:
                rep.add("(bank)", "BK01", f"{dom} {stats['domain'][dom]}/{n} = {share:.0%}, target {target:.0%}")
        spr_share = stats["format"]["spr"] / n
        if abs(spr_share - SPR_TARGET) > SPR_TOLERANCE:
            rep.add("(bank)", "BK02", f"spr {stats['format']['spr']}/{n} = {spr_share:.0%}, target {SPR_TARGET:.0%}")
        ctx_share = stats["context"] / n
        if abs(ctx_share - CONTEXT_TARGET) > CONTEXT_TOLERANCE:
            rep.add("(bank)", "BK03", f"in context {stats['context']}/{n} = {ctx_share:.0%}, target {CONTEXT_TARGET:.0%}")
        for level in DIFFICULTIES:
            if stats["difficulty"][level] == 0:
                rep.add("(bank)", "BK04", f"no {level} items")
        for route in ROUTES:
            if stats["route"][route] == 0:
                rep.add("(bank)", "BK04", f"no {route} items")
    return stats


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------


def print_rules() -> None:
    for rid, (sev, msg) in RULES.items():
        print(f"{rid}  {sev:5}  {msg}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--rules", action="store_true", help="list rules and exit")
    ap.add_argument("--quiet", action="store_true", help="counts only")
    ap.add_argument("--items", type=Path, default=None, help="path to items.ts (default: web/content/items.ts)")
    args = ap.parse_args(argv)
    if args.rules:
        print_rules()
        return 0

    items = load_items(args.items) if args.items else load_items()
    skills = {name: dom for dom, name in load_skills()}
    if len(skills) != 19:
        print(f"warning: expected 19 skills in skills.ts, found {len(skills)}", file=sys.stderr)

    rep = Report()
    for it in items:
        lint_item(it, skills, rep)
    stats = lint_bank(items, rep)

    if not args.quiet and rep.rows:
        width = max(len(r[0]) for r in rep.rows)
        print(f"{'item':{width}}  rule  sev    detail")
        for iid, rule, sev, detail in sorted(rep.rows, key=lambda r: (r[2] != "error", r[0], r[1])):
            print(f"{iid:{width}}  {rule}  {sev:5}  {detail}")
        print()

    counts = Counter(r[1] for r in rep.rows)
    print("counts by rule:")
    for rid in RULES:
        if counts[rid]:
            print(f"  {rid}  {RULES[rid][0]:5}  {counts[rid]:3}  {RULES[rid][1]}")
    n = stats["n"]
    print(f"\n{n} items; {rep.errors} error(s), {len(rep.rows) - rep.errors} warning(s)")
    if n:
        dom = stats["domain"]
        print("domain:     " + ", ".join(f"{d} {dom[d]} ({dom[d]/n:.0%}, target {DOMAIN_TARGET[d]:.0%})" for d in DOMAINS))
        print(f"format:     mc {stats['format']['mc']} / spr {stats['format']['spr']} ({stats['format']['spr']/n:.0%} spr, target 25%)")
        print(f"context:    {stats['context']} ({stats['context']/n:.0%}, target 30%)")
        print("difficulty: " + ", ".join(f"{k} {stats['difficulty'][k]}" for k in DIFFICULTIES))
        print("route:      " + ", ".join(f"{k} {stats['route'][k]}" for k in ROUTES))
        if stats["mc"]:
            print("key index:  " + ", ".join(f"{'ABCD'[p]} {stats['key_pos'][p]}" for p in range(4)))
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
