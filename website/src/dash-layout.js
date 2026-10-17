/* The dashboard's layout from Settings > Dashboard layout: which sections show, in what order, and the
   shortcuts pinned to the top. With the original layout nothing here changes the page. */
(function () {
  "use strict";
  var T = window.GraphiteTheme, hello = document.querySelector(".dash .hello");
  if (!T || !hello) return;
  var FULL = { kpis: true, play: true };  // these span the page; the rest flow in two columns
  var PINS = {
    levels: ["Level up", "levels.html"], speed: ["Speed round", "speed.html"], focus: ["Focus timer", "focus.html"], lessons: ["Lessons", "lessons.html"],
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
    var grid = document.querySelector(".dash-grid"); if (grid) grid.hidden = true;
  }
  apply();
  document.addEventListener("graphite:prefs", function (e) { apply(e.detail); });
})();
