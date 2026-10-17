/* Graphite speed round: ten quick questions on the server's clock, then the leaderboards.
   Live: /api/speed. Preview: the same requests go to play-local.js. */
(function () {
  "use strict";
  if (!document.querySelector(".speed-page")) return;
  var R = window.GraphiteRewards, call = R && R.call();
  var API = window.GraphiteAPI, LIVE = !!(API && API.live);
  var LETTERS = "ABCD";
  var info = null, run = null, cur = 0, startedAt = 0, offset = 0, tick = null, locked = false;
  function $(id) { return document.getElementById(id); }
  function esc(s) { return R.esc(s); }
  function signIn() { location.href = "/signin.html?next=/speed.html"; }
  function showError(m) { $("sp-error").textContent = m || ""; $("sp-error").hidden = !m; }
  function failed(err, fallback) {
    if (err && err.status === 401) { signIn(); return; }
    showError(err && err.status ? err.message : fallback);
  }
  if (!LIVE) { $("sp-preview-note").hidden = false; $("sp-board-sample").hidden = false; }
  if (!call) { $("sp-loading").textContent = "Speed rounds aren't available in this preview."; return; }

  function clock(ms, tenths) {
    ms = Math.max(0, ms || 0);
    var s = Math.floor(ms / 1000), m = Math.floor(s / 60), out = m + ":" + String(s % 60).padStart(2, "0");
    return tenths === false ? out : out + "." + Math.floor((ms % 1000) / 100);
  }
  function longDay(iso) { var p = iso.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]).toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric" }); }
  function show(view) {
    ["sp-intro", "sp-play", "sp-done"].forEach(function (id) { $(id).hidden = id !== view; });
  }

  /* ---------- before ---------- */
  function renderIntro() {
    var o = info;
    $("sp-day").textContent = longDay(o.day);
    $("sp-size").textContent = String(o.size);
    $("sp-penalty").textContent = String(Math.round(o.penalty_ms / 1000));
    var t = o.ranked_today;
    $("sp-today").textContent = !t ? "Not played yet" : t.open ? "In progress" : clock(t.score_ms) + " (" + t.correct + " of " + t.total + " right)";
    $("sp-best").textContent = o.personal_best_ms != null ? clock(o.personal_best_ms) : "–";
    $("sp-start").textContent = !t ? "Start today's round" : t.open ? "Finish today's round" : "Play again for practice";
    var b = o.board_profile;
    $("sp-visibility").innerHTML = b.opt_in && b.nickname
      ? "You show up as <strong>" + esc(b.nickname) + "</strong>" + (b.state_name ? " in " + esc(b.state_name) : "") + '. <a href="settings.html#leaderboard">Change</a>'
      : 'You\'re hidden on leaderboards. <a href="settings.html#leaderboard">Pick a nickname</a> to show up.';
    $("sp-scope-state-label").textContent = b.state ? b.state_name : "My state";
    show("sp-intro");
  }
  function load() {
    return call("/api/speed").then(function (o) { info = o; $("sp-loading").hidden = true; renderIntro(); loadBoard(); });
  }

  /* ---------- during ---------- */
  function begin() {
    showError("");
    var btn = $("sp-start"); btn.disabled = true;
    call("/api/speed/start", {}).then(function (r) {
      btn.disabled = false;
      run = r.run;
      cur = 0;
      while (cur < run.total && run.answered[String(cur)]) cur++;
      offset = run.elapsed_ms; startedAt = Date.now();
      show("sp-play");
      dots();
      renderQ();
      clearInterval(tick);
      tick = setInterval(function () { $("sp-clock").textContent = clock(offset + Date.now() - startedAt); }, 100);
      $("sp-play").scrollIntoView({ block: "start" });
    }).catch(function (err) { btn.disabled = false; failed(err, "We couldn't start the round. Check your connection and try again."); });
  }
  function dots() {
    var out = "";
    for (var i = 0; i < run.total; i++) {
      var a = run.answered[String(i)];
      out += '<i class="' + (a ? (a.correct ? "is-right" : "is-wrong") : i === cur ? "is-now" : "") + '"></i>';
    }
    $("sp-dots").innerHTML = out;
  }
  function renderQ() {
    var q = run.questions[cur];
    locked = false;
    $("sp-count").textContent = "Question " + (cur + 1) + " of " + run.total;
    $("sp-stem").innerHTML = q.stem;
    var box = $("sp-choices"); box.innerHTML = "";
    q.choices.forEach(function (c, k) {
      var b = document.createElement("button");
      b.type = "button"; b.className = "sp-choice"; b.setAttribute("data-k", String(k));
      b.innerHTML = '<span class="mc-letter">' + LETTERS[k] + '</span><span class="mc-text">' + c + "</span>";
      b.addEventListener("click", function () { answer(k); });
      box.appendChild(b);
    });
    var first = box.querySelector("button"); if (first) first.focus({ preventScroll: true });
  }
  function answer(k) {
    if (locked) return;
    locked = true;
    var btns = $("sp-choices").querySelectorAll("button");
    Array.prototype.forEach.call(btns, function (b) { b.disabled = true; });
    btns[k].classList.add("is-picked");
    call("/api/speed/runs/" + run.id + "/answer", { index: cur, answer: k }).then(function (r) {
      run.answered[String(cur)] = r.answer;
      btns[r.answer.answer_index].classList.add("is-key");
      if (!r.answer.correct) btns[k].classList.add("is-wrong");
      dots();
      var wait = r.answer.correct ? 350 : 900;  // a miss stays up a moment longer so you can see the answer
      setTimeout(function () {
        if (r.finished) { done(r.result, r.reward); return; }
        cur++;
        while (cur < run.total && run.answered[String(cur)]) cur++;
        if (cur >= run.total) { finishNow(); return; }
        dots(); renderQ();
      }, wait);
    }).catch(function (err) {
      if (err && err.status === 409) { finishNow(); return; }
      locked = false;
      Array.prototype.forEach.call(btns, function (b) { b.disabled = false; });
      btns[k].classList.remove("is-picked");
      failed(err, "That answer didn't go through. Try again.");
    });
  }
  function finishNow() {
    call("/api/speed/runs/" + run.id + "/finish", {}).then(function (r) { done(r.result, r.reward); })
      .catch(function (err) { failed(err, "We couldn't finish the round. Refresh the page."); });
  }
  document.addEventListener("keydown", function (e) {
    if ($("sp-play").hidden || e.altKey || e.ctrlKey || e.metaKey) return;
    var k = "1234".indexOf(e.key); if (k < 0) k = "abcd".indexOf(e.key.toLowerCase());
    if (k < 0 || !run || k >= run.questions[cur].choices.length) return;
    e.preventDefault(); answer(k);
  });

  /* ---------- after ---------- */
  function done(res, reward) {
    clearInterval(tick);
    $("sp-done-kind").textContent = res.ranked ? "Ranked round · on the leaderboard" : "Practice round · not ranked";
    $("sp-done-title").textContent = clock(res.score_ms);
    $("sp-done-right").textContent = res.correct + " of " + res.total;
    $("sp-done-raw").textContent = clock(res.raw_ms);
    $("sp-done-pen").textContent = "+" + clock(res.misses * info.penalty_ms, false) + (res.misses ? " (" + res.misses + (res.misses === 1 ? " miss)" : " misses)") : "");
    $("sp-done-place").textContent = "…";
    show("sp-done");
    $("sp-done").focus();
    if (reward) R.show(reward);
    call("/api/speed").then(function (o) { info = o; });
    loadBoard().then(function (b) {
      var you = b && b.you;
      $("sp-done-place").textContent = !res.ranked ? "Practice" : you ? "#" + you.rank + (b.scope === "state" && b.state_name ? " in " + b.state_name : " nationwide") + (you.visible ? "" : " (hidden)") : "–";
    });
  }
  $("sp-start").addEventListener("click", begin);
  $("sp-again").addEventListener("click", begin);

  /* ---------- leaderboards ---------- */
  function scope() { return $("sp-scope-nation").checked ? "nation" : "state"; }
  function period() { return $("sp-period-week").checked ? "week" : "today"; }
  function loadBoard() {
    var sc = scope();
    if (sc === "state" && info && !info.board_profile.state) { $("sp-scope-nation").checked = true; sc = "nation"; }
    return call("/api/speed/board?scope=" + sc + "&period=" + period()).then(function (b) { drawBoard(b); return b; })
      .catch(function (err) { failed(err, "We couldn't load the leaderboard."); });
  }
  function drawBoard(b) {
    $("sp-board-panel").hidden = false;
    var where = b.scope === "state" ? (b.state_name || "your state") : "the country";
    $("sp-board-note").textContent = (b.period === "today" ? "Today's" : "This week's") + " fastest in " + where + ". Time includes " + Math.round((info ? info.penalty_ms : 15000) / 1000) + " seconds for each miss. Each student's best ranked round counts.";
    $("sp-board").innerHTML = b.rows.length ? b.rows.map(function (r) {
      return '<tr class="' + (r.you ? "is-you" : "") + '"><td class="sp-rank">' + r.rank + "</td>" +
        '<td><span class="sp-player"><span class="avatar avatar-xs' + (r.avatar ? " is-drawn" : "") + '"' + (r.frame ? ' data-frame="' + esc(r.frame) + '"' : "") + ' aria-hidden="true">' +
        (r.avatar && window.GraphiteTheme ? GraphiteTheme.drawAvatar(r.avatar, "") : esc(r.nickname.charAt(0))) + "</span><span><strong>" + esc(r.nickname) + (r.you ? " (you)" : "") + "</strong>" +
        (r.title ? '<em>' + esc(r.title) + "</em>" : "") + "</span></span></td>" +
        '<td class="sp-col-state">' + esc(r.state || "") + "</td><td>" + r.correct + "/" + r.total + '</td><td class="sp-time">' + clock(r.score_ms) + "</td></tr>";
    }).join("") : '<tr><td colspan="5" class="pd-empty">No ranked rounds ' + (b.period === "today" ? "today" : "this week") + " yet. Be the first.</td></tr>";
    var you = b.you, el = $("sp-you");
    el.hidden = !you || you.visible;
    if (you && !you.visible) el.innerHTML = "Your best: <strong>" + clock(you.score_ms) + "</strong>, which would place <strong>#" + you.rank + "</strong> of " + you.of +
      '. You\'re hidden. <a href="settings.html#leaderboard">Show me on the leaderboard</a>';
  }
  ["sp-scope-state", "sp-scope-nation", "sp-period-today", "sp-period-week"].forEach(function (id) {
    $(id).addEventListener("change", function () {
      if (id === "sp-scope-state" && info && !info.board_profile.state) {
        $("sp-scope-nation").checked = true;
        $("sp-board-note").innerHTML = 'Add your state in <a href="settings.html#leaderboard">Settings</a> to see your state\'s board.';
        return;
      }
      loadBoard();
    });
  });

  load().catch(function (err) {
    if (err && err.status === 401) { signIn(); return; }
    $("sp-loading").textContent = err && err.status === 403 ? "Speed rounds are for student accounts." : "We couldn't load today's round. Check your connection and refresh the page.";
  });
})();
