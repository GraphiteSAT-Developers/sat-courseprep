"""Shared reader for web/content/items.ts (and the skill table in skills.ts).

Both verify_items.py and lint_items.py import this module, so there is a single
regex parser to keep in sync with the TypeScript schema in web/content/types.ts.
Stdlib only.

parse_items(source) -> list[dict] with these keys per item:
  id, format ("mc" | "spr"), domain, skill, difficulty, stem, route,
  techniques (list[str]), byHand (str), provenance (dict: author, created,
  notes?), desmos (dict: lines, read, verified) or None, and either
  choices (list[str]) + answerIndex (int) for MC or answers (list[Fraction])
  for SPR.

String values are unescaped the way the TS runtime would see them, so a stem
written "$\\frac{1}{2}$" in the file comes back as "$\frac{1}{2}$".
"""

from __future__ import annotations

import re
from fractions import Fraction
from pathlib import Path

CONTENT_DIR = Path(__file__).resolve().parents[1] / "content"
ITEMS_TS = CONTENT_DIR / "items.ts"
SKILLS_TS = CONTENT_DIR / "skills.ts"

DOMAINS = ("algebra", "advanced-math", "psda", "geometry-trig")
DIFFICULTIES = ("easy", "medium", "hard")
ROUTES = ("desmos-primary", "hand-primary", "either")

_STRING_RE = re.compile(r'"((?:[^"\\]|\\.)*)"')


def _unescape_ts(s: str) -> str:
    """Turn a TS double-quoted string body into its runtime value."""
    out = []
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == "\\" and i + 1 < len(s):
            nxt = s[i + 1]
            out.append({"n": "\n", "t": "\t"}.get(nxt, nxt))
            i += 2
        else:
            out.append(ch)
            i += 1
    return "".join(out)


def _string_field(block: str, key: str) -> str | None:
    m = re.search(r'(?<![A-Za-z])' + re.escape(key) + r':\s*' + _STRING_RE.pattern, block)
    return _unescape_ts(m.group(1)) if m else None


def _string_array(block: str, key: str) -> list[str] | None:
    """Parse `key: [ "a", "b", ... ]`, honouring escapes and `]` inside strings."""
    m = re.search(r'(?<![A-Za-z])' + re.escape(key) + r':\s*\[', block)
    if not m:
        return None
    i = m.end()
    out: list[str] = []
    while i < len(block):
        ch = block[i]
        if ch == "]":
            return out
        if ch == '"':
            sm = _STRING_RE.match(block, i)
            if not sm:
                raise ValueError(f"unterminated string in {key} array")
            out.append(_unescape_ts(sm.group(1)))
            i = sm.end()
            continue
        i += 1
    raise ValueError(f"unterminated {key} array")


def _parse_provenance(block: str) -> dict | None:
    m = re.search(r"provenance:\s*\{(.*?)\}", block, re.S)
    if not m:
        return None
    body = m.group(1)
    prov = {}
    for key in ("author", "created", "notes"):
        val = _string_field(body, key)
        if val is not None:
            prov[key] = val
    return prov


def _parse_desmos(block: str) -> dict | None:
    m = re.search(r"desmos:\s*\{", block)
    if not m:
        return None
    # Find the matching closing brace, skipping braces inside strings.
    i, depth = m.end(), 1
    while i < len(block) and depth:
        ch = block[i]
        if ch == '"':
            sm = _STRING_RE.match(block, i)
            i = sm.end() if sm else i + 1
            continue
        depth += {"{": 1, "}": -1}.get(ch, 0)
        i += 1
    body = block[m.end():i - 1]
    verified_m = re.search(r"verified:\s*([A-Za-z0-9_\"']+)", body)
    verified_raw = verified_m.group(1) if verified_m else None
    return {
        "lines": _string_array(body, "lines"),
        "read": _string_field(body, "read"),
        "verified": {"true": True, "false": False}.get(verified_raw, None),
        "verified_raw": verified_raw,
    }


def parse_items(source: str) -> list[dict]:
    """Split items.ts on `id: "..."` markers and parse every field of each item."""
    items: list[dict] = []
    starts = [m.start() for m in re.finditer(r'^\s*id: "', source, re.M)]
    for i, start in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else len(source)
        block = source[start:end]
        item: dict = {"id": _string_field(block, "id")}
        item["format"] = _string_field(block, "format")
        item["domain"] = _string_field(block, "domain")
        item["skill"] = _string_field(block, "skill")
        item["difficulty"] = _string_field(block, "difficulty")
        item["route"] = _string_field(block, "route")
        item["stem"] = _string_field(block, "stem")
        item["byHand"] = _string_field(block, "byHand")
        item["techniques"] = _string_array(block, "techniques")
        item["provenance"] = _parse_provenance(block)
        item["desmos"] = _parse_desmos(block)
        if item["format"] == "mc":
            item["choices"] = _string_array(block, "choices") or []
            am = re.search(r"answerIndex:\s*(\d)", block)
            item["answerIndex"] = int(am.group(1)) if am else None
        else:
            raw = re.search(r"answers:\s*\[(.*?)\]", block, re.S)
            item["answers"] = [
                Fraction(int(n), int(d))
                for n, d in re.findall(r"num:\s*(-?\d+),\s*den:\s*(\d+)", raw.group(1) if raw else "")
            ]
        items.append(item)
    return items


def load_items(path: Path = ITEMS_TS) -> list[dict]:
    return parse_items(path.read_text(encoding="utf-8"))


def parse_skills(source: str) -> list[tuple[str, str]]:
    """(domain, exact skill name) pairs from the SKILLS array in skills.ts."""
    return re.findall(r'domain:\s*"([a-z-]+)",\s*name:\s*"((?:[^"\\]|\\.)*)"', source)


def load_skills(path: Path = SKILLS_TS) -> list[tuple[str, str]]:
    return parse_skills(path.read_text(encoding="utf-8"))
