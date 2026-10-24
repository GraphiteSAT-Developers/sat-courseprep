/* Graphite SAT mock tests (practice.html): a full adaptive section with a break between the modules, one module, or
   untimed topic practice, for Math and for Reading and Writing. Live: /api/mock-tests and /api/practice. Preview: the
   same requests go to GraphitePracticeLocal (practice-local.js). Locked by plan: see GraphiteLock in site.js.
   Every question a student finishes goes on their done list (a cookie per section, and their account), and new sets
   never repeat it until the whole pool is done. */
(function () {
  "use strict";
  var root = document.getElementById("pr-domains");
  if (!root) return;
  function $(id) { return document.getElementById(id); }
  var API = window.GraphiteAPI;
  var LIVE = !!(API && API.live);
  var call = LIVE ? API.call : (window.GraphitePracticeLocal && window.GraphitePracticeLocal.call);
  var COUNT_KEY = "graphite_practice_count";
  var count = 10;
  try { count = Number(localStorage.getItem(COUNT_KEY)) || 0; } catch (e) { /* storage blocked */ }
  if (!count) count = (window.GraphiteTheme && GraphiteTheme.prefs().study.set_size) || 10;  // Settings > Practice defaults
  var busy = false;
  var SECTIONS = { math: "Math", rw: "Reading and Writing" };
  // Each section's elements share names: pr-mock-start for Math, pr-rw-mock-start for Reading and Writing.
  function el(section, name) { return $((section === "rw" ? "pr-rw-" : "pr-") + name); }

  // A small picture for each domain, so the topic list is easy to scan.
  var DOMAIN_ICONS = {
    "algebra": '<svg viewBox="0 0 24 24"><text x="3" y="17" font-size="13" font-family="Georgia,serif" font-style="italic" fill="currentColor">x=</text></svg>',
    "advanced-math": '<svg viewBox="0 0 24 24"><path d="M4 5c2 14 14 14 16 0" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    "psda": '<svg viewBox="0 0 24 24"><path d="M5 19V11M10 19V6M15 19v-5M20 19V9" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>',
    "geometry-trig": '<svg viewBox="0 0 24 24"><path d="M4 19 L12 5 L20 19 Z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>',
    "craft-structure": '<svg viewBox="0 0 24 24"><path d="M5 6h14M5 10h10M5 14h14M5 18h8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    "information-ideas": '<svg viewBox="0 0 24 24"><circle cx="10.5" cy="10.5" r="5.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M15 15l5 5" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>',
    "conventions": '<svg viewBox="0 0 24 24"><text x="4" y="18" font-size="16" font-family="Georgia,serif" font-weight="700" fill="currentColor">;</text><text x="12" y="18" font-size="16" font-family="Georgia,serif" font-weight="700" fill="currentColor">,</text></svg>',
    "expression-ideas": '<svg viewBox="0 0 24 24"><path d="M4 12h12M12 7l5 5-5 5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
  };
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function showError(msg) { var e = $("pr-error"); e.textContent = msg; e.hidden = !msg; }
  function signIn() { location.href = "/signin.html?next=/practice.html"; }
  function locked(err) { return window.GraphiteLock && window.GraphiteLock.handle(err); }

  if (!LIVE) $("pr-preview-note").hidden = false;

  // Section tabs: Math, or Reading and Writing.
  var SECTION_KEY = "graphite_subject";  // shared with the Math | Reading and Writing switch on other pages
  var tabs = Array.prototype.slice.call(document.querySelectorAll(".pr-section"));
  function pickSection(name, focus) {
    tabs.forEach(function (t) {
      var on = t.getAttribute("data-section") === name;
      t.setAttribute("aria-selected", String(on));
      t.tabIndex = on ? 0 : -1;
      $(t.getAttribute("aria-controls")).hidden = !on;
      if (on && focus) t.focus();
    });
    try { localStorage.setItem(SECTION_KEY, name); } catch (e) { /* storage blocked */ }
  }
  tabs.forEach(function (t, i) {
    t.addEventListener("click", function () { pickSection(t.getAttribute("data-section")); });
    t.addEventListener("keydown", function (e) {
      var d = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
      if (!d) return;
      e.preventDefault();
      pickSection(tabs[(i + d + tabs.length) % tabs.length].getAttribute("data-section"), true);
    });
  });
  var savedSection = null;
  try { savedSection = localStorage.getItem(SECTION_KEY); } catch (e) { /* storage blocked */ }
  if (location.hash === "#reading-writing") savedSection = "rw";
  if (savedSection === "rw") pickSection("rw");
  // The header shows who is signed in.
  if (LIVE) API.call("/api/me").then(function (r) { $("account-email").textContent = r.user.email; }, function () {});
  else { try { var who = sessionStorage.getItem("graphite_user"); $("account-email").textContent = who || ""; } catch (e) { /* storage blocked */ } }
  if (!call) { root.innerHTML = '<p class="fine">Practice isn\'t available in this preview.</p>'; return; }

  function start(data, btn) {
    if (busy) return;
    busy = true; showError("");
    var label = btn.textContent; btn.disabled = true; btn.textContent = "Building your set…";
    call("/api/practice/sessions", data).then(function (r) {
      location.href = "practice-test.html?session=" + r.session.id;
    }).catch(function (err) {
      if (err && err.status === 401) { signIn(); return; }
      busy = false; btn.disabled = false; btn.textContent = label;
      if (locked(err)) { loadMocks(); return; }
      showError(err && err.status ? err.message : "We couldn't start that set. Check your connection and try again.");
    });
  }

  /* ---------- mock tests ---------- */
  function day(iso) { var d = new Date(iso); return d.toLocaleDateString("en-US", { month: "short", day: "numeric" }); }
  function allowance(box, lock, noun) {
    if (!lock) { box.textContent = ""; return; }
    if (!lock.ok) { box.textContent = ""; return; }
    box.textContent = lock.limit == null ? "" : lock.left + " of " + lock.limit + " " + noun + " left this " + lock.period + ".";
  }
  function renderMocks(d) {
    var lock = d.access, off = lock && !lock.ok;
    ["math", "rw"].forEach(function (sec) {
      var box = el(sec, "mock-lock");
      box.innerHTML = "";
      allowance(el(sec, "mock-left"), lock, lock && lock.limit === 1 ? "practice test" : "practice tests");
      if (off && window.GraphiteLock) box.appendChild(GraphiteLock.card(lock, true));
      el(sec, "mock-start").hidden = off; el(sec, "test-start").hidden = off;
      el(sec, "mock-break").closest(".check").hidden = off;
      el(sec, "mock-break").checked = d.break_minutes ? el(sec, "mock-break").checked : false;
      var list = el(sec, "recent-list"); list.innerHTML = "";
      var mine = d.recent.filter(function (m) { return (m.section || "math") === sec; });
      mine.forEach(function (m) {
        var li = document.createElement("li"), href;
        if (m.status === "done") href = "practice-test.html?session=" + m.m2_session;
        else href = "practice-test.html?session=" + (m.status === "module2" || m.status === "break" ? m.m2_session : m.m1_session);  // the break comes before Module 2
        var what = m.status === "done" ? "<strong>" + m.score + "</strong> estimated " + esc(SECTIONS[sec]) + " · " + m.correct + " of " + (m.total || 44) + " right" +
          (m.route ? " · Module 2 " + m.route : "") : (m.status === "break" ? "On the break" : "In progress: Module " + (m.status === "module2" ? 2 : 1));
        li.innerHTML = '<div><strong></strong><p class="fine">' + what + '</p></div><a class="btn btn-quiet" href="' + href + '">' + (m.status === "done" ? "Review" : "Resume") + "</a>";
        li.querySelector("strong").textContent = m.section_name + " · " + day(m.created_at);
        list.appendChild(li);
      });
      el(sec, "recent").hidden = !mine.length;
    });
  }
  function loadMocks() {
    return call("/api/mock-tests").then(renderMocks).catch(function (err) { if (err && err.status === 401) signIn(); });
  }
  ["math", "rw"].forEach(function (sec) {
    el(sec, "mock-start").addEventListener("click", function () {
      var btn = el(sec, "mock-start");
      if (busy) return;
      busy = true; showError("");
      var label = btn.textContent; btn.disabled = true; btn.textContent = "Building your test…";
      call("/api/mock-tests", { section: sec, with_break: el(sec, "mock-break").checked }).then(function (r) {
        location.href = "practice-test.html?session=" + r.mock.m1_session;
      }).catch(function (err) {
        if (err && err.status === 401) { signIn(); return; }
        busy = false; btn.disabled = false; btn.textContent = label;
        if (locked(err)) { loadMocks(); return; }
        showError(err && err.status ? err.message : "We couldn't start the test. Check your connection and try again.");
      });
    });
    el(sec, "test-start").addEventListener("click", function () { start({ mode: "test", section: sec }, el(sec, "test-start")); });
  });
  loadMocks();

  function renderCounts(sec, counts) {
    var box = el(sec, "count"); box.innerHTML = "";
    if (counts.indexOf(count) < 0) count = 10;
    counts.forEach(function (n) {
      var id = "pr-" + sec + "-count-" + n;
      var wrap = document.createElement("span");
      wrap.innerHTML = '<input type="radio" name="pr-count-' + sec + '" id="' + id + '" value="' + n + '"' + (n === count ? " checked" : "") + '><label for="' + id + '">' + n + "</label>";
      wrap.querySelector("input").addEventListener("change", function () {
        count = n; try { localStorage.setItem(COUNT_KEY, String(n)); } catch (e) { /* storage blocked */ }
        var other = $("pr-" + (sec === "rw" ? "math" : "rw") + "-count-" + n); if (other) other.checked = true;
      });
      box.appendChild(wrap);
    });
  }

  var unfinished = { math: [], rw: [] };
  function renderUnfinished() {
    var all = unfinished.math.concat(unfinished.rw.filter(function (s) {
      return !unfinished.math.some(function (m) { return m.id === s.id; });
    }));
    var list = $("pr-unfinished-list"); list.innerHTML = "";
    all.forEach(function (s) {
      var li = document.createElement("li");
      var kind = s.mode === "test" ? (/: Module \d$/.test(s.title) ? "Full test" : "One module") : "Topic practice";
      var detail = s.mode === "topic" && s.checked ? s.checked + " of " + s.questions + " checked" : s.questions + " questions";
      li.innerHTML = '<div><strong>' + esc(s.title) + '</strong><p class="fine">' + esc(SECTIONS[s.section || "math"]) + " · " + kind + " · " + detail + "</p></div>" +
        '<a class="btn btn-quiet" href="practice-test.html?session=' + s.id + '">Resume</a>';
      list.appendChild(li);
    });
    $("pr-unfinished").hidden = !all.length;
  }

  function render(sec, d) {
    el(sec, "test-q").textContent = String(d.test.questions);
    el(sec, "test-min").textContent = String(d.test.minutes);
    renderCounts(sec, d.topic_counts);
    allowance(el(sec, "topic-left"), d.access, d.access && d.access.limit === 1 ? "topic set" : "topic sets");
    var tl = document.querySelector("#" + (sec === "rw" ? "pr-rw-topic" : "pr-topic") + " > .lock-card"); if (tl) tl.remove();
    if (d.access && !d.access.ok && window.GraphiteLock) el(sec, "topic-left").insertAdjacentElement("afterend", GraphiteLock.card(d.access, true));
    // The done list: questions finished this round. A topic starts over once all of its questions are done.
    el(sec, "progress").textContent = d.done ? "You've finished " + d.done + " of " + d.total + " " + SECTIONS[sec] +
      " questions. Questions you've done don't come back until you've done every one in a topic; then that topic starts over." : "";

    unfinished[sec] = d.unfinished;
    renderUnfinished();

    var box = el(sec, "domains");
    box.innerHTML = "";
    d.domains.forEach(function (dm) {
      var secEl = document.createElement("section");
      secEl.className = "pr-domain";
      var head = document.createElement("div");
      head.className = "pr-domain-head";
      head.innerHTML = '<h3><span class="dom-icon" aria-hidden="true">' + (DOMAIN_ICONS[dm.key] || "") + "</span>" + esc(dm.name) +
        ' <span class="fine pr-done">' + dm.done + " of " + dm.total + " done</span></h3>";
      var all = document.createElement("button");
      all.type = "button"; all.className = "btn btn-secondary pr-all";
      all.textContent = "Practice all";
      all.setAttribute("aria-label", "Practice all of " + dm.name);
      all.setAttribute("data-track", "practice_domain_start");
      all.addEventListener("click", function () { start({ mode: "topic", domain: dm.key, count: count }, all); });
      head.appendChild(all);
      secEl.appendChild(head);

      var ul = document.createElement("ul");
      ul.className = "pr-skills";
      dm.skills.forEach(function (sk) {
        var li = document.createElement("li");
        li.innerHTML = '<span class="pr-skill-name">' + esc(sk.name) + ' <span class="fine pr-done">' + sk.done + "/" + sk.total + "</span></span>";
        var b = document.createElement("button");
        b.type = "button"; b.className = "btn btn-quiet";
        b.textContent = "Practice";
        b.setAttribute("aria-label", "Practice " + sk.name);
        b.setAttribute("data-track", "practice_topic_start");
        b.addEventListener("click", function () { start({ mode: "topic", domain: dm.key, skill: sk.key, count: count }, b); });
        li.appendChild(b);
        ul.appendChild(li);
      });
      secEl.appendChild(ul);
      box.appendChild(secEl);
    });
  }

  ["math", "rw"].forEach(function (sec) {
    call("/api/practice" + (sec === "rw" ? "?section=rw" : "")).then(function (d) { render(sec, d); }).catch(function (err) {
      if (err && err.status === 401) { signIn(); return; }
      el(sec, "domains").innerHTML = '<p class="fine">We couldn\'t load your topics. Check your connection and refresh the page.</p>';
    });
  });
})();
