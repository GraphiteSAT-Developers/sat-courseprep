"""Compact index of the item bank for generation agents.

Prints one line per item so an agent can see every existing setup for a skill
without reading items.ts in full:

    id | difficulty | format | route | stem (truncated)

usage:
    python3 web/scripts/bank_index.py --skill "Linear functions"
    python3 web/scripts/bank_index.py --domain algebra
    python3 web/scripts/bank_index.py --counts        # items per skill
"""

from __future__ import annotations

import argparse
import re
from collections import Counter

from itembank import load_items

def short(text: str, n: int) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= n else text[: n - 1] + "…"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--skill")
    ap.add_argument("--domain")
    ap.add_argument("--width", type=int, default=160)
    ap.add_argument("--counts", action="store_true")
    args = ap.parse_args()
    items = load_items()

    if args.counts:
        c = Counter(i["skill"] for i in items)
        for skill, n in sorted(c.items(), key=lambda kv: (-kv[1], kv[0])):
            print(f"{n:4}  {skill}")
        print(f"{len(items):4}  total")
        return 0

    for it in items:
        if args.skill and it["skill"] != args.skill:
            continue
        if args.domain and it["domain"] != args.domain:
            continue
        print(f"{it['id']} | {it['difficulty']} | {it['format']} | {it['route']} | {short(it['stem'], args.width)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
