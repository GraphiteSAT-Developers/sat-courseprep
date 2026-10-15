# Item generation plan: to 300, then 500

_2026-10-15. Storage decision: items live in `web/content/items.ts` and are exported to `data/items.jsonl` for the AI side (Sonnet tutor, retrieval, evals). Firebase is deferred._

## Targets

The official distribution (`web/content/skills.ts`, from Table A31 of the Assessment Framework) scaled to a 300-item bank. Difficulty leans hard for the 700–800 audience but keeps easy/medium items so a practice module can be simulated faithfully (`docs/framework-design-notes.md` §1).

| Domain | Share | Target | Now | Skills |
|---|---|---|---|---|
| Algebra | 35% | 105 | 11 | 5 |
| Advanced Math | 35% | 105 | 21 | 3 |
| Problem-Solving and Data Analysis | 15% | 45 | 12 | 7 |
| Geometry and Trigonometry | 15% | 45 | 11 | 4 |

Bank-wide ratios to hold on every batch: **MC:SPR ≈ 3:1**, **≈30% in context** (word-problem stems), SPR present in every domain, key position spread evenly across A–D, difficulty mix per domain ≈ 20% easy / 40% medium / 40% hard.

## Per-skill targets (300-item bank)

| Skill | Target | Now |
|---|---|---|
| Linear equations in one variable | 18 | 2 |
| Linear functions | 24 | 2 |
| Linear equations in two variables | 18 | 2 |
| Systems of two linear equations in two variables | 24 | 4 |
| Linear inequalities in one or two variables | 21 | 1 |
| Equivalent expressions | 30 | 6 |
| Nonlinear equations in one variable and systems of equations in two variables | 40 | 10 |
| Nonlinear functions | 35 | 5 |
| Ratios, rates, proportional relationships, and units | 9 | 4 |
| Percentages | 7 | 2 |
| One-variable data: distributions and measures of center and spread | 7 | 3 |
| Two-variable data: models and scatterplots | 7 | 1 |
| Probability and conditional probability | 6 | 1 |
| Inference from sample statistics and margin of error | 5 | 1 |
| Evaluating statistical claims: observational studies and experiments | 4 | 0 |
| Area and volume | 12 | 1 |
| Lines, angles, and triangles | 12 | 5 |
| Right triangles and trigonometry | 12 | 3 |
| Circles | 9 | 2 |

## The cycle for every batch

1. **Brief.** One batch = one domain, 20–30 items, written from the batch brief template in `docs/item-writing.md` (skill counts, difficulty mix, MC/SPR mix, context share, route mix, techniques to exercise).
2. **Write.** A generation agent writes the items into its own file `web/content/batches/<batch-id>.ts` (never into `items.ts` directly, so batches run in parallel), following `docs/item-style-guide.md`, with one SymPy check function per item.
3. **Verify.** `python3 web/scripts/verify_items.py` recomputes every key. Any failure: fix or drop the item.
4. **Lint.** `python3 web/scripts/lint_items.py` applies the College Board style rules. Errors block; warnings are reported in the batch summary.
5. **Merge.** Passing items are appended to `items.ts` (or the batch file is registered in the bank index), the per-skill table above is updated, and the export is regenerated: `npm run items:export`.
6. **Review.** The owner reads the batch review sheet (stems as a student sees them). Keep / fix / drop.

Nothing reaches `data/items.jsonl` without steps 3 and 4 passing.

## Originality rules (non-negotiable)

- No College Board, Khan Academy, or commercial prep items, reworded or otherwise. Generation agents write from skill descriptions and the style guide only.
- Provenance on every item (`author`, `created`, `notes`).
- Bank-level duplicate check in the lint (shared 10-word windows).
- Before release, a near-duplicate check against public items is still owed (see the plan report).

## Order of batches

Fill the largest gaps first: Algebra (four batches), then Advanced Math (three), then PSDA (two), then Geometry/Trig (two). Each batch's brief comes from the table above minus the current count.
