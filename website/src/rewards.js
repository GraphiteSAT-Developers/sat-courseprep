/* Graphite Rewards page: rank, XP, streak, badges and the shop.
   Live: /api/game. Preview: the same requests go to play-local.js. */
(function () {
  "use strict";
  if (!document.querySelector(".rewards-page")) return;
  var R = window.GraphiteRewards, call = R && R.call();
  var esc = R.esc, num = R.num;
  var API = window.GraphiteAPI, LIVE = !!(API && API.live), T = window.GraphiteTheme;
  var data = null, busy = false;
  function $(id) { return document.getElementById(id); }
  function signIn() { location.href = "/signin.html?next=/rewards.html"; }
  if (!LIVE) $("rw-preview-note").hidden = false;
  if (!call) { $("rw-loading").textContent = "Rewards aren't available in this preview."; return; }

  var GLYPH = { first_steps: "1", on_a_roll: "5×", boss_slayer: "B", boss_hunter: "10B", flawless: "10/10", top_score: "9+",
    track_cleared: "10", streak_3: "3d", streak_7: "7d", streak_30: "30d", off_the_line: "GO", lightning: "3:00",
    deep_focus: "25", in_the_zone: "10×", recall_rookie: "R", memory_palace: "3R", total_recall: "8/8", fresh_look: "¢" };
  var KIND = { level_q: "Level up answer", boss: "Boss question", level_done: "Level finished", speed: "Speed round",
    focus: "Focus session", lesson: "Lesson", recall: "Recall check", streak: "Streak reward", shop: "Shop", gift: "Starting coins" };
  var KIND_NAMES = { accent: "Accent colors", frame: "Profile frames", title: "Titles" };

  function day(iso) { if (!iso) return ""; var d = new Date(iso.length === 10 ? iso + "T12:00:00" : iso); return d.toLocaleDateString("en-US", { month: "short", day: "numeric" }); }
  function showError(m) { $("rw-error").textContent = m; $("rw-error").hidden = !m; }

  function render() {
    var g = data;
    R.hud($("rw-hud"), g);
    $("rw-body").hidden = false;
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
    $("rw-badges-panel").hidden = false;

    $("rw-wallet").innerHTML = '<i class="coin" aria-hidden="true"></i><strong>' + num(g.coins) + "</strong> coins";
    var groups = {};
    g.shop.forEach(function (it) { (groups[it.kind] = groups[it.kind] || []).push(it); });
    var me = (T && T.me && T.me()) || {};
    var accentNow = (T && T.get().accent) || "pencil";
    $("rw-shop").innerHTML = ["frame", "title", "accent"].map(function (kind) {
      return '<div class="rw-shop-group"><h3>' + KIND_NAMES[kind] + '</h3><ul class="rw-items">' + groups[kind].map(function (it) {
        var preview = kind === "frame" ? '<span class="avatar avatar-md" data-frame="' + esc(it.value) + '">' + esc(T ? T.initials(me.name || "You") : "Y") + "</span>"
          : kind === "accent" ? '<span class="st-dot rw-swatch" data-swatch="' + esc(it.value) + '"></span>'
          : '<span class="rw-tag" aria-hidden="true">Title</span>';
        var worn = kind === "accent" ? accentNow === it.value : it.worn, action;
        if (!it.owned) action = '<button class="btn ' + (g.coins >= it.price ? "btn-primary" : "btn-quiet") + '" type="button" data-buy="' + esc(it.key) + '"' +
          (g.coins >= it.price ? "" : ' aria-disabled="true"') + '><i class="coin" aria-hidden="true"></i>' + it.price + "</button>";
        else if (worn) action = kind === "accent" ? '<span class="chip">In use</span>' : '<button class="btn btn-quiet" type="button" data-off="' + kind + '">Take off</button>';
        else action = '<button class="btn btn-secondary" type="button" data-wear="' + esc(it.key) + '">' + (kind === "accent" ? "Use it" : "Wear it") + "</button>";
        return '<li class="rw-item' + (it.owned ? " is-owned" : "") + '">' + preview + '<span class="rw-item-copy"><strong>' + esc(it.name) + '</strong><span class="fine">' + esc(it.about) + "</span></span>" + action + "</li>";
      }).join("") + "</ul></div>";
    }).join("");
    $("shop").hidden = false;

    $("rw-recent").innerHTML = g.recent.length ? g.recent.map(function (e) {
      var label = e.kind === "shop" ? "Bought " + ((g.shop.filter(function (i) { return i.key === e.detail; })[0] || {}).name || "an item") : e.kind === "streak" || e.kind === "gift" ? (e.detail || KIND[e.kind]) : KIND[e.kind] || e.kind;
      return "<li><span>" + esc(label) + '</span><span class="fine">' + day(e.at) + "</span><strong>" + (e.xp ? "+" + num(e.xp) + " XP " : "") +
        (e.coins ? (e.coins > 0 ? "+" : "−") + num(Math.abs(e.coins)) + ' <i class="coin" aria-hidden="true"></i>' : "") + "</strong></li>";
    }).join("") : '<li class="pd-empty">Nothing yet. Start a level, a speed round or a lesson.</li>';
    $("rw-recent-panel").hidden = false;
    $("rw-loading").hidden = true;
  }

  function status(kind, title) {
    var el = $("rw-shop-status"); el.className = "status is-shown " + kind; el.textContent = title;
  }
  function wearAccent(value) {
    if (T) T.set({ accent: value });
    if (LIVE) return API.call("/api/me/appearance", { accent: value }, "PATCH");
    return Promise.resolve();
  }
  $("rw-shop").addEventListener("click", function (e) {
    var b = e.target.closest("button"); if (!b || busy) return;
    if (b.getAttribute("aria-disabled") === "true") {
      var it0 = data.shop.filter(function (i) { return i.key === b.getAttribute("data-buy"); })[0];
      status("err", "You need " + (it0.price - data.coins) + " more coins for " + it0.name + ".");
      return;
    }
    var buy = b.getAttribute("data-buy"), wear = b.getAttribute("data-wear"), off = b.getAttribute("data-off");
    var item = data.shop.filter(function (i) { return i.key === (buy || wear); })[0];
    busy = true; b.disabled = true;
    var req;
    if (buy) req = call("/api/game/buy", { item: buy }).then(function (r) { R.show(r.reward); data = Object.assign(data, r.profile); status("ok", "You bought " + item.name + "."); });
    else if (wear && item.kind === "accent") req = wearAccent(item.value).then(function () { status("ok", item.name + " is your accent color now."); });
    else req = call("/api/game/equip", { kind: wear ? item.kind : off, value: wear ? item.value : null }).then(function (r) {
      data = Object.assign(data, r.profile);
      if (T && T.me && T.setMe) { var me = Object.assign({}, T.me(), { frame: data.frame, game_title: data.title }); T.setMe(me); }
      status("ok", wear ? "You're wearing " + item.name + "." : "Taken off.");
    });
    req.catch(function (err) {
      if (err && err.status === 401) { signIn(); return; }
      status("err", err && err.status ? err.message : "That didn't go through. Check your connection and try again.");
    }).then(function () { busy = false; render(); });
  });
  document.addEventListener("graphite:appearance", function () { if (data) render(); });

  Promise.all([call("/api/game"), call("/api/speed").catch(function () { return null; })]).then(function (r) {
    data = r[0];
    data.nickname = r[1] && r[1].board_profile && r[1].board_profile.nickname;
    render();
    if (location.hash === "#shop") $("shop").scrollIntoView();
  }).catch(function (err) {
    if (err && err.status === 401) { signIn(); return; }
    $("rw-loading").textContent = err && err.status === 403 ? "Rewards are for student accounts." : "We couldn't load your rewards. Check your connection and refresh the page.";
  });
})();
