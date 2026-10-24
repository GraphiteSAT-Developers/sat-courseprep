/* The dashboard's layout from Settings > Dashboard layout: which sections show, in what order, and the
   shortcuts pinned to the top. With the original layout nothing here changes the page. */
(function () {
  "use strict";
  var T = window.GraphiteTheme, hello = document.querySelector(".dash .hello");
  if (!T || !hello) return;
  var FULL = { kpis: true, play: true, account: true };  // these span the page; the rest flow in two columns
  var PINS = {
    levels: ["Practice Sets", "levels.html"], speed: ["Speed round", "speed.html"], focus: ["Focus timer", "focus.html"], lessons: ["Lessons", "lessons.html"],
    practice_test: ["Practice test", "practice.html", "test"], practice: ["Topic practice", "practice.html"], review: ["Review queue", "dashboard.html#review"],
    plan: ["Study plan", "plan.html"], rewards: ["Rewards and shop", "rewards.html"], calculator: ["Graphing calculator", "calculator.html"]
  };
  var DEFAULT = T.defaults.dashboard.order.join(",");
  function el(k) { return document.querySelector('[data-dash="' + k + '"]'); }

  function pins(list) {
    var nav = document.getElementById("dash-pins");
    if (!list.length) { if (nav) nav.remove(); return; }
    if (!nav) { nav = document.createElement("nav"); nav.id = "dash-pins"; nav.className = "dash-pins"; nav.setAttribute("aria-label", "Pinned shortcuts"); hello.insertAdjacentElement("afterend", nav); }
    nav.innerHTML = list.filter(function (k) { return PINS[k]; }).map(function (k) {
      return '<a class="btn btn-secondary" href="' + PINS[k][1] + '"' + (PINS[k][2] ? ' data-start="' + PINS[k][2] + '"' : "") + ">" + PINS[k][0] + "</a>";
    }).join("") + '<a class="dash-pins-edit" href="settings.html#layout">Edit</a>';
  }
  // "Practice test" starts a new random practice test straight away.
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("[data-start]"); if (!a) return;
    var API = window.GraphiteAPI, call = API && API.live ? API.call : (window.GraphitePracticeLocal && window.GraphitePracticeLocal.call);
    if (!call) return;
    e.preventDefault(); a.textContent = "Building your test…";
    call("/api/practice/sessions", { mode: "test" }).then(function (r) { location.href = "practice-test.html?session=" + r.session.id; })
      .catch(function () { location.href = "practice.html"; });
  });

  function apply(p) {
    var d = (p || T.prefs()).dashboard;
    pins(d.pins || []);
    var custom = d.order.join(",") !== DEFAULT || d.hidden.length;
    document.querySelectorAll("[data-dash]").forEach(function (n) { n.classList.toggle("is-user-hidden", d.hidden.indexOf(n.getAttribute("data-dash")) > -1); });
    if (!custom) return;
    var host = document.getElementById("dash-custom");
    if (!host) {
      host = document.createElement("div"); host.id = "dash-custom"; host.className = "dash-custom";
      (document.getElementById("dash-pins") || hello).insertAdjacentElement("afterend", host);
    }
    var flow = null;
    d.order.forEach(function (k) {
      var n = el(k); if (!n) return;
      if (FULL[k]) { host.appendChild(n); flow = null; return; }
      if (!flow) { flow = document.createElement("div"); flow.className = "dash-flow"; host.appendChild(flow); }
      flow.appendChild(n);
    });
    Array.prototype.forEach.call(host.querySelectorAll(".dash-flow"), function (f) {
      if (!f.children.length) { f.remove(); return; }
      var shown = Array.prototype.filter.call(f.children, function (c) { return !c.classList.contains("is-user-hidden"); }).length;
      f.classList.toggle("is-single", shown < 2);  // one section alone takes the full width
    });
    var grid = document.getElementById("dash-folds"); if (grid) grid.hidden = true;
  }
  apply();
  document.addEventListener("graphite:prefs", function (e) { apply(e.detail); });
})();

/* The fold-out cards: each closed card's summary line is read from the section inside it, so it stays right as
   the dashboard fills in (live data, the preview's sample student, a locked feature). A card shows only while its
   section does: "Play and earn" appears once its data arrives. */
(function () {
  "use strict";
  function txt(sel, root) { var n = (root || document).querySelector(sel); return n ? n.textContent.replace(/\s+/g, " ").trim() : ""; }
  var TEASE = {
    today: function () { return txt("#today-meta"); },
    play: function (p) { var r = txt(".dash-play-xp strong", p); return (r ? r + ". " : "") + "Speed round, lessons, Practice Sets and focus timer"; },
    scores: function () { var n = txt("#kpi-latest"); return /\d/.test(n) ? "Latest " + n + " · " + txt("#scores-meta") : txt("#scores-meta"); },
    domains: function (p) { var f = p.querySelectorAll(".bar-name .chip").length; return f ? f + (f === 1 ? " area" : " areas") + " marked Focus" : txt("#domains-meta"); },
    review: function (p) { var due = p.querySelectorAll(".due-now").length; return txt("#review-count") + (due ? " · " + due + " due today" : ""); },
    plan: function (p) {
      var now = p.querySelector(".weeks .is-now span:last-child"), w = now ? now.cloneNode(true) : null;
      if (w) Array.prototype.forEach.call(w.querySelectorAll(".now-tag"), function (t) { t.remove(); });
      return txt("#plan-meta") + (w ? " · this week: " + w.textContent.trim() : "");
    },
    account: function () { return "Your plan, weekly goal and parent access"; }
  };
  Array.prototype.forEach.call(document.querySelectorAll(".dash-fold"), function (card) {
    var k = card.getAttribute("data-dash"), panel = card.querySelector(".panel"), title = card.querySelector(".fold-title"),
        tease = card.querySelector(".fold-teaser"), busy = false;
    if (!panel) return;
    function sync() {
      if (busy) return; busy = true;
      card.hidden = panel.hidden;
      var h = txt("h2", panel); if (h) title.textContent = h;
      var lock = panel.querySelector(".lock-card strong");
      tease.textContent = lock ? lock.textContent : TEASE[k] ? TEASE[k](panel) : "";
      busy = false;
    }
    sync();
    new MutationObserver(sync).observe(panel, { subtree: true, childList: true, characterData: true, attributes: true, attributeFilter: ["hidden"] });
    // The numbers in Scores and Today's set come from the summary row above the cards.
    if (k === "scores") new MutationObserver(sync).observe(document.querySelector(".kpis") || panel, { subtree: true, childList: true, characterData: true });
  });
})();
