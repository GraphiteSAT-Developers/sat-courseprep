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

## Tutor API

A tutor or host page can read the calculator, and write to it when needed, through `window.topline`. Every value it returns is plain JSON. Non-finite numbers become `null`, points become `{x, y}` and complex numbers become `{re, im}`.

```js
const t = window.topline;                      // t.version is the API version
t.setExpressions(['f(x)=x^2-5x+6', 'f(3)']);   // replaces every line; returns the new ids
t.analyze();
// [{id, latex: 'f(x)=x^2-5x+6', type: 'expression', kind: 'fdef', name: 'f', value: null, error: null, missing: [], regression: null},
//  {id, latex: 'f(3)', kind: 'val', value: 0, ...}]
// A line like y_1\sim mx_1+b gets regression: {params: {m, b}, r2, rmse, n}; an undefined letter gives error plus missing: ['k'].
t.evaluate('f(5)');                            // {value: 6, error: null, missing: []}, and no line is added
const off = t.onChange(({ state, analysis }) => { /* ... */ });  // after any edit by the student or the API, debounced 100 ms
```

- `getState()` and `setState(state)` read and replace the whole calculator: lines, settings and view, in the same shape that is saved to local storage. `setState` checks its input and throws if the input is invalid.
- `getExpressions()` returns `[{id, latex, type}]`. `type` is `expression`, `note` or `table`, and a table also carries `table: {cols: [{name, cells}]}`.
- `setExpression({id?, latex, hidden?, color?, slider?})` updates the line with that id, keeping any fields you leave out, or adds a new line. It returns the id. `removeExpression(id)` returns `false` if there is no such line. Unlike Desmos, `setExpressions(list)` replaces every line. Ids are numbers that stay the same until the next `setState` or reload.
- `analyze()` uses these `kind` values: `val` (value), `vdef` (variable), `fdef` (function), `yx`/`xy`/`imp` (graphs), `reg`, `table`, `note` and `err`.
- `getSettings()` and `setSettings({degrees, complex, logX, logY, theme})` read and change the settings. `theme` is `'light'`, `'dark'` or `null`, which follows the system.

**Inside an iframe.** Send `{source: 'topline-host', id, method, args}` to the frame. `args` is an array of arguments, and every method above except `onChange` is available. The frame replies to the sender with `{source: 'topline', id, result}` or `{source: 'topline', id, error}`. When the frame is embedded, it also posts `{source: 'topline', event: 'change', state, analysis}` to `window.parent` after each change.

```js
frame.contentWindow.postMessage({ source: 'topline-host', id: 1, method: 'analyze', args: [] }, '*');
addEventListener('message', e => { if (e.data?.source === 'topline') console.log(e.data); });
```

By default the frame answers messages from any origin. Use `index.html?allowOrigin=https://tutor.example.com,https://other.example.com` to answer only those origins. Change events then go to the only allowed origin, or, when several are allowed, to whichever of them last messaged the frame.

## Notes

- Fonts load from Google Fonts. Everything else is inline in the one file.
- Tap a curve on the graph to trace it. Select any curve, including circles and lines like `3x + 2y = 12`, to see its intercepts, extremes, and intersections with the other curves (touching points included).
- `node tests/engine-check.js` runs the math engine in Node on SAT-style inputs written the way Desmos stores them.
- `node tests/api-check.js` tests the tutor API and the iframe bridge in headless Chromium. It needs Playwright, loaded from `/opt/node-tools/node_modules/playwright`.
