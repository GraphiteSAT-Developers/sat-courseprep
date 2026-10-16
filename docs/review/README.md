# Blind review of the item bank (2026-10-16)

Purpose: confirm every item stands on its own without Desmos. The SymPy verifier recomputes each key, but from the item author's own reading of the stem, so a misworded stem can pass. Here a reviewer solves each item **blind** (stem and choices only, `python3 web/scripts/blind_dump.py --chunk k --of 8`), then reveals the key, by-hand route and Desmos lines (`--reveal`) and records anything wrong.

Each `chunk-k.jsonl` lists only items with a finding, one JSON object per line:

```json
{"id": "...", "issue": "key-wrong | multiple-correct | ambiguous | missing-info | needs-calculator | byhand-wrong | byhand-incomplete | distractor-weak | difficulty-tag | desmos-route-wrong | other",
 "severity": "error | minor", "detail": "one or two sentences",
 "fix": {"field": "stem | choices | answerIndex | answers | byHand | difficulty | route | desmos", "old": "exact current text", "new": "replacement"}}
```

`severity: error` = a student could not get the keyed answer by hand from the stem as written (wrong key, two right answers, missing or contradictory information, an answer that needs a calculator to reach). These block release. `minor` = wording, explanation or tagging improvements.

## Result (2026-10-16)

All 1,000 items were solved blind by hand. **Every blind answer matched the key**: no wrong keys anywhere in the bank.

46 findings, all resolved:

| Finding | Errors | Minor | Resolution |
|---|---|---|---|
| Two defensible answers | 1 | | `adv-absolute-no-solution-c`: stem reworded so only one choice is correct |
| Needs a calculator | 2 | 14 | Two regression SPR items now state the least-squares slope, so the prediction follows by hand. Ten items got a paper route (elimination by special-angle bounds, powers by repeated multiplication) added to the explanation. Four trig items (tan 40°, tan 35°, arctan 7/24, sin 14°) need a scientific calculator and have no paper route; kept, since the SAT allows a calculator on every question and they don't need Desmos |
| By-hand explanation wrong | 1 | 7 | Corrected (e.g. a wrong expansion in `adv-grouping-cubic-four-terms`) |
| Explanation incomplete | | 4 | Completed |
| Distractor matches no real mistake | | 10 | Replaced with choices built from real mistakes, and explanations rewritten (`adv-exponent-k`, `adv-rational-divide-simplify`, `alg-inequality-integer-a`, `alg-no-solution-k`, `geo-cylinder-sphere`, `alg-print-shop-rate`, `alg-greatest-integer-inequality`, others) |
| Desmos lines wrong | | 4 | Fixed (variable `r` is reserved for polar graphs in Desmos; three misquoted readouts) |
| Ambiguous wording, difficulty tag, raw LaTeX | | 3 | Fixed |

After fixes: SymPy verifier 1,000 / 1,000 pass; style lint 0 errors.
