# data/ — the feed for the AI side

Generated files. The AI collaborator (the Sonnet tutor behind `web/lib/tutor/`, technique retrieval, and the evals) reads from here; the site itself reads `web/content/items.ts` directly. Do not edit these files by hand: regenerate them.

| File | What | Source |
|---|---|---|
| `items.jsonl` | One item per line, provider-neutral JSON | `web/content/items.ts` |
| `skills.json` | Domain titles, question distribution, and the official skill taxonomy with testing points | `web/content/skills.ts` |
| `techniques.json` | The Desmos technique library (T1–T13) with by-hand routes, pitfalls, caveats | `web/content/techniques.ts` |

## Item line shape

`id, domain, skill, difficulty, format ("mc" | "spr"), stem, techniques, route, desmos ({lines, read, verified} or null), byHand, provenance ({author, created, notes?}), status`, plus `choices` and `answerIndex` for MC or `answers` (exact rationals `{num, den}`) for SPR.

`status` is `"verified"` when `desmos.verified` is true (the headless Desmos service has run the lines) and `"draft"` otherwise. The tutor must never show unverified Desmos steps to a student; `byHand` and the keys are still usable. Math in `stem` and `choices` is inline LaTeX between `$...$`.

## Regenerate

```bash
cd web
npm run items:export     # writes data/items.jsonl, skills.json, techniques.json
```

Run it after any change to `web/content/items.ts`, `skills.ts`, or `techniques.ts`, and commit the result alongside the content change. `web/lib/export/items.test.ts` checks the line count and fields; `python3 web/scripts/verify_items.py` checks the keys.

Every item is original (see `docs/item-writing.md`). Nothing in this directory may contain College Board questions.
