/* Graphite lesson kit: the pieces lessons.js draws hands-on steps with, and the grading the preview uses.
   - An expression reader (numbers, x, + - * / ^, brackets, 2x and 3(x + 1), sqrt, abs, pi). Never eval.
     backend/app/services/mathexpr.py is the same reader in Python; a test checks they agree.
   - right(step, answer) and grade(steps, answers): the same rules as backend/app/services/lessons.py.
   - SVG drawing: graphs, number lines, a pie for sectors and a dot plot. */
(function () {
  "use strict";
  var MAX_LEN = 60;
  var SAMPLES = [-3.7, -2.2, -1.3, -0.4, 0.6, 1.9, 2.8, 4.1, 5.3];
  var FUNCS = { sqrt: Math.sqrt, abs: Math.abs };

  /* ---------- reading expressions ---------- */
  function clean(text) {
    var s = String(text == null ? "" : text).trim().toLowerCase();
    s = s.replace(/−|–/g, "-").replace(/·|×/g, "*").replace(/²/g, "^2").replace(/³/g, "^3")
         .replace(/√/g, "sqrt").replace(/π/g, "pi");
    s = s.replace(/^\s*(y|f\s*\(\s*x\s*\))\s*=/, "");
    return s.replace(/ /g, "");
  }
  function Bad(msg) { this.message = msg; }
  function tokens(s) {
    var out = [], i = 0, m;
    while (i < s.length) {
      var c = s.charAt(i);
      if (/\d/.test(c) || (c === "." && /\d/.test(s.charAt(i + 1)))) {
        m = /^(\d*\.?\d+|\d+\.?)/.exec(s.slice(i)); out.push(["num", parseFloat(m[0])]); i += m[0].length;
      } else if (/[a-z]/.test(c)) {
        m = /^(sqrt|abs|pi|[a-z])/.exec(s.slice(i)); out.push(["id", m[0]]); i += m[0].length;
      } else if ("+-*/^()".indexOf(c) >= 0) { out.push(["op", c]); i++; }
      else throw new Bad("Desmos would read that differently: " + c);
    }
    var res = [];
    out.forEach(function (t) {
      var p = res[res.length - 1];
      if (p) {
        var left = p[0] === "num" || (p[0] === "id" && !FUNCS[p[1]]) || (p[0] === "op" && p[1] === ")");
        var right = t[0] === "id" || (t[0] === "op" && t[1] === "(");
        if (left && right) res.push(["op", "*"]);
      }
      res.push(t);
    });
    return res;
  }
  function parse(text, names) {
    names = names || ["x"];
    var s = clean(text);
    if (!s || s.length > MAX_LEN) throw new Bad("Type an expression.");
    var t = tokens(s), i = 0;
    function peek() { return t[i] || [null, null]; }
    function isOp(o) { var p = peek(); return p[0] === "op" && p[1] === o; }
    function take(o) { if (o && !isOp(o)) throw new Bad("Check your brackets."); return t[i++]; }
    function expr() { var n = term(); while (isOp("+") || isOp("-")) { var o = take()[1]; n = [o, n, term()]; } return n; }
    function term() { var n = unary(); while (isOp("*") || isOp("/")) { var o = take()[1]; n = [o, n, unary()]; } return n; }
    function unary() { if (isOp("-")) { take(); return ["neg", unary()]; } if (isOp("+")) { take(); return unary(); } return power(); }
    function power() { var b = atom(); if (isOp("^")) { take(); return ["^", b, unary()]; } return b; }
    function atom() {
      var p = peek();
      if (p[0] === "num") { take(); return ["num", p[1]]; }
      if (p[0] === "id") {
        take();
        if (FUNCS[p[1]]) { take("("); var a = expr(); take(")"); return ["fn", p[1], a]; }
        if (p[1] === "pi") return ["num", Math.PI];
        if (names.indexOf(p[1]) < 0) throw new Bad("Use x for the variable, not " + p[1] + ".");
        return ["var", p[1]];
      }
      if (isOp("(")) { take(); var n = expr(); take(")"); return n; }
      throw new Bad("That isn't a complete expression yet.");
    }
    var node = expr();
    if (i !== t.length) throw new Bad("Check your brackets.");
    return node;
  }
  function evaluate(n, env) {
    switch (n[0]) {
      case "num": return n[1];
      case "var": return env[n[1]];
      case "neg": return -evaluate(n[1], env);
      case "fn": return FUNCS[n[1]](evaluate(n[2], env));
    }
    var a = evaluate(n[1], env), b = evaluate(n[2], env);
    switch (n[0]) {
      case "+": return a + b;
      case "-": return a - b;
      case "*": return a * b;
      case "/": return a / b;
      default: return Math.pow(a, b);
    }
  }
  function finite(v) { return typeof v === "number" && isFinite(v) ? v : null; }
  // compile once, then evaluate at many x (for drawing)
  function compile(text, params) {
    var names = ["x"].concat(Object.keys(params || {}));
    var node = parse(text, names);
    return function (x, env) { var e = Object.assign({}, params || {}, env || {}, { x: x }); return finite(evaluate(node, e)); };
  }
  function value(text, x, env) {
    try { return compile(text, env)(x); } catch (e) { return null; }
  }
  function check(text) { try { parse(text); return ""; } catch (e) { return e.message || "Check that again."; } }
  function same(a, b) {
    var fa, fb;
    try { fa = compile(a); fb = compile(b); } catch (e) { return false; }
    var agree = 0;
    for (var i = 0; i < SAMPLES.length; i++) {
      var va = fa(SAMPLES[i]), vb = fb(SAMPLES[i]);
      if (va === null || vb === null) { if ((va === null) !== (vb === null)) return false; continue; }
      if (Math.abs(va - vb) > 1e-6 * Math.max(1, Math.abs(va), Math.abs(vb))) return false;
      agree++;
    }
    return agree >= 3;
  }

  /* ---------- grading (same as lessons.right / lessons.grade) ---------- */
  function nrm(v) { return String(v == null ? "" : v).replace(/[\s,]/g, "").replace(/[−–]/g, "-").replace(/%+$/, "").toLowerCase(); }
  function num(v) { v = nrm(v); var m = /^(-?\d+)\/(\d+)$/.exec(v); if (m) return +m[2] ? +m[1] / +m[2] : null; return /^-?(\d+\.?\d*|\.\d+)$/.test(v) ? Number(v) : null; }
  function fillOk(accept, a) {
    if (typeof a !== "string" || a.length > 40) return false;
    return accept.some(function (x) { var n = num(a), y = num(x); return (n !== null && y !== null && Math.abs(n - y) < 1e-9) || nrm(x) === nrm(a); });
  }
  function isNum(v) { return typeof v === "number" && isFinite(v); }
  function isInt(v) { return typeof v === "number" && Math.floor(v) === v; }
  function sameList(a, b) { return Array.isArray(a) && a.length === b.length && a.every(function (v, i) { return v === b[i]; }); }
  function range(n) { var r = []; for (var i = 0; i < n; i++) r.push(i); return r; }
  function key(st) {
    switch (st.type) {
      case "recall": return true;
      case "predict": case "flash": case "slider": return st.answer;
      case "spot": return st.wrong;
      case "order": return range(st.items.length);
      case "fill": return st.accept[0];
      case "plot": return st.answer.slice();
      case "graph": return st.accept[0];
      case "sort": return st.cards.map(function (c) { return c.bucket; });
      case "match": return range(st.left.length);
      case "line": return { at: st.answer.at, closed: st.answer.closed, dir: st.answer.dir };
      case "build": return st.answers[0].slice();
      case "grid": return st.accept.map(function (a) { return a[0]; });
    }
  }
  function right(st, a) {
    switch (st.type) {
      case "recall": return a === true;
      case "predict": case "flash": return isInt(a) && a === st.answer;
      case "spot": return isInt(a) && a === st.wrong;
      case "order": return sameList(a, range(st.items.length));
      case "fill": return fillOk(st.accept, a);
      case "slider": return isNum(a) && Math.abs(a - st.answer) <= (st.tol || 0) + 1e-9;
      case "plot": {
        var tol = (st.tol || 0) + 1e-9;
        return Array.isArray(a) && a.length === 2 && isNum(a[0]) && isNum(a[1]) && Math.abs(a[0] - st.answer[0]) <= tol && Math.abs(a[1] - st.answer[1]) <= tol;
      }
      case "graph":
        return typeof a === "string" && a.length <= MAX_LEN && !(st.forbid || []).some(function (f) { return a.indexOf(f) >= 0; }) &&
          st.accept.some(function (x) { return same(a, x); });
      case "sort": return sameList(a, st.cards.map(function (c) { return c.bucket; }));
      case "match": return sameList(a, range(st.left.length));
      case "line": return !!a && typeof a === "object" && isNum(a.at) && Math.abs(a.at - st.answer.at) < 1e-9 && a.closed === st.answer.closed && a.dir === st.answer.dir;
      case "build": return Array.isArray(a) && st.answers.some(function (x) { return sameList(a, x); });
      case "grid": return Array.isArray(a) && a.length === st.accept.length && st.accept.every(function (acc, i) { return fillOk(acc, a[i]); });
    }
    return false;
  }
  function grade(steps, answers) {
    var n = 0;
    steps.forEach(function (st, i) {
      var gate = st.skip_if, a = answers[i];
      if (a === "skip" && isInt(gate) && gate >= 0 && gate < steps.length && steps[gate].skip_if == null) { if (right(steps[gate], answers[gate])) n++; }
      else if (right(st, a)) n++;
    });
    return n;
  }

  /* ---------- drawing ---------- */
  var GW = 480, GH = 340;
  function niceStep(span) { var s = [1, 2, 5, 10, 20, 25, 50, 100]; for (var i = 0; i < s.length; i++) if (span / s[i] <= 14) return s[i]; return 200; }
  function fmt(v) { v = Math.round(v * 1000) / 1000; return v < 0 ? "−" + Math.abs(v) : String(v); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  // A graph. o = { window: {x:[a,b], y:[c,d]}, curves: [{ f: function(x), cls }], dots: [[x,y]], rings: [[x,y]], mark: [x,y] }
  function Graph(win) {
    var x0 = win.x[0], x1 = win.x[1], y0 = win.y[0], y1 = win.y[1];
    var pad = 30;
    function px(x) { return pad + (x - x0) / (x1 - x0) * (GW - pad - 10); }
    function py(y) { return GH - pad - (y - y0) / (y1 - y0) * (GH - pad - 10); }
    function fromPx(X, Y) { return [x0 + (X - pad) / (GW - pad - 10) * (x1 - x0), y0 + (GH - pad - Y) / (GH - pad - 10) * (y1 - y0)]; }
    function grid() {
      var out = "", sx = niceStep(x1 - x0), sy = niceStep(y1 - y0), v;
      for (v = Math.ceil(x0 / sx) * sx; v <= x1; v += sx) {
        out += '<line class="lk-grid' + (v === 0 ? " lk-axis" : "") + '" x1="' + px(v) + '" x2="' + px(v) + '" y1="' + py(y0) + '" y2="' + py(y1) + '"/>';
        if (v !== 0) out += '<text class="lk-tick" x="' + px(v) + '" y="' + (Math.min(Math.max(py(0), py(y1) + 12), py(y0)) + 14) + '" text-anchor="middle">' + fmt(v) + "</text>";
      }
      for (v = Math.ceil(y0 / sy) * sy; v <= y1; v += sy) {
        out += '<line class="lk-grid' + (v === 0 ? " lk-axis" : "") + '" y1="' + py(v) + '" y2="' + py(v) + '" x1="' + px(x0) + '" x2="' + px(x1) + '"/>';
        if (v !== 0) out += '<text class="lk-tick" y="' + (py(v) + 4) + '" x="' + (Math.max(Math.min(px(0), px(x1) - 16), px(x0) + 2) - 5) + '" text-anchor="end">' + fmt(v) + "</text>";
      }
      return out;
    }
    function curve(f, cls) {
      var d = "", pen = false, prev = null, n = 360, span = y1 - y0;
      for (var i = 0; i <= n; i++) {
        var x = x0 + (x1 - x0) * i / n, y = null;
        try { y = f(x); } catch (e) { y = null; }
        if (y === null || y > y1 + span * 2 || y < y0 - span * 2 || (prev !== null && Math.abs(y - prev) > span * 1.5)) { pen = false; prev = y; continue; }
        d += (pen ? "L" : "M") + px(x).toFixed(1) + " " + py(y).toFixed(1);
        pen = true; prev = y;
      }
      return d ? '<path class="lk-curve ' + (cls || "lk-c0") + '" d="' + d + '"/>' : "";
    }
    return {
      px: px, py: py, fromPx: fromPx,
      svg: function (o) {
        var body = grid();
        (o.curves || []).forEach(function (c) { body += curve(c.f, c.cls); });
        (o.rings || []).forEach(function (p) { body += '<circle class="lk-ring" cx="' + px(p[0]) + '" cy="' + py(p[1]) + '" r="9"/>'; });
        (o.dots || []).forEach(function (p) { body += '<circle class="lk-dot" cx="' + px(p[0]) + '" cy="' + py(p[1]) + '" r="5"/>'; });
        if (o.mark) {
          var mx = px(o.mark[0]), my = py(o.mark[1]);
          body += '<g class="lk-mark' + (o.markCls ? " " + o.markCls : "") + '"><line x1="' + mx + '" x2="' + mx + '" y1="' + py(y0) + '" y2="' + py(y1) + '"/><line y1="' + my + '" y2="' + my + '" x1="' + px(x0) + '" x2="' + px(x1) + '"/>' +
            '<circle cx="' + mx + '" cy="' + my + '" r="7"/><text x="' + (mx + (mx > GW - 110 ? -12 : 12)) + '" y="' + (my < 26 ? my + 22 : my - 12) + '" text-anchor="' + (mx > GW - 110 ? "end" : "start") + '">(' + fmt(o.mark[0]) + ", " + fmt(o.mark[1]) + ")</text></g>";
        }
        return '<svg class="lk-graph" viewBox="0 0 ' + GW + " " + GH + '" role="img" aria-label="' + esc(o.label || "Graph") + '">' + body + "</svg>";
      }
    };
  }
  // A number line from lo to hi with an optional ray: { at, closed, dir }
  var NW = 480, NH = 90;
  function NumberLine(lo, hi) {
    function px(v) { return 24 + (v - lo) / (hi - lo) * (NW - 48); }
    function fromPx(X) { return lo + (X - 24) / (NW - 48) * (hi - lo); }
    return {
      px: px, fromPx: fromPx,
      svg: function (r, label) {
        var out = '<line class="lk-axis" x1="10" x2="' + (NW - 10) + '" y1="50" y2="50"/>', step = niceStep(hi - lo) > 2 ? niceStep(hi - lo) : 1;
        for (var v = Math.ceil(lo); v <= hi; v++) {
          out += '<line class="lk-grid" x1="' + px(v) + '" x2="' + px(v) + '" y1="44" y2="56"/>';
          if (v % step === 0) out += '<text class="lk-tick" x="' + px(v) + '" y="78" text-anchor="middle">' + fmt(v) + "</text>";
        }
        if (r && r.at != null) {
          var x = px(r.at), end = r.dir === "left" ? 10 : r.dir === "right" ? NW - 10 : x;
          if (r.dir) out += '<line class="lk-ray" x1="' + x + '" x2="' + end + '" y1="50" y2="50"/><path class="lk-ray-head" d="' + (r.dir === "left" ? "M10 50l12-8v16z" : "M" + (NW - 10) + " 50l-12-8v16z") + '"/>';
          out += '<circle class="lk-end' + (r.closed ? " is-closed" : "") + '" cx="' + x + '" cy="50" r="8"/>';
        }
        return '<svg class="lk-line" viewBox="0 0 ' + NW + " " + NH + '" role="img" aria-label="' + esc(label || "Number line") + '">' + out + "</svg>";
      }
    };
  }
  // A circle with a sector of `angle` degrees, drawn clockwise from the top.
  function pie(angle, label) {
    var r = 110, c = 130, a = Math.max(0, Math.min(360, angle)) * Math.PI / 180;
    var x = c + r * Math.sin(a), y = c - r * Math.cos(a);
    var sector = angle >= 360 ? '<circle class="lk-sector" cx="' + c + '" cy="' + c + '" r="' + r + '"/>'
      : angle <= 0 ? "" : '<path class="lk-sector" d="M' + c + " " + c + "L" + c + " " + (c - r) + "A" + r + " " + r + " 0 " + (angle > 180 ? 1 : 0) + " 1 " + x.toFixed(1) + " " + y.toFixed(1) + 'Z"/>';
    return '<svg class="lk-pie" viewBox="0 0 260 260" role="img" aria-label="' + esc(label || "Circle") + '"><circle class="lk-circle" cx="' + c + '" cy="' + c + '" r="' + r + '"/>' + sector +
      '<line class="lk-radius" x1="' + c + '" y1="' + c + '" x2="' + c + '" y2="' + (c - r) + '"/><circle class="lk-dot" cx="' + c + '" cy="' + c + '" r="4"/></svg>';
  }
  // A dot plot of values on [lo, hi], with a marker (for example the mean) at `mark`.
  function dotPlot(values, lo, hi, mark, markLabel) {
    var W = 480, H = 150, px = function (v) { return 24 + (v - lo) / (hi - lo) * (W - 48); }, stack = {}, out = "";
    out += '<line class="lk-axis" x1="14" x2="' + (W - 14) + '" y1="110" y2="110"/>';
    for (var t = lo; t <= hi; t += niceStep(hi - lo)) out += '<line class="lk-grid" x1="' + px(t) + '" x2="' + px(t) + '" y1="105" y2="115"/><text class="lk-tick" x="' + px(t) + '" y="134" text-anchor="middle">' + fmt(t) + "</text>";
    values.forEach(function (v, i) {
      var k = Math.round(v); stack[k] = (stack[k] || 0) + 1;
      out += '<circle class="lk-dot' + (i === values.length - 1 ? " lk-dot-live" : "") + '" cx="' + px(v) + '" cy="' + (110 - 14 * stack[k]) + '" r="6"/>';
    });
    if (mark != null) out += '<path class="lk-mean" d="M' + px(mark) + " 112l-8 14h16z" + '"/><text class="lk-mean-label" x="' + px(mark) + '" y="24" text-anchor="middle">' + esc(markLabel || "") + " " + fmt(mark) + '</text><line class="lk-mean-line" x1="' + px(mark) + '" x2="' + px(mark) + '" y1="30" y2="108"/>';
    return '<svg class="lk-dots" viewBox="0 0 ' + W + " " + H + '" role="img" aria-label="Dot plot">' + out + "</svg>";
  }

  window.GraphiteLessonKit = { parse: parse, compile: compile, value: value, check: check, same: same, key: key, right: right, grade: grade,
                               Graph: Graph, NumberLine: NumberLine, pie: pie, dotPlot: dotPlot, fmt: fmt, MAX_LEN: MAX_LEN };
})();
