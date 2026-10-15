"""Apply fixes from docs/review/chunk-*.jsonl to web/content/items.ts.

Each finding's "fix" names a field, the exact current text ("old", as the
parsed bank shows it) and a replacement ("new"). Text is re-escaped for the
TypeScript source before matching, and every replacement must match exactly
once inside that item's own entry, or the fix is skipped and reported.

usage:
    python3 web/scripts/apply_review_fixes.py docs/review/chunk-*.jsonl [--dry-run] [--severity error]
"""

from __future__ import annotations

import argparse
import json
import re
from fractions import Fraction
from pathlib import Path

from itembank import ITEMS_TS

TEXT_FIELDS = {"stem", "byHand"}


def ts_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def item_span(src: str, iid: str) -> tuple[int, int]:
    start = src.find(f'id: "{iid}"')
    if start < 0:
        raise KeyError(f"id {iid} not found")
    nxt = src.find("\n    id: \"", start + 5)
    end = src.find("\n];", start) if nxt < 0 else nxt
    return start, end


def to_answers(value) -> str:
    vals = value if isinstance(value, list) else [value]
    parts = []
    for v in vals:
        f = Fraction(str(v).strip())
        parts.append(f"{{ num: {f.numerator}, den: {f.denominator} }}")
    return "answers: [" + ", ".join(parts) + "]"


def apply_one(block: str, fix: dict) -> str:
    field, old, new = fix["field"], fix.get("old"), fix["new"]
    if field in TEXT_FIELDS or field == "choices":
        olds = old if isinstance(old, list) else [old]
        news = new if isinstance(new, list) else [new]
        if len(olds) != len(news):
            raise ValueError("old/new lists differ in length")
        for o, n in zip(olds, news):
            if o == n:
                continue
            eo, en = ts_escape(str(o)), ts_escape(str(n))
            if field == "choices":
                eo, en = f'"{eo}"', f'"{en}"'
            count = block.count(eo)
            if count != 1:
                raise ValueError(f"old text found {count} times in the item: {str(o)[:80]!r}")
            block = block.replace(eo, en)
        return block
    if field == "answerIndex":
        idx = new if isinstance(new, int) else "ABCD".index(str(new).strip().upper()) if str(new).strip().upper() in "ABCD" else int(new)
        block, n = re.subn(r"answerIndex: \d", f"answerIndex: {idx}", block)
        if n != 1:
            raise ValueError("answerIndex not found")
        return block
    if field == "answers":
        block, n = re.subn(r"answers: \[[^\]]*\]", to_answers(new), block)
        if n != 1:
            raise ValueError("answers not found")
        return block
    if field in ("difficulty", "route"):
        block, n = re.subn(rf'{field}: "[a-z-]+"', f'{field}: "{new}"', block)
        if n != 1:
            raise ValueError(f"{field} not found")
        return block
    raise ValueError(f"unsupported field {field}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+", type=Path)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--severity", choices=["error", "minor", "all"], default="all")
    args = ap.parse_args()

    src = ITEMS_TS.read_text(encoding="utf-8")
    applied, skipped, manual = [], [], []
    for path in args.files:
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            f = json.loads(line)
            if args.severity != "all" and f.get("severity") != args.severity:
                continue
            fixes = f.get("fix")
            if not fixes:
                manual.append(f)
                continue
            fixes = fixes if isinstance(fixes, list) else [fixes]
            try:
                s, e = item_span(src, f["id"])
                block = src[s:e]
                for fx in fixes:
                    block = apply_one(block, fx)
                src = src[:s] + block + src[e:]
                applied.append(f)
            except (KeyError, ValueError) as err:
                skipped.append((f, str(err)))

    if not args.dry_run:
        ITEMS_TS.write_text(src, encoding="utf-8")
    print(f"applied {len(applied)}, skipped {len(skipped)}, need manual handling {len(manual)}")
    for f, err in skipped:
        print(f"  SKIP {f['id']} ({f['issue']}, {f.get('severity')}): {err}")
    for f in manual:
        print(f"  MANUAL {f['id']} ({f['issue']}, {f.get('severity')}): {f['detail'][:160]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
