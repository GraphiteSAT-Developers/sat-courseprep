# Generation agent instructions (phase 2)

Every generation agent follows this file. Its own prompt supplies only the
**batch parameters** (batch id, skill(s) and counts, difficulty mix, format
mix, context share, route mix, testing-point focus).

## Read first

1. `docs/item-writing.md`: the checklist and every lint rule id.
2. `docs/item-style-guide.md`: the College Board-derived style rules.
3. `web/content/types.ts`, `web/content/skills.ts` (the official testing points for your skill), `web/content/techniques.ts`.
4. **Existing items for your skill:** `python3 web/scripts/bank_index.py --skill "<exact skill name>"` (one line per item). Do not reuse any setup, context or question frame listed there. Do not read all of `web/content/items.ts`; open it only to copy the entry style from two or three items of your skill (`grep -n "<id>" web/content/items.ts` then read ~30 lines).
5. `web/scripts/verify_items.py`, only the first ~70 lines (helpers `latex_to_sympy`, `latex_to_sympy_ext`, `_split_equation`) and two or three check functions for your domain as patterns.

## Rules that apply to every batch

- **Original only.** Write from the official testing points and the style guide. No College Board, Khan Academy or commercial prep items, reworded or otherwise. Own numbers, own contexts.
- **Spread across testing points.** Cover every testing point listed for your skill in `skills.ts` before repeating one; no more than 3 items on the same underlying setup.
- **Difficulty** must be honest: easy = one step; medium = two steps or one trap; hard = a chain, a structural insight, or a constant to reason about.
- **Constants** in the trailing clause form: "..., where k is a constant."
- **Units and rounding** go inside the question sentence ("What is the height, in meters, ... to the nearest tenth?").
- **Choices** are parallel in form and monotonic (ascending by default). Every MC distractor reflects a named mistake, and `byHand` names each distractor's mistake.
- **Key positions** spread across A–D, none above 40% of the batch's MC items.
- **SPR keys** fit Bluebook (5 characters positive, 6 negative, as a fraction or a full-width decimal); use the `Rational` type.
- **Context stems** stay ≤ 50 standardized words (characters ÷ 6). Contexts must be new to the bank.
- **Dollar amounts** are written as "23.00 dollars" in prose and ", in dollars," in the question (MathText uses `$` for math).
- **No figures.** Every item is fully specified in words; tables are described inline in one consistent sentence form.
- **Desmos:** `desmos.lines` are lines a student types in the College Board calculator; `verified: false`. Hand-primary items say honestly in `desmos.read` that Desmos is slower and how to use it as a check, or omit `desmos` with `techniques: []` for pure reasoning items.
- **Provenance:** `{ author: "claude-agent", created: "<today>", notes: "batch <id>; key verified with SymPy" }`.
- **Ids** are prefixed by domain (`alg-`, `adv-`, `psda-`, `geo-`), descriptive, and must not exist in the bank (check with `grep -c '"<id>"' web/content/items.ts`).

## Output (only these two files)

1. `web/content/batches/<batch-id>.ts`:
   ```ts
   import type { Item } from "../types";
   export const batch: Item[] = [
     ...entries in exactly the items.ts entry style...
   ];
   ```
2. `web/scripts/checks_<batch_id_with_underscores>.py`: `CHECKS = {item_id: fn}` in the verify_items.py conventions (a function returns the exact SymPy key, or a `(choices, idx)` callable for non-numeric choices). Header: `sys.path.insert(0, ...)` and `from verify_items import ...` (these lines are stripped when the batch is merged); keep the sympy imports and symbol definitions; prefix every helper with a batch-unique prefix (e.g. `_b7lf_`) so it can't collide with helpers already in verify_items.py.

Do not edit `items.ts`, `verify_items.py`, `lint_items.py` or any other shared file. Do not commit.

## Self-check (required before reporting)

Use a **private** scratchpad subfolder named after your batch id (other agents share the scratchpad).

1. Build a temp bank: a copy of `web/content/items.ts` with your entries inserted just before the first line that is exactly `];`.
2. `python3 web/scripts/verify_items.py --items <tmp> --checks web/scripts/checks_<...>.py --only-extra` → every item PASS.
3. Plant one wrong key in a second copy and confirm it FAILs.
4. `python3 web/scripts/lint_items.py --items <tmp>` → 0 errors. Fix every error in your batch. Fix every warning on your items except PR04 where the linter can't parse nested `\frac`/`\sqrt` choices; list any left with a reason.
5. `cd web && npm run typecheck` passes.
6. Re-read every stem as a student: which root or coordinate, exact vs decimal, units, degrees vs radians, domain restrictions, extraneous roots.

## Report

Counts by skill / difficulty / format / route / context, key positions, the testing points covered, lint warnings left standing, and anything you were unsure about. Keep it short.
