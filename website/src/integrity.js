/* Graphite SAT copy warnings, on every page with questions.
   Copying text from a question (or pasting into an answer) is noticed. The first time, a warning says that doing it
   again emails the student's parent. After that, each time is recorded, and linked parents get an email (the server
   sends at most one every 30 minutes). Live: POST /api/integrity/copy. Preview: counted in this browser, no email. */
(function () {
  "use strict";
  var API = window.GraphiteAPI;
  var LIVE = !!(API && API.live);
  var QUESTION = "#q-stem, #q-answer, .res-stem, .res-choices, .res-explain, .fb-explain, #sp-stem, #sp-choices, #pl-stem, #pl-answers, #pl-answer, " +
                 "#qstem, #qchoices, #ls-step";
  function page() {
    var p = location.pathname.split("/").pop().replace(".html", "") || "index";
    if (p === "practice-test" && document.documentElement.getAttribute("data-mock") === "1") return "mock-test";
    return p;
  }
  var KEY = "graphite_copy_count";
  var busy = false;

  function inside(node) {
    var el = node && (node.nodeType === 1 ? node : node.parentElement);
    return !!(el && el.closest && el.closest(QUESTION));
  }
  function selected() {
    var s = window.getSelection && window.getSelection();
    if (!s || s.isCollapsed || !s.rangeCount) return null;
    return s;
  }

  function dialog(title, text, tone) {
    var old = document.getElementById("copy-warn");
    if (old) old.remove();
    var wrap = document.createElement("div");
    wrap.className = "overlay copy-warn";
    wrap.id = "copy-warn";
    wrap.innerHTML = '<div class="dialog" role="alertdialog" aria-modal="true" aria-labelledby="copy-warn-title" aria-describedby="copy-warn-text">' +
      '<p class="label"></p><h2 id="copy-warn-title"></h2><p id="copy-warn-text"></p>' +
      '<div class="dialog-actions"><button class="btn btn-primary" type="button">I understand</button></div></div>';
    wrap.querySelector(".label").textContent = tone === "warn" ? "Warning" : "Recorded";
    wrap.querySelector("h2").textContent = title;
    wrap.querySelector("#copy-warn-text").textContent = text;
    var last = document.activeElement;
    function close() { wrap.remove(); if (last && last.focus) last.focus(); }
    wrap.querySelector("button").addEventListener("click", close);
    wrap.addEventListener("keydown", function (e) { if (e.key === "Escape") close(); });
    (document.querySelector(".exam") || document.body).appendChild(wrap);
    wrap.querySelector("button").focus();
  }

  function show(r) {
    var parent = r.parents > 0;
    if (r.action === "warned") {
      dialog("Copying questions isn't allowed",
        "Copying a question, or pasting an answer in, usually means looking the answer up instead of working it out. This time it's only a warning. " +
        (parent ? "If it happens again, your parent will get an email about it." :
                  "If it happens again, it's recorded on your account, and once a parent is connected they'll get an email about it."), "warn");
    } else if (r.action === "parent_emailed") {
      dialog("Your parent was emailed", "You were warned last time, so we emailed your parent that you copied or pasted question text. " +
        "It's also recorded on your account.", "note");
    } else if (r.action === "recorded") {
      dialog("This was recorded", parent ? "Copying or pasting question text was recorded on your account, and your parent has been emailed about it."
        : "Copying or pasting question text was recorded on your account.", "note");
    }
  }

  function report(kind, chars) {
    if (busy) return;
    busy = true;
    var data = { kind: kind, page: page(), chars: chars };
    var done = function (r) { busy = false; show(r || {}); };
    if (LIVE) {
      API.call("/api/integrity/copy", data).then(done).catch(function () { busy = false; });
      return;
    }
    // Preview: the same rules, counted in this browser. No email can be sent from the preview.
    var n = 0;
    try { n = Number(localStorage.getItem(KEY)) || 0; localStorage.setItem(KEY, String(n + 1)); } catch (e) { /* storage blocked */ }
    done({ action: n === 0 ? "warned" : "recorded", parents: 0 });
  }

  function onCopy(e) {
    var s = selected();
    if (!s || !(inside(s.anchorNode) || inside(s.focusNode))) return;
    report(e.type, String(s).length);
  }
  document.addEventListener("copy", onCopy);
  document.addEventListener("cut", onCopy);
  document.addEventListener("paste", function (e) {
    if (!inside(e.target)) return;
    var text = "";
    try { text = (e.clipboardData || window.clipboardData).getData("text") || ""; } catch (err) { /* no clipboard access */ }
    report("paste", text.length);
  });
})();
