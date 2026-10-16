# Training the AI tutor on Topline (our own graphing calculator)

_Researched 2026-10-16. Topline is the browser calculator in `topline/`, built so the course doesn't pay for the Desmos API. Later the same day Topline was changed to close the gaps found here (section 3). Tables and rules below describe the updated Topline._

## Method

- **Topline was tested directly.** Its math engine is the code between `// == ENGINE START ==` and `// == ENGINE END ==` in `topline/index.html`. It was run in Node on about 120 inputs written the way Desmos stores them, covering techniques T1–T13 from `desmos_techniques.md`. Point-of-interest behaviour was checked in headless Chromium with screenshots.
- **The checks are now a test script:** `node topline/tests/engine-check.js`, 38 cases.
- **Desmos claims are mostly unconfirmed.** desmos.com and help.desmos.com were blocked from this environment again. Any claim below about what Desmos or Bluebook does comes from background knowledge unless a source is given. Section 7 lists what to check by hand.

## 1. What changes when Topline replaces Desmos

The earlier plan (`docs/desmos-integration.md`, `reports/AI Desmos SAT math course plan.md`) assumed the official Desmos API in two places: the student's calculator and the AI's headless checking calculator. Topline changes four things.

1. **The checking calculator now costs nothing.** Topline's engine is about 1,400 lines of plain JavaScript with no browser dependencies. It runs in Node in milliseconds.
   - The Solver no longer needs Playwright, a headless browser, or a Desmos licence to execute and check its steps.
   - `topline/tests/engine-check.js` already shows how to load it, in about 5 lines.
2. **Nothing confirms Bluebook any more.** Students practise in Topline but sit the test in Bluebook's Desmos. A step that works in Topline isn't automatically valid in Desmos, and the reverse is also true.
   - Every keystroke the AI teaches has to come from a **shared subset** that works in both (rules in section 4).
   - The technique library needs a one-time human check in the College Board practice calculator (`desmos.com/testing/collegeboard/graphing`).
3. **The tutor couldn't read the student's calculator at first.** Desmos offered `getState`, `observeEvent('change')` and `expressionAnalysis`. Topline now has its own interface (section 6, item 1).
   - Today its state exists only as LaTeX lines in `localStorage['plotline-state-v1']`, which held the test input in this pass.
   - Section 6 specifies the interface the tutor needs.
4. **Intersection and extremum markers** were weaker than in Desmos at first. They are now fixed (section 3). Many SAT routines say "click the intersection", so this mattered for teaching.

## 2. Compatibility with the SAT Desmos techniques

✅ means it works the same way as the Desmos routine. ⚠️ means it works with a caveat the AI must know. ❌ means it doesn't work in Topline.

| Technique | Topline result | Detail |
|---|---|---|
| T1 Graph both sides and intersect | ✅ | Intersections are marked between any two equality curves: `y = …`, `x = …`, standard-form lines and circles. Tangent points are marked too. |
| T2 Systems | ✅ | `3x+2y=12` gets its intercepts and intersections marked. There's no need to rewrite it as `y = …`. |
| T3/T4 Sliders | ✅ | An undefined letter shows an "add slider: k" button. The new slider starts at 1 with a range of −10 to 10. |
| T5 Regression | ✅ | Linear, quadratic, exponential (`y_1\sim ab^{x_1}`), vertex form and `p\% of 20\sim9` all fit exactly. Shows R², RMSE and n. Warns when there are fewer points than unknowns. |
| T6 Tilde trick | ✅ | `(5x_1-17)(4x_1-c)\sim ax_1^2+bx_1+119` with `x_1=[2,3,4]` gives c = 7, a = 20, b = −103, matching the published example. |
| T7 List statistics | ✅ | `mean`, `median`, `stdev` (sample), `stdevp`, `quartile`, `total`, `length`, `min`, `max` are all correct. `{4,7}` used as a list fails, as in Desmos, with the error "Lists use square brackets…". |
| T8 Inequalities | ✅ | Shading works, with dashed borders for `<` and `>`. `<=` and `\le` are both accepted. |
| T9 Functions | ✅ | `f(3)`, `f(f(1))`, composition and `f'(x)` all work. |
| T10 Circles | ✅ | Click a circle to see its top and bottom points (center = their midpoint), intercepts and intersections. Like Desmos, left and right points aren't marked. `midpoint(A,B)`, `distance(A,B)`, `A.x` and `A.y` work. |
| T11 Exact answers | ✅ | Results that are exact fractions show an **a/b** toggle, as in Desmos (5.125 ↔ 41/8). Decimals show 6 significant figures. |
| T12 Trig | ✅ | Radians by default, with Degrees in Settings. `30°` and `30^{\circ}` are accepted and convert correctly in either mode. |
| T13 Plug in answer choices | ✅ | Define `f`, then evaluate `f(choice)` on each line. |

### Point-of-interest rules (from the code and confirmed on screen)

- Markers appear for the **selected** row. Clicking any curve selects it, including standard-form lines and circles.
- **Explicit curves** (`y = …`, `x = …`, functions of x, regressions) get:
  - intercepts
  - local maxima and minima (leftmost and rightmost points for `x = …`)
  - intersections with every other equality curve
- **Implicit curves** (`3x+2y=12`, circles, other conics) get:
  - intercepts
  - highest and lowest points (not leftmost and rightmost, matching user reports of Desmos)
  - intersections with every other equality curve
- **Touching points count.** A tangent line, or a double root such as `y=(x-2)^2` at (2, 0), is marked.
- Only points **inside the current view** are found, as in Desmos. "Zoom out before concluding no solution" still applies.
- Inequalities get no markers.

### Other inputs checked

| Input | Topline now | Desmos (unverified unless cited) |
|---|---|---|
| `20\% of 50`, `15%` | 10, 0.15. Typing `%` then `of` displays "% of". | Supported: typing `%` produces "% of" ([Desmos blog](https://blog.desmos.com/articles/friday-fave-for-september-15)) |
| `x1=[1,2]` | Read as `x_1`. The editor turns a digit typed after a lone letter into a subscript. | Desmos auto-subscripts the same way (to confirm) |
| `L[2...3]`, `L[2...]` | List slices | Supported in Desmos |
| `area=3` | Error: "a, r aren't defined yet". Multi-letter names are split into single letters. | Same in Desmos: use one letter or a subscript |
| `\log_{2}(8)`, `\log_2 8` | 3 | Same |
| `\sum_{n=1}^{10}n`, `[1...10]`, `3!`, `nCr(5,2)`, `\sqrt[3]{27}`, `\left|-3\right|` | All correct | Same |

## 3. Changes made to Topline

**Bug: `a(x-h)^2` was computed as `(a(x-h))^2`** when `a` was a variable such as a slider or regression parameter:

- `a=2` then `a(3)^2` gave 36, not 18.
- `y=a(x-2)^2+1` graphed the wrong parabola.
- The vertex-form regression `y_1\sim a(x_1-h)^2+k` returned a = √2 instead of 2.

This is the standard vertex form on the SAT, so it would have broken T3 and T5 lessons without any visible error.

- **Cause:** the parser reads `a(…)` as a possible function call before it knows whether `a` is a function.
- **Fix:** when `a` turns out not to be a function, the compiler moves the exponent onto the parentheses (`compile`, case `'b'`).

**Changes to match Desmos:**

| Change | Where in `topline/index.html` |
|---|---|
| Intercepts, extremes and intersections for implicit curves and `x = …` curves. Tangent points are marked. Clicking an implicit curve selects it. | `findPOIs`, `implicitOf`, `roots1D`, `newton2`, `hitTest` |
| `midpoint(A,B)` and `distance(A,B)` | builtins |
| `%` and "% of" | tokenizer, parser, editor display |
| `°` and `^{\circ}` degree input | tokenizer, parser (`degu` node) |
| `x1` read as `x_1`, and auto-subscripting in the editor | tokenizer, `typeChar` |
| List slices `L[a...b]` and `L[a...]` | parser |
| a/b fraction toggle on exact results | `toFrac`, `renderInfo` |
| Clearer error for `{4,7}` used as a list | `piecewise` |
| Warning when a regression has fewer points than unknowns | `renderInfo` |

**Testing:**

- `engine-check.js` now has 38 cases, all passing. The 3 vertex-form cases fail on the old code.
- A diff of the ~120-input probe set before and after the changes shows only the intended changes.
- Points of interest and editor typing were checked in headless Chromium:
  - the screenshots match the expected points;
  - no page errors;
  - redraw time while zooming is unchanged.

## 4. Rules for the AI (system-prompt block)

These rules go into the cached system prompt for both the Solver and the Tutor. Each one comes from a result above.

```
CALCULATOR RULES. Students practise in Topline and take the SAT in Bluebook's Desmos.
Teach only keystrokes that work in both.

Syntax
1. Write subscripts with an underscore: x_1, y_1, L_1. (Typing x1 also becomes x_1
   in both calculators' editors, but x_1 is unambiguous in written instructions.)
2. Lists use square brackets: [3,7,8]. Curly braces {} are only for restrictions
   like y=x^2{0<x<5} or piecewise definitions.
3. Use one-letter names (a, b, k, h) or subscripted names (v_0). Never multi-letter
   names like area or cost: they are read as products of letters.
4. "20% of 50" is fine. Typing % shows "% of".
5. For degree problems, prefer switching to Degrees in Settings, then sin(30).
   30° also works.
6. Until midpoint(), distance() and list slices L[2...3] are confirmed in the
   College Board build, teach the formulas: ((x_a+x_b)/2, (y_a+y_b)/2) and
   sqrt((x_b-x_a)^2+(y_b-y_a)^2), and filters like L[L>5].
7. Use only features Bluebook has: graphing, sliders, tables, regressions, lists,
   statistics, sums. Don't teach Topline extras such as ttest, distributions,
   histograms or matrices for SAT work.

Clicking points
8. Click a curve to see its points of interest: intercepts, maximum/minimum,
   top/bottom of a circle, and intersections with the other curves.
9. Only points on screen are marked. Tell the student to zoom out before
   concluding there is no solution.
10. For "exactly one solution" (tangency), the touching point is marked, but also
    confirm by substitution or the discriminant.

Answers
11. Results show 6 significant figures. If the a/b button appears, the value is an
    exact fraction: use it for free-response answers. Decimals entered must follow
    SAT rules (use every space: .6666, .6667, 0.666 or 0.667, not 0.67).
12. A regression needs at least as many data points as unknown letters. Topline
    shows a warning when there are too few.
13. Never tell a student to retype a rounded regression value. Use the
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
   - `midpoint(` / `distance(` → formulas (until confirmed in Bluebook)
   - `{…}` used as a list → `[…]`
   - multi-letter names → single letters
   - stray `$` around expressions
   - `y=` written where a regression needs `~`

   Log every rewrite so the error taxonomy comes from real model behaviour.
5. **Error feedback loop.** Topline's error messages are short and specific, for example "b, c aren't defined yet", "A closing ] is missing", "Regressions use list data, like y_1 ~ m x_1 + b", and "y_1 is already defined". Feed them back to the model for up to N retries, as the report planned for `expressionAnalysis`.
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

## 6. Topline work still needed

1. **Tutor interface. Done.** `window.topline` in `topline/index.html` (the "tutor API" block just before boot) has `getState`, `setState`, `getExpressions`, `setExpressions`, `setExpression`, `removeExpression`, `analyze`, `evaluate`, `onChange`, `getSettings` and `setSettings` (`setSettings({collegeBoard: true})` switches College Board mode). A `postMessage` bridge serves the same methods when the calculator sits in an iframe, and pushes change events to the parent page. An `?allowOrigin=` URL parameter limits which host origins it answers.
   - `analyze()` returns each line's kind, value (as plain JSON), error, undefined names and regression results (parameters, R², RMSE, n).
   - `evaluate(latex)` does what a Desmos `HelperExpression` did, without adding a line.
   - This replaces the Desmos `getState`, `observeEvent`, `expressionAnalysis` and `HelperExpression` calls the integration doc relies on. Usage is in `topline/README.md` ("Tutor API"), and `node topline/tests/api-check.js` tests it in headless Chromium.
2. **Engine-level points of interest** the Solver can call without a screen (section 5, item 2).
3. **A College Board mode** that hides Topline features Bluebook doesn't have, so students don't come to rely on them. *Done:* a "College Board mode" switch in Settings, or forced with `index.html?mode=collegeboard`. The list is `CB_OFF` at the top of the UI code in `topline/index.html`; the engine gets the names through its `OFF` set and `tests/engine-check.js` covers them.
   - Confirmed off (College Board lists images, folders and notes; Topline only has notes): notes.
   - Hidden but unconfirmed, needs checking in `desmos.com/testing/collegeboard/graphing`: matrices (`\begin{matrix}`, `det`, `inv`, `rref`, `transpose`, `trace`), `random` and `shuffle`, complex-number mode, and the manual log-axis toggles.
   - Kept (reported present in Bluebook, or no reason to doubt): distributions and their pdf/cdf/inverse helpers, `ttest`/`ittest`, histograms, dot plots and box plots, `mad`, `cov`, `corr`, `var`, `varp`, `csc`/`sec`/`cot`, integrals. Also worth checking there: `var`/`varp`/`corr`, `erf`, `gamma`, `polygon`, and `real`/`imag`/`conj`/`arg` outside complex mode.
4. **Fix whatever the hand checks in section 7 turn up.**

## 7. Still to verify by hand in the College Board practice calculator

- Whether `x1` is auto-subscripted in Desmos.
- Whether `distance()` and `midpoint()` exist in the College Board build.
- Whether `L[1...3]` works in the College Board build.
- How Desmos marks tangent intersections, implicit-curve intersections and double roots, so Topline's markers can be matched exactly. (Users report Desmos marks only the top and bottom of a circle; Topline now does the same.)
- Whether `midpoint()` and `distance()` work in the College Board build. They are in Desmos's function list, but the default and several state testing builds disable them.
- Display precision: Desmos may show about 12 significant digits where Topline shows 6.
- The College Board build's default angle mode (sources disagree).
- How Desmos handles a regression with too few points.
- The degree-symbol behaviour, and whether the College Board build shows the fraction toggle.
- Rounding and display precision, so the AI's decimal-entry advice matches what students see in Bluebook.
- Each technique-library entry, run once in `desmos.com/testing/collegeboard/graphing`.

### Web evidence gathered so far (2026-10-16)

desmos.com was blocked, so these come from search-result snippets.

| Behaviour | Finding | Confidence |
|---|---|---|
| `x1` → x₁ | Desmos auto-subscripts a digit typed after a single letter ([r/Sat Desmos thread](https://reddit.birdcat.cafe/r/Sat/comments/1c8at7a/official_desmos_thread/l0qri87)) | High |
| `midpoint`, `distance` | Listed in Desmos's Supported Functions (Geometry); disabled in the default testing build and several state builds ([Default testing calculators PDF](https://www.desmos.com/state-pdfs/Default_Desmos_Calculators.pdf)); SAT prep sites teach them for Bluebook | High / Medium for the College Board build |
| `L[2...4]`, `L[2...]` | Documented in the Desmos Lists help article ([help.desmos.com](https://help.desmos.com/hc/en-us/articles/4407889068557)) | High |
| `30°` | Accepted in expressions; how it interacts with degree mode isn't documented | Medium |
| Points of interest | Explicit-function intercepts, extrema and intersections are documented; users report circles show only top and bottom; implicit and tangent cases are undocumented | Low–medium |
| Too few regression points | Not documented | Low |
| Fraction toggle | Exists (button and Shift+Alt+A / Shift+Cmd+A); SAT prep sites describe it in Bluebook | High |
| Disabled in the College Board build | Officially only images, folders and notes ([College Board Desmos PDF](https://www.desmos.com/assessment-pdfs/CollegeBoard_Desmos_Calculator.pdf)); distributions and t-tests reported present (AP Statistics uses Bluebook Desmos from 2026) | High / Low for the rest |
| `20% of 50` | Typing `%` inserts "of" ([Desmos blog](https://blog.desmos.com/articles/friday-fave-for-september-15)) | High |

## Sources

- Topline source and tests in this repository: `topline/index.html`, `topline/tests/engine-check.js`.
- Desmos "% of" design note: [Desmos blog, Friday Fave for September 15](https://blog.desmos.com/articles/friday-fave-for-september-15).
- Technique list and published worked examples: `research_notes/AI Desmos SAT math course plan/desmos_techniques.md` and its sources.
- Training approach (Solver/Tutor split, rejection sampling, evals): `research_notes/AI Desmos SAT math course plan/gemini_desmos_ai.md`.
