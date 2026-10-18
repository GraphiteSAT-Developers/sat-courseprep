/* Graphite question tools: the graphing calculator and the tutor, on every page with math questions.
   On a computer they open as a panel on the right and the page slides left, so the whole question stays in view.
   On a phone they open as a sheet over the bottom of the screen. Nothing opens a new tab or window.

   A page turns it on with GraphiteTools.mount({ shift: "selector", top: "selector", bottom: "selector", launcher: true }):
     shift     the parts of the page that move aside (default: main, the trail and the footer)
     top       the bar the panel sits under (default: the site header)
     bottom    a bar the panel sits above (the practice test's question bar)
     launcher  show the Calculator / Tutor tabs on the right edge (pages with their own buttons turn it off)
   Then GraphiteTools.open("calc" | "tutor"), .toggle(tab), .close(), .context({ title, detail }) and
   .tutorAllowed(bool, why) for timed tests, where the tutor waits until the test is submitted. */
(function () {
  "use strict";
  var D = document, root = D.documentElement;
  var KEY = "graphite_tools_v1";
  var opts = null, el = null, tab = "calc", built = false, allowed = true, blockedWhy = "", ctx = null;
  var phone = window.matchMedia("(max-width: 860px)");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
  var saved = { w: 0 };
  try { saved = JSON.parse(localStorage.getItem(KEY)) || saved; } catch (e) { /* storage blocked */ }
  function store() { try { localStorage.setItem(KEY, JSON.stringify(saved)); } catch (e) { /* storage blocked */ } }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  var ICON = {
    calc: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="3" width="14" height="18" rx="2" fill="none" stroke="currentColor" stroke-width="1.8"/><rect x="8" y="6" width="8" height="3.5" rx=".6" fill="currentColor"/><circle cx="9" cy="13.5" r="1.1" fill="currentColor"/><circle cx="12" cy="13.5" r="1.1" fill="currentColor"/><circle cx="15" cy="13.5" r="1.1" fill="currentColor"/><circle cx="9" cy="17.3" r="1.1" fill="currentColor"/><circle cx="12" cy="17.3" r="1.1" fill="currentColor"/><circle cx="15" cy="17.3" r="1.1" fill="currentColor"/></svg>',
    tutor: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3h11A2.5 2.5 0 0 1 20 5.5v8a2.5 2.5 0 0 1-2.5 2.5H11l-4.5 4v-4h0A2.5 2.5 0 0 1 4 13.5z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M8.5 8.5h7M8.5 11.5h4.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>'
  };

  function build() {
    el = D.createElement("aside");
    el.className = "qt"; el.id = "qt"; el.hidden = true;
    el.setAttribute("aria-label", "Calculator and tutor");
    el.innerHTML =
      '<div class="qt-edge" id="qt-edge" role="separator" aria-orientation="vertical" aria-label="Resize the panel. Use the arrow keys." tabindex="0"></div>' +
      '<div class="qt-head">' +
        '<div class="qt-tabs" role="tablist" aria-label="Tools">' +
          '<button type="button" role="tab" id="qt-tab-calc" aria-controls="qt-calc" data-tab="calc">' + ICON.calc + "<span>Calculator</span></button>" +
          '<button type="button" role="tab" id="qt-tab-tutor" aria-controls="qt-tutor" data-tab="tutor">' + ICON.tutor + "<span>Tutor</span></button>" +
        "</div>" +
        '<button type="button" class="qt-close" id="qt-close" aria-label="Close the panel"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button>' +
      "</div>" +
      '<div class="qt-pane qt-calc" id="qt-calc" role="tabpanel" aria-labelledby="qt-tab-calc"><p class="qt-loading">Loading the calculator…</p></div>' +
      '<div class="qt-pane qt-tutor" id="qt-tutor" role="tabpanel" aria-labelledby="qt-tab-tutor" hidden></div>';
    D.body.appendChild(el);
    el.querySelector(".qt-tabs").addEventListener("click", function (e) {
      var b = e.target.closest("[data-tab]"); if (b) show(b.getAttribute("data-tab"));
    });
    el.querySelector(".qt-tabs").addEventListener("keydown", function (e) {
      if (e.key !== "ArrowLeft" && e.key !== "ArrowRight") return;
      show(tab === "calc" ? "tutor" : "calc"); D.getElementById("qt-tab-" + tab).focus();
    });
    D.getElementById("qt-close").addEventListener("click", close);
    edge(D.getElementById("qt-edge"));
    if (opts.launcher) {
      var l = D.createElement("div");
      l.className = "qt-launch"; l.id = "qt-launch";
      l.innerHTML = '<button type="button" data-open="calc" aria-controls="qt">' + ICON.calc + "<span>Calculator</span></button>" +
                    '<button type="button" data-open="tutor" aria-controls="qt">' + ICON.tutor + "<span>Tutor</span></button>";
      l.addEventListener("click", function (e) { var b = e.target.closest("[data-open]"); if (b) toggle(b.getAttribute("data-open")); });
      D.body.appendChild(l);
    }
    D.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && !el.hidden && el.contains(D.activeElement)) { close(); }
    });
    window.addEventListener("resize", layout);
    if (phone.addEventListener) phone.addEventListener("change", layout);
    renderTutor();
  }

  /* ---------- the calculator: the same one as the practice test, built on first open ---------- */
  function calcSource() {
    var bin = atob(window.TOPLINE_SRC_B64), bytes = new Uint8Array(bin.length);
    for (var k = 0; k < bin.length; k++) bytes[k] = bin.charCodeAt(k);
    return new TextDecoder().decode(bytes);
  }
  function theme() {
    var f = el && el.querySelector(".qt-calc iframe"); if (!f) return;
    var light = root.getAttribute("data-theme") === "light" || (opts && opts.light && opts.light());
    try { var b = f.contentDocument.getElementById(light ? "thLight" : "thDark"); if (b) b.click(); } catch (e) { /* other origin */ }
  }
  function buildCalc() {
    if (built) return; built = true;
    var f = D.createElement("iframe");
    f.title = "Graphing calculator";
    f.addEventListener("load", function () { var l = el.querySelector(".qt-loading"); if (l) l.remove(); theme(); });
    if (window.TOPLINE_SRC_B64) f.srcdoc = calcSource(); else f.src = "calculator.html";
    D.getElementById("qt-calc").appendChild(f);
  }

  /* ---------- the tutor (a placeholder until it's connected) ---------- */
  var ASKS = ["Give me a hint", "Where did I go wrong?", "Show me the Desmos way", "Explain the answer"];
  function renderTutor() {
    var p = D.getElementById("qt-tutor"); if (!p) return;
    var about = ctx && ctx.title ? '<p class="qt-about"><span class="label">Asking about</span><strong>' + esc(ctx.title) + "</strong>" +
      (ctx.detail ? '<span class="fine">' + esc(ctx.detail) + "</span>" : "") + "</p>" : "";
    if (!allowed) {
      p.innerHTML = about + '<div class="qt-wait"><p><strong>The tutor opens after you submit.</strong></p><p class="fine">' + esc(blockedWhy || "This one is timed, so your score stays your own work. Every question is waiting for you in the review.") + "</p></div>";
      return;
    }
    p.innerHTML = about +
      '<div class="qt-chat" aria-live="polite"><div class="qt-msg"><p>Stuck? Try the question first, then ask. Hints come one step at a time, so you still do the thinking.</p></div></div>' +
      '<div class="qt-asks" role="group" aria-label="Quick questions">' + ASKS.map(function (a) { return '<button type="button" class="qt-ask" disabled>' + esc(a) + "</button>"; }).join("") + "</div>" +
      '<div class="qt-input" role="note"><span>The message box for the tutor goes here.</span><span class="fine">Coming soon</span></div>' +
      '<p class="fine qt-note">The tutor is an automated helper. Your answers are always graded separately, and it can make mistakes, so check its work. <a href="tutor.html">Open the tutor page</a></p>';
  }

  /* ---------- open, close, layout ---------- */
  function show(t) {
    tab = t === "tutor" ? "tutor" : "calc";
    ["calc", "tutor"].forEach(function (k) {
      var b = D.getElementById("qt-tab-" + k), p = D.getElementById("qt-" + k);
      b.setAttribute("aria-selected", String(k === tab)); b.tabIndex = k === tab ? 0 : -1;
      p.hidden = k !== tab;
    });
    if (tab === "calc") buildCalc();
    marks();
  }
  function width() {
    var vw = window.innerWidth, w = saved.w || Math.round(Math.min(560, Math.max(380, vw * 0.4)));
    return Math.round(Math.max(340, Math.min(w, vw * 0.65)));
  }
  function measure(sel) { var n = sel && D.querySelector(sel); return n ? Math.round(n.getBoundingClientRect().height) : 0; }
  function layout() {
    if (!el) return;
    var open = !el.hidden;
    root.classList.toggle("qt-open", open);
    root.classList.toggle("qt-sheet", open && phone.matches);
    root.style.setProperty("--qt-top", measure(opts.top || ".site-header") + "px");
    root.style.setProperty("--qt-bottom", measure(opts.bottom) + "px");
    root.style.setProperty("--qt-w", open && !phone.matches ? width() + "px" : "0px");
    root.style.setProperty("--qt-h", open && phone.matches ? Math.round(window.innerHeight * 0.56) + "px" : "0px");
    marks();
  }
  function marks() {
    if (!opts) return;
    D.querySelectorAll("[data-qt-toggle]").forEach(function (b) {
      var on = el && !el.hidden && b.getAttribute("data-qt-toggle") === tab;
      b.setAttribute("aria-pressed", String(!!on)); b.classList.toggle("on", !!on);
    });
    var l = D.getElementById("qt-launch");
    if (l) l.querySelectorAll("[data-open]").forEach(function (b) {
      var on = el && !el.hidden && b.getAttribute("data-open") === tab;
      b.setAttribute("aria-expanded", String(!!on)); b.classList.toggle("on", !!on);
    });
  }
  function open(t) {
    if (!el) return;
    el.hidden = false;
    show(t || tab);
    layout();
    var b = D.getElementById("qt-tab-" + tab); if (b) b.focus({ preventScroll: true });
  }
  function close() {
    if (!el || el.hidden) return;
    el.hidden = true; layout();
    var back = D.querySelector('[data-qt-toggle="' + tab + '"]') || D.querySelector('#qt-launch [data-open="' + tab + '"]');
    if (back) back.focus({ preventScroll: true });
  }
  function toggle(t) {
    if (el && !el.hidden && (t || tab) === tab) close(); else open(t);
  }
  // Drag the left edge (or use the arrow keys on it) to make the panel wider or narrower.
  function edge(h) {
    var start = null;
    h.addEventListener("pointerdown", function (e) {
      if (phone.matches || e.button > 0) return;
      e.preventDefault(); h.setPointerCapture(e.pointerId);
      start = { x: e.clientX, w: width() }; root.classList.add("qt-resizing");
    });
    h.addEventListener("pointermove", function (e) { if (!start) return; saved.w = start.w + (start.x - e.clientX); layout(); });
    function end() { if (!start) return; start = null; saved.w = width(); store(); root.classList.remove("qt-resizing"); }
    h.addEventListener("pointerup", end); h.addEventListener("pointercancel", end);
    h.addEventListener("keydown", function (e) {
      var d = { ArrowLeft: 40, ArrowRight: -40 }[e.key]; if (!d) return;
      e.preventDefault(); saved.w = width() + d; layout(); saved.w = width(); store();
    });
  }

  window.GraphiteTools = {
    mount: function (o) {
      if (opts) return window.GraphiteTools;
      opts = Object.assign({ launcher: true }, o || {});
      var shift = opts.shift || "main, .crumbs-bar, .site-footer, .app-footer";
      D.querySelectorAll(shift).forEach(function (n) { n.classList.add("qt-shift"); });
      root.classList.toggle("qt-motion", !reduce.matches);
      build(); layout();
      D.querySelectorAll("[data-qt-toggle]").forEach(function (b) {
        b.addEventListener("click", function () { toggle(b.getAttribute("data-qt-toggle")); });
      });
      return window.GraphiteTools;
    },
    open: open, close: close, toggle: toggle, layout: layout, theme: theme,
    isOpen: function () { return !!(el && !el.hidden); },
    // Pages that only sometimes show math questions (the diagnostic) turn the tools on and off.
    available: function (yes) {
      var l = D.getElementById("qt-launch"); if (l) l.hidden = !yes;
      if (!yes) close();
    },
    context: function (c) { ctx = c || null; renderTutor(); },
    tutorAllowed: function (yes, why) { allowed = !!yes; blockedWhy = why || ""; renderTutor(); }
  };
})();
