/* The tutor page. Live: recent misses come from /api/me/history/questions, and once the server says the tutor is
   connected (GET /api/tutor), the message box sends the conversation to /api/tutor/chat, which asks Qwen.
   In the preview, or before QWEN_API_KEY / QWEN_BASE_URL is set, the conversation stays "Coming soon". */
(function () {
  "use strict";
  if (!document.querySelector(".tutor-page")) return;
  var API = window.GraphiteAPI, LIVE = !!(API && API.live);
  function $(id) { return document.getElementById(id); }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  var tools = window.GraphiteTools && window.GraphiteTools.mount({});
  var ctx = null;
  function about(q) {
    var box = $("tu-about");
    box.innerHTML = '<span class="label">Talking about</span><strong>' + esc(q.title) + "</strong>" + (q.detail ? '<span class="fine">' + esc(q.detail) + "</span>" : "");
    box.hidden = false;
    ctx = q;
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

  /* ---------- the conversation ---------- */
  var chat = $("tu-chat"), form = $("tu-form"), text = $("tu-text"), send = $("tu-send");
  var said = [], busy = false;
  function bubble(kind, words) {
    var el = document.createElement("div");
    el.className = "qt-msg" + (kind ? " is-" + kind : "");
    el.innerHTML = String(words).split(/\n{2,}/).map(function (p) { return "<p>" + esc(p).replace(/\n/g, "<br>") + "</p>"; }).join("");
    chat.appendChild(el);
    chat.scrollTop = chat.scrollHeight;
    return el;
  }
  function showLeft(lock) {
    var chip = $("tu-status");
    if (!lock || lock.left == null) { chip.hidden = true; return; }
    chip.hidden = false;
    chip.textContent = lock.left + " left today";
  }
  function ask(words) {
    words = (words || "").trim();
    if (!words || busy) return;
    busy = true; send.disabled = true;
    said.push({ role: "user", content: words });
    bubble("me", words);
    text.value = "";
    var wait = bubble("wait", "Thinking…");
    API.call("/api/tutor/chat", { messages: said, context: ctx }).then(function (r) {
      wait.remove();
      said.push({ role: "assistant", content: r.reply });
      bubble("", r.reply);
      showLeft(r.lock);
    }).catch(function (err) {
      wait.remove();
      said.pop();  // not answered, so it isn't part of the conversation
      text.value = words;
      var lock = err && err.data && err.data.code === "plan_required" && err.data.lock;
      if (lock && window.GraphiteLock) { showLeft(lock); window.GraphiteLock.dialog(lock); return; }
      if (err && err.status === 401) { location.href = "/signin.html?next=/tutor.html"; return; }
      bubble("err", (err && err.message) || "The tutor didn't answer. Try again in a moment.");
    }).then(function () { busy = false; send.disabled = false; text.focus(); });
  }
  function connect(st) {
    if (!st.connected) return;
    $("tu-soon").hidden = true;
    form.hidden = false;
    showLeft(st.lock);
    form.addEventListener("submit", function (e) { e.preventDefault(); ask(text.value); });
    text.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && !e.shiftKey && !e.isComposing) { e.preventDefault(); ask(text.value); }
    });
    $("tu-starts").querySelectorAll(".qt-ask").forEach(function (b) {
      b.disabled = false;
      b.addEventListener("click", function () {
        if (b.hasAttribute("data-send")) { ask(b.getAttribute("data-send")); return; }
        text.value = b.getAttribute("data-ask") || "";
        text.focus();
        text.setSelectionRange(text.value.length, text.value.length);
      });
    });
  }

  if (!LIVE) { render([]); return; }
  API.call("/api/tutor").then(connect).catch(function () { /* stays "Coming soon" */ });
  API.call("/api/me/history/questions").then(function (r) {
    var seen = {}, out = [];
    r.items.forEach(function (q) { if (q.correct === false && !seen[q.item_id] && out.length < 6) { seen[q.item_id] = 1; out.push(q); } });
    render(out);
  }).catch(function (err) {
    if (err && err.status === 401) { location.href = "/signin.html?next=/tutor.html"; return; }
    $("tu-misses").innerHTML = '<li class="fine">Your misses didn\'t load. Try again in a moment.</li>';
  });
})();
