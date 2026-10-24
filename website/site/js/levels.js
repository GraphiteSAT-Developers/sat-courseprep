/* Graphite SAT Practice Sets: practice sets that get harder one level at a time, for Math and for Reading and Writing.
   The Math | Reading and Writing switch (site.js) picks which tracks show.
   Live: talks to /api/levels. Preview: the same requests go to GraphitePracticeLocal (practice-local.js). */
(function () {
  "use strict";
  var grid = document.getElementById("lv-grid");
  if (!grid) return;
  function $(id) { return document.getElementById(id); }
  var API = window.GraphiteAPI;
  var LIVE = !!(API && API.live);
  var call = LIVE ? API.call : (window.GraphitePracticeLocal && window.GraphitePracticeLocal.call);
  var TRACK_KEY = "graphite_levels_track";
  var data = null, current = "mixed", busy = false;
  // Every plan opens the first data.free_levels levels of each track; planLock is the lock on the rest, if any.
  var planLock = null;
  function planLocked(n) { return !!planLock && n > (data.free_levels || 0); }
  function firstLevels(n) { return n === 1 ? "Level 1" : n === 2 ? "Levels 1 and 2" : "Levels 1 to " + n; }
  try { current = localStorage.getItem(TRACK_KEY) || "mixed"; } catch (e) { /* storage blocked */ }
  var m = /[#&]track=([\w-]+)/.exec(location.hash); if (m) current = m[1];

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function showError(msg) { var e = $("lv-error"); e.textContent = msg; e.hidden = !msg; }
  function signIn() { location.href = "/signin.html?next=/levels.html"; }
  if (!LIVE) $("lv-preview-note").hidden = false;
  if (LIVE) API.call("/api/me").then(function (r) { $("account-email").textContent = r.user.email; }, function () {});
  else { try { $("account-email").textContent = sessionStorage.getItem("graphite_user") || ""; } catch (e) { /* storage blocked */ } }
  if (!call) { $("lv-loading").textContent = "Levels aren't available in this preview."; return; }

  // Ten segments, one per question: easy, medium, hard.
  function meter(mix) {
    var out = "";
    ["easy", "medium", "hard"].forEach(function (d) { for (var i = 0; i < (mix[d] || 0); i++) out += '<i class="lv-' + d[0] + '"></i>'; });
    return out;
  }
  function mixText(mix) {
    return ["easy", "medium", "hard"].filter(function (d) { return mix[d]; }).map(function (d) { return mix[d] + " " + d; }).join(" · ");
  }
  function subject() { return document.documentElement.getAttribute("data-subject") === "rw" ? "rw" : "math"; }
  function shown() { return data.tracks.filter(function (t) { return (t.section || "math") === subject(); }); }
  function track() { var list = shown(); return list.filter(function (t) { return t.key === current; })[0] || list[0]; }

  function start(level, btn) {
    if (busy) return;
    busy = true; showError("");
    var label = btn.textContent; btn.disabled = true; btn.textContent = "Building your set…";
    call("/api/levels/start", { track: track().key, level: level }).then(function (r) {
      location.href = "practice-test.html?session=" + r.session.id;
    }).catch(function (err) {
      if (err && err.status === 401) { signIn(); return; }
      busy = false; btn.disabled = false; btn.textContent = label;
      if (window.GraphiteLock && GraphiteLock.handle(err)) return;
      showError(err && err.status ? err.message : "We couldn't start that level. Check your connection and try again.");
    });
  }

  function renderTabs() {
    var box = $("lv-tracks"); box.innerHTML = "";
    var list = shown();
    current = track().key;
    list.forEach(function (t, i) {
      var b = document.createElement("button");
      b.type = "button"; b.className = "lv-track"; b.setAttribute("role", "tab");
      b.setAttribute("aria-selected", String(t.key === current)); b.tabIndex = t.key === current ? 0 : -1;
      b.innerHTML = '<span class="lv-track-name"></span><span class="lv-track-meta"></span>';
      b.querySelector(".lv-track-name").textContent = t.name;
      b.querySelector(".lv-track-meta").textContent = t.all_passed ? "All cleared" : "Level " + t.unlocked;
      b.addEventListener("click", function () { pick(t.key); });
      b.addEventListener("keydown", function (e) {
        var d = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0; if (!d) return;
        e.preventDefault(); pick(list[(i + d + list.length) % list.length].key, true);
      });
      box.appendChild(b);
    });
  }
  function pick(key, focus) {
    current = key;
    try { localStorage.setItem(TRACK_KEY, key); } catch (e) { /* storage blocked */ }
    render();
    if (focus) { var b = document.querySelector('.lv-track[aria-selected="true"]'); if (b) b.focus(); }
  }

  function render() {
    renderTabs();
    var t = track(), lv = t.levels, next = lv[t.unlocked - 1];
    // Up next: the highest unlocked level, or a replay of the top one once every level is cleared.
    $("lv-next").hidden = false;
    $("lv-next-n").textContent = String(next.n);
    $("lv-next-kicker").textContent = planLocked(next.n) ? (planLock.reason || "Level " + next.n + (next.n < data.levels ? " and up come" : " comes") + " with " + planLock.need_name)
      : t.all_passed ? "Every level cleared" : next.resume_id ? "Pick up where you left off" : "Up next · " + t.name;
    $("lv-next-title").textContent = "Level " + next.n + " · " + next.tier;
    $("lv-next-meter").innerHTML = meter(next.mix);
    $("lv-next-meter").setAttribute("aria-label", "Difficulty: " + mixText(next.mix));
    $("lv-next-meta").textContent = data.size + " questions · " + mixText(next.mix) + " · pass with " + data.pass + " right" +
      (next.best != null ? " · your best so far: " + next.best + " of " + data.size : "");
    var btn = $("lv-next-btn");
    if (planLocked(next.n)) {
      btn.textContent = planLock.reason ? "Fix payment to open level " + next.n : "Unlock level " + next.n;
      btn.onclick = function () { location.href = GraphiteLock.url(planLock); };
    } else {
      btn.textContent = next.resume_id ? "Resume level " + next.n : t.all_passed ? "Replay level " + next.n : "Start level " + next.n;
      btn.onclick = function () { start(next.n, btn); };
    }

    grid.innerHTML = "";
    lv.forEach(function (l) {
      var li = document.createElement("li");
      li.className = "lv-rung is-" + l.status + (l.n === next.n ? " is-current" : "");
      var state = l.status === "passed" ? '<span class="lv-state ok">✓ Passed · best ' + l.best + "/" + data.size + "</span>"
        : l.status === "locked" || planLocked(l.n) ? '<span class="lv-state">Locked</span>'
        : '<span class="lv-state now">' + (l.resume_id ? "In progress" : l.best != null ? "Best " + l.best + "/" + data.size : "Ready") + "</span>";
      li.innerHTML = '<span class="lv-num">' + l.n + '</span><span class="lv-tier">' + esc(l.tier) + "</span>" +
        '<span class="lv-meter" role="img" aria-label="Difficulty: ' + esc(mixText(l.mix)) + '">' + meter(l.mix) + "</span>" + state;
      if (l.status !== "locked" && planLocked(l.n)) {
        // Open by progress but not on this plan: the button goes where the plan can be changed or paid.
        var a = document.createElement("a");
        a.className = "btn btn-quiet lv-go"; a.href = GraphiteLock.url(planLock);
        a.textContent = planLock.reason ? "Fix payment" : "With " + planLock.need_name;
        a.setAttribute("aria-label", a.textContent + " to open level " + l.n);
        li.appendChild(a);
      } else if (l.status !== "locked") {
        var b = document.createElement("button");
        b.type = "button"; b.className = "btn btn-quiet lv-go";
        b.textContent = l.resume_id ? "Resume" : l.status === "passed" ? "Replay" : "Start";
        b.setAttribute("aria-label", b.textContent + " level " + l.n);
        b.addEventListener("click", function () { start(l.n, b); });
        li.appendChild(b);
      } else {
        li.insertAdjacentHTML("beforeend", '<span class="lv-lock" aria-hidden="true"><svg viewBox="0 0 16 16"><rect x="3" y="7" width="10" height="7" rx="1.5" fill="currentColor"/><path d="M5.5 7V5a2.5 2.5 0 0 1 5 0v2" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></span>');
      }
      grid.appendChild(li);
    });
    $("lv-all").hidden = false;
  }

  if (window.GraphiteRewards && GraphiteRewards.call()) {
    GraphiteRewards.call()("/api/game/summary").then(function (g) { GraphiteRewards.hud($("lv-hud"), g); }).catch(function () { /* levels work without it */ });
  }
  document.addEventListener("graphite:subject", function () { if (data) render(); });
  call("/api/levels").then(function (d) {
    data = d;
    $("lv-pass").textContent = String(d.pass); $("lv-size").textContent = String(d.size);
    if (!d.tracks.some(function (t) { return t.key === current; })) current = d.tracks[0].key;
    $("lv-loading").hidden = true;
    planLock = d.access && !d.access.ok && window.GraphiteLock ? d.access : null;
    render();
    if (planLock && !document.querySelector(".lv-plan-lock")) {
      var card = GraphiteLock.card(planLock, true); card.classList.add("lv-plan-lock");
      if (!planLock.reason && d.free_levels) {
        card.querySelector("p").textContent = firstLevels(d.free_levels) + " of every topic are open on your plan. " + planLock.need_name + " opens all " + d.levels + ".";
      }
      $("lv-loading").insertAdjacentElement("afterend", card);
    }
  }).catch(function (err) {
    if (err && err.status === 401) { signIn(); return; }
    $("lv-loading").textContent = "We couldn't load your levels. Check your connection and refresh the page.";
  });
})();
