/* Graphite SAT lessons: active recall instead of reading. Every step asks for an answer before it explains.
   Step types (backend/app/services/lessons.py): recall, predict, fill, order, spot, and the hands-on ones:
   slider, plot, graph, sort, match, line, build, grid, flash (drawn with lesson-kit.js).
   Each lesson has a format that changes how it plays (hearts, a clock, a cold open, a story, a case file,
   a shortcut, checking a student's work, a race, an experiment, or the classic flow).
   Desmos hacks opens first for everyone; the rest of the list opens after it.
   Live: /api/lessons. Preview: the same requests go to play-local.js. */
(function () {
  "use strict";
  if (!document.querySelector(".lessons-page")) return;
  var R = window.GraphiteRewards, call = R && R.call(), esc = R.esc;
  var K = window.GraphiteLessonKit, T = K ? K.tex : esc, P = K ? K.plain : String;
  var API = window.GraphiteAPI, LIVE = !!(API && API.live);
  var params = new URLSearchParams(location.search);
  var START = "desmos-hacks";
  var lesson = null, steps = [], kind = "lesson", at = 0, answered = false, answers = [], pending = null, firstTime = false;
  var allLessons = true;  // false on the free plan, which opens the starter lessons only
  var play = null;  // per-run format state: hearts, clock, lanes, shortcut
  function $(id) { return document.getElementById(id); }
  function signIn() { location.href = "/signin.html?next=" + encodeURIComponent("/lessons.html" + location.search); }
  function showError(m) { $("ls-error").textContent = m || ""; $("ls-error").hidden = !m; }
  function failed(err, fallback) { if (err && err.status === 401) { signIn(); return; } showError(err && err.status ? err.message : fallback); }
  function startFirst(err) { return err && err.status === 409 && err.data && err.data.code === "start_first"; }
  if (!LIVE) $("ls-preview-note").hidden = false;
  // Calculator and tutor (qtools.js), on math and Desmos lessons.
  var tools = window.GraphiteTools && window.GraphiteTools.mount({});
  if (tools) tools.available(false);
  if (!call || !K) { $("ls-loading").textContent = "Lessons aren't available in this preview."; return; }

  function day(iso) { var p = iso.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]).toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric" }); }
  function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  function mixed(n) { var o = shuffle(Array.from({ length: n }, function (_, i) { return i; })); if (n > 1 && o.every(function (v, i) { return v === i; })) o.push(o.shift()); return o; }
  function each(list, fn) { Array.prototype.forEach.call(list, fn); }

  var FORMAT = {
    classic: "Classic", lives: "Three hearts", timed: "Beat the clock", "cold-open": "Cold open", story: "Story",
    "case": "Case file", path: "Shortcut", teach: "Check the work", race: "Race", lab: "Experiment"
  };
  var HEART = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7.5-4.6-9.6-9.2C.9 8.4 3 4.5 6.7 4.5c2.1 0 3.6 1.2 5.3 3.1 1.7-1.9 3.2-3.1 5.3-3.1 3.7 0 5.8 3.9 4.3 7.3C19.5 16.4 12 21 12 21z"/></svg>';

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
  // The Math | Reading and Writing switch (site.js) picks which lessons show. Reading and Writing lessons
  // don't wait for Desmos hacks.
  function subject() { return document.documentElement.getAttribute("data-subject") === "rw" ? "rw" : "math"; }
  var listData = null;
  document.addEventListener("graphite:subject", function () { if (listData && !$("ls-list-view").hidden) renderList(listData); });
  function renderList(o) {
    listData = o;
    $("ls-loading").hidden = true;
    var rw = subject() === "rw";
    $("ls-lede-rw").hidden = !rw; $("ls-lede-math").hidden = rw;
    var locked = !!o.start_with && !rw;
    $("ls-start").hidden = !locked;
    var due = o.lessons.filter(function (l) { return l.progress.due && !l.locked; });
    // The free plan opens a few starter lessons; the rest come with a paid plan (services/access.py).
    var lock = o.access && !o.access.ok && window.GraphiteLock ? o.access : null;
    var plan = $("ls-plan");
    if (plan) {
      plan.innerHTML = "";
      plan.hidden = !lock;
      if (lock) {
        var byId = {}; o.lessons.forEach(function (l) { byId[l.id] = l; });
        var free = (o.free_lessons || []).map(function (id) { return byId[id]; }).filter(Boolean);
        var card = window.GraphiteLock.card(lock, true);
        card.querySelector("p").textContent = (lock.reason ? card.querySelector("p").textContent + " " : "") +
          "Open on your plan: " + free.map(function (l) { return P(l.title).replace(/:.*$/, ""); }).join(", ") + ". " +
          (lock.reason ? "" : lock.need_name + " and up open all " + o.lessons.length + ".");
        plan.appendChild(card);
      }
    }
    $("ls-due").hidden = !due.length;
    $("ls-due-count").textContent = due.length + " due";
    $("ls-due-list").innerHTML = due.map(function (l) {
      return '<li><span><strong>' + T(l.title) + '</strong><span class="fine">' + esc(l.skill_name) + "</span></span>" +
        '<a class="btn btn-primary" href="lessons.html?lesson=' + encodeURIComponent(l.id) + '&amp;mode=recall">Start recall check</a></li>';
    }).join("");
    var groups = {}, order = [];
    o.lessons.filter(function (l) { return (l.section || "math") === subject(); })
      .forEach(function (l) { if (!groups[l.domain]) { groups[l.domain] = []; order.push(l.domain); } groups[l.domain].push(l); });
    var ABOUT = { memory: "How to make anything you study stick, and how these lessons use it.",
                  desmos: "The calculator you get on test day. Start with Desmos hacks, then the moves one at a time, and when doing it by hand is faster.",
                  "craft-structure": "The first questions in every module: precise words, what a sentence is doing, and how two texts talk to each other.",
                  "information-ideas": "Main ideas, the evidence that proves a claim (quotes, findings, tables and graphs), and what must be true.",
                  "conventions": "Where sentences end, and making every subject, verb, pronoun and modifier agree.",
                  "expression-ideas": "The last questions in every module: transitions and writing from a student's notes." };
    $("ls-jump").innerHTML = order.map(function (d) {
      var done = groups[d].filter(function (l) { return l.progress.done; }).length;
      return '<li><a href="#ls-sec-' + esc(d) + '">' + esc(groups[d][0].domain_name) + ' <span class="fine">' + done + "/" + groups[d].length + "</span></a></li>";
    }).join("");
    $("ls-jump-wrap").hidden = order.length < 2;
    $("ls-groups").innerHTML = order.map(function (d) {
      var done = groups[d].filter(function (l) { return l.progress.done; }).length;
      return '<section class="panel ls-group" id="ls-sec-' + esc(d) + '" aria-labelledby="ls-g-' + esc(d) + '"><div class="panel-head"><h2 id="ls-g-' + esc(d) + '">' + esc(groups[d][0].domain_name) + '</h2><span class="label">' + done + " of " + groups[d].length + " done</span></div>" +
        (ABOUT[d] ? '<p class="panel-lede">' + ABOUT[d] + "</p>" : "") +
        '<ul class="ls-list">' + groups[d].map(function (l) {
          var st = stateText(l.progress, o.recall_days), paid = !!(lock && l.locked), shut = paid || (locked && l.id !== o.start_with);
          var href = "lessons.html?lesson=" + encodeURIComponent(l.id);
          if (paid && l.progress.due === false && l.progress.done && !l.progress.mastered) st = { chip: "Done", cls: "chip-quiet", line: "Recall checks wait until your plan includes this lesson." };
          return '<li class="ls-item' + (shut ? " is-locked" : "") + (paid ? " is-plan-locked" : "") + (l.id === START ? " is-start" : "") + '"><div class="ls-item-copy"><h3>' + (shut ? T(l.title) : '<a href="' + href + '">' + T(l.title) + "</a>") + "</h3>" +
            '<p class="fine">' + T(l.hook) + "</p>" +
            '<p class="ls-meta">' + (lock && l.free ? '<span class="chip ls-free-chip">Free</span>' : "") + '<span class="chip ' + st.cls + '">' + st.chip + '</span><span class="ls-format-chip ls-f-' + esc(l.format || "classic") + '">' + esc(FORMAT[l.format] || "Classic") + "</span><span>" + l.minutes + " min · " + l.steps + " steps · " + esc(l.skill_name) + "</span>" +
            (l.progress.done ? stageDots(l.progress, o.recall_days) : "") + "</p>" + (st.line ? '<p class="fine">' + st.line + "</p>" : "") + "</div>" +
            (paid ? '<a class="btn btn-quiet ls-plan-btn" href="' + esc(window.GraphiteLock.url(lock)) + '"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="10.5" width="14" height="10" rx="2.2" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M8.5 10.5V8a3.5 3.5 0 0 1 7 0v2.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>' + (lock.reason ? "Fix payment" : "With " + esc(lock.need_name)) + "</a>"
             : shut ? '<span class="ls-lock fine">Opens after Desmos hacks</span>'
                  : '<a class="btn ' + (l.progress.done ? "btn-quiet" : "btn-secondary") + '" href="' + href + '">' + (l.progress.done ? "Do it again" : "Start") + "</a>") + "</li>";
        }).join("") + "</ul></section>";
    }).join("");
  }

  /* ---------- one lesson ---------- */
  function open(id, mode, note) {
    $("ls-list-view").hidden = true;
    call("/api/lessons/" + encodeURIComponent(id)).then(function (r) {
      lesson = r.lesson;
      allLessons = r.all_lessons !== false;
      firstTime = lesson.id === START && !lesson.progress.done;
      kind = mode === "recall" && lesson.progress.done ? "recall" : "lesson";
      steps = kind === "recall" ? lesson.recall : lesson.steps;
      $("ls-kicker").textContent = (kind === "recall" ? "Recall check · " : "Lesson · ") + lesson.skill_name;
      $("ls-title").innerHTML = T(lesson.title);
      document.title = P(lesson.title) + " | Graphite SAT";
      if (window.GraphiteCrumb) window.GraphiteCrumb(P(lesson.title), "lessons.html?list=1");
      if (tools) { tools.available(lesson.domain !== "memory"); tools.context({ title: P(lesson.title), detail: lesson.skill_name }); }
      $("ls-player").hidden = false;
      $("ls-progress").setAttribute("aria-valuemax", String(steps.length));
      $("ls-firsttime").hidden = !(firstTime || note);
      if (note || firstTime) $("ls-firsttime").textContent = note || "Everyone starts here. Every other lesson opens when you finish this one.";
      begin();
      $("ls-title").focus();
    }).catch(function (err) {
      if (window.GraphiteLock && GraphiteLock.handle(err)) return;
      if (startFirst(err) && id !== START) { open(START, null, "Start with Desmos hacks. Every other lesson opens after it, including that one."); return; }
      $("ls-list-view").hidden = false;
      failed(err, "We couldn't open that lesson.");
      loadList();
    });
  }
  function fmt() { return kind === "recall" ? "classic" : (lesson.format || "classic"); }
  function begin() {
    at = 0; answers = []; answered = false;
    play = { hearts: 3, noHearts: false, beat: 0, timed: 0, lanes: { hand: [], desmos: [] }, skipped: 0, coldRight: null, rematchRight: null, clock: null, watch: null, started: 0 };
    hud();
    var f = fmt();
    if (kind === "recall" || f === "classic") { renderStep(); return; }
    // How this one works
    $("ls-next").hidden = true;
    progress(true);
    if ($("ls-clock")) $("ls-clock").hidden = true;  // the clock starts with the first step
    var box = $("ls-step"); box.className = "panel ls-step ls-intro ls-f-" + f;
    var extra = "";
    if (f === "lives") extra = '<p class="ls-hearts-demo">' + HEART + HEART + HEART + "</p><p>Run out and you can start over or keep going without them.</p>";
    if (f === "timed") extra = "<p>" + (lesson.seconds || 45) + " seconds a step. Run over and you can still finish it: the clock is just to push you.</p>";
    if (f === "cold-open") extra = "<p>The first question is the hard one, before any teaching. Miss it? Good. You'll get a twin of it at the end.</p>";
    if (f === "path") extra = "<p>Already know this? The first question is a shortcut. Get it right and you skip the warm-up.</p>";
    if (f === "race") extra = "<p>Steps marked <strong>By hand</strong> and <strong>In Desmos</strong> are timed, so you'll see which way is faster for you.</p>";
    if (f === "lab") extra = "<p>Play with the graph or the numbers first. Then put into words what you found.</p>";
    box.innerHTML = '<p class="label">How this one works</p><h2 class="ls-format-name">' + esc(FORMAT[f]) + "</h2>" +
      '<p class="ls-format-rule">' + esc(lesson.format_rule || "") + "</p>" + (lesson.intro ? '<p class="ls-story-intro">' + T(lesson.intro) + "</p>" : "") + extra +
      '<button class="btn btn-primary" type="button" id="ls-go">Start</button>';
    $("ls-go").addEventListener("click", function () { renderStep(); focusStep(); });
  }
  function progress(intro) {
    $("ls-progress").firstElementChild.style.width = Math.round(at / steps.length * 100) + "%";
    $("ls-progress").setAttribute("aria-valuenow", String(at));
    $("ls-step-count").textContent = intro ? steps.length + " steps" : "Step " + (at + 1) + " of " + steps.length + (kind === "recall" ? " · from memory, no notes" : "");
  }
  function hud() {
    var f = fmt(), h = $("ls-hud"), out = "";
    if (f === "lives" && !play.noHearts) {
      out += '<span class="ls-hearts" aria-label="' + play.hearts + ' hearts left">';
      for (var i = 0; i < 3; i++) out += '<span class="' + (i < play.hearts ? "is-full" : "is-lost") + '">' + HEART + "</span>";
      out += "</span>";
    }
    if (f === "timed") out += '<span class="ls-clock" id="ls-clock"><span class="ls-clock-bar"><i id="ls-clock-fill"></i></span><span id="ls-clock-n" aria-live="off"></span></span>';
    if (f === "race") out += '<span class="ls-watch" id="ls-watch" hidden></span>';
    h.innerHTML = out; h.hidden = !out;
  }
  function stopClocks() { if (play.clock) clearInterval(play.clock); if (play.watch) clearInterval(play.watch); play.clock = play.watch = null; }
  function startClocks(s) {
    stopClocks();
    var f = fmt();
    play.started = Date.now();
    if (f === "timed") {
      var total = s.seconds || lesson.seconds || 45;
      $("ls-clock").hidden = false;
      play.timed++;
      var tick = function () {
        var left = Math.max(0, total - (Date.now() - play.started) / 1000);
        var fill = $("ls-clock-fill"), n = $("ls-clock-n"); if (!fill) return;
        fill.style.width = (left / total * 100) + "%";
        n.textContent = left > 0 ? Math.ceil(left) + "s" : "Time's up";
        $("ls-clock").classList.toggle("is-low", left < total * 0.25);
        if (left <= 0) clearInterval(play.clock);
      };
      tick(); play.clock = setInterval(tick, 250);
    }
    if (f === "race" && s.lane) {
      var w = $("ls-watch"); w.hidden = false;
      var t = function () { w.textContent = (s.lane === "hand" ? "By hand " : "In Desmos ") + Math.floor((Date.now() - play.started) / 1000) + "s"; };
      t(); play.watch = setInterval(t, 500);
    } else if (f === "race") $("ls-watch").hidden = true;
  }

  var KICK = { recall: "From memory", predict: "Predict first", fill: "Fill in the step", order: "Put it in order", spot: "Find the mistake",
               slider: "Drag to explore", plot: "Tap the graph", graph: "Type it, see it", sort: "Sort the cards", match: "Match them up",
               line: "Mark the number line", build: "Build it", grid: "Fill in the table", flash: "Quick look" };
  var HANDS_ON = { slider: 1, plot: 1, graph: 1, sort: 1, match: 1, line: 1, build: 1, grid: 1, flash: 1 };
  function kicker(s) {
    var f = fmt(), k = KICK[s.type];
    if (s.cold) return "Cold open · before the lesson";
    if (s.rematch) return "Rematch";
    if (s.gate) return "Shortcut question · get it right to skip the warm-up";
    if (f === "case") return (at === steps.length - 1 ? "Close the case" : "Clue " + (at + 1)) + " · " + k;
    if (f === "teach" && s.type === "spot") return "Check " + (lesson.student || "Sam") + "'s work";
    if (f === "lab") {
      var firstRecall = steps.findIndex(function (x) { return x.type === "recall"; });
      if (HANDS_ON[s.type] && (firstRecall < 0 || at < firstRecall)) return "Experiment · " + k;
      if (at === firstRecall) return "Name the rule";
    }
    return k;
  }
  function table(t) {
    if (!t) return "";
    return '<div class="ls-table-wrap"><table class="ls-table">' + (t.caption ? "<caption>" + T(t.caption) + "</caption>" : "") +
      "<thead><tr>" + t.head.map(function (h) { return '<th scope="col">' + T(h) + "</th>"; }).join("") + "</tr></thead><tbody>" +
      t.rows.map(function (r) { return "<tr>" + r.map(function (c, i) { return i ? "<td>" + T(c) + "</td>" : '<th scope="row">' + T(c) + "</th>"; }).join("") + "</tr>"; }).join("") +
      "</tbody></table></div>";
  }
  // Keystrokes for the Desmos course, with a link to the College Board's own Desmos to try them.
  function desmos(lines) {
    if (!lines || !lines.length) return "";
    return '<div class="ls-desmos"><p class="label">Type in Desmos</p><ol>' + lines.map(function (l) { return "<li><code>" + esc(l) + "</code></li>"; }).join("") + "</ol>" +
      '<a href="https://www.desmos.com/testing/collegeboard/graphing" target="_blank" rel="noopener">Try it in the College Board Desmos<span class="visually-hidden"> (opens in a new tab)</span></a></div>';
  }
  var PRAISE = ["Right.", "Yes.", "Exactly.", "Got it.", "Nice.", "That's it."];
  function feedback(right, why, extra) {
    var s = steps[at], f = fmt();
    stopClocks();
    var notes = "";
    if (f === "timed" && play.started) {
      var used = (Date.now() - play.started) / 1000, limit = s.seconds || lesson.seconds || 45;
      if (used <= limit) { play.beat++; notes += '<span class="chip ls-chip-win">Beat the clock · ' + Math.round(used) + "s</span>"; }
      else notes += '<span class="chip chip-quiet">Over time · ' + Math.round(used) + "s</span>";
    }
    if (f === "race" && s.lane) { var secs = Math.round((Date.now() - play.started) / 1000); play.lanes[s.lane].push(secs); notes += '<span class="chip chip-quiet">' + (s.lane === "hand" ? "By hand: " : "In Desmos: ") + secs + "s</span>"; }
    if (s.cold) play.coldRight = right;
    if (s.rematch) play.rematchRight = right;
    var fb = document.createElement("div");
    fb.className = "ls-fb " + (right ? "ok" : "no"); fb.tabIndex = -1;
    fb.innerHTML = '<strong class="ls-fb-head">' + (right ? PRAISE[at % PRAISE.length] : s.cold ? "Not yet, and that's fine." : "Not quite.") + "</strong>" + (extra ? '<span class="ls-fb-extra">' + extra + "</span>" : "") + (why ? "<span>" + T(why) + "</span>" : "") + (notes ? '<span class="ls-fb-notes">' + notes + "</span>" : "");
    $("ls-step").appendChild(fb);
    if (s.gate && right) {
      var skip = steps.filter(function (x) { return x.skip_if === 0; }).length;
      if (skip) { var n = document.createElement("p"); n.className = "ls-shortcut"; n.textContent = "Shortcut! You skip " + skip + " warm-up step" + (skip === 1 ? "" : "s") + "."; fb.appendChild(n); }
    }
    if (tools && lesson.domain !== "memory") {
      var ask = document.createElement("button"); ask.type = "button"; ask.className = "btn btn-quiet ask-tutor";
      ask.textContent = right ? "Ask the tutor to go deeper" : "Ask the tutor why";
      var step = at + 1;
      ask.addEventListener("click", function () { tools.context({ title: lesson.title, detail: "Step " + step + " of " + steps.length }); tools.open("tutor"); });
      fb.appendChild(ask);
    }
    answers[at] = pending;  // the first try, sent to the server, which does the grading
    answered = true;
    if (f === "lives" && !right && !play.noHearts && !s.cold) {
      play.hearts--; hud();
      if (play.hearts <= 0) { outOfHearts(); return; }
    }
    $("ls-next").hidden = false;
    $("ls-next").textContent = nextIndex() < steps.length ? "Next" : "Finish";
    $("ls-next").focus();
  }
  function outOfHearts() {
    var p = document.createElement("div"); p.className = "ls-out"; p.setAttribute("role", "alert");
    p.innerHTML = '<p class="ls-hearts is-empty">' + HEART + HEART + HEART + '</p><p><strong>Out of hearts.</strong> Start over for a clean run, or keep going without hearts.</p>' +
      '<div class="pd-row"><button class="btn btn-primary" type="button" data-out="restart">Start over</button><button class="btn btn-secondary" type="button" data-out="go">Keep going</button></div>';
    $("ls-step").appendChild(p);
    p.addEventListener("click", function (e) {
      var b = e.target.closest("[data-out]"); if (!b) return;
      if (b.getAttribute("data-out") === "restart") { begin(); if (!$("ls-go")) renderStep(); focusStep(); return; }
      play.noHearts = true; hud(); p.remove();
      $("ls-next").hidden = false; $("ls-next").textContent = nextIndex() < steps.length ? "Next" : "Finish"; $("ls-next").focus();
    });
    p.querySelector("button").focus();
  }
  // After the shortcut question, warm-up steps are passed over when it was right.
  function nextIndex() {
    var i = at + 1;
    var gate = steps[0] && steps[0].gate ? 0 : -1;
    while (i < steps.length && gate === 0 && steps[i].skip_if === 0 && K.right(steps[0], answers[0])) i++;
    return i;
  }

  function renderStep() {
    var s = steps[at], box = $("ls-step");
    answered = false; $("ls-next").hidden = true;
    progress();
    box.className = "panel ls-step is-" + s.type + (s.cold ? " is-cold" : "") + (s.rematch ? " is-rematch" : "") + (s.gate ? " is-gate" : "");
    box.innerHTML = '<p class="label">' + esc(kicker(s)) + (s.lane ? ' <span class="ls-lane ls-lane-' + s.lane + '">' + (s.lane === "hand" ? "By hand" : "In Desmos") + "</span>" : "") + "</p>" +
      (s.scene ? '<p class="ls-scene">' + T(s.scene) + "</p>" : "") +
      table(s.table) + '<p class="ls-prompt">' + T(s.prompt) + "</p>" + desmos(s.desmos);
    STEP[s.type](s, box);
    startClocks(s);
  }
  function focusStep() { var p = $("ls-step").querySelector("input, button, textarea, select"); if (p) p.focus({ preventScroll: true }); }

  /* ---------- the classic steps ---------- */
  function stepRecall(s, box) {
    var area = document.createElement("div"); area.className = "ls-recall";
    area.innerHTML = '<label class="fine" for="ls-recall-text">Type it, or just say it in your head:</label><textarea id="ls-recall-text" rows="3"></textarea>' +
      '<button class="btn btn-secondary" type="button">Show the answer</button>';
    box.appendChild(area);
    area.querySelector("button").addEventListener("click", function () {
      this.remove();
      var rev = document.createElement("div"); rev.className = "ls-reveal";
      rev.innerHTML = '<p class="label">Answer</p><p class="ls-answer">' + T(s.answer) + '</p><p class="fine">How did you do?</p>' +
        '<div class="ls-rate"><button class="btn btn-quiet" type="button" data-r="1">Got it</button><button class="btn btn-quiet" type="button" data-r="0">Partly</button><button class="btn btn-quiet" type="button" data-r="0">Not yet</button></div>';
      box.appendChild(rev);
      rev.querySelector(".ls-rate").addEventListener("click", function (e) {
        var b = e.target.closest("button"); if (!b || answered) return;
        each(this.querySelectorAll("button"), function (x) { x.disabled = true; x.classList.toggle("is-picked", x === b); });
        pending = b.getAttribute("data-r") === "1";
        feedback(pending, pending ? "" : "That's what the rest of this lesson is for.");
      });
      rev.querySelector(".ls-rate button").focus();
    });
  }
  function choices(s, box) {
    var list = document.createElement("div"); list.className = "ls-choices"; list.setAttribute("role", "group"); list.setAttribute("aria-label", "Choices");
    s.choices.forEach(function (c, k) {
      var b = document.createElement("button"); b.type = "button"; b.className = "sp-choice";
      b.innerHTML = '<span class="mc-letter">' + "ABCD"[k] + '</span><span class="mc-text">' + T(c) + "</span>";
      b.addEventListener("click", function () {
        if (answered) return;
        each(list.children, function (x, i) { x.disabled = true; if (i === s.answer) x.classList.add("is-key"); });
        if (k !== s.answer) b.classList.add("is-wrong");
        pending = k;
        feedback(k === s.answer, s.why);
      });
      list.appendChild(b);
    });
    box.appendChild(list);
  }
  function stepFill(s, box) {
    var work = document.createElement("form"); work.className = "ls-work"; work.setAttribute("novalidate", "");
    work.innerHTML = s.lines.map(function (line) {
      if (line.indexOf("___") < 0) return '<p class="ls-line">' + T(line) + "</p>";
      var parts = line.split("___");
      return '<p class="ls-line">' + T(parts[0]) + '<label class="visually-hidden" for="ls-blank">Missing value</label><input id="ls-blank" class="ls-blank" data-no-filter autocomplete="off" inputmode="decimal" spellcheck="false" maxlength="12">' + T(parts[1] || "") + "</p>";
    }).join("") + '<button class="btn btn-secondary" type="submit">Check</button>';
    box.appendChild(work);
    var input = work.querySelector("input");
    if (s.accept.some(function (x) { return /[^\d.\-\u2212]/.test(x); })) input.setAttribute("inputmode", "text");  // fractions and letters need the full keyboard
    work.addEventListener("submit", function (e) {
      e.preventDefault();
      if (answered || !input.value.trim()) { input.focus(); return; }
      pending = input.value.trim();
      var right = K.right(s, pending);
      input.readOnly = true; input.classList.add(right ? "is-right" : "is-wrong");
      work.querySelector("button").remove();
      feedback(right, s.why, right ? "" : "It's <strong>" + K.answer(s.accept[0]) + "</strong>. ");
    });
  }
  function stepOrder(s, box) {
    var placed = [], pool = mixed(s.items.length);
    var wrap = document.createElement("div"); wrap.className = "ls-order";
    wrap.innerHTML = '<div><p class="fine">Tap the steps in order.</p><ol class="ls-pool" id="ls-pool"></ol></div><div><p class="fine">Your order (tap one to take it back):</p><ol class="ls-placed" id="ls-placed"></ol></div>' +
      '<button class="btn btn-secondary" type="button" id="ls-order-check" disabled>Check</button>';
    box.appendChild(wrap);
    function draw() {
      $("ls-pool").innerHTML = pool.map(function (i) { return '<li><button type="button" class="ls-tile" data-i="' + i + '">' + T(s.items[i]) + "</button></li>"; }).join("");
      $("ls-placed").innerHTML = placed.map(function (i, n) { return '<li><button type="button" class="ls-tile is-placed" data-i="' + i + '"><span class="ls-n">' + (n + 1) + "</span>" + T(s.items[i]) + "</button></li>"; }).join("");
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
      pending = placed.slice();
      var right = K.right(s, pending);
      this.remove();
      each($("ls-placed").querySelectorAll(".ls-tile"), function (b, n) { b.disabled = true; b.classList.add(placed[n] === n ? "is-right" : "is-wrong"); });
      var correct = right ? "" : "<ol class=\"ls-correct\">" + s.items.map(function (t) { return "<li>" + T(t) + "</li>"; }).join("") + "</ol>";
      feedback(right, s.why, right ? "" : "Here's the order:" + correct);
    });
    draw();
  }
  function stepSpot(s, box) {
    var list = document.createElement("ol"); list.className = "ls-lines";
    s.lines.forEach(function (line, k) {
      var li = document.createElement("li"), b = document.createElement("button");
      b.type = "button"; b.className = "ls-tile"; b.innerHTML = T(line);
      b.addEventListener("click", function () {
        if (answered) return;
        each(list.querySelectorAll("button"), function (x, i) { x.disabled = true; if (i === s.wrong) x.classList.add("is-key-wrong"); });
        if (k !== s.wrong) b.classList.add("is-picked");
        pending = k;
        feedback(k === s.wrong, s.why, k === s.wrong ? "" : "The mistake is in line " + (s.wrong + 1) + ". ");
      });
      li.appendChild(b); list.appendChild(li);
    });
    box.appendChild(list);
  }

  /* ---------- hands-on steps ---------- */
  function checkButton(label) { var b = document.createElement("button"); b.type = "button"; b.className = "btn btn-secondary ls-check"; b.textContent = label || "Check"; return b; }
  function snapOf(s) { var sn = s.snap == null ? 1 : s.snap; return Array.isArray(sn) ? sn : [sn, sn]; }
  function round(v, step) { return Math.round(Math.round(v / step) * step * 1e6) / 1e6; }

  // Drag a constant and watch a graph, a dot plot or a circle respond.
  function stepSlider(s, box) {
    var p = s.param, name = p.name, v = p.start, env = {};
    var fns = (s.curves || []).map(function (c) { return K.compile(c, (env[name] = 0, env)); });
    var fixed = (s.fixed || []).map(function (c) { return K.compile(c); });
    var graph = s.curves ? K.Graph(s.window) : null;
    var wrap = document.createElement("div"); wrap.className = "lk-wrap";
    wrap.innerHTML = '<div class="lk-visual" id="lk-visual"></div><div class="lk-controls">' +
      '<label class="lk-range-label" for="lk-range"><span class="lk-name">' + esc(name) + '</span> = <output id="lk-out" for="lk-range"></output></label>' +
      '<div class="lk-range-row"><button type="button" class="lk-nudge" data-d="-1" aria-label="Decrease ' + esc(name) + '">−</button>' +
      '<input type="range" id="lk-range" min="' + p.min + '" max="' + p.max + '" step="' + p.step + '" value="' + p.start + '">' +
      '<button type="button" class="lk-nudge" data-d="1" aria-label="Increase ' + esc(name) + '">+</button></div>' +
      '<p class="lk-readout" id="lk-readout" aria-live="polite"></p></div>';
    box.appendChild(wrap);
    var chk = checkButton(); box.appendChild(chk);
    function readout(val) {
      if (!s.readout) return "";
      return s.readout.replace(/\{=([^}]+)\}/g, function (_, ex) { var o = {}; o[name] = val; var r = K.value(ex, 0, o); return r === null ? "?" : String(Math.round(r * 100) / 100); })
                      .replace(new RegExp("\\{" + name + "\\}", "g"), val < 0 ? "(" + val + ")" : String(val));
    }
    function draw(val, state) {
      var e = {}; e[name] = val;
      if (graph) {
        $("lk-visual").innerHTML = graph.svg({ label: "Graph with " + name + " = " + val,
          curves: fixed.map(function (f) { return { f: f, cls: "lk-fixed" }; }).concat(fns.map(function (f, i) { return { f: function (x) { return f(x, e); }, cls: "lk-c" + i + (state ? " " + state : "") }; })),
          rings: s.points || [] });
      } else if (s.dots) {
        var vals = s.dots.values.map(function (x) { return K.value(x, 0, e); });
        $("lk-visual").innerHTML = K.dotPlot(vals, s.dots.min, s.dots.max, K.value(s.dots.mark, 0, e), "Mean");
      } else if (s.pie) {
        $("lk-visual").innerHTML = K.pie(K.value(s.pie.angle, 0, e), "Sector of " + val + " degrees");
      }
      $("lk-out").textContent = K.fmt(val);
      $("lk-readout").innerHTML = T(readout(val));
    }
    var range = $("lk-range");
    range.addEventListener("input", function () { if (answered) return; v = Number(this.value); draw(v); });
    wrap.addEventListener("click", function (e) {
      var b = e.target.closest(".lk-nudge"); if (!b || answered) return;
      v = Math.min(p.max, Math.max(p.min, round(v + Number(b.getAttribute("data-d")) * p.step, p.step))); range.value = v; draw(v);
    });
    chk.addEventListener("click", function () {
      if (answered) return;
      pending = round(v, p.step);
      var right = K.right(s, pending);
      chk.remove(); range.disabled = true; each(wrap.querySelectorAll(".lk-nudge"), function (b) { b.disabled = true; });
      if (!right) { v = s.answer; range.value = v; draw(v, "is-answer"); }
      feedback(right, s.why, right ? "" : "It's " + esc(name) + " = <strong>" + K.fmt(s.answer) + "</strong>. The graph shows it now. ");
    });
    draw(v);
  }

  // Tap a point on a graph (or type its coordinates).
  function stepPlot(s, box) {
    var g = K.Graph(s.window), sn = snapOf(s), pick = null;
    var curves = s.curves.map(function (c, i) { var f = K.compile(c); return { f: f, cls: "lk-c" + (i % 3) }; });
    var wrap = document.createElement("div"); wrap.className = "lk-wrap";
    wrap.innerHTML = '<div class="lk-visual lk-tap" id="lk-visual"></div><div class="lk-controls lk-xy"><p class="fine">Tap the graph, or type the point:</p>' +
      '<label>x <input type="number" id="lk-x" step="' + sn[0] + '" inputmode="decimal"></label><label>y <input type="number" id="lk-y" step="' + sn[1] + '" inputmode="decimal"></label></div>';
    box.appendChild(wrap);
    var chk = checkButton(); chk.disabled = true; box.appendChild(chk);
    function draw(extra) { $("lk-visual").innerHTML = g.svg({ curves: curves, dots: s.points || [], mark: pick, label: "Graph. " + (pick ? "Your point is (" + pick[0] + ", " + pick[1] + ")." : "No point yet."), markCls: extra && extra.cls }) + (extra && extra.svg || ""); }
    function set(x, y) { pick = [round(x, sn[0]), round(y, sn[1])]; $("lk-x").value = pick[0]; $("lk-y").value = pick[1]; chk.disabled = false; draw(); }
    $("lk-visual").addEventListener("click", function (e) {
      if (answered) return;
      var svg = this.querySelector("svg"), r = svg.getBoundingClientRect();
      var pt = g.fromPx((e.clientX - r.left) * 480 / r.width, (e.clientY - r.top) * 340 / r.height);
      set(pt[0], pt[1]);
    });
    function typed() { var x = parseFloat($("lk-x").value), y = parseFloat($("lk-y").value); if (isFinite(x) && isFinite(y)) set(x, y); }
    $("lk-x").addEventListener("change", typed); $("lk-y").addEventListener("change", typed);
    chk.addEventListener("click", function () {
      if (answered || !pick) return;
      pending = pick.slice();
      var right = K.right(s, pending);
      chk.remove(); $("lk-x").disabled = $("lk-y").disabled = true;
      var ans = s.answer;
      $("lk-visual").innerHTML = g.svg({ curves: curves, dots: s.points || [], mark: right ? pick : ans, markCls: "is-answer", rings: right ? [] : [pick], label: "The answer is (" + ans[0] + ", " + ans[1] + ")." });
      feedback(right, s.why, right ? "" : "The point is <strong>(" + K.fmt(ans[0]) + ", " + K.fmt(ans[1]) + ")</strong>. ");
    });
    draw();
  }

  // Type an equation; it's drawn as you type, the way Desmos does.
  function stepGraph(s, box) {
    var g = K.Graph(s.window), fixed = (s.fixed || []).map(function (c) { return K.compile(c); }), mine = null;
    var wrap = document.createElement("div"); wrap.className = "lk-wrap";
    wrap.innerHTML = '<div class="lk-visual" id="lk-visual"></div><div class="lk-controls"><label class="lk-type" for="lk-expr"><span>y =</span>' +
      '<input id="lk-expr" type="text" autocomplete="off" autocapitalize="off" spellcheck="false" data-no-filter maxlength="' + K.MAX_LEN + '" placeholder="like 2x + 1 or x^2 - 4"></label>' +
      '<p class="fine lk-hint" id="lk-hint" aria-live="polite">Use ^ for powers, like x^2.' + (s.forbid ? " No brackets this time." : "") + "</p></div>";
    box.appendChild(wrap);
    var chk = checkButton(); chk.disabled = true; box.appendChild(chk);
    function draw(extra) {
      var cs = fixed.map(function (f) { return { f: f, cls: "lk-fixed" }; });
      if (mine) cs.push({ f: mine, cls: "lk-c0" });
      if (extra) cs.push(extra);
      $("lk-visual").innerHTML = g.svg({ curves: cs, dots: s.points || [], label: mine ? "Your graph" : "Graph" });
    }
    $("lk-expr").addEventListener("input", function () {
      if (answered) return;
      var t = this.value.trim(), msg = t ? K.check(t) : "";
      mine = null;
      if (t && !msg) { try { mine = K.compile(t); } catch (e) { mine = null; } }
      $("lk-hint").textContent = msg || (t ? "Drawn." : "Use ^ for powers, like x^2.");
      chk.disabled = !mine;
      draw();
    });
    $("lk-expr").addEventListener("keydown", function (e) { if (e.key === "Enter" && !chk.disabled) { e.preventDefault(); chk.click(); } });
    chk.addEventListener("click", function () {
      if (answered) return;
      pending = $("lk-expr").value.trim();
      var right = K.right(s, pending);
      chk.remove(); $("lk-expr").readOnly = true;
      if (!right) draw({ f: K.compile(s.accept[0]), cls: "lk-c1 is-answer" });
      feedback(right, s.why, right ? "" : "One answer: <strong>" + K.answer("y=" + s.accept[0]) + "</strong>" + (s.forbid && (s.forbid.some(function (f) { return pending.indexOf(f) >= 0; })) ? ", written without brackets" : "") + ". ");
    });
    draw();
  }

  // Put each card in a bucket.
  function stepSort(s, box) {
    var order = mixed(s.cards.length), picks = s.cards.map(function () { return null; });
    var list = document.createElement("ul"); list.className = "lk-sort";
    list.innerHTML = order.map(function (ci) {
      return '<li class="lk-card" data-c="' + ci + '"><span class="lk-card-text" id="lk-card-' + ci + '">' + T(s.cards[ci].text) + '</span><span class="lk-buckets" role="group" aria-labelledby="lk-card-' + ci + '">' +
        s.buckets.map(function (b, bi) { return '<button type="button" class="lk-bucket" data-b="' + bi + '" aria-pressed="false">' + T(b) + "</button>"; }).join("") + "</span></li>";
    }).join("");
    box.appendChild(list);
    var chk = checkButton(); chk.disabled = true; box.appendChild(chk);
    list.addEventListener("click", function (e) {
      var b = e.target.closest(".lk-bucket"); if (!b || answered) return;
      var card = b.closest(".lk-card"), ci = Number(card.getAttribute("data-c"));
      picks[ci] = Number(b.getAttribute("data-b"));
      each(card.querySelectorAll(".lk-bucket"), function (x) { x.setAttribute("aria-pressed", String(x === b)); });
      card.classList.add("is-set");
      chk.disabled = picks.some(function (x) { return x === null; });
    });
    chk.addEventListener("click", function () {
      if (answered) return;
      pending = picks.slice();
      var right = K.right(s, pending), wrong = 0;
      chk.remove();
      each(list.querySelectorAll(".lk-card"), function (card) {
        var ci = Number(card.getAttribute("data-c")), ok = picks[ci] === s.cards[ci].bucket;
        if (!ok) wrong++;
        card.classList.add(ok ? "is-right" : "is-wrong");
        each(card.querySelectorAll(".lk-bucket"), function (x) { x.disabled = true; if (Number(x.getAttribute("data-b")) === s.cards[ci].bucket) x.classList.add("is-key"); });
      });
      feedback(right, s.why, right ? "" : wrong + " of " + s.cards.length + " in the wrong group. The right group is outlined. ");
    });
  }

  // Pair each item on the left with one on the right.
  function stepMatch(s, box) {
    var n = s.left.length, rightOrder = mixed(n), pairOf = s.left.map(function () { return null; }), active = null;
    var wrap = document.createElement("div"); wrap.className = "lk-match";
    wrap.innerHTML = '<p class="fine">Tap one on the left, then its partner on the right. Tap a pair again to undo it.</p><div class="lk-match-cols"><ul class="lk-left">' +
      s.left.map(function (t, i) { return '<li><button type="button" class="lk-m" data-l="' + i + '" aria-pressed="false"><span class="lk-pair-n" aria-hidden="true"></span>' + T(t) + "</button></li>"; }).join("") +
      '</ul><ul class="lk-right">' + rightOrder.map(function (ri) { return '<li><button type="button" class="lk-m" data-r="' + ri + '"><span class="lk-pair-n" aria-hidden="true"></span>' + T(s.right[ri]) + "</button></li>"; }).join("") + "</ul></div>";
    box.appendChild(wrap);
    var chk = checkButton(); chk.disabled = true; box.appendChild(chk);
    function draw() {
      each(wrap.querySelectorAll("[data-l]"), function (b) {
        var i = Number(b.getAttribute("data-l")), p = pairOf[i];
        b.setAttribute("aria-pressed", String(active === i)); b.classList.toggle("is-active", active === i);
        b.className = b.className.replace(/\blk-p\d\b/g, "").trim(); if (p !== null) b.classList.add("lk-p" + (i % 6));
        b.querySelector(".lk-pair-n").textContent = p !== null ? String(i + 1) : "";
        b.setAttribute("aria-label", b.textContent.replace(/^\d/, "") + (p !== null ? ", paired with " + s.right[p] : ""));
      });
      each(wrap.querySelectorAll("[data-r]"), function (b) {
        var ri = Number(b.getAttribute("data-r")), li = pairOf.indexOf(ri);
        b.className = b.className.replace(/\blk-p\d\b/g, "").trim(); if (li >= 0) b.classList.add("lk-p" + (li % 6));
        b.querySelector(".lk-pair-n").textContent = li >= 0 ? String(li + 1) : "";
      });
      chk.disabled = pairOf.some(function (p) { return p === null; });
    }
    wrap.addEventListener("click", function (e) {
      var b = e.target.closest(".lk-m"); if (!b || answered) return;
      if (b.hasAttribute("data-l")) {
        var i = Number(b.getAttribute("data-l"));
        if (pairOf[i] !== null) pairOf[i] = null;
        active = i;
      } else {
        var ri = Number(b.getAttribute("data-r")), had = pairOf.indexOf(ri);
        if (had >= 0) { pairOf[had] = null; if (active === null) { draw(); return; } }
        if (active === null) { var free = pairOf.indexOf(null); if (free < 0) return; active = free; }
        pairOf[active] = ri; active = null;
        var nextFree = pairOf.indexOf(null); if (nextFree >= 0) active = nextFree;
      }
      draw();
    });
    chk.addEventListener("click", function () {
      if (answered) return;
      pending = pairOf.slice();
      var right = K.right(s, pending);
      chk.remove(); active = null; draw();
      each(wrap.querySelectorAll("[data-l]"), function (b) { var i = Number(b.getAttribute("data-l")); b.disabled = true; b.classList.add(pairOf[i] === i ? "is-right" : "is-wrong"); });
      each(wrap.querySelectorAll("[data-r]"), function (b) { b.disabled = true; });
      var fix = right ? "" : '<ul class="ls-correct">' + s.left.map(function (l, i) { return "<li>" + T(l) + " → " + T(s.right[i]) + "</li>"; }).join("") + "</ul>";
      feedback(right, s.why, right ? "" : "The pairs:" + fix);
    });
    active = 0; draw();
  }

  // Mark an inequality on a number line.
  function stepLine(s, box) {
    var nl = K.NumberLine(s.min, s.max), st = { at: null, closed: null, dir: null };
    var wrap = document.createElement("div"); wrap.className = "lk-wrap lk-nl";
    wrap.innerHTML = '<div class="lk-visual lk-tap" id="lk-visual"></div><div class="lk-controls lk-nl-controls">' +
      '<label>Endpoint <input type="number" id="lk-at" step="1" min="' + s.min + '" max="' + s.max + '" inputmode="numeric"></label>' +
      '<div class="seg" role="radiogroup" aria-label="Endpoint"><span><input type="radio" name="lk-c" id="lk-open" value="open"><label for="lk-open">Open circle</label></span><span><input type="radio" name="lk-c" id="lk-closed" value="closed"><label for="lk-closed">Closed dot</label></span></div>' +
      '<div class="seg" role="radiogroup" aria-label="Direction"><span><input type="radio" name="lk-d" id="lk-left" value="left"><label for="lk-left">← Left</label></span><span><input type="radio" name="lk-d" id="lk-right" value="right"><label for="lk-right">Right →</label></span></div></div>';
    box.appendChild(wrap);
    var chk = checkButton(); chk.disabled = true; box.appendChild(chk);
    function draw() { $("lk-visual").innerHTML = nl.svg(st, "Number line" + (st.at !== null ? ", endpoint " + st.at : "")); chk.disabled = st.at === null || st.closed === null || !st.dir; }
    $("lk-visual").addEventListener("click", function (e) {
      if (answered) return;
      var r = this.querySelector("svg").getBoundingClientRect();
      st.at = Math.max(s.min, Math.min(s.max, Math.round(nl.fromPx((e.clientX - r.left) * 480 / r.width))));
      $("lk-at").value = st.at; draw();
    });
    $("lk-at").addEventListener("input", function () { var v = parseFloat(this.value); if (isFinite(v)) { st.at = Math.max(s.min, Math.min(s.max, v)); draw(); } });
    wrap.addEventListener("change", function (e) {
      if (e.target.name === "lk-c") st.closed = e.target.value === "closed";
      if (e.target.name === "lk-d") st.dir = e.target.value;
      draw();
    });
    chk.addEventListener("click", function () {
      if (answered) return;
      pending = { at: st.at, closed: st.closed, dir: st.dir };
      var right = K.right(s, pending);
      chk.remove(); each(wrap.querySelectorAll("input"), function (x) { x.disabled = true; });
      if (!right) $("lk-visual").innerHTML = nl.svg(st) + '<p class="fine lk-key-label">The answer:</p>' + nl.svg(s.answer, "The answer");
      var a = s.answer;
      feedback(right, s.why, right ? "" : "It's " + (a.closed ? "a closed dot" : "an open circle") + " at <strong>" + K.fmt(a.at) + "</strong>, pointing " + a.dir + ". ");
    });
    draw();
  }

  // Tap tiles to build an equation or a chain.
  function stepBuild(s, box) {
    var pool = mixed(s.tiles.length), placed = [];
    var wrap = document.createElement("div"); wrap.className = "lk-build";
    wrap.innerHTML = '<p class="fine">Tap tiles to build it. Tap a placed tile to take it back.</p><div class="lk-bar" id="lk-bar" aria-live="polite"></div><div class="lk-tiles" id="lk-tiles"></div>';
    box.appendChild(wrap);
    var chk = checkButton(); chk.disabled = true; box.appendChild(chk);
    function draw() {
      $("lk-bar").innerHTML = placed.length ? placed.map(function (i) { return '<button type="button" class="lk-tile is-placed" data-i="' + i + '">' + T(s.tiles[i]) + "</button>"; }).join("") : '<span class="fine">Your answer goes here</span>';
      $("lk-tiles").innerHTML = pool.map(function (i) { return '<button type="button" class="lk-tile" data-i="' + i + '">' + T(s.tiles[i]) + "</button>"; }).join("");
      chk.disabled = !placed.length;
    }
    wrap.addEventListener("click", function (e) {
      var b = e.target.closest(".lk-tile"); if (!b || answered) return;
      var i = Number(b.getAttribute("data-i"));
      if (b.classList.contains("is-placed")) { placed.splice(placed.indexOf(i), 1); pool.push(i); } else { pool.splice(pool.indexOf(i), 1); placed.push(i); }
      draw();
      var next = $("lk-tiles").querySelector("button") || chk; if (next && !next.disabled) next.focus();
    });
    chk.addEventListener("click", function () {
      if (answered) return;
      pending = placed.slice();
      var right = K.right(s, pending);
      chk.remove(); $("lk-bar").classList.add(right ? "is-right" : "is-wrong");
      each(wrap.querySelectorAll(".lk-tile"), function (b) { b.disabled = true; });
      feedback(right, s.why, right ? "" : "It's <strong>" + s.answers[0].map(function (i) { return T(s.tiles[i]); }).join(" ") + "</strong>. ");
    });
    draw();
  }

  // Fill in the blanks of a table.
  function stepGrid(s, box) {
    var n = 0;
    var wrap = document.createElement("form"); wrap.className = "lk-grid"; wrap.setAttribute("novalidate", "");
    wrap.innerHTML = '<div class="ls-table-wrap"><table class="ls-table"><thead><tr>' + s.head.map(function (h) { return '<th scope="col">' + T(h) + "</th>"; }).join("") + "</tr></thead><tbody>" +
      s.rows.map(function (r) {
        return "<tr>" + r.map(function (c, ci) {
          var cell = c.indexOf("___") < 0 ? T(c) : c.split("___").map(T).join('<input class="ls-blank lk-cell" data-k="' + (n++) + '" aria-label="' + esc(P(s.head[ci]) + ", " + P(r[0])) + '" data-no-filter autocomplete="off" spellcheck="false" maxlength="10">');
          return ci ? "<td>" + cell + "</td>" : '<th scope="row">' + cell + "</th>";
        }).join("") + "</tr>";
      }).join("") + "</tbody></table></div>";
    box.appendChild(wrap);
    var chk = checkButton(); chk.disabled = true; chk.type = "submit"; wrap.appendChild(chk);
    var cells = wrap.querySelectorAll(".lk-cell");
    wrap.addEventListener("input", function () { chk.disabled = Array.prototype.some.call(cells, function (c) { return !c.value.trim(); }); });
    wrap.addEventListener("submit", function (e) {
      e.preventDefault();
      if (answered || chk.disabled) return;
      pending = Array.prototype.map.call(cells, function (c) { return c.value.trim(); });
      var right = K.right(s, pending);
      chk.remove();
      each(cells, function (c, i) { c.readOnly = true; var ok = K.right({ type: "fill", accept: s.accept[i] }, pending[i]); c.classList.add(ok ? "is-right" : "is-wrong"); if (!ok) c.title = "It's " + s.accept[i][0]; });
      var fix = right ? "" : "The blanks are " + s.accept.map(function (a) { return "<strong>" + K.answer(a[0]) + "</strong>"; }).join(", ") + ". ";
      feedback(right, s.why, fix);
    });
  }

  // A list shows for a few seconds, hides, then you're asked about it.
  function stepFlash(s, box) {
    var prompt = box.querySelector(".ls-prompt"); prompt.textContent = "Look closely. This disappears in " + s.seconds + " seconds.";
    var card = document.createElement("div"); card.className = "lk-flash";
    card.innerHTML = '<div class="lk-flash-bar"><i id="lk-flash-fill"></i></div><ul>' + s.show.map(function (t) { return "<li>" + T(t) + "</li>"; }).join("") + "</ul>" +
      '<button type="button" class="btn btn-quiet" id="lk-ready">I\'m ready</button>';
    box.appendChild(card);
    var t0 = Date.now(), timer = setInterval(tick, 100);
    function tick() { var left = Math.max(0, 1 - (Date.now() - t0) / (s.seconds * 1000)); var f = $("lk-flash-fill"); if (f) f.style.width = left * 100 + "%"; if (left <= 0) hide(); }
    function hide() {
      clearInterval(timer); if (!card.parentNode) return;
      card.remove(); prompt.innerHTML = T(s.prompt);
      choices(s, box); var b = box.querySelector(".sp-choice"); if (b) b.focus();
    }
    $("lk-ready").addEventListener("click", hide);
  }

  var STEP = { recall: stepRecall, predict: choices, fill: stepFill, order: stepOrder, spot: stepSpot, slider: stepSlider, plot: stepPlot, graph: stepGraph,
               sort: stepSort, match: stepMatch, line: stepLine, build: stepBuild, grid: stepGrid, flash: stepFlash };

  $("ls-next").addEventListener("click", function () {
    if (!answered) return;
    var to = nextIndex();
    for (var i = at + 1; i < to; i++) { answers[i] = "skip"; play.skipped++; }
    at = to;
    if (at < steps.length) { renderStep(); focusStep(); $("ls-step").scrollIntoView({ block: "nearest" }); return; }
    finishLesson();
  });
  function formatLine() {
    var f = fmt(), out = [];
    if (f === "cold-open" && play.coldRight !== null) out.push("Cold open: " + (play.coldRight ? "right" : "missed") + ". Rematch: " + (play.rematchRight ? "right." : "missed, so it's worth another look."));
    if (f === "timed" && play.timed) out.push("You beat the clock on " + play.beat + " of " + play.timed + " steps.");
    if (f === "lives") out.push(play.noHearts ? "You ran out of hearts and kept going. That counts." : play.hearts + " of 3 hearts left.");
    if (f === "path" && play.skipped) out.push("You took the shortcut and skipped " + play.skipped + " warm-up step" + (play.skipped === 1 ? "." : "s."));
    if (f === "race") {
      var avg = function (a) { return a.length ? Math.round(a.reduce(function (x, y) { return x + y; }, 0) / a.length) : null; };
      var h = avg(play.lanes.hand), d = avg(play.lanes.desmos);
      if (h !== null && d !== null) out.push("By hand: about " + h + "s a step. In Desmos: about " + d + "s. " + (h < d ? "By hand was faster for you here." : h > d ? "Desmos was faster for you here." : "A tie."));
    }
    if (f === "case") out.push("Case closed.");
    return out.join(" ");
  }
  function finishLesson() {
    stopClocks();
    var b = $("ls-next"); b.disabled = true; b.textContent = "Saving…";
    call("/api/lessons/" + encodeURIComponent(lesson.id) + "/complete", { kind: kind, answers: answers }).then(function (r) {
      b.disabled = false;
      $("ls-player").hidden = true; $("ls-end").hidden = false;
      $("ls-end-kicker").textContent = kind === "recall" ? "Recall check finished" : "Lesson finished";
      $("ls-end-title").textContent = kind === "recall" ? (r.passed ? "It stuck." : "Almost there.") : r.score === steps.length ? "Every step right the first time." : "Lesson done.";
      $("ls-end-score").textContent = r.score + " of " + steps.length + " right the first time." +
        (kind === "recall" && !r.passed ? " This one comes back tomorrow for another try." : "");
      var fl = formatLine(); $("ls-end-format").textContent = fl; $("ls-end-format").hidden = !fl;
      $("ls-unlocked").hidden = !(lesson.id === START && firstTime);
      $("ls-unlocked-text").textContent = allLessons ? "Every lesson is open now." : "Your starter lessons are open now.";
      $("ls-keys").innerHTML = lesson.keys.map(function (k) { return "<li>" + T(k) + "</li>"; }).join("");
      var p = r.progress;
      $("ls-next-recall").innerHTML = p.mastered ? "<strong>Mastered.</strong> You've passed every recall check for this lesson."
        : p.due_on ? "Recall check <strong>" + (p.due_on === new Date().toISOString().slice(0, 10) ? "today" : day(p.due_on)) + "</strong>: three questions from memory, " + (p.stage + 1) + " of " + lesson.recall_days.length + "." : "";
      var pr = lesson.practice;
      $("ls-practice").hidden = !pr;
      if (pr) { $("ls-practice").setAttribute("data-domain", pr.domain); $("ls-practice").setAttribute("data-skill", pr.skill); }
      if (r.xp || r.coins || (r.badges && r.badges.length)) R.show(r);
      $("ls-end-title").focus();
    }).catch(function (err) { b.disabled = false; b.textContent = "Finish"; if (window.GraphiteLock && GraphiteLock.handle(err)) return; failed(err, "We couldn't save your lesson. Check your connection and press Finish again."); });
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

  function loadList(auto) {
    return call("/api/lessons").then(function (o) {
      if (auto && o.start_with && subject() !== "rw") { open(o.start_with); return; }  // first visit to Math lessons: Desmos hacks, straight away
      renderList(o);
    }).catch(function (err) {
      if (err && err.status === 401) { signIn(); return; }
      $("ls-loading").textContent = err && err.status === 403 ? "Lessons are for student accounts." : "We couldn't load lessons. Check your connection and refresh the page.";
    });
  }
  if (params.get("lesson")) open(params.get("lesson"), params.get("mode")); else loadList(!params.get("list"));
})();
