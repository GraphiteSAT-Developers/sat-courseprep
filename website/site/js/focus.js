/* Graphite focus timer. The server keeps the real clock (/api/focus); this page shows the countdown, handles
   pausing, plays the chime and runs the break. Preview: the same requests go to play-local.js. */
(function () {
  "use strict";
  if (!document.querySelector(".focus-page")) return;
  var R = window.GraphiteRewards, call = R && R.call();
  var API = window.GraphiteAPI, LIVE = !!(API && API.live);
  var PKEY = "graphite_focus_pause", SKEY = "graphite_focus_sound";
  var ov = null, pick = { minutes: 25, label: "practice" }, run = null, tick = null, mode = "focus", breakEnd = 0, ending = false;
  var title = document.title;
  function $(id) { return document.getElementById(id); }
  function signIn() { location.href = "/signin.html?next=/focus.html"; }
  function showError(m) { $("fo-error").textContent = m || ""; $("fo-error").hidden = !m; }
  if (!LIVE) $("fo-preview-note").hidden = false;
  if (!call) { $("fo-loading").textContent = "The focus timer isn't available in this preview."; return; }
  var soundPref = window.GraphiteTheme ? GraphiteTheme.prefs().study.sounds : true;  // Settings > Practice defaults
  try { var saved = localStorage.getItem(SKEY); $("fo-sound").checked = saved ? saved !== "off" : soundPref; } catch (e) { $("fo-sound").checked = soundPref; }
  $("fo-sound").addEventListener("change", function () { try { localStorage.setItem(SKEY, this.checked ? "on" : "off"); } catch (e) { /* storage blocked */ } });

  function mmss(s) { s = Math.max(0, Math.ceil(s)); return Math.floor(s / 60) + ":" + String(s % 60).padStart(2, "0"); }
  function hours(sec) { var h = sec / 3600; return h < 10 ? (Math.round(h * 10) / 10).toString() : String(Math.round(h)); }
  function pauseState() { try { return JSON.parse(localStorage.getItem(PKEY)) || {}; } catch (e) { return {}; } }
  function savePause(p) { try { localStorage.setItem(PKEY, JSON.stringify(p)); } catch (e) { /* storage blocked */ } }

  /* ---------- overview ---------- */
  function renderOverview() {
    var o = ov, goal = o.goal_hours * 3600, pct = goal ? Math.min(100, Math.round(o.week_seconds / goal * 100)) : 0;
    $("fo-goal-text").textContent = hours(o.week_seconds) + " of " + o.goal_hours + " hours this week";
    $("fo-goal-left").textContent = o.week_seconds >= goal ? "Goal reached" : hours(goal - o.week_seconds) + " to go";
    $("fo-goal-bar").setAttribute("aria-valuenow", String(pct));
    $("fo-goal-bar").firstElementChild.style.width = pct + "%";
    $("fo-today").textContent = String(Math.round(o.today_focus_seconds / 60));
    $("fo-done").textContent = String(o.sessions_done);
    $("fo-streak").textContent = String(o.streak.days);
    $("fo-week").hidden = false;
    var names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], top = Math.max.apply(null, o.week_days.concat([1500]));
    $("fo-days").innerHTML = o.week_days.map(function (s, i) {
      var m = Math.round(s / 60);
      return '<li><span class="fo-bar"><span style="height:' + Math.round(s / top * 100) + '%"></span></span><strong>' + m + "</strong><span>" + names[i] + "</span></li>";
    }).join("");
    $("fo-days").setAttribute("aria-label", "Focus minutes each day this week: " + o.week_days.map(function (s, i) { return names[i] + " " + Math.round(s / 60); }).join(", "));
    $("fo-recent").innerHTML = o.recent.length ? o.recent.map(function (r) {
      return "<li><span>" + R.esc(r.label_name) + '</span><span class="fine">' + r.minutes + "-minute session</span><strong>" +
        (r.completed ? "Finished" : Math.round((r.seconds || 0) / 60) + " min, ended early") + "</strong></li>";
    }).join("") : '<li class="pd-empty">No sessions yet this week.</li>';
    $("fo-hist").hidden = false;
  }
  function renderSetup() {
    $("fo-lengths").innerHTML = ov.lengths.map(function (l) {
      return '<label class="fo-length" for="fo-len-' + l.minutes + '"><input type="radio" name="fo-len" id="fo-len-' + l.minutes + '" value="' + l.minutes + '"' + (l.minutes === pick.minutes ? " checked" : "") + ">" +
        "<strong>" + l.minutes + " min</strong><span>then a " + l.break + "-minute break</span></label>";
    }).join("");
    $("fo-labels").innerHTML = ov.labels.map(function (l) {
      return '<label class="fo-label" for="fo-lab-' + l.key + '"><input type="radio" name="fo-lab" id="fo-lab-' + l.key + '" value="' + l.key + '"' + (l.key === pick.label ? " checked" : "") + "><span>" + R.esc(l.name) + "</span></label>";
    }).join("");
    Array.prototype.forEach.call(document.querySelectorAll('input[name="fo-len"]'), function (r) { r.addEventListener("change", function () { pick.minutes = Number(r.value); }); });
    Array.prototype.forEach.call(document.querySelectorAll('input[name="fo-lab"]'), function (r) { r.addEventListener("change", function () { pick.label = r.value; labelNote(); }); });
    labelNote();
  }
  function labelNote() {
    $("fo-label-note").textContent = ov.counted_elsewhere.indexOf(pick.label) > -1
      ? "Time on practice sets and the review queue already counts toward your goal from the sets themselves, so this session earns XP but doesn't add the same time twice."
      : "This time counts toward your weekly study goal.";
  }
  function show(view) { $("fo-setup").hidden = view !== "setup"; $("fo-run").hidden = view !== "run"; }

  /* ---------- running ---------- */
  function remaining() {
    if (mode === "break") return (breakEnd - Date.now()) / 1000;
    var p = pauseState(), paused = p.id === run.id ? (p.total || 0) + (p.at ? Date.now() - p.at : 0) : 0;
    return run.minutes * 60 - (Date.now() - run.startedAt - paused) / 1000;
  }
  function draw() {
    var left = remaining(), total = mode === "break" ? run.break_minutes * 60 : run.minutes * 60;
    $("fo-time").textContent = mmss(left);
    $("fo-ring").style.strokeDashoffset = String(Math.round(1000 * (1 - Math.max(0, left) / total)));
    document.title = mmss(left) + (mode === "break" ? " · Break" : " · Focus") + " | Graphite";
    if (Math.ceil(left) % 60 === 0) $("fo-time-sr").textContent = Math.ceil(left / 60) + " minutes left";
    if (left <= 0) { if (mode === "break") endBreak(); else if (!pauseState().at) finish(true); }
  }
  function startTicking() { clearInterval(tick); tick = setInterval(draw, 250); draw(); }
  function showRun() {
    var p = pauseState(), paused = mode === "focus" && p.id === run.id && !!p.at;
    $("fo-run-kind").textContent = mode === "break" ? "Break" : paused ? "Paused" : "Focusing";
    $("fo-run-label").textContent = mode === "break" ? "Stand up, stretch, get water" : run.label_name;
    $("fo-run-note").textContent = mode === "break" ? "Your next session starts when you're ready." : "The timer keeps going if you switch tabs or close this page. Come back anytime.";
    $("fo-pause").textContent = mode === "break" ? "Skip break" : paused ? "Resume" : "Pause";
    $("fo-end").hidden = mode === "break";
    $("fo-run").classList.toggle("is-break", mode === "break");
    $("fo-run").classList.toggle("is-paused", paused);
    show("run");
  }
  function adopt(s) {
    run = { id: s.id, minutes: s.minutes, label_name: s.label_name, break_minutes: s.break_minutes, startedAt: Date.now() - s.elapsed_ms };
    mode = "focus"; ending = false;
    showRun(); startTicking();
  }
  $("fo-start").addEventListener("click", function () {
    showError("");
    var b = this; b.disabled = true;
    call("/api/focus/start", { minutes: pick.minutes, label: pick.label }).then(function (r) {
      b.disabled = false; savePause({}); adopt(r.session); $("fo-run").scrollIntoView({ block: "center" });
    }).catch(function (err) {
      b.disabled = false;
      if (err && err.status === 401) { signIn(); return; }
      showError(err && err.status ? err.message : "We couldn't start the timer. Check your connection and try again.");
    });
  });
  $("fo-pause").addEventListener("click", function () {
    if (mode === "break") { endBreak(); return; }
    var p = pauseState();
    if (p.id !== run.id) p = { id: run.id, total: 0 };
    if (p.at) { p.total = (p.total || 0) + Date.now() - p.at; p.at = null; } else p.at = Date.now();
    savePause(p); showRun(); draw();
  });
  $("fo-end").addEventListener("click", function () { finish(false); });

  function chime() {
    if (!$("fo-sound").checked) return;
    try {
      var A = window.AudioContext || window.webkitAudioContext, ctx = new A();
      [[660, 0], [880, 0.22], [990, 0.44]].forEach(function (n) {
        var o = ctx.createOscillator(), g = ctx.createGain();
        o.type = "sine"; o.frequency.value = n[0]; o.connect(g); g.connect(ctx.destination);
        g.gain.setValueAtTime(0.0001, ctx.currentTime + n[1]);
        g.gain.exponentialRampToValueAtTime(0.2, ctx.currentTime + n[1] + 0.02);
        g.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + n[1] + 0.5);
        o.start(ctx.currentTime + n[1]); o.stop(ctx.currentTime + n[1] + 0.55);
      });
    } catch (e) { /* no audio */ }
  }
  function finish(completed) {
    if (ending) return;
    ending = true; clearInterval(tick);
    call("/api/focus/" + run.id + "/finish", { completed: completed }).then(function (r) {
      savePause({});
      ov = r.overview; renderOverview();
      if (r.reward) R.show(r.reward);
      if (r.session.completed) {
        chime();
        mode = "break"; breakEnd = Date.now() + run.break_minutes * 60000;
        showRun(); startTicking();
      } else {
        document.title = title; show("setup");
        if (!r.reward) showError(r.session.seconds < 60 ? "Sessions under a minute aren't saved." : "");
      }
    }).catch(function (err) {
      ending = false; startTicking();
      if (err && err.status === 401) { signIn(); return; }
      showError(err && err.status ? err.message : "We couldn't save that session. Check your connection; we'll try again.");
    });
  }
  function endBreak() { clearInterval(tick); mode = "focus"; document.title = title; show("setup"); $("fo-start").textContent = "Start another session"; $("fo-start").focus(); }

  call("/api/focus").then(function (o) {
    ov = o; $("fo-loading").hidden = true;
    renderOverview(); renderSetup();
    if (o.open) adopt(o.open); else show("setup");
  }).catch(function (err) {
    if (err && err.status === 401) { signIn(); return; }
    $("fo-loading").textContent = err && err.status === 403 ? "The focus timer is for student accounts." : "We couldn't load the focus timer. Check your connection and refresh the page.";
  });
})();
