/* Graphite SAT study plan: the 10-question diagnostic, its results, and the week-by-week plan.
   Live: talks to /api/plan. Preview: the same requests go to GraphitePracticeLocal (practice-local.js). */
(function () {
  "use strict";
  var root = document.getElementById("pl-done");
  if (!root) return;
  function $(id) { return document.getElementById(id); }
  var API = window.GraphiteAPI;
  var LIVE = !!(API && API.live);
  var call = LIVE ? API.call : (window.GraphitePracticeLocal && window.GraphitePracticeLocal.call);
  var LETTERS = "ABCD";
  var state = null, diag = null, pos = 0, saved = null, busy = false;

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function today() { var d = new Date(); return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0"); }
  function niceDate(iso, long) { return new Date(iso + "T12:00:00").toLocaleDateString("en-US", long ? { weekday: "long", month: "long", day: "numeric" } : { month: "short", day: "numeric" }); }
  function showError(msg) { $("pl-error").textContent = msg || ""; $("pl-error").hidden = !msg; }
  function failed(err, fallback) {
    if (err && err.status === 401) { location.href = "/signin.html?next=/plan.html"; return; }
    if (window.GraphiteLock && GraphiteLock.handle(err)) return;
    showError(err && err.status ? err.message : fallback);
  }
  function view(name) {
    $("pl-loading").hidden = true;
    $("pl-intro").hidden = name !== "intro";
    $("pl-quiz").hidden = name !== "quiz";
    $("pl-done").hidden = name !== "done";
    if (name !== "quiz") setCalc(false);
  }
  function store(k, v) { try { if (v === undefined) return JSON.parse(localStorage.getItem(k)); localStorage.setItem(k, JSON.stringify(v)); } catch (e) { return null; } }

  if (!LIVE) $("pl-preview-note").hidden = false;
  if (!LIVE) store("graphite_diag_prompted", true);
  if (/[?&]welcome=1/.test(location.search)) {
    $("pl-intro-kicker").textContent = "Welcome to Graphite SAT";
    $("pl-intro-title").textContent = "Let's start with a quick 10-question diagnostic";
  }
  if (LIVE) API.call("/api/me").then(function (r) { $("account-email").textContent = r.user.email; }, function () {});
  else { try { $("account-email").textContent = sessionStorage.getItem("graphite_user") || ""; } catch (e) { /* storage blocked */ } }
  if (!call) { $("pl-loading").textContent = "The study plan isn't available in this preview."; return; }

  ["pl-hours", "pl-hours2"].forEach(function (id) {
    var sel = $(id);
    for (var h = 1; h <= 10; h++) {
      var o = document.createElement("option"); o.value = String(h); o.textContent = h + (h === 1 ? " hour" : " hours"); sel.appendChild(o);
    }
    sel.value = "3";
  });
  ["pl-date", "pl-date2"].forEach(function (id) { $(id).min = today(); });

  /* ---------- load ---------- */
  function load() {
    call("/api/plan?today=" + today()).then(function (r) {
      state = r;
      var u = r.user || {};
      if (u.test_date) { $("pl-date").value = u.test_date; $("pl-date2").value = u.test_date; }
      if (u.weekly_goal_hours) { $("pl-hours").value = String(Math.min(10, u.weekly_goal_hours)); $("pl-hours2").value = $("pl-hours").value; }
      var open = r.diagnostic && !r.diagnostic.submitted ? r.diagnostic : null;
      if (r.plan) {
        renderDone(r);
        $("pl-resume").hidden = !open;
        if (open) $("pl-resume-btn").onclick = function () { startQuiz(open); };
        view("done");
      } else {
        $("pl-start").textContent = open ? "Resume the diagnostic" : "Start the diagnostic";
        view("intro");
      }
    }).catch(function (err) { $("pl-loading").hidden = true; failed(err, "We couldn't load your plan. Check your connection and refresh the page."); });
  }

  $("pl-start-form").addEventListener("submit", function (e) {
    e.preventDefault();
    if (busy) return;
    busy = true; showError(""); $("pl-start").disabled = true;
    call("/api/plan/diagnostic", { test_date: $("pl-date").value || null, weekly_goal_hours: Number($("pl-hours").value) })
      .then(function (r) { startQuiz(r.diagnostic); })
      .catch(function (err) { failed(err, "We couldn't start the diagnostic. Check your connection and try again."); })
      .then(function () { busy = false; $("pl-start").disabled = false; });
  });

  /* ---------- diagnostic ---------- */
  function key() { return "graphite_diag_" + diag.id; }
  function startQuiz(d) {
    diag = d;
    saved = store(key()) || { answers: {}, sure: {}, pos: 0 };
    pos = Math.min(saved.pos || 0, d.questions.length - 1);
    view("quiz"); renderQ();
    window.scrollTo(0, 0);
  }
  function answered(i) { var a = saved.answers[i]; return a !== undefined && a !== null && a !== ""; }
  function renderQ() {
    var q = diag.questions[pos], N = diag.questions.length;
    $("pl-q-meta").textContent = "Question " + (pos + 1) + " of " + N + " · " + q.section + " · " + q.domain;
    $("pl-calc").hidden = q.section !== "Math";
    if (q.section !== "Math") setCalc(false);
    if (tools) tools.context({ title: "Diagnostic question " + (pos + 1), detail: q.domain });
    $("pl-steps").innerHTML = diag.questions.map(function (_, i) {
      return '<span class="' + (i === pos ? "is-now" : (answered(i) || saved.answers[i] === null ? "is-done" : "")) + '"></span>';
    }).join("");
    $("pl-stem").innerHTML = q.stem;
    var box = $("pl-answer"); box.innerHTML = "";
    if (q.type === "mc") {
      var list = document.createElement("div"); list.className = "choices pl-choices"; list.setAttribute("role", "radiogroup"); list.setAttribute("aria-label", "Answer choices");
      q.choices.forEach(function (c, k) {
        var b = document.createElement("button"); b.type = "button"; b.className = "mc-choice";
        b.setAttribute("role", "radio"); b.setAttribute("aria-checked", String(saved.answers[pos] === k));
        b.innerHTML = '<span class="mc-letter">' + LETTERS[k] + '</span><span class="mc-text">' + c + "</span>";
        b.addEventListener("click", function () { saved.answers[pos] = k; save(); renderQ(); list.querySelectorAll(".mc-choice")[k].focus(); });
        list.appendChild(b);
      });
      box.appendChild(list);
    } else {
      box.innerHTML = '<div class="spr"><label class="pl-small" for="pl-spr">Your answer</label><input type="text" id="pl-spr" autocomplete="off" spellcheck="false" maxlength="6"><p class="fine">Type a number, a fraction like 7/2, or a decimal.</p></div>';
      var inp = $("pl-spr"); inp.value = answered(pos) ? saved.answers[pos] : "";
      inp.addEventListener("input", function () { saved.answers[pos] = inp.value.replace(/\s+/g, ""); save(); syncNext(); });
    }
    var s = saved.sure[pos];
    $("pl-sure-yes").checked = s === true; $("pl-sure-no").checked = s === false;
    $("pl-back").disabled = pos === 0;
    $("pl-next").textContent = pos === N - 1 ? "See my results" : "Next";
    syncNext();
  }
  /* ---------- calculator (qtools.js): a panel on the right, and the question slides left ---------- */
  var tools = window.GraphiteTools && window.GraphiteTools.mount({ launcher: false });
  if (tools) tools.tutorAllowed(false, "The diagnostic measures where you are right now, so it's just you. The tutor is ready once your plan is built.");
  function setCalc(open) { if (!tools) return; if (open) tools.open("calc"); else tools.close(); }

  function syncNext() { $("pl-next").disabled = !(answered(pos) && typeof saved.sure[pos] === "boolean") || busy; }
  function save() { saved.pos = pos; store(key(), saved); }
  $("pl-sure-yes").addEventListener("change", function () { saved.sure[pos] = true; save(); syncNext(); });
  $("pl-sure-no").addEventListener("change", function () { saved.sure[pos] = false; save(); syncNext(); });
  $("pl-back").addEventListener("click", function () { if (pos > 0) { pos--; save(); renderQ(); } });
  $("pl-skip").addEventListener("click", function () { saved.answers[pos] = null; delete saved.sure[pos]; advance(); });
  $("pl-next").addEventListener("click", advance);
  function advance() {
    if (pos < diag.questions.length - 1) { pos++; save(); renderQ(); $("pl-stem").focus && window.scrollTo(0, 0); return; }
    submitDiag();
  }
  function submitDiag() {
    if (busy) return;
    busy = true; syncNext(); showError(""); $("pl-next").textContent = "Building your plan…";
    var answers = {}, sure = {};
    Object.keys(saved.answers).forEach(function (k) { if (answered(k)) { answers[k] = saved.answers[k]; sure[k] = saved.sure[k] === true; } });
    call("/api/plan/diagnostic/" + diag.id + "/submit", { answers: answers, sure: sure })
      .then(function (r) {
        try { localStorage.removeItem(key()); } catch (e) { /* storage blocked */ }
        busy = false;
        state = state || {};
        state.diagnostic = { id: diag.id, submitted: true, questions: diag.questions, results: r.results };
        state.plan = r.plan;
        if (r.access) state.access = r.access;
        renderDone(state); $("pl-resume").hidden = true; view("done"); window.scrollTo(0, 0);
      })
      .catch(function (err) { busy = false; renderQ(); failed(err, "We couldn't send your answers. Check your connection and press See my results again."); });
  }

  /* ---------- results ---------- */
  function renderDone(r) {
    var res = r.diagnostic && r.diagnostic.results;
    // A retake in progress: show the results the current plan came from, if we have them.
    if (!res && r.plan && r.plan.results) res = r.plan.results;
    if (res) renderResults(res);
    renderPlan(r.plan);
    // The diagnostic is free; the week-by-week plan comes with No. 2 and up.
    if (r.access && !r.access.ok && window.GraphiteLock) GraphiteLock.panel($("pl-plan-title").closest(".panel"), r.access);
  }
  function renderResults(res) {
    $("pl-score").textContent = res.correct + " of " + res.total + " right";
    function tags(list, empty) { return list.length ? list.map(function (n) { return "<li>" + esc(n) + "</li>"; }).join("") : '<li class="is-empty">' + empty + "</li>"; }
    $("pl-strengths").innerHTML = tags(res.strengths, "None yet. Your plan builds them.");
    $("pl-focus").innerHTML = tags(res.focus, "No big gaps. Your plan keeps every area sharp.");
    var groups = {};
    res.domains.forEach(function (d) { (groups[d.section] = groups[d.section] || []).push(d); });
    $("pl-domains").innerHTML = ["Math", "Reading and Writing"].filter(function (s) { return groups[s]; }).map(function (s) {
      return '<div><h3 class="bar-group-title">' + s + '</h3><ul class="bars">' + groups[s].map(function (d) {
        var pct = Math.round(d.score * 100);
        return '<li><span class="bar-name">' + esc(d.domain) + ' <span class="chip ' + (d.label === "Strength" ? "" : "chip-quiet") + '">' + d.label + '</span></span><span class="bar-track"><span style="width:' + pct + '%"></span></span><span class="bar-val">' + pct + "%</span></li>";
      }).join("") + "</ul></div>";
    }).join("");
    var list = $("pl-answers"); list.innerHTML = "";
    res.questions.forEach(function (q) {
      var d = document.createElement("details"); d.className = "res-item " + (q.correct ? "ok" : "no");
      var verdict = !q.answered ? "Skipped" : (q.correct ? (q.sure ? "Correct" : "Correct, guessed") : "Incorrect");
      d.innerHTML = '<summary><span class="res-n">' + (q.index + 1) + '</span><span class="res-verdict">' + verdict + '</span><span class="res-dom"></span>' +
        '<span class="res-ans">Yours: <strong>' + esc(q.your_answer || "None") + "</strong> · Answer: <strong>" + esc(q.answer) + "</strong></span></summary>" +
        '<div class="res-body"><div class="res-stem">' + q.stem + "</div>" +
        (q.type === "mc" ? '<ol class="res-choices" type="A">' + q.choices.map(function (c, k) { return '<li class="' + (k === q.answer_index ? "is-key" : "") + '">' + c + "</li>"; }).join("") + "</ol>" : "") +
        '<div class="res-explain">' + (q.explain_html || "") + "</div></div>";
      d.querySelector(".res-dom").textContent = q.section + " · " + q.skill;
      list.appendChild(d);
    });
  }

  /* ---------- plan ---------- */
  function taskState(plan, t) { return (plan.tasks || {})[t.key]; }
  function taskButton(plan, wi, t, primary) {
    var st = taskState(plan, t);
    var label = st && st.submitted ? "Do it again" : (st ? "Resume" : "Start");
    return '<button class="btn ' + (primary && !(st && st.done) ? "btn-primary" : "btn-quiet") + '" type="button" data-week="' + wi + '" data-task="' + esc(t.key) + '">' + label + "</button>";
  }
  function taskLine(plan, wi, t, primary) {
    var st = taskState(plan, t);
    var what = t.kind === "drill" ? "Skill drill · 10 questions" : (t.kind === "quiz" ? "Quiz on this week's topics · 10 questions" : "Timed Math module · 35 minutes");
    var done = st && st.done ? '<span class="pl-check">Done' + (st.submitted && st.total ? " · " + st.correct + "/" + st.total : "") + "</span>" : "";
    return '<li class="' + (st && st.done ? "is-done" : "") + '"><div><strong>' + esc(t.kind === "drill" ? "Drill: " + t.title : t.title) + "</strong>" +
      '<span class="fine">' + what + "</span></div>" + done + taskButton(plan, wi, t, primary) + "</li>";
  }
  function renderPlan(plan) {
    var weeks = plan.weeks, now = plan.current_week || 0, w = weeks[now];
    $("pl-h1").textContent = "Your SAT study plan";
    $("pl-plan-title").textContent = plan.test_date ? "Your plan to " + niceDate(plan.test_date) : "Your next " + weeks.length + " weeks";
    $("pl-plan-meta").textContent = weeks.length + (weeks.length === 1 ? " week" : " weeks") + " · " + plan.hours + " h a week";
    $("pl-summary").textContent = plan.summary;

    var firstOpen = -1;
    w.tasks.some(function (t, i) { var st = taskState(plan, t); if (!(st && st.done)) { firstOpen = i; return true; } return false; });
    var html = '<div class="pl-now-head"><p class="label">This week · Week ' + w.n + " of " + weeks.length + " · " + esc(w.phase_label) + "</p>" +
      '<h3 id="pl-now-title">' + (w.phase === "test" ? "Test week" : w.focus.map(function (f) { return esc(f.name); }).join(" + ")) + "</h3>" +
      '<p class="pl-diff"><span class="chip">' + esc(w.difficulty_label) + "</span>" + (w.review ? " <span class=\"fine\">Plus a review of " + esc(w.review.name) + "</span>" : "") + "</p></div>" +
      '<ul class="pl-tasks">' + w.tasks.map(function (t, i) { return taskLine(plan, now, t, i === firstOpen); }).join("") + "</ul>";
    if (w.checklist) html += '<ul class="pl-checklist">' + w.checklist.map(function (c) { return "<li>" + esc(c) + "</li>"; }).join("") + "</ul>";
    if (w.rw_focus) html += '<p class="fine pl-rw">Reading and Writing focus: <strong>' + esc(w.rw_focus) + "</strong>. Practice for it is coming soon.</p>";
    $("pl-now").innerHTML = html;

    $("pl-weeks").innerHTML = weeks.map(function (wk, i) {
      var cls = i < now ? "is-past" : (i === now ? "is-now" : "");
      var focus = wk.phase === "test" ? "Warm-up quiz, rest and test-day prep" : wk.focus.map(function (f) { return esc(f.name); }).join(" + ");
      var tasks = i === now ? "" : '<ul class="pl-tasks pl-tasks-small">' + wk.tasks.map(function (t) { return taskLine(plan, i, t, false); }).join("") + "</ul>";
      return '<li class="' + cls + '"><details><summary><span class="mono">Wk ' + wk.n + '</span><span class="pl-wk-date">' + niceDate(wk.week_of) +
        '</span><span class="pl-wk-focus">' + focus + '</span><span class="pl-wk-diff">' + esc(wk.phase_label) + " · " + esc(wk.difficulty_label) + (i === now ? ' <em class="now-tag">This week</em>' : "") +
        "</span></summary>" + (tasks || '<p class="fine pl-wk-note">Shown above.</p>') + "</details></li>";
    }).join("");
  }

  root.addEventListener("click", function (e) {
    var b = e.target.closest("button[data-task]");
    if (!b || busy) return;
    busy = true; showError("");
    var label = b.textContent; b.disabled = true; b.textContent = "Building…";
    call("/api/plan/tasks", { week: Number(b.getAttribute("data-week")), task: b.getAttribute("data-task") })
      .then(function (r) { location.href = "practice-test.html?session=" + r.session.id; })
      .catch(function (err) { busy = false; b.disabled = false; b.textContent = label; failed(err, "We couldn't start that. Check your connection and try again."); });
  });

  $("pl-edit-form").addEventListener("submit", function (e) {
    e.preventDefault();
    if (busy) return;
    busy = true; showError("");
    call("/api/plan/rebuild?today=" + today(), { test_date: $("pl-date2").value || null, weekly_goal_hours: Number($("pl-hours2").value) })
      .then(function () { busy = false; load(); })
      .catch(function (err) { busy = false; failed(err, "We couldn't update your plan. Check your connection and try again."); });
  });

  $("pl-retake").addEventListener("click", function () {
    if (busy) return;
    busy = true; showError("");
    call("/api/plan/diagnostic", {}).then(function (r) { busy = false; startQuiz(r.diagnostic); })
      .catch(function (err) { busy = false; failed(err, "We couldn't start the diagnostic. Check your connection and try again."); });
  });

  load();
})();
