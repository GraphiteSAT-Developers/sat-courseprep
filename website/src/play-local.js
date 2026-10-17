/* Graphite rewards, speed rounds, focus sessions and lessons, preview mode only.
   The live site sends these requests to the backend (routes/play.py). With no server, this file answers the same
   requests in the browser and keeps progress in localStorage. The rules and numbers come from the backend through
   GRAPHITE_BANK.play (services/game.py, speed.py, focus.py, lessons.py), so they match the server.
   Leaderboards here show sample players, labeled as such: a preview has no other students. */
(function () {
  "use strict";
  var BANK = window.GRAPHITE_BANK;
  if (!BANK || !BANK.play) return;
  var P = BANK.play, R = P.rules, KEY = "graphite_play_v1", PREVIEW_COINS = 500;
  var byId = {};
  BANK.items.forEach(function (q) { byId[q.id] = q; });

  function load() {
    var s = null;
    try { s = JSON.parse(localStorage.getItem(KEY)); } catch (e) { /* storage blocked */ }
    if (s && s.events) return s;
    return { events: [{ kind: "gift", xp: 0, coins: PREVIEW_COINS, detail: "Preview coins", day: today(), at: now() }],
             badges: {}, inventory: {}, frame: null, title: null, state: null, opt_in: false, nickname: null,
             runs: {}, focus: {}, lessons: {}, nextId: 1 };
  }
  function save(s) { try { localStorage.setItem(KEY, JSON.stringify(s)); } catch (e) { /* storage blocked */ } }
  function fail(status, message, field) { var e = new Error(message); e.status = status; e.field = field; e.data = { error: message, field: field }; return Promise.reject(e); }
  function ok(x) { return Promise.resolve(x); }
  function now() { return new Date().toISOString().replace(/\.\d+Z$/, "Z"); }
  function iso(d) { return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0"); }
  function today() { return iso(new Date()); }
  function addDays(dayIso, n) { var p = dayIso.split("-"), d = new Date(+p[0], +p[1] - 1, +p[2]); d.setDate(d.getDate() + n); return iso(d); }
  function ms() { return Date.now(); }

  /* ---------- rewards (services/game.py) ---------- */
  function totals(s) { var x = 0, c = 0; s.events.forEach(function (e) { x += e.xp; c += e.coins; }); return { xp: x, coins: c }; }
  function rankFor(xp) {
    var i = 0; R.ranks.forEach(function (r, n) { if (xp >= r.at) i = n; });
    var out = { n: i + 1, name: R.ranks[i].name, floor: R.ranks[i].at, of: R.ranks.length };
    var nx = R.ranks[i + 1];
    if (nx) { out.next_at = nx.at; out.next_name = nx.name; out.progress = Math.round((xp - out.floor) / (nx.at - out.floor) * 1000) / 1000; }
    else { out.next_at = null; out.next_name = null; out.progress = 1; }
    return out;
  }
  function streak(s, on) {
    on = on || today();
    var days = {}; s.events.forEach(function (e) { if (e.xp > 0) days[e.day] = 1; });
    var earned = !!days[on], d = earned ? on : addDays(on, -1), n = 0;
    while (days[d]) { n++; d = addDays(d, -1); }
    return { days: n, today: earned };
  }
  function badge(key) { return R.badges.filter(function (b) { return b.key === key; })[0]; }
  function earnBadge(s, key) { if (s.badges[key] || !badge(key)) return null; s.badges[key] = now(); return badge(key); }
  function count(s, kind) { return s.events.filter(function (e) { return e.kind === kind; }).length; }
  function award(s, kind, xp, coins, detail) {
    var before = streak(s), on = today();
    s.events.push({ kind: kind, xp: xp, coins: coins, detail: detail || null, day: on, at: now() });
    if (xp <= 0 || before.today) return null;
    var days = before.days + 1, out = { days: days, coins: 0, badges: [] };
    var bonus = R.streak_coins[String(days)];
    if (bonus) { s.events.push({ kind: "streak", xp: 0, coins: bonus, detail: days + "-day streak", day: on, at: now() }); out.coins = bonus; }
    [[3, "streak_3"], [7, "streak_7"], [30, "streak_30"]].forEach(function (p) { if (days >= p[0]) { var b = earnBadge(s, p[1]); if (b) out.badges.push(b); } });
    return out;
  }
  function report(s, xpBefore, xp, coins, badges, st, extra) {
    var t = totals(s), rank = rankFor(t.xp);
    var out = { xp: xp, coins: coins, total_xp: t.xp, total_coins: t.coins, rank: rank, rank_up: rank.n > rankFor(xpBefore).n,
                badges: (badges || []).filter(Boolean), streak: st || null };
    if (st) { out.badges = out.badges.concat(st.badges); out.coins += st.coins; }
    Object.keys(extra || {}).forEach(function (k) { out[k] = extra[k]; });
    return out;
  }
  function summary(s) { var t = totals(s); return { xp: t.xp, coins: t.coins, rank: rankFor(t.xp), streak: streak(s) }; }
  function accent() { try { return (JSON.parse(localStorage.getItem("graphite_appearance")) || {}).accent || "pencil"; } catch (e) { return "pencil"; } }
  function profile(s) {
    var T = window.GraphiteTheme, av = T && T.prefs().avatar;
    var out = summary(s), worn = { frame: s.frame, title: s.title, accent: accent(), theme: T ? T.get().theme : null, avatar: av && av.mode === "drawn" ? av.parts.acc : null };
    out.badges = R.badges.map(function (b) { return Object.assign({}, b, { earned_at: s.badges[b.key] || null }); });
    out.shop = R.shop.map(function (i) { return Object.assign({}, i, { owned: !!s.inventory[i.key], worn: worn[i.kind] === i.value }); });
    out.frame = s.frame; out.title = s.title;
    out.ranks = R.ranks; out.streak_coins = Object.keys(R.streak_coins).map(function (d) { return { days: +d, coins: R.streak_coins[d] }; });
    out.earn = R.earn;
    out.recent = s.events.slice(-12).reverse();
    return out;
  }

  // Level up hooks, called by practice-local.js (same rules as game.level_check and game.level_finish).
  function levelCheck(session, index, correct, right, total) {
    var s = load(), xpBefore = totals(s).xp, boss = index === total - 1, combo = 0, i = index, badges = [], xp, coins;
    while (i >= 0 && right[i]) { combo++; i--; }
    if (correct) {
      xp = R.xp_right + Math.min(R.combo_cap, R.combo_step * (combo - 1)); coins = R.coins_right;
      if (boss) { xp += R.xp_boss; coins += R.coins_boss; }
      if (combo >= 5) badges.push(earnBadge(s, "on_a_roll"));
    } else { xp = R.xp_miss; coins = 0; }
    var st = award(s, boss && correct ? "boss" : "level_q", xp, coins, "practice-" + session.id + ":" + index);
    if (boss && correct) { badges.push(earnBadge(s, "boss_slayer")); if (count(s, "boss") >= 10) badges.push(earnBadge(s, "boss_hunter")); }
    var out = report(s, xpBefore, xp, coins, badges, st, { combo: correct ? combo : 0, boss: boss, correct: correct });
    save(s); return out;
  }
  function levelFinish(session, level, correct, total, passed, firstClear, top) {
    var s = load(), xpBefore = totals(s).xp, xp = R.xp_level_done, coins = 0, lines = [["Finished the set", R.xp_level_done, 0]];
    var badges = [earnBadge(s, "first_steps")];
    if (passed) {
      xp += R.xp_level_pass; lines.push(["Passed level " + level, R.xp_level_pass, 0]);
      if (firstClear) { xp += R.xp_first_clear; coins += R.coins_first_clear * level; lines.push(["First clear", R.xp_first_clear, R.coins_first_clear * level]); }
      if (level >= 9) badges.push(earnBadge(s, "top_score"));
      if (level === top) badges.push(earnBadge(s, "track_cleared"));
    }
    if (correct === total) { xp += R.xp_perfect; lines.push(["Perfect set", R.xp_perfect, 0]); badges.push(earnBadge(s, "flawless")); }
    var st = award(s, "level_done", xp, coins, "practice-" + session.id);
    var sx = 0, sc = 0, pre = "practice-" + session.id + ":";
    s.events.forEach(function (e) { if ((e.kind === "level_q" || e.kind === "boss") && e.detail && e.detail.indexOf(pre) === 0) { sx += e.xp; sc += e.coins; } });
    lines.unshift(["Answers, combos and the boss", sx, sc]);
    var out = report(s, xpBefore, xp, coins, badges, st, { lines: lines.map(function (l) { return { label: l[0], xp: l[1], coins: l[2] }; }), set_xp: sx + xp, set_coins: sc + coins });
    save(s); return out;
  }

  function gameCall(path, data) {
    var s = load();
    if (path === "/api/game") return ok(profile(s));
    if (path === "/api/game/summary") return ok(summary(s));
    if (path === "/api/game/buy") {
      var item = R.shop.filter(function (i) { return i.key === (data && data.item); })[0];
      if (!item) return fail(400, "That item isn't in the shop.", "item");
      if (s.inventory[item.key]) return fail(400, "You already have that.", "item");
      var t = totals(s);
      if (t.coins < item.price) return fail(400, "You need " + (item.price - t.coins) + " more coins for that.", "item");
      s.inventory[item.key] = now();
      s.events.push({ kind: "shop", xp: 0, coins: -item.price, detail: item.key, day: today(), at: now() });
      var rep = report(s, t.xp, 0, -item.price, [earnBadge(s, "fresh_look")]);
      save(s); return ok({ reward: rep, profile: profile(s) });
    }
    if (path === "/api/game/equip") {
      var kind = data && data.kind, value = data ? data.value : null;
      if (kind !== "frame" && kind !== "title") return fail(400, "You can only wear frames and titles.");
      if (value != null) {
        var it = R.shop.filter(function (i) { return i.kind === kind && i.value === value; })[0];
        if (!it || !s.inventory[it.key]) return fail(400, "Buy that in the shop first.");
      }
      s[kind] = value; save(s);
      return ok({ profile: profile(s) });
    }
    return fail(404, "Not found.");
  }

  /* ---------- speed rounds (services/speed.py) ---------- */
  var SP = P.speed;
  function seeded(str) {  // mulberry32 seeded from a string
    var h = 1779033703 ^ str.length;
    for (var i = 0; i < str.length; i++) { h = Math.imul(h ^ str.charCodeAt(i), 3432918353); h = (h << 13) | (h >>> 19); }
    var a = h >>> 0;
    return function () { a |= 0; a = (a + 0x6D2B79F5) | 0; var t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  }
  function dayItems(day) {
    var pool = BANK.items.filter(function (q) { return q.type === "mc" && (q.difficulty === "easy" || q.difficulty === "medium") && SP.domains.indexOf(q.domain_key) > -1; })
      .map(function (q) { return q.id; }).sort();
    var rnd = seeded("speed:" + day), out = [];
    while (out.length < SP.size) { var id = pool[Math.floor(rnd() * pool.length)]; if (out.indexOf(id) < 0) out.push(id); }
    return out;
  }
  function publicQ(q) { return { id: q.id, type: q.type, stem: q.stem, choices: q.choices, domain: q.domain, skill: q.skill, difficulty: q.difficulty }; }
  function isRight(id, a) { return Number(a) === byId[id].answer; }
  function runResult(r) {
    return { correct: r.correct, total: r.total, raw_ms: r.finished_ms - r.started_ms, misses: r.total - r.correct, score_ms: r.score_ms, ranked: r.ranked };
  }
  function runOut(r) {
    var ans = {};
    Object.keys(r.answers).forEach(function (k) { ans[k] = { answer: r.answers[k], correct: isRight(r.item_ids[k], r.answers[k]), answer_index: byId[r.item_ids[k]].answer }; });
    var out = { id: r.id, day: r.day, ranked: r.ranked, total: r.total, questions: r.item_ids.map(function (id) { return publicQ(byId[id]); }),
      answered: ans, elapsed_ms: Math.min(SP.max_ms, ms() - r.started_ms), finished: r.finished_ms != null, penalty_ms: SP.penalty_ms, max_ms: SP.max_ms };
    if (r.finished_ms != null) out.result = runResult(r);
    return out;
  }
  function finishRun(s, r, t) {
    if (r.finished_ms != null) return null;
    t = Math.min(t || ms(), r.started_ms + SP.max_ms);
    var correct = Object.keys(r.answers).filter(function (k) { return isRight(r.item_ids[k], r.answers[k]); }).length, raw = t - r.started_ms;
    r.finished_ms = t; r.correct = correct; r.score_ms = raw + SP.penalty_ms * (r.total - correct);
    var xpBefore = totals(s).xp, xp = R.xp_speed_done + R.xp_speed_right * correct, coins = r.ranked ? R.coins_speed_done : 0;
    var st = award(s, "speed", xp, coins, "speed-" + r.id), badges = [earnBadge(s, "off_the_line")];
    if (correct === r.total && raw <= SP.lightning_ms) badges.push(earnBadge(s, "lightning"));
    return report(s, xpBefore, xp, coins, badges, st);
  }
  function runsOf(s) { return Object.keys(s.runs).map(function (k) { return s.runs[k]; }); }
  function boardProfile(s) {
    var st = SP.states.filter(function (x) { return x.code === s.state; })[0];
    return { opt_in: !!s.opt_in, nickname: s.nickname, state: s.state, state_name: st ? st.name : null };
  }
  // Sample players so the preview's boards aren't empty. Same for everyone on a given day.
  function samplePlayers(day, period) {
    var rnd = seeded("players:" + (period === "week" ? weekStart(day) : day)), out = [];
    var titles = R.shop.filter(function (i) { return i.kind === "title"; }), frames = R.shop.filter(function (i) { return i.kind === "frame"; });
    var states = ["FL", "FL", "FL", "CA", "TX", "NY", "GA", "FL", "IL", "NJ", "FL", "WA", "OH", "FL", "MA", "AZ", "FL", "NC"];
    for (var i = 0; i < 18; i++) {
      var correct = 7 + Math.floor(rnd() * 4), raw = 70000 + Math.floor(rnd() * 170000);
      out.push({ sample: true, nickname: SP.adjectives[Math.floor(rnd() * SP.adjectives.length)] + " " + SP.nouns[Math.floor(rnd() * SP.nouns.length)] + " " + (10 + Math.floor(rnd() * 90)),
        state: states[i], correct: correct, total: SP.size, raw_ms: raw, score_ms: raw + SP.penalty_ms * (SP.size - correct),
        title: rnd() < 0.35 ? titles[Math.floor(rnd() * titles.length)].value : null, frame: rnd() < 0.4 ? frames[Math.floor(rnd() * frames.length)].value : null,
        avatar: rnd() < 0.6 ? sampleAvatar(rnd) : null });
    }
    return out;
  }
  var AV = { bg: ["sky", "mint", "sun", "rose", "lilac", "slate", "peach", "teal"], skin: ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8"],
    hair: ["none", "short", "curly", "long", "bun", "buzz", "waves", "ponytail"], hair_color: ["black", "brown", "auburn", "blonde", "gray", "blue", "pink", "green"],
    eyes: ["dots", "happy", "wide", "sleepy"], mouth: ["smile", "grin", "flat", "open"], acc: ["none", "none", "glasses", "beanie", "headphones", "crown"],
    shirt: ["pencil", "sky", "mint", "coral", "lilac", "slate", "white", "black"] };
  function sampleAvatar(rnd) { var o = {}; Object.keys(AV).forEach(function (k) { o[k] = AV[k][Math.floor(rnd() * AV[k].length)]; }); return o; }
  function myAvatar() { var T = window.GraphiteTheme, a = T && T.prefs().avatar; return a && a.mode === "drawn" ? a.parts : null; }
  function weekStart(day) { var p = day.split("-"), d = new Date(+p[0], +p[1] - 1, +p[2]); d.setDate(d.getDate() - ((d.getDay() + 6) % 7)); return iso(d); }
  function board(s, scope, period) {
    var day = today(), since = period === "today" ? day : weekStart(day);
    if (scope === "state" && !s.state) return { scope: scope, period: period, needs_state: true, rows: [], you: null };
    var mine = runsOf(s).filter(function (r) { return r.ranked && r.finished_ms != null && r.day >= since && r.day <= day; })
      .sort(function (a, b) { return a.score_ms - b.score_ms; })[0];
    var people = samplePlayers(day, period).filter(function (p) { return scope === "nation" || p.state === s.state; });
    var visible = !!(s.opt_in && s.nickname);
    if (mine && visible) people.push({ you: true, nickname: s.nickname, state: s.state, title: s.title, frame: s.frame, avatar: myAvatar(), correct: mine.correct, total: mine.total, raw_ms: mine.finished_ms - mine.started_ms, score_ms: mine.score_ms });
    people.sort(function (a, b) { return a.score_ms - b.score_ms; });
    var rows = people.slice(0, 25).map(function (p, i) { return Object.assign({ rank: i + 1, day: day }, p); });
    var you = null;
    if (mine) {
      var place = visible ? people.map(function (p) { return !!p.you; }).indexOf(true) + 1 : 1 + people.filter(function (p) { return p.score_ms < mine.score_ms; }).length;
      you = { rank: place, visible: visible, of: people.length + (visible ? 0 : 1), score_ms: mine.score_ms, raw_ms: mine.finished_ms - mine.started_ms, correct: mine.correct, total: mine.total, day: mine.day };
    }
    var stn = SP.states.filter(function (x) { return x.code === s.state; })[0];
    return { scope: scope, period: period, state: scope === "state" ? s.state : null, state_name: scope === "state" && stn ? stn.name : null,
             rows: rows, you: you, players: people.length, sample: true };
  }
  function speedCall(path, data, method) {
    var s = load(), day = today(), m;
    if (path === "/api/speed") {
      var ranked = runsOf(s).filter(function (r) { return r.day === day && r.ranked; })[0];
      var best = runsOf(s).filter(function (r) { return r.ranked && r.finished_ms != null; }).map(function (r) { return r.score_ms; }).sort(function (a, b) { return a - b; })[0];
      return ok({ day: day, size: SP.size, penalty_ms: SP.penalty_ms, max_ms: SP.max_ms,
        ranked_today: !ranked ? null : ranked.finished_ms != null ? runResult(ranked) : { open: true },
        personal_best_ms: best == null ? null : best,
        recent: runsOf(s).filter(function (r) { return r.finished_ms != null; }).sort(function (a, b) { return b.id - a.id; }).slice(0, 5).map(function (r) { return Object.assign(runResult(r), { day: r.day }); }),
        board_profile: boardProfile(s) });
    }
    if (path === "/api/speed/start") {
      var open = runsOf(s).filter(function (r) { return r.day === day && r.finished_ms == null; }).sort(function (a, b) { return b.id - a.id; })[0];
      if (open && ms() - open.started_ms < SP.max_ms) return ok({ run: runOut(open) });
      if (open) finishRun(s, open, open.started_ms + SP.max_ms);
      var isRanked = !runsOf(s).some(function (r) { return r.day === day && r.ranked; });
      var r = { id: s.nextId++, day: day, item_ids: dayItems(day), answers: {}, started_ms: ms(), finished_ms: null, correct: null, total: SP.size, score_ms: null, ranked: isRanked, state: s.state };
      s.runs[r.id] = r; save(s);
      return ok({ run: runOut(r) });
    }
    if ((m = /^\/api\/speed\/runs\/(\d+)(\/(answer|finish))?$/.exec(path))) {
      var run = s.runs[m[1]];
      if (!run) return fail(404, "That speed round doesn't exist.");
      if (!m[3]) return ok({ run: runOut(run) });
      if (m[3] === "finish") { var rep0 = finishRun(s, run); save(s); return ok({ result: runResult(run), reward: rep0 }); }
      if (run.finished_ms != null) return fail(409, "This round is already over.");
      var i = data && data.index;
      if (typeof i !== "number" || i < 0 || i >= run.item_ids.length) return fail(400, "That question isn't in this round.");
      var a = Number(data.answer);
      if (!(a >= 0 && a < byId[run.item_ids[i]].choices.length)) return fail(400, "Choose an answer.", "answer");
      var t = ms();
      if (!(String(i) in run.answers) && t - run.started_ms <= SP.max_ms) run.answers[i] = a;
      var rep = null;
      if (Object.keys(run.answers).length >= run.item_ids.length || t - run.started_ms > SP.max_ms) rep = finishRun(s, run, t);
      save(s);
      var out = { answer: { index: i, correct: isRight(run.item_ids[i], run.answers[i]), answer_index: byId[run.item_ids[i]].answer }, finished: run.finished_ms != null };
      if (out.finished) { out.result = runResult(run); out.reward = rep; }
      return ok(out);
    }
    if (path.indexOf("/api/speed/board") === 0) {
      var q = (path.split("?")[1] || "") + "&" + ((data && data.query) || "");
      var scope = /scope=nation/.test(q) ? "nation" : "state", period = /period=week/.test(q) ? "week" : "today";
      return ok(board(s, scope, period));
    }
    if (path === "/api/speed/nicknames") {
      var names = []; for (var k = 0; k < 4; k++) names.push(SP.adjectives[Math.floor(Math.random() * SP.adjectives.length)] + " " + SP.nouns[Math.floor(Math.random() * SP.nouns.length)] + " " + (10 + Math.floor(Math.random() * 90)));
      return ok({ nicknames: names });
    }
    if (path === "/api/speed/states") return ok({ states: SP.states });
    if (path === "/api/speed/profile") {
      data = data || {};
      if ("state" in data) { if (data.state !== null && !SP.states.some(function (x) { return x.code === data.state; })) return fail(400, "Pick your state.", "state"); }
      if ("nickname" in data) {  // same rules as speed.clean_nickname (the preview has no other students, so none are taken)
        var nk = String(data.nickname || "").trim().replace(/\s+/g, " ");
        if (nk.length < 3 || nk.length > 20) return fail(400, "Nicknames are 3 to 20 characters.", "nickname");
        if (!/^[A-Za-z0-9][A-Za-z0-9 ._'-]*$/.test(nk)) return fail(400, "Use letters, numbers, spaces and . _ ' - only.", "nickname");
        if (window.GraphiteWords && !window.GraphiteWords.isClean(nk)) return fail(400, window.GraphiteWords.message, "nickname");
        data.nickname = nk;
      }
      var nick = "nickname" in data ? data.nickname : s.nickname;
      if (data.opt_in && !nick) return fail(400, "Pick a nickname to show on the leaderboard.", "nickname");
      if ("state" in data) s.state = data.state;
      if ("nickname" in data) s.nickname = data.nickname;
      if ("opt_in" in data) s.opt_in = !!data.opt_in;
      save(s); return ok({ board_profile: boardProfile(s) });
    }
    return fail(404, "Not found.");
  }

  /* ---------- focus (services/focus.py) ---------- */
  var FO = P.focus;
  function labelName(k) { var l = FO.labels.filter(function (x) { return x.key === k; })[0]; return l ? l.name : k; }
  function breakFor(m) { var l = FO.lengths.filter(function (x) { return x.minutes === m; })[0]; return l ? l.break : 5; }
  function focusOut(f) {
    return { id: f.id, minutes: f.minutes, label: f.label, label_name: labelName(f.label), elapsed_ms: ms() - f.started_ms,
             finished: !!f.finished_at, completed: !!f.completed, seconds: f.seconds, break_minutes: breakFor(f.minutes) };
  }
  function focusList(s) { return Object.keys(s.focus).map(function (k) { return s.focus[k]; }); }
  function finishFocus(s, f, completed) {
    if (f.finished_at) return null;
    var planned = f.minutes * 60000, elapsed = ms() - f.started_ms, done = !!completed && elapsed >= planned * FO.finish_share;
    f.finished_at = now(); f.seconds = Math.floor(Math.min(elapsed, planned) / 1000); f.completed = done;
    if (f.seconds < FO.min_credit) return null;
    var xpBefore = totals(s).xp, minutes = Math.floor(f.seconds / 60);
    var xp = done ? R.xp_focus_minute * minutes : Math.floor(R.xp_focus_minute * minutes / 2), coins = done ? R.coins_focus_done : 0;
    var st = award(s, "focus", xp, coins, "focus-" + f.id), badges = [];
    if (done) { badges.push(earnBadge(s, "deep_focus")); if (focusList(s).filter(function (x) { return x.completed; }).length >= 10) badges.push(earnBadge(s, "in_the_zone")); }
    return report(s, xpBefore, xp, coins, badges, st, { completed: done, seconds: f.seconds });
  }
  function focusOverview(s) {
    var d = new Date(), monday = new Date(d.getFullYear(), d.getMonth(), d.getDate() - ((d.getDay() + 6) % 7)), mondayIso = iso(monday);
    var days = [0, 0, 0, 0, 0, 0, 0], week = 0;
    focusList(s).filter(function (f) { return f.finished_at && f.day >= mondayIso; }).forEach(function (f) {
      var p = f.day.split("-"), i = Math.round((new Date(+p[0], +p[1] - 1, +p[2]) - monday) / 86400000);
      if (i >= 0 && i < 7) days[i] += f.seconds || 0;
      if (FO.counted_elsewhere.indexOf(f.label) < 0 && (f.seconds || 0) >= FO.min_credit) week += f.seconds || 0;
    });
    var open = focusList(s).filter(function (f) { return !f.finished_at; }).sort(function (a, b) { return b.id - a.id; })[0];
    if (open && ms() - open.started_ms > open.minutes * 60000 * 3) { finishFocus(s, open, false); open = null; save(s); }
    var goal = 3; try { goal = (JSON.parse(localStorage.getItem("graphite_preview_profile") || "{}").weekly_goal_hours) || 3; } catch (e) { /* storage blocked */ }
    return { lengths: FO.lengths, labels: FO.labels, counted_elsewhere: FO.counted_elsewhere, goal_hours: goal,
      week_seconds: week, week_focus_seconds: days.reduce(function (a, b) { return a + b; }, 0), week_days: days, today_focus_seconds: days[(d.getDay() + 6) % 7],
      sessions_done: focusList(s).filter(function (f) { return f.completed; }).length,
      recent: focusList(s).filter(function (f) { return f.finished_at && (f.seconds || 0) >= FO.min_credit; }).sort(function (a, b) { return b.id - a.id; }).slice(0, 6).map(focusOut),
      open: open ? focusOut(open) : null, streak: streak(s) };
  }
  function focusCall(path, data) {
    var s = load(), m;
    if (path === "/api/focus") { var o = focusOverview(s); save(s); return ok(o); }
    if (path === "/api/focus/start") {
      data = data || {};
      if (!FO.lengths.some(function (l) { return l.minutes === data.minutes; })) return fail(400, "Pick how long to focus.", "minutes");
      if (!FO.labels.some(function (l) { return l.key === data.label; })) return fail(400, "Pick what you're working on.", "label");
      focusList(s).filter(function (f) { return !f.finished_at; }).forEach(function (f) { finishFocus(s, f, false); });
      var f = { id: s.nextId++, minutes: data.minutes, label: data.label, started_ms: ms(), finished_at: null, seconds: null, completed: false, day: today() };
      s.focus[f.id] = f; save(s);
      return ok({ session: focusOut(f) });
    }
    if ((m = /^\/api\/focus\/(\d+)\/finish$/.exec(path))) {
      var row = s.focus[m[1]];
      if (!row) return fail(404, "That focus session doesn't exist.");
      var rep = finishFocus(s, row, data && data.completed);
      save(s);
      return ok({ session: focusOut(row), reward: rep, overview: focusOverview(s) });
    }
    return fail(404, "Not found.");
  }

  /* ---------- lessons (services/lessons.py) ---------- */
  var LESSONS = P.lessons, DAYS = P.recall_days;
  function lessonById(id) { return LESSONS.filter(function (l) { return l.id === id; })[0]; }
  function lstatus(row) {
    if (!row) return { done: false, stage: 0, mastered: false, due: false, due_on: null, best: null, total: null };
    var mastered = row.stage >= DAYS.length;
    return { done: true, stage: row.stage, mastered: mastered, best: row.best, total: row.total, due_on: row.due_on, due: !!row.due_on && !mastered && row.due_on <= today() };
  }
  function names(l) { return { domain_name: P.topic_names[l.domain] || l.domain, skill_name: P.topic_names[l.domain + "/" + l.skill] || l.skill }; }
  function lessonsCall(path, data) {
    var s = load(), m;
    if (path === "/api/lessons") {
      var items = LESSONS.map(function (l) {
        return Object.assign({ id: l.id, title: l.title, hook: l.hook, minutes: l.minutes, domain: l.domain, skill: l.skill, steps: l.steps.length, progress: lstatus(s.lessons[l.id]) }, names(l));
      });
      return ok({ lessons: items, recall_days: DAYS, due: items.filter(function (i) { return i.progress.due; }).map(function (i) { return i.id; }),
                  done: items.filter(function (i) { return i.progress.done; }).length, mastered: items.filter(function (i) { return i.progress.mastered; }).length });
    }
    if ((m = /^\/api\/lessons\/([\w-]+)(\/complete)?$/.exec(path))) {
      var l = lessonById(m[1]);
      if (!l) return fail(404, "That lesson doesn't exist.");
      if (!m[2]) return ok({ lesson: Object.assign({}, l, names(l), { progress: lstatus(s.lessons[l.id]), recall_days: DAYS }) });
      data = data || {};
      var kind = data.kind || "lesson", total = (kind === "lesson" ? l.steps : l.recall).length;
      var score = Math.max(0, Math.min(total, Number(data.score) || 0)), row = s.lessons[l.id], xpBefore = totals(s).xp, badges = [], passed = null, xp, coins;
      if (kind === "lesson") {
        if (row) {
          var replayed = (row.last_recall_at || row.completed_at).slice(0, 10) === today();
          xp = replayed ? 0 : R.xp_lesson_replay; coins = 0; row.best = Math.max(row.best, score); row.last_recall_at = today();
        } else {
          xp = R.xp_lesson_first; coins = R.coins_lesson_first;
          row = s.lessons[l.id] = { completed_at: today(), best: score, total: total, stage: 0, due_on: addDays(today(), DAYS[0]), last_recall_at: null };
          badges.push(earnBadge(s, "recall_rookie"));
        }
      } else {
        if (!row) return fail(400, "Finish the lesson before its recall check.");
        var st0 = lstatus(row);
        passed = score >= Math.ceil(total * P.recall_pass);
        if (!st0.due) { xp = 0; coins = 0; }
        else if (passed) { row.stage += 1; row.due_on = row.stage >= DAYS.length ? null : addDays(today(), DAYS[row.stage]); row.last_recall_at = today(); xp = R.xp_recall_pass; coins = R.coins_recall_pass; }
        else { row.due_on = addDays(today(), 1); row.last_recall_at = today(); xp = R.xp_recall_try; coins = 0; }
      }
      var rows = Object.keys(s.lessons).map(function (k) { return s.lessons[k]; });
      if (rows.filter(function (r) { return r.stage >= DAYS.length; }).length >= 3) badges.push(earnBadge(s, "memory_palace"));
      if (rows.length === LESSONS.length) badges.push(earnBadge(s, "total_recall"));
      var st = xp || coins ? award(s, kind === "lesson" ? "lesson" : "recall", xp, coins, "lesson:" + l.id) : null;
      var rep = report(s, xpBefore, xp, coins, badges, st, { score: score, total: total, passed: passed, progress: lstatus(s.lessons[l.id]) });
      save(s); return ok(rep);
    }
    return fail(404, "Not found.");
  }

  function call(path, data, method) {
    var clean = path.split("?")[0];
    if (clean.indexOf("/api/game") === 0) return gameCall(clean, data);
    if (clean.indexOf("/api/speed/board") === 0) return speedCall(path, data, method);
    if (clean.indexOf("/api/speed") === 0) return speedCall(clean, data, method);
    if (clean.indexOf("/api/focus") === 0) return focusCall(clean, data);
    if (clean.indexOf("/api/lessons") === 0) return lessonsCall(clean, data);
    if (window.GraphitePracticeLocal) return window.GraphitePracticeLocal.call(path, data, method);
    return fail(404, "Not found.");
  }

  window.GraphitePlayLocal = { call: call, levelCheck: levelCheck, levelFinish: levelFinish, profile: function () { return profile(load()); } };
})();
