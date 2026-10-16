"""The question bank: 1,000 original SAT Math questions from app/content/bank/.

items.jsonl comes from the item pipeline on the scaffold-course-site branch
(data/items.jsonl). This module turns each item into what the site shows:
the question as HTML, its answer key, and a full explanation that walks
through the Desmos route and the by-hand route.

Nothing here touches the database, so website/build.py can import it to
build the offline preview from the same source.
"""
import html
import json
import re
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

BANK_DIR = Path(__file__).resolve().parent.parent / "content" / "bank"

LETTERS = "ABCD"
DIFFICULTY_ORDER = {"easy": 0, "medium": 1, "hard": 2}

# Questions per domain in one practice module (the real test draws 13–15 Algebra and
# Advanced Math and 5–7 of the other two per 44 questions, so about half that per module).
MODULE_MIX = {"algebra": 8, "advanced-math": 8, "psda": 3, "geometry-trig": 3}
MODULE_MINUTES = 35

ROUTE_ADVICE = {
    "desmos-primary": "Desmos is the fastest route here. Graph it, read the answer, then sanity-check it.",
    "hand-primary": "Solving by hand is faster on this one. Use Desmos as a quick check if you have time.",
    "either": "Both routes take about the same time. Use the one you trust more, and the other to check.",
}


# ---------- math rendering ----------

SYMBOLS = {
    "le": "≤", "leq": "≤", "ge": "≥", "geq": "≥", "ne": "≠", "neq": "≠", "pi": "π", "circ": "°",
    "ell": "ℓ", "cdot": "·", "theta": "θ", "pm": "±", "times": "×", "div": "÷", "angle": "∠",
    "alpha": "α", "beta": "β", "infty": "∞", "approx": "≈", "sim": "~", "degree": "°",
    "%": "%", "$": "$", ",": "\u2009", " ": " ", ";": " ", "!": "", "{": "{", "}": "}", "|": "‖",
}
FUNCTIONS = {"sin", "cos", "tan", "arcsin", "arccos", "arctan", "log", "ln", "sec", "csc", "cot", "min", "max"}
TEXT_COMMANDS = {"text", "mathrm", "textrm", "mathit", "operatorname", "mathbf", "textbf"}
FRACTIONS = {"frac", "dfrac", "tfrac"}


class _Math:
    """A small LaTeX-to-HTML converter for the subset the bank uses."""

    def __init__(self, src, prose=False):
        self.s, self.i, self.prose = src, 0, prose

    def peek(self):
        return self.s[self.i] if self.i < len(self.s) else ""

    def command(self):
        self.i += 1  # the backslash
        m = re.match(r"[A-Za-z]+", self.s[self.i:])
        if m:
            self.i += m.end()
            return m.group(0)
        ch = self.peek()
        self.i += 1
        return ch

    def group(self):
        """A {...} group, or one token when there are no braces."""
        while self.peek() == " ":
            self.i += 1
        if self.peek() == "{":
            self.i += 1
            inner = self.run("}")
            self.i += 1
            return inner
        return self.token()

    def script(self):
        """What follows ^ or _. In prose, x^2y means x²·y and 2^(n+1) keeps the parentheses' contents."""
        if not self.prose or self.peek() == "{":
            return self.group()
        if self.peek() == "(":
            depth, start = 0, self.i
            while self.i < len(self.s):
                c = self.s[self.i]
                depth += c == "("
                depth -= c == ")"
                self.i += 1
                if depth == 0:
                    break
            return _Math(self.s[start + 1:self.i - 1], prose=True).run()
        m = re.match(r"-?(\d+(\.\d+)?|[A-Za-z])", self.s[self.i:])
        if m:
            self.i += m.end()
            return _Math(m.group(0), prose=True).run()
        return self.token()

    def token(self):
        ch = self.peek()
        if not ch:
            return ""
        if ch == "\\":
            return self.after_command(self.command())
        if ch == "{":
            self.i += 1
            inner = self.run("}")
            self.i += 1
            return inner
        self.i += 1
        if ch.isalpha() and not self.prose:
            word = ch
            while self.peek().isalpha():
                word += self.peek()
                self.i += 1
            return f"<var>{html.escape(word)}</var>"
        if ch == "-" and not self.prose:
            return "−"
        if ch == "~":
            return "~"
        return html.escape(ch)

    def after_command(self, name):
        if name in FRACTIONS:
            top, bottom = self.group(), self.group()
            return f'<span class="frac"><span>{top}</span><span>{bottom}</span></span>'
        if name == "sqrt":
            index = ""
            if self.peek() == "[":
                end = self.s.index("]", self.i)
                index = f"<sup class=\"root-index\">{html.escape(self.s[self.i + 1:end])}</sup>"
                self.i = end + 1
            return f'<span class="sqrt">{index}√<span class="sqrt-arg">{self.group()}</span></span>'
        if name in ("left", "right"):
            if self.peek() == "\\":
                sym = self.command()
                return html.escape(SYMBOLS.get(sym, sym))
            ch = self.peek()
            self.i += 1
            return "" if ch == "." else html.escape(ch)
        if name in TEXT_COMMANDS:
            while self.peek() == " ":
                self.i += 1
            if self.peek() == "{":
                end = self._match_brace(self.i)
                inner = self.s[self.i + 1:end]
                self.i = end + 1
                return html.escape(inner)
            return ""
        if name in FUNCTIONS:
            return name
        if name in SYMBOLS:
            return SYMBOLS[name]
        return html.escape(name)

    def _match_brace(self, start):
        depth = 0
        for j in range(start, len(self.s)):
            depth += self.s[j] == "{"
            depth -= self.s[j] == "}"
            if depth == 0:
                return j
        return len(self.s) - 1

    def run(self, stop=""):
        out = []
        while self.i < len(self.s) and self.peek() != stop:
            ch = self.peek()
            if ch in "^_":
                self.i += 1
                tag = "sup" if ch == "^" else "sub"
                out.append(f"<{tag}>{self.script()}</{tag}>")
            elif ch == "}" and stop != "}":
                self.i += 1  # stray brace
            else:
                out.append(self.token())
        return "".join(out)


def math_html(src):
    return _Math(src).run()


def rich_html(text):
    """Text that mixes words with $...$ math, as HTML. Bare LaTeX and x^2 outside $...$ also render."""
    parts = re.split(r"(?<!\\)\$", text or "")
    out = []
    for k, part in enumerate(parts):
        if k % 2:
            out.append(math_html(part))
        else:
            out.append(_Math(part.replace("\\$", "$"), prose=True).run().replace(" - ", " − "))
    return "".join(out)


def keystrokes(latex):
    """A Desmos line as the keys a student types: \\frac{a}{b} becomes (a)/(b), \\sqrt{x} becomes sqrt(x)."""
    s = re.sub(r"\\(pi|theta)(?=[A-Za-z\\])", r"\\\1 ", latex)
    s = re.sub(r"\\operatorname\{([^{}]*)\}", r"\1", s)
    s = re.sub(r"\\(left|right)\\?([()\[\]|{}])", r"\2", s)
    for _ in range(6):  # innermost first, so nested fractions and roots unwind
        s = re.sub(r"\\[dt]?frac\{([^{}]*)\}\{([^{}]*)\}", lambda m: f"{_wrap(m.group(1))}/{_wrap(m.group(2))}", s)
        s = re.sub(r"\\sqrt\{([^{}]*)\}", r"sqrt(\1)", s)
        s = re.sub(r"\^\{([^{}]*)\}", lambda m: "^" + _wrap(m.group(1)), s)
        s = re.sub(r"_\{([^{}]*)\}", r"_\1", s)
    s = s.replace("\\cdot", "*").replace("\\sim", "~").replace("\\le", "<=").replace("\\ge", ">=")
    s = s.replace("\\pi", "pi").replace("\\theta", "theta").replace("\\div", "/").replace("\\{", "{").replace("\\}", "}")
    s = re.sub(r"\\([A-Za-z]+)", r"\1", s)
    return s.replace(">==", ">=").replace("<==", "<=")


def _wrap(expr):
    return expr if re.fullmatch(r"-?[A-Za-z0-9.]+(\([^()]*\))?", expr) else f"({expr})"


# ---------- answers ----------

def fraction_text(fr):
    return str(fr.numerator) if fr.denominator == 1 else f"{fr.numerator}/{fr.denominator}"


def accepted_entries(fr):
    """What a student can type for an exact answer, following the Bluebook entry rules."""
    if fr.denominator == 1:
        return [str(fr.numerator)]
    width = 6 if fr < 0 else 5
    sign = "-" if fr < 0 else ""
    a = abs(fr)
    whole = a.numerator // a.denominator
    out = []
    if len(fraction_text(fr)) <= width:
        out.append(fraction_text(fr))
    for lead in ([str(whole)] if whole else ["", "0"]):
        places = width - len(sign) - len(lead) - 1
        if places < 1:
            continue
        exact = next((p for p in range(1, places + 1) if (a * 10 ** p).denominator == 1), None)
        if exact:
            out.append(sign + lead + "." + _digits(a, exact, False))
        else:
            for rounding in (False, True):
                digits = _digits(a, places, rounding)
                if digits:
                    out.append(sign + lead + "." + digits)
    return list(dict.fromkeys(out))


def _digits(a, places, rounding):
    """The decimal digits of a (0 <= a), cut or rounded to `places`."""
    scaled = a * 10 ** places
    n = (scaled + Fraction(1, 2)).__floor__() if rounding else scaled.__floor__()
    n -= (a.numerator // a.denominator) * 10 ** places
    if n >= 10 ** places:
        return None  # rounding carries into the whole number; the cut-off form still counts
    return str(n).rjust(places, "0")


SPR_PATTERN = re.compile(r"^-?(\d+\.?\d*|\.\d+|\d+/\d+)$")


def parse_entry(raw):
    """A typed answer as an exact Fraction, or None if it isn't a valid entry."""
    text = re.sub(r"\s+", "", str(raw or ""))
    if not text or not SPR_PATTERN.match(text):
        return None
    neg = text.startswith("-")
    body = text.lstrip("-")
    if "/" in body:
        top, bottom = body.split("/")
        if int(bottom) == 0:
            return None
        value = Fraction(int(top), int(bottom))
    else:
        value = Fraction(body)
    return -value if neg else value


def spr_matches(raw, key):
    """True if a typed answer earns credit for the exact answer key.

    Exact values always count. A decimal that can't be exact counts when it fills every
    space (5 characters, 6 with a minus sign) and is the key truncated or rounded, as on
    the real test: for 2/3, .6666, .6667, 0.666 and 0.667 count, but 0.67 does not.
    """
    text = re.sub(r"\s+", "", str(raw or ""))
    value = parse_entry(text)
    if value is None:
        return False
    if value == key:
        return True
    if "/" in text or "." not in text:
        return False
    width = 6 if text.startswith("-") else 5
    if len(text) < width:
        return False
    places = len(text.split(".")[1])
    target = abs(key)
    trunc = Fraction(target.numerator * 10 ** places // target.denominator, 10 ** places)
    rounded = Fraction(round(target * 10 ** places), 10 ** places)
    return (value < 0) == (key < 0) and abs(value) in (trunc, rounded)


# ---------- explanations ----------

STEP_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z(√$])")
TRAP_START = re.compile(r"^(The trap|A common (trap|mistake|error)|Common (mistake|error)|Trap:|Watch out)", re.I)


def _clean(text):
    """Drops the item writers' internal technique codes, like "(T13)" or "the proposed T15 move"."""
    text = re.sub(r"\s*\((the )?(proposed )?T\d+( move| picture)?\)", "", text or "")
    text = re.sub(r"\((the )?proposed T\d+ (move|picture):\s*", "(", text)
    text = re.sub(r"(,\s*|:\s*|\s+)(the )?(proposed )?T\d+( move| picture)?(?=[).:;,\s])", "", text)
    return text.replace("()", "")


def _split_hand(text):
    """By-hand text as (steps, distractor notes, trap notes)."""
    text = _clean(text)
    distractors = []
    m = re.search(r"\bDistractors?:\s*", text)
    if m:
        tail = text[m.end():].strip()
        text = text[:m.start()].strip()
        distractors = [d.strip().rstrip(".") for d in re.split(r";\s+", tail) if d.strip()]
    sentences = [s.strip() for s in STEP_SPLIT.split(text) if s.strip()]
    steps, traps = [], []
    for s in sentences:
        (traps if TRAP_START.match(s) else steps).append(s)
    return steps, distractors, traps


def _sentence(text):
    text = text.strip()
    return text[0].upper() + text[1:] if text else text


def explanation_html(item, techniques):
    """The full worked explanation for one item, as HTML."""
    steps, distractors, traps = _split_hand(item["byHand"])
    desmos = item.get("desmos")
    route = item["route"] if desmos else "hand-primary"
    techs = [techniques[t] for t in item.get("techniques", []) if t in techniques]

    parts = ['<div class="xp">']
    answer = answer_display_html(item)
    parts.append(f'<p class="xp-answer"><span class="label">Answer</span> <strong>{answer}</strong></p>')

    advice = ROUTE_ADVICE[route] if desmos else "Solve this one by hand. A graph doesn't make it faster."
    parts.append(f'<section class="xp-sec xp-route"><h4>Best approach</h4><p>{html.escape(advice)}</p></section>')

    desmos_sec = ""
    if desmos:
        title = "Desmos hack" if route != "hand-primary" else "Check it with Desmos"
        name = techs[0]["name"] if techs else ""
        head = f"{title}: {html.escape(name)}" if name else title
        lines = "".join(
            f'<li>Type <code class="keys">{html.escape(keystrokes(line))}</code>'
            f'<span class="xp-pretty" aria-hidden="true">{math_html(line)}</span></li>'
            for line in desmos["lines"])
        read = f"<li>{rich_html(_clean(desmos['read']))}</li>" if desmos.get("read") else ""
        why = f'<p class="xp-why">{rich_html(techs[0]["summary"])}</p>' if techs else ""
        tip = ""
        if techs and techs[0].get("pitfalls"):
            tip = f'<p class="xp-tip"><strong>Watch out:</strong> {rich_html(techs[0]["pitfalls"][0])}</p>'
        desmos_sec = (f'<section class="xp-sec xp-desmos"><h4>{head}</h4>{why}'
                      f'<ol class="xp-steps">{lines}{read}</ol>{tip}</section>')

    hand_sec = ""
    if steps:
        items_html = "".join(f"<li>{rich_html(s)}</li>" for s in steps)
        hand_sec = f'<section class="xp-sec xp-hand"><h4>Solve it by hand</h4><ol class="xp-steps">{items_html}</ol></section>'

    parts.extend([desmos_sec, hand_sec] if route == "desmos-primary" else [hand_sec, desmos_sec])

    if distractors:
        lis = "".join(f"<li>{rich_html(_sentence(d))}.</li>" for d in distractors)
        parts.append(f'<section class="xp-sec xp-wrong"><h4>Why the other choices are tempting</h4><ul>{lis}</ul></section>')
    if traps:
        lis = "".join(f"<li>{rich_html(t)}</li>" for t in traps)
        parts.append(f'<section class="xp-sec xp-wrong"><h4>Common trap</h4><ul>{lis}</ul></section>')

    if item["format"] == "spr":
        keys = [Fraction(a["num"], a["den"]) for a in item["answers"]]
        forms = []
        for k in keys:
            forms.extend(accepted_entries(k))
        shown = ", ".join(f"<code>{html.escape(f)}</code>" for f in dict.fromkeys(forms))
        note = ""
        if any(k.denominator != 1 and (Fraction(k) * 10 ** 4).denominator != 1 for k in keys):
            note = " A shorter decimal, like 0.67 for 2/3, is marked wrong: fill every space."
        parts.append(f'<section class="xp-sec xp-entry"><h4>Entering your answer</h4><p>Any of these earns credit: {shown}.{html.escape(note)}</p></section>')

    parts.append("</div>")
    return "".join(p for p in parts if p)


def answer_display_html(item):
    if item["format"] == "mc":
        k = item["answerIndex"]
        return f"{LETTERS[k]}. {rich_html(item['choices'][k])}"
    return " or ".join(html.escape(fraction_text(Fraction(a["num"], a["den"]))) for a in item["answers"])


# ---------- loading ----------

def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


@lru_cache(maxsize=None)
def meta():
    skills = json.loads((BANK_DIR / "skills.json").read_text())
    techniques = {t["id"]: t for t in json.loads((BANK_DIR / "techniques.json").read_text())["techniques"]}
    return skills, techniques


@lru_cache(maxsize=None)
def all_items():
    """Every item, ready to serve: {id: question}. Keys stay on the server."""
    skills, techniques = meta()
    names = skills["domains"]
    items = {}
    for line in (BANK_DIR / "items.jsonl").read_text().splitlines():
        if not line.strip():
            continue
        raw = json.loads(line)
        q = {
            "id": raw["id"],
            "domain_key": raw["domain"],
            "domain": names[raw["domain"]],
            "skill": raw["skill"],
            "skill_key": slug(raw["skill"]),
            "difficulty": raw["difficulty"],
            "type": raw["format"],
            "stem": rich_html(raw["stem"]),
            "explain_html": explanation_html(raw, techniques),
        }
        if raw["format"] == "mc":
            q["choices"] = [rich_html(c) for c in raw["choices"]]
            q["answer"] = raw["answerIndex"]
        else:
            q["keys"] = [[a["num"], a["den"]] for a in raw["answers"]]
            q["answer_text"] = " or ".join(fraction_text(Fraction(n, d)) for n, d in q["keys"])
        items[q["id"]] = q
    return items


@lru_cache(maxsize=None)
def topics():
    """Domains in test order, each with its skills, as listed in skills.json."""
    skills, _ = meta()
    counts = {}
    for q in all_items().values():
        counts.setdefault(q["domain_key"], {}).setdefault(q["skill"], 0)
        counts[q["domain_key"]][q["skill"]] += 1
    out = []
    for key, name in skills["domains"].items():
        listed = [s["name"] for s in skills["skills"] if s["domain"] == key]
        extra = sorted(set(counts.get(key, {})) - set(listed))
        out.append({"key": key, "name": name, "skills": [
            {"key": slug(s), "name": s, "total": counts[key][s]} for s in listed + extra if counts.get(key, {}).get(s)]})
    return out


def pool(domain=None, skill=None):
    """Item ids for a topic: one skill, one domain, or the whole bank."""
    return [q["id"] for q in all_items().values()
            if (not domain or q["domain_key"] == domain) and (not skill or q["skill_key"] == skill)]


# ---------- grading ----------

def is_correct(q, answer):
    if answer is None or answer == "":
        return False
    if q["type"] == "mc":
        return answer == q["answer"]
    return any(spr_matches(answer, Fraction(n, d)) for n, d in q["keys"])


def public_question(q):
    """The question as the student sees it before answering."""
    out = {k: q[k] for k in ("id", "domain", "skill", "difficulty", "type", "stem") if k in q}
    if q["type"] == "mc":
        out["choices"] = q["choices"]
    return out


def graded_question(q, index, answer):
    ok = is_correct(q, answer)
    answered = answer is not None and answer != ""
    item = {
        "index": index, "id": q["id"], "type": q["type"], "domain": q["domain"], "skill": q["skill"],
        "difficulty": q["difficulty"], "stem": q["stem"], "correct": ok, "answered": answered,
        "your_answer": (LETTERS[answer] if q["type"] == "mc" else str(answer)) if answered else None,
        "answer": LETTERS[q["answer"]] if q["type"] == "mc" else q["answer_text"],
        "explain_html": q["explain_html"],
    }
    if q["type"] == "mc":
        item["choices"] = q["choices"]
        item["answer_index"] = q["answer"]
    return item


def clean_answer(q, value):
    """A well-formed answer for one question, or None."""
    if value is None or value == "":
        return None
    if q["type"] == "mc":
        if isinstance(value, int) and not isinstance(value, bool) and 0 <= value < len(q["choices"]):
            return value
        return None
    text = re.sub(r"\s+", "", str(value))[:6]
    return text or None


def grade(item_ids, answers):
    """Grades a whole set. answers: {index: answer}. Same shape as services.grading.grade."""
    items = all_items()
    questions, by_domain, correct = [], {}, 0
    mc = {"right": 0, "total": 0}
    spr = {"right": 0, "total": 0}
    for i, item_id in enumerate(item_ids):
        q = items[item_id]
        g = graded_question(q, i, answers.get(i))
        correct += g["correct"]
        bucket = mc if q["type"] == "mc" else spr
        bucket["total"] += 1
        bucket["right"] += g["correct"]
        d = by_domain.setdefault(q["domain"], {"domain": q["domain"], "right": 0, "total": 0})
        d["total"] += 1
        d["right"] += g["correct"]
        questions.append(g)
    return {"correct": correct, "total": len(item_ids), "multiple_choice": mc, "student_produced": spr,
            "by_domain": list(by_domain.values()), "questions": questions}
