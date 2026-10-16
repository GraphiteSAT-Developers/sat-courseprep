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
  var LESSONS = DATA.lessons, TOPICS = DATA.topics || [], BY_ID = {}, UNITS = {};
  LESSONS.forEach(function (l, i) { l.n = i + 1; BY_ID[l.id] = l; });
  TOPICS.forEach(function (l, i) { l.n = i + 1; BY_ID[l.id] = l; });  // optional topic lessons, one per question bank topic
  var DOMAINS = [["algebra", "Algebra"], ["advanced-math", "Advanced Math"], ["psda", "Problem-Solving and Data Analysis"], ["geometry-trig", "Geometry and Trigonometry"]];
  var DOMAIN_NAME = {}; DOMAINS.forEach(function (d) { DOMAIN_NAME[d[0]] = d[1]; });
  function isTopic(l) { return l.kind === "topic"; }
  function usesCalc(l) { return l.kind !== "drill" && l.calculator !== false; }
  DATA.units.forEach(function (u, i) { u.n = i + 1; UNITS[u.id] = u; });
  var LETTERS = "ABCD";

  var progress = {};   // lesson id: {step, total, completed}
  var lesson = null;   // the open lesson
  var at = 0;          // checkpoints passed in the open lesson
  var calc = null;     // window.Topline inside the iframe, once it's ready
  var calcWaiters = [];
  var tryReady = false; // has the student done the calculator work for the SAT-style question?
  var quiz = null;       // the practice quiz in progress: {i, right, ready, answered}

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function store(k, v) {
    try {
      if (v === undefined) return JSON.parse(localStorage.getItem(k));
      if (v === null) localStorage.removeItem(k); else localStorage.setItem(k, JSON.stringify(v));
    } catch (e) { return null; }
  }
  function showError(msg) { $("dm-error").textContent = msg || ""; $("dm-error").hidden = !msg; }
  var QUIZ_SIZE = 3;  // each attempt draws this many questions from the lesson's pool
  function quizSize(l) { return Math.min(QUIZ_SIZE, (l.quiz || []).length); }
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
  function saveQuiz(l, correct) {
    var p = progress[l.id] || (progress[l.id] = { step: 0, total: total(l), completed: false });
    if (p.quiz_best == null || correct > p.quiz_best) p.quiz_best = correct;
    p.quiz_total = quizSize(l);
    if (!LIVE) { store(PREVIEW_KEY, progress); return; }
    API.call("/api/masterclass/quiz", { lesson: l.id, correct: correct }).catch(function (err) {
      if (err && err.status === 401) { location.href = "/signin.html?next=/masterclass.html"; return; }
      showError("Your quiz score couldn't be saved. Check your connection and try again.");
    });
  }
  function saveProgress(l, step) {
    var n = total(l), cur = stepOf(l);
    if (step <= cur) return;
    var old = progress[l.id] || {};
    progress[l.id] = { step: step, total: n, completed: step >= n, quiz_best: old.quiz_best, quiz_total: old.quiz_total };
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
  function nextLesson() { return LESSONS.filter(function (l) { return !done(l); })[0]; }
  var homeScrolled = false;
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
    $("dm-topics").innerHTML = DOMAINS.map(function (d) {
      var ls = TOPICS.filter(function (l) { return l.domain === d[0]; });
      if (!ls.length) return "";
      return '<section class="dm-unit" aria-labelledby="dm-t-' + d[0] + '"><div class="dm-unit-head dm-topic-head"><div><h3 id="dm-t-' + d[0] + '">' + esc(d[1]) + "</h3></div>" +
        '<span class="label dm-unit-count">' + ls.filter(done).length + " of " + ls.length + " done</span></div>" +
        '<ul class="dm-cards">' + ls.map(card).join("") + "</ul></section>";
    }).join("");
    // Returning students land on the next lesson instead of the top of the list.
    var up = $("dm-up-next");
    if (up && !homeScrolled) { homeScrolled = true; up.scrollIntoView({ block: "center" }); }
  }
  function card(l) {
    var s = stepOf(l), n = total(l), state = s >= n ? "done" : s > 0 ? "started" : "new";
    var status = state === "done" ? '<span class="dm-status is-done">' + ICONS.done + "Done</span>"
      : state === "started" ? '<span class="dm-status is-started">' + s + " of " + n + " steps</span>"
      : '<span class="dm-status">' + l.minutes + " min</span>";
    var p = progress[l.id];
    if (p && p.quiz_best != null && l.quiz) status += '<span class="dm-status dm-quiz-best">Quiz ' + p.quiz_best + " of " + quizSize(l) + "</span>";
    if (state === "done" && l.quiz && l.quiz.length) status += '<span class="dm-status dm-retake">' + (p && p.quiz_best != null ? "Retake quiz" : "Take the quiz") + " →</span>";
    status = '<span class="dm-card-foot">' + status + "</span>";
    var next = !isTopic(l) && nextLesson() === l && LESSONS.some(function (x) { return stepOf(x) > 0; });
    var href = "#" + l.id + (state === "done" && l.quiz && l.quiz.length ? "/quiz" : "");
    return '<li><a class="dm-card is-' + state + (next ? " is-next" : "") + '" href="' + href + '"' + (next ? ' id="dm-up-next"' : "") + ">" +
      (next ? '<span class="dm-next-badge">Up next</span>' : "") +
      '<span class="dm-card-top"><span class="dm-card-n">' + (isTopic(l) ? "Topic lesson" : "Lesson " + l.n) + '</span><span class="chip chip-quiet">' + esc(isTopic(l) ? "Quiz" : l.technique) + "</span></span>" +
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
    checkQuiz();
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
    if (location.hash.slice(1) !== id) { location.hash = id; return; }  // the hashchange handler opens it (#id, or #id/quiz)
    show(id);
  }
  function show(id) {
    showError("");
    var parts = String(id).split("/"), toQuiz = parts[1] === "quiz";
    id = parts[0];
    var l = BY_ID[id];
    if (!l) { lesson = null; $("dm-lesson").hidden = true; $("dm-home").hidden = false; renderHome(); document.title = "Desmos Masterclass | Graphite SAT Tutoring"; return; }
    lesson = l;
    at = stepOf(l);
    tryReady = false;
    quiz = null;
    $("dm-home").hidden = true;
    $("dm-lesson").hidden = false;
    document.title = l.title + " | Desmos Masterclass | Graphite";
    window.scrollTo(0, 0);
    if (isTopic(l)) {
      $("dm-back").textContent = "Practice";
      $("dm-back").setAttribute("href", "practice.html");
      $("dm-crumb-unit").textContent = "Topic lesson: " + DOMAIN_NAME[l.domain];
      $("dm-kicker").textContent = "Topic lesson · " + DOMAIN_NAME[l.domain] + " · about " + l.minutes + " min · optional";
    } else {
      var unit = UNITS[l.unit];
      $("dm-back").textContent = "All lessons";
      $("dm-back").setAttribute("href", "#");
      $("dm-crumb-unit").textContent = "Unit " + unit.n + ": " + unit.title;
      $("dm-kicker").textContent = "Lesson " + l.n + " of " + LESSONS.length + " · " + l.technique + " · about " + l.minutes + " min";
    }
    $("dm-title").textContent = l.title;
    $("dm-goal").textContent = l.goal;
    var prob = $("dm-problem");
    prob.hidden = !l.problem;
    prob.innerHTML = l.problem ? '<p class="label">The question</p><p class="q-stem">' + l.problem + "</p>" + (l.table ? dataTable(l.table) : "") : "";
    $("dm-intro").innerHTML = l.intro.map(function (p) { return "<p>" + p + "</p>"; }).join("");
    $("dm-rules").hidden = !l.rules;
    $("dm-rules-list").innerHTML = (l.rules || []).map(function (r) { return "<li>" + r + "</li>"; }).join("");
    $("dm-example").hidden = !l.example;
    $("dm-example-body").innerHTML = l.example ? '<p class="q-stem">' + l.example.problem + '</p><ol class="dm-example-steps">' +
      l.example.solution.map(function (s) { return "<li>" + s + "</li>"; }).join("") + "</ol>" : "";
    var drill = l.kind === "drill";
    $("dm-steps-wrap").hidden = drill || !l.steps.length;
    $("dm-reads-wrap").hidden = drill || !(l.reads || []).length;
    $("dm-try-wrap").hidden = drill || !l.try;
    $("dm-drill-wrap").hidden = !drill;
    $("dm-layout").classList.toggle("no-calc", !usesCalc(l));
    $("dm-calc-open").hidden = !usesCalc(l);
    setCalcOpen(false);
    $("dm-wrapup").innerHTML = wrapup(l);
    if (isTopic(l)) {
      $("dm-next").textContent = "Practice this topic now";
      $("dm-next").setAttribute("href", "practice.html?topic=" + encodeURIComponent(l.domain + "/" + l.skill));
    } else {
      var nx = LESSONS[l.n];
      $("dm-next").textContent = nx ? "Next: " + nx.title : "Back to all lessons";
      $("dm-next").setAttribute("href", nx ? "#" + nx.id : "#");
    }
    if (drill) { renderDrill(); refresh(); return; }
    renderSteps(); renderReads(); renderTry(); refresh();
    checkTry();
    if (toQuiz && !$("dm-quiz-wrap").hidden) setTimeout(function () { $("dm-quiz-wrap").scrollIntoView({ block: "start" }); }, 0);
    if (!usesCalc(l)) return;
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
    if (l.related && l.related.length) out += '<div class="dm-note"><h3>Desmos moves for this topic</h3><ul>' + l.related.map(function (id) {
      var r = BY_ID[id]; return r ? '<li><a href="#' + r.id + '">Lesson ' + r.n + ": " + esc(r.title) + "</a></li>" : "";
    }).join("") + "</ul></div>";
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
        '<p class="dm-hint" id="dm-hint-' + i + '" hidden>' + esc(s.hint) + "</p>" +
        '<div class="dm-showme" id="dm-showme-' + i + '" hidden>' + showText(s) + "</div></div></li>";
    }).join("");
  }
  // "Show me" says exactly what to type, but the student still types it: the calculator never fills itself in.
  function showText(s) {
    var parts = [];
    if (s.showSetting === "deg") parts.push("Open <strong>Settings</strong> and choose <strong>Degrees</strong>.");
    (s.show || []).forEach(function (sp) {
      if (sp.table) {
        parts.push("Type <code>table</code> on an empty line, then fill in " + sp.table.cols.map(function (c) {
          return "<code>" + esc(c.name) + "</code>: " + esc(c.cells.join(", "));
        }).join(" and ") + ".");
      } else {
        var text = typeof sp === "string" ? sp : sp.text;
        parts.push((sp.slider ? "Set the slider to " : "Type ") + "<code>" + esc(text) + "</code>");
      }
    });
    return '<p class="label">Type this yourself</p><ul>' + parts.map(function (x) { return "<li>" + x + "</li>"; }).join("") + "</ul>";
  }
  $("dm-steps").addEventListener("click", function (e) {
    var h = e.target.closest("[data-hint]"), s = e.target.closest("[data-show]");
    if (h) {
      var i = +h.getAttribute("data-hint");
      $("dm-hint-" + i).hidden = false;
      h.hidden = true;
      $("dm-steps").querySelector('[data-show="' + i + '"]').hidden = false;  // "Show me" only after a hint
    }
    if (s) {
      $("dm-showme-" + s.getAttribute("data-show")).hidden = false;
      s.hidden = true;
      setCalcOpen(true);
    }
  });
  // The SAT-style question opens only once the calculator holds the work for it.
  function checkTry() {
    if (tryReady || !lesson || !lesson.try || at !== qIndex("t")) return;
    if (!lesson.try.check || (calc && C.passes(lesson.try.check, calc.lines(), calc))) {
      tryReady = true;
      refresh();
      if (lesson.try.check) $("dm-calc-status").textContent = "Calculator work found";
    }
  }
  function checkStep() {
    checkTry();
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
    checkTry();
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
    var gate = q.check ? '<p class="dm-gate" id="dm-gate-' + key + '"><span class="dm-gate-lock" aria-hidden="true"></span><span><strong>Use the calculator first.</strong> ' + esc(q.use) + " Answers open when your work is in the calculator.</span></p>" : "";
    return '<div class="dm-q" id="dm-q-' + key + '">' + (label ? '<p class="label">' + label + "</p>" : "") +
      '<p class="q-stem">' + (q.prompt || q.stem) + "</p>" + gate + body +
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
    if (key === "t" && !tryReady) return;  // and only after the calculator work
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
    var f = e.target.closest(".dm-spr"); if (!f || !f.hasAttribute("data-q")) return;  // the quiz handles its own
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
        var locked = idx !== at || (k === "t" && !tryReady);
        box.querySelectorAll("button, input").forEach(function (x) { if (!x.hasAttribute("data-reveal")) x.disabled = locked; });
        var gate = $("dm-gate-" + k);
        if (gate) gate.hidden = k !== "t" || tryReady || idx < at;
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
    var hasQuiz = !!(l.quiz && l.quiz.length);
    $("dm-quiz-wrap").hidden = !hasQuiz || !complete;
    if (hasQuiz && complete && !quiz) startQuiz();
    if (complete) $("dm-complete-title").textContent = l.kind === "drill" ? "Nice work. You've got the strategy." : isTopic(l) ? "Nice work. Try the quiz below, then practice this topic." : "Nice work. Lesson " + l.n + " is done.";
  }

  /* the practice quiz: after the lesson, one question at a time, each opened by calculator work */
  function quizMeta() {
    var p = progress[lesson.id];
    return p && p.quiz_best != null ? "Best score: " + p.quiz_best + " of " + quizSize(lesson) : quizSize(lesson) + " questions";
  }
  // A fresh draw each attempt: questions from the last attempt go to the back of the line, so a retake shows new ones.
  function drawQuiz(l) {
    var key = "graphite_masterclass_quiz_last_" + l.id, last = store(key) || [];
    var all = l.quiz.map(function (q, k) { return k; });
    for (var a = all.length - 1; a > 0; a--) { var b = Math.floor(Math.random() * (a + 1)), tmp = all[a]; all[a] = all[b]; all[b] = tmp; }
    var fresh = all.filter(function (k) { return last.indexOf(k) < 0; }), seen = all.filter(function (k) { return last.indexOf(k) >= 0; });
    var items = fresh.concat(seen).slice(0, quizSize(l));
    store(key, items);
    return items;
  }
  function quizQ() { return lesson.quiz[quiz.items[quiz.i]]; }
  function startQuiz() {
    quiz = { i: 0, right: 0, ready: false, answered: false, marks: [], items: drawQuiz(lesson) };
    var picked = quiz.items.map(function (k) { return lesson.quiz[k]; });
    var gated = picked.filter(function (x) { return x.check; }).length, n = picked.length;
    $("dm-quiz-lede").textContent = (isTopic(lesson) ? n + " SAT-style questions on this topic. " : n + " new questions on what this lesson taught. ") +
      (gated === n ? "Use the calculator for each one: the answer box opens once your work is in it. "
        : gated ? "Questions marked with a lock need calculator work before you can answer. " : "") + "One try per question, and you can retake it.";
    $("dm-quiz-meta").textContent = quizMeta();
    renderQuizQuestion();
    showFresh();
    checkQuiz();
  }
  function renderQuizQuestion() {
    var q = quizQ(), n = quiz.items.length;
    var body = q.choices
      ? '<div class="choices dm-choices" role="group" aria-label="Answer choices">' + q.choices.map(function (c, i) {
          return '<button class="choice" type="button" data-zchoice="' + i + '" disabled><span class="bubble">' + LETTERS[i] + '</span><span class="choice-text">' + esc(c) + "</span></button>";
        }).join("") + "</div>"
      : '<form class="dm-spr" id="dm-z-form" novalidate><label class="visually-hidden" for="dm-z-in">Your answer</label>' +
        '<input id="dm-z-in" inputmode="decimal" autocomplete="off" spellcheck="false" placeholder="Your answer" disabled>' +
        '<button class="btn btn-primary" type="submit" disabled>Submit</button></form>';
    $("dm-quiz").innerHTML = '<div class="dm-q dm-zq"><div class="dm-quiz-top"><p class="label">Question ' + (quiz.i + 1) + " of " + n + "</p>" +
      '<ol class="dm-quiz-dots" aria-hidden="true">' + quiz.items.map(function (x, i) {
        return '<li class="' + (i < quiz.i ? (quiz.marks[i] ? "is-right" : "is-wrong") : i === quiz.i ? "is-now" : "") + '"></li>';
      }).join("") + "</ol></div>" +
      '<p class="q-stem">' + q.stem + "</p>" +
      (q.check ? '<p class="dm-gate" id="dm-z-gate"><span class="dm-gate-lock" aria-hidden="true"></span><span><strong>Use the calculator first.</strong> ' + esc(q.use) + " Answers open when your work is in the calculator.</span></p>" : "") +
      (q.check ? '<p class="dm-fresh" id="dm-z-fresh" hidden>Your calculator still has earlier work, and its letters can clash with this question\'s. <button class="btn btn-quiet dm-small" type="button" id="dm-z-clear">Clear the calculator</button></p>' : "") +
      body + '<p class="dm-feedback" id="dm-z-fb" role="status" hidden></p>' +
      '<div class="dm-explain" id="dm-z-ex" hidden><p>' + q.explain + "</p></div>" +
      '<button class="btn btn-primary" type="button" id="dm-z-next" hidden>' + (quiz.i + 1 < n ? "Next question" : "See your score") + "</button></div>";
  }
  function showFresh() {
    var f = $("dm-z-fresh");
    if (f) f.hidden = !(calc && calc.lines().some(function (l) { return l.text || l.columns; }));
  }
  function checkQuiz() {
    if (!quiz || quiz.ready || quiz.done || !lesson.quiz) return;
    var check = quizQ().check;
    if (check && !(calc && C.passes(check, calc.lines(), calc))) return;
    quiz.ready = true;
    if ($("dm-z-gate")) $("dm-z-gate").hidden = true;
    $("dm-quiz").querySelectorAll("[data-zchoice], #dm-z-in, #dm-z-form button").forEach(function (x) { x.disabled = false; });
    if (check) $("dm-calc-status").textContent = "Calculator work found";
  }
  function answerQuiz(right, picked) {
    if (!quiz || !quiz.ready || quiz.answered) return;  // one try, and only after the calculator work
    var q = quizQ();
    quiz.answered = true;
    quiz.marks = quiz.marks || [];
    quiz.marks[quiz.i] = right;
    if (right) quiz.right++;
    $("dm-quiz").querySelectorAll("[data-zchoice], #dm-z-in, #dm-z-form button").forEach(function (x) { x.disabled = true; });
    if (q.choices) {
      var bs = $("dm-quiz").querySelectorAll(".choice");
      bs[q.answer].classList.add("is-right");
      if (!right) bs[picked].classList.add("is-wrong");
    }
    var fb = $("dm-z-fb");
    fb.hidden = false;
    fb.className = "dm-feedback " + (right ? "is-right" : "is-wrong");
    fb.textContent = right ? "Right." : "Not this time. The answer is " + (q.choices ? LETTERS[q.answer] + ". " + q.choices[q.answer] : String(q.answer).replace("-", "\u2212")) + ".";
    $("dm-z-ex").hidden = false;
    $("dm-z-next").hidden = false;
    $("dm-z-next").focus();
  }
  function quizNext() {
    if (quiz.i + 1 < quiz.items.length) {
      quiz.i++; quiz.ready = false; quiz.answered = false;
      renderQuizQuestion();
      showFresh();
      checkQuiz();
      return;
    }
    quiz.done = true;
    var n = quiz.items.length;
    saveQuiz(lesson, quiz.right);
    $("dm-quiz-meta").textContent = quizMeta();
    var msg = quiz.right === n ? "A perfect score. You're ready to use this on test day."
      : quiz.right >= n - 1 ? "Nearly there. Read the explanation for the one you missed, then retake it for a new set."
      : "Go back over the lesson above, then retake the quiz. Each retake draws different questions.";
    msg += " Retaking clears the calculator, so you'll do the work again.";
    $("dm-quiz").innerHTML = '<div class="dm-q dm-quiz-result"><p class="label">Your score</p><p class="dm-quiz-score"><strong>' + quiz.right + "</strong> of " + n + "</p>" +
      '<ol class="dm-quiz-dots" aria-hidden="true">' + quiz.marks.map(function (m) { return '<li class="' + (m ? "is-right" : "is-wrong") + '"></li>'; }).join("") + "</ol>" +
      "<p>" + msg + '</p><button class="btn btn-secondary" type="button" id="dm-z-retake">Retake the quiz</button></div>';
  }
  $("dm-quiz").addEventListener("click", function (e) {
    var c = e.target.closest("[data-zchoice]");
    if (c) { var i = +c.getAttribute("data-zchoice"); answerQuiz(i === quizQ().answer, i); return; }
    if (e.target.closest("#dm-z-next")) { quizNext(); return; }
    if (e.target.closest("#dm-z-clear")) { if (calc) calc.clear(); $("dm-z-fresh").hidden = true; setCalcOpen(true); return; }
    if (e.target.closest("#dm-z-retake")) {
      // A retake starts from a blank calculator, so every answer needs fresh work.
      if (calc) calc.clear();
      startQuiz();
      $("dm-calc-status").textContent = "Calculator cleared for the retake";
      $("dm-quiz-wrap").scrollIntoView({ block: "start" });
    }
  });
  $("dm-quiz").addEventListener("submit", function (e) {
    e.preventDefault();
    var v = $("dm-z-in").value;
    if (!v.trim()) return;
    answerQuiz(C.answerMatches(v, quizQ()));
  });

  // On phones the calculator button sits above the cookie banner while the banner is showing.
  (function () {
    var banner = document.getElementById("cookie-banner"), fab = $("dm-calc-open");
    if (!banner || !fab || !window.ResizeObserver) return;
    function place() { fab.style.bottom = banner.hidden ? "" : (banner.offsetHeight + 16) + "px"; }
    new ResizeObserver(place).observe(banner);
    new MutationObserver(place).observe(banner, { attributes: true, attributeFilter: ["hidden", "class", "style"] });
    place();
  })();

  /* ---------- routing ---------- */
  $("dm-back").addEventListener("click", function (e) { if (lesson && isTopic(lesson)) return; e.preventDefault(); location.hash = ""; });
  window.addEventListener("hashchange", function () { show(location.hash.slice(1)); });

  loadProgress().then(function () { show(location.hash.slice(1)); }, function (err) {
    if (err && err.status === 401) { location.href = "/signin.html?next=/masterclass.html"; return; }
    show(location.hash.slice(1));
    showError("We couldn't load your progress. Lessons still work; refresh to try again.");
  });
})();
