# Technique library (T1–T13)

Source of truth: `web/content/techniques.ts` (data) and `web/content/technique-types.ts` (shape). This page is the human index. Both the course lessons and the AI tutor's retrieval read the same entries, so edit the TypeScript, not this table, and keep the two in step.

Every entry is `verified: false` until the headless verification service has run its `desmosLines` with `COLLEGE_BOARD_OPTIONS` (`web/lib/desmos/config.ts`). Entries also carry `caveats` wherever the research notes marked a claim as contested, third-party-only, or untested in the College Board build. The tutor must not teach a caveated claim as fact.

## Index

| ID | Name | When to use | Route |
|---|---|---|---|
| T1 | Graph both sides, read intersection or zeros | Any one-variable equation: "what is the solution to", "positive solution", "how many solutions" | desmos-primary |
| T2 | Systems by intersection | Two equations in x and y; solution (x, y), x + y, or the solution count | desmos-primary |
| T3 | Sliders for unknown constants in systems | "For what k does the system have no / infinitely many / one solution" (contested) | hand-primary |
| T4 | Sliders, general | A parameter whose sign, size or effect is asked; "for what c does ... have two real solutions" | either |
| T5 | Table regression | Line or curve of best fit, model from a table of points, line through two points | desmos-primary |
| T6 | Tilde trick: find the constants | "For all x, ... = ..., where a, b, c are constants"; equivalent expressions with unknowns | either |
| T7 | Lists and statistics | Mean, median, range, standard deviation of listed data | either |
| T8 | Inequality shading | Systems of inequalities; "which point satisfies"; "which graph represents" | either |
| T9 | Define and evaluate functions | f(3), composition f(g(2)), many evaluations of one function | either |
| T10 | Circles from expanded form | Center and radius from x² + y² + Dx + Ey + F = 0; diameter endpoints (contested) | hand-primary |
| T11 | Exact vs decimal answers | Every SPR item; any long or repeating decimal on screen; reusing a result | either |
| T12 | Trig with angle mode | Any sin / cos / tan evaluation; degrees vs radians | hand-primary |
| T13 | Graph or plug in answer choices | Multiple choice with expression, equation or numeric choices | either |

Shared pre-flight checklist (from the notes): angle mode, zoom to fit, parentheses and signs, `[]` vs `{}`, and whether an exact form is required. Each entry's `preflight` field adds move-specific checks.

## Candidate moves not yet in the library

The report ("Thirteen Desmos moves", `reports/AI Desmos SAT math course plan.md`) and the technique notes list these as useful but **unsourced**: they come from background knowledge of Desmos, not from any fetched page. Test each in `desmos.com/testing/collegeboard/graphing` (and in Bluebook practice) before adding it as T14+.

1. **Vertex / max / min by clicking points of interest.** Clicking a parabola shows gray points (vertex, zeros, y-intercept). Covers vertex-form, maximum-height and zero questions. Also relevant to the headless service: no documented API route exposes these gray points, so a verification query has to recompute the value independently.
2. **Sum and product notation.** `sum` / `prod` give Σ / Π templates; `total([list])` sums a list. Pair with list generation.
3. **List generation with ranges.** `[1...10]` builds a list; useful for "for how many integer values of x" and sequence items.
4. **Absolute-value solution counting.** Graph `y=|x-3|` and `y=k` with a slider on k, then count intersections (a T1/T3 combination). Confirm `|` and `abs()` both work.
5. **Percent syntax.** Whether `%` is accepted in the College Board build (e.g. `20% of 50`). Plain decimal arithmetic is the safer teaching default until confirmed.
6. **Domain restriction.** Append `{0<x<5}` to an expression. This is the "restriction" meaning of `{}` that T7 warns about; the two meanings should be taught together.
7. **Implicit multiplication and auto-subscripting.** `ab` parses as a·b, so multi-letter parameters must be single letters or subscripted (`a_1`); `x1` may auto-subscript but `x_1` is the safe form. Needed by T4, T6 and the LaTeX normalizer.
8. **Exponential growth and decay with sliders.** Graph `y=a(1+r)^x` with sliders, or regress `y_1 \sim a b^{x_1}` on given points (overlaps T4 and T5).
9. **One-click regression button next to a table.** Seen in one ~2024 SuperTutorTV video; unverified in the current Bluebook build (`sat_math_format.md` §4).
10. **Piecewise functions.** `sat_math_format.md` lists piecewise support among the features to confirm in the College Board build before teaching.

Open verification items that affect existing entries (all tracked in each entry's `caveats`): the `{}` vs `[]` statistics pitfall (T7, third-party only), the exact slider bounds/step UI (T3, T4), `midpoint()` / `distance()` and the gray top/bottom points on circles (T10), the fraction toggle on every numeric line (T11), the location of the angle-mode setting (T12), and Log Mode behavior on exact-fit regressions (T5, T6).
