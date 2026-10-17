/* Graphite lessons: active recall instead of reading. Every step asks for an answer before it explains.
   Step types (backend/app/services/lessons.py): recall, predict, fill, order, spot.
   Live: /api/lessons. Preview: the same requests go to play-local.js. */
(function () {
  "use strict";
  if (!document.querySelector(".lessons-page")) return;
  var R = window.GraphiteRewards, call = R && R.call(), esc = R.esc;
  var API = window.GraphiteAPI, LIVE = !!(API && API.live);
  var params = new URLSearchParams(location.search);
  var lesson = null, steps = [], kind = "lesson", at = 0, score = 0, answered = false, answers = [], pending = null;
  function $(id) { return document.getElementById(id); }
  function signIn() { location.href = "/signin.html?next=" + encodeURIComponent("/lessons.html" + location.search); }
  function showError(m) { $("ls-error").textContent = m || ""; $("ls-error").hidden = !m; }
  function failed(err, fallback) { if (err && err.status === 401) { signIn(); return; } showError(err && err.status ? err.message : fallback); }
  if (!LIVE) $("ls-preview-note").hidden = false;
  if (!call) { $("ls-loading").textContent = "Lessons aren't available in this preview."; return; }

  function day(iso) { var p = iso.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]).toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric" }); }
  function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }

  /* ---------- the list ---------- */
  function stateText(p, days) {
    if (!p.done) return { chip: "New", cls: "chip-quiet", line: "" };
    if (p.mastered) return { chip: "Mastered", cls: "", line: "All " + days.length + " recall checks passed." };
    if (p.due) return { chip: "Recall due", cls: "chip-due", line: "Your recall check is ready." };
    return { chip: "Done", cls: "chip-quiet", line: "Next recall check " + day(p.due_on) + "." };
  }
  function stageDots(p, days) {
    var out = "";
    for (var i = 0; i < days.length; i++) out += '<i class="' + (i < p.stage ? "is-on" : "") + '"></i>';
    return '<span class="ls-stages" aria-label="' + p.stage + " of " + days.length + ' recall checks passed">' + out + "</span>";
  }
  function renderList(o) {
    $("ls-loading").hidden = true;
    var due = o.lessons.filter(function (l) { return l.progress.due; });
    $("ls-due").hidden = !due.length;
    $("ls-due-count").textContent = due.length + " due";
    $("ls-due-list").innerHTML = due.map(function (l) {
      return '<li><span><strong>' + esc(l.title) + '</strong><span class="fine">' + esc(l.skill_name) + "</span></span>" +
        '<a class="btn btn-primary" href="lessons.html?lesson=' + encodeURIComponent(l.id) + '&amp;mode=recall">Start recall check</a></li>';
    }).join("");
    var groups = {}, order = [];
    o.lessons.forEach(function (l) { if (!groups[l.domain]) { groups[l.domain] = []; order.push(l.domain); } groups[l.domain].push(l); });
    $("ls-groups").innerHTML = order.map(function (d) {
      return '<section class="panel" aria-labelledby="ls-g-' + esc(d) + '"><div class="panel-head"><h2 id="ls-g-' + esc(d) + '">' + esc(groups[d][0].domain_name) + "</h2></div>" +
        '<ul class="ls-list">' + groups[d].map(function (l) {
          var st = stateText(l.progress, o.recall_days);
          return '<li class="ls-item"><div class="ls-item-copy"><h3><a href="lessons.html?lesson=' + encodeURIComponent(l.id) + '">' + esc(l.title) + "</a></h3>" +
            '<p class="fine">' + esc(l.hook) + "</p>" +
            '<p class="ls-meta"><span class="chip ' + st.cls + '">' + st.chip + "</span><span>" + l.minutes + " min · " + l.steps + " steps · " + esc(l.skill_name) + "</span>" +
            (l.progress.done ? stageDots(l.progress, o.recall_days) : "") + "</p>" + (st.line ? '<p class="fine">' + st.line + "</p>" : "") + "</div>" +
            '<a class="btn ' + (l.progress.done ? "btn-quiet" : "btn-secondary") + '" href="lessons.html?lesson=' + encodeURIComponent(l.id) + '">' + (l.progress.done ? "Do it again" : "Start") + "</a></li>";
        }).join("") + "</ul></section>";
    }).join("");
  }

  /* ---------- one lesson ---------- */
  function open(id, mode) {
    $("ls-list-view").hidden = true;
    call("/api/lessons/" + encodeURIComponent(id)).then(function (r) {
      lesson = r.lesson;
      kind = mode === "recall" && lesson.progress.done ? "recall" : "lesson";
      steps = kind === "recall" ? lesson.recall : lesson.steps;
      at = 0; score = 0; answers = [];
      $("ls-kicker").textContent = (kind === "recall" ? "Recall check · " : "Lesson · ") + lesson.skill_name;
      $("ls-title").textContent = lesson.title;
      document.title = lesson.title + " | Graphite SAT Tutoring";
      $("ls-player").hidden = false;
      $("ls-progress").setAttribute("aria-valuemax", String(steps.length));
      renderStep();
      $("ls-title").focus();
    }).catch(function (err) {
      $("ls-list-view").hidden = false;
      failed(err, "We couldn't open that lesson.");
      loadList();
    });
  }
  function progress() {
    $("ls-progress").firstElementChild.style.width = Math.round(at / steps.length * 100) + "%";
    $("ls-progress").setAttribute("aria-valuenow", String(at));
    $("ls-step-count").textContent = "Step " + (at + 1) + " of " + steps.length + (kind === "recall" ? " · from memory, no notes" : "");
  }
  var KICK = { recall: "From memory", predict: "Predict first", fill: "Fill in the step", order: "Put it in order", spot: "Find the mistake" };
  function table(t) {
    if (!t) return "";
    return '<div class="ls-table-wrap"><table class="ls-table">' + (t.caption ? "<caption>" + esc(t.caption) + "</caption>" : "") +
      "<thead><tr>" + t.head.map(function (h) { return '<th scope="col">' + esc(h) + "</th>"; }).join("") + "</tr></thead><tbody>" +
      t.rows.map(function (r) { return "<tr>" + r.map(function (c, i) { return i ? "<td>" + esc(c) + "</td>" : '<th scope="row">' + esc(c) + "</th>"; }).join("") + "</tr>"; }).join("") +
      "</tbody></table></div>";
  }
  function feedback(right, why, extra) {
    var f = document.createElement("div");
    f.className = "ls-fb " + (right ? "ok" : "no"); f.tabIndex = -1;
    f.innerHTML = "<strong>" + (right ? ["Right.", "Yes.", "Exactly.", "Got it."][at % 4] : "Not quite.") + "</strong> " + (extra || "") + (why ? "<span>" + esc(why) + "</span>" : "");
    $("ls-step").appendChild(f);
    if (right) score++;
    answers[at] = pending;  // the first try, sent to the server, which does the grading
    answered = true;
    $("ls-next").hidden = false;
    $("ls-next").textContent = at + 1 < steps.length ? "Next" : "Finish";
    $("ls-next").focus();
  }

  function renderStep() {
    var s = steps[at], box = $("ls-step");
    answered = false; $("ls-next").hidden = true;
    progress();
    box.className = "panel ls-step is-" + s.type;
    box.innerHTML = '<p class="label">' + KICK[s.type] + "</p>" + table(s.table) + '<p class="ls-prompt">' + esc(s.prompt) + "</p>";
    ({ recall: stepRecall, predict: stepPredict, fill: stepFill, order: stepOrder, spot: stepSpot })[s.type](s, box);
  }

  function stepRecall(s, box) {
    var area = document.createElement("div"); area.className = "ls-recall";
    area.innerHTML = '<label class="fine" for="ls-recall-text">Type it, or just say it in your head:</label><textarea id="ls-recall-text" rows="3"></textarea>' +
      '<button class="btn btn-secondary" type="button">Show the answer</button>';
    box.appendChild(area);
    area.querySelector("button").addEventListener("click", function () {
      this.remove();
      var rev = document.createElement("div"); rev.className = "ls-reveal";
      rev.innerHTML = '<p class="label">Answer</p><p class="ls-answer">' + esc(s.answer) + '</p><p class="fine">How did you do?</p>' +
        '<div class="ls-rate"><button class="btn btn-quiet" type="button" data-r="1">Got it</button><button class="btn btn-quiet" type="button" data-r="0">Partly</button><button class="btn btn-quiet" type="button" data-r="0">Not yet</button></div>';
      box.appendChild(rev);
      rev.querySelector(".ls-rate").addEventListener("click", function (e) {
        var b = e.target.closest("button"); if (!b || answered) return;
        Array.prototype.forEach.call(this.querySelectorAll("button"), function (x) { x.disabled = true; x.classList.toggle("is-picked", x === b); });
        pending = b.getAttribute("data-r") === "1";
        feedback(pending, pending ? "" : "That's what the rest of this lesson is for.");
      });
      rev.querySelector(".ls-rate button").focus();
    });
  }
  function stepPredict(s, box) {
    var list = document.createElement("div"); list.className = "ls-choices"; list.setAttribute("role", "group"); list.setAttribute("aria-label", "Choices");
    s.choices.forEach(function (c, k) {
      var b = document.createElement("button"); b.type = "button"; b.className = "sp-choice";
      b.innerHTML = '<span class="mc-letter">' + "ABCD"[k] + '</span><span class="mc-text">' + esc(c) + "</span>";
      b.addEventListener("click", function () {
        if (answered) return;
        Array.prototype.forEach.call(list.children, function (x, i) { x.disabled = true; if (i === s.answer) x.classList.add("is-key"); });
        if (k !== s.answer) b.classList.add("is-wrong");
        pending = k;
        feedback(k === s.answer, s.why);
      });
      list.appendChild(b);
    });
    box.appendChild(list);
  }
  function norm(v) { return String(v || "").replace(/[\s,]/g, "").replace(/[−–]/g, "-").replace(/%$/, "").toLowerCase(); }
  function value(v) {
    v = norm(v);
    var m = /^(-?\d+)\/(\d+)$/.exec(v); if (m) return Number(m[1]) / Number(m[2]);
    return /^-?(\d+\.?\d*|\.\d+)$/.test(v) ? Number(v) : NaN;
  }
  function matches(input, accept) {
    var n = value(input);
    return accept.some(function (a) { var x = value(a); return !isNaN(n) && !isNaN(x) ? Math.abs(n - x) < 1e-9 : norm(a) === norm(input); });
  }
  function stepFill(s, box) {
    var work = document.createElement("form"); work.className = "ls-work"; work.setAttribute("novalidate", "");
    work.innerHTML = s.lines.map(function (line) {
      if (line.indexOf("___") < 0) return '<p class="ls-line">' + esc(line) + "</p>";
      var parts = line.split("___");
      return '<p class="ls-line">' + esc(parts[0]) + '<label class="visually-hidden" for="ls-blank">Missing value</label><input id="ls-blank" class="ls-blank" data-no-filter autocomplete="off" inputmode="decimal" spellcheck="false" maxlength="12">' + esc(parts[1] || "") + "</p>";
    }).join("") + '<button class="btn btn-secondary" type="submit">Check</button>';
    box.appendChild(work);
    var input = work.querySelector("input"); input.focus();
    work.addEventListener("submit", function (e) {
      e.preventDefault();
      if (answered || !input.value.trim()) { input.focus(); return; }
      var right = matches(input.value, s.accept);
      pending = input.value.trim();
      input.readOnly = true; input.classList.add(right ? "is-right" : "is-wrong");
      work.querySelector("button").remove();
      feedback(right, s.why, right ? "" : "It's <strong>" + esc(s.accept[0]) + "</strong>. ");
    });
  }
  function stepOrder(s, box) {
    var placed = [], pool = shuffle(s.items.map(function (t, i) { return i; }));
    if (pool.every(function (v, i) { return v === i; }) && pool.length > 1) pool.push(pool.shift());  // never start already in order
    var wrap = document.createElement("div"); wrap.className = "ls-order";
    wrap.innerHTML = '<div><p class="fine">Tap the steps in order.</p><ol class="ls-pool" id="ls-pool"></ol></div><div><p class="fine">Your order (tap one to take it back):</p><ol class="ls-placed" id="ls-placed"></ol></div>' +
      '<button class="btn btn-secondary" type="button" id="ls-order-check" disabled>Check</button>';
    box.appendChild(wrap);
    function draw() {
      $("ls-pool").innerHTML = pool.map(function (i) { return '<li><button type="button" class="ls-tile" data-i="' + i + '">' + esc(s.items[i]) + "</button></li>"; }).join("");
      $("ls-placed").innerHTML = placed.map(function (i, n) { return '<li><button type="button" class="ls-tile is-placed" data-i="' + i + '"><span class="ls-n">' + (n + 1) + "</span>" + esc(s.items[i]) + "</button></li>"; }).join("");
      $("ls-order-check").disabled = placed.length !== s.items.length;
    }
    wrap.addEventListener("click", function (e) {
      var b = e.target.closest(".ls-tile"); if (!b || answered) return;
      var i = Number(b.getAttribute("data-i"));
      if (b.classList.contains("is-placed")) { placed.splice(placed.indexOf(i), 1); pool.push(i); } else { pool.splice(pool.indexOf(i), 1); placed.push(i); }
      draw();
      var next = $("ls-pool").querySelector("button") || $("ls-order-check"); if (next && !next.disabled) next.focus();
    });
    $("ls-order-check").addEventListener("click", function () {
      if (answered) return;
      var right = placed.every(function (v, n) { return v === n; });
      pending = placed.slice();
      this.remove();
      Array.prototype.forEach.call($("ls-placed").querySelectorAll(".ls-tile"), function (b, n) { b.disabled = true; b.classList.add(placed[n] === n ? "is-right" : "is-wrong"); });
      var correct = right ? "" : "<ol class=\"ls-correct\">" + s.items.map(function (t) { return "<li>" + esc(t) + "</li>"; }).join("") + "</ol>";
      feedback(right, s.why, right ? "" : "Here's the order:" + correct);
    });
    draw();
  }
  function stepSpot(s, box) {
    var list = document.createElement("ol"); list.className = "ls-lines";
    s.lines.forEach(function (line, k) {
      var li = document.createElement("li"), b = document.createElement("button");
      b.type = "button"; b.className = "ls-tile"; b.textContent = line;
      b.addEventListener("click", function () {
        if (answered) return;
        Array.prototype.forEach.call(list.querySelectorAll("button"), function (x, i) { x.disabled = true; if (i === s.wrong) x.classList.add("is-key-wrong"); });
        if (k !== s.wrong) b.classList.add("is-picked");
        pending = k;
        feedback(k === s.wrong, s.why, k === s.wrong ? "" : "The mistake is in line " + (s.wrong + 1) + ". ");
      });
      li.appendChild(b); list.appendChild(li);
    });
    box.appendChild(list);
  }

  $("ls-next").addEventListener("click", function () {
    if (!answered) return;
    at++;
    if (at < steps.length) { renderStep(); var p = $("ls-step").querySelector("button, input, textarea"); if (p) p.focus({ preventScroll: true }); $("ls-step").scrollIntoView({ block: "nearest" }); return; }
    finishLesson();
  });
  function finishLesson() {
    var b = $("ls-next"); b.disabled = true; b.textContent = "Saving…";
    call("/api/lessons/" + encodeURIComponent(lesson.id) + "/complete", { kind: kind, answers: answers }).then(function (r) {
      b.disabled = false;
      $("ls-player").hidden = true; $("ls-end").hidden = false;
      $("ls-end-kicker").textContent = kind === "recall" ? "Recall check finished" : "Lesson finished";
      $("ls-end-title").textContent = kind === "recall" ? (r.passed ? "It stuck." : "Almost there.") : r.score === steps.length ? "Every step right the first time." : "Lesson done.";
      $("ls-end-score").textContent = r.score + " of " + steps.length + " right the first time." +
        (kind === "recall" && !r.passed ? " This one comes back tomorrow for another try." : "");
      $("ls-keys").innerHTML = lesson.keys.map(function (k) { return "<li>" + esc(k) + "</li>"; }).join("");
      var p = r.progress;
      $("ls-next-recall").innerHTML = p.mastered ? "<strong>Mastered.</strong> You've passed every recall check for this lesson."
        : p.due_on ? "Recall check <strong>" + (p.due_on === new Date().toISOString().slice(0, 10) ? "today" : day(p.due_on)) + "</strong>: three questions from memory, " + (p.stage + 1) + " of " + lesson.recall_days.length + "." : "";
      $("ls-practice").setAttribute("data-domain", lesson.domain); $("ls-practice").setAttribute("data-skill", lesson.skill);
      if (r.xp || r.coins || (r.badges && r.badges.length)) R.show(r);
      $("ls-end-title").focus();
    }).catch(function (err) { b.disabled = false; b.textContent = "Finish"; failed(err, "We couldn't save your lesson. Check your connection and press Finish again."); });
  }
  // "Practice this skill": a 10-question topic set on the lesson's skill.
  $("ls-practice").addEventListener("click", function (e) {
    var a = this, d = a.getAttribute("data-domain"); if (!d) return;
    e.preventDefault();
    var practice = LIVE ? API.call : (window.GraphitePracticeLocal && window.GraphitePracticeLocal.call);
    a.textContent = "Building your set…";
    practice("/api/practice/sessions", { mode: "topic", domain: d, skill: a.getAttribute("data-skill"), count: 10 }).then(function (r) {
      location.href = "practice-test.html?session=" + r.session.id;
    }).catch(function () { location.href = "practice.html"; });
  });

  function loadList() {
    return call("/api/lessons").then(renderList).catch(function (err) {
      if (err && err.status === 401) { signIn(); return; }
      $("ls-loading").textContent = err && err.status === 403 ? "Lessons are for student accounts." : "We couldn't load lessons. Check your connection and refresh the page.";
    });
  }
  if (params.get("lesson")) open(params.get("lesson"), params.get("mode")); else loadList();
})();
