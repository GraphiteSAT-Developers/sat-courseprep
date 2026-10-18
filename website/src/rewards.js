/* Graphite Rewards: the locker (try on, buy and wear cosmetics), the pet, and badges and ranks.
   Live: /api/game and /api/pet. Preview: the same requests go to play-local.js. */
(function () {
  "use strict";
  if (!document.querySelector(".rewards-page")) return;
  var R = window.GraphiteRewards, call = R && R.call();
  var esc = R.esc, num = R.num;
  var API = window.GraphiteAPI, LIVE = !!(API && API.live), T = window.GraphiteTheme, P = window.GraphitePets;
  var data = null, pets = null, busy = false, cat = "hat", show = "all", trying = null, tab = "locker";
  function $(id) { return document.getElementById(id); }
  function signIn() { location.href = "/signin.html?next=/rewards.html"; }
  function coin(n) { return '<i class="coin" aria-hidden="true"></i>' + num(n); }
  if (!LIVE) $("rw-preview-note").hidden = false;
  if (!call) { $("rw-loading").textContent = "Rewards aren't available in this preview."; return; }

  var CATS = [
    { id: "hat", label: "Hats", kind: "avatar", slot: "hat", note: "Hats go on your drawn avatar. Wearing one switches your picture to the drawn avatar." },
    { id: "face", label: "Glasses", kind: "avatar", slot: "face", note: "Glasses, shades and masks for your drawn avatar." },
    { id: "outfit", label: "Outfits", kind: "avatar", slot: "outfit", note: "Outfits use your shirt color from Settings where they can." },
    { id: "backdrop", label: "Backdrops", kind: "avatar", slot: "backdrop", note: "The scene behind your avatar." },
    { id: "frame", label: "Frames", kind: "frame", note: "A ring around your picture, everywhere it shows up." },
    { id: "title", label: "Titles", kind: "title", note: "Shows under your name here and on the leaderboard." },
    { id: "effect", label: "Backgrounds", kind: "effect", note: "The moving background behind every main page." },
    { id: "theme", label: "Themes", kind: "theme", note: "The colors of the whole site." },
    { id: "accent", label: "Colors", kind: "accent", note: "Your accent color for buttons, links and highlights." },
    { id: "petgear", label: "Pet gear", kind: "petgear", note: "Your active pet wears it." }
  ];
  var RARITY = { common: "Common", rare: "Rare", epic: "Epic", legendary: "Legendary" };
  var GLYPH = { first_steps: "1", on_a_roll: "5×", boss_slayer: "B", boss_hunter: "10B", flawless: "10/10", top_score: "9+",
    track_cleared: "10", streak_3: "3d", streak_7: "7d", streak_30: "30d", off_the_line: "GO", lightning: "3:00",
    deep_focus: "25", in_the_zone: "10×", recall_rookie: "R", memory_palace: "3R", total_recall: "All", fresh_look: "¢",
    market_debut: "$", buy_low: "↑", collector: "Set", first_hatch: "Egg", best_friends: "10♥", pet_parent: "3♥" };
  var KIND = { level_q: "Level up answer", boss: "Boss question", level_done: "Level finished", speed: "Speed round",
    focus: "Focus session", lesson: "Lesson", recall: "Recall check", streak: "Streak reward", shop: "Shop", gift: "Starting coins",
    market_buy: "Market", market_sell: "Market", pet_treat: "Pet treat" };
  var EFFECT_ART = {
    none: '<rect width="60" height="40" fill="var(--bg)"/>',
    ripple: '<rect width="60" height="40" fill="var(--bg)"/><g fill="var(--line)"><circle cx="10" cy="10" r="1.4"/><circle cx="22" cy="10" r="1.4"/><circle cx="46" cy="10" r="1.4"/><circle cx="10" cy="30" r="1.4"/><circle cx="50" cy="30" r="1.4"/></g><circle cx="30" cy="20" r="9" fill="none" stroke="var(--accent)" stroke-width="2"/><circle cx="30" cy="20" r="2" fill="var(--accent)"/>',
    dots: '<rect width="60" height="40" fill="var(--bg)"/><g fill="var(--line)"><circle cx="10" cy="10" r="1.6"/><circle cx="25" cy="10" r="1.6"/><circle cx="40" cy="10" r="1.6"/><circle cx="55" cy="10" r="1.6"/><circle cx="10" cy="25" r="1.6"/><circle cx="25" cy="25" r="1.6"/><circle cx="40" cy="25" r="1.6"/><circle cx="55" cy="25" r="1.6"/></g>',
    snow: '<rect width="60" height="40" fill="var(--bg)"/><g fill="#dfe8f2"><circle cx="8" cy="6" r="1.6"/><circle cx="20" cy="18" r="1.2"/><circle cx="34" cy="9" r="2"/><circle cx="48" cy="24" r="1.4"/><circle cx="14" cy="32" r="1.8"/><circle cx="40" cy="34" r="1.2"/><circle cx="54" cy="8" r="1.2"/></g>',
    constellation: '<rect width="60" height="40" fill="var(--bg)"/><path d="M8 30L20 14 34 22 50 8M34 22L44 32" fill="none" stroke="var(--line)" stroke-width="1.2"/><g fill="var(--accent)"><circle cx="8" cy="30" r="1.8"/><circle cx="20" cy="14" r="1.8"/><circle cx="34" cy="22" r="1.8"/><circle cx="50" cy="8" r="1.8"/><circle cx="44" cy="32" r="1.8"/></g>',
    symbols: '<rect width="60" height="40" fill="var(--bg)"/><g fill="var(--line)" font-family="system-ui,sans-serif" font-weight="700"><text x="6" y="16" font-size="12">π</text><text x="26" y="30" font-size="13">Σ</text><text x="44" y="18" font-size="12">√</text></g>',
    waves: '<rect width="60" height="40" fill="var(--bg)"/><path d="M0 22q7.5-8 15 0t15 0 15 0 15 0" fill="none" stroke="var(--line)" stroke-width="2"/><path d="M0 30q7.5-6 15 0t15 0 15 0 15 0" fill="none" stroke="var(--accent)" stroke-width="2"/>',
    fireflies: '<rect width="60" height="40" fill="var(--bg)"/><g fill="var(--accent)"><circle cx="12" cy="12" r="5" opacity=".2"/><circle cx="12" cy="12" r="1.6"/><circle cx="40" cy="26" r="5" opacity=".2"/><circle cx="40" cy="26" r="1.6"/><circle cx="50" cy="10" r="1.2"/></g>',
    warp: '<rect width="60" height="40" fill="var(--bg)"/><g stroke="#dfe8f2" stroke-width="1.2" stroke-linecap="round"><path d="M30 20L6 6M30 20l26-12M30 20L4 30M30 20l24 16M30 20v-18M30 20l-6 18"/></g>'
  };

  function day(iso) { if (!iso) return ""; var d = new Date(iso.length === 10 ? iso + "T12:00:00" : iso); return d.toLocaleDateString("en-US", { month: "short", day: "numeric" }); }
  function status(id, kind, title) { var el = $(id); el.className = "status is-shown " + kind; el.textContent = title; }
  function me() { return (T && T.me && T.me()) || {}; }
  function baseParts() { return (data && data.avatar && data.avatar.parts) || (T && T.prefs().avatar.parts) || {}; }
  function activePet() { return pets && pets.active; }

  /* ---------- the look at the top ---------- */
  function renderHero() {
    var u = me(), parts = Object.assign({}, baseParts()), frame = data.frame, title = data.title;
    if (trying) {
      if (trying.kind === "avatar") parts[trying.slot] = trying.value;
      if (trying.kind === "frame") frame = trying.value;
      if (trying.kind === "title") title = trying.value;
    }
    var drawn = (data.avatar && data.avatar.mode === "drawn") || (trying && trying.kind === "avatar") || !u.avatar_url;
    var el = $("rw-me-avatar");
    if (drawn && T) { el.innerHTML = T.drawAvatar(parts, "Your avatar"); el.classList.add("is-drawn"); }
    else if (T) T.avatar(el, u);
    if (frame) el.setAttribute("data-frame", frame); else el.removeAttribute("data-frame");
    $("rw-me-rank").textContent = "Rank " + data.rank.n + " · " + data.rank.name;
    $("rw-me-name").textContent = data.nickname || u.name || "You";
    $("rw-me-title").textContent = title || "No title yet";
    $("rw-me-title").classList.toggle("is-empty", !title);
    $("rw-me-trying").textContent = trying ? "Trying on: " + trying.name : "";
    var p = activePet(), egg = pets && pets.egg;
    $("rw-pet-mini").innerHTML = P ? (p ? P.draw({ species: p.species, stage: p.stage, gear: p.gear, mood: pets.mood, name: p.name }) +
        '<span><strong>' + esc(p.name) + '</strong><span class="fine">Level ' + p.level + " " + esc(p.species_name) + "</span></span>"
      : egg ? P.draw({ egg: true, progress: egg.progress / egg.need }) + '<span><strong>' + (egg.ready ? "Ready to hatch!" : "Your egg") + '</strong><span class="fine">' + num(egg.progress) + " of " + num(egg.need) + " XP</span></span>" : "") : "";
    $("rw-hero").hidden = false;
  }

  /* ---------- locker ---------- */
  function itemsIn(c) {
    return data.shop.filter(function (it) { return it.kind === c.kind && (!c.slot || it.slot === c.slot) && (show === "all" || it.owned); })
      .sort(function (a, b) { return (a.price || 0) - (b.price || 0); });
  }
  function preview(it) {
    var parts = baseParts();
    if (it.kind === "avatar" && T) { var p = Object.assign({}, parts); p[it.slot] = it.value; return '<span class="rw-av">' + T.drawAvatar(p, "") + "</span>"; }
    if (it.kind === "frame") return '<span class="avatar avatar-md is-drawn" data-frame="' + esc(it.value) + '">' + (T ? T.drawAvatar(parts, "") : "") + "</span>";
    if (it.kind === "title") return '<span class="rw-tag">' + esc(it.value) + "</span>";
    if (it.kind === "effect") return '<svg class="rw-fx" viewBox="0 0 60 40" aria-hidden="true">' + (EFFECT_ART[it.value] || EFFECT_ART.none) + "</svg>";
    if (it.kind === "theme") return '<span class="st-theme-art st-art-' + esc(it.value) + '" aria-hidden="true"><i></i><i></i><i></i></span>';
    if (it.kind === "accent") return '<span class="st-dot rw-swatch' + (it.value === "custom" ? " st-dot-custom" : "") + '" data-swatch="' + esc(it.value) + '"></span>';
    if (it.kind === "petgear" && P) { var a = activePet(); return '<span class="rw-petgear">' + P.draw({ species: a ? a.species : "sketch", stage: "young", gear: it.value, mood: "happy" }) + "</span>"; }
    return "";
  }
  function stateOf(it) {
    var cur = T ? T.get() : {};
    if (it.kind === "theme") return cur.theme === it.value ? "worn" : it.owned ? "owned" : "shop";
    if (it.kind === "accent") return cur.accent === it.value ? "worn" : it.owned ? "owned" : "shop";
    return it.worn ? "worn" : it.owned ? "owned" : "shop";
  }
  function renderCats() {
    $("rw-cats").innerHTML = CATS.map(function (c) {
      var n = data.shop.filter(function (it) { return it.kind === c.kind && (!c.slot || it.slot === c.slot); }).length;
      return '<button type="button" data-cat="' + c.id + '" aria-pressed="' + (c.id === cat) + '"' + (c.id === cat ? ' class="on"' : "") + ">" + esc(c.label) + ' <span class="fine">' + n + "</span></button>";
    }).join("");
  }
  function renderGrid() {
    var c = CATS.filter(function (x) { return x.id === cat; })[0];
    $("rw-cat-note").textContent = c.note;
    var list = itemsIn(c);
    $("rw-grid").innerHTML = list.length ? list.map(function (it) {
      var st = stateOf(it), sel = trying && trying.key === it.key;
      var tag = st === "worn" ? '<span class="rw-state is-worn">' + (it.kind === "theme" || it.kind === "accent" || it.kind === "effect" ? "In use" : "Wearing") + "</span>"
        : st === "owned" ? '<span class="rw-state">' + (it.free ? "Free" : "Owned") + "</span>" : it.exclusive ? '<span class="rw-state">Market set</span>' : '<span class="rw-price">' + coin(it.price) + "</span>";
      return '<li><button type="button" class="rw-tile r-' + esc(it.rarity || "common") + (sel ? " is-trying" : "") + '" data-key="' + esc(it.key) + '" aria-pressed="' + sel + '">' +
        '<span class="rw-tile-art">' + preview(it) + "</span>" +
        '<span class="rw-tile-name">' + esc(it.name) + "</span>" +
        '<span class="rw-tile-meta"><span class="rw-rarity r-' + esc(it.rarity || "common") + '">' + RARITY[it.rarity || "common"] + "</span>" + tag + "</span></button></li>";
    }).join("") : '<li class="fine rw-empty">Nothing here yet. Switch to Everything to see what you can get.</li>';
  }
  function renderPick() {
    var it = trying;
    $("rw-pick").hidden = !it;
    if (!it) return;
    it = data.shop.filter(function (x) { return x.key === it.key; })[0] || it;
    $("rw-pick-name").textContent = it.name + " · " + RARITY[it.rarity || "common"];
    $("rw-pick-about").textContent = it.about || "";
    var st = stateOf(it), html = "";
    if (st === "shop" && it.exclusive) {
      html = '<a class="btn btn-secondary" href="market.html">Finish its set on the market</a>';
    } else if (st === "shop") {
      var short = it.price - data.coins;
      html = '<button class="btn btn-primary" type="button" data-act="buy"' + (short > 0 ? " disabled" : "") + ">Buy and wear for " + coin(it.price) + "</button>" +
        (short > 0 ? '<span class="fine">You need ' + num(short) + " more coins.</span>" : "");
    } else if (st === "owned") {
      html = '<button class="btn btn-primary" type="button" data-act="wear">' + (it.kind === "theme" || it.kind === "accent" || it.kind === "effect" ? "Use it" : "Wear it") + "</button>";
    } else if (it.kind !== "theme" && it.kind !== "accent" && !(it.kind === "avatar" && it.free && (it.value === "tee" || it.value === "solid")) && it.value !== "none") {
      html = '<button class="btn btn-secondary" type="button" data-act="off">Take it off</button>';
    } else {
      html = '<span class="chip chip-quiet">In use</span>';
    }
    if (it.kind === "accent" && it.value === "custom" && st !== "shop") html += ' <a class="btn btn-quiet" href="settings.html#appearance">Pick a color</a>';
    $("rw-pick-actions").innerHTML = html;
  }
  function renderLocker() { renderCats(); renderGrid(); renderPick(); }

  function applyUser(user) {
    if (user && T && T.setMe) T.setMe(user);
  }
  function equip(it, off) {
    var body = { kind: it.kind, value: off ? null : it.value };
    if (it.kind === "avatar") body.slot = it.slot;
    if (off && it.kind === "effect") body.value = "none";
    return call("/api/game/equip", body).then(function (r) {
      data = Object.assign(data, r.profile, { nickname: data.nickname });
      applyUser(r.user);
    });
  }
  $("rw-cats").addEventListener("click", function (e) {
    var b = e.target.closest("[data-cat]"); if (!b) return;
    cat = b.getAttribute("data-cat"); trying = null; renderLocker(); renderHero();
  });
  document.querySelectorAll('input[name="rw-show"]').forEach(function (r) { r.addEventListener("change", function () { show = r.value; renderGrid(); }); });
  $("rw-grid").addEventListener("click", function (e) {
    var b = e.target.closest("[data-key]"); if (!b) return;
    var key = b.getAttribute("data-key");
    trying = trying && trying.key === key ? null : data.shop.filter(function (x) { return x.key === key; })[0];
    renderGrid(); renderPick(); renderHero();
    if (trying && window.matchMedia("(max-width: 700px)").matches) $("rw-pick").scrollIntoView({ block: "nearest" });
  });
  $("rw-pick-actions").addEventListener("click", function (e) {
    var b = e.target.closest("[data-act]"); if (!b || busy || !trying) return;
    var it = data.shop.filter(function (x) { return x.key === trying.key; })[0], act = b.getAttribute("data-act");
    busy = true; b.disabled = true;
    var req = act === "buy"
      ? call("/api/game/buy", { item: it.key }).then(function (r) { R.show(r.reward); data = Object.assign(data, r.profile, { nickname: data.nickname }); return equip(it); })
          .then(function () { status("rw-shop-status", "ok", "It's yours. You're wearing " + it.name + "."); })
      : equip(it, act === "off").then(function () { status("rw-shop-status", "ok", act === "off" ? "Taken off." : it.kind === "theme" || it.kind === "accent" || it.kind === "effect" ? it.name + " is on." : "You're wearing " + it.name + "."); });
    req.catch(function (err) {
      if (err && err.status === 401) { signIn(); return; }
      status("rw-shop-status", "err", err && err.status ? err.message : "That didn't go through. Check your connection and try again.");
    }).then(function () { busy = false; trying = null; renderAll(); });
  });

  /* ---------- pet ---------- */
  function petArt(p, mood) { return P ? P.draw({ species: p.species, stage: p.stage, gear: p.gear, mood: mood, name: p.name }) : ""; }
  function renderPet() {
    if (!pets) return;
    var p = pets.active, egg = pets.egg, r = pets.rules, box = $("rw-pet-main");
    if (p) {
      var pct = p.need ? Math.round(p.into / p.need * 100) : 100;
      box.innerHTML = '<div class="rw-pet-stage">' + petArt(p, pets.mood) + "</div>" +
        '<div class="rw-pet-info"><p class="label">' + esc(p.species_name) + " · " + RARITY[p.rarity] + " · " + esc(p.stage.charAt(0).toUpperCase() + p.stage.slice(1)) + "</p>" +
        '<form class="rw-pet-name" id="rw-pet-name"><label class="visually-hidden" for="rw-pet-name-in">Pet name</label><input id="rw-pet-name-in" maxlength="16" value="' + esc(p.name) + '" autocomplete="off"><button class="btn btn-quiet" type="submit">Rename</button></form>' +
        '<p class="fine">' + esc(p.about) + "</p>" +
        '<div class="rw-pet-level"><strong>Level ' + p.level + "</strong><span class=\"fine\">" + (p.need ? num(p.into) + " of " + num(p.need) + " XP to level " + (p.level + 1) : "Top level") + "</span></div>" +
        '<div class="hud-bar" role="progressbar" aria-label="Progress to the next pet level" aria-valuemin="0" aria-valuemax="100" aria-valuenow="' + pct + '"><span style="width:' + pct + '%"></span></div>' +
        '<p class="fine">' + (pets.mood === "happy" ? esc(p.name) + " is wide awake because you studied today." : esc(p.name) + " is napping. Earn some XP today to wake them up.") + "</p>" +
        '<div class="pd-row"><button class="btn btn-primary" type="button" id="rw-treat"' + (pets.treats_left ? "" : " disabled") + ">Give a treat for " + coin(r.treat_price) + "</button>" +
        '<span class="fine">+' + r.treat_xp + " pet XP · " + pets.treats_left + " left today</span></div></div>";
      $("rw-pet-name").addEventListener("submit", function (e) { e.preventDefault(); petCall("/api/pet/" + p.id + "/name", { name: $("rw-pet-name-in").value }, "Renamed."); });
      $("rw-treat").addEventListener("click", function () { petCall("/api/pet/treat", {}, null); });
    } else if (egg) {
      var pctE = Math.round(egg.progress / egg.need * 100);
      box.innerHTML = '<div class="rw-pet-stage">' + (P ? P.draw({ egg: true, progress: egg.progress / egg.need }) : "") + "</div>" +
        '<div class="rw-pet-info"><p class="label">Your egg</p><h2>' + (egg.ready ? "It's moving. Time to hatch!" : "Study to hatch it") + "</h2>" +
        '<p class="fine">Every XP you earn anywhere warms it up. ' + num(egg.progress) + " of " + num(egg.need) + " XP.</p>" +
        '<div class="hud-bar" role="progressbar" aria-label="Egg warmth" aria-valuemin="0" aria-valuemax="100" aria-valuenow="' + pctE + '"><span style="width:' + pctE + '%"></span></div>' +
        (egg.ready ? '<div class="pd-row"><button class="btn btn-primary" type="button" id="rw-hatch">Hatch it</button></div>' : '<div class="pd-row"><a class="btn btn-secondary" href="levels.html">Earn XP in Level up</a></div>') + "</div>";
      if (egg.ready) $("rw-hatch").addEventListener("click", function () { hatch(egg.id); });
    }
    $("rw-pets").innerHTML = pets.pets.map(function (q) {
      if (q.egg) return '<li><span class="rw-pets-art">' + (P ? P.draw({ egg: true, progress: q.progress / q.need }) : "") + '</span><span><strong>Egg</strong><span class="fine">' + num(q.progress) + " of " + num(q.need) + " XP</span></span>" +
        (q.ready ? '<button class="btn btn-primary" type="button" data-hatch="' + q.id + '">Hatch</button>' : "") + "</li>";
      return '<li class="' + (q.active ? "is-active" : "") + '"><span class="rw-pets-art">' + petArt(q, q.active ? pets.mood : "sleepy") + "</span><span><strong>" + esc(q.name) + '</strong><span class="fine">Level ' + q.level + " " + esc(q.species_name) + "</span></span>" +
        (q.active ? '<span class="chip chip-quiet">Active</span>' : '<button class="btn btn-quiet" type="button" data-active="' + q.id + '">Make active</button>') + "</li>";
    }).join("") + (pets.egg ? "" : '<li class="rw-pets-buy"><button class="btn btn-secondary" type="button" id="rw-buy-egg"' + (data.coins < pets.rules.egg_price ? " disabled" : "") + ">Get a new egg for " + coin(pets.rules.egg_price) + "</button></li>");
    var be = $("rw-buy-egg"); if (be) be.addEventListener("click", function () { petCall("/api/pet/egg", {}, "A new egg! Earn XP to hatch it."); });
    $("rw-pet-rules").innerHTML = [
      "An egg hatches after you earn " + r.egg_xp + " XP anywhere on Graphite.",
      "Your active pet grows with every XP you earn. Treats add a little more, up to " + r.treats_per_day + " a day.",
      "Pets change as they grow: baby, young, teen, grown, and a legend at level " + r.max_level + ".",
      "Some kinds are rare. Nova is the rarest."
    ].map(function (t) { return "<li>" + esc(t) + "</li>"; }).join("");
  }
  function petCall(path, body, done) {
    if (busy) return; busy = true;
    call(path, body).then(function (r) {
      pets = r.overview || r;
      if (r.reward) { R.show(r.reward); data.coins = r.reward.total_coins; }
      if (r.level_up) status("rw-pet-status", "ok", pets.active.name + " grew to level " + pets.active.level + "!");
      else if (done) status("rw-pet-status", "ok", done);
      else if (r.pet) status("rw-pet-status", "ok", "+" + pets.rules.treat_xp + " XP for " + r.pet.name + ".");
    }).catch(function (err) {
      if (err && err.status === 401) { signIn(); return; }
      status("rw-pet-status", "err", err && err.status ? err.message : "That didn't go through. Try again.");
    }).then(function () { busy = false; renderAll(); });
  }
  function hatch(id) {
    if (busy) return; busy = true;
    var stage = $("rw-pet-main").querySelector(".rw-pet-stage"); if (stage) stage.classList.add("is-hatching");
    setTimeout(function () {
      call("/api/pet/" + id + "/hatch", {}).then(function (r) {
        pets = r.overview; R.show(r.reward);
        status("rw-pet-status", "ok", "It's a " + r.pet.species_name + "! " + (r.pet.rarity !== "common" ? "That's a " + r.pet.rarity + " one. " : "") + "Give it a name.");
      }).catch(function (err) { status("rw-pet-status", "err", err && err.status ? err.message : "That didn't hatch. Try again."); })
        .then(function () { busy = false; renderAll(); var n = $("rw-pet-name-in"); if (n) n.focus(); });
    }, R.reduceMotion ? 0 : 900);
  }
  $("rw-pets").addEventListener("click", function (e) {
    var a = e.target.closest("[data-active]"), h = e.target.closest("[data-hatch]");
    if (a) petCall("/api/pet/" + a.getAttribute("data-active") + "/active", {}, "Switched your active pet.");
    if (h) { setTab("pet"); hatch(+h.getAttribute("data-hatch")); }
  });

  /* ---------- badges, ranks, earning, recent ---------- */
  function renderProgress() {
    var g = data;
    $("rw-earn").innerHTML = g.earn.map(function (e) {
      return "<tr><th scope=\"row\">" + esc(e.what) + '</th><td data-label="XP">' + esc(e.xp) + '</td><td data-label="Coins">' + (e.coins ? esc(e.coins) : "–") + "</td></tr>";
    }).join("");
    $("rw-streak-coins").textContent = "Streak rewards: " + g.streak_coins.map(function (s) { return s.days + " days, " + s.coins + " coins"; }).join(" · ") + ".";
    $("rw-ranks").innerHTML = g.ranks.map(function (r, i) {
      var here = i + 1 === g.rank.n, past = i + 1 < g.rank.n;
      return '<li class="' + (here ? "is-current" : past ? "is-past" : "") + '"><span class="rw-rank-n">' + (i + 1) + '</span><span class="rw-rank-name">' + esc(r.name) +
        (here ? ' <span class="chip">You</span>' : "") + '</span><span class="rw-rank-at">' + num(r.at) + " XP</span></li>";
    }).join("");
    var earned = g.badges.filter(function (b) { return b.earned_at; }).length;
    $("rw-badge-count").textContent = earned + " of " + g.badges.length;
    $("rw-badges").innerHTML = g.badges.slice().sort(function (a, b) { return (b.earned_at ? 1 : 0) - (a.earned_at ? 1 : 0); }).map(function (b) {
      return '<li class="rw-badge' + (b.earned_at ? " is-earned" : "") + '"><span class="medal" aria-hidden="true"><span>' + esc(GLYPH[b.key] || b.name.charAt(0)) + "</span></span>" +
        "<span><strong>" + esc(b.name) + "</strong><span class=\"fine\">" + esc(b.how) + "</span></span>" +
        '<span class="rw-badge-when">' + (b.earned_at ? "Earned " + day(b.earned_at) : "Not yet") + "</span></li>";
    }).join("");
    var MARKET = ((window.GRAPHITE_BANK || {}).play || {}).market;
    $("rw-recent").innerHTML = g.recent.length ? g.recent.map(function (e) {
      var mk = e.kind.indexOf("market_") === 0 ? e.name || (((MARKET && MARKET.items) || []).filter(function (i) { return i.key === e.detail; })[0] || {}).name || e.detail : null;
      var item = (g.shop.filter(function (i) { return i.key === e.detail; })[0] || {}).name;
      var label = mk ? (e.kind === "market_buy" ? "Bought " : "Sold ") + mk + " on the market" : e.kind === "shop" ? (e.detail === "pet:egg" ? "Bought a pet egg" : "Bought " + (item || "an item"))
        : e.kind === "streak" || e.kind === "gift" ? (e.detail || KIND[e.kind]) : KIND[e.kind] || e.kind;
      return "<li><span>" + esc(label) + '</span><span class="fine">' + day(e.at) + "</span><strong>" + (e.xp ? "+" + num(e.xp) + " XP " : "") +
        (e.coins ? (e.coins > 0 ? "+" : "−") + num(Math.abs(e.coins)) + ' <i class="coin" aria-hidden="true"></i>' : "") + "</strong></li>";
    }).join("") : '<li class="pd-empty">Nothing yet. Start a level, a speed round or a lesson.</li>';
  }

  /* ---------- tabs ---------- */
  function setTab(t) {
    tab = t;
    ["locker", "pet", "progress"].forEach(function (id) {
      var b = $("tab-" + id); b.setAttribute("aria-selected", String(id === t)); b.tabIndex = id === t ? 0 : -1;
      $(id).hidden = id !== t;
    });
  }
  $("rw-tabs").addEventListener("click", function (e) { var b = e.target.closest("[data-tab]"); if (b) setTab(b.getAttribute("data-tab")); });
  $("rw-tabs").addEventListener("keydown", function (e) {
    var order = ["locker", "pet", "progress"], i = order.indexOf(tab), d = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
    if (!d) return; e.preventDefault(); setTab(order[(i + d + 3) % 3]); $("tab-" + tab).focus();
  });
  $("rw-pet-mini").addEventListener("click", function (e) { e.preventDefault(); setTab("pet"); $("pet").scrollIntoView({ block: "start" }); });

  function renderAll() {
    $("rw-wallet").innerHTML = coin(data.coins) + " coins";
    R.hud($("rw-hud"), data);
    renderHero(); renderLocker(); renderPet(); renderProgress();
    $("rw-tabs").hidden = false; $("rw-loading").hidden = true;
  }
  document.addEventListener("graphite:appearance", function () { if (data) { renderGrid(); renderPick(); } });

  Promise.all([call("/api/game"), call("/api/pet").catch(function () { return null; }), call("/api/speed").catch(function () { return null; })]).then(function (r) {
    data = r[0]; pets = r[1];
    data.nickname = r[2] && r[2].board_profile && r[2].board_profile.nickname;
    var h = location.hash.slice(1);
    setTab(h === "pet" || h === "progress" ? h : "locker");
    if (h === "shop" || h === "locker") setTab("locker");
    renderAll();
  }).catch(function (err) {
    if (err && err.status === 401) { signIn(); return; }
    $("rw-loading").textContent = err && err.status === 403 ? "Rewards are for student accounts." : "We couldn't load your rewards. Check your connection and refresh the page.";
  });
})();
