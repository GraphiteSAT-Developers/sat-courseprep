import type { TechniqueId } from "./types";
import type { Technique } from "./technique-types";

// The thirteen Desmos moves from research_notes/.../desmos_techniques.md and the
// "Thirteen Desmos moves" table in reports/AI Desmos SAT math course plan.md.
//
// Everything here comes from those notes. The notes themselves were built from
// search-result summaries of prep-company blogs (the only official sources are
// the College Board Desmos PDF and the Desmos Help Center), so each entry
// carries `caveats` for anything contested, third-party-only, or not yet
// checked in the College Board build. `verified` is false everywhere until the
// headless verification service has run the lines with COLLEGE_BOARD_OPTIONS.
//
// desmosLines use angle-bracket placeholders (<left side>) for the part an
// item fills in. Lines with no placeholder are complete and typeable as-is.

const SHARED_PREFLIGHT = [
  "Zoom out (or zoom to fit) before concluding that something is missing or has no solution.",
  "Check parentheses and signs against the question, then re-read the variable names.",
  "Decide whether the answer must be exact (fraction) or a decimal is enough before reading it off.",
];

const techniques: Technique[] = [
  {
    id: "T1",
    name: "Graph both sides, read intersection or zeros",
    summary:
      "Solve any one-variable equation by graphing each side as y = ... and clicking the intersection, or by moving everything to one side and reading the x-intercepts.",
    domains: ["algebra", "advanced-math"],
    skills: [
      "Linear equations in one variable",
      "Nonlinear equations in one variable and systems of equations in two variables",
      "Nonlinear functions",
    ],
    triggerConditions: [
      "What is the solution to the equation ...",
      "What value of x satisfies ...",
      "What is the positive (or negative) solution to ...",
      "An equation in one variable with messy coefficients, fractions, radicals, or absolute values",
      "How many solutions does the equation ... have",
    ],
    desmosLines: ["y=<left side>", "y=<right side>"],
    readOff:
      "Click the gray intersection point and read its x-coordinate. Alternatively type <left side>-<right side>=0 as a single line y=<left side>-<right side> and click each x-intercept.",
    pitfalls: [
      "An intersection can be off-screen. Zoom out before concluding there is no solution (\"many SAT traps are just 'you didn't zoom'\").",
      "Zooming too far in loses context and can hide a second crossing.",
      "Reading an approximate value as exact. 0.667 on screen may be 2/3.",
      "Missing parentheses or a sign error when typing a side changes the equation.",
    ],
    byHand: {
      method: "Isolate x by inverse operations, or factor and set each factor to zero.",
      whenFaster: "Whenever the equation can be solved in under about 15 seconds by hand (simple linear, clean factoring). Also for SPR items that need an exact fraction the graph can only approximate.",
    },
    defaultRoute: "desmos-primary",
    preflight: SHARED_PREFLIGHT,
    verified: false,
    sources: [
      "https://acely.com/sat-prep/desmos-cheat-sheet",
      "https://www.cheetahprep.com/desmos/system-linear-equations-infinite",
      "https://www.oneprep.co/blog/sat-math-tips-desmos-2026-12-calculator-moves",
      "https://miyagilabs.ai/blog/desmos-sat-tips-guide",
    ],
  },
  {
    id: "T2",
    name: "Systems by intersection",
    summary:
      "Type both equations of a system and click the intersection point to read (x, y). Overlapping graphs mean infinitely many solutions; parallel lines that never touch mean none.",
    domains: ["algebra", "advanced-math"],
    skills: [
      "Systems of two linear equations in two variables",
      "Nonlinear equations in one variable and systems of equations in two variables",
    ],
    triggerConditions: [
      "The solution to the system of equations is (x, y). What is ...",
      "Two equations given together, each in x and y",
      "How many solutions does the system have",
      "A line and a parabola or circle given together",
      "What is the value of x + y (or xy, or x - y) for the solution of the system",
    ],
    desmosLines: ["<equation 1>", "<equation 2>"],
    readOff:
      "Click the gray intersection point(s) and read (x, y). Count the points for \"how many solutions\". If the graphs lie on top of each other, the system has infinitely many solutions; if they are parallel and never meet, none.",
    pitfalls: [
      "Intersections can be off-screen. Zoom out before counting.",
      "A line tangent to a parabola looks like a crossing at normal zoom. Zoom in to confirm one point versus two.",
      "The question often asks for a combination (x + y, 2x) rather than x or y. Read both coordinates and compute.",
    ],
    byHand: {
      method: "Elimination (add or subtract multiples of the equations) or substitution.",
      whenFaster: "When the coefficients are small integers and elimination takes one step, or when the question asks for x + y and adding the equations gives it directly.",
    },
    defaultRoute: "desmos-primary",
    preflight: SHARED_PREFLIGHT,
    verified: false,
    sources: [
      "https://thetestadvantage.com/blog/systems-of-equations-on-desmos-sat-math-shortcut-guide",
      "https://www.cheetahprep.com/desmos/system-linear-equations-infinite",
    ],
  },
  {
    id: "T3",
    name: "Sliders for unknown constants in systems",
    summary:
      "For \"for what value of k does the system have no / infinitely many / exactly one solution\", type the equations with the unknown letter, accept the slider, and drag until the graphs are parallel, coincide, or are tangent. The notes mark this move as contested; the hand method (coefficient ratios) is primary.",
    domains: ["algebra", "advanced-math"],
    skills: [
      "Systems of two linear equations in two variables",
      "Nonlinear equations in one variable and systems of equations in two variables",
      "Linear equations in two variables",
    ],
    triggerConditions: [
      "For what value of k (or a, b, c) does the system have no solution",
      "... has infinitely many solutions",
      "... has exactly one solution",
      "A system where one or more coefficients is a letter",
      "If the system has no solution, what is the value of ...",
    ],
    desmosLines: ["<equation 1 with k>", "<equation 2>"],
    readOff:
      "Click \"add slider\" for k. Drag k until the two graphs coincide (infinitely many), become parallel (none), or just touch (exactly one). Read k from the slider; narrow the slider's range or step if the value is not landing exactly.",
    pitfalls: [
      "Slider ranges may hide the answer (default range is -10 to 10). Edit the bounds.",
      "Dragging gives an approximate k. Confirm by substituting or by the ratio method.",
      "Say Hello College lists parallel-line systems among the problems to avoid doing in Desmos.",
      "Two unknown constants need two sliders and are hard to tune by dragging; use the ratio method.",
    ],
    byHand: {
      method:
        "Write both equations in Ax + By = C form. Infinitely many solutions: all three ratios A1/A2, B1/B2, C1/C2 equal. No solution: A1/A2 = B1/B2 but not C1/C2. Exactly one: A1/A2 differs from B1/B2. Example: ax + 4y = 12 and 6x + by = 18 coincide when every ratio equals 12/18 = 2/3, so a = 4 and b = 6. Then graph to confirm the overlap. For a line and a parabola, set them equal and use the discriminant.",
      whenFaster: "Almost always for linear systems: the ratio comparison takes under 15 seconds and gives an exact value. Use the slider to confirm or when the structure is unclear.",
    },
    defaultRoute: "hand-primary",
    preflight: [
      ...SHARED_PREFLIGHT,
      "After reading k from the slider, type it back into the equations (or run the ratio check) to confirm it is exact.",
    ],
    caveats: [
      "Contested in the notes: The Test Advantage, Aniko and Edison OS teach sliders for this; Say Hello College advises avoiding Desmos for parallel-line systems. The course teaches ratios first and uses Desmos to confirm.",
      "The exact slider UI (bounds and step controls) in the College Board build was not verified in the notes.",
    ],
    verified: false,
    sources: [
      "https://thetestadvantage.com/blog/sat-infinite-solutions-systems-on-desmos-may-2026-full-guide",
      "https://sayhellocollege.com/blog/guide-to-using-the-desmos-sat-calculator/",
      "https://www.aniko.ai/free-resources/sat/courses/desmos/how-many-solutions",
      "https://www.edisonos.com/digital-sat/desmos-guide",
    ],
  },
  {
    id: "T4",
    name: "Sliders, general",
    summary:
      "Any undefined letter in an expression (y = mx + b, y = a(x - h)^2 + k) prompts Desmos to offer a slider. Drag it to explore how a parameter changes the graph or to count solutions as a parameter varies.",
    domains: ["algebra", "advanced-math"],
    skills: [
      "Linear functions",
      "Nonlinear functions",
      "Nonlinear equations in one variable and systems of equations in two variables",
    ],
    triggerConditions: [
      "For what values of c does the equation have two real solutions",
      "How many solutions does ... have, where k is a constant",
      "Which of the following could be the graph of ... for some positive a",
      "A parameter whose sign or size the question asks about",
      "Describe the effect of changing a constant on the graph",
    ],
    desmosLines: ["<expression with parameter a>"],
    readOff:
      "Click \"add slider\" for each letter. Drag the slider and watch the graph; count intersections or x-intercepts for solution-count questions. Edit the slider bounds and step when the default range is too narrow.",
    pitfalls: [
      "Slider ranges may hide the answer. The default bounds are narrow; set them to cover the plausible values.",
      "Multi-letter names are parsed as products (ab is a times b), so use single letters or subscripts (a_1).",
      "Sliders give an approximate boundary value; find the exact boundary by hand (discriminant) once the picture is clear.",
    ],
    byHand: {
      method: "Discriminant reasoning (b^2 - 4ac > 0, = 0, < 0) for quadratics; sign and magnitude reasoning for transformations.",
      whenFaster: "When the question asks for the exact boundary value of the parameter, or when the discriminant is a one-line computation.",
    },
    defaultRoute: "either",
    preflight: SHARED_PREFLIGHT,
    caveats: [
      "The implicit-multiplication parsing (ab = a times b, use a_1) comes from background knowledge in the notes, not a fetched source. Test it in the College Board build.",
    ],
    verified: false,
    sources: [
      "https://www.edisonos.com/digital-sat/desmos-guide",
      "https://www.aniko.ai/free-resources/sat/courses/desmos/how-many-solutions",
    ],
  },
  {
    id: "T5",
    name: "Table regression (line or curve of best fit)",
    summary:
      "Put the data in a table with columns x_1 and y_1, then type a model with ~ in place of =. Desmos fits the parameters and stores them as variables.",
    domains: ["algebra", "psda", "advanced-math"],
    skills: [
      "Two-variable data: models and scatterplots",
      "Linear functions",
      "Linear equations in two variables",
      "Nonlinear functions",
    ],
    triggerConditions: [
      "A line of best fit, or a line that passes through the given points",
      "A table of values and an equation that models the data",
      "Which equation represents the linear (or exponential) relationship shown",
      "The function f is defined by ... and f(1) = ..., f(2) = ... (points given, model form known)",
      "Find the slope and y-intercept of the line through two points",
    ],
    desmosLines: ["x_1=[<x values>]", "y_1=[<y values>]", "y_1\\sim mx_1+b", "y_1\\sim ab^{x_1}"],
    readOff:
      "Read the fitted parameters (m, b, or a, b) listed under the regression line. Use the linear line for a line and the exponential line for growth or decay; delete the one you do not need.",
    pitfalls: [
      "Regression needs at least 2 points. With one point and a slope, type the formula by hand instead.",
      "Omitting the subscript (x instead of x_1) breaks the link to the table.",
      "The College Board version turns on Log Mode automatically for applicable exponential, logarithmic and power regressions, so the fitted parameters can differ from a least-squares fit when the data are not exact.",
      "Don't retype the rounded decimals Desmos shows. Reference m and b directly, since Desmos stores more digits.",
    ],
    byHand: {
      method: "Slope formula m = (y2 - y1)/(x2 - x1), then b = y - mx with one point. For exponentials, the ratio of consecutive outputs gives the base.",
      whenFaster: "Two clean points: the slope formula takes under 15 seconds. Use regression when there are three or more points, or when the model is exponential or quadratic.",
    },
    defaultRoute: "desmos-primary",
    preflight: [
      ...SHARED_PREFLIGHT,
      "Confirm the model form (linear vs exponential vs quadratic) matches the question before reading parameters.",
      "Check that the table columns are x_1 and y_1 and the regression uses the same subscripts.",
    ],
    caveats: [
      "The exponential form y_1 ~ a b^{x_1} is shown in a shared Desmos graph in the notes, not in an official regression article; the official Help Center regression page could not be fetched.",
      "The one-click regression button next to a table (SuperTutorTV, ~2024) is unverified in the current Bluebook build.",
    ],
    verified: false,
    sources: [
      "https://www.edisonos.com/digital-sat/desmos-guide",
      "https://desmos.com/calculator/vrhmsznixn?lang=de",
      "https://www.desmos.com/assessment-pdfs/CollegeBoard_Desmos_Calculator.pdf",
      "https://thetestadvantage.com/blog/how-to-use-desmos-on-the-sat-complete-may-2026-guide",
      "https://pursu.io/guide/sat-regression-questions-solved-the-5-desmos-tricks-to-find-constraints-line-of-best-fit",
      "https://learndesmos.com/curriculum/regression",
      "https://regressiontrainer.org/",
    ],
  },
  {
    id: "T6",
    name: "Tilde trick: find the constants in an identity",
    summary:
      "For \"for all x, (expression) = (expression with unknown a, b, c)\", replace = with ~ and x with x_1, then supply a list of test values for x_1 with at least as many values as unknowns. Desmos solves for the constants.",
    domains: ["advanced-math", "algebra"],
    skills: ["Equivalent expressions", "Nonlinear functions", "Linear equations in one variable"],
    triggerConditions: [
      "For all values of x, ... = ..., where a, b and c are constants. What is the value of ...",
      "The expression ... is equivalent to ..., where k is a constant",
      "Which expression is equivalent to ...",
      "If ... is rewritten in the form ..., what is the value of ...",
      "An identity in x with letters on one side",
    ],
    desmosLines: ["x_1=[1,2,3]", "<left side in x_1>\\sim<right side in x_1 with a,b,c>"],
    readOff:
      "Read a, b, c from the parameters listed under the regression line. Worked example from the notes: (5x_1-17)(4x_1-c) ~ ax_1^2+bx_1+119 with x_1=[2,3,4] gives c = 7, a = 20, b = -103, which expands to 20x^2 - 103x + 119.",
    pitfalls: [
      "Leaving out the x_1 list fails silently: Desmos reports nothing useful. The setup line is required.",
      "Use at least as many test values as there are unknown constants.",
      "Regression returns only one solution. If the identity has two valid constant sets, Desmos shows one.",
      "The constants must actually be constant; a letter that depends on x will not fit.",
      "Don't retype the rounded decimals Desmos shows. Reference the parameter names.",
      "Every x in the question must become x_1, including inside the right-hand side.",
    ],
    byHand: {
      method: "Expand both sides and match coefficients term by term, or substitute convenient x values (x = 0, 1, -1) to get equations in the constants. For \"which expression is equivalent\", graph both as y = ... and look for exact overlap.",
      whenFaster: "When matching one coefficient (the constant term, the leading term) answers the question directly, or when the expression is a two-term expansion.",
    },
    defaultRoute: "either",
    preflight: [
      ...SHARED_PREFLIGHT,
      "Confirm the x_1 list line is present and has at least as many values as unknowns.",
      "Confirm = was replaced by ~ and every x by x_1.",
      "Confirm the fitted constants are near-integers before answering; a non-integer suggests a typo.",
    ],
    caveats: [
      "Sourced from a single prep-company guide (Resolve Prep) plus LearnDesmos and Pursu coverage; the official Help Center regression article was not fetched.",
      "Behavior when the fit is exact (residuals zero) in the College Board build's Log Mode default is untested.",
    ],
    verified: false,
    sources: [
      "https://resolveprep.com/blog/desmos-regression-sat-guide",
      "https://resolveprep.com/blog/key-desmos-features",
      "https://learndesmos.com/curriculum/regression",
    ],
  },
  {
    id: "T7",
    name: "Lists and statistics",
    summary:
      "Enter data as a list in square brackets and apply mean, median, min, max, quartile, quantile, stdev (sample) or stdevp (population).",
    domains: ["psda"],
    skills: ["One-variable data: distributions and measures of center and spread"],
    triggerConditions: [
      "What is the mean (median, range, standard deviation) of the data",
      "A data set listed as numbers, a dot plot, a frequency table",
      "Which data set has the greater standard deviation",
      "By how much does the mean change if a value is added or removed",
    ],
    desmosLines: [
      "L=[<values>]",
      "\\operatorname{mean}(L)",
      "\\operatorname{median}(L)",
      "\\operatorname{max}(L)-\\operatorname{min}(L)",
      "\\operatorname{stdev}(L)",
      "\\operatorname{stdevp}(L)",
    ],
    readOff:
      "Read the value shown to the right of each statistic line. For a frequency table, repeat each value as many times as its frequency in the list.",
    pitfalls: [
      "Curly braces mean a restriction, not a list: L = {4, 7} builds no list and the statistics come back blank. Use square brackets.",
      "stdev is the sample standard deviation and stdevp the population one. The SAT rarely needs the number itself, but if it does, check which one the question means.",
      "Frequency tables must be expanded (each value repeated) before the statistics are right.",
    ],
    byHand: {
      method: "Mean = sum / count; median = middle value of the sorted list; range = max - min. For \"what happens to the mean/median\" questions, reason about the effect without computing.",
      whenFaster: "Conceptual questions (\"which is larger, the mean or the median\", \"how does removing the outlier affect ...\") and small lists of five or fewer values.",
    },
    defaultRoute: "either",
    preflight: [
      ...SHARED_PREFLIGHT,
      "Confirm the list uses [ ] not { } and the count of entries matches the data.",
      "Confirm sample vs population SD if the question asks for a number.",
    ],
    caveats: [
      "The {} vs [] pitfall is a third-party claim (Learner Labs) not confirmed on the Help Center page.",
      "The notes list `quartile` and `quantile` as official functions but do not describe the SAT use or exact argument order; verify before teaching.",
    ],
    verified: false,
    sources: [
      "https://help.desmos.com/hc/en-us/articles/212235786-Supported-Functions",
      "https://desmos.s3.amazonaws.com/Desmos_User_Guide.pdf",
      "https://learnerlabs.app/sat-prep/desmos/stats-from-list",
    ],
  },
  {
    id: "T8",
    name: "Inequality shading",
    summary:
      "Type each inequality and Desmos shades it. Strict inequalities get a dashed boundary, inclusive ones a solid boundary, and the darker overlap is the solution set of a system.",
    domains: ["algebra"],
    skills: ["Linear inequalities in one or two variables"],
    triggerConditions: [
      "Which point (x, y) is a solution to the system of inequalities",
      "Which of the following ordered pairs satisfies ...",
      "Which graph represents the system of inequalities",
      "A system of two or more inequalities in x and y",
      "For how many integer values of x is the inequality true",
    ],
    desmosLines: ["y\\le<expression>", "y>-<expression>", "(<x>,<y>)"],
    readOff:
      "Look for the region where every shading overlaps (darkest). Plot the candidate point as (x, y) and check that it lands inside the overlap; a point on a dashed boundary is not a solution.",
    pitfalls: [
      "Overlapping colors can mislead. Confirm with a test point rather than trusting the shade.",
      "Dashed boundary (strict) versus solid (inclusive) matters for points on the line.",
      "Typing <= or >= auto-converts to the symbol; a stray = after < can mean something else.",
      "The overlap may be far from the origin. Zoom out.",
    ],
    byHand: {
      method: "Substitute each answer choice into every inequality and keep the one that satisfies all. For \"which graph\", check the y-intercept and slope direction and whether (0, 0) satisfies each inequality.",
      whenFaster: "When the choices are four ordered pairs and substituting takes a few seconds each, or when the inequalities are simple enough to test (0, 0) mentally.",
    },
    defaultRoute: "either",
    preflight: [
      ...SHARED_PREFLIGHT,
      "Confirm each inequality's direction and strictness matches the question (dashed vs solid).",
    ],
    verified: false,
    sources: [
      "https://www.effortlessmath.com/blog/desmos-sat-math-cheat-sheet-12-moves/",
      "https://bwseducationconsulting.com/wp-content/uploads/2024/07/Desmos_SAT_Tips_and_Tricks.pdf",
    ],
  },
  {
    id: "T9",
    name: "Define and evaluate functions",
    summary:
      "Define f(x) = ... on one line, then evaluate f(3), f(g(2)) or f(x+1) on later lines. Desmos shows the numeric value beside the line.",
    domains: ["algebra", "advanced-math"],
    skills: ["Linear functions", "Nonlinear functions", "Equivalent expressions"],
    triggerConditions: [
      "The function f is defined by ... What is the value of f(3)",
      "If g(x) = f(x + 2), what is g(1)",
      "Composition: f(g(x)), f(f(2))",
      "For which value of x is f(x) = 0 (combine with T1)",
      "A function given by an equation and a specific input asked for",
    ],
    desmosLines: ["f(x)=<expression>", "f(<input>)"],
    readOff:
      "Read the value shown to the right of the evaluation line. For a table of inputs, type f(x_1) next to a column x_1 to fill a column of outputs.",
    pitfalls: [
      "Variable-name collisions: a slider named a or a list named L defined earlier changes the meaning of the function.",
      "Desmos reserves some names (e.g. e, pi); a function named with a multi-letter name is parsed as a product.",
      "Missing parentheses around a composite input (f(x+1) vs f(x)+1).",
    ],
    byHand: {
      method: "Direct substitution, then arithmetic.",
      whenFaster: "Nearly always for a single clean evaluation like f(3) with small integers. Desmos wins for composition, messy decimals, or when the same function is evaluated many times.",
    },
    defaultRoute: "either",
    preflight: [
      ...SHARED_PREFLIGHT,
      "Confirm no earlier line redefines a letter used inside the function.",
    ],
    verified: false,
    sources: ["https://www.edisonos.com/digital-sat/desmos-guide"],
  },
  {
    id: "T10",
    name: "Circles from expanded form",
    summary:
      "Graph the expanded circle equation directly; Desmos draws it without completing the square. Click the curve to see the top and bottom points; the center is their midpoint and the radius half their distance. The notes mark this move as contested; completing the square is primary.",
    domains: ["geometry-trig"],
    skills: ["Circles"],
    triggerConditions: [
      "The equation x^2 + y^2 + Dx + Ey + F = 0 represents a circle. What is the center (or radius)",
      "Which equation represents a circle with center ... and radius ...",
      "A circle whose diameter has endpoints ... What is the equation",
      "Where does the circle intersect the line (or the axis) (combine with T2)",
    ],
    desmosLines: [
      "x^2+y^2-6x+4y-3=0",
      "A=(<x1>,<y1>)",
      "B=(<x2>,<y2>)",
      "\\operatorname{midpoint}(A,B)",
      "\\operatorname{distance}(A,B)/2",
    ],
    readOff:
      "Click the circle; gray dots appear at the top and bottom. Center = midpoint of those two points, radius = half the distance between them. Example from the notes: x^2+y^2-6x+4y-3=0 has center (3, -2) and radius 4. For diameter endpoints A and B, midpoint(A,B) is the center and distance(A,B)/2 the radius.",
    pitfalls: [
      "Desmos does not reliably mark the leftmost and rightmost points; use top and bottom.",
      "Reading the center by eye from the grid is error-prone. Use the gray points or the midpoint formula.",
      "Say Hello College lists center/radius of circles among problems to avoid in Desmos.",
      "The radius read off the graph is approximate; the answer often needs the exact value or r^2.",
    ],
    byHand: {
      method: "Complete the square in x and in y: (x - h)^2 + (y - k)^2 = r^2. For diameter endpoints, center = midpoint, radius = half the distance.",
      whenFaster: "Almost always for a single circle: completing the square is two short steps and gives exact values. Use Desmos to confirm, or when the circle meets a line and the intersection is asked.",
    },
    defaultRoute: "hand-primary",
    preflight: [
      ...SHARED_PREFLIGHT,
      "Confirm the equation has equal x^2 and y^2 coefficients (otherwise it is not a circle).",
      "If the question asks for r^2 or the exact radius, compute it by hand rather than reading a decimal.",
    ],
    caveats: [
      "Contested in the notes: Pursu, Learner Labs and Aniko teach it; Say Hello College says avoid. The course teaches completing the square first.",
      "Whether clicking the curve reliably exposes the top and bottom points in the College Board build is a third-party claim; verify.",
      "midpoint() and distance() are reported by Learner Labs; confirm they are enabled in the College Board build.",
    ],
    verified: false,
    sources: [
      "https://pursu.io/guide/sat-circles-made-easy-7-ways-to-solve-geometry-problems-using-desmos-with-examples",
      "https://learnerlabs.app/sat-prep/desmos/circles",
      "https://www.aniko.ai/free-resources/sat/courses/desmos/circle-equations-in-the-graph",
      "https://sayhellocollege.com/blog/guide-to-using-the-desmos-sat-calculator/",
    ],
  },
  {
    id: "T11",
    name: "Exact vs decimal answers",
    summary:
      "Use the fraction toggle beside a numeric result to convert a decimal to an exact fraction (5.125 becomes 41/8), and store exact values in variables so later lines do not accumulate rounding error. Decide before answering whether the SPR box needs an exact value.",
    domains: ["algebra", "advanced-math", "psda", "geometry-trig"],
    skills: [
      "Linear equations in one variable",
      "Nonlinear equations in one variable and systems of equations in two variables",
      "Ratios, rates, proportional relationships, and units",
      "Percentages",
    ],
    triggerConditions: [
      "Any student-produced response (SPR) item",
      "A result on screen that is a repeating or long decimal (0.6667, 0.8333)",
      "The answer must be entered as a fraction or decimal",
      "A follow-up computation that reuses an earlier result",
    ],
    desmosLines: ["r=<expression>", "r"],
    readOff:
      "Click the fraction toggle next to the value to see the exact form. Give later lines the variable name (r) rather than the rounded decimal. For SPR: enter the fraction, or a decimal filling the full box (5 characters positive, 6 negative, minus sign counted). 0.67 for 2/3 is marked wrong.",
    pitfalls: [
      "Reading an approximate value as exact.",
      "Retyping a rounded decimal into a later line and compounding the error.",
      "Rounding an SPR decimal too coarsely: .67 for 2/3 earns no credit; .6667 or 2/3 does.",
      "Mixed numbers are not accepted; enter an improper fraction or a decimal.",
    ],
    byHand: {
      method: "Solve algebraically to get the exact fraction, then simplify or convert for the answer box.",
      whenFaster: "When a Desmos result is a messy decimal and the fraction toggle gives a surprising denominator: re-derive by hand to confirm. One source recommends by-hand for free-response exactness as the default.",
    },
    defaultRoute: "either",
    preflight: [
      ...SHARED_PREFLIGHT,
      "Check whether the item is SPR and apply the 5/6-character rule before typing the answer.",
    ],
    caveats: [
      "The fraction toggle and \"store exact values in variables\" come from a single prep blog (LearnQ). Whether the toggle appears for every numeric line in the College Board build is unverified.",
    ],
    verified: false,
    sources: [
      "https://blogs.learnq.ai/math-calcutor-desmos-digital-sat/",
      "https://sherpalai.com/sat-r-desmos-calculator-tips/sat-math-desmos-cheat-sheet",
    ],
  },
  {
    id: "T12",
    name: "Trig with angle mode",
    summary:
      "Before any trig evaluation, check whether the calculator is in degrees or radians and switch to match the question. Wrong angle mode is the most common and costly trig error.",
    domains: ["geometry-trig"],
    skills: ["Right triangles and trigonometry"],
    triggerConditions: [
      "sin, cos or tan of a given angle",
      "An angle given in degrees (with the degree symbol) or in radians (with pi)",
      "Convert between degrees and radians",
      "A right triangle with a side and an angle given",
      "The value of sin(x) equals cos(90 - x) style identities",
    ],
    desmosLines: ["\\sin(<angle>)", "\\cos(<angle>)", "\\tan(<angle>)"],
    readOff:
      "Open the settings (wrench) and confirm Degrees or Radians before reading. Read the value beside the line. For an exact value, use the fraction toggle (T11) or recall the special angle.",
    pitfalls: [
      "Wrong angle mode (radians vs degrees) silently gives a wrong number.",
      "Most SAT trig questions are about ratios in a right triangle or the complementary-angle identity, where the calculator adds nothing.",
      "A decimal like 0.866 should be recognized as sqrt(3)/2 when an exact answer is needed.",
    ],
    byHand: {
      method: "Special right triangles (30-60-90, 45-45-90), SOH-CAH-TOA, the unit circle, and sin(x) = cos(90 - x).",
      whenFaster: "Nearly always: SAT trig is reasoning about ratios and complementary angles, not evaluation. Use Desmos only to check a numeric value or to convert units.",
    },
    defaultRoute: "hand-primary",
    preflight: [
      "Angle mode: Degrees or Radians, matching the question.",
      ...SHARED_PREFLIGHT,
    ],
    caveats: [
      "The notes record the pitfall (angle mode) but no sourced Desmos trig worked example for the SAT. Where the angle-mode setting lives in the College Board build's UI was not verified.",
    ],
    verified: false,
    sources: [
      "https://miyagilabs.ai/blog/desmos-sat-tips-guide",
      "https://acely.com/sat-prep/desmos-cheat-sheet",
    ],
  },
  {
    id: "T13",
    name: "Graph or plug in answer choices",
    summary:
      "For multiple choice, type each answer choice into Desmos (as a graph or a value) and eliminate the ones that do not match the condition in the question.",
    domains: ["algebra", "advanced-math", "psda", "geometry-trig"],
    skills: [
      "Equivalent expressions",
      "Nonlinear functions",
      "Linear functions",
      "Linear inequalities in one or two variables",
      "Systems of two linear equations in two variables",
    ],
    triggerConditions: [
      "Which of the following is equivalent to ...",
      "Which equation (or graph) represents ...",
      "Which of the following could be the value of ...",
      "Which ordered pair satisfies ...",
      "Multiple choice where the choices are expressions, equations or specific numbers",
    ],
    desmosLines: ["y=<original expression>", "y=<choice A>", "y=<choice B>", "y=<choice C>", "y=<choice D>"],
    readOff:
      "The choice whose graph lies exactly on top of the original (or whose value satisfies the condition) is the answer. Toggle lines off one at a time to see which one coincides. For numeric choices, substitute each into the condition and read true/false or the value.",
    pitfalls: [
      "Slow when all four choices must be tested. Start with the most likely choice, or narrow by hand first.",
      "Two graphs can look coincident at one zoom level but differ elsewhere. Zoom out and in.",
      "A typo in one choice makes the wrong one look right. Retype carefully, or copy the original line and edit.",
      "Only works for multiple choice; SPR needs a direct method.",
    ],
    byHand: {
      method: "Estimation and elimination: rule out choices by sign, size, degree or a quick substitution of x = 0 or x = 1.",
      whenFaster: "When one quick substitution (x = 0) separates the choices, or when the choices differ by sign only.",
    },
    defaultRoute: "either",
    preflight: SHARED_PREFLIGHT,
    verified: false,
    sources: [
      "https://www.strategictestprep.com/post/6-desmos-hacks-to-boost-your-sat-math-score",
      "https://sherpalai.com/sat-r-desmos-calculator-tips/sat-math-desmos-cheat-sheet",
    ],
  },
];

export function listTechniques(): Technique[] {
  return techniques;
}

export function getTechnique(id: TechniqueId): Technique | undefined {
  return techniques.find((t) => t.id === id);
}
