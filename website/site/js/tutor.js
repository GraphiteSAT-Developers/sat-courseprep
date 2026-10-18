/* The tutor page. The conversation itself is a placeholder until the tutor is connected.
   Live: recent misses come from /api/me/history/questions. */
(function () {
  "use strict";
  if (!document.querySelector(".tutor-page")) return;
  var API = window.GraphiteAPI, LIVE = !!(API && API.live);
  function $(id) { return document.getElementById(id); }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  var tools = window.GraphiteTools && window.GraphiteTools.mount({});
  function about(q) {
    var box = $("tu-about");
    box.innerHTML = '<span class="label">Talking about</span><strong>' + esc(q.title) + "</strong>" + (q.detail ? '<span class="fine">' + esc(q.detail) + "</span>" : "");
    box.hidden = false;
    if (tools) tools.context(q);
  }
  function render(items) {
    var list = $("tu-misses");
    if (!items.length) { list.innerHTML = '<li class="fine">' + (LIVE ? "No misses yet. Questions you get wrong show up here." : "In the preview there's no history yet. On the live site your misses show up here.") + "</li>"; return; }
    list.innerHTML = items.map(function (q, i) {
      return '<li><button type="button" data-i="' + i + '"><strong>' + esc(q.skill || q.item_id) + '</strong><span class="fine">' + esc(q.source_name) + " · your answer: " + esc(q.answer) + "</span></button></li>";
    }).join("");
    list.addEventListener("click", function (e) {
      var b = e.target.closest("[data-i]"); if (!b) return;
      var q = items[+b.getAttribute("data-i")];
      about({ title: q.skill || "A question you missed", detail: q.source_name + " · your answer: " + q.answer });
      list.querySelectorAll("button").forEach(function (x) { x.classList.toggle("on", x === b); });
    });
  }
  if (!LIVE) { render([]); return; }
  API.call("/api/me/history/questions").then(function (r) {
    var seen = {}, out = [];
    r.items.forEach(function (q) { if (q.correct === false && !seen[q.item_id] && out.length < 6) { seen[q.item_id] = 1; out.push(q); } });
    render(out);
  }).catch(function (err) {
    if (err && err.status === 401) { location.href = "/signin.html?next=/tutor.html"; return; }
    $("tu-misses").innerHTML = '<li class="fine">Your misses didn\'t load. Try again in a moment.</li>';
  });
})();
