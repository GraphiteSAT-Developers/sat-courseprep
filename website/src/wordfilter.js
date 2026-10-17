/* Graphite word filter: no curse words in any text box. The same rules as backend/app/services/wordfilter.py,
   from the same list (backend/app/content/blocked_words.txt, ROT13). build.py fills in WORDS.
   Every text box and text area is checked as you type and before its form sends. Boxes where it doesn't
   apply (passwords, sign-in emails, codes, answers) carry data-no-filter. The server checks again. */
(function () {
  "use strict";
  var WORDS = "__BLOCKED_WORDS__";
  var MESSAGE = "Please keep it clean. That has a word we don't allow.";
  var LEET = { "0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "7": "t", "@": "a", "$": "s", "!": "i", "|": "i" };
  var ENDINGS = ["ings", "ing", "ers", "er", "ed", "es", "s", "y", "ier", "iest", "in"];

  function rot13(s) { return s.replace(/[a-z]/gi, function (c) { var b = c <= "Z" ? 65 : 97; return String.fromCharCode((c.charCodeAt(0) - b + 13) % 26 + b); }); }
  function esc(c) { return c.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }
  function pattern(w) { return w.split("").map(function (c) { return "aeiou".indexOf(c) > -1 ? "[" + c + "*]" : esc(c); }).join(""); }
  var LIST = (Array.isArray(WORDS) ? WORDS : []).map(function (line) {
    var mode = line[0] === "*" ? "any" : line[0] === "~" ? "edge" : "word";
    var p = pattern(rot13(line.replace(/^[*~]/, "")).toLowerCase());
    return { mode: mode, any: new RegExp(p), whole: new RegExp("^" + p + "$"), start: new RegExp("^" + p), end: new RegExp(p + "$") };
  });

  function squeeze(t, atLeast) { return t.replace(new RegExp("(.)\\1{" + (atLeast - 1) + ",}", "g"), "$1"); }
  function tokens(text) {
    var t = String(text || "").normalize ? String(text || "").normalize("NFKD") : String(text || "");
    t = t.replace(/[̀-ͯ]/g, "").toLowerCase().replace(/[013457@$!|]/g, function (c) { return LEET[c]; });
    var parts = t.match(/[a-z*]+/g) || [], out = [], run = [];
    parts.concat([""]).forEach(function (p) {
      if (p.length === 1) { run.push(p); return; }      // f u c k, f.u.c.k
      if (run.length > 1) out.push(run.join("")); else out = out.concat(run);
      run = [];
      if (p) out.push(p);
    });
    return out;
  }
  function stems(t) {
    var out = [t];
    ENDINGS.forEach(function (e) { if (t.length - e.length >= 2 && t.slice(-e.length) === e) out.push(t.slice(0, -e.length)); });
    return out;
  }
  function hit(token) {
    var stretched = squeeze(token, 3);
    return LIST.some(function (w) {
      if (w.mode === "any") return [token, stretched, squeeze(token, 2)].some(function (t) { return w.any.test(t); });
      return [token, stretched].some(function (t) {
        return stems(t).some(function (s) { return w.mode === "word" ? w.whole.test(s) : (w.start.test(s) || w.end.test(s)); });
      });
    });
  }
  function isClean(text) { return !tokens(text).some(hit); }
  window.GraphiteWords = { isClean: isClean, message: MESSAGE };

  /* ---------- every text box ---------- */
  var SKIP = '[data-no-filter], [type="password"], [aria-hidden="true"], .hp input, [tabindex="-1"]';
  function checkable(el) {
    if (!el || !el.matches) return false;
    var text = el.tagName === "TEXTAREA" || (el.tagName === "INPUT" && /^(text|email|search|)$/.test(el.type || ""));
    return text && !el.matches(SKIP) && !el.closest("[data-no-filter]");
  }
  function errorEl(el) {
    var id = (el.id || el.name || "field") + "-clean", e = document.getElementById(id);
    if (!e) {
      e = document.createElement("p"); e.id = id; e.className = "field-error wf-error"; e.setAttribute("role", "alert"); e.hidden = true;
      var box = el.closest(".field") || el.parentNode;
      if (box === el.parentNode) el.insertAdjacentElement("afterend", e); else box.appendChild(e);
    }
    return e;
  }
  function value(el) { return el.type === "email" ? String(el.value).split("@")[0] : el.value; }
  function check(el) {
    var bad = !isClean(value(el)), e = document.getElementById((el.id || el.name || "field") + "-clean");
    if (!bad && !e) return true;
    e = e || errorEl(el);
    e.textContent = bad ? MESSAGE : ""; e.hidden = !bad;
    if (el.setCustomValidity) el.setCustomValidity(bad ? MESSAGE : "");
    var d = (el.getAttribute("aria-describedby") || "").split(" ").filter(function (x) { return x && x !== e.id; });
    if (bad) { d.push(e.id); el.setAttribute("aria-invalid", "true"); } else if (el.getAttribute("aria-invalid") === "true" && !el.validationMessage) el.removeAttribute("aria-invalid");
    if (d.length) el.setAttribute("aria-describedby", d.join(" ")); else el.removeAttribute("aria-describedby");
    return !bad;
  }
  var timer = null;
  document.addEventListener("input", function (ev) {
    var el = ev.target; if (!checkable(el)) return;
    clearTimeout(timer); timer = setTimeout(function () { check(el); }, 250);
  });
  document.addEventListener("blur", function (ev) { if (checkable(ev.target)) check(ev.target); }, true);
  // Before any form's own submit handler: stop it if a box has a blocked word.
  document.addEventListener("submit", function (ev) {
    var form = ev.target, first = null;
    Array.prototype.forEach.call(form.querySelectorAll("input, textarea"), function (el) { if (checkable(el) && !check(el) && !first) first = el; });
    if (first) { ev.preventDefault(); ev.stopImmediatePropagation(); first.focus(); }
  }, true);
})();
