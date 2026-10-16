# Item style guide: writing to the College Board framework

_Derived from chapter 4 ("The Math Section") of the College Board_
_Assessment Framework for the Digital SAT Suite (v3.01), plus the Math
section directions reproduced in its appendix D. Chapter 4 is the official
statement of what the Math section tests and how its questions are written;
this guide turns it into rules for every item batch. It complements
`docs/item-writing.md` (process: provenance, SymPy checks, Desmos fields),
which still applies. Where the two disagree, this guide wins on style and
`item-writing.md` wins on process._

The framework's sample questions are College Board content. They were read
to extract conventions and **none of them is reproduced here**, nor may any
of them, or any paraphrase, number swap or "inspired by" variant, go into
`web/content/items.ts`. See section 9.

## 1. Section facts (SAT; Tables 15, 16, 19, 20)

| Fact | Value |
|---|---|
| Design | Two-stage adaptive: one Math section, two separately timed modules |
| Questions | 44 total: module 1 = 20 operational + 2 pretest; module 2 = 20 operational + 2 pretest |
| Time | 35 min + 35 min = 70 min; average 1.59 min per question |
| Score | 200–800 in 10-point steps; half the total score |
| Adaptivity | Module 1 (the "routing" module) is a broad mix of easy, medium and hard. Module 2 is also a mix, but its average difficulty is higher or lower depending on module 1 performance. All operational questions in both modules count toward the score. |
| Order within a module | Questions are arranged "from easiest to hardest". Pretest questions sit in varying positions. |
| Navigation | Free within a module (preview, flag, return). No return to module 1 once module 2 starts. |
| Formats | Four-option multiple choice ≈75% (28–32 of 40 operational); student-produced response (SPR) ≈25% (8–12). |
| Context | ≈30% of questions in context (10–14 of 40). Topics: science, social studies, real-world. |
| Word count | A majority of in-context questions are 50 standardized (6-character) words or fewer. |
| Graphics | "A wide range of data displays, geometric figures, and xy-plane graphs" |
| Domains per module | All four domains appear in every module. |
| Pretest | 2 per module, 4 per form; indistinguishable from operational items. |

Domain weights (operational questions per form, SAT):

| Domain | Share | Questions | MC | SPR |
|---|---|---|---|---|
| Algebra | ≈35% | 13–15 | 10–11 | 3–4 |
| Advanced Math | ≈35% | 13–15 | 10–11 | 3–4 |
| Problem-Solving and Data Analysis | ≈15% | 5–7 | 4–5 | 1–2 |
| Geometry and Trigonometry | ≈15% | 5–7 | 4–5 | 1–2 |
| Total | 100% | 40 | 28–32 | 8–12 |

PSAT/NMSQT and PSAT 10 shift to 35 / 32.5 / 20 / 12.5 and PSAT 8/9 to
42.5 / 20 / 25 / 12.5 (Tables 17–18). This course targets the SAT only; the
42.5/20/25/12.5 figures that appear in search results are PSAT 8/9 and must
not be used. Two SAT-only facts: **circles are assessed only on the SAT**, and
rational and radical equations and trigonometry are absent from PSAT 8/9, so
third-party banks that mix suite levels under-represent exactly the topics a
700–800 course needs.

Batch implication: a 40-item "form-shaped" batch is 14/14/6/6 by domain,
about 30 MC and 10 SPR, with SPR spread across all four domains (at least one
PSDA and one Geometry/Trig SPR), about 12 items in context, and every domain
present in any module-sized subset.

## 2. Domains and skill/knowledge testing points

Each question "is classified as belonging to a single content domain" and,
within it, to one skill/knowledge testing point. The `skill` field must use
the exact names below (Table 16; Tables 21–24). The claim sentence for each
domain is the framework's own one-line description of what the domain tests.

### Algebra (`domain: "algebra"`)

Claim: students "interpret, create, use, represent, and solve problems using
linear representations and make connections between different representations
of linear relationships."

| Skill name (exact) | Framework sub-points seen in sample explanations |
|---|---|
| Linear equations in one variable | solve; create from a context |
| Linear equations in two variables | "Make connections between an algebraic representation and a graph"; "interpret a solution, constant, variable, factor, or term based on the context" |
| Linear functions | "Evaluate a linear function given an input value"; "Interpret the graph of a linear function in terms of a context" |
| Systems of two linear equations in two variables | "Create and use a system of two linear equations" |
| Linear inequalities in one or two variables | "For a linear inequality, interpret a point in the xy-plane" |

### Advanced Math (`domain: "advanced-math"`)

Claim: students "interpret, rewrite, fluently solve, make strategic use of
structure, and create absolute value, quadratic, exponential, polynomial,
rational, radical, and other nonlinear equations and make connections between
different representations of a nonlinear relationship between two variables."

| Skill name (exact) | Sub-points |
|---|---|
| Equivalent expressions | "Rewrite a rational expression"; also polynomial, radical and exponential rewrites |
| Nonlinear equations in one variable and systems of equations in two variables | "Determine the conditions under which a quadratic equation has zero, one, two, or infinitely many real solutions"; "Solve systems of linear and nonlinear equations in two variables" |
| Nonlinear functions | "Determine the most suitable form of a function to display key features"; "Make connections between algebraic representations and a graph"; "Create and use quadratic or exponential functions" |

Absolute value belongs to Advanced Math (it is named in the claim), not to
Algebra.

### Problem-Solving and Data Analysis (`domain: "psda"`)

Claim (SAT): "fluently solve problems using percentages, proportional
relationships, ratios, rates, and units; analyze and interpret distributions
of data; use various representations of data to find relative frequency,
probabilities, and conditional probabilities; fit models to data and compare
linear and exponential growth; and calculate, compare, and interpret mean,
median, range and standard deviation, understand basic study design, estimate
population parameters from sample statistics, and interpret margin of error."

| Skill name (exact) | Sub-points |
|---|---|
| Ratios, rates, proportional relationships, and units | "Solve problems involving derived units" (density, speed, unit conversion) |
| Percentages | "Use percentages to solve problems" (including percent of a percent) |
| One-variable data: distributions and measures of center and spread | "Compare distributions using measures of center and spread" (effect of shifting every value on median and range) |
| Two-variable data: models and scatterplots | "Analyze and interpret data in a scatterplot" (read a line of best fit) |
| Probability and conditional probability | relative frequency from tables |
| Inference from sample statistics and margin of error | interpretation, SAT only in this full form |
| Evaluating statistical claims: observational studies and experiments | SAT only |

### Geometry and Trigonometry (`domain: "geometry-trig"`)

Claim (SAT): "solve problems associated with length, area, volume, and scale
factors using geometric figures; determine congruence, similarity, and
sufficiency using concepts and theorems about vertical angles, triangles, and
parallel lines cut by a transversal; solve problems using the Pythagorean
theorem, right triangle and unit circle trigonometry, and properties of
special right triangles; and use properties and theorems relating to circles
to solve problems."

| Skill name (exact) | Sub-points |
|---|---|
| Area and volume | length/area/volume and scale factors |
| Lines, angles, and triangles | "Use concepts of congruence and similarity of triangles to solve problems"; "Determine which statements may be required to prove certain relationships or satisfy a given theorem" |
| Right triangles and trigonometry | "Use the Pythagorean theorem to solve problems"; right-triangle and unit-circle trig; special right triangles |
| Circles | "Use definitions, properties, and theorems relating to circles to solve problems" (arc measure vs. arc length, circumference) |

### Name reconciliation with the project

- `web/content/types.ts` keeps `skill` as a free string and uses the domain
  slugs `algebra`, `advanced-math`, `psda`, `geometry-trig`. The slugs stay;
  the `skill` string must be one of the 19 exact names above.
- `research_notes/.../sat_math_format.md` lists the same 19 names and marked
  the list "unverified". It is now verified against Table 16; only the
  ordering differs (the framework lists Linear functions third, after Linear
  equations in two variables).
- The research note's "Problem-Solving & Data Analysis" and "Geometry &
  Trigonometry" use ampersands; the framework uses "and". Use "and" in
  anything student-facing.
- `docs/hard-question-map.md` uses informal type names ("Vieta", "tangent
  line"). Those are fine as a planning vocabulary but every item still carries
  one of the 19 official skill names.
- Two of the framework's sample items list a sub-point without naming the
  parent skill (the dot-plot comparison and the parallel-line sufficiency
  item). Map those to "One-variable data: distributions and measures of
  center and spread" and "Lines, angles, and triangles" respectively.

## 3. Stem conventions

Observed across the chapter's twenty sample questions. Follow them; they are
what makes an item read as SAT rather than textbook.

**Displayed equation, then a short question.** When the item is about one
equation, inequality or function rule, the equation is set on its own line
above the prose and the prose refers to it as "the given equation", "the given
inequality" or "the given function". The prose line is then one sentence:
"How many distinct real solutions does the given equation have?", "What is the
minimum value of the given function?", "Which point (x, y) is a solution to
the given inequality in the xy-plane?" Do not restate the equation in the
sentence.

**Constants are declared in a trailing "where" clause**, with the sign or
domain restriction that makes the answer unique: "where b is a positive
constant", "where a and b are positive constants", "where k is a constant".
The restriction is part of the math, not decoration: the explanations use it
to discard the second root. If the key needs a restriction to be unique, the
stem must carry it.

**Functions.** Introduce a function as "The function h is defined by
h(x) = ...", or inline as "If f(x) = ... and g(x) = ...". Ask for values as
"what is the value of f(2)?" or of a combination "what is the value of
4f(2) − g(2)?". Ask for a product of constants as "What is the value of ab?".
Exponential behavior can be described without a formula: "for each increase
in x by 1, the value of f(x) decreases by 80%" (the student must build the
model).

**Graphs and the xy-plane.** A graph of a function is "the graph of y = h(x)
in the xy-plane", a line is "a line with equation ...", a parabola "a
parabola with equation ...". Points are "passes through the points (0, 10)
and (−2, k)". Intercepts: "The y-intercept of the graph of ... in the
xy-plane is (0, y)". Tangency is phrased as "intersects ... at exactly one
point". Always say "in the xy-plane" when a graph, point or intersection is
involved; never "on the coordinate plane" or "on a graph".

**Context phrasing.** Word problems open with one or two plain declarative
sentences that set the scenario and define variables, then end with the
question. Pattern: "[Scenario]. [Second fact]. The equation ... represents
this situation, where x is ... and y is ... . Which statement is the best
interpretation of 6 in this context?" Variables are always tied to a quantity
with its unit: "the estimated temperature y, in kelvins, ... when its pressure
is x atmospheres". Prices are written with a dollar sign and two decimals
($5.50, $37.00). Quantities with units are written in words: "353 kilograms
per cubic meter", "3 inches", "45°" (the degree sign is used, not the word).

**Units go inside the question, set off by commas**: "What is the
circumference, in inches, of the circle?", "How tall, in feet, is the other
tree?", "What is the estimated temperature, in kelvins, ...?". The unit is
never only in the answer choices.

**Rounding and estimation instructions live in the stem**: "To the nearest
hundredth of a meter, what is ...?"; "which of the following is closest to
the y-value predicted by the line of best fit?" ("closest to" whenever the
answer is read from a graph).

**Sentence length.** Stems are two to four sentences; the question sentence
is almost always under 20 words. The framework's rule for context items is
50 words or fewer for most of them, "simple, clear, and direct" language, and
no topic-specific prior knowledge. If a context stem passes 60 words, cut.

**Stem vs. figure.** Anything that can be read from a figure (axis labels and
units, point values, angle marks, data values) is not repeated in the stem;
the stem says what the figure shows ("The graph shows ...", "The scatterplot
shows the relationship between two variables, x and y. A line of best fit for
the data is also shown.", "Data set A has 15 values and is represented by the
dot plot shown.") and asks the question. Conversely, geometry items that need
no figure get none: a rectangle with a given diagonal, a circle with a given
arc, two trees and their shadows are all described in words. When a figure is
referenced but not drawn, say so: "(not shown)".

**"Which of the following" framing.** Used when the choices are objects
rather than numbers: "Which expression is equivalent to ...?", "Which point
(x, y) is a solution to ...?", "Which statement is the best interpretation of
6 in this context?", "Which of the following correctly compares the medians
and the ranges of data sets A and B?", "Which additional piece of information
is sufficient to prove that lines j and k are parallel?". Numeric answers use
"What is the value of ...?" or "How many ...?" instead.

**Tone.** Third person, present tense, no names of people, no "you". Contexts
are generic (a store, a tank of gas, a type of wood, two trees, a group of
items), never a real organization. "Certain" and "a certain" mark an
unspecified instance ("a certain purchase", "a certain type of wood").

## 4. Answer-choice conventions

- Exactly four options, labeled A–D, one key. The framework: each distractor
  "represents a common error that students might reasonably make ... or
  common misconception", is "plausible to degrees varying depending on the
  intended difficulty", and "no distractor is meant to compete with the key".
- **Numeric choices are ordered monotonically.** Ascending is the norm (−5,
  1, 22, 28; 0.98, 0.99, 1.01, 1.02; √17, 20, 15√2, 400), but the sample set
  also uses descending (3,025; 110; 55; 0 and 12, 8, 5, 4). Pick one direction
  per item and never mix. `item-writing.md` says ascending; keep that as the
  default, but descending is legitimate SAT style and is allowed.
- **Non-numeric choices are parallel in structure and ordered by a visible
  logic.** Count-of-solutions choices read "Exactly one / Exactly two /
  Infinitely many / Zero". Variable-valued choices go in alphabetical variable
  order (w, x, y, z). Comparison choices form a 2×2 grid (greater/equal ×
  greater/equal) with every sentence built from the same template.
  Interpretation choices are full sentences with the same frame ("Each side of
  figure B has a length of 6 inches." / "The number of sides of figure B is
  6."). Expression choices share a visual form so the choice cannot be made
  by shape alone.
- Percent choices carry the % sign; dollar choices would carry $; plain
  numbers carry nothing. Choices never carry a unit that the stem already
  fixed ("in inches").
- Distractors in the sample explanations are built from these mistakes, which
  form the house list:
  - the value of the wrong variable or the wrong quantity (the number of
    pints of raspberries, not blackberries; the x-value where the minimum
    occurs, not the minimum; the pressure, not the temperature)
  - an intermediate result reported as final (f(2) − g(2) when 4f(2) − g(2)
    was asked; the arc length itself; the square of the side rather than the
    side; a^(−2)·b instead of ab)
  - an order-of-operations or grouping slip (4·2 + 7 for 4(2 + 7))
  - a wrong operation on the given numbers (difference of the shadows;
    doubling the arc length; squaring it)
  - the wrong percent operation (40% − 30%, 40% + 30%, 30 as a percent of 40,
    instead of 30% of 40%)
  - reading the graph at the neighboring x-value (x = 31 or 33 instead of 32),
    or reporting the residual instead of the prediction
  - a true-but-irrelevant fact (vertical angles are always equal; the
    supplementary angle is always 140°) in a sufficiency item
  - the sign error or the discarded root when a constant is restricted
- Explanations name the mistake for each distractor they can; the rest get
  "may result from conceptual or calculation errors". In `byHand`, name the
  mistake for every distractor; do not fall back to the generic phrase.
- Key position: no pattern in the samples (C, C, D, A, C, C, C, D, A, C, A, B,
  B, B, B, D, A). Spread it across a batch.

## 5. SPR conventions

From section 4.1.6 and the Math directions in appendix D.

- The answer is a single number: integer, fraction, or decimal. "Up to 5
  characters for a positive answer and up to 6 characters (including the
  negative sign) for a negative answer."
- "If you find more than one correct answer, enter only one." Items may have
  several keys; the official key list shows every acceptable form (e.g. a
  decimal and its fraction, "3.44, 86/25"). Our `answers` array holds one
  `Rational` per distinct value, and the grader derives acceptable forms.
- Fractions that do not fit are entered as decimals; decimals that do not fit
  are "truncated or rounded at the fourth digit". Mixed numbers are not
  accepted (3 1/2 is wrong; 7/2 or 3.5 is right). No symbols: no %, comma or
  $ sign.
- Acceptable/unacceptable examples in the directions: 3.5 → 3.5, 3.50, 7/2
  (not 31/2, 3 1/2). 2/3 → 2/3, .6666, .6667, 0.666, 0.667 (not .66, 0.66,
  .67, 0.67). −1/3 → −1/3, −.3333, −0.333 (not −.33, −0.33). Bluebook rejects
  entries with too many digits or any character other than digits, "−", "/"
  and ".".
- Consequences for writers:
  - A key must be expressible in 5 (or 6) characters as either a reduced
    fraction or a decimal; prefer keys that fit exactly (integers, short
    fractions, terminating decimals). A key like 86/25 is fine because 3.44
    also fits. A key like 1/7 is fine (fraction fits) but write `desmos.read`
    to tell the student to use the fraction toggle rather than 0.142857.
  - Never key a percent, a dollar amount with a sign, a unit, a coordinate
    pair, an expression, or "x = 3". If the stem is about a percent, ask for
    "the value of p" where p% is defined in the stem.
  - If several values satisfy the stem, say so: "What is one possible value
    of x?" and list all of them in `answers`.
  - Use a constant restriction ("where b is a positive constant") to make a
    key unique rather than leaving two roots and hoping.
  - The sample SPR stems are the same shape as MC stems; nothing in the stem
    signals the format.
- Directions that apply to every item unless the stem says otherwise: "All
  variables and expressions represent real numbers", "Figures provided are
  drawn to scale", "All figures lie in a plane", and "The domain of a given
  function f is the set of all real numbers x for which f(x) is a real
  number". Do not add these sentences to stems; override them only when
  needed ("where x is an integer").

## 6. Difficulty

The framework does not define easy/medium/hard. What it does say:

- Each module is "a broad mix of easy, medium-difficulty, and hard
  questions", arranged easiest to hardest; the hard Module 2 raises the
  average.
- Distractor plausibility scales with intended difficulty: on a hard item the
  distractors must each be the product of a real, specific mistake, not
  throwaways.
- The samples are "merely illustrative and do not necessarily reflect the
  full range of question content or difficulty".

What the sample explanations reveal about what adds difficulty, in rough
order of weight:

1. **An unknown constant with a restriction** that must be used to pick the
   root (positive constant, discriminant set to zero, then choose the sign).
2. **Translating a verbal rule into a model before computing** (an 80%
   decrease per unit step becomes a base of 0.2; density and mass become a
   volume, then a cube root).
3. **Two concepts chained** (arc measure to fraction of the circle to
   circumference; similarity to proportion to solve; Pythagorean theorem with
   a radical hypotenuse).
4. **A structural insight replacing computation** (a square is never
   negative, so an equation has zero solutions; adding a constant shifts the
   median but not the range).
5. **Sufficiency reasoning** rather than calculation (which angle fact
   proves parallel lines), where every distractor is a true statement.
6. **Reading precision** (nearest hundredth; "closest to"; the correct
   expression among four with the same denominator form).

Easy items in the samples are one-step: evaluate a function at an input,
substitute 0 for x, read a value off a graph, test a point in an inequality.
Map to our tags: `easy` = one step and one representation; `medium` = one
idea with one trap or one translation; `hard` = a restricted constant, a
structural insight, or two ideas chained, with every distractor a named
mistake. This agrees with `item-writing.md` section 4.

## 7. Figures and tables

- Graphics appear on "select questions"; the chapter's samples use four
  (a line graph in context, a scatterplot with a line of best fit, a dot
  plot, a transversal diagram) out of twenty. Budget roughly one figure in
  five items, more in PSDA.
- xy-plane graphs show both axes with arrowheads, the origin marked O, axis
  variables x and y at the arrow tips, and, in context, axis titles with
  units ("Temperature (kelvins)", "Pressure (atmospheres)"). Gridlines are
  drawn when the student must read values; tick labels are at regular
  intervals (100, 200, ... or 24, 26, 28, ...). A broken axis is drawn when
  the x-range does not start at 0.
- Scatterplots: the stem says a line of best fit "is also shown"; the line is
  drawn through the cloud, not labeled with an equation.
- Dot plots carry a title ("Data Set A") and integer tick labels; the stem
  states the number of values.
- Geometric figures use italic single letters for lines (j, k, ℓ) and points
  (A, B, O), variable angle measures written "x°", given measures written
  "40°". Figures are drawn to scale by default (directions). When a figure is
  deliberately not to scale, the caption "Note: Figure not drawn to scale."
  goes directly under the figure, above the stem, exactly that wording.
- The stem refers to a figure as "the figure shown", "the graph", "the
  scatterplot", "the dot plot shown". Tables (none in the chapter's samples,
  but listed under informational graphics) follow the same pattern: title
  above, the stem says what the table shows.
- The reference sheet available in Bluebook holds: area of circle, rectangle
  and triangle; circumference; Pythagorean theorem; 30-60-90 and 45-45-90
  side ratios; volume of box, cylinder, sphere, cone and pyramid; 360° and 2π
  per circle; 180° per triangle. Do not write stems that hand the student one
  of these formulas; do write stems that need a formula not on the sheet
  (vertex form, discriminant, arc length, circle equation) without giving it.

## 8. Explanation style (for `byHand`)

The sample explanations follow one voice, and `byHand` should too, because
the tutor surfaces it:

- Open with the fact used: "It's given that ...". Each step is "Substituting
  2 for x in ... yields ...", "Subtracting 9 from both sides ... yields ...",
  "It follows that ...", "Therefore, ...".
- State the principle before applying it ("A quadratic equation in the form
  ax² + bx + c = 0 ... has exactly one solution when the discriminant ... is
  equal to zero").
- Finish with the answer in the stem's terms ("Therefore, the other tree is
  4 feet tall").
- Add "Alternate approach:" when a second method is natural (the samples do
  this for the exponential SPR).
- Then a "Distractor" paragraph naming each wrong choice's mistake.

## 9. Originality

Every item is written from scratch. The framework's sample questions, the
Question Bank, Bluebook tests and Khan Academy items are College Board
content and may not be reused, paraphrased, re-numbered or used as a template
with the same structure and a new context. Matching a *skill* and these
*conventions* is the goal; matching a published item's setup is a defect. If
you read a published item to learn the skill, close it before writing, and
note in `provenance.notes` that the item was written without reference to any
published item.

## 10. Do / don't checklist

Do
- [ ] Tag with one of the four domains and one of the 19 exact skill names.
- [ ] Put a single equation on its own line and call it "the given equation".
- [ ] Declare every constant with a "where ... is a (positive) constant" clause
      that makes the key unique.
- [ ] Say "in the xy-plane" for any graph, point or intersection.
- [ ] Put units and rounding in the question sentence ("in inches",
      "to the nearest tenth").
- [ ] Keep context stems at or under 50 words; define each variable with its
      unit; invent generic contexts.
- [ ] Order numeric choices monotonically; build verbal choices from one
      template; make each distractor a named mistake.
- [ ] Give SPR items a key that fits 5 (or 6) characters as a fraction or a
      decimal; say "one possible value" when there are several.
- [ ] Caption figures "Note: Figure not drawn to scale." only when they are
      not, and only in that wording.
- [ ] Write `byHand` in the "It's given that ... yields ... Therefore" voice
      with a distractor paragraph.
- [ ] Plan batches at 35/35/15/15, ≈3 MC : 1 SPR, ≈30% in context, SPR in
      every domain.

Don't
- [ ] Don't reuse, paraphrase or re-skin any College Board item, including
      the framework's samples.
- [ ] Don't use "you", names of people, real companies, or topic knowledge
      the student would need to know in advance.
- [ ] Don't put the unit only in the choices, or put a %, $ or unit into an
      SPR key.
- [ ] Don't leave two valid roots when one is wanted; restrict the constant.
- [ ] Don't write "none of the above", two choices equal in different forms,
      or distractors that no plausible mistake produces.
- [ ] Don't restate in the stem what the figure already shows, and don't
      draw a figure for an item that words describe fully.
- [ ] Don't hand the student a formula from the reference sheet in the stem.
- [ ] Don't mix ascending and descending within one item's choices, or let
      the key sit in the same position across a batch.
