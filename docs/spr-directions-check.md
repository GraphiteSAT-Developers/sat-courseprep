# SPR directions vs. the grader

Source: College Board, *Assessment Framework for the Digital SAT Suite*, Appendix D "Digital SAT Suite Test Directions", Section 2: Math (framework p. 205). Checked against `web/lib/grading/spr.ts` and `web/lib/grading/spr.test.ts`.

## The official directions (quoted)

> For **student-produced response questions**, solve each problem and enter your answer as described below.
>
> - If you find **more than one correct answer**, enter only one answer.
> - You can enter up to 5 characters for a **positive** answer and up to 6 characters (including the negative sign) for a **negative** answer.
> - If your answer is a **fraction** that doesn't fit in the provided space, enter the decimal equivalent.
> - If your answer is a **decimal** that doesn't fit in the provided space, enter it by truncating or rounding at the fourth digit.
> - If your answer is a **mixed number** (such as 3½), enter it as an improper fraction (7/2) or its decimal equivalent (3.5).
> - Don't enter **symbols** such as a percent sign, comma, or dollar sign.

The directions' example table:

| Answer | Acceptable | Unacceptable: will NOT receive credit |
| --- | --- | --- |
| 3.5 | `3.5`, `3.50`, `7/2` | `31/2`, `3 1/2` |
| 2/3 | `2/3`, `.6666`, `.6667`, `0.666`, `0.667` | `0.66`, `.66`, `0.67`, `.67` |
| −1/3 | `-1/3`, `-.3333`, `-0.333` | `-.33`, `-0.33` |

Also relevant from the same page: "Use of a calculator is permitted for all questions." and "For multiple-choice questions ... Each multiple-choice question has a single correct answer."

## Rule-by-rule check

| # | Rule | Grader | Tests | Verdict |
| --- | --- | --- | --- | --- |
| 1 | More than one correct answer: enter only one | `gradeSpr(raw, keys: Rational[])` accepts any key in the list | "accepts any of several keys" | Covered |
| 2 | Up to 5 characters positive, 6 negative including the sign | `MAX_POSITIVE_LENGTH = 5`, `MAX_NEGATIVE_LENGTH = 6`, enforced in `validateSprEntry` on the trimmed entry | "enforces 5 characters for positive and 6 for negative answers" | Covered |
| 3 | Fraction that doesn't fit: enter the decimal | Fractions are compared by exact cross-multiplication, so any fitting fraction (reduced or not, `4/6`) is correct; a too-long fraction is rejected as invalid, and `acceptedEntries` lists the decimal forms | "accepts unreduced fractions and exact decimals"; "lists the official 8/9 forms" | Covered |
| 4 | Decimal that doesn't fit: truncate or round at the fourth digit | `scaledCandidates` computes truncated and half-up rounded values at the entered number of places, accepted only when the entry fills the full width (`entry.length === limit`). Reproduces every row of the example table (`.6666`, `.6667`, `0.666`, `0.667`, `-.3333`, `-0.333`; rejects `.66`, `0.67`, `-.33`) | 8/9 table, 2/3 and −2/3 cases | Covered for repeating decimals; wrong for long terminating decimals (see G1) |
| 5 | Mixed number: enter improper fraction or decimal | Whitespace in the entry is rejected with a message naming `7/2` or `3.5`; `31/2` is a valid entry that simply does not equal 3.5 and is marked incorrect | "rejects mixed numbers, symbols and junk" covers `3 1/2`; `31/2` is not tested | Covered (test gap: add `31/2` → incorrect) |
| 6 | No symbols (%, comma, $) | `/[,%$]/` rejected with a specific reason; anything else non-numeric fails `ENTRY_PATTERN` | `50%`, `$5`, `1,000`, `x`, `--1`, `1/2/3` | Covered |
| 7 | Leading zero is optional (`0.666` and `.666` both appear in the table) | `ENTRY_PATTERN` allows `\d+\.?\d*` and `\.\d+`; `parseEntry` treats a missing whole part as 0 | Implicit in the 8/9 and 2/3 cases | Covered |
| 8 | Trailing zeros allowed (`3.50`) | Decimal compared as exact rational, so `2.50` = `5/2` | "accepts unreduced fractions and exact decimals" | Covered |
| 9 | `-0`, `-0/5` for a zero key | `matchesExactly` skips the sign check when the key is zero, so `-0` is accepted for 0 | Not tested | Covered; Bluebook behaviour for `-0` is not documented, so this is a reasonable choice |

## Gaps and questionable behaviour

Verified by running `gradeSpr` / `acceptedEntries` on the cases below.

- **G1. Terminating decimals that don't fit are rejected (bug).** The directions treat "a decimal that doesn't fit in the provided space" generically and say to truncate or round; they do not distinguish repeating decimals from long terminating ones. `gradeSpr` only runs the truncate/round branch when `terminates(key)` is false, so for key 1/32 = 0.03125 (six characters) it marks `.0312` and `.0313` **incorrect**, and for 15/32 = 0.46875 it marks `.4687` and `.4688` **incorrect**, accepting only the fraction. `acceptedEntries` has the matching problem: `exactDecimal` is used for every terminating key and the result is silently dropped when it exceeds the width, so `acceptedEntries({num:1,den:32})` returns `["1/32"]` with no decimal form. The branch should run whenever the exact decimal does not fit, not only when it never terminates.
- **G2. Multi-digit whole parts are handled but untested.** 100/7 accepts `14.28` and `14.29`; 1234/3 (fraction too long at six characters) accepts `411.3` and `acceptedEntries` returns only `["411.3"]`. Both match the directions' logic. No test covers a repeating decimal whose integer part eats into the width; add one.
- **G3. Mixed-number look-alike `31/2`** is a valid entry graded incorrect for 3.5, as the table requires, but no test asserts it. `3 1/2` is rejected as invalid with a hint to enter `7/2` or `3.5`.
- **G4. Negative zero.** `-0` is graded correct for key 0 (the sign check is skipped for a zero key). Bluebook's behaviour is undocumented; keep it, but add a test so the choice is deliberate.
- **G5. Negative truncation and rounding.** Truncation is toward zero and rounding is half-up on the absolute value, so −2/3 accepts `-.6666`/`-.6667` and −1/3 accepts `-.3333`/`-0.333`, matching the table. Tested; no action.
- **G6. "Rounding at the fourth digit" vs. the examples.** `0.667` rounds at the third decimal yet is listed as acceptable; the grader follows the examples (any full-width truncation or rounding) rather than the literal prose. Correct; no action.
- **G7. "Enter only one answer."** A double entry such as `3,5` or `3 5` is reported as *invalid* (symbols/whitespace), not *incorrect*, which is the right UX. The UI should still display this direction.
- **G8. Non-grading directions.** "Use of a calculator is permitted for all questions", "All variables and expressions represent real numbers", "Figures provided are drawn to scale", "All figures lie in a plane", and the domain-of-f convention are not grader concerns but belong in the practice UI's Math directions panel next to the SPR rules.

## Recommended follow-ups (do not edit spr.ts in this pass)

1. Fix G1: in `gradeSpr`, replace `if (parsed.kind !== "decimal" || terminates(key)) continue;` with "skip only when the key's exact decimal fits in the available width"; run the truncate/round branch otherwise. Mirror the change in `acceptedEntries` so it lists `.0312`, `.0313`, `0.031` for 1/32 instead of only the fraction.
2. Add tests: `31/2` is incorrect for 3.5; 15/32 accepts `.4687`, `.4688`, `0.468`, `0.469`; 100/7 accepts `14.28`, `14.29`; 1234/3 accepts `411.3`; `-0` for key 0.
3. Surface the full Appendix D Math directions (calculator allowed, real numbers, figures to scale) in the UI next to the SPR entry rules.
