/* The score check (score-check.html): 20 questions without an account, scored like the SAT.
   Live: questions come from /api/score-check with a signed token, and /api/score-check/grade scores them
   (services/scorecheck.py). Preview: practice-local.js answers the same two requests in the browser.
   The answers so far stay in this browser (sessionStorage), so a reload doesn't lose them. */
(function () {
  "use strict";
  var root = document.getElementById("sc-intro");
  if (!root) return;
  var API = window.GraphiteAPI;
  var call = API && API.live ? API.call : (window.GraphitePracticeLocal && window.GraphitePracticeLocal.call);
  var KEY = "graphite_score_check_v1", LETTERS = "ABCD";
  var $ = function (id) { return document.getElementById(id); };
  var S = null;  // { token, questions, answers: {i: value}, sure: {i: bool}, cur }
  var tools = window.GraphiteTools && window.GraphiteTools.mount({ launcher: false, calc: "score-check" });
  if (tools) tools.tutorAllowed(false, "The tutor is for accounts. Make a free one after the score check to ask about any question.");

  function save() { try { sessionStorage.setItem(KEY, JSON.stringify(S)); } catch (e) { /* storage blocked */ } }
  function forget() { try { sessionStorage.removeItem(KEY); } catch (e) { /* storage blocked */ } }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function show(id) {
    ["sc-intro", "sc-test", "sc-results"].forEach(function (v) { $(v).hidden = v !== id; });
    window.scrollTo(0, 0);
  }
  function track(name, props) { if (window.GraphiteAnalytics) window.GraphiteAnalytics.track(name, props || {}); }
  function error(msg) { var e = $("sc-error"); e.textContent = msg; e.hidden = !msg; }

  function start() {
    if (!call) return error("The score check isn't available here.");
    $("sc-start").disabled = true; error("");
    call("/api/score-check").then(function (r) {
      S = { token: r.token, questions: r.questions, answers: {}, sure: {}, cur: 0 };
      save(); show("sc-test"); render();
      track("score_check_begin");
    }).catch(function (e) { error(e.message || "Couldn't start the score check. Try again in a moment."); })
      .then(function () { $("sc-start").disabled = false; });
  }

  function answered(i) { var a = S.answers[i]; return a !== undefined && a !== null && a !== ""; }

  function render() {
    var i = S.cur, q = S.questions[i], n = S.questions.length;
    var math = q.section !== "rw";
    $("sc-qnum").textContent = "Question " + (i + 1) + " of " + n;
    $("sc-qsec").textContent = (math ? "Math · " : "Reading and Writing · ") + q.domain;
    $("sc-bar").style.width = Math.round(i / n * 100) + "%";
    $("sc-stem").innerHTML = q.stem;
    var fs = $("sc-choices");
    fs.hidden = q.type !== "mc"; $("sc-spr").hidden = q.type === "mc";
    if (q.type === "mc") {
      fs.innerHTML = '<legend class="visually-hidden">Answer choices</legend>';
      q.choices.forEach(function (c, k) {
        var lab = document.createElement("label"); lab.className = "choice";
        lab.innerHTML = '<input type="radio" name="sc-q" value="' + k + '"' + (S.answers[i] === k ? " checked" : "") + '><span class="bubble" aria-hidden="true">' + LETTERS[k] +
          '</span><span class="visually-hidden">Choice ' + LETTERS[k] + ': </span><span class="choice-text">' + c + "</span>";
        fs.appendChild(lab);
      });
    } else {
      $("sc-spr-input").value = answered(i) ? S.answers[i] : "";
    }
    sureButtons();
    $("sc-back").disabled = i === 0;
    $("sc-calc").hidden = !math || !tools;
    if (!math && tools) tools.close();
    $("sc-next").textContent = i === n - 1 ? "See my score" : "Next";
  }
  function sureButtons() {
    var v = S.sure[S.cur];
    Array.prototype.forEach.call(document.querySelectorAll(".sc-sure button"), function (b) {
      b.setAttribute("aria-checked", String(v !== undefined && String(+v) === b.getAttribute("data-sure")));
    });
  }

  $("sc-choices").addEventListener("change", function (e) {
    S.answers[S.cur] = Number(e.target.value); save();
  });
  $("sc-spr-input").addEventListener("input", function (e) {
    S.answers[S.cur] = e.target.value.replace(/\s+/g, "").slice(0, 6); save();
  });
  Array.prototype.forEach.call(document.querySelectorAll(".sc-sure button"), function (b) {
    b.addEventListener("click", function () { S.sure[S.cur] = b.getAttribute("data-sure") === "1"; save(); sureButtons(); });
  });
  $("sc-back").addEventListener("click", function () { if (S.cur > 0) { S.cur--; save(); render(); } });
  $("sc-calc").addEventListener("click", function () { if (tools) tools.toggle("calc"); });
  $("sc-next").addEventListener("click", function () {
    if (S.cur < S.questions.length - 1) { S.cur++; save(); render(); window.scrollTo(0, 0); return; }
    var skipped = S.questions.filter(function (q, i) { return !answered(i); }).length;
    if (skipped && !window.confirm(skipped + (skipped === 1 ? " question has" : " questions have") + " no answer. Score it anyway? On the SAT there's no penalty for guessing.")) return;
    grade();
  });

  function grade() {
    var btn = $("sc-next"); btn.disabled = true; btn.textContent = "Scoring…";
    var sure = {};
    Object.keys(S.sure).forEach(function (k) { sure[k] = S.sure[k] ? 1 : 0; });
    call("/api/score-check/grade", { token: S.token, answers: S.answers, sure: sure }).then(function (r) {
      forget();
      if (tools) tools.close();
      results(r.result);
      track("score_check_done", { total: r.result.total.score });
    }).catch(function (e) {
      btn.disabled = false; btn.textContent = "See my score";
      var msg = e.message || "Couldn't score it. Try again in a moment.";
      if (e.data && (e.data.code === "expired" || e.data.code === "already_graded")) { forget(); S = null; show("sc-intro"); error(msg); }
      else window.alert(msg);
    });
  }

  function results(r) {
    show("sc-results");
    $("sc-total").textContent = String(r.total.score);
    $("sc-range").textContent = "Likely between " + r.total.low + " and " + r.total.high;
    $("sc-right").textContent = r.correct + " of " + r.count + " right";
    $("sc-sections").innerHTML = r.sections.map(function (s) {
      return '<div class="sc-sec"><p class="label">' + esc(s.name) + '</p><p class="sc-sec-score"><strong>' + s.score + '</strong><span>out of 800</span></p>' +
        '<p class="fine">Likely ' + s.low + "–" + s.high + " · " + s.right + " of " + s.total + " right · would reach the " + esc(s.route) + " Module 2</p></div>";
    }).join("");
    var sk = $("sc-skills");
    sk.innerHTML = r.skills.length ? r.skills.map(function (s) {
      var why = [s.missed ? s.missed + " missed" : "", s.guessed ? s.guessed + " guessed" : ""].filter(Boolean).join(", ");
      return '<li><span class="sc-pts">+' + s.points + '</span><span class="sc-skill"><strong>' + esc(s.skill) + '</strong><span class="fine">' +
        esc(s.section) + " · " + esc(s.domain) + " · " + why + "</span></span></li>";
    }).join("") : "<li><span class=\"sc-skill\"><strong>Nothing missed, and you were sure every time.</strong><span class=\"fine\">A full mock test is the next real check.</span></span></li>";
    // What fixing those skills is worth, all together, as a score to aim for.
    var pot = $("sc-potential"), gain = (r.potential || 0) - r.total.score;
    pot.hidden = !(r.skills.length && gain > 0);
    if (!pot.hidden) pot.innerHTML = "Get these " + (r.skills.length === 1 ? "questions" : r.skills.length + " skills") + " right and your estimate rises to about <strong>" +
      r.potential + "</strong>, a gain of <strong>+" + gain + "</strong>.";
    // A low or mostly skipped check: say what it means and what to do, so the number isn't the last word.
    var enc = $("sc-encourage"), notes = [];
    if (r.skipped >= 3) notes.push("You left " + r.skipped + " questions blank, and blanks count as wrong. On the real SAT there's no penalty for guessing, so always answer.");
    if (r.total.score < 1000) notes.push("This is a starting point, not a verdict. A low first score means more questions you can learn to get right, and the list below shows where to begin.");
    enc.hidden = !notes.length;
    enc.textContent = notes.join(" ");
    var list = $("sc-list"); list.innerHTML = "";
    r.questions.forEach(function (q) {
      var yours = !q.answered ? "No answer" : esc(q.your_answer);
      var d = document.createElement("details"); d.className = "res-item " + (q.correct ? "ok" : "no");
      d.innerHTML = '<summary><span class="res-n">' + (q.index + 1) + '</span><span class="res-verdict">' + (q.correct ? (q.sure ? "Correct" : "Correct, guessed") : (q.answered ? "Incorrect" : "Skipped")) +
        '</span><span class="res-dom">' + esc(q.skill) + '</span><span class="res-ans">Yours: <strong>' + yours + "</strong> · Answer: <strong>" + esc(q.answer) + "</strong></span></summary>" +
        '<div class="res-body"><div class="res-stem">' + q.stem + "</div>" +
        (q.type === "mc" ? '<ol class="res-choices" type="A">' + q.choices.map(function (c, k) { return '<li class="' + (k === q.answer_index ? "is-key" : "") + '">' + c + "</li>"; }).join("") + "</ol>" : "") +
        '<div class="res-explain">' + (q.explain_html || "") + "</div></div>";
      list.appendChild(d);
    });
    // Kept on this device, so the sign-up form can remind the student what the check found (site.js).
    try { localStorage.setItem("graphite_score_check_last", JSON.stringify({ total: r.total, sections: r.sections.map(function (s) { return { name: s.name, score: s.score }; }),
      skills: r.skills.map(function (s) { return s.skill; }), at: new Date().toISOString() })); } catch (e) { /* storage blocked */ }
  }

  $("sc-start").addEventListener("click", start);
  $("sc-again").addEventListener("click", function () { S = null; forget(); show("sc-intro"); start(); });

  // Pick up where a reload left off.
  try { S = JSON.parse(sessionStorage.getItem(KEY)); } catch (e) { S = null; }
  if (S && S.questions && S.questions.length) { show("sc-test"); render(); } else S = null;
})();
