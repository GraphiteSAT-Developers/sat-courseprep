/* Graphite SAT practice test engine.
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
  // Reading and Writing: every question has a passage, shown above the question like a Math question's stem. No calculator or reference sheet.
  var RW = N > 0 && Q.every(function (q) { return q.section === "rw"; });
  var SECTION = RW ? "Reading and Writing" : "Math";
  root.classList.toggle("is-rw", RW);
  $("dir-rw").hidden = !RW; $("dir-math").hidden = RW;
  var TOPIC = T.mode === "topic" || T.mode === "quiz" || T.mode === "review", UNTIMED = !T.minutes;
  var REVIEW = T.mode === "review";
  var LEVEL = (T.session && T.session.level) || null; // a Level up set
  var MOCK = (T.session && T.session.mock) || null; // a module of an adaptive mock test (services/mock.py)
  var FROM_PLAN = !!(T.session && T.session.plan_task) && !REVIEW && !LEVEL && !MOCK;
  if (MOCK) { BACK_URL = "practice.html"; document.documentElement.setAttribute("data-mock", "1"); }
  if (FROM_PLAN) BACK_URL = "plan.html";
  if (LEVEL) BACK_URL = "levels.html#track=" + LEVEL.track;
  if (REVIEW) BACK_URL = "dashboard.html#review";
  var checked = (T.session && T.session.checked) || {}; // topic practice: graded questions, by index
  var checking = false;
  var KEY = "graphite_test_" + T.id + (user ? "_u" + user.id : "");
  if (user) $("exam-student").textContent = user.name;
  $("start-btn").disabled = false; $("start-btn").textContent = T.minutes ? "Begin module" : "Start practicing";
  var submitting = false;
  function load() { try { return JSON.parse(localStorage.getItem(KEY)); } catch (e) { return null; } }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) { /* storage blocked */ } }
  function fresh() {
    // Settings > Practice defaults: test colors and whether the timer starts hidden.
    var d = window.GraphiteTheme ? GraphiteTheme.prefs().study : { colors: "graphite", timer: "show" };
    return { started: false, submitted: false, cur: 0, remaining: T.minutes * 60, elapsed: 0, answers: {}, crossed: {}, marked: {},
             view: d.colors === "testday" ? "light" : "graphite", timerHidden: d.timer === "hide", page: "q" };
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
    renderGameTag(i);
    $("mark-btn").setAttribute("aria-pressed", String(!!S.marked[i]));
    $("mark-btn").classList.toggle("on", !!S.marked[i]);
    $("elim-toggle").hidden = q.type !== "mc";
    // Two panes, like the real test: a Reading and Writing passage, or a grid-in question's entry directions, on the
    // left; the question on the right. Multiple-choice Math stays in one column.
    var split = !!q.passage || q.type === "spr";
    $("q-view").classList.toggle("is-split", split);
    $("q-divider").hidden = !split;
    $("q-passage").hidden = !split;
    if (q.passage) { $("q-passage").innerHTML = q.passage; paintNotes(i); }
    else if (split) {
      $("q-passage").innerHTML = $("spr-directions").innerHTML;
      if (window.matchMedia("(max-width: 860px)").matches) $("q-passage").querySelector("details").open = false;
    } else $("q-passage").innerHTML = "";
    $("q-stem").innerHTML = q.passage ? q.prompt : q.stem;
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
      var inp = document.createElement("input"); inp.type = "text"; inp.id = "spr-input"; inp.setAttribute("data-no-filter", ""); inp.autocomplete = "off"; inp.inputMode = "text"; inp.spellcheck = false;
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
    var verdict = g.correct ? PRAISE[i % PRAISE.length] : "Not quite, and that's how you learn.";
    area.innerHTML = '<div class="fb ' + (g.correct ? "ok" : "no") + '" tabindex="-1" id="fb"><p class="fb-verdict"><strong>' + verdict + "</strong>" +
      (g.correct ? "" : ' <span>The answer is <strong>' + (g.type === "mc" ? g.answer : previewHTML(g.answer.split(" or ")[0])) + "</strong>. Here's how to get there.</span>") + "</p>" +
      '<div class="fb-explain"></div></div>';
    area.querySelector(".fb-explain").innerHTML = g.explain_html || "";
    if (tools) {
      var ask = document.createElement("button"); ask.type = "button"; ask.className = "btn btn-quiet ask-tutor";
      ask.textContent = g.correct ? "Ask the tutor about this one" : "Ask the tutor where it went wrong";
      ask.addEventListener("click", function () { tools.context({ title: "Question " + (i + 1), detail: Q[i].skill || Q[i].domain || "" }); tools.open("tutor"); });
      area.querySelector(".fb").appendChild(ask);
    }
    if (g.game) {
      var line = document.createElement("p"); line.className = "fb-reward";
      line.textContent = "+" + g.game.xp + " XP" + (g.game.combo > 1 ? " · combo ×" + g.game.combo : "") +
        (g.game.coins ? " · +" + g.game.coins + (g.game.coins === 1 ? " coin" : " coins") : "") + (g.game.boss && g.correct ? " · boss beaten" : "");
      area.querySelector(".fb-verdict").insertAdjacentElement("afterend", line);
    }
  }
  // Level up: the boss question and the current combo, next to the question number.
  function comboAt(i) { var n = 0; while (i >= 0 && checked[i] && checked[i].correct) { n++; i--; } return n; }
  function renderGameTag(i) {
    var tag = $("q-game");
    if (!LEVEL) { if (tag) tag.hidden = true; return; }
    if (!tag) {
      tag = document.createElement("span"); tag.id = "q-game"; tag.className = "q-game";
      $("q-num").insertAdjacentElement("afterend", tag);
    }
    var boss = i === (LEVEL.boss != null ? LEVEL.boss : N - 1);
    var last = -1; for (var k = 0; k < N; k++) if (checked[k]) last = k;
    var combo = last >= 0 ? comboAt(last) : 0;
    tag.className = "q-game" + (boss ? " is-boss" : "");
    tag.innerHTML = (boss ? "<strong>Boss question</strong><span>Hardest of the level · bonus XP and coins</span>" : "") +
      (combo > 1 && !boss ? "<span>Combo ×" + combo + "</span>" : "");
    tag.hidden = !boss && combo < 2;
  }
  var PRAISE = ["Nice work!", "You got it!", "Correct!", "Nailed it.", "That's right!", "Spot on."];
  function checkAnswer() {
    var i = S.cur;
    if (checking || checked[i] || !isAnswered(i)) return;
    checking = true; renderCheck();
    practiceCall("/api/practice/sessions/" + T.session.id + "/check", { index: i, answer: S.answers[i] })
      .then(function (r) {
        checked[i] = r.question; S.answers[i] = answerValue(r.question);
        if (r.finished && r.finished.length) S.finished = r.finished;
        save();
        checking = false;
        if (S.cur === i) { renderQuestion(); var fb = $("fb"); if (fb) fb.focus({ preventScroll: false }); }
        renderNav();
        var rv = r.question.review;
        if (rv) toast(rv.cleared ? "Cleared from your review queue. Right twice means it stuck." : "Nice. One more right answer clears it. It comes back in 3 days.");
        celebrate(r.finished);
        if (r.question.game && window.GraphiteRewards) GraphiteRewards.show(r.question.game, { quick: true });
      })
      .catch(function (err) {
        checking = false; renderCheck();
        if (err && err.status === 401) { save(); location.href = "/signin.html?next=" + encodeURIComponent("/practice-test.html?session=" + T.session.id); return; }
        toast(err && err.status ? err.message : "We couldn't check that answer. Check your connection and try again.");
      });
  }
  function focusChoice(k) { var b = $("q-answer").querySelectorAll(".mc-choice")[k]; if (b) b.focus(); }

  /* ---------- annotate: highlight words in a passage and leave a note (Reading and Writing) ----------
     Notes are kept per question as character offsets into the passage text: S.notes[i] = [{s, e, note}]. */
  var passageBox = $("q-passage"), annoAt = null, lastSel = null;
  $("annotate-btn").hidden = !RW;
  function textOffset(node, offset) {
    var r = document.createRange(); r.selectNodeContents(passageBox); r.setEnd(node, offset);
    return r.toString().length;
  }
  function wrapRange(s, e, k, note) {
    var walker = document.createTreeWalker(passageBox, NodeFilter.SHOW_TEXT), pos = 0, n, parts = [];
    while ((n = walker.nextNode())) {
      var len = n.nodeValue.length, a = Math.max(s, pos), b = Math.min(e, pos + len);
      // Text inside a graph (SVG) or the screen-reader copy of its data can't hold a highlight.
      if (a < b && !n.parentNode.closest("svg, .visually-hidden")) parts.push([n, a - pos, b - pos]);
      pos += len;
    }
    parts.forEach(function (p) {
      var node = p[0];
      if (p[2] < node.nodeValue.length) node.splitText(p[2]);
      if (p[1] > 0) node = node.splitText(p[1]);
      var m = document.createElement("mark");
      m.className = "anno" + (note ? " has-note" : ""); m.setAttribute("data-k", String(k)); m.tabIndex = 0;
      m.setAttribute("aria-label", note ? "Highlight with a note: " + note : "Highlighted text");
      if (note) m.title = note;
      node.parentNode.insertBefore(m, node); m.appendChild(node);
    });
  }
  function paintNotes(i) { (S.notes && S.notes[i] || []).forEach(function (n, k) { wrapRange(n.s, n.e, k, n.note); }); }
  function repaint() { var q = Q[S.cur]; if (q.passage) { passageBox.innerHTML = q.passage; paintNotes(S.cur); } }
  document.addEventListener("selectionchange", function () {
    var sel = window.getSelection();
    if (!sel.rangeCount || sel.isCollapsed) return;
    var r = sel.getRangeAt(0);
    if (!passageBox.contains(r.commonAncestorContainer)) return;
    lastSel = { s: textOffset(r.startContainer, r.startOffset), e: textOffset(r.endContainer, r.endOffset), at: S.cur };
  });
  function openNote(k) {
    var n = S.notes[S.cur][k];
    annoAt = k;
    var text = passageBox.textContent.slice(n.s, n.e).replace(/\s+/g, " ").trim();
    $("anno-quote").textContent = "\u201C" + (text.length > 140 ? text.slice(0, 140) + "\u2026" : text) + "\u201D";
    $("anno-text").value = n.note || "";
    $("anno-pop").hidden = false;
    $("anno-text").focus();
  }
  function closeNote() { $("anno-pop").hidden = true; annoAt = null; }
  $("annotate-btn").addEventListener("click", function () {
    var sel = lastSel && lastSel.at === S.cur && lastSel.e > lastSel.s ? lastSel : null;
    if (!sel || !Q[S.cur].passage) { toast("Select words in the passage first, then press Annotate."); return; }
    S.notes = S.notes || {};
    var list = S.notes[S.cur] = S.notes[S.cur] || [];
    var hit = list.map(function (n, k) { return n.s < sel.e && sel.s < n.e ? k : -1; }).filter(function (k) { return k >= 0; })[0];
    if (hit === undefined) { list.push({ s: sel.s, e: sel.e, note: "" }); hit = list.length - 1; save(); repaint(); }
    window.getSelection().removeAllRanges(); lastSel = null;
    openNote(hit);
  });
  passageBox.addEventListener("click", function (e) {
    var m = e.target.closest("mark.anno"); if (m) openNote(Number(m.getAttribute("data-k")));
  });
  passageBox.addEventListener("keydown", function (e) {
    var m = e.target.closest && e.target.closest("mark.anno");
    if (m && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); openNote(Number(m.getAttribute("data-k"))); }
  });
  $("anno-save").addEventListener("click", function () {
    if (annoAt === null) return;
    S.notes[S.cur][annoAt].note = $("anno-text").value.trim().slice(0, 500);
    save(); repaint(); closeNote();
  });
  $("anno-delete").addEventListener("click", function () {
    if (annoAt === null) return;
    S.notes[S.cur].splice(annoAt, 1);
    save(); repaint(); closeNote();
  });
  $("anno-close").addEventListener("click", closeNote);

  /* ---------- the divider between the panes: drag it, use the arrow keys, or press a side's button to widen it ---------- */
  var SPLIT_KEY = "graphite_split";
  var leftShare = 50;
  try { leftShare = Number(localStorage.getItem(SPLIT_KEY)) || 50; } catch (e) { /* storage blocked */ }
  function setSplit(v) {
    leftShare = Math.max(25, Math.min(75, Math.round(v)));
    $("q-view").style.setProperty("--left", leftShare + "fr"); $("q-view").style.setProperty("--right", (100 - leftShare) + "fr");
    $("q-divider").setAttribute("aria-valuenow", String(leftShare));
    try { localStorage.setItem(SPLIT_KEY, String(leftShare)); } catch (e) { /* storage blocked */ }
  }
  setSplit(leftShare);
  $("widen-left").addEventListener("click", function () { setSplit(leftShare >= 70 ? 50 : 70); });
  $("widen-right").addEventListener("click", function () { setSplit(leftShare <= 30 ? 50 : 30); });
  $("q-divider").addEventListener("keydown", function (e) {
    if (e.target !== $("q-divider")) return;
    if (e.key === "ArrowLeft") { e.preventDefault(); setSplit(leftShare - 5); }
    if (e.key === "ArrowRight") { e.preventDefault(); setSplit(leftShare + 5); }
  });
  $("q-divider").addEventListener("pointerdown", function (e) {
    if (e.target.closest("button")) return;
    e.preventDefault();
    var box = $("q-view").getBoundingClientRect();
    function move(ev) { setSplit((ev.clientX - box.left) / box.width * 100); }
    function up() { document.removeEventListener("pointermove", move); document.removeEventListener("pointerup", up); }
    document.addEventListener("pointermove", move); document.addEventListener("pointerup", up);
  });

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
    $("exam").classList.toggle("is-results", p === "results");  // hides the clock, which stopped at submit
    $("next-btn").hidden = p !== "q";
    $("back-btn").hidden = p === "results";
    $("back-btn").disabled = p === "q" && S.cur === 0;
    $("submit-confirm").hidden = true;
    if (p === "review") { renderReview(); $("nav-label").textContent = "Review page"; }
    if (p === "q") renderQuestion();
    $("q-area").scrollTop = 0;
    tutorRules(); tutorContext();
  }
  function goTo(i) { closeNote(); S.cur = Math.max(0, Math.min(N - 1, i)); showPage("q"); renderNav(); $("q-area").focus({ preventScroll: true }); }

  /* ---------- submit & results ---------- */
  function submit(auto) {
    if (S.submitted || submitting) return;
    clearInterval(tickTimer);
    var seconds = UNTIMED ? (S.elapsed || 0) : T.minutes * 60 - S.remaining;
    var finish = function (result) {
      S.submitted = true; S.result = result; save();
      tutorRules();
      if (MOCK && MOCK.module === 1) { showNext((result.mock && result.mock.next_session) || MOCK.m2_session, auto); return; }
      if (auto) toast("Time's up. Your module was submitted.");
      renderResults(result); showPage("results");
      closePopup();
      celebrate(result.finished);
      if (result.game && window.GraphiteRewards) GraphiteRewards.show(result.game);
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
  /* ---------- finishing a topic ---------- */
  // finished: [{kind: "skill" | "domain", name}] from the server, for topics this answer or set completed.
  function finishedText(list) {
    return list.map(function (t) {
      return "You've answered every question in " + t.name + (t.kind === "domain" ? ", the whole domain." : ".");
    }).join(" ");
  }
  function celebrate(list) {
    if (!list || !list.length) return;
    $("done-title").textContent = "Congratulations! You have finished " + (list.length > 1 || list[0].kind === "domain" ? "a whole domain" : "this topic") + "!";
    $("done-text").textContent = finishedText(list);
    openDialog("done-dialog");
  }
  // Level up: did this set pass, and what's next.
  function renderLevel(lv, gm) {
    var box = $("res-level");
    box.hidden = !lv;
    if (!lv) return;
    box.classList.toggle("is-pass", lv.passed);
    var head = lv.passed ? (lv.next ? "Level " + lv.level + " passed! Level " + lv.next + " is unlocked." : "You cleared the top level of " + lv.track_name + "!")
      : "Not quite. You need " + lv.pass + " of " + lv.total + " to pass level " + lv.level + ".";
    var sub = lv.passed ? (lv.next ? "The next set is a little harder. Keep the streak going." : "Every level in this track is done. Try another track, or replay a level with new questions.")
      : "Read the explanations below, then try the level again with new questions.";
    box.innerHTML = "<strong></strong><span></span>";
    box.querySelector("strong").textContent = head;
    box.querySelector("span").textContent = sub;
    if (gm && window.GraphiteRewards) {
      var rw = document.createElement("div"); rw.className = "res-reward";
      rw.innerHTML = '<p class="res-reward-total"><strong>+' + GraphiteRewards.num(gm.set_xp) + " XP</strong>" +
        (gm.set_coins ? ' <span><i class="coin" aria-hidden="true"></i>+' + gm.set_coins + (gm.set_coins === 1 ? " coin" : " coins") + "</span>" : "") +
        ' <a href="rewards.html">Rank: ' + GraphiteRewards.esc(gm.rank.name) + "</a></p>" + GraphiteRewards.lines(gm.lines);
      box.appendChild(rw);
    }
    var b = $("retake");
    b.hidden = false;
    b.setAttribute("data-level", String(lv.passed && lv.next ? lv.next : lv.level));
    b.textContent = lv.passed && lv.next ? "Start level " + lv.next : "Try level " + lv.level + " again";
    // The same button up top, so the next step is right under the score.
    var go = document.createElement("button");
    go.type = "button"; go.className = "btn " + (lv.passed ? "btn-primary" : "btn-secondary");
    go.textContent = b.textContent;
    go.addEventListener("click", function () { go.disabled = true; go.textContent = "Building your set…"; b.click(); });
    box.appendChild(go);
  }

  function renderResults(r) {
    var marked = 0;
    var fin = r.finished && r.finished.length ? r.finished : (S.finished || []);
    $("res-finished").hidden = !fin.length;
    if (fin.length) $("res-finished").innerHTML = "<strong>Congratulations! You have finished " + (fin.length > 1 || fin[0].kind === "domain" ? "a whole domain" : "this topic") + "!</strong> <span></span>";
    if (fin.length) $("res-finished").querySelector("span").textContent = finishedText(fin);
    renderLevel(r.level, r.game);
    renderMockScore(r);
    for (var m = 0; m < N; m++) if (S.marked[m]) marked++;
    var pct = r.total ? r.correct / r.total : 0;
    var cheer = pct >= 0.9 ? "Outstanding!" : pct >= 0.7 ? "Solid work!" : pct >= 0.5 ? "Good effort." : "Every miss shows you what to practice.";
    $("results-title").textContent = cheer + " You got " + r.correct + " of " + r.total + " right.";
    $("res-time").textContent = fmt(r.seconds_used);
    $("res-mc").textContent = r.multiple_choice.right + " of " + r.multiple_choice.total;
    $("res-spr").textContent = r.student_produced.right + " of " + r.student_produced.total;
    $("res-spr").parentNode.hidden = !r.student_produced.total;  // Reading and Writing is all multiple choice
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
      d.querySelector(".res-dom").textContent = (q.module ? "Module " + q.module + " · " : "") + (q.skill && T.session ? q.skill : q.domain);
      if (q.explain_html) d.querySelector(".res-explain").innerHTML = q.explain_html;
      else d.querySelector(".res-explain").textContent = q.explain || "";
      if (q.calc) d.querySelector(".res-calc span").textContent = q.calc;
      if (tools) {
        var ask = document.createElement("button"); ask.type = "button"; ask.className = "btn btn-quiet ask-tutor";
        ask.textContent = q.correct ? "Ask the tutor about it" : "Ask the tutor where it went wrong";
        ask.addEventListener("click", function () { tools.context({ title: "Question " + (q.index + 1), detail: q.skill || q.domain || "" }); tools.open("tutor"); });
        d.querySelector(".res-body").appendChild(ask);
      }
      list.appendChild(d);
    });
  }

  /* ---------- calculator and tutor (qtools.js): a floating window; the question reflows beside it ---------- */
  var tools = window.GraphiteTools && window.GraphiteTools.mount({ shift: ".exam-body", top: ".exam-top", bottom: ".exam-bottom", launcher: false,
    light: function () { return S.view === "light"; } });
  function themeCalc() { if (tools) tools.theme(); }
  // Timed tests keep the tutor closed until you submit, so the score stays your own work.
  function tutorRules() {
    // Timed tests have no tutor at all until the whole test is over (a mock test: after Module 2).
    var off = !TOPIC && (!S.submitted || (MOCK && MOCK.module === 1));
    document.documentElement.classList.toggle("no-tutor", !!off);
    if (!tools) return;
    tools.tutorAllowed(!off, "The tutor isn't available during a timed test, so your score stays your own work. Every question is waiting for you in the review.");
    if (off && tools.tab && tools.tab() === "tutor") tools.close();
  }
  function tutorContext() {
    if (!tools) return;
    var q = Q[S.cur];
    if (S.page === "results") tools.context({ title: "Your results", detail: "Ask about any question you missed." });
    else if (q) tools.context({ title: "Question " + (S.cur + 1), detail: q.skill || q.domain || "" });
  }
  function setCalc(open) { if (tools) { if (open) tools.open("calc"); else tools.close(); } }
  function closePopup() { /* the calculator never leaves the page anymore */ }

  /* ---------- mock tests: the step to Module 2, and the break between the modules ---------- */
  var breakTimer = null;
  function breakCall(action) { return practiceCall("/api/mock-tests/" + MOCK.id + "/break", { action: action }); }
  function showBreak() {
    $("start-overlay").hidden = true; $("break-overlay").hidden = false;
    var left = MOCK.break_left, until = Date.now() + left * 1000;
    function tick() {
      left = Math.max(0, Math.round((until - Date.now()) / 1000));
      $("break-clock").textContent = fmt(left);
      if (!left) endBreak(true);
    }
    tick();
    clearInterval(breakTimer); breakTimer = setInterval(tick, 1000);
    if (!MOCK.break_started) breakCall("start").then(function (r) { MOCK = Object.assign(MOCK, r.mock); }).catch(function () { /* the clock still runs here */ });
    $("break-resume").focus();
  }
  function endBreak(auto) {
    clearInterval(breakTimer);
    breakCall("end").catch(function () { /* the server ends it on its own clock too */ });
    MOCK.status = "module2";
    $("break-overlay").hidden = true; $("start-overlay").hidden = false;
    if (auto) toast("The break is over. Module 2 starts when you begin.");
    $("start-btn").focus();
  }
  function showNext(sessionId, auto) {
    $("start-overlay").hidden = true;
    $("next-go").setAttribute("href", "practice-test.html?session=" + sessionId);
    $("next-title").textContent = auto ? "Time's up for Module 1" : "Module 1 is done";
    if (MOCK.with_break) $("next-go").textContent = "Start the 10-minute break";
    $("next-overlay").hidden = false;
    $("next-go").focus();
  }
  function renderMockScore(r) {
    var box = $("res-mock");
    box.hidden = r.score == null;
    if (r.score == null) return;
    var m = r.modules || [];
    box.innerHTML = '<p class="label">Estimated ' + SECTION + ' score</p><p class="res-score"><strong></strong><span>out of 800</span></p><p class="res-modules"></p>' +
      '<p class="fine">An estimate from how many you got right in each module, using our own questions. It isn\'t an official College Board score.</p>';
    box.querySelector("strong").textContent = String(r.score);
    box.querySelector(".res-modules").textContent = m.map(function (x) {
      return "Module " + x.n + (x.route ? " (" + x.route + ")" : "") + ": " + x.correct + " of " + x.total;
    }).join(" · ");
  }

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
    if (!$("anno-pop").hidden) { closeNote(); $("annotate-btn").focus(); }
    else if (!$("done-dialog").hidden) closeDialog($("done-dialog"));
    else if (!$("dir-dialog").hidden) closeDialog($("dir-dialog"));
    else if (!$("ref-dialog").hidden) closeDialog($("ref-dialog"));
    else if (!$("nav-pop").hidden) { closeNav(); $("nav-toggle").focus(); }
    else if (!$("more-menu").hidden) { $("more-menu").hidden = true; $("more-toggle").setAttribute("aria-expanded", "false"); $("more-toggle").focus(); }
  });

  /* ---------- wire controls ---------- */
  $("break-resume").addEventListener("click", function () { endBreak(false); });
  $("start-btn").addEventListener("click", function () {
    S.started = true; save();
    if (tools) tools.resetCalc();  // a new attempt starts with a blank calculator, like test day
    $("start-overlay").hidden = true; startClock(); renderTimer();
    $("q-area").focus({ preventScroll: true });
    if (!RW && window.GraphiteTheme && GraphiteTheme.prefs().study.calculator === "open") setCalc(true);  // Settings > Practice defaults
  });
  $("timer-toggle").addEventListener("click", function () { S.timerHidden = !S.timerHidden; save(); renderTimer(); });
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
    if (FROM_PLAN) { location.href = "plan.html"; return; }
    var s = T.session, b = $("retake");
    var data = s.mode === "test" ? { mode: "test", section: RW ? "rw" : "math" } : { mode: "topic", domain: s.domain, skill: s.skill, count: N };
    var url = "/api/practice/sessions";
    if (MOCK) { url = "/api/mock-tests"; data = { section: MOCK.section, with_break: MOCK.with_break }; }
    if (LEVEL) { url = "/api/levels/start"; data = { track: LEVEL.track, level: Number(b.getAttribute("data-level")) || LEVEL.n }; }
    var label = b.textContent;
    b.disabled = true; b.textContent = "Building your set…";
    practiceCall(url, data).then(function (r) {
      location.href = "practice-test.html?session=" + (r.mock ? r.mock.m1_session : r.session.id);
    }).catch(function (err) {
      b.disabled = false; b.textContent = label;
      if (window.GraphiteLock && GraphiteLock.handle(err)) return;
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
    // Like Bluebook: Reading and Writing is Section 1, Math is Section 2.
    var heading = MOCK ? "Section " + (RW ? 1 : 2) + ", Module " + MOCK.module + ": " + SECTION : T.mode === "test" ? SECTION + " module" : T.title;
    var kind = MOCK ? "Mock test · " + SECTION + " · Module " + MOCK.module + " of 2" : REVIEW ? "Review queue · one question" : LEVEL ? "Level up · " + LEVEL.tier : FROM_PLAN ? "Study plan · " + (T.mode === "test" ? SECTION + " practice test" : T.title)
      : (T.mode === "test" ? "Mock test · one " + SECTION + " module" : "Topic practice · " + (T.session.skill ? "one skill" : "whole domain"));
    $("exam-title").textContent = heading;
    $("start-title").textContent = heading;
    document.querySelector("#start-overlay .label").textContent = kind;
    document.querySelector("#results-view > .label").textContent = kind;
    $("review-heading").textContent = heading + " questions";
    document.querySelector("#nav-pop .review-card-head strong").textContent = heading + " questions";
    var facts = '<li><strong>' + N + "</strong> questions</li>" +
      (UNTIMED ? "<li>Untimed. The clock counts up so you can see your pace</li><li>Check each answer as you go</li>"
               : "<li><strong>" + T.minutes + "</strong> minutes</li><li>" + (RW ? "One short passage per question, all multiple choice" : "Graphing calculator on every question") + "</li>" +
                 (MOCK ? "<li>" + (MOCK.module === 1 ? "Module 2 adapts to how this one goes" : "The last module: your score comes next") + "</li>" : "") +
                 "<li>No tutor until the test is over</li>");
    document.querySelector("#start-overlay .start-facts").innerHTML = facts;
    var intro = document.querySelector("#start-overlay .dialog > p:not(.label)");
    if (intro) intro.textContent = MOCK
      ? (MOCK.module === 1 ? "This module mixes easy, medium and hard questions. How it goes decides Module 2: harder after a strong start, easier otherwise, like the real test. The timer starts when you begin, and the module submits itself when time runs out."
        : "Module 2 is " + "built from how Module 1 went. You can't go back to Module 1. When you submit, you'll see your estimated " + SECTION + " score and every explanation.")
      : LEVEL
      ? "Get " + LEVEL.pass + " of " + N + " right to pass" + (LEVEL.n < LEVEL.top ? " and unlock level " + (LEVEL.n + 1) : " the top level") + ". Check each answer as you go and read the full explanation right away."
      : UNTIMED
      ? (RW ? "Answer a question, then press Check answer to see if you got it, why, and a strategy for that kind of question. Your progress saves as you go."
            : "Answer a question, then press Check answer to see if you got it and read the full explanation, with the Desmos shortcut when one helps. Your progress saves as you go.")
      : "New questions you haven't answered before, in the same mix as the real test. The timer starts when you begin. Your answers save as you go, and the module submits itself when time runs out.";
    $("start-btn").textContent = UNTIMED ? "Start practicing" : MOCK ? "Begin Module " + MOCK.module : "Begin module";
    $("submit-open").textContent = TOPIC ? "Finish set" : "Submit module";
    $("confirm-title").textContent = TOPIC ? "Finish this set?" : "Submit this module?";
    if (TOPIC) $("confirm-desc").textContent = "Questions you haven't answered go back into the pool for next time.";
    $("retake").textContent = FROM_PLAN ? "Back to your plan" : LEVEL ? "Try this level again" : MOCK ? "Take another mock test" : (TOPIC ? "New set, same topic" : "Take another module");
    if (MOCK && MOCK.module === 2) document.querySelector("#results-view > .label").textContent = "Mock test · " + SECTION + " · both modules";
    if (RW) {
      $("next-text").textContent = "Module 2 is ready: " + N + " questions and " + T.minutes + " minutes. Like on test day, you can't go back to Module 1. Your score comes at the end of Module 2.";
      document.querySelector("#next-overlay .label").textContent = "Mock test · " + SECTION;
    }
    Array.prototype.forEach.call(document.querySelectorAll('a[href$="dashboard.html"]'), function (a) {
      if (a.id === "save-exit" || a.closest(".dialog-actions")) a.setAttribute("href", BACK_URL);
    });
    var backText = FROM_PLAN ? "Back to your plan" : LEVEL ? "Back to Level up" : "Back to mock tests";
    var back = document.querySelector(".res-actions a"); if (back) { back.setAttribute("href", BACK_URL); back.textContent = backText; }
    if (FROM_PLAN || REVIEW) { var r2 = $("retake"); r2.hidden = true; }
    if (REVIEW && back) back.textContent = "Back to your dashboard";
    var doneLink = document.querySelector("#done-dialog a");
    if (doneLink) { doneLink.setAttribute("href", BACK_URL); doneLink.textContent = backText; }
    document.title = heading + " | Graphite SAT";
  }

  /* ---------- boot ---------- */
  applyView(); renderTimer();
  if (S.submitted && !S.result) { S = fresh(); save(); }
  if (S.submitted && MOCK && MOCK.module === 1) { tutorRules(); showNext(MOCK.m2_session || (S.result && S.result.mock && S.result.mock.next_session), false); }
  else if (S.submitted) { renderResults(S.result); showPage("results"); $("start-overlay").hidden = true; }
  else if (MOCK && MOCK.module === 2 && MOCK.status === "break" && !S.started) { showPage("q"); renderNav(); tutorRules(); showBreak(); }
  else {
    showPage(S.page === "review" ? "review" : "q"); renderNav();
    if (S.started) { $("start-overlay").hidden = true; startClock(); if (resumed) toast(UNTIMED ? "Picked up where you left off." : "Picked up where you left off. " + fmt(S.remaining) + " left."); }
  }
  }
})();
