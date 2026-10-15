# Hard-question map for the 700–800 band

_Added 2026-10-15 from a review of a commercial "150 hard questions" set (PrepPros, used as reference only; nothing copied). The value was its topic map: which question types recur at the top of the difficulty range. This page lists those types, which of them the bank covers, and the default route for each. It drives item batch 2._

Legend: **D** = Desmos-primary, **H** = hand-primary, **E** = either. "Items" counts the current bank (27 items)._

## Algebra

| Hard type | Route | Why | Items |
|---|---|---|---|
| Constant k that gives no / one / infinitely many solutions (one-variable and systems) | E | Coefficient ratios by hand (T3); slider to confirm | 2 |
| Identity true for all x: find constants | H | Match coefficients; slider only as a check | 1 |
| "Which second equation gives no solution" (choices) | E | Ratio check by hand; T13 graph each choice | 0 |
| Point that lies on both lines "for every real r" | H | Parametric substitution; T13 with a chosen r to check | 0 |
| Lines with variable coordinates, perpendicular lines with constants | H | Slope algebra; graph to confirm | 1 |
| Systems with four unknowns or sum/difference tricks (find 7(j−k)) | H | Treat (j−k) as one variable; Desmos can't name it directly | 0 |
| Linear word problem to equation, "which equation represents" | E | T13 plug numbers into choices | 1 |
| Inequalities with word problems (maximum count within budget) | D | T8 shade both constraints, read the corner | 1 |
| Interpreting a constant in a linear model | H | Conceptual; no graphing needed | 0 |

## Advanced math

| Hard type | Route | Why | Items |
|---|---|---|---|
| Discriminant with unknown constants: "greatest possible value of ac" | H | b² − 4ac ≤ 0 reasoning; a slider only illustrates | 0 |
| Tangent line / exactly one intersection with a parabola | D | T1/T4 slider until tangent; confirm by discriminant | 1 |
| Product or sum of solutions (c/a, −b/a), including constant coefficients | H | Vieta; Desmos only for a numeric check | 0 |
| Vertex form from a vertex and a point; f and 3f y-intercepts | E | Hand: a(x−h)²+k; Desmos: T6 tilde with a point list, or vertex regression | 1 |
| Function shifts: g(x) = f(x+4), y-intercept of the shifted graph | D | Define f from the table by regression (T5), then type g(x)=f(x+4) and read g(0) | 0 |
| Composite / rational function from a table of values | E | T9 define and evaluate | 0 |
| Absolute-value equation: value of k for exactly one solution, or "no solution" inequality on k | D | Graph y = a·|x−h|+c and y = k with a slider; count intersections | 0 |
| Rational exponents and radicals: solve for the exponent | H | Exponent algebra; T13 numeric check | 1 |
| Exponential through two points (c, 8) and (2c, 350): find b | E | Ratio trick by hand; Desmos regression with a chosen c | 1 |
| Equivalent exponential form that "displays" the max/min or the value at x = 2 | H | Rewrite with exponent rules; T13 to verify choices numerically | 0 |
| Exponential growth/decay rate: "p% less each step", "every 2 months" interpretation | H | Read the base; conceptual | 0 |
| Polynomial product with constants: f(x)·g(x) = 5x³ + 1715, find k | D | T6 tilde: (x+7)(5x²−kx+245) ~ 5x³+1715 with an x list | 1 |
| Factor theorem: (x+2a) is a factor, which polynomial | E | Substitute x = −2a; T13 | 0 |
| Equation with a square root and exactly one real solution | H | Square, then discriminant; graph shows extraneous roots | 0 |
| Special quadratics: (x−y)² from x² + y² and xy | H | Identity manipulation | 1 |

## Problem solving and data analysis

| Hard type | Route | Why | Items |
|---|---|---|---|
| Percent chains: "a is 480% of b, a is 70% of c, p% of b is c" | E | Set b = 100 and compute; Desmos as calculator | 1 |
| Mixing solutions / alloys (two-variable system) | D | T2 system intersection | 0 |
| Weighted averages of two data sets | H | Total = mean × count | 0 |
| Standard deviation from frequency tables: which is smallest / effect of removing extremes | H | Conceptual spread; T7 stdev only to confirm | 0 |
| Margin of error: why one sample's is smaller | H | Conceptual (sample size); no computation | 0 |
| Conditional probability from a two-way table | H | Fraction of a row or column | 1 |
| Ratios with a total split across groups | H | Parts-to-total arithmetic | 0 |
| Unit conversion with squared/cubed units (mi² to yd², m/s² to mi/min²) | H | Dimensional analysis; Desmos as calculator | 0 |
| Density and volume | H | d = m/V; Desmos as calculator | 0 |
| Regression / line of best fit from a table | D | T5 | 1 |

## Geometry and trigonometry

| Hard type | Route | Why | Items |
|---|---|---|---|
| Special right triangles (30-60-90, 45-45-90), including inscribed in circles | H | Ratios; Desmos irrelevant | 1 |
| Trig identities: sin A = cos B when A + B = 90, sin²+cos² | H | Identity; T12 numeric check in degrees | 1 |
| Coterminal angles in radians (975π/60) | H | Subtract 2π multiples; T12 in radians to check | 0 |
| Similar triangles and scale factors for area / volume / surface area | H | Ratio², ratio³ | 0 |
| Circles: completing the square to find c; point on / inside / outside | E | T10 contested; hand first | 1 |
| Arcs and inscribed angles, arc expressions in x | H | Angle arithmetic | 0 |
| Parallel lines and transversals: which equation proves parallel | H | Angle relationships | 0 |
| Polygon interior angles (97 sides) | H | 180(n−2); calculator arithmetic | 0 |
| Pyramids, prisms, cylinders: surface area from volume | E | Formula then solve; T1 to solve the equation | 1 |
| Congruent-triangle sufficiency (I, II, III) | H | Postulates; conceptual | 0 |

## What this says about the course

1. **Hand-primary dominates the hard end.** Of the ~45 recurring hard types, about 25 are hand-first. Desmos is the lead on ~10 and a tie on ~10. That matches the research estimate that Desmos solves or verifies a third to half of the test, and it means the by-hand half of the course is not a footnote.
2. **Desmos's hard-end wins are specific:** sliders for solution counting (absolute value, tangency, k-constants), tilde for polynomial constants, regression for function shifts, shading for budget inequalities, intersections for mixtures. These are the moves to teach with the most care.
3. **Two candidate techniques for the library, pending the Bluebook audit:** absolute-value solution counting with a slider (T14), and defining a function by regression and then evaluating a shifted version (T15).

## Batch 2 targets

Every type with **0** items above gets at least one original item. Priority to the Desmos-primary zeros (absolute value with slider, function shifts, mixing systems, factor-theorem plug-in) and the hand-primary zeros that mark the boundary (discriminant max, Vieta, scale factors, unit conversion, margin of error, parallel-line proofs).
