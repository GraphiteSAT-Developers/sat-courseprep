# Training the AI tutor on Topline (our own graphing calculator)

_Researched 2026-10-16. Topline is the browser calculator in `topline/`, built so the course doesn't pay for the Desmos API._

## Method

- **Topline was tested directly.** Its math engine is the code between `// == ENGINE START ==` and `// == ENGINE END ==` in `topline/index.html`. It was run in Node on about 120 inputs written the way Desmos stores them, covering techniques T1–T13 from `desmos_techniques.md`. Point-of-interest behaviour was checked in headless Chromium with screenshots.
- **The checks are now a test script:** `node topline/tests/engine-check.js`, 27 cases.
- **Desmos claims are mostly unconfirmed.** desmos.com and help.desmos.com were blocked from this environment again. Any claim below about what Desmos or Bluebook does comes from background knowledge unless a source is given. Section 7 lists what to check by hand.

## 1. What changes when Topline replaces Desmos

The earlier plan (`docs/desmos-integration.md`, `reports/AI Desmos SAT math course plan.md`) assumed the official Desmos API in two places: the student's calculator and the AI's headless checking calculator. Topline changes four things.

1. **The checking calculator now costs nothing.** Topline's engine is about 1,400 lines of plain JavaScript with no browser dependencies. It runs in Node in milliseconds.
   - The Solver no longer needs Playwright, a headless browser, or a Desmos licence to execute and check its steps.
   - `topline/tests/engine-check.js` already shows how to load it, in about 5 lines.
2. **Nothing confirms Bluebook any more.** Students practise in Topline but sit the test in Bluebook's Desmos. A step that works in Topline isn't automatically valid in Desmos, and the reverse is also true.
   - Every keystroke the AI teaches has to come from a **shared subset** that works in both (rules in section 4).
   - The technique library needs a one-time human check in the College Board practice calculator (`desmos.com/testing/collegeboard/graphing`).
3. **The tutor can't read the student's calculator yet.** Desmos offered `getState`, `observeEvent('change')` and `expressionAnalysis`. Topline has no programmatic interface.
   - Today its state exists only as LaTeX lines in `localStorage['plotline-state-v1']`, which held the test input in this pass.
   - Section 6 specifies the interface the tutor needs.
4. **Intersection and extremum markers are weaker than in Desmos.** Section 2 has the details. Many SAT routines say "click the intersection", so this matters for teaching.

## 2. Compatibility with the SAT Desmos techniques

✅ means it works the same way as the Desmos routine. ⚠️ means it works with a caveat the AI must know. ❌ means it doesn't work in Topline.

| Technique | Topline result | Detail |
|---|---|---|
| T1 Graph both sides and intersect | ⚠️ | Correct graphs. Intersection markers appear only between two `y = …` curves (see below). |
| T2 Systems | ⚠️ | `3x+2y=12` and `x^2+y^2=25` graph correctly but get **no markers at all**: no intercepts and no intersections. Rewrite lines as `y = …` to get a clickable intersection. |
| T3/T4 Sliders | ✅ | An undefined letter shows an "add slider: k" button. The new slider starts at 1 with a range of −10 to 10. |
| T5 Regression | ✅ | Linear, quadratic, exponential (`y_1\sim ab^{x_1}`) and vertex form all fit exactly. Shows R², RMSE and n. Vertex form was wrong before this pass (section 3). |
| T6 Tilde trick | ✅ | `(5x_1-17)(4x_1-c)\sim ax_1^2+bx_1+119` with `x_1=[2,3,4]` gives c = 7, a = 20, b = −103, matching the published example. |
| T7 List statistics | ✅ | `mean`, `median`, `stdev` (sample), `stdevp`, `quartile`, `total`, `length`, `min`, `max` are all correct. `{4,7}` used as a list fails, as in Desmos, but the error says *"The 'otherwise' value has to come last"*. |
| T8 Inequalities | ✅ | Shading works, with dashed borders for `<` and `>`. `<=` and `\le` are both accepted. |
| T9 Functions | ✅ | `f(3)`, `f(f(1))`, composition and `f'(x)` all work. |
| T10 Circles | ⚠️ / ❌ | Expanded-form circles graph, but you **can't click the top and bottom points** because implicit curves get no markers. `midpoint(A,B)` and `distance(A,B)` **don't exist** (the error messages are misleading, see below). `A.x` and `A.y` do work. |
| T11 Exact answers | ❌ | No fraction toggle. Results show 6 significant figures (`2/3` shows as `0.666667`). |
| T12 Trig | ⚠️ | Radians by default, with Degrees in Settings, like Desmos. Typing `°` or `30^{\circ}` is an error. |
| T13 Plug in answer choices | ✅ | Define `f`, then evaluate `f(choice)` on each line. |

### Point-of-interest rules (from the code and confirmed on screen)

- Markers appear only for the **selected** row, and only when that row is a `y = f(x)` curve, a function of `x`, or a regression.
- **Intersections** are found only against other `y = …` curves. They are missed against standard-form lines, circles, `x = 3`, and inequalities.
- **Tangent points are missed.** For example, `y=x^2` and `y=2x-1` touch at (1, 1) and get no marker, because the search looks for a sign change. A double root such as `y=(x-2)^2` gets a "Local minimum" marker, not an x-intercept marker.
- Only points **inside the current view** are found. "Zoom out before concluding no solution" applies even more than in Desmos.

### Other differences found

| Input | Topline | Desmos (unverified unless cited) |
|---|---|---|
| `20\% of 50` | Error: `\% isn't supported here` | Supported: typing `%` produces "% of" ([Desmos blog](https://blog.desmos.com/articles/friday-fave-for-september-15)) |
| `x1=[1,2]` (no underscore) | **Silently** read as x·1 and graphed as an implicit curve | Students commonly type it, so check whether Desmos auto-subscripts |
| `L[1...2]` (list slice) | Error: "A closing ] is missing" | Supported in Desmos |
| `midpoint(A,B)` | Error: "Write integrals as int(t, 0, x, t^2)" because the name contains `int` | Supported, per third-party SAT guides |
| `distance(A,B)` | Error: "d, i, s, c aren't defined yet" | Supported, per third-party SAT guides |
| `area=3` | Error: "a, r aren't defined yet". Multi-letter names are split into single letters. | Same in Desmos: use one letter or a subscript |
| `\log_{2}(8)`, `\log_2 8` | 3 | Same |
| `\sum_{n=1}^{10}n`, `[1...10]`, `3!`, `nCr(5,2)`, `\sqrt[3]{27}`, `\left|-3\right|` | All correct | Same |
| A regression with fewer points than unknowns | Returns some fit with **no warning** (1 point with `mx_1+b` gives m = 1.5, b = 2, R² undefined) | Unknown |

## 3. Bug fixed in this pass

**`a(x-h)^2` was computed as `(a(x-h))^2`** when `a` was a variable such as a slider or regression parameter:

- `a=2` then `a(3)^2` gave 36, not 18.
- `y=a(x-2)^2+1` graphed the wrong parabola.
- The vertex-form regression `y_1\sim a(x_1-h)^2+k` returned a = √2 instead of 2.

This is the standard vertex form on the SAT, so it would have broken T3 and T5 lessons without any visible error.

- **Cause:** the parser reads `a(…)` as a possible function call before it knows whether `a` is a function.
- **Fix:** when `a` turns out not to be a function, the compiler moves the exponent onto the parentheses (`topline/index.html`, `compile`, case `'b'`).
- **Regression coverage:** `engine-check.js` has three cases for it. All three fail on the old code and pass on the new code. All 27 cases pass.

## 4. Rules for the AI (system-prompt block)

These rules go into the cached system prompt for both the Solver and the Tutor. Each one comes from a result above.

```
CALCULATOR RULES. Students practise in Topline and take the SAT in Bluebook's Desmos.
Teach only keystrokes that work in both.

Syntax
1. Always use subscripts with an underscore: x_1, y_1, L_1. Never x1.
2. Lists use square brackets: [3,7,8]. Curly braces {} are only for restrictions
   like y=x^2{0<x<5} or piecewise definitions.
3. Use one-letter names (a, b, k, h) or subscripted names (v_0). Never multi-letter
   names like area or cost: they are read as products of letters.
4. Write percents as decimals (0.2*50), not "20% of 50".
5. No degree symbol. For degree problems, tell the student to switch to Degrees
   in Settings first, then type sin(30).
6. Write midpoint and distance with formulas: ((x_a+x_b)/2, (y_a+y_b)/2) and
   sqrt((x_b-x_a)^2+(y_b-y_a)^2). Not midpoint() or distance().
7. Don't slice lists with L[1...3]. Use L[n] for one item or a filter like L[L>5].
8. Use only features Bluebook has: graphing, sliders, tables, regressions, lists,
   statistics, sums. Don't teach Topline extras such as ttest, distributions,
   histograms or matrices for SAT work.

Clicking points
9. To get a clickable intersection, both curves must be written as y = ...
   Convert standard-form lines (3x+2y=12 -> y=(12-3x)/2) before telling a
   student to click an intersection.
10. Topline does not mark intersections with circles, x = c lines or inequalities.
    For those, solve with a regression (tilde) or algebra instead of clicking.
11. Tangent points (exactly one solution) are not marked. Confirm tangency by
    substitution or the discriminant, not by looking for a dot.
12. Only points on screen are marked. Tell the student to zoom out before
    concluding there is no solution.

Answers
13. Topline shows 6 significant figures and has no fraction toggle. For
    free-response answers, give the exact form from algebra. If a decimal is
    entered, it must follow SAT rules (use every space: .6666, .6667, 0.666 or 0.667, not 0.67).
14. A regression needs at least as many data points as unknown letters. Topline
    does not warn when there are too few, so count them first.
15. Never tell a student to retype a rounded regression value. Use the
    parameter name (m, b, a) in later lines.
```

## 5. How to train the AI on Topline

This keeps the no-fine-tuning plan from the report (Gemini 3.x has no tuning). Topline replaces headless Desmos as the executor.

1. **Solver tool: `topline_run`.**
   - **Input:** `{lines: string[], degrees: bool}`.
   - **Output per line:** kind (value, function, graph, regression, error), value, error message and regression parameters.
   - **Implementation:** wrap `analyzeAll` the same way `engine-check.js` loads it. It runs in the API server's own process, with no browser and no licence.
   - **Answer check:** each answer must also agree with SymPy, so a Topline bug can't certify a wrong answer. This pass found one such bug (section 3).
2. **Move point-of-interest finding into the engine.**
   - `findPOIs` sits in the user-interface code and depends on the visible screen area.
   - Move it into the engine as `pois(rowA, rowB, xmin, xmax)` so the Solver can confirm that "click the intersection" will show the point the trace claims.
   - Add tangency and implicit-curve detection at the same time (section 6).
3. **Technique library entries record both calculators.**

   ```yaml
   id: T6-tilde-coefficients
   when: "find constants a, b, c that make two expressions equivalent"
   lines: ["x_1=[2,3,4]", "(5x_1-17)(4x_1-c)\\sim ax_1^2+bx_1+119"]
   read: "c, a, b from the regression output"
   topline: verified        # set automatically by engine-check style test
   bluebook: verified-2026-10-xx-by-<name>   # human check in the College Board practice calculator
   pitfalls: ["x_1 list must have at least as many values as unknowns", "don't retype rounded values"]
   by_hand: "expand, then match coefficients"
   ```

   An entry is used only when both fields say verified.
4. **Normalizer.** Rewrite or reject common model output before it reaches the student:
   - `x1` → `x_1`
   - `% of` → a decimal
   - `midpoint(` / `distance(` → formulas
   - `°` → a degree-mode note
   - `{…}` used as a list → `[…]`
   - multi-letter names → single letters
   - stray `$` around expressions
   - `y=` written where a regression needs `~`

   Log every rewrite so the error taxonomy comes from real model behaviour.
5. **Error feedback loop.** Topline's error messages are short and specific, for example "b, c aren't defined yet", "A closing ] is missing", "Regressions use list data, like y_1 ~ m x_1 + b", and "y_1 is already defined". Feed them back to the model for up to N retries, as the report planned for `expressionAnalysis`. Two messages mislead and should be fixed in Topline (section 6).
6. **Rejection-sampled worked examples.** Keep a sampled solution only if:
   - every line runs in Topline without an error;
   - every line passes the shared-subset lint (section 4);
   - the final answer matches the key and SymPy;
   - the solution uses the fewest lines a student could retype.

   The survivors become few-shot examples, retrieval entries, and a future fine-tuning dataset.
7. **Add a parity layer to the evals.**
   - Grow `engine-check.js` into a regression suite that runs on every Topline change.
   - Keep a list of Bluebook checks done by hand, one per technique entry.
   - Track the **share of taught keystrokes inside the shared subset**, with a launch target of 100%.

## 6. Topline changes needed before the AI can rely on it (priority order)

1. **Tutor interface.** Expose `window.topline = { getState(), setState(), onChange(cb), analyze() }`, plus a `postMessage` bridge if the calculator sits in an iframe next to the question.
   - `analyze()` returns per-line values and errors.
   - This replaces the Desmos `getState`, `observeEvent` and `expressionAnalysis` calls the integration doc relies on.
2. **Better points of interest:**
   - intersections with implicit curves (standard-form lines and circles)
   - top, bottom, left and right points of circles
   - tangent intersections and double roots marked as x-intercepts
   - an engine-level function the Solver can call
3. **`midpoint` and `distance`**, so circle and coordinate-geometry routines from SAT guides work. Also fix the misleading errors: `midpoint` is caught by the integral hint, and `distance` is split into letters.
4. **`%` as "% of"**, matching Desmos.
5. **`x1`:** turn it into `x_1` automatically, or show an error, instead of silently reading it as x·1.
6. **List slicing** `L[1...3]`.
7. **Fraction display** for rational results, needed for exact free-response answers.
8. **A clearer error for `{4,7}` used as a list**, for example "Use [ ] for lists; { } is for conditions."
9. **A warning when a regression has fewer points than unknowns.**

## 7. Still to verify by hand in the College Board practice calculator

- Whether `x1` is auto-subscripted in Desmos.
- Whether `distance()` and `midpoint()` exist in the College Board build.
- Whether `L[1...3]` works in the College Board build.
- How Desmos marks tangent intersections and intersections of implicit curves. The AI rules in section 4 assume Desmos does mark them, so the advice to rewrite as `y = …` is only a Topline workaround.
- How Desmos handles a regression with too few points.
- The degree-symbol behaviour.
- Rounding and display precision, so the AI's decimal-entry advice matches what students see in Bluebook.
- Each technique-library entry, run once in `desmos.com/testing/collegeboard/graphing`.

## Sources

- Topline source and tests in this repository: `topline/index.html`, `topline/tests/engine-check.js`.
- Desmos "% of" design note: [Desmos blog, Friday Fave for September 15](https://blog.desmos.com/articles/friday-fave-for-september-15).
- Technique list and published worked examples: `research_notes/AI Desmos SAT math course plan/desmos_techniques.md` and its sources.
- Training approach (Solver/Tutor split, rejection sampling, evals): `research_notes/AI Desmos SAT math course plan/gemini_desmos_ai.md`.
