# Topline

A browser graphing calculator with a live math editor, built as a single self-contained page. Open `index.html` in a browser; there is nothing to install or build.

## What it does

- **Live math typing.** `/` makes a fraction, `^` an exponent and `_` a subscript (press → or space to leave them). `sqrt`, `pi`, `int`, `sum` and `prod` turn into √, π, ∫, Σ and Π, and `d/dx` becomes a derivative. You can type `\` commands such as `\frac` or paste LaTeX. Every line is stored as LaTeX.
- **Graphing.** Functions, `x = …` curves, implicit equations, inequalities with shading, domain restrictions like `{-2 < x < 2}`, piecewise functions, recursion, points with labels and connecting lines, and log scales.
- **Calculus.** `f'(x)`, `d/dx`, definite integrals, sums and products, and `with` substitution.
- **Lists, tables and matrices.** Ranges, filters, list comprehensions with `for`, tables (type `table` into an empty line), and det, inv, transpose, rref and trace.
- **Statistics.** Summary statistics, normal, t, binomial, Poisson and uniform distributions, t-tests, random values, histograms, dot plots and box plots.
- **Regressions.** Fits written as `y_1 ~ m x_1 + b`, or any nonlinear model, with R² and RMSE.
- **Other.** Complex numbers, degrees or radians, and light and dark themes. Expressions are saved in the browser's local storage.

## Notes

- Fonts load from Google Fonts. Everything else is inline in the one file.
- Tap a curve on the graph to trace it. Select a function's line to see its intercepts, extrema and intersections.
