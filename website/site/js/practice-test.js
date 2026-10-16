/* Graphite practice test engine.
   Live (served by the backend): questions come from /api/tests/<id> without answers, and the server grades.
   Static preview: questions come from GRAPHITE_TEST in questions.js and are graded in the browser.
   With ?session=<id>, the page runs a practice set from the question bank instead (see practice.js):
   a timed random practice test, or untimed topic practice where each answer is checked as you go. */
(function () {
  "use strict";
  var root = document.getElementById("exam");
  if (!root) return;
  function $(id) { return document.getElementById(id); }
  var API = window.GraphiteAPI;
  var LIVE = !!(API && API.live);
  var TEST_ID = root.getAttribute("data-test") || "pt4-math-m1";
  var SESSION_ID = (/[?&]session=(\d+)/.exec(location.search) || [])[1] || null;
  var practiceCall = LIVE ? (API && API.call) : (window.GraphitePracticeLocal && window.GraphitePracticeLocal.call);
  var BACK_URL = SESSION_ID ? "practice.html" : "dashboard.html";

  function loadFailed(err, here) {
    if (err && err.status === 401) { location.href = "/signin.html?next=" + encodeURIComponent(here); return; }
    $("start-btn").textContent = "Couldn't load";
    var p = document.querySelector("#start-overlay .dialog > p:not(.label)");
    if (p) p.textContent = err && err.status === 404 ? "We couldn't find this practice set. Start a new one from the practice page."
      : "We couldn't load this test. Check your connection and refresh the page.";
  }

  if (SESSION_ID) {
    $("start-btn").disabled = true; $("start-btn").textContent = "Loading…";
    if (!practiceCall) { loadFailed(null); return; }
    Promise.all([practiceCall("/api/practice/sessions/" + SESSION_ID), LIVE ? API.call("/api/me") : Promise.resolve({ user: null })])
      .then(function (r) {
        var s = r[0].session;
        boot({ id: "practice-" + s.id, session: s, mode: s.mode, title: s.title, name: s.mode === "test" ? "Practice test" : "Topic practice",
               minutes: s.minutes, questions: s.questions }, r[1].user);
      })
      .catch(function (err) { loadFailed(err, "/practice-test.html?session=" + SESSION_ID); });
  } else if (LIVE) {
    $("start-btn").disabled = true; $("start-btn").textContent = "Loading…";
    Promise.all([API.call("/api/tests/" + TEST_ID), API.call("/api/me")])
      .then(function (r) { boot(r[0].test, r[1].user); })
      .catch(function (err) { loadFailed(err, "/practice-test.html"); });
  } else {
    boot(window.GRAPHITE_TEST, null);
  }

  function boot(T, user) {
  if (!T) return;
  var Q = T.questions, N = Q.length, LETTERS = "ABCD";
  var TOPIC = T.mode === "topic", UNTIMED = !T.minutes;
  var checked = (T.session && T.session.checked) || {}; // topic practice: graded questions, by index
  var checking = false;
  var KEY = "graphite_test_" + T.id + (user ? "_u" + user.id : "");
  if (user) $("exam-student").textContent = user.name;
  $("start-btn").disabled = false; $("start-btn").textContent = T.minutes ? "Begin module" : "Start practicing";
  var submitting = false;
  function load() { try { return JSON.parse(localStorage.getItem(KEY)); } catch (e) { return null; } }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) { /* storage blocked */ } }
  function fresh() {
    return { started: false, submitted: false, cur: 0, remaining: T.minutes * 60, elapsed: 0, answers: {}, crossed: {}, marked: {}, view: "graphite", timerHidden: false, page: "q" };
  }
  var S = load() || fresh();
  if (T.session) {
    // The server's copy wins: answers it already checked, and a set finished on another device.
    Object.keys(checked).forEach(function (k) { S.answers[k] = answerValue(checked[k]); });
    if (T.session.submitted && T.session.result) { S.started = true; S.submitted = true; S.result = T.session.result; }
    if (!T.session.submitted && S.submitted) S = fresh();
  }
  function answerValue(g) { return g.type === "mc" ? LETTERS.indexOf(g.your_answer) : g.your_answer; }
  applyLabels();
  var resumed = !!(S.started && !S.submitted);
  var tickTimer = null, toastTimer = null;

  /* ---------- helpers ---------- */
  function fmt(sec) { sec = Math.max(0, Math.round(sec)); var m = Math.floor(sec / 60), s = sec % 60; return m + ":" + (s < 10 ? "0" : "") + s; }
  function toast(msg) {
    var t = $("toast"); t.textContent = msg; t.hidden = false;
    clearTimeout(toastTimer); toastTimer = setTimeout(function () { t.hidden = true; }, 3600);
  }
  function sprValue(raw) {
    if (raw == null) return null;
    var s = String(raw).replace(/\s+/g, "");
    if (!/^-?(\d+\.?\d*|\.\d+|\d+\/\d+)$/.test(s)) return null;
    if (s.indexOf("/") > -1) { var p = s.replace("-", "").split("/"); var v = Number(p[0]) / Number(p[1]); if (!isFinite(v)) return null; return s[0] === "-" ? -v : v; }
    return Number(s);
  }
  function isAnswered(i) { var a = S.answers[i]; return a !== undefined && a !== null && a !== ""; }
  // Static preview only: grades in the browser and returns the same shape the server sends.
  function gradeLocal(seconds) {
    var res = { correct: 0, total: N, seconds_used: seconds, multiple_choice: { right: 0, total: 0 }, student_produced: { right: 0, total: 0 }, by_domain: [], questions: [] };
    var dom = {};
    Q.forEach(function (q, i) {
      var a = S.answers[i], answered = isAnswered(i), ok = false;
      if (answered) {
        if (q.type === "mc") ok = a === q.answer;
        else { var v = sprValue(a); ok = v !== null && Math.abs(v - q.answer) < 1e-9; }
      }
      if (ok) res.correct++;
      var b = q.type === "mc" ? res.multiple_choice : res.student_produced; b.total++; if (ok) b.right++;
      if (!dom[q.domain]) { dom[q.domain] = { domain: q.domain, right: 0, total: 0 }; res.by_domain.push(dom[q.domain]); }
      dom[q.domain].total++; if (ok) dom[q.domain].right++;
      res.questions.push({ index: i, type: q.type, domain: q.domain, stem: q.stem, correct: ok, answered: answered,
        your_answer: answered ? (q.type === "mc" ? LETTERS[a] : a) : null,
        answer: q.type === "mc" ? LETTERS[q.answer] : String(q.answer), answer_index: q.answer,
        choices: q.choices, explain: q.explain, calc: q.calc });
    });
    return res;
  }
  function previewHTML(raw) {
    var s = String(raw || "").replace(/\s+/g, "");
    if (!s) return "";
    var esc = s.replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; });
    var m = /^(-?)(\d+)\/(\d+)$/.exec(s);
    if (m) return m[1] + '<span class="frac"><span>' + m[2] + "</span><span>" + m[3] + "</span></span>";
    return esc.replace(/^-/, "−");
  }

  /* ---------- view & timer ---------- */
  function applyView() {
    root.setAttribute("data-view", S.view);
    $("view-toggle").setAttribute("aria-pressed", String(S.view === "light"));
    $("view-toggle").textContent = S.view === "light" ? "Graphite colors" : "Test-day colors";
    themeCalc();
  }
  function renderTimer() {
    if (UNTIMED) {
      $("timer").textContent = fmt(S.elapsed || 0);
      $("timer").classList.toggle("is-hidden", !!S.timerHidden);
      $("timer-toggle").textContent = S.timerHidden ? "Show" : "Hide";
      $("timer-toggle").setAttribute("aria-pressed", String(!!S.timerHidden));
      return;
    }
    $("timer").textContent = fmt(S.remaining);
    var last5 = S.remaining <= 300;
    var hidden = S.timerHidden && !last5;
    $("timer").classList.toggle("is-hidden", hidden);
    $("timer").classList.toggle("is-low", last5);
    $("timer-toggle").textContent = hidden ? "Show" : "Hide";
    $("timer-toggle").setAttribute("aria-pressed", String(hidden));
    $("timer-toggle").hidden = last5;
  }
  function startClock() {
    clearInterval(tickTimer);
    tickTimer = setInterval(function () {
      if (!S.started || S.submitted) return;
      if (UNTIMED) { S.elapsed = (S.elapsed || 0) + 1; renderTimer(); if (S.elapsed % 5 === 0) save(); return; }
      S.remaining -= 1;
      if (S.remaining === 300) toast("5 minutes remaining.");
      if (S.remaining <= 0) { S.remaining = 0; renderTimer(); submit(true); return; }
      renderTimer();
      if (S.remaining % 5 === 0) save();
    }, 1000);
  }

  /* ---------- question rendering ---------- */
  function renderQuestion() {
    var i = S.cur, q = Q[i];
    $("q-num").textContent = String(i + 1);
    $("mark-btn").setAttribute("aria-pressed", String(!!S.marked[i]));
    $("mark-btn").classList.toggle("on", !!S.marked[i]);
    $("elim-toggle").hidden = q.type !== "mc";
    $("spr-help").hidden = q.type !== "spr";
    $("q-stem").innerHTML = q.stem;
    var box = $("q-answer"); box.innerHTML = "";
    var locked = !!checked[i];
    var elimOn = !locked && $("elim-toggle").getAttribute("aria-pressed") === "true";
    $("elim-toggle").hidden = q.type !== "mc" || locked;

    if (q.type === "mc") {
      var list = document.createElement("div");
      list.className = "mc"; list.setAttribute("role", "radiogroup"); list.setAttribute("aria-label", "Answer choices for question " + (i + 1));
      var crossed = S.crossed[i] || {};
      q.choices.forEach(function (c, k) {
        var row = document.createElement("div"); row.className = "mc-row" + (crossed[k] ? " is-crossed" : "");
        var b = document.createElement("button"); b.type = "button"; b.className = "mc-choice";
        b.setAttribute("role", "radio"); b.setAttribute("aria-checked", String(S.answers[i] === k));
        if (locked) {
          b.disabled = true;
          if (k === checked[i].answer_index) row.classList.add("is-key");
          else if (S.answers[i] === k) row.classList.add("is-wrong");
        }
        b.innerHTML = '<span class="mc-letter">' + LETTERS[k] + '</span><span class="mc-text">' + c + "</span>";
        b.addEventListener("click", function () {
          if (checked[i]) return;
          if ((S.crossed[i] || {})[k]) { S.crossed[i][k] = false; }
          S.answers[i] = S.answers[i] === k ? null : k;
          save(); renderQuestion(); renderNav(); focusChoice(k);
        });
        row.appendChild(b);
        if (elimOn) {
          var x = document.createElement("button"); x.type = "button"; x.className = "mc-x";
          x.textContent = crossed[k] ? "Undo" : LETTERS[k];
          x.setAttribute("aria-label", (crossed[k] ? "Undo cross out of choice " : "Cross out choice ") + LETTERS[k]);
          x.addEventListener("click", function () {
            S.crossed[i] = S.crossed[i] || {};
            S.crossed[i][k] = !S.crossed[i][k];
            if (S.crossed[i][k] && S.answers[i] === k) S.answers[i] = null;
            save(); renderQuestion(); renderNav();
            var again = box.querySelectorAll(".mc-x")[k]; if (again) again.focus();
          });
          row.appendChild(x);
        }
        list.appendChild(row);
      });
      box.appendChild(list);
    } else {
      var wrap = document.createElement("div"); wrap.className = "spr";
      var lab = document.createElement("label"); lab.setAttribute("for", "spr-input"); lab.className = "visually-hidden"; lab.textContent = "Your answer to question " + (i + 1);
      var inp = document.createElement("input"); inp.type = "text"; inp.id = "spr-input"; inp.autocomplete = "off"; inp.inputMode = "text"; inp.spellcheck = false;
      inp.maxLength = 6; inp.value = S.answers[i] || ""; inp.readOnly = locked;
      var prev = document.createElement("p"); prev.className = "spr-preview"; prev.setAttribute("aria-live", "polite");
      var err = document.createElement("p"); err.className = "field-error"; err.id = "spr-error"; err.hidden = true;
      function update() {
        var v = inp.value.replace(/\s+/g, "");
        var neg = v[0] === "-";
        if (v.length > (neg ? 6 : 5)) { v = v.slice(0, neg ? 6 : 5); inp.value = v; }
        var valid = v === "" || sprValue(v) !== null;
        err.hidden = valid || /[\/.\-]$/.test(v);
        err.textContent = "Use digits, one decimal point or one fraction bar, and a leading minus sign if needed.";
        inp.setAttribute("aria-invalid", String(!err.hidden));
        prev.innerHTML = v ? "Answer Preview: <strong>" + previewHTML(v) + "</strong>" : "Answer Preview:";
        S.answers[i] = v; save(); renderNav(); renderCheck();
      }
      inp.addEventListener("input", update);
      wrap.appendChild(lab); wrap.appendChild(inp); wrap.appendChild(prev); wrap.appendChild(err);
      box.appendChild(wrap);
      prev.innerHTML = inp.value ? "Answer Preview: <strong>" + previewHTML(inp.value) + "</strong>" : "Answer Preview:";
      if (!locked) inp.addEventListener("keydown", function (e) { if (e.key === "Enter" && TOPIC) checkAnswer(); });
    }
    renderCheck();
    $("back-btn").disabled = i === 0 && S.page === "q";
    $("nav-label").textContent = "Question " + (i + 1) + " of " + N;
  }
  // Topic practice: a Check button under the answer, then the verdict and full explanation once checked.
  function renderCheck() {
    var area = $("q-check");
    if (!TOPIC) { area.hidden = true; return; }
    area.hidden = false;
    var i = S.cur, g = checked[i];
    if (!g) {
      area.innerHTML = '<button class="btn btn-primary" type="button" id="check-btn">Check answer</button>';
      var btn = $("check-btn");
      btn.disabled = !isAnswered(i) || checking;
      btn.addEventListener("click", checkAnswer);
      return;
    }
    var verdict = g.correct ? "Correct" : "Not quite";
    area.innerHTML = '<div class="fb ' + (g.correct ? "ok" : "no") + '" tabindex="-1" id="fb"><p class="fb-verdict"><strong>' + verdict + "</strong>" +
      (g.correct ? "" : ' <span>The answer is <strong>' + (g.type === "mc" ? g.answer : previewHTML(g.answer.split(" or ")[0])) + "</strong>.</span>") + "</p>" +
      '<div class="fb-explain"></div></div>';
    area.querySelector(".fb-explain").innerHTML = g.explain_html || "";
  }
  function checkAnswer() {
    var i = S.cur;
    if (checking || checked[i] || !isAnswered(i)) return;
    checking = true; renderCheck();
    practiceCall("/api/practice/sessions/" + T.session.id + "/check", { index: i, answer: S.answers[i] })
      .then(function (r) {
        checked[i] = r.question; S.answers[i] = answerValue(r.question); save();
        checking = false;
        if (S.cur === i) { renderQuestion(); var fb = $("fb"); if (fb) fb.focus({ preventScroll: false }); }
        renderNav();
      })
      .catch(function (err) {
        checking = false; renderCheck();
        if (err && err.status === 401) { save(); location.href = "/signin.html?next=" + encodeURIComponent("/practice-test.html?session=" + T.session.id); return; }
        toast(err && err.status ? err.message : "We couldn't check that answer. Check your connection and try again.");
      });
  }
  function focusChoice(k) { var b = $("q-answer").querySelectorAll(".mc-choice")[k]; if (b) b.focus(); }

  /* ---------- navigator & review ---------- */
  function buildGrid(el, closeAfter) {
    el.innerHTML = "";
    for (var i = 0; i < N; i++) {
      (function (i) {
        var b = document.createElement("button"); b.type = "button"; b.className = "g-cell";
        if (isAnswered(i)) b.classList.add("is-answered");
        if (checked[i]) b.classList.add(checked[i].correct ? "is-right" : "is-wrong");
        if (S.marked[i]) b.classList.add("is-marked");
        if (i === S.cur && S.page === "q") { b.classList.add("is-current"); b.setAttribute("aria-current", "step"); }
        b.textContent = String(i + 1);
        b.setAttribute("aria-label", "Question " + (i + 1) + (isAnswered(i) ? ", answered" : ", unanswered") + (S.marked[i] ? ", marked for review" : ""));
        b.addEventListener("click", function () { goTo(i); if (closeAfter) closeNav(); });
        el.appendChild(b);
      })(i);
    }
  }
  function renderNav() {
    buildGrid($("nav-grid"), true);
    if (S.page === "review") renderReview();
  }
  function renderReview() {
    buildGrid($("review-grid"), false);
    var answered = 0, marked = 0;
    for (var i = 0; i < N; i++) { if (isAnswered(i)) answered++; if (S.marked[i]) marked++; }
    $("review-summary").textContent = answered + " of " + N + " answered · " + marked + " marked for review";
  }
  function openNav() { $("nav-pop").hidden = false; $("nav-toggle").setAttribute("aria-expanded", "true"); renderNav(); var c = $("nav-grid").querySelector(".is-current") || $("nav-grid").firstChild; if (c) c.focus(); }
  function closeNav() { $("nav-pop").hidden = true; $("nav-toggle").setAttribute("aria-expanded", "false"); }

  function showPage(p) {
    S.page = p; save();
    $("q-view").hidden = p !== "q";
    $("review-view").hidden = p !== "review";
    $("results-view").hidden = p !== "results";
    $("exam-bottom").classList.toggle("is-results", p === "results");
    $("next-btn").hidden = p !== "q";
    $("back-btn").hidden = p === "results";
    $("back-btn").disabled = p === "q" && S.cur === 0;
    $("submit-confirm").hidden = true;
    if (p === "review") { renderReview(); $("nav-label").textContent = "Review page"; }
    if (p === "q") renderQuestion();
    $("q-area").scrollTop = 0;
  }
  function goTo(i) { S.cur = Math.max(0, Math.min(N - 1, i)); showPage("q"); renderNav(); $("q-area").focus({ preventScroll: true }); }

  /* ---------- submit & results ---------- */
  function submit(auto) {
    if (S.submitted || submitting) return;
    clearInterval(tickTimer);
    var seconds = UNTIMED ? (S.elapsed || 0) : T.minutes * 60 - S.remaining;
    var finish = function (result) {
      S.submitted = true; S.result = result; save();
      if (auto) toast("Time's up. Your module was submitted.");
      renderResults(result); showPage("results");
    };
    if (!LIVE && !T.session) { finish(gradeLocal(seconds)); return; }
    var answers = {};
    Object.keys(S.answers).forEach(function (k) { if (isAnswered(Number(k))) answers[k] = S.answers[k]; });
    submitting = true; $("submit-go").disabled = true; $("submit-go").textContent = "Submitting…";
    var url = T.session ? "/api/practice/sessions/" + T.session.id + "/submit" : "/api/tests/" + T.id + "/attempts";
    (T.session ? practiceCall : API.call)(url, { answers: answers, seconds_used: seconds })
      .then(function (r) { finish(r.result); })
      .catch(function (err) {
        if (err && err.status === 401) { save(); location.href = "/signin.html?next=" + encodeURIComponent(location.pathname + location.search); return; }
        showPage("review");
        toast(err && err.status ? err.message : "We couldn't submit. Check your connection, then press Submit module again.");
      })
      .then(function () { submitting = false; $("submit-go").disabled = false; $("submit-go").textContent = "Yes, submit"; });
  }
  function renderResults(r) {
    var marked = 0;
    for (var m = 0; m < N; m++) if (S.marked[m]) marked++;
    $("results-title").textContent = "You got " + r.correct + " of " + r.total + " right";
    $("res-time").textContent = fmt(r.seconds_used);
    $("res-mc").textContent = r.multiple_choice.right + " of " + r.multiple_choice.total;
    $("res-spr").textContent = r.student_produced.right + " of " + r.student_produced.total;
    $("res-marked").textContent = String(marked);

    var bars = $("res-domains"); bars.innerHTML = "";
    r.by_domain.forEach(function (d) {
      var pct = Math.round(d.right / d.total * 100);
      var li = document.createElement("li");
      li.innerHTML = '<span class="bar-name"></span><span class="bar-track"><span style="width:' + pct + '%"></span></span><span class="bar-val">' + d.right + "/" + d.total + "</span>";
      li.querySelector(".bar-name").textContent = d.domain;
      bars.appendChild(li);
    });

    var list = $("res-list"); list.innerHTML = "";
    r.questions.forEach(function (q) {
      var yours = !q.answered ? "No answer" : (q.type === "mc" ? q.your_answer : previewHTML(q.your_answer));
      var correct = String(q.answer).replace(/^-/, "−");
      var d = document.createElement("details"); d.className = "res-item " + (q.correct ? "ok" : "no");
      d.innerHTML = '<summary><span class="res-n">' + (q.index + 1) + '</span><span class="res-verdict">' + (q.correct ? "Correct" : (q.answered ? "Incorrect" : "Skipped")) +
        '</span><span class="res-dom"></span><span class="res-ans">Yours: <strong>' + yours + "</strong> · Answer: <strong>" + correct + "</strong></span></summary>" +
        '<div class="res-body"><div class="res-stem">' + q.stem + "</div>" +
        (q.type === "mc" ? '<ol class="res-choices" type="A">' + q.choices.map(function (c, k) { return '<li class="' + (k === q.answer_index ? "is-key" : "") + '">' + c + "</li>"; }).join("") + "</ol>" : "") +
        '<div class="res-explain"></div>' + (q.calc ? '<p class="res-calc"><strong>With the calculator:</strong> <span></span></p>' : "") + "</div>";
      d.querySelector(".res-dom").textContent = q.skill && T.session ? q.skill : q.domain;
      if (q.explain_html) d.querySelector(".res-explain").innerHTML = q.explain_html;
      else d.querySelector(".res-explain").textContent = q.explain || "";
      if (q.calc) d.querySelector(".res-calc span").textContent = q.calc;
      list.appendChild(d);
    });
  }

  /* ---------- calculator panel ---------- */
  var calcBuilt = false;
  function themeCalc() {
    var f = $("calc-frame").querySelector("iframe");
    try {
      var btn = f && f.contentDocument && f.contentDocument.getElementById(S.view === "light" ? "thLight" : "thDark");
      if (btn) btn.click();
    } catch (e) { /* calculator served from another origin */ }
  }
  function buildCalc() {
    if (calcBuilt) return; calcBuilt = true;
    var f = document.createElement("iframe");
    f.title = "Graphing calculator";
    f.addEventListener("load", function () { var l = $("calc-frame").querySelector(".calc-loading"); if (l) l.remove(); themeCalc(); });
    if (window.TOPLINE_SRC_B64) {
      var bin = atob(window.TOPLINE_SRC_B64), bytes = new Uint8Array(bin.length);
      for (var k = 0; k < bin.length; k++) bytes[k] = bin.charCodeAt(k);
      f.srcdoc = new TextDecoder().decode(bytes);
    } else {
      f.src = "calculator.html";
    }
    $("calc-frame").appendChild(f);
  }
  function setCalc(open) {
    $("calc-panel").hidden = !open;
    $("calc-toggle").setAttribute("aria-pressed", String(open));
    $("calc-toggle").classList.toggle("on", open);
    root.classList.toggle("calc-open", open);
    if (open) buildCalc();
  }
  function setCalcWidth(px) {
    var max = Math.round(window.innerWidth * 0.75);
    px = Math.max(320, Math.min(max, px));
    $("calc-panel").style.width = px + "px";
    $("calc-resize").setAttribute("aria-valuenow", String(px));
  }
  (function resizer() {
    var handle = $("calc-resize"), dragging = false;
    handle.addEventListener("pointerdown", function (e) {
      dragging = true; handle.setPointerCapture(e.pointerId); root.classList.add("is-resizing");
    });
    handle.addEventListener("pointermove", function (e) {
      if (!dragging) return;
      var left = $("calc-panel").getBoundingClientRect().left;
      setCalcWidth(e.clientX - left);
    });
    function stop() { dragging = false; root.classList.remove("is-resizing"); }
    handle.addEventListener("pointerup", stop); handle.addEventListener("pointercancel", stop);
    handle.addEventListener("keydown", function (e) {
      var w = $("calc-panel").getBoundingClientRect().width;
      if (e.key === "ArrowRight") { setCalcWidth(w + 32); e.preventDefault(); }
      if (e.key === "ArrowLeft") { setCalcWidth(w - 32); e.preventDefault(); }
    });
  })();

  /* ---------- dialogs ---------- */
  var lastFocus = null;
  function openDialog(id) {
    lastFocus = document.activeElement;
    var d = $(id); d.hidden = false;
    var f = d.querySelector("button, a"); if (f) f.focus();
  }
  function closeDialog(d) { d.hidden = true; if (lastFocus) lastFocus.focus(); }
  Array.prototype.forEach.call(document.querySelectorAll("[data-close]"), function (b) {
    b.addEventListener("click", function () { closeDialog(b.closest(".overlay")); });
  });
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    if (!$("dir-dialog").hidden) closeDialog($("dir-dialog"));
    else if (!$("ref-dialog").hidden) closeDialog($("ref-dialog"));
    else if (!$("nav-pop").hidden) { closeNav(); $("nav-toggle").focus(); }
    else if (!$("more-menu").hidden) { $("more-menu").hidden = true; $("more-toggle").setAttribute("aria-expanded", "false"); $("more-toggle").focus(); }
  });

  /* ---------- wire controls ---------- */
  $("start-btn").addEventListener("click", function () {
    S.started = true; save();
    $("start-overlay").hidden = true; startClock(); renderTimer();
    $("q-area").focus({ preventScroll: true });
  });
  $("timer-toggle").addEventListener("click", function () { S.timerHidden = !S.timerHidden; save(); renderTimer(); });
  $("calc-toggle").addEventListener("click", function () { setCalc($("calc-panel").hidden); });
  $("calc-close").addEventListener("click", function () { setCalc(false); $("calc-toggle").focus(); });
  $("calc-expand").addEventListener("click", function () {
    var on = $("calc-expand").getAttribute("aria-pressed") !== "true";
    $("calc-expand").setAttribute("aria-pressed", String(on));
    $("calc-expand").textContent = on ? "Collapse" : "Expand";
    setCalcWidth(on ? window.innerWidth * 0.65 : 480);
  });
  $("ref-open").addEventListener("click", function () { openDialog("ref-dialog"); });
  $("open-directions").addEventListener("click", function () { openDialog("dir-dialog"); });
  $("more-toggle").addEventListener("click", function () {
    var open = $("more-menu").hidden;
    $("more-menu").hidden = !open; $("more-toggle").setAttribute("aria-expanded", String(open));
  });
  document.addEventListener("click", function (e) {
    if (!$("more-menu").hidden && !e.target.closest(".more-wrap")) { $("more-menu").hidden = true; $("more-toggle").setAttribute("aria-expanded", "false"); }
    if (!$("nav-pop").hidden && !e.target.closest(".nav-wrap")) closeNav();
  });
  $("view-toggle").addEventListener("click", function () { S.view = S.view === "light" ? "graphite" : "light"; save(); applyView(); });
  var restartArmed = false;
  $("restart-test").addEventListener("click", function () {
    if (!restartArmed) { restartArmed = true; $("restart-test").textContent = "Tap again to erase answers"; setTimeout(function () { restartArmed = false; $("restart-test").textContent = "Start over"; }, 4000); return; }
    reset();
  });
  $("save-exit").addEventListener("click", save);
  $("mark-btn").addEventListener("click", function () { S.marked[S.cur] = !S.marked[S.cur]; save(); renderQuestion(); renderNav(); });
  $("elim-toggle").addEventListener("click", function () {
    var on = $("elim-toggle").getAttribute("aria-pressed") !== "true";
    $("elim-toggle").setAttribute("aria-pressed", String(on)); $("elim-toggle").classList.toggle("on", on);
    renderQuestion();
  });
  $("nav-toggle").addEventListener("click", function () { if ($("nav-pop").hidden) openNav(); else closeNav(); });
  $("nav-close").addEventListener("click", function () { closeNav(); $("nav-toggle").focus(); });
  $("go-review").addEventListener("click", function () { closeNav(); showPage("review"); });
  $("back-btn").addEventListener("click", function () {
    if (S.page === "review") { goTo(N - 1); return; }
    if (S.cur > 0) goTo(S.cur - 1);
  });
  $("next-btn").addEventListener("click", function () {
    if (S.cur < N - 1) goTo(S.cur + 1); else showPage("review");
  });
  $("submit-open").addEventListener("click", function () { $("submit-confirm").hidden = false; $("submit-go").focus(); });
  $("submit-cancel").addEventListener("click", function () { $("submit-confirm").hidden = true; $("submit-open").focus(); });
  $("submit-go").addEventListener("click", function () { submit(false); });
  $("retake").addEventListener("click", function () {
    if (!T.session) { reset(); return; }
    var s = T.session, b = $("retake");
    var data = s.mode === "test" ? { mode: "test" } : { mode: "topic", domain: s.domain, skill: s.skill, count: N };
    b.disabled = true; b.textContent = "Building your set…";
    practiceCall("/api/practice/sessions", data).then(function (r) {
      location.href = "practice-test.html?session=" + r.session.id;
    }).catch(function (err) {
      b.disabled = false; b.textContent = "New set, same topic";
      toast(err && err.status ? err.message : "We couldn't start a new set. Check your connection and try again.");
    });
  });

  function reset() {
    var view = S.view; S = fresh(); S.view = view;
    Object.keys(checked).forEach(function (k) { S.answers[k] = answerValue(checked[k]); });
    save();
    clearInterval(tickTimer); restartArmed = false;
    $("restart-test").textContent = "Start over"; $("more-menu").hidden = true;
    applyView(); renderTimer(); showPage("q"); renderNav();
    $("start-overlay").hidden = false; $("start-btn").focus();
  }

  /* ---------- labels for practice sets ---------- */
  function applyLabels() {
    if (!T.session) return;
    var heading = T.mode === "test" ? "Math practice test" : T.title;
    var kind = T.mode === "test" ? "Practice test · Math" : "Topic practice · " + (T.session.skill ? "one skill" : "whole domain");
    $("exam-title").textContent = heading;
    $("start-title").textContent = heading;
    document.querySelector("#start-overlay .label").textContent = kind;
    document.querySelector("#results-view > .label").textContent = kind;
    $("review-heading").textContent = heading + " questions";
    document.querySelector("#nav-pop .review-card-head strong").textContent = heading + " questions";
    var facts = '<li><strong>' + N + "</strong> questions</li>" +
      (UNTIMED ? "<li>Untimed. The clock counts up so you can see your pace</li><li>Check each answer as you go</li>"
               : "<li><strong>" + T.minutes + "</strong> minutes</li><li>Graphing calculator on every question</li>");
    document.querySelector("#start-overlay .start-facts").innerHTML = facts;
    var intro = document.querySelector("#start-overlay .dialog > p:not(.label)");
    if (intro) intro.textContent = UNTIMED
      ? "Answer a question, then press Check answer to see if you got it and read the full explanation, with the Desmos shortcut when one helps. Your progress saves as you go."
      : "New questions you haven't answered before, in the same mix as the real test. The timer starts when you begin. Your answers save as you go, and the module submits itself when time runs out.";
    $("start-btn").textContent = UNTIMED ? "Start practicing" : "Begin module";
    $("submit-open").textContent = TOPIC ? "Finish set" : "Submit module";
    $("confirm-title").textContent = TOPIC ? "Finish this set?" : "Submit this module?";
    if (TOPIC) $("confirm-desc").textContent = "Questions you haven't answered go back into the pool for next time.";
    $("retake").textContent = TOPIC ? "New set, same topic" : "Take another practice test";
    Array.prototype.forEach.call(document.querySelectorAll('a[href$="dashboard.html"]'), function (a) {
      if (a.id === "save-exit" || a.closest(".dialog-actions")) a.setAttribute("href", BACK_URL);
    });
    var back = document.querySelector(".res-actions a"); if (back) { back.setAttribute("href", BACK_URL); back.textContent = "Back to practice"; }
    document.title = heading + " | Graphite SAT Tutoring";
  }

  /* ---------- boot ---------- */
  applyView(); renderTimer();
  if (S.submitted && !S.result) { S = fresh(); save(); }
  if (S.submitted) { renderResults(S.result); showPage("results"); $("start-overlay").hidden = true; }
  else {
    showPage(S.page === "review" ? "review" : "q"); renderNav();
    if (S.started) { $("start-overlay").hidden = true; startClock(); if (resumed) toast(UNTIMED ? "Picked up where you left off." : "Picked up where you left off. " + fmt(S.remaining) + " left."); }
  }
  }
})();
