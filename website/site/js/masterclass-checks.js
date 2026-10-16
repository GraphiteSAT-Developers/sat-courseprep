/* Desmos masterclass: does the student's calculator do what a lesson step asks?
   Each check in content/masterclass/lessons.json is a small object, tested here against
   Topline's live lines (window.Topline.lines() in the calculator iframe). website/verify_masterclass.mjs
   runs every step's "show" lines through these same checks in a real browser. */
(function (root) {
  "use strict";
  var SAMPLE_X = [-3.7, -2.2, -0.9, 0.4, 1.3, 2.6, 3.3, 4.9, 6.1, 8.4];

  function close(a, b, tol) {
    return typeof a === "number" && typeof b === "number" && isFinite(a) && Math.abs(a - b) <= (tol == null ? 1e-6 : tol) * Math.max(1, Math.abs(b));
  }
  function live(lines) { return lines.filter(function (l) { return !l.hidden && !l.error; }); }

  // Is (x, y) on this line's curve? Works for y = f(x), x = f(y) and equations like 3x + 2y = 16.
  function onCurve(l, x, y) {
    if (l.op && l.op !== "=") return false;
    if (l.f) return l.variable === "y" ? close(l.f(y), x, 1e-6) : close(l.f(x), y, 1e-6);
    if (l.conds && l.conds.length === 1 && l.conds[0].op === "=") return close(l.conds[0].G(x, y), 0, 1e-6);
    return false;
  }
  var CMP = {
    "<": function (a, b) { return a < b; }, ">": function (a, b) { return a > b; },
    "<=": function (a, b) { return a <= b + 1e-9; }, ">=": function (a, b) { return a >= b - 1e-9; }
  };
  // Is (x, y) in this line's shaded region?
  function inRegion(l, x, y) {
    if (l.f && l.op && CMP[l.op]) return l.variable === "y" ? CMP[l.op](x, l.f(y)) : CMP[l.op](y, l.f(x));
    if (l.conds && l.conds.length === 1 && CMP[l.conds[0].op]) return CMP[l.conds[0].op](l.conds[0].G(x, y), 0);
    return false;
  }
  function onEdge(l, x, y) {
    if (l.f) return l.variable === "y" ? close(l.f(y), x) : close(l.f(x), y);
    if (l.conds && l.conds.length === 1) return close(l.conds[0].G(x, y), 0);
    return false;
  }
  function opOf(l) { return l.conds && l.conds.length === 1 ? l.conds[0].op : l.op; }
  function sameList(a, b) {
    return Array.isArray(a) && a.length === b.length && a.every(function (v, i) { return close(v, b[i]); });
  }

  var CHECKS = {
    // A number on its own line (or a variable that holds one) equals the value.
    value: function (c, lines) {
      var re = c.text ? new RegExp(c.text) : null;
      return live(lines).some(function (l) {
        return (l.kind === "val" || (l.kind === "vdef" && !l.slider)) && close(l.value, c.value, c.tol) && (!re || re.test(l.text));
      });
    },
    // A list with exactly these values.
    list: function (c, lines) { return live(lines).some(function (l) { return sameList(l.value, c.list); }); },
    // A list variable with at least n different numbers, like x_1 = [1, 2, 3, 4].
    listAtLeast: function (c, lines) {
      return live(lines).some(function (l) {
        if (l.kind !== "vdef" || !Array.isArray(l.value)) return false;
        var seen = {};
        l.value.forEach(function (v) { if (typeof v === "number" && isFinite(v)) seen[v] = true; });
        return Object.keys(seen).length >= c.listAtLeast;
      });
    },
    // The graph of y = <expression>, in any equivalent form, including f(x) = <expression>.
    graph: function (c, lines, T) {
      var target = T.fn(c.graph);
      return live(lines).some(function (l) {
        if (!l.f || l.variable !== "x" || (l.op && l.op !== "=")) return false;
        var n = 0;
        for (var i = 0; i < SAMPLE_X.length; i++) {
          var t = target(SAMPLE_X[i]);
          if (typeof t !== "number" || !isFinite(t)) continue;
          if (!close(l.f(SAMPLE_X[i]), t)) return false;
          n++;
        }
        return n >= 3;
      });
    },
    // A curve through every point in "curve" and through none of the points in "off".
    curve: function (c, lines) {
      return live(lines).some(function (l) {
        return c.curve.every(function (p) { return onCurve(l, p[0], p[1]); }) &&
          (c.off || []).every(function (p) { return !onCurve(l, p[0], p[1]); });
      });
    },
    // An inequality with this edge, shading "in" and not "out", with the right kind of edge (dashed or solid).
    region: function (c, lines) {
      var r = c.region, strict = r.op.indexOf("=") < 0;
      return live(lines).some(function (l) {
        var op = opOf(l);
        if (!CMP[op] || (op.indexOf("=") < 0) !== strict) return false;
        return r.edge.every(function (p) { return onEdge(l, p[0], p[1]); }) && inRegion(l, r["in"][0], r["in"][1]) && !inRegion(l, r.out[0], r.out[1]);
      });
    },
    // A variable with this name, like a slider k. With "near", its value too.
    slider: function (c, lines) {
      return live(lines).some(function (l) {
        return l.kind === "vdef" && l.name === c.slider && typeof l.value === "number" && (c.near == null || close(l.value, c.near, c.tol));
      });
    },
    // A regression whose fitted constants match. With anyNames, the letters can be anything.
    fit: function (c, lines) {
      var want = Object.keys(c.fit).map(function (k) { return c.fit[k]; }).sort(function (a, b) { return a - b; });
      return live(lines).some(function (l) {
        if (!l.fit) return false;
        if (c.anyNames) {
          var got = Object.keys(l.fit).map(function (k) { return l.fit[k]; }).sort(function (a, b) { return a - b; });
          return got.length === want.length && got.every(function (v, i) { return close(v, want[i], 1e-5); });
        }
        return Object.keys(c.fit).every(function (k) { return close(l.fit[k], c.fit[k], 1e-5); });
      });
    },
    // A table with these columns, in this order, next to each other.
    table: function (c, lines) {
      return live(lines).some(function (l) {
        if (!l.columns) return false;
        for (var s = 0; s + c.table.length <= l.columns.length; s++) {
          var ok = c.table.every(function (col, k) {
            var vals = l.columns[s + k].values.filter(function (v) { return typeof v === "number" && isFinite(v); });
            return sameList(vals, col);
          });
          if (ok) return true;
        }
        return false;
      });
    },
    deg: function (c, lines, T) { return T.settings().deg === c.deg; },
    // Every one of several checks, like two graphs for "graph both sides".
    all: function (c, lines, T) { return c.all.every(function (sub) { return passes(sub, lines, T); }); }
  };

  function passes(check, lines, T) {
    var kind = Object.keys(CHECKS).filter(function (k) { return k in check; })[0];
    if (!kind) throw new Error("Unknown check: " + JSON.stringify(check));
    try { return !!CHECKS[kind](check, lines, T); } catch (e) { return false; }
  }

  // A typed answer: "11/5", "2.2", "−3". Returns a number, or NaN.
  function parseAnswer(text) {
    var s = String(text == null ? "" : text).replace(/[−–]/g, "-").replace(/\s+/g, "");
    var m = /^(-?\d+(?:\.\d*)?|-?\.\d+)\/(\d+(?:\.\d*)?|\.\d+)$/.exec(s);
    if (m) return Number(m[1]) / Number(m[2]);
    return /^-?(\d+(\.\d*)?|\.\d+)$/.test(s) ? Number(s) : NaN;
  }
  // Is a typed answer right? answer is exact ("31/24") unless tol is set; accept lists other strings that count.
  function answerMatches(text, q) {
    var s = String(text == null ? "" : text).replace(/[−–]/g, "-").replace(/\s+/g, "");
    if ((q.accept || []).indexOf(s) >= 0) return true;
    var got = parseAnswer(s), want = parseAnswer(q.answer);
    if (!isFinite(got)) return false;
    return q.tol ? Math.abs(got - want) <= q.tol + 1e-12 : Math.abs(got - want) <= 1e-9 * Math.max(1, Math.abs(want));
  }

  // "Show me": put a step's lines in the calculator. A line like k = 2 replaces the k that's already there.
  function applyShow(T, step) {
    if (step.showSetting === "deg") T.setDeg(true);
    (step.show || []).forEach(function (spec) {
      var text = typeof spec === "string" ? spec : spec.text || "";
      var m = /^\s*([a-zA-Z](?:_\w+)?)\s*=/.exec(text);
      var lines = T.lines();
      var same = m ? lines.filter(function (l) { return l.name === m[1] && (l.kind === "vdef" || (l.kind === "err" && /^\s*\w+\s*=/.test(l.text))); })[0] : null;
      if (same) T.set(same.index, spec); else T.add([spec]);
    });
  }

  var api = { passes: passes, parseAnswer: parseAnswer, answerMatches: answerMatches, applyShow: applyShow, kinds: Object.keys(CHECKS) };
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.GraphiteMasterclassChecks = api;
})(this);
