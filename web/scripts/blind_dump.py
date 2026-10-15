"""Print a slice of the bank for blind review: stem and choices only, no key.

The review agent solves each item by hand from this output, then runs the same
command with --reveal to compare against the key, the by-hand route and the
Desmos lines.

usage:
    python3 web/scripts/blind_dump.py --chunk 3 --of 8            # blind
    python3 web/scripts/blind_dump.py --chunk 3 --of 8 --reveal   # keys + routes
    python3 web/scripts/blind_dump.py --ids alg-foo,adv-bar --reveal

Items are sorted by skill, then id, so each chunk covers one or two skills.
"""

from __future__ import annotations

import argparse
from fractions import Fraction

from itembank import load_items


def fmt_answer(a: Fraction) -> str:
    return str(a.numerator) if a.denominator == 1 else f"{a.numerator}/{a.denominator}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--chunk", type=int)
    ap.add_argument("--of", type=int, default=8)
    ap.add_argument("--ids")
    ap.add_argument("--reveal", action="store_true")
    args = ap.parse_args()

    items = sorted(load_items(), key=lambda i: (i["skill"], i["id"]))
    if args.ids:
        wanted = set(args.ids.split(","))
        items = [i for i in items if i["id"] in wanted]
    elif args.chunk is not None:
        size = -(-len(items) // args.of)
        items = items[(args.chunk - 1) * size : args.chunk * size]

    for it in items:
        print(f"### {it['id']}  [{it['skill']} | {it['difficulty']} | {it['format']}]")
        print(it["stem"])
        if it["format"] == "mc":
            for j, c in enumerate(it["choices"]):
                print(f"  {'ABCD'[j]}) {c}")
        else:
            print("  (student-produced response)")
        if args.reveal:
            if it["format"] == "mc":
                print(f"KEY: {'ABCD'[it['answerIndex']]}")
            else:
                print("KEY: " + " or ".join(fmt_answer(a) for a in it["answers"]))
            print(f"BY HAND: {it['byHand']}")
            if it.get("desmos"):
                print("DESMOS: " + " | ".join(it["desmos"]["lines"]) + f"  -> {it['desmos']['read']}")
        print()
    print(f"# {len(items)} items")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
