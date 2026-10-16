# Topline

A browser graphing calculator with a live math editor, built as a single self-contained page. Open `index.html` in a browser; there is nothing to install or build.

## What it does

- **Live math typing.** `/` makes a fraction, `^` an exponent and `_` a subscript (press → or space to leave them). `sqrt`, `pi`, `int`, `sum` and `prod` turn into √, π, ∫, Σ and Π, and `d/dx` becomes a derivative. You can type `\` commands such as `\frac` or paste LaTeX. Every line is stored as LaTeX.
- **Graphing.** Functions, `x = …` curves, implicit equations, inequalities with shading, domain restrictions like `{-2 < x < 2}`, piecewise functions, recursion, points with labels and connecting lines, and log scales.
- **Calculus.** `f'(x)`, `d/dx`, definite integrals, sums and products, and `with` substitution.
- **Lists, tables and matrices.** Ranges, filters, list comprehensions with `for`, tables (type `table` into an empty line), and det, inv, transpose, rref and trace.
- **Statistics.** Summary statistics, normal, t, binomial, Poisson and uniform distributions, t-tests, random values, histograms, dot plots and box plots.
- **Regressions.** Fits written as `y_1 ~ m x_1 + b`, or any nonlinear model, with R² and RMSE.
- **Geometry.** Points, `A.x` and `A.y`, `midpoint(A, B)` and `distance(A, B)`.
- **Desmos-style input.** `20% of 50`, `30°`, list slices like `L[2...4]`, and `x1` turning into `x₁` as you type.
- **Other.** Complex numbers, degrees or radians, an a/b toggle for results that are exact fractions, and light and dark themes. Expressions are saved in the browser's local storage.

## Notes

- Fonts load from Google Fonts. Everything else is inline in the one file.
- Tap a curve on the graph to trace it. Select any curve, including circles and lines like `3x + 2y = 12`, to see its intercepts, extremes, and intersections with the other curves (touching points included).
- `node tests/engine-check.js` runs the math engine in Node on SAT-style inputs written the way Desmos stores them.
