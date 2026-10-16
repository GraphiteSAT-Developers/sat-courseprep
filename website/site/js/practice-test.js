/* Graphite practice test engine. Reads GRAPHITE_TEST from questions.js. */
(function () {
  "use strict";
  var T = window.GRAPHITE_TEST;
  var root = document.getElementById("exam");
  if (!T || !root) return;

  var Q = T.questions, N = Q.length, LETTERS = "ABCD";
  var KEY = "graphite_test_" + T.id;
  function $(id) { return document.getElementById(id); }
  function load() { try { return JSON.parse(localStorage.getItem(KEY)); } catch (e) { return null; } }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) { /* storage blocked */ } }
  function fresh() {
    return { started: false, submitted: false, cur: 0, remaining: T.minutes * 60, answers: {}, crossed: {}, marked: {}, view: "graphite", timerHidden: false, page: "q" };
  }
  var S = load() || fresh();
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
  function isCorrect(i) {
    var q = Q[i], a = S.answers[i];
    if (!isAnswered(i)) return false;
    if (q.type === "mc") return a === q.answer;
    var v = sprValue(a); return v !== null && Math.abs(v - q.answer) < 1e-9;
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
    var elimOn = $("elim-toggle").getAttribute("aria-pressed") === "true";

    if (q.type === "mc") {
      var list = document.createElement("div");
      list.className = "mc"; list.setAttribute("role", "radiogroup"); list.setAttribute("aria-label", "Answer choices for question " + (i + 1));
      var crossed = S.crossed[i] || {};
      q.choices.forEach(function (c, k) {
        var row = document.createElement("div"); row.className = "mc-row" + (crossed[k] ? " is-crossed" : "");
        var b = document.createElement("button"); b.type = "button"; b.className = "mc-choice";
        b.setAttribute("role", "radio"); b.setAttribute("aria-checked", String(S.answers[i] === k));
        b.innerHTML = '<span class="mc-letter">' + LETTERS[k] + '</span><span class="mc-text">' + c + "</span>";
        b.addEventListener("click", function () {
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
      inp.maxLength = 6; inp.value = S.answers[i] || "";
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
        S.answers[i] = v; save(); renderNav();
      }
      inp.addEventListener("input", update);
      wrap.appendChild(lab); wrap.appendChild(inp); wrap.appendChild(prev); wrap.appendChild(err);
      box.appendChild(wrap);
      prev.innerHTML = inp.value ? "Answer Preview: <strong>" + previewHTML(inp.value) + "</strong>" : "Answer Preview:";
    }
    $("back-btn").disabled = i === 0 && S.page === "q";
    $("nav-label").textContent = "Question " + (i + 1) + " of " + N;
  }
  function focusChoice(k) { var b = $("q-answer").querySelectorAll(".mc-choice")[k]; if (b) b.focus(); }

  /* ---------- navigator & review ---------- */
  function buildGrid(el, closeAfter) {
    el.innerHTML = "";
    for (var i = 0; i < N; i++) {
      (function (i) {
        var b = document.createElement("button"); b.type = "button"; b.className = "g-cell";
        if (isAnswered(i)) b.classList.add("is-answered");
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
    if (S.submitted) return;
    S.submitted = true; clearInterval(tickTimer); save();
    if (auto) toast("Time's up. Your module was submitted.");
    renderResults(); showPage("results");
  }
  function renderResults() {
    var right = 0, mcR = 0, sprR = 0, mcN = 0, sprN = 0, marked = 0, dom = {};
    Q.forEach(function (q, i) {
      var ok = isCorrect(i);
      if (ok) right++;
      if (q.type === "mc") { mcN++; if (ok) mcR++; } else { sprN++; if (ok) sprR++; }
      if (S.marked[i]) marked++;
      dom[q.domain] = dom[q.domain] || { r: 0, n: 0 }; dom[q.domain].n++; if (ok) dom[q.domain].r++;
    });
    $("res-correct").textContent = String(right);
    $("res-time").textContent = fmt(T.minutes * 60 - S.remaining);
    $("res-mc").textContent = mcR + " of " + mcN;
    $("res-spr").textContent = sprR + " of " + sprN;
    $("res-marked").textContent = String(marked);

    var bars = $("res-domains"); bars.innerHTML = "";
    Object.keys(dom).forEach(function (d) {
      var pct = Math.round(dom[d].r / dom[d].n * 100);
      var li = document.createElement("li");
      li.innerHTML = '<span class="bar-name"></span><span class="bar-track"><span style="width:' + pct + '%"></span></span><span class="bar-val">' + dom[d].r + "/" + dom[d].n + "</span>";
      li.querySelector(".bar-name").textContent = d;
      bars.appendChild(li);
    });

    var list = $("res-list"); list.innerHTML = "";
    Q.forEach(function (q, i) {
      var ok = isCorrect(i), a = S.answers[i];
      var yours = !isAnswered(i) ? "No answer" : (q.type === "mc" ? LETTERS[a] : previewHTML(a));
      var correct = q.type === "mc" ? LETTERS[q.answer] : String(q.answer).replace(/^-/, "−");
      var d = document.createElement("details"); d.className = "res-item " + (ok ? "ok" : "no");
      d.innerHTML = '<summary><span class="res-n">' + (i + 1) + '</span><span class="res-verdict">' + (ok ? "Correct" : (isAnswered(i) ? "Incorrect" : "Skipped")) +
        '</span><span class="res-dom"></span><span class="res-ans">Yours: <strong>' + yours + "</strong> · Answer: <strong>" + correct + "</strong></span></summary>" +
        '<div class="res-body"><div class="res-stem">' + q.stem + "</div>" +
        (q.type === "mc" ? '<ol class="res-choices" type="A">' + q.choices.map(function (c, k) { return '<li class="' + (k === q.answer ? "is-key" : "") + '">' + c + "</li>"; }).join("") + "</ol>" : "") +
        '<p class="res-explain"></p>' + (q.calc ? '<p class="res-calc"><strong>With the calculator:</strong> <span></span></p>' : "") + "</div>";
      d.querySelector(".res-dom").textContent = q.domain;
      d.querySelector(".res-explain").textContent = q.explain;
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
  $("retake").addEventListener("click", reset);

  function reset() {
    var view = S.view; S = fresh(); S.view = view; save();
    clearInterval(tickTimer); restartArmed = false;
    $("restart-test").textContent = "Start over"; $("more-menu").hidden = true;
    applyView(); renderTimer(); showPage("q"); renderNav();
    $("start-overlay").hidden = false; $("start-btn").focus();
  }

  /* ---------- boot ---------- */
  applyView(); renderTimer();
  if (S.submitted) { renderResults(); showPage("results"); $("start-overlay").hidden = true; }
  else {
    showPage(S.page === "review" ? "review" : "q"); renderNav();
    if (S.started) { $("start-overlay").hidden = true; startClock(); if (resumed) toast("Picked up where you left off. " + fmt(S.remaining) + " left."); }
  }
})();
