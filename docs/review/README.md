# Blind review of the item bank (2026-10-16)

Purpose: confirm every item stands on its own without Desmos. The SymPy verifier recomputes each key, but from the item author's own reading of the stem, so a misworded stem can pass. Here a reviewer solves each item **blind** (stem and choices only, `python3 web/scripts/blind_dump.py --chunk k --of 8`), then reveals the key, by-hand route and Desmos lines (`--reveal`) and records anything wrong.

Each `chunk-k.jsonl` lists only items with a finding, one JSON object per line:

```json
{"id": "...", "issue": "key-wrong | multiple-correct | ambiguous | missing-info | needs-calculator | byhand-wrong | byhand-incomplete | distractor-weak | difficulty-tag | desmos-route-wrong | other",
 "severity": "error | minor", "detail": "one or two sentences",
 "fix": {"field": "stem | choices | answerIndex | answers | byHand | difficulty | route", "old": "exact current text", "new": "replacement"}}
```

`severity: error` = a student could not get the keyed answer by hand from the stem as written (wrong key, two right answers, missing or contradictory information, an answer that needs a calculator to reach). These block release. `minor` = wording, explanation or tagging improvements.
