/* The tutor page. Live: recent misses come from /api/me/history/questions, and once the tutor is switched on
   (/api/tutor says enabled) the conversation runs on the same chat as the Tutor tab (qtools.js, GraphiteTutor).
   Off, or in the static preview, the page keeps its "coming soon" conversation. */
(function () {
  "use strict";
  if (!document.querySelector(".tutor-page")) return;
  var API = window.GraphiteAPI, LIVE = !!(API && API.live);
  function $(id) { return document.getElementById(id); }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  var tools = window.GraphiteTools && window.GraphiteTools.mount({});
  var chat = null, picked = null, all = null;
  // The Math | Reading and Writing switch (site.js) picks which misses show. Reading and Writing questions have ids that start with rw-.
  function subject() { return document.documentElement.getAttribute("data-subject") === "rw" ? "rw" : "math"; }
  function sectionOf(q) { return /^rw-/.test(q.item_id || "") ? "rw" : "math"; }
  function missedSkills() {
    var seen = {}, out = [];
    (all || []).forEach(function (q) { if (sectionOf(q) === subject() && q.skill && !seen[q.skill]) { seen[q.skill] = 1; out.push(q.skill); } });
    return out.slice(0, 3);
  }
  // Ways to start: "send" goes straight to the tutor; "fill" starts the message for the student to finish.
  var STARTS = [
    { label: "Explain a topic", fill: "Can you explain " },
    { label: "Check my work", fill: "Can you check my work? Here's what I did: " },
    { label: "Quiz me on what I missed", send: function () {
      var s = missedSkills();
      return s.length ? "Quiz me with one quick question on " + s.join(", ") + ", then check my answer." : "Quiz me with one quick SAT question, then check my answer.";
    } },
    { label: "Show me the Desmos way", subject: "math", send: "Can you show me the Desmos way for this one?", needs: "item" },
    { label: "Point me to the line that proves it", subject: "rw", send: "Can you point me to the part of the passage that settles this?", needs: "item" },
    { label: "Explain this grammar rule", subject: "rw", send: "Can you explain the grammar rule this question tests?", needs: "item" },
    { label: "Where did I go wrong?", send: "Where did I go wrong?", needs: "item" },
    { label: "Plan my week", send: "Help me plan my SAT study for this week." }
  ];
  function about(q) {
    var box = $("tu-about");
    box.innerHTML = '<span class="label">Talking about</span><strong>' + esc(q.title) + "</strong>" + (q.detail ? '<span class="fine">' + esc(q.detail) + "</span>" : "");
    box.hidden = false;
    if (tools) tools.context(q);
    if (chat) chat.setContext(q);
  }
  function context() { return picked || { title: subject() === "rw" ? "Reading and Writing" : "Math" }; }
  document.addEventListener("graphite:subject", function () {
    if (all) render(all);
    if (chat && !picked) chat.setContext(context());
  });
  function render(every) {
    all = every;
    var list = $("tu-misses");
    var items = every.filter(function (q) { return sectionOf(q) === subject(); }).slice(0, 6);
    if (!items.length) { list.innerHTML = '<li class="fine">' + (LIVE ? "No misses yet. Questions you get wrong show up here." : "In the preview there's no history yet. On the live site your misses show up here.") + "</li>"; return; }
    list.innerHTML = items.map(function (q, i) {
      return '<li><button type="button" data-i="' + i + '"><strong>' + esc(q.skill || q.item_id) + '</strong><span class="fine">' + esc(q.source_name) + " · your answer: " + esc(q.answer) + "</span></button></li>";
    }).join("");
    list.onclick = function (e) {
      var b = e.target.closest("[data-i]"); if (!b) return;
      var q = items[+b.getAttribute("data-i")];
      // Only questions from the bank (they have a skill) can go to the tutor by id; others are talked through in general.
      picked = { title: q.skill || "A question you missed", detail: q.source_name + " · your answer: " + q.answer,
                 item_id: q.skill ? q.item_id : null, section: sectionOf(q) };
      about(picked);
      list.querySelectorAll("button").forEach(function (x) { x.classList.toggle("on", x === b); });
      if (chat) chat.focus();
    };
  }
  if (!LIVE) { render([]); return; }
  window.GraphiteTutor.status().then(function (st) {
    if (!st || !st.enabled) return;
    var host = $("tu-live");
    host.innerHTML = ""; host.classList.add("qt-live");
    $("tu-soon").hidden = true;
    chat = window.GraphiteTutor.chat(host, { starters: STARTS, credits: st.credits });
    chat.setContext(context());
  });
  API.call("/api/me/history/questions").then(function (r) {
    var seen = {}, out = [];
    r.items.forEach(function (q) { if (q.correct === false && !seen[q.item_id]) { seen[q.item_id] = 1; out.push(q); } });
    render(out);
  }).catch(function (err) {
    if (err && err.status === 401) { location.href = "/signin.html?next=/tutor.html"; return; }
    $("tu-misses").innerHTML = '<li class="fine">Your misses didn\'t load. Try again in a moment.</li>';
  });
})();
