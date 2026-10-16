/* Graphite practice hub: start a random practice test or practice one topic.
   Live: talks to /api/practice. Preview: the same requests go to GraphitePracticeLocal (practice-local.js). */
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
  try { count = Number(localStorage.getItem(COUNT_KEY)) || 10; } catch (e) { /* storage blocked */ }
  var busy = false;

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function showError(msg) { var e = $("pr-error"); e.textContent = msg; e.hidden = !msg; }
  function signIn() { location.href = "/signin.html?next=/practice.html"; }

  if (!LIVE) $("pr-preview-note").hidden = false;

  // Section tabs: Math, or Reading and Writing (placeholder until its questions exist).
  var SECTION_KEY = "graphite_practice_section";
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
      showError(err && err.status ? err.message : "We couldn't start that set. Check your connection and try again.");
    });
  }

  function renderCounts(counts) {
    var box = $("pr-count"); box.innerHTML = "";
    if (counts.indexOf(count) < 0) count = 10;
    counts.forEach(function (n) {
      var id = "pr-count-" + n;
      var wrap = document.createElement("span");
      wrap.innerHTML = '<input type="radio" name="pr-count" id="' + id + '" value="' + n + '"' + (n === count ? " checked" : "") + '><label for="' + id + '">' + n + "</label>";
      wrap.querySelector("input").addEventListener("change", function () {
        count = n; try { localStorage.setItem(COUNT_KEY, String(n)); } catch (e) { /* storage blocked */ }
      });
      box.appendChild(wrap);
    });
  }

  function render(d) {
    $("pr-test-q").textContent = String(d.test.questions);
    $("pr-test-min").textContent = String(d.test.minutes);
    renderCounts(d.topic_counts);

    var list = $("pr-unfinished-list"); list.innerHTML = "";
    d.unfinished.forEach(function (s) {
      var li = document.createElement("li");
      var kind = s.mode === "test" ? "Practice test" : "Topic practice";
      var detail = s.mode === "topic" && s.checked ? s.checked + " of " + s.questions + " checked" : s.questions + " questions";
      li.innerHTML = '<div><strong>' + esc(s.title) + '</strong><p class="fine">' + kind + " · " + detail + "</p></div>" +
        '<a class="btn btn-quiet" href="practice-test.html?session=' + s.id + '">Resume</a>';
      list.appendChild(li);
    });
    $("pr-unfinished").hidden = !d.unfinished.length;

    root.innerHTML = "";
    d.domains.forEach(function (dm) {
      var sec = document.createElement("section");
      sec.className = "pr-domain";
      var head = document.createElement("div");
      head.className = "pr-domain-head";
      head.innerHTML = '<h3>' + esc(dm.name) + "</h3>";
      var all = document.createElement("button");
      all.type = "button"; all.className = "btn btn-secondary pr-all";
      all.textContent = "Practice all";
      all.setAttribute("aria-label", "Practice all of " + dm.name);
      all.setAttribute("data-track", "practice_domain_start");
      all.addEventListener("click", function () { start({ mode: "topic", domain: dm.key, count: count }, all); });
      head.appendChild(all);
      sec.appendChild(head);

      var ul = document.createElement("ul");
      ul.className = "pr-skills";
      dm.skills.forEach(function (sk) {
        var li = document.createElement("li");
        li.innerHTML = '<span class="pr-skill-name">' + esc(sk.name) + "</span>";
        var b = document.createElement("button");
        b.type = "button"; b.className = "btn btn-quiet";
        b.textContent = "Practice";
        b.setAttribute("aria-label", "Practice " + sk.name);
        b.setAttribute("data-track", "practice_topic_start");
        b.addEventListener("click", function () { start({ mode: "topic", domain: dm.key, skill: sk.key, count: count }, b); });
        li.appendChild(b);
        ul.appendChild(li);
      });
      sec.appendChild(ul);
      root.appendChild(sec);
    });
  }

  $("pr-test-start").addEventListener("click", function () { start({ mode: "test" }, $("pr-test-start")); });

  call("/api/practice").then(render).catch(function (err) {
    if (err && err.status === 401) { signIn(); return; }
    root.innerHTML = '<p class="fine">We couldn\'t load your topics. Check your connection and refresh the page.</p>';
  });
})();
