/* Graphite SAT question tools: the graphing calculator and the tutor, on every page with math questions.
   On a computer or tablet they open as a floating window: drag its title bar to move it anywhere, drag an edge or
   corner to resize it, and double-click the title bar to put it back. The question reflows into the space beside it,
   on whichever side has more room, so the whole question stays in view. The window remembers where it was.
   On a phone they open as a sheet over the bottom of the screen. Nothing opens a new tab or window.

   A page turns it on with GraphiteTools.mount({ shift: "selector", top: "selector", bottom: "selector", launcher: true }):
     shift     the parts of the page that move aside (default: main, the trail and the footer)
     top       the bar the window stays below (default: the site header)
     bottom    a bar the window stays above (the practice test's question bar)
     launcher  show the Calculator / Tutor tabs on the right edge (pages with their own buttons turn it off)
   Then GraphiteTools.open("calc" | "tutor"), .toggle(tab), .close(), .context({ title, detail }) and
   .tutorAllowed(bool, why) for timed tests, where the tutor waits until the test is submitted. */
(function () {
  "use strict";
  var D = document, root = D.documentElement;
  var KEY = "graphite_tools_v2";
  var GAP = 16, MIN_W = 340, MIN_H = 240, MIN_TEXT = 260;
  var opts = null, el = null, tab = "calc", built = false, allowed = true, blockedWhy = "", ctx = null;
  var phone = window.matchMedia("(max-width: 640px)");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
  var saved = {};
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
      ["n", "s", "e", "w", "ne", "nw", "se", "sw"].map(function (d) { return '<div class="qt-rs qt-rs-' + d + '" data-dir="' + d + '" aria-hidden="true"></div>'; }).join("") +
      '<div class="qt-head" id="qt-head">' +
        '<button type="button" class="qt-grip" id="qt-grip" aria-label="Move the window. Use the arrow keys to move it, or Shift and the arrow keys to resize it."><svg viewBox="0 0 24 24" aria-hidden="true"><g fill="currentColor"><circle cx="9" cy="6" r="1.6"/><circle cx="15" cy="6" r="1.6"/><circle cx="9" cy="12" r="1.6"/><circle cx="15" cy="12" r="1.6"/><circle cx="9" cy="18" r="1.6"/><circle cx="15" cy="18" r="1.6"/></g></svg></button>' +
        '<div class="qt-tabs" role="tablist" aria-label="Tools">' +
          '<button type="button" role="tab" id="qt-tab-calc" aria-controls="qt-calc" data-tab="calc">' + ICON.calc + "<span>Calculator</span></button>" +
          '<button type="button" role="tab" id="qt-tab-tutor" aria-controls="qt-tutor" data-tab="tutor">' + ICON.tutor + "<span>Tutor</span></button>" +
        "</div>" +
        '<button type="button" class="qt-close" id="qt-close" aria-label="Close the window"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button>' +
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
    drag(D.getElementById("qt-head"));
    el.querySelectorAll(".qt-rs").forEach(resizer);
    keys(D.getElementById("qt-grip"));
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
  function measure(sel) { var n = sel && D.querySelector(sel); return n ? Math.round(n.getBoundingClientRect().height) : 0; }
  // The room the window may use: the whole viewport, less the bars it stays between.
  function bounds() {
    var top = measure(opts.top || ".site-header"), bottom = window.innerHeight - measure(opts.bottom);
    return { l: 0, r: root.clientWidth || window.innerWidth, t: top, b: Math.max(top + MIN_H, bottom) };
  }
  // Where the window is, from what the student last chose (or the top right the first time), kept on screen.
  function box() {
    var b = bounds(), vw = b.r - b.l, vh = b.b - b.t;
    var w = saved.w || Math.round(Math.min(460, Math.max(MIN_W, vw * 0.38)));
    var h = saved.h || Math.round(Math.min(640, vh - 2 * GAP));
    w = Math.max(Math.min(MIN_W, vw), Math.min(w, vw));
    h = Math.max(Math.min(MIN_H, vh), Math.min(h, vh));
    var x = saved.x == null ? b.r - w - GAP : saved.x, y = saved.y == null ? b.t + GAP : saved.y;
    x = Math.max(b.l, Math.min(x, b.r - w));
    y = Math.max(b.t, Math.min(y, b.b - h));
    return { x: Math.round(x), y: Math.round(y), w: Math.round(w), h: Math.round(h) };
  }
  // The question moves out from under the window, to whichever side of it has more room.
  function reflow(r) {
    var b = bounds(), left = r.x - b.l, right = b.r - (r.x + r.w), padL = 0, padR = 0;
    if (right >= left) padL = Math.min(r.x + r.w + GAP - b.l, b.r - b.l - MIN_TEXT);
    else padR = Math.min(b.r - r.x + GAP, b.r - b.l - MIN_TEXT);
    root.style.setProperty("--qt-l", Math.max(0, padL) + "px");
    root.style.setProperty("--qt-r", Math.max(0, padR) + "px");
  }
  function layout() {
    if (!el) return;
    var open = !el.hidden, sheet = open && phone.matches;
    root.classList.toggle("qt-open", open);
    root.classList.toggle("qt-sheet", sheet);
    root.style.setProperty("--qt-bottom", measure(opts.bottom) + "px");
    root.style.setProperty("--qt-h", sheet ? Math.round(window.innerHeight * 0.56) + "px" : "0px");
    if (open && !sheet) {
      var r = box();
      el.style.left = r.x + "px"; el.style.top = r.y + "px"; el.style.width = r.w + "px"; el.style.height = r.h + "px";
      reflow(r);
    } else {
      el.style.left = el.style.top = el.style.width = el.style.height = "";
      root.style.setProperty("--qt-l", "0px"); root.style.setProperty("--qt-r", "0px");
    }
    marks();
  }
  var frame = 0;
  function soon() { if (!frame) frame = requestAnimationFrame(function () { frame = 0; layout(); }); }
  function keep() { var r = box(); saved = { x: r.x, y: r.y, w: r.w, h: r.h }; store(); }
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
  // Pointer moves (mouse, pen or touch) on a handle, as offsets from where they started. With slack, a press only
  // becomes a drag once it has moved a few pixels, so the buttons on the title bar still take a plain click or tap.
  function track(h, slack, move) {
    var start = null, dragged = false;
    h.addEventListener("pointerdown", function (e) {
      if (phone.matches || e.button > 0) return;
      start = { px: e.clientX, py: e.clientY, r: box(), id: e.pointerId, live: false };
      // Listen on the window, and let the calculator's frame ignore the pointer, so a quick flick isn't lost.
      window.addEventListener("pointermove", step, true);
      window.addEventListener("pointerup", end, true); window.addEventListener("pointercancel", end, true);
      root.classList.add("qt-pressing");
      if (!slack) { e.preventDefault(); begin(); }
    });
    function begin() { start.live = true; try { h.setPointerCapture(start.id); } catch (err) { /* already up */ } root.classList.add("qt-resizing"); }
    function step(e) {
      if (!start || e.pointerId !== start.id) return;
      if (e.pointerType === "mouse" && !e.buttons) { end(); return; } // the button came up somewhere we didn't hear about
      var dx = e.clientX - start.px, dy = e.clientY - start.py;
      if (!start.live) { if (Math.abs(dx) + Math.abs(dy) < 6) return; begin(); }
      move(start.r, dx, dy); soon();
    }
    function end() {
      window.removeEventListener("pointermove", step, true);
      window.removeEventListener("pointerup", end, true); window.removeEventListener("pointercancel", end, true);
      root.classList.remove("qt-pressing");
      if (!start) return;
      var live = start.live; start = null; if (!live) return;
      dragged = true; setTimeout(function () { dragged = false; }, 0); root.classList.remove("qt-resizing"); layout(); keep();
    }
    h.addEventListener("lostpointercapture", function (e) { if (e.target === h) end(); });
    // the click that ends a drag isn't a click on whatever button the drag started on
    h.addEventListener("click", function (e) { if (dragged) { e.stopPropagation(); e.preventDefault(); } }, true);
  }
  // Drag anywhere on the title bar to move the window; double-click it to put the window back where it started.
  function drag(h) {
    track(h, true, function (r, dx, dy) { saved.x = r.x + dx; saved.y = r.y + dy; });
    h.addEventListener("dblclick", function (e) { if (e.target.closest(".qt-tabs button, .qt-close")) return; saved = {}; store(); layout(); });
  }
  // Drag an edge or corner to resize; the opposite edge stays put.
  function resizer(h) {
    var dir = h.getAttribute("data-dir");
    track(h, false, function (r, dx, dy) {
      var x = r.x, y = r.y, w = r.w, hh = r.h;
      if (dir.indexOf("e") >= 0) w = Math.max(MIN_W, r.w + dx);
      if (dir.indexOf("w") >= 0) { w = Math.max(MIN_W, r.w - dx); x = r.x + r.w - w; }
      if (dir.indexOf("s") >= 0) hh = Math.max(MIN_H, r.h + dy);
      if (dir.indexOf("n") >= 0) { hh = Math.max(MIN_H, r.h - dy); y = r.y + r.h - hh; }
      var b = bounds();
      if (x < b.l) { w -= b.l - x; x = b.l; }
      if (y < b.t) { hh -= b.t - y; y = b.t; }
      w = Math.min(w, b.r - x); hh = Math.min(hh, b.b - y);
      saved = { x: x, y: y, w: w, h: hh };
    });
  }
  // From the keyboard: the arrow keys move the window, and Shift with them resizes it.
  function keys(h) {
    h.addEventListener("keydown", function (e) {
      var d = { ArrowLeft: [-1, 0], ArrowRight: [1, 0], ArrowUp: [0, -1], ArrowDown: [0, 1] }[e.key]; if (!d) return;
      e.preventDefault();
      var r = box(), step = 32;
      if (e.shiftKey) saved = { x: r.x, y: r.y, w: Math.max(MIN_W, r.w + d[0] * step), h: Math.max(MIN_H, r.h + d[1] * step) };
      else saved = { x: r.x + d[0] * step, y: r.y + d[1] * step, w: r.w, h: r.h };
      layout(); keep();
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
