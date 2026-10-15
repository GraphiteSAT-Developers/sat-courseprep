# Bluebook Desmos audit: hands-on checklist

**Purpose.** Confirm, feature by feature, that the calculator embedded in `web/` behaves the way the College Board calculator does on test day, and settle the Desmos behaviours the technique library relies on but no source confirmed. The result feeds `web/lib/desmos/config.ts` (`COLLEGE_BOARD_OPTIONS`), the technique library (T1–T13), and the headless verification service, which must import the same options.

**What the notes claim, and how sure they are.** The only official source found was Desmos's College Board reference PDF, which says the test version disables **images, folders and notes** and automatically turns on **Log Mode** for applicable exponential, logarithmic and power regressions ([CB Desmos PDF](https://www.desmos.com/assessment-pdfs/CollegeBoard_Desmos_Calculator.pdf)). Third-party guides say tables, `~` regression, sliders, lists and statistics all work ([sat_math_format notes](../../research_notes/AI%20Desmos%20SAT%20math%20course%20plan/sat_math_format.md)). One guide claims the test version "is not stripped down", which contradicts the PDF ([The Test Advantage](https://thetestadvantage.com/blog/is-desmos-allowed-on-the-sat)). College Board says students can **resize** the calculator from 2026–27 ([CB changes](https://satsuite.collegeboard.org/k12-educators/educator-experience/in-school/start/changes)). The research could not open desmos.com or collegeboard.org directly, so even the PDF claim was read from a search summary. **Nothing in this file is verified until the "Observed" columns are filled in.**

## Setup

You need three windows open side by side:

1. **Bluebook practice mode.** Install Bluebook, open a full-length practice test (Test 4–11) or the test preview, go to any Math question, and open the calculator. This is the ground truth. Note the Bluebook version number and the date.
2. **The public College Board configuration:** desmos.com/testing/collegeboard/graphing. Useful because it's always available; treat Bluebook as the tie-breaker if they differ.
3. **Our embed.** Run the site locally (`web/README.md`) with a real Desmos API key in `NEXT_PUBLIC_DESMOS_API_KEY` (only the mock has been tested so far). Note the API version loaded (`NEXT_PUBLIC_DESMOS_API_VERSION`, default `v1.11`).

For each row: try the same keystrokes in all three, write what you saw, and pick an action. Take a screenshot of anything surprising and save it next to this file as `audit-<row>.png`.

Fill the Observed columns with: **works / disabled / missing / differs (how)**.

## Part A: feature parity (config.ts options)

| # | Feature | Expected per notes | Source | Observed in Bluebook | Observed at desmos.com/testing | Observed in our embed | Action |
|---|---|---|---|---|---|---|---|
| A1 | Images (add image to graph) | Disabled | CB PDF | | | `images: false` → | |
| A2 | Folders | Disabled | CB PDF | | | `folders: false` → | |
| A3 | Notes (text expressions) | Disabled | CB PDF | | | `notes: false` → | |
| A4 | Sliders (type `y=kx`, accept "add slider") | Works | Test Advantage, EdisonOS | | | `sliders: true` → | |
| A5 | Tables (`+` → table, or type a table) | Works | sat_math_format notes | | | (Desmos default) | |
| A6 | Linear regression `y_1 ~ m x_1 + b` on a table | Works | EdisonOS | | | | |
| A7 | Nonlinear regression `y_1 ~ a b^{x_1}` (exponential) | Works; **Log Mode auto-on** | CB PDF | Is "Log Mode" shown and checked? | | | |
| A8 | Power and log regressions (`y_1 ~ a x_1^b`, `y_1 ~ a + b\ln(x_1)`) | Log Mode auto-on | CB PDF | | | | |
| A9 | Regression statistics shown (r, R², residuals) | Shown in UI; no API route to R² | gemini_desmos_ai notes | What statistics appear? | | | Decide whether the tutor may teach "read R²" |
| A10 | One-click regression button (if any, in the table or expression menu) | Unknown; flagged for checking | sat_math_format gap | Does a button exist? What does it insert? | | | |
| A11 | Lists `[1,5,5,10]` | Works | Desmos Supported Functions | | | | |
| A12 | Stats functions `mean`, `median`, `stdev`, `stdevp`, `min`, `max`, `quartile`, `quantile` | Work | Desmos Supported Functions | Try each | | | |
| A13 | Default angle mode on open | Unknown; Desmos default is radians | config.ts comment | Open fresh: degrees or radians? Where is the toggle? | | `degreeMode: false` → | Set `degreeMode` to match Bluebook |
| A14 | Points of interest (gray dots) on click: intersections, zeros, y-intercept, vertex | Clickable in UI; coordinates shown | Test Advantage, Learner Labs | Click a parabola and a pair of lines | | | |
| A15 | Circle points of interest (top/bottom marked; left/right not reliable) | Partly | Learner Labs | Graph `x^2+y^2-6x+4y-3=0`; which points are marked? | | | Keep T10 hand-primary unless all four appear |
| A16 | Resize the calculator panel | Works from 2026–27 | CB changes page | Can you drag the panel size? | n/a | Is our panel resizable? | |
| A17 | Settings menu (grid, axes, angle mode, zoom square) | Assumed on | config.ts | | | `settingsMenu: true` → | |
| A18 | Zoom buttons and zoom-to-fit | Assumed on | config.ts | | | `zoomButtons: true` → | |
| A19 | Share / graph links, paste a graph link | Off in our embed by choice | config.ts | Is there any share UI in Bluebook? | | `links: false`, `pasteGraphLink: false` | |
| A20 | Fraction toggle (decimal → exact, 5.125 → 41/8) | Works | LearnQ | | | | Needed for T11 |
| A21 | Switch between graphing and scientific calculator; content does not carry over | Both available, separate state | Desmos Help 30913914831757 | | n/a | We embed graphing only: decide whether to add scientific | |
| A22 | Keypad / on-screen keyboard | Unknown | | Is there a keypad? Which keys (`~`, `|`, `≤`)? | | | |
| A23 | Piecewise functions `{x<0: -x, x}` | Flagged for checking | sat_math_format gap | | | | |
| A24 | Inequalities: `<=` auto-converts, dashed vs solid boundary, shading | Works | Effortless Math | | | | |
| A25 | Function definition and evaluation (`f(x)=2x+5`, then `f(3)`) | Works | EdisonOS | | | | |
| A26 | `midpoint(A,B)`, `distance(A,B)` with named points | Works | Learner Labs | | | | |
| A27 | Expression count or other limits (any cap on lines?) | Unknown | | Add 30+ expressions | | | |
| A28 | Default viewport on open (axis ranges) | Unknown | | Note the default window | | | Match in `setMathBounds` if different |

## Part B: unsourced moves from the technique notes (test before teaching)

These came from background knowledge, not from any source ([desmos_techniques notes, Inferences](../../research_notes/AI%20Desmos%20SAT%20math%20course%20plan/desmos_techniques.md)). A "works in Bluebook" result is required before any of them goes into the curriculum or the AI's technique library.

| # | Move | What to type | Expected (unverified) | Observed in Bluebook | Observed in our embed | Action |
|---|---|---|---|---|---|---|
| B1 | Vertex / max / min by clicking | `y=x^2-4x+1`, click the curve | Gray dots at vertex, zeros, y-intercept; click shows coordinates | | | |
| B2 | Sum and product | `sum`, `prod`, `total([1,2,3])` | Σ/Π templates appear; `total` sums a list | | | |
| B3 | List generation | `[1...10]`, `[2,4,...,20]` | Produces the list | | | |
| B4 | Absolute-value solution counting | `y=|x-3|`, `y=k` with slider | Count intersections as k slides | | | |
| B5 | Percent syntax | `20% of 50`, `20%` | May or may not parse | | | If unsupported, teach decimals only |
| B6 | Domain restriction with braces | `y=x^2 {0<x<5}` | Restricts the graph; confirms `{}` ≠ list | | | Pair with T7 pitfall |
| B7 | Implicit multiplication | `ab`, `ax^2+bx+c`, `x1` | `ab` = a·b with sliders offered; `x1` may auto-subscript | | | Settle the "use `x_1`" rule |
| B8 | Tilde "find the constants" (T6) | `(5x_1-17)(4x_1-c) ~ a x_1^2 + b x_1 + 119` with `x_1=[2,3,4]` | c=7, a=20, b=−103 | | | Confirm it works without a table |
| B9 | Tilde with list omitted | Same, no `x_1=[...]` line | Fails silently (no values) | | | Confirm the failure mode the tutor must warn about |
| B10 | Exponential growth with sliders | `y=a(1+r)^x` | Sliders for a and r | | | |

## Part C: things the headless verification service needs to know

The AI collaborator owns the service, but the answers come from this audit.

| # | Question | Why | Observed | Action |
|---|---|---|---|---|
| C1 | Which API version does Bluebook's build correspond to, if visible? | Pin `NEXT_PUBLIC_DESMOS_API_VERSION` to match | | |
| C2 | Do regression parameters (a, b, m) become usable variables in later lines? | Verification reads them via `HelperExpression` | | |
| C3 | Does the embed's `expressionAnalysis` report an error for things Bluebook also rejects (e.g. a note, an image)? | Error parity | | |
| C4 | Any difference in number formatting (digits shown, rounding) between Bluebook and the embed | SPR answers are truncated/rounded at the 4th digit | | |

## When done

1. Edit `web/lib/desmos/config.ts` so every option matches column "Observed in Bluebook", and replace the UNVERIFIED comment with the audit date and Bluebook version.
2. In the technique library, mark each of B1–B10 as "verified in Bluebook on <date>" or remove it.
3. Hand Part C to the AI collaborator.
4. Record the audit date and any discrepancies in `HANDOFF.md`.
