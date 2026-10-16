// Runs Topline's math engine in Node (no browser) against SAT-style Desmos inputs.
// Usage: node topline/tests/engine-check.js
// Each case is a list of lines, typed the way Desmos stores them, and the value expected from the last line.
// A case with `error: true` expects the last line to fail.
const fs = require('fs');
const path = require('path');

const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const m = /\/\/ == ENGINE START ==([\s\S]*)\/\/ == ENGINE END ==/.exec(html);
if (!m) throw new Error('Engine markers not found in index.html');
const E = new Function(`${m[1]}; return { analyzeAll, setMode: (d, c) => { DEG = d; COMPLEX = c; } };`)();

const CASES = [
  // T1/T9 functions and evaluation
  { name: 'evaluate f(3)', lines: ['f\\left(x\\right)=2x+5', 'f\\left(3\\right)'], want: 11 },
  { name: 'composition', lines: ['f(x)=2x+5', 'f(f(1))'], want: 19 },
  { name: 'zero check', lines: ['f(x)=x^2-5x+6', 'f(3)'], want: 0 },
  // vertex form: a letter times a squared bracket
  { name: 'a(3)^2 = a*9', lines: ['a=2', 'a(3)^2'], want: 18 },
  { name: 'c(x+1)^2 in a function', lines: ['c=3', 'f(x)=c(x+1)^2', 'f(1)'], want: 12 },
  { name: 'f(x+1)^2 stays a function call', lines: ['f(x)=x^2', 'g(x)=f(x+1)^2', 'g(1)'], want: 16 },
  // T5/T6 regressions
  { name: 'linear regression slope', lines: ['x_1=[1,2,3,4,5]', 'y_1=[2.1,3.9,6.2,7.8,10.1]', 'y_1\\sim mx_1+b', 'm'], want: 1.99 },
  { name: 'exponential regression base', lines: ['x_1=[0,1,2,3]', 'y_1=[3,6,12,24]', 'y_1\\sim ab^{x_1}', 'b'], want: 2 },
  { name: 'vertex-form regression a', lines: ['x_1=[-1,0,2]', 'y_1=[6,2,6]', 'y_1\\sim a(x_1-h)^2+k', 'a'], want: 2 },
  { name: 'tilde trick c', lines: ['x_{1}=\\left[2,3,4\\right]', '\\left(5x_{1}-17\\right)\\left(4x_{1}-c\\right)\\sim ax_{1}^{2}+bx_{1}+119', 'c'], want: 7 },
  { name: 'tilde trick b', lines: ['x_1=[2,3,4]', '(5x_1-17)(4x_1-c)\\sim ax_1^2+bx_1+119', 'b'], want: -103 },
  // T7 statistics
  { name: 'mean', lines: ['L=[4,7,7,10,22]', '\\operatorname{mean}(L)'], want: 10 },
  { name: 'median', lines: ['L=[4,7,7,10,22]', '\\operatorname{median}(L)'], want: 7 },
  { name: 'stdev (sample)', lines: ['L=[3,7,8,12,15]', '\\operatorname{stdev}(L)'], want: Math.sqrt(21.5) },
  { name: 'stdevp (population)', lines: ['L=[3,7,8,12,15]', '\\operatorname{stdevp}(L)'], want: Math.sqrt(17.2) },
  { name: 'range by max-min', lines: ['L=[4,7,7,10,22]', '\\max(L)-\\min(L)'], want: 18 },
  { name: 'curly braces are not a list', lines: ['L_1=\\left\\{4,7\\right\\}'], error: true },
  // arithmetic and notation
  { name: 'fraction sum', lines: ['\\frac{3}{4}+\\frac{5}{6}'], want: 19 / 12 },
  { name: 'cube root', lines: ['\\sqrt[3]{27}'], want: 3 },
  { name: 'log base 2', lines: ['\\log_{2}(8)'], want: 3 },
  { name: 'absolute value bars', lines: ['\\left|-3\\right|'], want: 3 },
  { name: 'sum notation', lines: ['\\sum_{n=1}^{10}n'], want: 55 },
  { name: 'implicit multiplication', lines: ['a=2', 'b=3', 'ab'], want: 6 },
  { name: 'point coordinate', lines: ['A=(-2,1)', 'A.x'], want: -2 },
  { name: 'list filter', lines: ['L=[5,6,7]', '\\operatorname{length}(L[L>5])'], want: 2 },
  // Desmos syntax added for parity
  { name: 'midpoint', lines: ['A=(-2,1)', 'B=(4,9)', 'M=\\operatorname{midpoint}(A,B)', 'M.y'], want: 5 },
  { name: 'distance', lines: ['A=(-2,1)', 'B=(4,9)', '\\operatorname{distance}(A,B)'], want: 10 },
  { name: 'percent of', lines: ['20\\%\\operatorname{of}50'], want: 10 },
  { name: 'percent of binds before +', lines: ['50\\% of 20+10'], want: 20 },
  { name: 'bare percent', lines: ['15%'], want: 0.15 },
  { name: 'percent regression', lines: ['p\\% \\operatorname{of}20\\sim9', 'p'], want: 45 },
  { name: 'x1 is x_1', lines: ['x1=[1,2,3]', '\\operatorname{mean}(x_1)'], want: 2 },
  { name: 'list slice', lines: ['L=[5,6,7,8]', '\\operatorname{total}(L[2...3])'], want: 13 },
  { name: 'open list slice', lines: ['L=[5,6,7,8]', '\\operatorname{total}(L[2...])'], want: 21 },
  { name: 'degree symbol in radian mode', lines: ['\\sin(30^{\\circ})'], want: 0.5 },
  { name: 'degree symbol in degree mode', lines: ['\\sin(30°)'], want: 0.5, deg: true },
  // T12 angle mode
  { name: 'sin(30) radians', lines: ['\\sin(30)'], want: Math.sin(30) },
  { name: 'sin(30) degrees', lines: ['\\sin(30)'], want: 0.5, deg: true },
];

let fail = 0;
for (const c of CASES) {
  E.setMode(!!c.deg, false);
  const out = E.analyzeAll(c.lines.map((text, i) => ({ text, seed: i + 1 })));
  const R = out[out.length - 1];
  let ok, got;
  if (c.error) { ok = R.kind === 'err'; got = R.kind === 'err' ? `error: ${R.error}` : `no error (${R.kind})`; }
  else { got = R.kind === 'err' ? `error: ${R.error}` : R.value; ok = typeof got === 'number' && Math.abs(got - c.want) < 1e-6 * Math.max(1, Math.abs(c.want)); }
  if (!ok) fail++;
  console.log(`${ok ? 'ok  ' : 'FAIL'} ${c.name}${ok ? '' : `: got ${got}, want ${c.error ? 'an error' : c.want}`}`);
}
console.log(`\n${CASES.length - fail}/${CASES.length} passed`);
process.exit(fail ? 1 : 0);
