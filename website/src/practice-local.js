/* Graphite practice, preview mode only.
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
    var o = { id: s.id, mode: s.mode, title: s.title, domain: s.domain, skill: s.skill, minutes: s.minutes, created_at: s.created_at,
      submitted: !!s.submitted_at, questions: s.item_ids.map(function (id) { return publicQ(byId[id]); }), checked: checked };
    if (s.result) o.result = s.result;
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
    if (s.mode !== "topic") return fail(400, "Answers on a practice test are checked when you submit it.");
    if (s.submitted_at) return fail(409, "This set is already finished.");
    var i = Number(data.index);
    if (!(i >= 0 && i < s.item_ids.length)) return fail(400, "That question isn't in this set.");
    var q = byId[s.item_ids[i]], a = cleanAnswer(q, data.answer);
    if (a === null) return fail(400, "Choose or type an answer first.");
    var finished = [];
    if (!(String(i) in s.checked)) { s.checked[i] = a; finished = markSeen(st, [q.id]); save(st); }
    return Promise.resolve({ question: graded(q, i, s.checked[i]), finished: finished });
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
    s.submitted_at = res.submitted_at; s.result = res; save(st);
    return Promise.resolve({ result: res });
  }

  function call(path, data) {
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
