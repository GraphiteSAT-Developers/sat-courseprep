/* Graphite SAT rewards, speed rounds, focus sessions and lessons, preview mode only.
   The live site sends these requests to the backend (routes/play.py). With no server, this file answers the same
   requests in the browser and keeps progress in localStorage. The rules and numbers come from the backend through
   GRAPHITE_BANK.play (services/game.py, speed.py, focus.py, lessons.py), so they match the server.
   Leaderboards here show sample players, labeled as such: a preview has no other students. */
(function () {
  "use strict";
  var BANK = window.GRAPHITE_BANK;
  if (!BANK || !BANK.play) return;
  var P = BANK.play, R = P.rules, KEY = "graphite_play_v1", PREVIEW_COINS = 100000;
  var byId = {};
  BANK.items.forEach(function (q) { byId[q.id] = q; });

  function load() {
    var s = null;
    try { s = JSON.parse(localStorage.getItem(KEY)); } catch (e) { /* storage blocked */ }
    if (s && s.events) {
      if (!s.coins100k) {  // previews started before the 100,000-coin start get topped up once
        var gift = 0; s.events.forEach(function (e) { if (e.kind === "gift") gift += e.coins; });
        if (gift < PREVIEW_COINS) s.events.push({ kind: "gift", xp: 0, coins: PREVIEW_COINS - gift, detail: "Preview coins", day: today(), at: now() });
        s.coins100k = true;
      }
      return s;
    }
    return { events: [{ kind: "gift", xp: 0, coins: PREVIEW_COINS, detail: "Preview coins", day: today(), at: now() }],
             badges: {}, inventory: {}, frame: null, title: null, state: null, opt_in: false, nickname: null,
             runs: {}, focus: {}, lessons: {}, nextId: 1, coins100k: true };
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
    // Same as game.streak_from: a streak freeze covers one missed day a week (Monday to Sunday).
    var earned = !!days[on], d = earned ? on : addDays(on, -1), n = 0, frozen = [], weeks = {};
    var monday = function (iso) { var w = (new Date(iso + "T12:00:00Z").getUTCDay() + 6) % 7; return addDays(iso, -w); };
    for (;;) {
      if (days[d]) n++;
      else {
        var wk = monday(d);
        if (weeks[wk] || !days[addDays(d, -1)]) break;
        weeks[wk] = 1; frozen.push(d);
      }
      d = addDays(d, -1);
    }
    return { days: n, today: earned, frozen: frozen, freeze_ready: !weeks[monday(on)] };
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
  function petGear(s) { var a = (s.pets || []).filter(function (x) { return x.active && x.hatched_at; })[0]; return a ? a.gear || null : null; }
  function profile(s) {
    var T = window.GraphiteTheme, av = T ? T.prefs().avatar : { mode: "photo", parts: {} }, look = T ? T.get() : {};
    var drawn = av.mode === "drawn";
    var worn = { frame: s.frame, title: s.title, accent: accent(), theme: look.theme || null, effect: look.effect || "ripple", petgear: petGear(s) };
    function isWorn(i) { return i.kind === "avatar" ? drawn && av.parts[i.slot] === i.value : worn[i.kind] === i.value; }
    var out = summary(s);
    out.badges = R.badges.map(function (b) { return Object.assign({}, b, { earned_at: s.badges[b.key] || null }); });
    out.shop = R.shop.map(function (i) { return Object.assign({}, i, { owned: !!s.inventory[i.key], worn: isWorn(i) }); })
      .concat((R.free || []).map(function (i) { return Object.assign({}, i, { owned: true, worn: isWorn(i) }); }));
    out.frame = s.frame; out.title = s.title;
    out.avatar = { mode: av.mode, parts: av.parts };
    out.ranks = R.ranks; out.streak_coins = Object.keys(R.streak_coins).map(function (d) { return { days: +d, coins: R.streak_coins[d] }; });
    out.earn = R.earn;
    out.recent = s.events.slice(-12).reverse();
    return out;
  }
  // What /api/me would say after a change, so the page can apply it (theme.js setMe).
  function meNow(s) {
    var T = window.GraphiteTheme; if (!T) return null;
    var pr = T.prefs();
    return Object.assign({}, T.me(), { frame: s.frame || null, game_title: s.title || null, appearance: T.get(),
      avatar_drawn: pr.avatar.mode === "drawn" ? pr.avatar.parts : null, prefs: { dashboard: pr.dashboard, study: pr.study, avatar: pr.avatar } });
  }
  var DEFAULT_SLOT = { hat: "none", face: "none", outfit: "tee", backdrop: "solid" };
  function equipLocal(s, kind, value, slot) {
    var T = window.GraphiteTheme;
    var item = R.shop.filter(function (i) { return i.kind === kind && i.value === value; })[0];
    var free = (R.free || []).filter(function (i) { return i.kind === kind && i.value === value; })[0];
    if (value != null && item && !s.inventory[item.key]) return "Buy that in the shop first.";
    if (kind === "frame" || kind === "title") {
      if (value != null && !item) return "That isn't in the shop.";
      s[kind] = value; return null;
    }
    if (kind === "avatar") {
      slot = slot || (item || free || {}).slot;
      if (!DEFAULT_SLOT[slot]) return "Pick something to wear.";
      if (value != null && !item && !free) return "Pick something to wear.";
      var av = T.prefs().avatar, parts = Object.assign({}, av.parts); parts[slot] = value == null ? DEFAULT_SLOT[slot] : value;
      T.setPrefs({ avatar: { mode: "drawn", parts: parts } }); return null;
    }
    if (kind === "effect") { value = value || "none"; if (!item && !free) return "Pick a background."; T.set({ effect: value }); return null; }
    if (kind === "theme") {
      if (T.themes.indexOf(value) < 0) return "Pick a theme.";
      if (T.shopThemes.indexOf(value) > -1 && !s.inventory["theme:" + value]) return "Buy that in the shop first.";
      T.set({ theme: value }); return null;
    }
    if (kind === "accent") {
      if (T.accents.indexOf(value) < 0) return "Pick a color.";
      if (["rose", "blueprint", "ember", "custom"].indexOf(value) > -1 && !s.inventory["accent:" + value]) return "Buy that in the shop first.";
      T.set({ accent: value }); return null;
    }
    if (kind === "petgear") {
      var act = (s.pets || []).filter(function (x) { return x.active && x.hatched_at; })[0];
      if (!act) return "Hatch a pet first.";
      act.gear = value; return null;
    }
    return "That can't be worn.";
  }

  /* ---------- pets (services/pet.py) ---------- */
  var PR = P.pet;
  function petLevel(xp) { var level = 1, need = 60; while (level < PR.max_level && xp >= need) { xp -= need; level++; need = 40 + 20 * level; } return [level, xp, level >= PR.max_level ? null : need]; }
  function petStage(level) { var st = "baby"; PR.stages.forEach(function (x) { if (level >= x.at) st = x.name; }); return st; }
  function petXp(p, total) { return p.hatched_at ? p.banked + (p.active ? total - p.xp_base : 0) : 0; }
  function petOut(p, total) {
    if (!p.hatched_at) { var got = Math.max(0, total - p.egg_base); return { id: p.id, egg: true, progress: Math.min(got, PR.egg_xp), need: PR.egg_xp, ready: got >= PR.egg_xp }; }
    var sp = PR.species.filter(function (x) { return x.key === p.species; })[0] || PR.species[0], xp = petXp(p, total), lv = petLevel(xp);
    return { id: p.id, egg: false, species: sp.key, species_name: sp.name, rarity: sp.rarity, about: sp.about, name: p.name || sp.name, xp: xp,
             level: lv[0], into: lv[1], need: lv[2], stage: petStage(lv[0]), active: !!p.active, gear: p.gear || null, hatched_at: p.hatched_at };
  }
  function petOverview(s) {
    if (!s.pets || !s.pets.length) { s.pets = [{ id: 1, egg_base: totals(s).xp, xp_base: 0, banked: 0, active: false, gear: null, hatched_at: null }]; s.nextPet = 2; }
    var total = totals(s).xp, list = s.pets.map(function (p) { return petOut(p, total); }), d = today();
    var treats = s.events.filter(function (e) { return e.kind === "pet_treat" && e.day === d; }).length;
    var studied = s.events.some(function (e) { return e.day === d && e.xp > 0; });
    return { pets: list, active: list.filter(function (p) { return !p.egg && p.active; })[0] || null, egg: list.filter(function (p) { return p.egg; })[0] || null,
             mood: studied ? "happy" : "sleepy", treats_left: Math.max(0, PR.treats_per_day - treats), rules: PR,
             gear: R.shop.filter(function (i) { return i.kind === "petgear"; }).map(function (i) { return Object.assign({}, i, { owned: !!s.inventory[i.key] }); }) };
  }
  var WEIGHTS = { sketch: 26, inky: 26, hoot: 26, foxel: 9, axel: 9, nova: 4 };
  function petCall(path, data) {
    var s = load(), m, o = petOverview(s), total = totals(s).xp;
    function find(id) { return s.pets.filter(function (p) { return p.id === +id; })[0]; }
    if (path === "/api/pet") { save(s); return ok(o); }
    if ((m = /^\/api\/pet\/(\d+)\/hatch$/.exec(path))) {
      var p = find(m[1]); if (!p) return fail(400, "That pet isn't yours.");
      if (p.hatched_at) return fail(400, "That egg already hatched.");
      if (total - p.egg_base < PR.egg_xp) return fail(400, "Earn " + (PR.egg_xp - (total - p.egg_base)) + " more XP to hatch it.");
      var bag = []; Object.keys(WEIGHTS).forEach(function (k) { for (var i = 0; i < WEIGHTS[k]; i++) bag.push(k); });
      p.species = bag[Math.floor(Math.random() * bag.length)];
      p.hatched_at = now(); p.xp_base = total; p.banked = 0;
      p.active = !s.pets.some(function (x) { return x.active && x.hatched_at && x !== p; });
      var badges = [earnBadge(s, "first_hatch")];
      if (s.pets.filter(function (x) { return x.hatched_at; }).length >= 3) badges.push(earnBadge(s, "pet_parent"));
      var rep = report(s, total, 0, 0, badges), out = { pet: petOut(p, total), reward: rep, overview: petOverview(s) };
      save(s); return ok(out);
    }
    if ((m = /^\/api\/pet\/(\d+)\/active$/.exec(path))) {
      var q = find(m[1]); if (!q || !q.hatched_at) return fail(400, "Hatch it first.");
      s.pets.forEach(function (x) { if (x.active && x !== q) { x.banked = petXp(x, total); x.active = false; } });
      if (!q.active) { q.active = true; q.xp_base = total; }
      save(s); return ok(petOverview(s));
    }
    if ((m = /^\/api\/pet\/(\d+)\/name$/.exec(path))) {
      var r = find(m[1]), name = String((data && data.name) || "").replace(/\s+/g, " ").trim();
      if (!r) return fail(400, "That pet isn't yours.");
      if (!/^[A-Za-z0-9][A-Za-z0-9 '\-]{0,15}$/.test(name)) return fail(400, "Use 1 to 16 letters, numbers or spaces.");
      if (window.GraphiteWords && !window.GraphiteWords.isClean(name)) return fail(400, "Pick a different name.");
      r.name = name; save(s); return ok(petOverview(s));
    }
    if (path === "/api/pet/treat") {
      var act = s.pets.filter(function (x) { return x.active && x.hatched_at; })[0];
      if (!act) return fail(400, "Hatch a pet first.");
      if (!o.treats_left) return fail(400, "That's " + PR.treats_per_day + " treats today. Your pet is full.");
      var t = totals(s); if (t.coins < PR.treat_price) return fail(400, "You need " + (PR.treat_price - t.coins) + " more coins.");
      var before = petLevel(petXp(act, total))[0];
      act.banked += PR.treat_xp;
      s.events.push({ kind: "pet_treat", xp: 0, coins: -PR.treat_price, detail: String(act.id), day: today(), at: now() });
      var po = petOut(act, total), bs = po.level >= 10 ? [earnBadge(s, "best_friends")] : [];
      var res = { pet: po, level_up: po.level > before, reward: report(s, t.xp, 0, -PR.treat_price, bs), overview: petOverview(s) };
      save(s); return ok(res);
    }
    if (path === "/api/pet/egg") {
      if (s.pets.some(function (x) { return !x.hatched_at; })) return fail(400, "Hatch the egg you have first.");
      if (s.pets.length >= PR.max_pets) return fail(400, "You can have up to " + PR.max_pets + " pets.");
      var tt = totals(s); if (tt.coins < PR.egg_price) return fail(400, "You need " + (PR.egg_price - tt.coins) + " more coins.");
      s.pets.push({ id: s.nextPet++, egg_base: tt.xp, xp_base: 0, banked: 0, active: false, gear: null, hatched_at: null });
      s.events.push({ kind: "shop", xp: 0, coins: -PR.egg_price, detail: "pet:egg", day: today(), at: now() });
      var rp = report(s, tt.xp, 0, -PR.egg_price); save(s);
      return ok({ reward: rp, overview: petOverview(s) });
    }
    return fail(404, "Not found.");
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
      if (item.exclusive) return fail(400, "That one can't be bought. Finish its market set to earn it.", "item");
      if (s.inventory[item.key]) return fail(400, "You already have that.", "item");
      var t = totals(s);
      if (t.coins < item.price) return fail(400, "You need " + (item.price - t.coins) + " more coins for that.", "item");
      s.inventory[item.key] = now();
      s.events.push({ kind: "shop", xp: 0, coins: -item.price, detail: item.key, day: today(), at: now() });
      var rep = report(s, t.xp, 0, -item.price, [earnBadge(s, "fresh_look")]);
      save(s); return ok({ reward: rep, profile: profile(s) });
    }
    if (path === "/api/game/equip") {
      var err = equipLocal(s, data && data.kind, data ? data.value : null, data && data.slot);
      if (err) return fail(400, err, "value");
      save(s);
      return ok({ profile: profile(s), user: meNow(s) });
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
  // Grading is lesson-kit.js (the same rules as lessons.right and lessons.grade on the server).
  function gradeSteps(steps, given) { var K = window.GraphiteLessonKit; return K ? K.grade(steps, given) : 0; }
  function startFirst(s, id) { return id !== P.start_lesson && !!lessonById(P.start_lesson) && !s.lessons[P.start_lesson]; }
  function failFirst() { var e = new Error("Start with Desmos hacks. Every other lesson opens after it."); e.status = 409; e.data = { error: e.message, code: "start_first" }; return Promise.reject(e); }
  function lessonById(id) { return LESSONS.filter(function (l) { return l.id === id; })[0]; }
  function lstatus(row) {
    if (!row) return { done: false, stage: 0, mastered: false, due: false, due_on: null, best: null, total: null };
    var mastered = row.stage >= DAYS.length;
    return { done: true, stage: row.stage, mastered: mastered, best: row.best, total: row.total, due_on: row.due_on, due: !!row.due_on && !mastered && row.due_on <= today() };
  }
  // The free plan opens P.free_lessons only (services/lessons.py plan_locked); the plan state is practice-local.js's.
  function lessonLock() {
    var a = window.GraphitePracticeLocal && window.GraphitePracticeLocal.access && window.GraphitePracticeLocal.access();
    return a && a.features && a.features.lessons ? a.features.lessons : { ok: true };
  }
  function planLocked(id, lock) { return (P.free_lessons || []).indexOf(id) < 0 && !(lock || lessonLock()).ok; }
  function failPlan(lock) {
    var verb = lock.reason ? lock.reason + ", so every lesson is locked until it's paid. Fix it on your subscription page." : "Every lesson comes with the " + lock.need_name + " plan and up.";
    var e = new Error(verb); e.status = 402; e.data = { error: e.message, code: "plan_required", lock: lock }; return Promise.reject(e);
  }
  function names(l) { return { domain_name: P.topic_names[l.domain] || l.domain, skill_name: P.topic_names[l.domain + "/" + l.skill] || l.skill }; }
  function lessonsCall(path, data) {
    var s = load(), m;
    if (path === "/api/lessons") {
      var lock = lessonLock(), free = P.free_lessons || [];
      var items = LESSONS.map(function (l) {
        var it = Object.assign({ id: l.id, title: l.title, hook: l.hook, minutes: l.minutes, domain: l.domain, skill: l.skill, steps: l.steps.length, format: l.format || "classic", progress: lstatus(s.lessons[l.id]),
                                 locked: planLocked(l.id, lock), free: free.indexOf(l.id) >= 0 }, names(l));
        if (it.locked) it.progress.due = false;
        return it;
      });
      return ok({ lessons: items, recall_days: DAYS, access: lock, free_lessons: free, start_with: startFirst(s, "") ? P.start_lesson : null, formats: P.lesson_formats, due: items.filter(function (i) { return i.progress.due; }).map(function (i) { return i.id; }),
                  done: items.filter(function (i) { return i.progress.done; }).length, mastered: items.filter(function (i) { return i.progress.mastered; }).length });
    }
    if ((m = /^\/api\/lessons\/([\w-]+)(\/complete)?$/.exec(path))) {
      var l = lessonById(m[1]);
      if (!l) return fail(404, "That lesson doesn't exist.");
      if (startFirst(s, l.id)) return failFirst();
      var lk = lessonLock();
      if (planLocked(l.id, lk)) return failPlan(lk);
      if (!m[2]) return ok({ all_lessons: !!lk.ok, lesson: Object.assign({}, l, names(l), { progress: lstatus(s.lessons[l.id]), recall_days: DAYS, format_rule: (P.lesson_formats || {})[l.format || "classic"] }) });
      data = data || {};
      var kind = data.kind || "lesson", total = (kind === "lesson" ? l.steps : l.recall).length;
      var steps = kind === "lesson" ? l.steps : l.recall, given = Array.isArray(data.answers) ? data.answers : [];
      if (given.length !== steps.length) return fail(400, "Send one answer for each step.");
      var score = gradeSteps(steps, given);  // same grading as lessons.grade
      var row = s.lessons[l.id], xpBefore = totals(s).xp, badges = [], passed = null, xp, coins;
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

  /* ---------- market (services/market.py) ----------
     Same prices, limits and badges as the server. A preview has no other students, so pretend players trade
     in the background (from a seeded random walk) to show how other people's trades move prices. */
  var MK = P.market, MK_ITEMS = MK && MK.items, MK_BY = {}, HALF = MK ? MK.half_life_hours * 3600000 : 1;
  (MK_ITEMS || []).forEach(function (i) { MK_BY[i.key] = i; });
  function mkLimits(it) { var g = Math.log(MK.rarities[it.rarity].growth); return [Math.log(MK.floor) / g, Math.log(MK.ceiling) / g]; }
  function mkDecay(d, since, at) { return d ? d * Math.pow(0.5, Math.max(0, at - since) / HALF) : 0; }
  function mkPrice(it, d) { var l = mkLimits(it); d = Math.min(l[1], Math.max(l[0], d)); return Math.max(1, Math.round(it.base * Math.pow(MK.rarities[it.rarity].growth, d))); }
  function mkSell(p) { return Math.max(1, Math.floor(p * (1 - MK.spread))); }
  function mkClamp(it, d) { var l = mkLimits(it); return Math.min(l[1], Math.max(l[0], d)); }
  function mkState(s) {
    if (!s.market) s.market = { demand: {}, trades: [], holdings: {}, others: {}, simAt: ms() - 7 * 86400000 };
    var m = s.market;
    MK_ITEMS.forEach(function (it) {
      if (!m.demand[it.key]) m.demand[it.key] = { d: 0, ms: 0 };
      if (m.others[it.key] == null) { var sup = MK.rarities[it.rarity].supply; m.others[it.key] = sup ? Math.floor(sup * (0.55 + 0.3 * seeded("held" + it.key)())) : 0; }
    });
    mkSimulate(m);
    return m;
  }
  function mkRecord(m, it, side, price, at, mine) {
    var cur = m.demand[it.key], d = mkDecay(cur.d, cur.ms, at), nd = mkClamp(it, d + (side === "buy" ? 1 : -1));
    m.demand[it.key] = { d: nd, ms: at };
    m.trades.push({ item: it.key, side: side, price: price, demand_after: nd, at_ms: at, mine: !!mine, day: today() });
    return d;
  }
  function mkSimulate(m) {
    var end = ms(), t = Math.max(m.simAt, end - 7 * 86400000), weights = { common: 5, uncommon: 3, rare: 2, legendary: 1 };
    var pool = []; MK_ITEMS.forEach(function (it) { for (var w = 0; w < weights[it.rarity]; w++) pool.push(it); });
    var rnd = seeded("market" + Math.floor(t / 60000));
    while (true) {
      t += Math.round(-Math.log(1 - rnd()) * 25 * 60000);  // about one pretend trade every 25 minutes
      if (t > end) break;
      var it = pool[Math.floor(rnd() * pool.length)];
      // Each item has slow waves of buying and selling, so prices trend instead of jittering.
      var phase = seeded("phase" + it.key)() * 6.28, mood = Math.sin(t / (36 * 3600000) + phase) * 0.35 + Math.sin(t / (9 * 3600000) + 2 * phase) * 0.12;
      var side = rnd() < 0.5 + mood ? "buy" : "sell", sup = MK.rarities[it.rarity].supply, held = m.others[it.key];
      if (side === "sell" && sup && held <= 0) side = "buy";
      if (side === "buy" && sup && held + mkMine(m, it.key) >= sup) side = "sell";
      var cur = m.demand[it.key], p = mkPrice(it, mkDecay(cur.d, cur.ms, t));
      mkRecord(m, it, side, side === "buy" ? p : mkSell(p), t, false);
      if (sup) m.others[it.key] += side === "buy" ? 1 : -1;
    }
    m.simAt = end;
    var cut = end - 8 * 86400000, last = {};
    m.trades = m.trades.filter(function (tr) { if (tr.at_ms >= cut) return true; last[tr.item] = tr; return false; });
    Object.keys(last).forEach(function (k) { m.trades.unshift(last[k]); });  // keep one older trade per item for the charts
    m.trades.sort(function (a, b) { return a.at_ms - b.at_ms; });
  }
  function mkMine(m, key) { var h = m.holdings[key]; return h ? h.qty : 0; }
  function mkHistory(m, key, hours, at) {
    var it = MK_BY[key], end = at || ms(), start = end - hours * 3600000, N = MK.history_points, d = 0, since = start, i = 0, out = [];
    var trades = m.trades.filter(function (t) { return t.item === key; });
    trades.forEach(function (t) { if (t.at_ms <= start) { d = t.demand_after; since = t.at_ms; } });
    trades = trades.filter(function (t) { return t.at_ms > start && t.at_ms <= end; });
    for (var n = 0; n < N; n++) {
      var t = start + Math.floor((end - start) * n / (N - 1));
      while (i < trades.length && trades[i].at_ms <= t) { d = trades[i].demand_after; since = trades[i].at_ms; i++; }
      out.push({ at_ms: t, price: mkPrice(it, mkDecay(d, since, t)) });
    }
    return out;
  }
  function mkItem(m, it, at) {
    var cur = m.demand[it.key], buy = mkPrice(it, mkDecay(cur.d, cur.ms, at)), r = MK.rarities[it.rarity], h = m.holdings[it.key];
    var then = mkHistory(m, it.key, 24, at)[0].price, owned = h ? h.qty : 0;
    return { key: it.key, set: it.set, name: it.name, about: it.about, rarity: it.rarity, rarity_name: r.name, art: it.art,
             glyph: it.glyph || null, color: it.color || null, shape: it.shape || null, tool: it.tool || null, base: it.base, price: buy, sell_price: mkSell(buy),
             change_24h: then ? Math.round((buy - then) / then * 1000) / 10 : 0, supply: r.supply,
             left: r.supply == null ? null : Math.max(0, r.supply - m.others[it.key] - owned), max_hold: r.max_hold,
             owned: owned, avg_cost: owned ? Math.round(h.cost / owned) : null };
  }
  function mkTradesToday(m) { var d = today(); return m.trades.filter(function (t) { return t.mine && t.day === d; }).length; }
  function mkOverview(s) {
    var m = mkState(s), at = ms(), items = MK_ITEMS.map(function (it) { return mkItem(m, it, at); });
    var mine = {}; items.forEach(function (i) { if (i.owned) mine[i.key] = 1; });
    var paid = 0; Object.keys(m.holdings).forEach(function (k) { paid += m.holdings[k].cost; });
    return {
      items: items, sets: MK.sets.map(function (st) {
        var of = MK_ITEMS.filter(function (i) { return i.set === st.key; });
        return { key: st.key, name: st.name, about: st.about, have: of.filter(function (i) { return mine[i.key]; }).length, of: of.length };
      }),
      coins: totals(s).coins, value: items.reduce(function (a, i) { return a + i.owned * i.sell_price; }, 0), paid: paid,
      trades_left: Math.max(0, MK.trades_per_day - mkTradesToday(m)), trades_per_day: MK.trades_per_day,
      activity: m.trades.slice(-12).reverse().map(function (t) { return { item: t.item, name: MK_BY[t.item].name, side: t.side, price: t.price, at_ms: t.at_ms }; }),
      mine: m.trades.filter(function (t) { return t.mine; }).slice(-15).reverse().map(function (t) { return { item: t.item, name: MK_BY[t.item].name, side: t.side, price: t.price, at_ms: t.at_ms }; }),
      set_titles: Object.keys(MK.set_titles || {}).map(function (k) { return { set: k, title: MK.set_titles[k], owned: !!s.inventory["title:set-" + k] }; }),
      rules: MK,
    };
  }
  function marketCall(path, data) {
    var s = load(), m = mkState(s), parts = path.split("?"), clean = parts[0];
    if (clean === "/api/market") { var o = mkOverview(s); save(s); return ok(o); }
    var hm = /^\/api\/market\/([^/]+)\/history$/.exec(clean);
    if (hm) {
      var hrs = (/hours=(\d+)/.exec(parts[1] || "") || [0, "24"])[1];
      if (hrs !== "24" && hrs !== "168") return fail(400, "Pick a day or a week.");
      if (!MK_BY[hm[1]]) return fail(404, "That isn't in the market.");
      save(s); return ok({ key: hm[1], hours: +hrs, points: mkHistory(m, hm[1], +hrs) });
    }
    if (clean === "/api/market/trade") {
      var it = MK_BY[data && data.item], side = data && data.side;
      if (!it || (side !== "buy" && side !== "sell")) return fail(400, "Pick something to buy or sell.", "item");
      if (mkTradesToday(m) >= MK.trades_per_day) return fail(429, "That's " + MK.trades_per_day + " trades today. The market opens again for you tomorrow.");
      var at = ms(), cur = m.demand[it.key], buy = mkPrice(it, mkDecay(cur.d, cur.ms, at)), r = MK.rarities[it.rarity];
      var h = m.holdings[it.key] || { qty: 0, cost: 0 }, t0 = totals(s), badges = [], price;
      if (side === "buy") {
        if (data.price != null && data.price !== buy) return Promise.reject(Object.assign(new Error("The price changed since you looked."), { status: 409, data: { error: "The price changed since you looked.", price: buy } }));
        if (h.qty >= r.max_hold) return fail(400, "You can hold up to " + r.max_hold + " of this one.");
        if (r.supply != null && m.others[it.key] + h.qty >= r.supply) return fail(409, "Sold out. One comes back when someone sells.");
        if (t0.coins < buy) return fail(400, "You need " + (buy - t0.coins) + " more coins for that.");
        price = buy; h.qty += 1; h.cost += price;
      } else {
        price = mkSell(buy);
        if (data.price != null && data.price !== price) return Promise.reject(Object.assign(new Error("The price changed since you looked."), { status: 409, data: { error: "The price changed since you looked.", price: price } }));
        if (h.qty < 1) return fail(400, "You don't have one to sell.");
        var avg = Math.round(h.cost / h.qty); h.qty -= 1; h.cost = Math.max(0, h.cost - avg);
        if (price > avg) badges.push(earnBadge(s, "buy_low"));
      }
      m.holdings[it.key] = h;
      mkRecord(m, it, side, price, at, true);
      s.events.push({ kind: "market_" + side, xp: 0, coins: side === "buy" ? -price : price, detail: it.key, day: today(), at: now() });
      badges.push(earnBadge(s, "market_debut"));
      var unlocked = null;
      if (side === "buy") MK.sets.forEach(function (st) {
        if (!MK_ITEMS.filter(function (i) { return i.set === st.key; }).every(function (i) { return mkMine(m, i.key) > 0; })) return;
        badges.push(earnBadge(s, "collector"));
        if (st.key === it.set && !s.inventory["title:set-" + st.key]) { s.inventory["title:set-" + st.key] = now(); unlocked = MK.set_titles[st.key]; }
      });
      var rep = report(s, t0.xp, 0, side === "buy" ? -price : price, badges);
      var out = { reward: rep, item: mkItem(m, it, ms()), price: price, side: side, unlocked_title: unlocked };
      save(s); return ok(out);
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
    if (clean.indexOf("/api/market") === 0 && MK) return marketCall(path, data);
    if (clean.indexOf("/api/pet") === 0 && PR) return petCall(clean, data);
    if (window.GraphitePracticeLocal) return window.GraphitePracticeLocal.call(path, data, method);
    return fail(404, "Not found.");
  }

  window.GraphitePlayLocal = { call: call, levelCheck: levelCheck, levelFinish: levelFinish, profile: function () { return profile(load()); } };
})();
