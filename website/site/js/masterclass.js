/* Graphite Desmos masterclass: the lesson list and the lessons themselves.
   Lessons come from masterclass-data.js (built from backend/app/content/masterclass/lessons.json).
   Each calculator step is checked live against the student's calculator by masterclass-checks.js.
   Live: progress is saved to /api/masterclass. Preview: it's kept in this browser. */
(function () {
  "use strict";
  var root = document.getElementById("dm-units");
  if (!root) return;
  function $(id) { return document.getElementById(id); }
  var API = window.GraphiteAPI;
  var LIVE = !!(API && API.live);
  var DATA = window.GRAPHITE_MASTERCLASS;
  var C = window.GraphiteMasterclassChecks;
  var LESSONS = DATA.lessons, BY_ID = {}, UNITS = {};
  LESSONS.forEach(function (l, i) { l.n = i + 1; BY_ID[l.id] = l; });
  DATA.units.forEach(function (u, i) { u.n = i + 1; UNITS[u.id] = u; });
  var LETTERS = "ABCD";

  var progress = {};   // lesson id: {step, total, completed}
  var lesson = null;   // the open lesson
  var at = 0;          // checkpoints passed in the open lesson
  var calc = null;     // window.Topline inside the iframe, once it's ready
  var calcWaiters = [];

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function store(k, v) {
    try {
      if (v === undefined) return JSON.parse(localStorage.getItem(k));
      if (v === null) localStorage.removeItem(k); else localStorage.setItem(k, JSON.stringify(v));
    } catch (e) { return null; }
  }
  function showError(msg) { $("dm-error").textContent = msg || ""; $("dm-error").hidden = !msg; }
  function total(l) { return l.kind === "drill" ? l.items.length : l.steps.length + (l.reads || []).length + (l.try ? 1 : 0); }
  function stepOf(l) { var p = progress[l.id]; return p ? p.step : 0; }
  function done(l) { return stepOf(l) >= total(l); }

  if (!LIVE) $("dm-preview-note").hidden = false;
  if (LIVE) API.call("/api/me").then(function (r) { $("account-email").textContent = r.user.email; }, function () {});
  else { try { $("account-email").textContent = sessionStorage.getItem("graphite_user") || ""; } catch (e) { /* storage blocked */ } }

  /* ---------- progress ---------- */
  var PREVIEW_KEY = "graphite_masterclass_progress";
  function loadProgress() {
    if (!LIVE) { progress = store(PREVIEW_KEY) || {}; return Promise.resolve(); }
    return API.call("/api/masterclass").then(function (r) { progress = r.progress || {}; });
  }
  function saveProgress(l, step) {
    var n = total(l), cur = stepOf(l);
    if (step <= cur) return;
    progress[l.id] = { step: step, total: n, completed: step >= n };
    if (!LIVE) { store(PREVIEW_KEY, progress); return; }
    API.call("/api/masterclass/progress", { lesson: l.id, step: step }).catch(function (err) {
      if (err && err.status === 401) { location.href = "/signin.html?next=/masterclass.html"; return; }
      showError("Your progress couldn't be saved. Check your connection; it'll save again on your next step.");
    });
  }

  /* ---------- all lessons ---------- */
  var ICONS = {
    done: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5 L10 17 L19 7" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
  };
  function renderHome() {
    var finished = LESSONS.filter(done).length;
    $("dm-done").textContent = finished;
    $("dm-total").textContent = LESSONS.length;
    $("dm-meter").style.width = Math.round(100 * finished / LESSONS.length) + "%";
    var next = LESSONS.filter(function (l) { return !done(l); })[0];
    var btn = $("dm-continue");
    if (!next) { btn.textContent = "Review any lesson"; btn.onclick = function () { open(LESSONS[0].id); }; }
    else {
      btn.textContent = finished || stepOf(next) ? "Continue: " + next.title : "Start the first lesson";
      btn.onclick = function () { open(next.id); };
    }
    root.innerHTML = DATA.units.map(function (u) {
      var ls = LESSONS.filter(function (l) { return l.unit === u.id; });
      var unitDone = ls.filter(done).length;
      return '<section class="dm-unit" aria-labelledby="dm-u-' + u.id + '">' +
        '<div class="dm-unit-head"><span class="dm-unit-n" aria-hidden="true">' + u.n + '</span><div><h2 id="dm-u-' + u.id + '">' + esc(u.title) + '</h2><p class="fine">' + esc(u.summary) + '</p></div>' +
        '<span class="label dm-unit-count">' + unitDone + " of " + ls.length + " done</span></div>" +
        '<ul class="dm-cards">' + ls.map(card).join("") + "</ul></section>";
    }).join("");
  }
  function card(l) {
    var s = stepOf(l), n = total(l), state = s >= n ? "done" : s > 0 ? "started" : "new";
    var status = state === "done" ? '<span class="dm-status is-done">' + ICONS.done + "Done</span>"
      : state === "started" ? '<span class="dm-status is-started">' + s + " of " + n + " steps</span>"
      : '<span class="dm-status">' + l.minutes + " min</span>";
    return '<li><a class="dm-card is-' + state + '" href="#' + l.id + '">' +
      '<span class="dm-card-top"><span class="dm-card-n">Lesson ' + l.n + '</span><span class="chip chip-quiet">' + esc(l.technique) + "</span></span>" +
      '<strong class="dm-card-title">' + esc(l.title) + '</strong><span class="dm-card-sum">' + esc(l.summary) + "</span>" + status + "</a></li>";
  }

  /* ---------- calculator ---------- */
  var calcBuilt = false, saveTimer = 0;
  function buildCalc() {
    if (calcBuilt) return; calcBuilt = true;
    var f = document.createElement("iframe");
    f.title = "Graphing calculator";
    f.addEventListener("load", function () {
      var l = $("dm-calc-frame").querySelector(".calc-loading"); if (l) l.remove();
      var tries = 0;
      (function ready() {
        var w = f.contentWindow, T = null;
        try { T = w && w.Topline; } catch (e) { /* other origin */ }
        if (!T) { if (++tries < 100) setTimeout(ready, 50); else showError("The calculator didn't load. Refresh the page to try again."); return; }
        try { var dark = f.contentDocument.getElementById("thDark"); if (dark) dark.click(); } catch (e) { /* other origin */ }
        T.keepSaved(false);  // lessons keep their own copy, below; the practice test's calculator stays as it was
        T.onChange(onCalcChange);
        calc = T;
        calcWaiters.splice(0).forEach(function (fn) { fn(); });
      })();
    });
    if (window.TOPLINE_SRC_B64) {  // preview: the calculator is built into the page
      var bin = atob(window.TOPLINE_SRC_B64), bytes = new Uint8Array(bin.length);
      for (var k = 0; k < bin.length; k++) bytes[k] = bin.charCodeAt(k);
      f.srcdoc = new TextDecoder().decode(bytes);
    } else {
      f.src = "calculator.html";
    }
    $("dm-calc-frame").appendChild(f);
  }
  function withCalc(fn) { if (calc) fn(); else { calcWaiters.push(fn); buildCalc(); } }
  function calcKey(id) { return "graphite_masterclass_calc_" + id; }
  function onCalcChange() {
    if (!lesson) return;
    var id = lesson.id;
    clearTimeout(saveTimer);
    saveTimer = setTimeout(function () { if (calc && lesson && lesson.id === id) store(calcKey(id), calc.snapshot()); }, 400);
    checkStep();
  }
  function setCalcOpen(open) {
    $("dm-layout").classList.toggle("calc-open", open);
    $("dm-calc-open").setAttribute("aria-expanded", String(open));
  }
  $("dm-calc-open").addEventListener("click", function () { setCalcOpen(!$("dm-layout").classList.contains("calc-open")); });
  $("dm-calc-close").addEventListener("click", function () { setCalcOpen(false); });
  $("dm-calc-clear").addEventListener("click", function () { if (calc) calc.clear(); });

  /* ---------- one lesson ---------- */
  function open(id) {
    if (location.hash.slice(1) !== id) { location.hash = id; return; }  // the hashchange handler opens it
    show(id);
  }
  function show(id) {
    showError("");
    var l = BY_ID[id];
    if (!l) { lesson = null; $("dm-lesson").hidden = true; $("dm-home").hidden = false; renderHome(); document.title = "Desmos Masterclass | Graphite SAT Tutoring"; return; }
    lesson = l;
    at = stepOf(l);
    $("dm-home").hidden = true;
    $("dm-lesson").hidden = false;
    document.title = l.title + " | Desmos Masterclass | Graphite";
    window.scrollTo(0, 0);
    var unit = UNITS[l.unit];
    $("dm-crumb-unit").textContent = "Unit " + unit.n + ": " + unit.title;
    $("dm-kicker").textContent = "Lesson " + l.n + " of " + LESSONS.length + " · " + l.technique + " · about " + l.minutes + " min";
    $("dm-title").textContent = l.title;
    $("dm-goal").textContent = l.goal;
    var prob = $("dm-problem");
    prob.hidden = !l.problem;
    prob.innerHTML = l.problem ? '<p class="label">The question</p><p class="q-stem">' + l.problem + "</p>" + (l.table ? dataTable(l.table) : "") : "";
    $("dm-intro").innerHTML = l.intro.map(function (p) { return "<p>" + p + "</p>"; }).join("");
    var drill = l.kind === "drill";
    $("dm-steps-wrap").hidden = drill;
    $("dm-reads-wrap").hidden = drill || !(l.reads || []).length;
    $("dm-try-wrap").hidden = drill || !l.try;
    $("dm-drill-wrap").hidden = !drill;
    $("dm-layout").classList.toggle("no-calc", drill);
    $("dm-calc-open").hidden = drill;
    setCalcOpen(false);
    $("dm-wrapup").innerHTML = wrapup(l);
    var nx = LESSONS[l.n];
    $("dm-next").textContent = nx ? "Next: " + nx.title : "Back to all lessons";
    $("dm-next").setAttribute("href", nx ? "#" + nx.id : "#");
    if (drill) { renderDrill(); refresh(); return; }
    renderSteps(); renderReads(); renderTry(); refresh();
    withCalc(function () {
      var saved = store(calcKey(l.id));
      if (saved) calc.restore(saved); else calc.clear();
      checkStep();
    });
  }
  function dataTable(t) {
    return '<table class="dm-table"><thead><tr><th scope="row">x</th>' + t.x.map(function (v) { return "<td>" + v + "</td>"; }).join("") +
      '</tr></thead><tbody><tr><th scope="row">y</th>' + t.y.map(function (v) { return "<td>" + v + "</td>"; }).join("") + "</tr></tbody></table>";
  }
  function wrapup(l) {
    var out = "";
    if (l.pitfalls) out += '<div class="dm-note"><h3>Watch out for</h3><ul>' + l.pitfalls.map(function (p) { return "<li>" + p + "</li>"; }).join("") + "</ul></div>";
    if (l.checklist) out += '<div class="dm-note"><h3>Pre-flight check before you trust a graph</h3><ol>' + l.checklist.map(function (p) { return "<li>" + p + "</li>"; }).join("") + "</ol></div>";
    if (l.byHand) out += '<div class="dm-note"><h3>When it\'s faster by hand</h3><p>' + l.byHand + "</p></div>";
    if (l.bluebook) out += '<div class="dm-note"><h3>On test day</h3><p>' + l.bluebook + "</p></div>";
    return out;
  }

  /* steps: one at a time, each checked live against the calculator */
  function renderSteps() {
    $("dm-steps").innerHTML = lesson.steps.map(function (s, i) {
      return '<li class="dm-step" id="dm-step-' + i + '"><span class="dm-step-n" aria-hidden="true"><span>' + (i + 1) + "</span>" + ICONS.done + "</span>" +
        '<div class="dm-step-body"><p class="dm-step-do">' + s.do + "</p>" +
        (s.keys ? '<p class="dm-keys"><span class="dm-keys-label">Keys</span> <code>' + esc(s.keys) + "</code></p>" : "") +
        '<p class="dm-step-done">' + esc(s.done) + "</p>" +
        '<div class="dm-step-help"><button class="btn btn-quiet dm-small" type="button" data-hint="' + i + '">Hint</button>' +
        '<button class="btn btn-quiet dm-small" type="button" data-show="' + i + '" hidden>Show me</button></div>' +
        '<p class="dm-hint" id="dm-hint-' + i + '" hidden>' + esc(s.hint) + "</p></div></li>";
    }).join("");
  }
  $("dm-steps").addEventListener("click", function (e) {
    var h = e.target.closest("[data-hint]"), s = e.target.closest("[data-show]");
    if (h) {
      var i = +h.getAttribute("data-hint");
      $("dm-hint-" + i).hidden = false;
      h.hidden = true;
      $("dm-steps").querySelector('[data-show="' + i + '"]').hidden = false;  // "Show me" only after a hint
    }
    if (s && calc) {
      C.applyShow(calc, lesson.steps[+s.getAttribute("data-show")]);
      setCalcOpen(true);
    }
  });
  function checkStep() {
    if (!lesson || lesson.kind === "drill" || !calc || at >= lesson.steps.length) return;
    var step = lesson.steps[at];
    if (!C.passes(step.check, calc.lines(), calc)) return;
    advance();
    $("dm-calc-status").textContent = "Step " + at + " done";
    setTimeout(function () { $("dm-calc-status").textContent = ""; }, 2400);
    checkStep();  // the next step may already be done too
  }
  function advance() {
    at++;
    saveProgress(lesson, at);
    refresh();
  }

  /* questions: the reads, then the SAT-style question */
  function question(q, key, label) {
    var body = q.choices
      ? '<div class="choices dm-choices" role="group" aria-label="Answer choices">' + q.choices.map(function (c, i) {
          return '<button class="choice" type="button" data-q="' + key + '" data-choice="' + i + '"><span class="bubble">' + LETTERS[i] + '</span><span class="choice-text">' + esc(c) + "</span></button>";
        }).join("") + "</div>"
      : '<form class="dm-spr" data-q="' + key + '" novalidate><label class="visually-hidden" for="dm-in-' + key + '">Your answer</label>' +
        '<input id="dm-in-' + key + '" inputmode="decimal" autocomplete="off" spellcheck="false" placeholder="Your answer">' +
        '<button class="btn btn-primary" type="submit">Check</button></form>';
    return '<div class="dm-q" id="dm-q-' + key + '">' + (label ? '<p class="label">' + label + "</p>" : "") +
      '<p class="q-stem">' + (q.prompt || q.stem) + "</p>" + body +
      '<p class="dm-feedback" id="dm-fb-' + key + '" role="status" hidden></p>' +
      '<button class="btn btn-quiet dm-small" type="button" data-reveal="' + key + '" hidden>Show the answer</button>' +
      '<div class="dm-explain" id="dm-ex-' + key + '" hidden><p>' + q.explain + "</p></div></div>";
  }
  function renderReads() {
    $("dm-reads").innerHTML = (lesson.reads || []).map(function (q, i) { return question(q, "r" + i); }).join("");
  }
  function renderTry() {
    $("dm-try").innerHTML = lesson.try ? question(lesson.try, "t", "") : "";
  }
  function qByKey(key) { return key === "t" ? lesson.try : lesson.reads[+key.slice(1)]; }
  function qIndex(key) { return key === "t" ? lesson.steps.length + (lesson.reads || []).length : lesson.steps.length + (+key.slice(1)); }
  var misses = {};
  function answer(key, right, picked) {
    var q = qByKey(key), fb = $("dm-fb-" + key), box = $("dm-q-" + key);
    if (qIndex(key) !== at) return;  // only the current question takes answers
    if (q.choices) {
      box.querySelectorAll(".choice").forEach(function (b, i) {
        b.classList.toggle("is-right", right && i === picked);
        b.classList.toggle("is-wrong", !right && i === picked);
      });
    }
    fb.hidden = false;
    if (right) {
      fb.className = "dm-feedback is-right";
      fb.textContent = "That's it.";
      finish(key);
    } else {
      misses[key] = (misses[key] || 0) + 1;
      fb.className = "dm-feedback is-wrong";
      fb.textContent = misses[key] > 1 ? "Not quite. Look at the calculator again, or see the answer." : "Not quite. Check the calculator and try again.";
      if (misses[key] > 1) box.querySelector("[data-reveal]").hidden = false;
    }
  }
  function finish(key) {
    var box = $("dm-q-" + key);
    $("dm-ex-" + key).hidden = false;
    box.querySelector("[data-reveal]").hidden = true;
    box.classList.add("is-answered");
    advance();
  }
  document.addEventListener("submit", function (e) {
    var f = e.target.closest(".dm-spr"); if (!f) return;
    e.preventDefault();
    var key = f.getAttribute("data-q"), v = f.querySelector("input").value;
    if (!v.trim()) return;
    answer(key, C.answerMatches(v, qByKey(key)));
  });
  document.addEventListener("click", function (e) {
    var c = e.target.closest("[data-choice]");
    if (c && lesson) { var key = c.getAttribute("data-q"), i = +c.getAttribute("data-choice"); answer(key, i === qByKey(key).answer, i); return; }
    var r = e.target.closest("[data-reveal]");
    if (r && lesson) {
      var k = r.getAttribute("data-reveal"), q = qByKey(k), fb = $("dm-fb-" + k);
      fb.className = "dm-feedback";
      fb.textContent = "The answer is " + (q.choices ? LETTERS[q.answer] + ". " + q.choices[q.answer] : String(q.answer).replace("-", "−")) + ".";
      if (q.choices) $("dm-q-" + k).querySelectorAll(".choice")[q.answer].classList.add("is-right");
      finish(k);
    }
  });

  /* the strategy drill */
  var drillPicks = {};
  function renderDrill() {
    drillPicks = {};
    $("dm-drill").innerHTML = lesson.items.map(function (it, i) {
      return '<li class="dm-drill-item" id="dm-d-' + i + '"><p class="q-stem">' + esc(it.stem) + "</p>" +
        '<div class="dm-drill-btns" role="group" aria-label="Fastest route"><button class="btn btn-secondary" type="button" data-drill="' + i + '" data-pick="desmos">Desmos</button>' +
        '<button class="btn btn-secondary" type="button" data-drill="' + i + '" data-pick="hand">By hand</button></div>' +
        '<p class="dm-feedback" role="status" hidden></p></li>';
    }).join("");
  }
  $("dm-drill").addEventListener("click", function (e) {
    var b = e.target.closest("[data-drill]"); if (!b) return;
    var i = +b.getAttribute("data-drill"); if (i in drillPicks) return;
    var it = lesson.items[i], pick = b.getAttribute("data-pick"), right = pick === it.answer;
    drillPicks[i] = right;
    var li = $("dm-d-" + i), fb = li.querySelector(".dm-feedback");
    li.querySelectorAll("[data-drill]").forEach(function (x) { x.disabled = true; x.classList.toggle("is-picked", x === b); });
    li.classList.add(right ? "is-right" : "is-wrong");
    fb.hidden = false;
    fb.className = "dm-feedback " + (right ? "is-right" : "is-wrong");
    fb.textContent = (right ? "Yes. " : "Better " + (it.answer === "hand" ? "by hand" : "on Desmos") + ". ") + it.why;
    var answered = Object.keys(drillPicks).length;
    $("dm-drill-score").textContent = Object.keys(drillPicks).filter(function (k) { return drillPicks[k]; }).length + " of " + answered + " right";
    saveProgress(lesson, answered);
    at = Math.max(at, answered);
    refresh();
  });

  /* what's done, what's next, what's locked */
  function refresh() {
    var l = lesson, n = total(l);
    if (l.kind !== "drill") {
      l.steps.forEach(function (s, i) {
        var li = $("dm-step-" + i);
        li.classList.toggle("is-done", i < at);
        li.classList.toggle("is-current", i === at);
        li.classList.toggle("is-locked", i > at);
        if (i === at) li.setAttribute("aria-current", "step"); else li.removeAttribute("aria-current");
      });
      var stepsDone = Math.min(at, l.steps.length);
      $("dm-steps-count").textContent = stepsDone + " of " + l.steps.length + " done";
      var keys = (l.reads || []).map(function (q, i) { return "r" + i; }).concat(l.try ? ["t"] : []);
      keys.forEach(function (k) {
        var box = $("dm-q-" + k), idx = qIndex(k);
        box.classList.toggle("is-locked", idx > at);
        box.querySelectorAll("button, input").forEach(function (x) { if (!x.hasAttribute("data-reveal")) x.disabled = idx !== at; });
        if (idx < at && !box.classList.contains("is-answered")) {  // finished on an earlier visit
          box.classList.add("is-answered");
          $("dm-ex-" + k).hidden = false;
        }
      });
      var firstQ = keys.length ? $("dm-q-" + keys[0]) : null;
      if (firstQ && at < l.steps.length) firstQ.setAttribute("data-wait", "Finish the calculator steps first");
      else if (firstQ) firstQ.removeAttribute("data-wait");
    }
    var complete = at >= n;
    $("dm-complete").hidden = !complete;
    if (complete) $("dm-complete-title").textContent = l.kind === "drill" ? "Nice work. You've got the strategy." : "Nice work. Lesson " + l.n + " is done.";
  }

  /* ---------- routing ---------- */
  $("dm-back").addEventListener("click", function (e) { e.preventDefault(); location.hash = ""; });
  window.addEventListener("hashchange", function () { show(location.hash.slice(1)); });

  loadProgress().then(function () { show(location.hash.slice(1)); }, function (err) {
    if (err && err.status === 401) { location.href = "/signin.html?next=/masterclass.html"; return; }
    show(location.hash.slice(1));
    showError("We couldn't load your progress. Lessons still work; refresh to try again.");
  });
})();
