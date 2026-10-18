/* Graphite SAT practice, preview mode only.
   The live site sends these requests to the backend (backend/app/routes/practice.py). In the static preview there
   is no server, so this file answers the same requests in the browser from GRAPHITE_BANK (bank.js, built from the
   backend's question bank) and keeps the done list in localStorage. The rules match services/practice.py. */
(function () {
  "use strict";
  var BANK = window.GRAPHITE_BANK;
  if (!BANK) return;
  var KEY = "graphite_practice_v1", LETTERS = "ABCD";
  var byId = {};
  BANK.items.forEach(function (q) { byId[q.id] = q; });

  function load() {
    var s = null;
    try { s = JSON.parse(localStorage.getItem(KEY)); } catch (e) { /* storage blocked */ }
    if (s && s.sessions) { s.completed = s.completed || {}; return s; }
    return { seen: {}, sessions: {}, completed: {}, nextId: 1 };
  }
  function save(s) { try { localStorage.setItem(KEY, JSON.stringify(s)); } catch (e) { /* storage blocked */ } }
  function fail(status, message) { var e = new Error(message); e.status = status; return Promise.reject(e); }
  function now() { return new Date().toISOString().replace(/\.\d+Z$/, "Z"); }
  function shuffle(a) { for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }

  function pool(domain, skill) {
    return BANK.items.filter(function (q) { return (!domain || q.domain_key === domain) && (!skill || q.skill_key === skill); })
      .map(function (q) { return q.id; });
  }
  // Up to n questions not yet done. Fewer left than n: just those (fill tops a practice test up with done ones).
  // Once every question in the pool is done, its list starts again.
  function draw(st, ids, n, fill) {
    var unseen = shuffle(ids.filter(function (id) { return !st.seen[id]; }));
    if (!unseen.length) {
      topicsOf(ids).forEach(function (t) { delete st.completed[t]; });
      ids.forEach(function (id) { delete st.seen[id]; });
      unseen = shuffle(ids.slice());
    }
    if (unseen.length >= n || !fill) return unseen.slice(0, n);
    var done = shuffle(ids.filter(function (id) { return unseen.indexOf(id) < 0; }));
    return unseen.concat(done.slice(0, n - unseen.length));
  }
  function topicsOf(ids) {
    var keys = {};
    ids.forEach(function (id) { var q = byId[id]; keys["skill:" + q.domain_key + "/" + q.skill_key] = 1; keys["domain:" + q.domain_key] = 1; });
    return Object.keys(keys).sort(function (a, b) { return (a.indexOf("skill:") ? 1 : 0) - (b.indexOf("skill:") ? 1 : 0) || (a < b ? -1 : 1); });
  }
  function topicTitle(domain, skill) {
    for (var i = 0; i < BANK.topics.length; i++) {
      var d = BANK.topics[i];
      if (d.key !== domain) continue;
      if (!skill) return d.name;
      for (var k = 0; k < d.skills.length; k++) if (d.skills[k].key === skill) return d.skills[k].name;
    }
    return null;
  }

  /* ---------- grading (same rules as services/bank.py) ---------- */
  function parseEntry(raw) {
    var t = String(raw == null ? "" : raw).replace(/\s+/g, "");
    if (!/^-?(\d+\.?\d*|\.\d+|\d+\/\d+)$/.test(t)) return null;
    var neg = t[0] === "-", body = t.replace("-", "");
    if (body.indexOf("/") > -1) {
      var p = body.split("/"); if (Number(p[1]) === 0) return null;
      return { n: (neg ? -1 : 1) * Number(p[0]), d: Number(p[1]) };
    }
    var parts = body.split("."), places = parts[1] ? parts[1].length : 0;
    return { n: (neg ? -1 : 1) * Number((parts[0] || "0") + (parts[1] || "")), d: Math.pow(10, places) };
  }
  function sprMatches(raw, key) {
    var t = String(raw == null ? "" : raw).replace(/\s+/g, ""), v = parseEntry(t);
    var kn = key[0], kd = key[1];
    if (!v) return false;
    if (v.n * kd === kn * v.d) return true;
    if (t.indexOf("/") > -1 || t.indexOf(".") < 0) return false;
    if (t.length < (t[0] === "-" ? 6 : 5)) return false;
    if ((v.n < 0) !== (kn < 0)) return false;
    var places = t.split(".")[1].length, scale = Math.pow(10, places), a = Math.abs(kn);
    var entered = Math.abs(v.n) * (scale / v.d);
    return entered === Math.floor(a * scale / kd) || entered === Math.floor((2 * a * scale + kd) / (2 * kd));
  }
  function isCorrect(q, a) {
    if (a === undefined || a === null || a === "") return false;
    if (q.type === "mc") return a === q.answer;
    return q.keys.some(function (k) { return sprMatches(a, k); });
  }
  function cleanAnswer(q, v) {
    if (v === undefined || v === null || v === "") return null;
    if (q.type === "mc") return (typeof v === "number" && v >= 0 && v < q.choices.length) ? v : null;
    var t = String(v).replace(/\s+/g, "").slice(0, 6);
    return t || null;
  }
  function graded(q, i, a) {
    var answered = a !== undefined && a !== null && a !== "";
    var out = { index: i, id: q.id, type: q.type, domain: q.domain, skill: q.skill, difficulty: q.difficulty, stem: q.stem,
      correct: isCorrect(q, a), answered: answered,
      your_answer: answered ? (q.type === "mc" ? LETTERS[a] : String(a)) : null,
      answer: q.type === "mc" ? LETTERS[q.answer] : q.answer_text, explain_html: q.explain_html };
    if (q.type === "mc") { out.choices = q.choices; out.answer_index = q.answer; }
    return out;
  }
  function publicQ(q) {
    var o = { id: q.id, domain: q.domain, skill: q.skill, difficulty: q.difficulty, type: q.type, stem: q.stem };
    if (q.type === "mc") o.choices = q.choices;
    return o;
  }
  function publicSession(s) {
    var checked = {};
    Object.keys(s.checked).forEach(function (k) { checked[k] = graded(byId[s.item_ids[k]], Number(k), s.checked[k]); });
    var o = { id: s.id, mode: s.mode, title: s.title, plan_task: s.plan_task || null, domain: s.domain, skill: s.skill, minutes: s.minutes, created_at: s.created_at,
      submitted: !!s.submitted_at, questions: s.item_ids.map(function (id) { return publicQ(byId[id]); }), checked: checked };
    if (s.result) o.result = s.result;
    var tag = parseTag(s.plan_task);
    if (tag) o.level = { track: tag.track, n: tag.level, tier: BANK.levels.rungs[tag.level - 1].tier, pass: BANK.levels.pass, top: BANK.levels.count, boss: s.item_ids.length - 1 };
    return o;
  }

  /* ---------- requests ---------- */
  function overview() {
    var st = load();
    var domains = BANK.topics.map(function (d) {
      var skills = d.skills.map(function (sk) {
        var done = pool(d.key, sk.key).filter(function (id) { return st.seen[id]; }).length;
        return { key: sk.key, name: sk.name, total: sk.total, done: done };
      });
      return { key: d.key, name: d.name, skills: skills,
        total: skills.reduce(function (a, s) { return a + s.total; }, 0), done: skills.reduce(function (a, s) { return a + s.done; }, 0) };
    });
    var unfinished = Object.keys(st.sessions).map(function (k) { return st.sessions[k]; })
      .filter(function (s) { return !s.submitted_at; }).sort(function (a, b) { return b.id - a.id; }).slice(0, 5)
      .map(function (s) { return { id: s.id, mode: s.mode, title: s.title, created_at: s.created_at, questions: s.item_ids.length, checked: Object.keys(s.checked).length }; });
    return { total: BANK.items.length, done: domains.reduce(function (a, d) { return a + d.done; }, 0), domains: domains,
      test: { questions: BANK.test.questions, minutes: BANK.test.minutes }, topic_counts: BANK.topic_counts, unfinished: unfinished };
  }
  function create(data) {
    var st = load(), ids, title, minutes = 0;
    if (data.mode === "test") {
      ids = [];
      Object.keys(BANK.mix).forEach(function (d) { ids = ids.concat(draw(st, pool(d), BANK.mix[d], true)); });
      ids = shuffle(ids).sort(function (a, b) { return BANK.order[byId[a].difficulty] - BANK.order[byId[b].difficulty]; });
      title = "Math practice test"; minutes = BANK.test.minutes;
    } else if (data.mode === "topic") {
      title = topicTitle(data.domain, data.skill || null);
      if (!title) return fail(400, "Pick a topic to practice.");
      if (BANK.topic_counts.indexOf(data.count) < 0) return fail(400, "Pick how many questions you want.");
      ids = draw(st, pool(data.domain, data.skill || null), data.count);
    } else {
      return fail(400, "Choose a practice test or a topic.");
    }
    var s = { id: st.nextId++, mode: data.mode, domain: data.domain || null, skill: data.skill || null, title: title,
      item_ids: ids, minutes: minutes, checked: {}, created_at: now(), submitted_at: null, result: null };
    st.sessions[s.id] = s; save(st);
    return Promise.resolve({ session: publicSession(s) });
  }
  // Adds questions to the done list; returns the topics this finished, like the server does.
  function markSeen(st, ids) {
    ids.forEach(function (id) { st.seen[id] = 1; });
    if (!ids.length) return [];
    var finished = [];
    topicsOf(ids).forEach(function (t) {
      var kind = t.split(":")[0], rest = t.split(":")[1].split("/");
      var all = pool(rest[0], rest[1] || null).every(function (id) { return st.seen[id]; });
      if (!all || st.completed[t]) return;
      st.completed[t] = 1;
      finished.push({ kind: kind, name: topicTitle(rest[0], rest[1] || null) });
    });
    return finished;
  }
  function check(st, s, data) {
    if (s.mode !== "topic" && s.mode !== "quiz") return fail(400, "Answers on a practice test are checked when you submit it.");
    if (s.submitted_at) return fail(409, "This set is already finished.");
    var i = Number(data.index);
    if (!(i >= 0 && i < s.item_ids.length)) return fail(400, "That question isn't in this set.");
    var q = byId[s.item_ids[i]], a = cleanAnswer(q, data.answer);
    if (a === null) return fail(400, "Choose or type an answer first.");
    var finished = [], fresh = !(String(i) in s.checked);
    if (fresh) { s.checked[i] = a; finished = markSeen(st, [q.id]); save(st); }
    var g = graded(q, i, s.checked[i]);
    // Level up rewards: XP, combos and the boss question (play-local.js, same rules as services/game.py).
    if (fresh && parseTag(s.plan_task) && window.GraphitePlayLocal) {
      var right = {};
      Object.keys(s.checked).forEach(function (k) { right[k] = isCorrect(byId[s.item_ids[k]], s.checked[k]); });
      g.game = window.GraphitePlayLocal.levelCheck(s, i, g.correct, right, s.item_ids.length);
    }
    return Promise.resolve({ question: g, finished: finished });
  }
  function submit(st, s, data) {
    if (s.submitted_at) return Promise.resolve({ result: s.result });
    var answers = {};
    Object.keys(data.answers || {}).forEach(function (k) {
      var i = Number(k); if (!(i >= 0 && i < s.item_ids.length)) return;
      var a = cleanAnswer(byId[s.item_ids[i]], data.answers[k]); if (a !== null) answers[i] = a;
    });
    Object.keys(s.checked).forEach(function (k) { answers[k] = s.checked[k]; });
    var res = { correct: 0, total: s.item_ids.length, multiple_choice: { right: 0, total: 0 }, student_produced: { right: 0, total: 0 }, by_domain: [], questions: [] };
    var dom = {};
    s.item_ids.forEach(function (id, i) {
      var q = byId[id], g = graded(q, i, answers[i]);
      if (g.correct) res.correct++;
      var b = q.type === "mc" ? res.multiple_choice : res.student_produced; b.total++; if (g.correct) b.right++;
      if (!dom[q.domain]) { dom[q.domain] = { domain: q.domain, right: 0, total: 0 }; res.by_domain.push(dom[q.domain]); }
      dom[q.domain].total++; if (g.correct) dom[q.domain].right++;
      res.questions.push(g);
    });
    res.finished = markSeen(st, Object.keys(answers).map(function (k) { return s.item_ids[k]; }));
    var limit = s.minutes ? s.minutes * 60 + 120 : s.item_ids.length * 600;
    res.seconds_used = Math.max(0, Math.min(Number(data.seconds_used) || 0, limit));
    res.practice_id = s.id; res.mode = s.mode; res.title = s.title; res.submitted_at = now();
    var tag = parseTag(s.plan_task);
    if (tag) {
      var before = lvProgress(st, tag.track).levels[tag.level];
      res.level = levelResult(st, s, res.correct);
      if (window.GraphitePlayLocal) res.game = window.GraphitePlayLocal.levelFinish(s, tag.level, res.correct, res.total, res.level.passed, !(before && before.passed), res.level.top);
    }
    s.submitted_at = res.submitted_at; s.result = res; save(st);
    return Promise.resolve({ result: res });
  }


  /* ---------- study plan (same rules as services/diagnostic.py, studyplan.py and practice.py) ---------- */
  var RW = {}, DG = BANK.diagnostic;
  (BANK.rw || []).forEach(function (q) { RW[q.id] = q; });
  function itemAny(id) { return RW[id] || byId[id]; }
  function newSession(st, mode, title, ids, minutes, extra) {
    var s = { id: st.nextId++, mode: mode, domain: null, skill: null, title: title, item_ids: ids, minutes: minutes,
      checked: {}, created_at: now(), submitted_at: null, result: null, plan_id: null, plan_task: null };
    Object.keys(extra || {}).forEach(function (k) { s[k] = extra[k]; });
    st.sessions[s.id] = s;
    return s;
  }
  function buildTest(st) {
    var ids = [];
    Object.keys(BANK.mix).forEach(function (d) { ids = ids.concat(draw(st, pool(d), BANK.mix[d], true)); });
    return shuffle(ids).sort(function (a, b) { return BANK.order[byId[a].difficulty] - BANK.order[byId[b].difficulty]; });
  }
  function pickDiagnostic(st) {
    var ids = [], used = {};
    DG.math_slots.forEach(function (slot) {
      var cands = BANK.items.filter(function (q) { return q.domain_key === slot[0] && q.difficulty === slot[1] && !used[q.skill_key]; });
      var fresh = cands.filter(function (q) { return !st.seen[q.id]; });
      var list = fresh.length ? fresh : cands, q = list[Math.floor(Math.random() * list.length)];
      used[q.skill_key] = 1; ids.push(q.id);
    });
    DG.rw_domains.forEach(function (d) {
      var c = (BANK.rw || []).filter(function (q) { return q.domain === d; });
      ids.push(c[Math.floor(Math.random() * c.length)].id);
    });
    return ids;
  }
  function publicDiagQ(id) {
    var q = itemAny(id), o = { id: id, section: q.section || "Math", domain: q.domain, skill: q.skill, type: q.type, stem: q.stem };
    if (q.type === "mc") o.choices = q.choices;
    return o;
  }
  function gradeDiagnostic(ids, answers, sure) {
    var questions = [], byDom = {}, order = [], pts = 0, wt = 0;
    ids.forEach(function (id, i) {
      var q = itemAny(id), rw = q.section === "Reading and Writing", a = answers[i], g;
      if (rw) {
        g = { index: i, id: id, type: "mc", domain: q.domain, skill: q.skill, stem: q.stem, choices: q.choices, answer_index: q.answer,
          answer: LETTERS[q.answer], answered: a !== undefined, correct: a === q.answer, your_answer: a !== undefined ? LETTERS[a] : null, explain_html: q.explain_html };
      } else {
        g = graded(q, i, a);
      }
      g.section = rw ? "Reading and Writing" : "Math";
      g.sure = !!sure[i];
      g.score = g.correct ? (g.sure ? DG.sure : DG.guess) : 0;
      if (!rw) { g.skill_key = q.skill_key; g.domain_key = q.domain_key; var w = DG.weight[q.difficulty]; pts += g.score * w; wt += w; }
      if (!byDom[q.domain]) { byDom[q.domain] = { section: g.section, domain: q.domain, domain_key: q.domain_key || null, points: 0, count: 0 }; order.push(q.domain); }
      byDom[q.domain].points += g.score; byDom[q.domain].count++;
      questions.push(g);
    });
    var rank = BANK.topics.map(function (t) { return t.name; }).concat(DG.rw_domains);
    var domains = order.map(function (k) {
      var d = byDom[k], score = Math.round(d.points / d.count * 100) / 100;
      return { section: d.section, domain: d.domain, domain_key: d.domain_key, score: score, label: score >= DG.strong ? "Strength" : (score < DG.weak ? "Focus" : "Building") };
    }).sort(function (a, b) { return rank.indexOf(a.domain) - rank.indexOf(b.domain); });
    var skills = {};
    questions.forEach(function (q) { if (q.section === "Math") skills[q.skill_key] = q.score; });
    return { questions: questions, correct: questions.filter(function (q) { return q.correct; }).length, total: questions.length,
      domains: domains, skills: skills, level: wt ? Math.round(pts / wt * 100) / 100 : 0.5,
      strengths: domains.slice().sort(function (a, b) { return b.score - a.score; }).filter(function (d) { return d.score >= DG.strong; }).map(function (d) { return d.domain; }),
      focus: domains.slice().sort(function (a, b) { return a.score - b.score; }).filter(function (d) { return d.score < DG.weak; }).map(function (d) { return d.domain; }) };
  }

  function isoDate(d) { return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0"); }
  function parseDate(s) { var p = s.split("-"); return new Date(Number(p[0]), Number(p[1]) - 1, Number(p[2])); }
  function addDays(d, n) { var x = new Date(d.getTime()); x.setDate(x.getDate() + n); return x; }
  function daysBetween(a, b) { return Math.round((b - a) / 86400000); }
  function r2(x) { return Math.round(x * 100) / 100; }
  function difficultyAt(level, p) { var s = 0.2 + 0.3 * level, e = 0.75 + 0.2 * level; return r2(Math.min(0.95, Math.max(0.05, s + (e - s) * p))); }
  function mixFor(d, n) {
    n = n || 10;
    var hard = Math.min(1, Math.max(0, (d - 0.3) / 0.7)) * 0.8, easy = Math.min(1, Math.max(0, (0.5 - d) / 0.5)) * 0.6;
    var shares = { easy: easy, medium: Math.max(0, 1 - easy - hard), hard: hard }, counts = {}, sum = 0;
    Object.keys(shares).forEach(function (k) { counts[k] = Math.floor(shares[k] * n); sum += counts[k]; });
    Object.keys(shares).sort(function (a, b) { return (shares[b] * n - counts[b]) - (shares[a] * n - counts[a]); })
      .slice(0, n - sum).forEach(function (k) { counts[k]++; });
    return counts;
  }
  function mixLabel(mix) {
    var parts = Object.keys(mix).filter(function (k) { return mix[k]; }).sort(function (a, b) { return mix[b] - mix[a] || (a < b ? 1 : -1); });
    if (!parts.length) return "";
    return "Mostly " + parts[0] + (parts.length > 1 ? ", some " + parts[1] : "");
  }
  function buildPlan(results, testDate, hours, today) {
    var monday = addDays(today, -((today.getDay() + 6) % 7)), exam = testDate ? parseDate(testDate) : null;
    if (exam && exam < today) exam = null;
    var total = exam ? Math.min(26, Math.floor(daysBetween(monday, exam) / 7) + 1) : 8;
    var hasTest = !!exam && total >= 2, study = hasTest ? total - 1 : total, level = results.level;
    hours = hours || 3;
    var domScore = {};
    results.domains.forEach(function (d) { if (d.section === "Math") domScore[d.domain_key] = d.score; });
    var skills = [];
    BANK.topics.forEach(function (d) { d.skills.forEach(function (s) {
      var base = domScore[d.key] !== undefined ? domScore[d.key] : 0.5, t = results.skills[s.key];
      skills.push({ domain: d.key, skill: s.key, name: s.name, est: r2(t !== undefined ? 0.7 * t + 0.3 * base : base) });
    }); });
    var prio = {}, growth = {}, by = {}, ord = {};
    skills.forEach(function (s, i) { prio[s.skill] = (1 - s.est) + 0.05; growth[s.skill] = 0.06 + 0.12 * (1 - s.est); by[s.skill] = s; ord[s.skill] = i; });
    var focused = [], lastSeen = {};
    var rwSorted = results.domains.filter(function (d) { return d.section === "Reading and Writing"; }).sort(function (a, b) { return a.score - b.score; }).map(function (d) { return d.domain; });
    var rwOrder = rwSorted.length ? rwSorted : DG.rw_domains;
    function ref(k) { return { domain: by[k].domain, skill: k, name: by[k].name }; }
    var weeks = [];
    for (var w = 0; w < study; w++) {
      var p = study > 1 ? w / (study - 1) : 1;
      var phase = p >= 0.75 ? "sharpen" : ((p >= 0.34 || study < 3) ? "build" : "foundation");
      var d = difficultyAt(level, p), mix = mixFor(d);
      var picks = Object.keys(prio).sort(function (a, b) { return (prio[b] - prio[a]) || (ord[a] - ord[b]); }).slice(0, 2);
      Object.keys(prio).forEach(function (k) { prio[k] += growth[k]; });
      picks.forEach(function (k) { prio[k] = (1 - by[k].est) * 0.25; });
      var earlier = {};
      focused.forEach(function (f) { if (f[0] <= w - 2 && picks.indexOf(f[1]) < 0) earlier[f[1]] = 1; });
      var ek = Object.keys(earlier).sort(function (a, b) { return (lastSeen[a] - lastSeen[b]) || (by[a].est - by[b].est) || (ord[a] - ord[b]); });
      var review = ek.length ? ek[0] : null;
      picks.forEach(function (k) { focused.push([w, k]); });
      picks.concat(review ? [review] : []).forEach(function (k) { lastSeen[k] = w; });
      var focus = picks.map(ref), n = w + 1;
      var tasks = [{ key: "w" + n + "-drill-1", kind: "drill", title: focus[0].name, skill: focus[0], count: 10 }];
      if (hours >= 2) tasks.push({ key: "w" + n + "-drill-2", kind: "drill", title: focus[1].name, skill: focus[1], count: 10 });
      tasks.push({ key: "w" + n + "-quiz", kind: "quiz", title: "Week " + n + " quiz", count: 10 });
      if (phase !== "foundation" && (phase === "sharpen" || w % 2 === 1)) tasks.push({ key: "w" + n + "-test", kind: "test", title: "Math practice test" });
      weeks.push({ n: n, week_of: isoDate(addDays(monday, 7 * w)), phase: phase, phase_label: DG.phases[phase], difficulty: d, mix: mix,
        difficulty_label: mixLabel(mix), focus: focus, review: review ? ref(review) : null, rw_focus: rwOrder[w % rwOrder.length], tasks: tasks });
    }
    var byEst = skills.slice().sort(function (a, b) { return (a.est - b.est) || (ord[a.skill] - ord[b.skill]); });
    if (hasTest) {
      var best = skills.slice().sort(function (a, b) { return (b.est - a.est) || (ord[a.skill] - ord[b.skill]); })[0];
      weeks.push({ n: study + 1, week_of: isoDate(addDays(monday, 7 * study)), phase: "test", phase_label: DG.phases.test, difficulty: 0.3,
        mix: { easy: 5, medium: 5, hard: 0 }, difficulty_label: "Easy and medium, to build confidence",
        focus: [byEst[0], best].map(function (s) { return ref(s.skill); }), review: null, rw_focus: null,
        tasks: [{ key: "w" + (study + 1) + "-quiz", kind: "quiz", title: "Warm-up quiz", count: 10 }], checklist: DG.checklist });
    }
    var math = results.domains.filter(function (d) { return d.section === "Math"; }).sort(function (a, b) { return b.score - a.score; });
    var parts = [];
    if (results.strengths.length) parts.push("Your strongest area is " + results.strengths[0] + ".");
    else if (math.length) parts.push("Your strongest Math area right now is " + math[0].domain + ".");
    parts.push("Your plan opens with " + byEst[0].name + " and " + byEst[1].name + ", where you have the most points to gain, and brings every Math topic back around before test day.");
    var sw = weeks.filter(function (x) { return x.phase !== "test"; }), first = sw[0].difficulty_label.toLowerCase(), last = sw[sw.length - 1].difficulty_label.toLowerCase();
    parts.push(last !== first ? "Quizzes start " + first + " and build to " + last + (exam ? " by " + exam.toLocaleDateString("en-US", { month: "long" }) + " " + exam.getDate() + "." : ".") : "Quizzes run " + first + ".");
    return { version: 1, created: isoDate(today), start: isoDate(monday), test_date: exam ? isoDate(exam) : null, hours: hours, level: level,
      summary: parts.join(" "), strengths: results.strengths, focus_areas: results.focus, weeks: weeks };
  }
  function currentWeek(plan, today) { return Math.max(0, Math.min(plan.weeks.length - 1, Math.floor(daysBetween(parseDate(plan.start), today) / 7))); }
  var NEIGHBORS = { easy: ["medium", "hard"], medium: ["easy", "hard"], hard: ["medium", "easy"] };
  function drawMix(st, skills, mix) {
    var poolIds = [];
    skills.forEach(function (s) { poolIds = poolIds.concat(pool(s.domain, s.skill)); });
    var un = {};
    ["easy", "medium", "hard"].forEach(function (d) { un[d] = shuffle(poolIds.filter(function (id) { return !st.seen[id] && byId[id].difficulty === d; })); });
    var picked = [];
    Object.keys(mix).forEach(function (d) {
      var n = mix[d];
      [d].concat(NEIGHBORS[d]).forEach(function (src) { while (n && un[src].length) { picked.push(un[src].pop()); n--; } });
      if (n) {
        var rest = poolIds.filter(function (id) { return picked.indexOf(id) < 0; });
        draw(st, rest, n, true).forEach(function (id) { if (picked.indexOf(id) < 0) picked.push(id); });
      }
    });
    return picked.sort(function (a, b) { return BANK.order[byId[a].difficulty] - BANK.order[byId[b].difficulty]; });
  }
  function adjustedMix(st, planId, difficulty, n) {
    var rows = Object.keys(st.sessions).map(function (k) { return st.sessions[k]; })
      .filter(function (s) { return s.plan_id === planId && s.mode === "quiz" && s.submitted_at; })
      .sort(function (a, b) { return b.id - a.id; }).slice(0, 2);
    if (rows.length) {
      var right = 0, tot = 0;
      rows.forEach(function (s) { right += s.result.correct; tot += s.item_ids.length; });
      if (right / tot >= 0.8) difficulty += 0.1; else if (right / tot <= 0.5) difficulty -= 0.1;
    }
    return mixFor(Math.min(0.95, Math.max(0.05, difficulty)), n);
  }
  function latestPlan(st) { return st.plans.length ? st.plans[st.plans.length - 1] : null; }
  function planTasks(st, planId) {
    var out = {};
    Object.keys(st.sessions).map(function (k) { return st.sessions[k]; }).filter(function (s) { return s.plan_id === planId; })
      .sort(function (a, b) { return a.id - b.id; }).forEach(function (s) {
        var prev = out[s.plan_task];
        out[s.plan_task] = { session_id: s.id, submitted: !!s.submitted_at, done: (prev && prev.done) || !!s.submitted_at,
          correct: s.result ? s.result.correct : null, total: s.item_ids.length };
      });
    return out;
  }
  function planOut(st, row, today) {
    var o = JSON.parse(JSON.stringify(row.plan));
    o.id = row.id; o.current_week = currentWeek(row.plan, today); o.tasks = planTasks(st, row.id);
    o.results = st.diagnostics[row.diagnostic_id].results;
    return o;
  }
  function savePlan(st, diagId, today) {
    var row = { id: st.plans.length + 1, diagnostic_id: diagId,
      plan: buildPlan(st.diagnostics[diagId].results, st.profile.test_date, st.profile.weekly_goal_hours, today) };
    st.plans.push(row);
    return row;
  }
  function setProfile(st, data) {
    if (data.test_date) st.profile.test_date = data.test_date;
    var h = Number(data.weekly_goal_hours);
    if (h >= 1 && h <= 20) st.profile.weekly_goal_hours = h;
  }
  function planCall(path, data) {
    var st = load(), today = new Date(); today = new Date(today.getFullYear(), today.getMonth(), today.getDate());
    st.diagnostics = st.diagnostics || {}; st.plans = st.plans || []; st.profile = st.profile || { test_date: null, weekly_goal_hours: 3 };
    var diags = Object.keys(st.diagnostics).map(function (k) { return st.diagnostics[k]; }).sort(function (a, b) { return a.id - b.id; });
    var lastDiag = diags[diags.length - 1];
    function pubDiag(d) { var o = { id: d.id, submitted: !!d.submitted_at, questions: d.item_ids.map(publicDiagQ) }; if (d.results) o.results = d.results; return o; }
    if (path === "/api/plan") {
      var row = latestPlan(st);
      return Promise.resolve({ user: st.profile, diagnostic: lastDiag ? pubDiag(lastDiag) : null, plan: row ? planOut(st, row, today) : null });
    }
    if (path === "/api/plan/diagnostic") {
      setProfile(st, data || {});
      var open = diags.filter(function (d) { return !d.submitted_at; }).pop();
      if (!open) { open = { id: (lastDiag ? lastDiag.id : 0) + 1, item_ids: pickDiagnostic(st), submitted_at: null, results: null }; st.diagnostics[open.id] = open; }
      save(st);
      return Promise.resolve({ diagnostic: pubDiag(open) });
    }
    var m = /^\/api\/plan\/diagnostic\/(\d+)\/submit$/.exec(path);
    if (m) {
      var d = st.diagnostics[m[1]];
      if (!d) return fail(404, "That diagnostic doesn't exist.");
      if (d.submitted_at) return fail(409, "This diagnostic is already finished.");
      var answers = {}, sure = {};
      Object.keys((data && data.answers) || {}).forEach(function (k) {
        var i = Number(k), id = d.item_ids[i]; if (!id) return;
        var q = itemAny(id), v = data.answers[k];
        var a = q.section === "Reading and Writing" ? (typeof v === "number" && v >= 0 && v < 4 ? v : null) : cleanAnswer(q, v);
        if (a !== null) { answers[i] = a; sure[i] = data.sure && data.sure[k] === true; }
      });
      d.results = gradeDiagnostic(d.item_ids, answers, sure); d.submitted_at = now();
      markSeen(st, Object.keys(answers).map(function (k) { return d.item_ids[k]; }).filter(function (id) { return !RW[id]; }));
      var r = savePlan(st, d.id, today); save(st);
      return Promise.resolve({ results: d.results, plan: planOut(st, r, today) });
    }
    if (path === "/api/plan/rebuild") {
      setProfile(st, data || {});
      var done = diags.filter(function (x) { return x.submitted_at; }).pop();
      if (!done) return fail(400, "Take the diagnostic first.");
      var r3 = savePlan(st, done.id, today); save(st);
      return Promise.resolve({ plan: planOut(st, r3, today) });
    }
    if (path === "/api/plan/tasks") {
      var pr = latestPlan(st);
      if (!pr) return fail(400, "Take the diagnostic first.");
      var wi = Number(data.week), week = pr.plan.weeks[wi];
      if (!week) return fail(400, "That week isn't in your plan.");
      var task = week.tasks.filter(function (t) { return t.key === data.task; })[0];
      if (!task) return fail(400, "That task isn't in your plan.");
      var openS = Object.keys(st.sessions).map(function (k) { return st.sessions[k]; })
        .filter(function (s) { return s.plan_id === pr.id && s.plan_task === task.key && !s.submitted_at; }).pop();
      var s;
      if (openS) s = openS;
      else if (task.kind === "test") s = newSession(st, "test", "Math practice test", buildTest(st), BANK.test.minutes, { plan_id: pr.id, plan_task: task.key });
      else {
        var sk = task.kind === "drill" ? [task.skill] : week.focus.concat(week.review ? [week.review] : []);
        var mix = week.phase === "test" ? week.mix : adjustedMix(st, pr.id, week.difficulty, task.count);
        s = newSession(st, "quiz", task.kind === "drill" ? "Week " + week.n + ": " + task.skill.name : task.title, drawMix(st, sk, mix), 0, { plan_id: pr.id, plan_task: task.key });
      }
      save(st);
      return Promise.resolve({ session: publicSession(s) });
    }
    return fail(404, "Not found.");
  }

  /* ---------- Level up (same rules as services/levels.py) ---------- */
  var LV = BANK.levels;
  function parseTag(task) {
    var p = String(task || "").split(":");
    return p.length === 3 && p[0] === "ladder" && /^\d+$/.test(p[2]) ? { track: p[1], level: Number(p[2]) } : null;
  }
  function lvTrack(key) { return LV.tracks.filter(function (t) { return t.key === key; })[0] || null; }
  function lvProgress(st, key) {
    var out = {}, top = 0;
    Object.keys(st.sessions).map(function (k) { return st.sessions[k]; }).sort(function (a, b) { return a.id - b.id; }).forEach(function (s) {
      var t = parseTag(s.plan_task); if (!t || t.track !== key) return;
      var lv = out[t.level] = out[t.level] || { best: null, passed: false, open_id: null };
      if (s.submitted_at) { lv.best = Math.max(lv.best || 0, s.result.correct); lv.passed = lv.passed || s.result.correct >= LV.pass; lv.open_id = null; }
      else lv.open_id = s.id;
    });
    Object.keys(out).forEach(function (n) { if (out[n].passed) top = Math.max(top, Number(n)); });
    return { levels: out, unlocked: Math.min(LV.count, top + 1) };
  }
  function levelResult(st, s, correct) {
    var t = parseTag(s.plan_task), p = lvProgress(st, t.track), passed = correct >= LV.pass, tr = lvTrack(t.track);
    return { track: t.track, track_name: tr ? tr.name : t.track, level: t.level, pass: LV.pass, total: s.item_ids.length, passed: passed,
      next: passed && t.level < LV.count ? t.level + 1 : null, unlocked: passed ? Math.max(p.unlocked, Math.min(LV.count, t.level + 1)) : p.unlocked, top: LV.count };
  }
  // The hardest question goes last: it's the level's boss question (same as levels.boss_last).
  var HARD = { easy: 0, medium: 1, hard: 2 };
  function bossLast(ids) {
    if (!ids.length) return ids;
    var b = 0; ids.forEach(function (id, i) { if (HARD[byId[id].difficulty] >= HARD[byId[ids[b]].difficulty]) b = i; });
    return ids.slice(0, b).concat(ids.slice(b + 1), [ids[b]]);
  }
  function levelsCall(path, data) {
    var st = load();
    if (path === "/api/levels") {
      return Promise.resolve({ size: LV.size, pass: LV.pass, levels: LV.count, tracks: LV.tracks.map(function (t) {
        var p = lvProgress(st, t.key);
        var levels = LV.rungs.map(function (r) {
          var x = p.levels[r.n] || {};
          return { n: r.n, tier: r.tier, mix: r.mix, mix_label: r.mix_label, status: x.passed ? "passed" : (r.n <= p.unlocked ? "open" : "locked"),
            best: x.best == null ? null : x.best, resume_id: x.open_id || null };
        });
        return { key: t.key, name: t.name, unlocked: p.unlocked, levels: levels, all_passed: levels.every(function (l) { return l.status === "passed"; }) };
      }) });
    }
    if (path === "/api/levels/start") {
      var tr = lvTrack(data && data.track), n = data && data.level;
      if (!tr) return fail(400, "Pick a track to practice.");
      if (typeof n !== "number" || n % 1 || n < 1 || n > LV.count) return fail(400, "Pick a level.");
      var p = lvProgress(st, tr.key);
      if (n > p.unlocked) return fail(403, "Pass level " + (n - 1) + " first to unlock level " + n + ".");
      var open = p.levels[n] && p.levels[n].open_id, s = open ? st.sessions[open] : null;
      if (!s) {
        s = newSession(st, "quiz", tr.name + " · Level " + n, bossLast(drawMix(st, tr.skills, LV.rungs[n - 1].mix)), 0,
          { domain: tr.key === "mixed" ? null : tr.key, plan_task: "ladder:" + tr.key + ":" + n });
        save(st);
      }
      return Promise.resolve({ session: publicSession(s) });
    }
    return fail(404, "Not found.");
  }

  /* ---------- parent dashboard (same rules as services/parent.py and routes/family.py) ----------
     The preview's student is the practice done in this browser. Linking uses the code the student made on
     their dashboard (site.js keeps it in graphite_family); the test parent ("beta2") is linked already. */
  var PB = BANK.parent, FKEY = "graphite_family";
  function fam() { try { return JSON.parse(localStorage.getItem(FKEY)) || { parents: [] }; } catch (e) { return { parents: [] }; } }
  function saveFam(f) { try { localStorage.setItem(FKEY, JSON.stringify(f)); } catch (e) { /* storage blocked */ } }
  function who() { var e = ""; try { e = sessionStorage.getItem("graphite_user") || ""; } catch (x) { /* storage blocked */ } return e; }
  function parentName() {
    var e = who(); if (e === "beta2") return "Beta2 Parent";
    var n = (e.split("@")[0] || "Parent").replace(/[._-]+/g, " ");
    return n.replace(/\b\w/g, function (c) { return c.toUpperCase(); });
  }
  function linked(f) { return f.parents.length > 0 || who() === "beta2"; }
  function money(c) { return "$" + (c / 100).toLocaleString("en-US", { maximumFractionDigits: 2 }); }
  function iso10(d) { return isoDate(d); }
  function addMonths(d, n) { var x = new Date(d.getFullYear(), d.getMonth() + n, 1), last = new Date(x.getFullYear(), x.getMonth() + 1, 0).getDate(); x.setDate(Math.min(d.getDate(), last)); return x; }
  function niceDay(s) { var d = parseDate(s); return d.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" }); }
  var OLD_PLANS = { daily: "sharpened", coached: "masterstroke" };
  function planInfo(key) { key = OLD_PLANS[key] || key; return PB.plans.filter(function (p) { return p.key === key; })[0]; }
  var WORDS = { week: "weekly", month: "monthly", year: "yearly" };
  // Same wording as plans.price_label: always per month, plus what's billed.
  function priceLabel(p, iv) {
    if (!iv || !p.cents[iv]) return "Free";
    var each = money(p.per_month_cents[iv]) + "/month";
    return iv === "month" ? each : each + ", billed " + money(p.cents[iv]) + " " + WORDS[iv];
  }
  function subOut(f, today) {
    var sub = f.sub || { plan: "free", interval: null, status: "active", renews_on: null, paused_until: null };
    var t = iso10(today);
    if (sub.status === "canceled" && sub.renews_on && sub.renews_on < t) sub = { plan: "free", interval: null, status: "active", renews_on: null, paused_until: null };
    if (sub.status === "paused" && sub.paused_until && sub.paused_until < t) { sub.status = "active"; sub.paused_until = null; }
    f.sub = sub;
    var p = planInfo(sub.plan) || planInfo("free");
    sub.plan = p.key;
    var iv = WORDS[sub.interval] ? sub.interval : null, price = iv ? p.cents[iv] : 0;
    return { plan: p.key, plan_name: p.name, interval: iv, status: sub.status, renews_on: sub.renews_on, paused_until: sub.paused_until,
      price_cents: price, price_label: priceLabel(p, iv) };
  }
  function billEvent(f, kind, detail, amount) {
    if (amount) detail += " No card was charged: payments aren't connected yet.";
    f.billing = [{ at: now(), kind: kind, detail: detail, amount_cents: amount || 0 }].concat(f.billing || []).slice(0, 20);
  }
  function parentSummary(st, f, today) {
    var all = Object.keys(st.sessions).map(function (k) { return st.sessions[k]; });
    var monday = new Date(today); monday.setDate(today.getDate() - ((today.getDay() + 6) % 7));
    var since = iso10(monday), dates = {};
    all.forEach(function (x) { dates[x.created_at.slice(0, 10)] = 1; if (x.submitted_at) dates[x.submitted_at.slice(0, 10)] = 1; });
    Object.keys(st.diagnostics || {}).forEach(function (k) { var d = st.diagnostics[k]; if (d.submitted_at) dates[d.submitted_at.slice(0, 10)] = 1; });
    var streak = 0, day = new Date(today); if (!dates[iso10(day)]) day.setDate(day.getDate() - 1);
    while (dates[iso10(day)]) { streak++; day.setDate(day.getDate() - 1); }
    var times = Object.keys(dates).sort(), last = times.length ? times[times.length - 1] + "T12:00:00Z" : null;
    var week = all.filter(function (x) { return x.submitted_at && x.submitted_at.slice(0, 10) >= since; });
    var asked = 0, right = 0, secs = 0, answered = 0;
    week.forEach(function (x) { asked += x.item_ids.length; right += x.result.correct; secs += x.result.seconds_used || 0; });
    all.forEach(function (x) { if (x.created_at.slice(0, 10) >= since) answered += x.submitted_at ? x.result.questions.filter(function (q) { return q.answered; }).length : Object.keys(x.checked).length; });
    var days = [0, 1, 2, 3, 4, 5, 6].map(function (i) { var d = new Date(monday); d.setDate(monday.getDate() + i); return !!dates[iso10(d)]; });
    var prof = st.profile || {}, goal = (prof.weekly_goal_hours || 3) * 60;
    var o = { last_active: last, streak_days: streak, minutes_week: Math.floor(secs / 60), goal_minutes: goal, study_days_week: days,
      days_to_test: prof.test_date ? Math.max(0, daysBetween(today, parseDate(prof.test_date))) : null,
      questions_week: answered, accuracy_week: asked ? Math.round(right / asked * 100) : null };
    var tests = all.filter(function (x) { return x.mode === "test" && x.submitted_at; }).sort(function (a, b) { return a.submitted_at < b.submitted_at ? -1 : 1; });
    var scores = tests.map(function (x) { var d = parseDate(x.submitted_at.slice(0, 10)); return { label: d.toLocaleDateString("en-US", { month: "short", day: "numeric" }), date: x.submitted_at.slice(0, 10), pct: Math.round(x.result.correct / x.result.total * 100), correct: x.result.correct, total: x.result.total }; });
    var latest = tests.length ? tests[tests.length - 1].result : null, byDom = {};
    if (latest) latest.by_domain.forEach(function (d) { byDom[d.domain] = Math.round(d.right / d.total * 100); });
    var measured = BANK.topics.map(function (t) { return t.name; }).filter(function (n) { return byDom[n] != null && byDom[n] < 100; }).sort(function (a, b) { return byDom[a] - byDom[b]; }).slice(0, 3);
    var domains = BANK.topics.map(function (t) { return { name: t.name, pct: byDom[t.name] == null ? null : byDom[t.name], focus: measured.indexOf(t.name) >= 0 }; });
    var dsub = Object.keys(st.diagnostics || {}).map(function (k) { return st.diagnostics[k]; }).filter(function (d) { return d.submitted_at; }).sort(function (a, b) { return a.id - b.id; }).pop();
    var diagnostic = dsub ? { at: dsub.submitted_at, correct: dsub.results.correct, total: dsub.results.total, strengths: dsub.results.strengths || [], focus: dsub.results.focus || [] } : null;
    var plan = null, prow = st.plans && st.plans.length ? st.plans[st.plans.length - 1] : null;
    if (prow) {
      var po = planOut(st, prow, today), w = po.weeks[po.current_week], states = po.tasks;
      plan = { week: w.n, weeks: po.weeks.length, phase: w.phase_label, difficulty: w.difficulty_label, focus: (w.focus || []).map(function (x) { return x.name; }),
        done: w.tasks.filter(function (t) { return states[t.key] && states[t.key].done; }).length, tasks: w.tasks.length };
    }
    var ladder = LV.tracks.map(function (t) { var p = lvProgress(st, t.key); return { name: t.name, unlocked: p.unlocked, passed: Object.keys(p.levels).filter(function (n) { return p.levels[n].passed; }).length, levels: LV.count }; });
    var activity = all.filter(function (x) { return x.submitted_at; }).map(function (x) {
      var task = x.plan_task || "";
      var kind = x.mode === "test" ? "Practice test" : task.indexOf("ladder:") === 0 ? "Level up" : x.mode === "quiz" ? "Study plan" : x.mode === "review" ? "Review" : "Topic practice";
      return { title: x.title, kind: kind, at: x.submitted_at, correct: x.result.correct, total: x.item_ids.length, minutes: Math.round((x.result.seconds_used || 0) / 60) };
    });
    if (dsub) activity.push({ title: "10-question diagnostic", kind: "Diagnostic", at: dsub.submitted_at, correct: dsub.results.correct, total: dsub.results.total, minutes: null });
    activity.sort(function (a, b) { return a.at < b.at ? 1 : -1; });
    var settings = f.settings || { weekly_report: true, alert_days: 3 }, first = "Maya", alerts = [];
    if (settings.alert_days) {
      if (!last) alerts.push({ level: "warn", text: first + " hasn't started practicing yet." });
      else { var idle = daysBetween(parseDate(last.slice(0, 10)), today); if (idle >= settings.alert_days) alerts.push({ level: "warn", text: first + " hasn't practiced in " + idle + " days." }); }
    }
    if (o.days_to_test != null && o.days_to_test <= 21 && !diagnostic) alerts.push({ level: "warn", text: "The SAT is " + o.days_to_test + " days away and the diagnostic isn't done yet." });
    if (scores.length >= 2) {
      var ch = scores[scores.length - 1].pct - scores[scores.length - 2].pct;
      if (ch <= -10) alerts.push({ level: "warn", text: "The latest practice test was " + Math.abs(ch) + " points lower than the one before." });
      else if (ch >= 10) alerts.push({ level: "good", text: "Up " + ch + " points on the latest practice test." });
    }
    if ((today.getDay() + 6) % 7 >= 3 && goal && o.minutes_week < goal / 2) alerts.push({ level: "info", text: o.minutes_week + " of " + goal + " minutes studied this week so far." });
    if (streak >= 5) alerts.push({ level: "good", text: first + " has practiced " + streak + " days in a row." });
    return { student: { id: 1, name: "Maya Rivera", first_name: first, email: "student (preview)", grade: 11, test_date: prof.test_date || null,
        target_score: prof.target_score || null, weekly_goal_hours: prof.weekly_goal_hours || 3 },
      settings: settings, overview: o, alerts: alerts, scores: scores, domains: domains, diagnostic: diagnostic, plan: plan, levels: ladder,
      review: { total: 0, due: 0 }, activity: activity.slice(0, 15), subscription: subOut(f, today), billing: f.billing || [] };
  }
  function parentCall(path, data, method) {
    var st = load(), f = fam(), today = new Date(); today = new Date(today.getFullYear(), today.getMonth(), today.getDate());
    st.diagnostics = st.diagnostics || {}; st.plans = st.plans || []; st.profile = st.profile || { test_date: null, weekly_goal_hours: 3 };
    var students = linked(f) ? [{ id: 1, name: "Maya Rivera" }] : [];
    if (path === "/api/parent") return Promise.resolve({ parent: { name: parentName(), email: who() || "parent (preview)" }, students: students,
      plans: PB.plans, payments_live: false, alert_days: PB.alert_days });
    if (path === "/api/parent/link") {
      var code = String((data && data.code) || "").toUpperCase().replace(/[^A-Z0-9]/g, "");
      var mine = f.code && f.code.code.replace("-", "");
      if (!mine || code !== mine || new Date(f.code.expires_at) < new Date()) return fail(400, "That code didn't work. In this preview, make a code on the student dashboard's Account panel in this browser.");
      f.parents = [{ id: 1, name: parentName(), email: who() || "parent (preview)", since: now() }]; delete f.code; saveFam(f);
      return Promise.resolve({ student: { id: 1, name: "Maya Rivera" } });
    }
    var m = /^\/api\/parent\/students\/1(\/(settings|plan|report)(\/(pause|resume|cancel))?)?$/.exec(path);
    if (!m || !students.length) return fail(404, "That student isn't connected to your account.");
    var part = m[2], act = m[4];
    if (!part && method === "DELETE") { f.parents = []; saveFam(f); return Promise.resolve({ ok: true }); }
    if (!part) { var out = parentSummary(st, f, today); saveFam(f); return Promise.resolve(out); }
    if (part === "settings") {
      var d = data || {};
      if ("weekly_goal_hours" in d) { if (!(d.weekly_goal_hours >= 1 && d.weekly_goal_hours <= 20)) return fail(400, "Weekly goals run from 1 to 20 hours."); st.profile.weekly_goal_hours = d.weekly_goal_hours; }
      if ("test_date" in d) st.profile.test_date = d.test_date || null;
      if ("target_score" in d) st.profile.target_score = d.target_score || null;
      f.settings = { weekly_report: "weekly_report" in d ? !!d.weekly_report : (f.settings || {}).weekly_report !== false,
        alert_days: "alert_days" in d ? d.alert_days : ((f.settings || {}).alert_days == null ? 3 : f.settings.alert_days) };
      save(st); var s2 = parentSummary(st, f, today); saveFam(f); return Promise.resolve(s2);
    }
    if (part === "report") return Promise.resolve({ ok: true, to: (who() || "you") + " (in this preview, nothing is actually emailed)" });
    var sub = subOut(f, today);
    if (!act) {
      var plan = data && data.plan, iv = data && data.interval;
      if (!planInfo(plan)) return fail(400, "Pick a plan.");
      if (plan !== "free" && !WORDS[iv]) return fail(400, "Pick weekly, monthly or yearly billing.");
      if (plan === "free") {
        // Same as canceling: the paid plan runs to the end of the time paid for, then the free plan starts.
        if (sub.plan !== "free" && sub.status !== "canceled") {
          f.sub.status = "canceled"; f.sub.paused_until = null;
          billEvent(f, "cancel", "Canceled. " + sub.plan_name + " stays on until " + niceDay(f.sub.renews_on) + ", then the plan returns to the free " + planInfo("free").name + " plan.");
        }
      }
      else {
        var next = iv === "week" ? new Date(today.getFullYear(), today.getMonth(), today.getDate() + 7) : addMonths(today, iv === "month" ? 1 : 12);
        var renews = iso10(next), price = planInfo(plan).cents[iv];
        f.sub = { plan: plan, interval: iv, status: "active", renews_on: renews, paused_until: null };
        billEvent(f, "change", planInfo(plan).name + ", billed " + WORDS[iv] + " at " + money(price) + ". Renews " + niceDay(renews) + ".", price);
      }
    } else {
      var ok = { pause: sub.plan !== "free" && sub.status === "active", cancel: sub.plan !== "free" && sub.status !== "canceled", resume: sub.status !== "active" }[act];
      if (!ok) return fail(409, "That change doesn't apply to the current plan.");
      if (act === "pause") {
        var until = new Date(today); until.setDate(until.getDate() + PB.pause_days);
        var nr = parseDate(f.sub.renews_on); nr.setDate(nr.getDate() + PB.pause_days);
        f.sub.status = "paused"; f.sub.paused_until = iso10(until); f.sub.renews_on = iso10(nr);
        billEvent(f, "pause", "Paused until " + niceDay(f.sub.paused_until) + ". The next bill moves to " + niceDay(f.sub.renews_on) + ".");
      } else if (act === "cancel") {
        f.sub.status = "canceled"; f.sub.paused_until = null;
        billEvent(f, "cancel", "Canceled. " + sub.plan_name + " stays on until " + niceDay(f.sub.renews_on) + ", then the plan returns to the free " + planInfo("free").name + " plan.");
      } else {
        var was = f.sub.status; f.sub.status = "active"; f.sub.paused_until = null;
        billEvent(f, "resume", was === "paused" ? "Resumed." : "Cancellation undone. Renews " + niceDay(f.sub.renews_on) + ".");
      }
    }
    var fresh = subOut(f, today); saveFam(f);
    return Promise.resolve({ subscription: fresh, billing: f.billing || [] });
  }

  function call(path, data, method) {
    path = path.split("?")[0];
    if (path.indexOf("/api/parent") === 0) return parentCall(path, data, method);
    if (path.indexOf("/api/levels") === 0) return levelsCall(path, data);
    if (path.indexOf("/api/plan") === 0) return planCall(path, data);
    if (path === "/api/practice") return Promise.resolve(overview());
    if (path === "/api/practice/sessions" && data) return create(data);
    var m = /^\/api\/practice\/sessions\/(\d+)(\/(check|submit))?$/.exec(path);
    if (!m) return fail(404, "Not found.");
    var st = load(), s = st.sessions[m[1]];
    if (!s) return fail(404, "That practice set doesn't exist.");
    if (!m[3]) return Promise.resolve({ session: publicSession(s) });
    return m[3] === "check" ? check(st, s, data || {}) : submit(st, s, data || {});
  }

  window.GraphitePracticeLocal = { call: call };
})();
