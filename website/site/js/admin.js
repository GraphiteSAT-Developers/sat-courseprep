/* Graphite SAT admin page: home page signups and accounts, from /api/admin (ADMIN_ACCOUNTS only). */
(function () {
  "use strict";
  function $(id) { return document.getElementById(id); }
  var API = window.GraphiteAPI;
  if (!$("ad-students")) return;
  if (!(API && API.live)) { $("ad-preview-note").hidden = false; return; }

  function day(iso) { return iso ? new Date(iso).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" }) : ""; }
  function fill(id, rows, cells, empty) {
    var body = $(id); body.innerHTML = "";
    if (!rows.length) { var tr = document.createElement("tr"), td = document.createElement("td"); td.colSpan = 7; td.textContent = empty; tr.appendChild(td); body.appendChild(tr); return; }
    rows.forEach(function (r) {
      var tr = document.createElement("tr");
      cells(r).forEach(function (v) { var td = document.createElement("td"); td.textContent = v == null ? "" : v; tr.appendChild(td); });
      body.appendChild(tr);
    });
  }

  API.call("/api/admin").then(function (d) {
    var c = d.counts;
    $("ad-counts").textContent = c.students + " students, " + c.parents + " parents, " + c.leads + " home page signups." +
      (Math.max(c.students, c.parents, c.leads) > d.limit ? " Lists show the newest " + d.limit + "." : "");
    fill("ad-students", d.students, function (s) {
      return [day(s.created_at), s.name, s.email, s.grade, s.test_date, s.target_score, s.plan_name + (s.status === "active" ? "" : " (" + s.status.replace("_", " ") + ")")];
    }, "No students yet.");
    fill("ad-leads", d.leads, function (l) { return [day(l.created_at), l.name, l.email, l.grade, l.test_date, l.target_score, l.message]; }, "No signups yet.");
    fill("ad-parents", d.parents, function (p) { return [day(p.created_at), p.name, p.email]; }, "No parents yet.");
  }).catch(function (err) {
    var s = $("ad-status"); s.className = "status is-shown err"; s.textContent = (err && err.message) || "The admin data didn't load.";
  });
})();
