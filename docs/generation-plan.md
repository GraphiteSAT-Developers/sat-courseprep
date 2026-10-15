# Item generation plan: to 1,000

_2026-10-15, bank at 301 after batch 5 (first milestone reached). Storage decision: items live in `web/content/items.ts` and are exported to `data/items.jsonl` for the AI side (Sonnet tutor, retrieval, evals). Firebase is deferred._

## Targets

The official distribution (`web/content/skills.ts`, from Table A31 of the Assessment Framework) scaled to a 300-item bank. Difficulty leans hard for the 700–800 audience but keeps easy/medium items so a practice module can be simulated faithfully (`docs/framework-design-notes.md` §1).

| Domain | Share | Target | Now | Skills |
|---|---|---|---|---|
| Algebra | 35% | 105 | 105 | 5 |
| Advanced Math | 35% | 105 | 105 | 3 |
| Problem-Solving and Data Analysis | 15% | 45 | 46 | 7 |
| Geometry and Trigonometry | 15% | 45 | 45 | 4 |

Bank-wide ratios to hold on every batch: **MC:SPR ≈ 3:1**, **≈30% in context** (word-problem stems), SPR present in every domain, key position spread evenly across A–D, difficulty mix per domain ≈ 20% easy / 40% medium / 40% hard.

## Per-skill targets (300-item bank)

| Skill | Target | Now |
|---|---|---|
| Linear equations in one variable | 18 | 18 |
| Linear functions | 24 | 24 |
| Linear equations in two variables | 18 | 18 |
| Systems of two linear equations in two variables | 24 | 23 |
| Linear inequalities in one or two variables | 21 | 22 |
| Equivalent expressions | 30 | 30 |
| Nonlinear equations in one variable and systems of equations in two variables | 40 | 40 |
| Nonlinear functions | 35 | 35 |
| Ratios, rates, proportional relationships, and units | 9 | 10 |
| Percentages | 7 | 7 |
| One-variable data: distributions and measures of center and spread | 7 | 8 |
| Two-variable data: models and scatterplots | 7 | 7 |
| Probability and conditional probability | 6 | 6 |
| Inference from sample statistics and margin of error | 5 | 4 |
| Evaluating statistical claims: observational studies and experiments | 4 | 4 |
| Area and volume | 12 | 10 |
| Lines, angles, and triangles | 12 | 13 |
| Right triangles and trigonometry | 12 | 12 |
| Circles | 9 | 10 |

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

## Phase 2: 301 → 1,000 (started 2026-10-15)

Same guidelines and ratios, scaled to a 1,000-item bank. Per-skill targets are the 300-item targets × 10/3.

| Skill | Target (1,000) | At 301 | To write | Batches |
|---|---|---|---|---|
| Linear equations in one variable | 60 | 18 | 42 | 2 × 21 |
| Linear functions | 80 | 24 | 56 | 2 × 28 |
| Linear equations in two variables | 60 | 18 | 42 | 2 × 21 |
| Systems of two linear equations in two variables | 80 | 23 | 57 | 29 + 28 |
| Linear inequalities in one or two variables | 70 | 22 | 48 | 2 × 24 |
| Equivalent expressions | 100 | 30 | 70 | 24 + 23 + 23 |
| Nonlinear equations in one variable and systems of equations in two variables | 133 | 40 | 93 | 3 × 31 |
| Nonlinear functions | 117 | 35 | 82 | 28 + 27 + 27 |
| Ratios, rates, proportional relationships, and units | 30 | 10 | 20 | psda-A |
| Percentages | 23 | 7 | 16 | psda-A 6, psda-B 10 |
| One-variable data: distributions and measures of center and spread | 23 | 8 | 15 | psda-B |
| Two-variable data: models and scatterplots | 23 | 7 | 16 | psda-C |
| Probability and conditional probability | 20 | 6 | 14 | psda-C 10, psda-D 4 |
| Inference from sample statistics and margin of error | 17 | 4 | 13 | psda-D |
| Evaluating statistical claims: observational studies and experiments | 14 | 4 | 10 | psda-D |
| Area and volume | 40 | 10 | 30 | geo-A |
| Lines, angles, and triangles | 40 | 13 | 27 | geo-B |
| Right triangles and trigonometry | 40 | 12 | 28 | geo-C |
| Circles | 30 | 10 | 20 | geo-D |
| **Total** | **1,000** | **301** | **699** | **27 batches** |

Per batch: difficulty ≈ 20/40/40, MC:SPR ≈ 3:1, route ≈ one third each (geometry and PSDA lean hand-primary), context ≈ 30% (PSDA ≈ 80%).

Scale changes from phase 1:
- Batches are per skill (not per domain), so each agent goes deep on one skill's testing points.
- Agents read `python3 web/scripts/bank_index.py --skill "<name>"` (one line per existing item) instead of the whole bank, to avoid setups already used.
- Two batches of the same skill never run in the same wave; the second one sees the first's items in the index.
- Waves of 5 agents, merged and committed as each finishes (`merge_batch.py`, verify, lint, export).
