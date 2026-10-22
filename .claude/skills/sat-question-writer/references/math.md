# Math questions

## Format (one JSON object per line)

```json
{"id": "adv-vertex-from-two-points", "domain": "advanced-math", "skill": "Nonlinear functions", "difficulty": "hard",
 "format": "spr", "stem": "...", "techniques": ["T5"], "route": "desmos-primary",
 "desmos": {"lines": ["x_1=[-1,0,2]", "y_1=[6,2,6]", "y_1\\sim a(x_1-h)^2+k"], "read": "Read $h = 0.5$ from the fit ...", "verified": false},
 "byHand": "... Distractors: ...",
 "provenance": {"author": "claude-question-writer", "created": "2026-10-22", "notes": "batch alg-gaps-1"},
 "status": "draft", "answers": [{"num": 1, "den": 2}], "tex": true,
 "check": {"sympy": "...", "topline": {"expect": {"param": "h", "value": 0.5}}, "value": "1/2", "blind": "1/2"}}
```

| Field | Rule |
|---|---|
| `id` | Unique, kebab-case, prefixed by domain: `alg-`, `adv-`, `psda-`, `geo-`, then what the item tests (`adv-tangent-k`, `psda-weighted-mean-new-members`). Not a number. |
| `domain` | `algebra`, `advanced-math`, `psda`, `geometry-trig` |
| `skill` | Exactly one of the names in `skills.json` for that domain |
| `difficulty` | `easy`, `medium`, `hard` |
| `format` | `mc` (four `choices` + `answerIndex` 0–3) or `spr` (`answers`: list of `{"num", "den"}` exact fractions; usually one) |
| `stem` | The question. Math in `$...$`. A table goes in the stem as text the bank already uses ("A table of values ... lists the pairs ..."), or describe a figure in words precisely enough to solve without a picture |
| `choices` | MC only. Four distinct strings, math in `$...$` |
| `techniques` | Desmos technique ids from `techniques.json` that the Desmos route uses (`[]` for hand-only) |
| `route` | `desmos-primary` (calculator is faster), `hand-primary` (hand is faster), or `either` |
| `desmos` | `null` for hand-only items; otherwise `lines` (calculator input, one string per line, Desmos LaTeX) and `read` (what the student does and reads: "Click the intersection: $(4, 3)$") and `verified: false` (the exporter sets it) |
| `byHand` | The worked solution a student could do on paper, then `Distractors:` and one note per wrong choice naming the mistake that produces it, separated by semicolons. For SPR, cover the common wrong answers and any entry trap (rounding, sign) instead |
| `provenance` | `author: "claude-question-writer"`, today's `created` date, `notes` with the batch name and how the key was checked |
| `status` | `"draft"` |
| `tex` | `true` |

## SPR (student-produced response) rules

- The answer must be enterable in Bluebook: up to 5 characters for a positive answer, 6 for a negative one (the minus sign counts). Fractions and decimals are both accepted, but a decimal can't be rounded more coarsely than the box allows (for $\frac{2}{3}$: `2/3`, `.6666`, `.6667`, `0.666`, `0.667` are right; `0.67` is wrong).
- So SPR answers are rational numbers stored as exact fractions. If the answer is irrational ($\sqrt{2}$, $\pi$), make it multiple choice or ask for a rational quantity (like the square of a length).
- If the answer has a messy decimal, mention the entry rule in `desmos.read` the way the bank does ("Enter $\frac{2}{3}$ or .6667; 0.67 is marked wrong").
- If several answers are acceptable ("one possible value"), list them all in `answers`.

## Calculator lines (`desmos.lines`)

Students practise in Topline (our calculator) and sit the test in Bluebook's Desmos, so lines must work in both. The checker runs every line through Topline and fails the item on any error.

- Subscripts with an underscore: `x_1`, `y_1`. Lists in square brackets: `[2,3,4]`. Curly braces only for restrictions or piecewise (`y=x^2\left\{0<x<5\right\}`).
- Single-letter names (`a`, `b`, `k`, `h`) or subscripted (`v_0`). Multi-letter names are read as products of letters.
- Regressions and the tilde trick use `\sim` with list data: `y_1\sim mx_1+b`, `(5x_1-17)(4x_1-c)\sim ax_1^2+bx_1+119` with `x_1=[2,3,4]` (at least as many list values as unknowns).
- Use `\frac{}{}`, `\sqrt{}`, `\left|...\right|`, `\operatorname{mean}(L)`, `\operatorname{median}(L)`, `\operatorname{stdev}(L)` (sample), `\operatorname{stdevp}(L)` (population).
- Degree problems: say in `read` to switch to Degrees; don't rely on `°`.
- Prefer the midpoint/distance formulas to `midpoint()`/`distance()` until those are confirmed in the College Board build.
- Points of interest (intersections, intercepts, vertices) are clicked, not computed by a line. Say what to click in `read`, and for the checker add a helper line that computes the same value in `check.topline.lines`.

Choose the route honestly: `desmos-primary` when typing it in is clearly faster than the algebra (messy roots, regressions, many-step evaluation), `hand-primary` when a student who knows the move finishes in under about 30 seconds, `either` when they're close. Many items are faster by hand (interpretation, structure, quick algebra); mark them `hand-primary` and keep a Desmos check route only if it's genuinely useful.

## What good Math items look like

- Contexts are realistic and short: a rate, a recipe, a gym membership, a lab measurement. Units are consistent and stated.
- Money is written in words, as the bank does: "45.00 dollars", "3.50 dollars per mile". Never use a `$` sign for money: `$` starts math, and the bank's LaTeX tests fail on it.
- Numbers are chosen so the hand route is clean and the calculator route still works; hard items get their difficulty from structure, not arithmetic.
- Unknown-constant items ("for what value of $k$ ...") are good hard items and often have a slider or tilde route (T3, T6).
- Data items (PSDA) give the data in the stem (a list or a described table) so the student can type it into a list.
- Geometry items describe the figure fully in words; avoid anything that needs a drawing to be solvable unless a figure will be added later (note it in `check.notes`).
- Check the skill's `testingPoints` in `skills.json` and cover the variety there, not just the most familiar one.
