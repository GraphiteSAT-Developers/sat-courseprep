/* Graphite SAT market: collectibles whose prices move with what every student buys and sells.
   Live: /api/market (backend/app/services/market.py). Preview: the same requests go to play-local.js. */
(function () {
  "use strict";
  if (!document.querySelector(".market-page")) return;
  var R = window.GraphiteRewards, call = R && R.call();
  var API = window.GraphiteAPI, LIVE = !!(API && API.live);
  var data = null, current = null, hours = 24, filter = "all", sort = "set", busy = false;
  var SAVED = "graphite_market_view", WATCH = "graphite_market_watch", watch = {};
  try { watch = JSON.parse(localStorage.getItem(WATCH)) || {}; } catch (e) { /* storage blocked */ }
  function saveWatch() { try { localStorage.setItem(WATCH, JSON.stringify(watch)); } catch (e) { /* storage blocked */ } }
  function $(id) { return document.getElementById(id); }
  function esc(s) { return R.esc(s); }
  function num(n) { return R.num(n); }
  function coins(n) { return '<i class="coin" aria-hidden="true"></i>' + num(n); }
  function showError(m) { $("mk-error").textContent = m || ""; $("mk-error").hidden = !m; }
  function failed(err, fallback) {
    if (err && err.status === 401) { location.href = "/signin.html?next=/market.html"; return; }
    showError(err && err.status ? err.message : fallback);
  }
  if (!LIVE) $("mk-preview-note").hidden = false;
  if (!call) { $("mk-loading").textContent = "The market isn't available in this preview."; return; }
  try { var v = JSON.parse(localStorage.getItem(SAVED)) || {}; filter = v.filter || filter; sort = v.sort || sort; } catch (e) { /* storage blocked */ }
  function remember() { try { localStorage.setItem(SAVED, JSON.stringify({ filter: filter, sort: sort })); } catch (e) { /* storage blocked */ } }

  /* ---------- art ---------- */
  function pencil(color) {
    return '<svg viewBox="0 0 64 64" aria-hidden="true" focusable="false"><g transform="rotate(-40 32 32)">' +
      '<rect x="14" y="26" width="30" height="12" fill="' + esc(color) + '"/>' +
      '<rect x="14" y="26" width="30" height="4" fill="#ffffff" opacity="0.18"/>' +
      '<rect x="8" y="26" width="6" height="12" fill="#b9bec6"/><rect x="2" y="26" width="6" height="12" rx="2" fill="#f09ab0"/>' +
      '<path d="M44 26 L56 32 L44 38 Z" fill="#e8c9a0"/><path d="M52 30 L56 32 L52 34 Z" fill="#2b2f36"/></g></svg>';
  }
  var SHAPE = {
    triangle: '<path d="M32 10L56 52H8Z" fill="#4f9be0" stroke="#2b6cb0" stroke-width="2" stroke-linejoin="round"/>',
    circle: '<circle cx="32" cy="32" r="22" fill="#3fb87f" stroke="#2a8a5c" stroke-width="2"/><circle cx="32" cy="32" r="2" fill="#1d1a19"/><path d="M32 32h22" stroke="#1d1a19" stroke-width="1.6" stroke-dasharray="3 2"/>',
    hexagon: '<path d="M32 8l21 12v24L32 56 11 44V20Z" fill="#f2c14e" stroke="#c99a2a" stroke-width="2" stroke-linejoin="round"/>',
    star: '<path d="M32 7l7.6 15.4 17 2.5-12.3 12 2.9 16.9L32 46l-15.2 7.8 2.9-16.9-12.3-12 17-2.5Z" fill="#ec6f58" stroke="#b84a36" stroke-width="2" stroke-linejoin="round"/>',
    cube: '<path d="M32 8l22 12v24L32 56 10 44V20Z" fill="#9b7be6"/><path d="M32 32L10 20 32 8 54 20Z" fill="#c4a8ff"/><path d="M32 32v24L54 44V20Z" fill="#7a5cc6"/>',
    spiral: '<path d="M33 33a2 2 0 0 1-2-2 3 3 0 0 1 3-3 5 5 0 0 1 5 5 8 8 0 0 1-8 8 13 13 0 0 1-13-13 21 21 0 0 1 21-21" fill="none" stroke="#e3a92b" stroke-width="3" stroke-linecap="round"/>'
  };
  var TOOL = {
    abacus: '<rect x="10" y="12" width="44" height="40" rx="3" fill="none" stroke="#8a5636" stroke-width="3"/><g stroke="#8a5636" stroke-width="1.4"><path d="M12 22h40M12 32h40M12 42h40"/></g><g fill="#ec6f58"><circle cx="18" cy="22" r="3"/><circle cx="25" cy="22" r="3"/><circle cx="42" cy="32" r="3"/><circle cx="35" cy="32" r="3"/><circle cx="20" cy="42" r="3"/></g><g fill="#4f9be0"><circle cx="46" cy="22" r="3"/><circle cx="28" cy="42" r="3"/><circle cx="46" cy="42" r="3"/></g>',
    protractor: '<path d="M8 46a24 24 0 0 1 48 0Z" fill="#9cc9f5" fill-opacity=".55" stroke="#2b6cb0" stroke-width="2"/><g stroke="#2b6cb0" stroke-width="1.2"><path d="M32 46V26M32 46l14-14M32 46l-14-14M32 46h20M32 46H12"/></g><circle cx="32" cy="46" r="2" fill="#2b6cb0"/>',
    sliderule: '<rect x="6" y="22" width="52" height="20" rx="2" fill="#efe6d2" stroke="#8a7a5a" stroke-width="1.6"/><rect x="6" y="29" width="52" height="6" fill="#e2d6b8"/><g stroke="#6b5c3e" stroke-width="1"><path d="M12 22v4M18 22v3M24 22v4M30 22v3M36 22v4M42 22v3M48 22v4M54 22v3M12 42v-4M20 42v-3M28 42v-4M36 42v-3M44 42v-4M52 42v-3"/></g><rect x="26" y="18" width="10" height="28" rx="2" fill="none" stroke="#c94f4f" stroke-width="1.6"/>',
    calculator: '<rect x="14" y="6" width="36" height="52" rx="5" fill="#e3a92b" stroke="#a8760f" stroke-width="2"/><rect x="19" y="11" width="26" height="12" rx="2" fill="#2f3237"/><path d="M21 20l5-5 4 3 6-5 6 4" fill="none" stroke="#9fe3c1" stroke-width="1.4"/><g fill="#a8760f"><rect x="19" y="28" width="7" height="6" rx="1.5"/><rect x="28.5" y="28" width="7" height="6" rx="1.5"/><rect x="38" y="28" width="7" height="6" rx="1.5"/><rect x="19" y="37" width="7" height="6" rx="1.5"/><rect x="28.5" y="37" width="7" height="6" rx="1.5"/><rect x="38" y="37" width="7" height="15" rx="1.5"/><rect x="19" y="46" width="16.5" height="6" rx="1.5"/></g>'
  };
  function art(it, big) {
    if (it.art === "shape" || it.art === "tool") {
      return '<span class="mk-art r-' + esc(it.rarity) + (big ? " is-big" : "") + '" aria-hidden="true"><svg viewBox="0 0 64 64">' + ((it.art === "shape" ? SHAPE[it.shape] : TOOL[it.tool]) || "") + "</svg></span>";
    }
    var inner = it.art === "pencil" ? pencil(it.color)
      : '<span class="mk-glyph' + (String(it.glyph).length > 2 ? " is-long" : "") + '">' + esc(it.glyph) + "</span>";
    return '<span class="mk-art r-' + esc(it.rarity) + (big ? " is-big" : "") + '" aria-hidden="true">' + inner + "</span>";
  }
  function change(pct) {
    if (!pct) return '<span class="mk-chg">No change today</span>';
    var up = pct > 0;
    return '<span class="mk-chg ' + (up ? "is-up" : "is-down") + '">' + (up ? "+" : "−") + Math.abs(pct).toFixed(1) + "%" +
      '<span class="visually-hidden">' + (up ? " up today" : " down today") + "</span></span>";
  }
  function ago(ms) {
    var s = Math.max(0, Math.round((Date.now() - ms) / 1000));
    if (s < 60) return "just now";
    var m = Math.round(s / 60); if (m < 60) return m + " min ago";
    var h = Math.round(m / 60); if (h < 24) return h + (h === 1 ? " hour ago" : " hours ago");
    var d = Math.round(h / 24); return d + (d === 1 ? " day ago" : " days ago");
  }
  function setName(key) { return (data.sets.filter(function (s) { return s.key === key; })[0] || {}).name || ""; }

  /* ---------- list ---------- */
  function renderFilter() {
    var opts = [["all", "All"]].concat(data.sets.map(function (s) { return [s.key, s.name]; })).concat([["mine", "Mine"], ["watch", "Watching"]]);
    $("mk-filter").innerHTML = opts.map(function (o) {
      return '<span><input type="radio" name="mk-filter" id="mk-f-' + o[0] + '" value="' + o[0] + '"' + (filter === o[0] ? " checked" : "") +
        '><label for="mk-f-' + o[0] + '">' + esc(o[1]) + "</label></span>";
    }).join("");
    $("mk-sort").value = sort;
  }
  function sorted() {
    var list = data.items.filter(function (i) { return filter === "all" ? true : filter === "mine" ? i.owned > 0 : filter === "watch" ? watch[i.key] : i.set === filter; });
    var order = data.items.map(function (i) { return i.key; });
    var by = {
      set: function (a, b) { return order.indexOf(a.key) - order.indexOf(b.key); },
      up: function (a, b) { return b.change_24h - a.change_24h; }, down: function (a, b) { return a.change_24h - b.change_24h; },
      high: function (a, b) { return b.price - a.price; }, low: function (a, b) { return a.price - b.price; },
    }[sort] || function () { return 0; };
    return list.slice().sort(by);
  }
  function renderList() {
    var list = sorted();
    $("mk-items").innerHTML = list.length ? list.map(function (it) {
      return '<li><button type="button" class="mk-item' + (current && current.key === it.key ? " is-current" : "") + '" data-item="' + esc(it.key) + '"' +
        (current && current.key === it.key ? ' aria-current="true"' : "") + ">" + art(it) +
        '<span class="mk-item-name"><strong>' + esc(it.name) + (watch[it.key] ? ' <span class="mk-star" aria-label="Watching">★</span>' : "") + '</strong><span class="mk-rarity r-' + esc(it.rarity) + '">' + esc(it.rarity_name) + "</span>" +
        (it.owned ? '<span class="fine">You own ' + it.owned + "</span>" : "") + "</span>" +
        '<span class="mk-item-price"><strong>' + coins(it.price) + "</strong>" + change(it.change_24h) + "</span></button></li>";
    }).join("") : '<li class="fine mk-empty">' + (filter === "watch" ? "Nothing on your watchlist. Open a collectible and press Watch." : "Nothing here yet. Buy something and it shows up under Mine.") + "</li>";
  }

  /* ---------- detail ---------- */
  function chart(points) {
    var W = 320, H = 120, P = 6, prices = points.map(function (p) { return p.price; });
    var lo = Math.min.apply(null, prices), hi = Math.max.apply(null, prices);
    if (hi === lo) { hi += 1; lo = Math.max(0, lo - 1); }
    var xy = points.map(function (p, i) {
      return [P + (W - 2 * P) * i / (points.length - 1), P + (H - 2 * P) * (1 - (p.price - lo) / (hi - lo))];
    });
    var line = xy.map(function (q) { return q[0].toFixed(1) + "," + q[1].toFixed(1); }).join(" ");
    var first = prices[0], last = prices[prices.length - 1];
    var label = "Price chart. " + (hours === 24 ? "Over the last day" : "Over the last week") + " the price went from " + first + " to " + last +
      " coins, between " + Math.min.apply(null, prices) + " and " + Math.max.apply(null, prices) + ".";
    return '<svg viewBox="0 0 ' + W + " " + H + '" preserveAspectRatio="none" role="img" aria-label="' + esc(label) + '">' +
      '<line x1="0" x2="' + W + '" y1="' + (H - 1) + '" y2="' + (H - 1) + '" class="mk-axis"/>' +
      '<polygon class="mk-area" points="' + P + "," + H + " " + line + " " + (W - P) + "," + H + '"/>' +
      '<polyline class="mk-line" points="' + line + '"/>' +
      '<circle class="mk-dot" cx="' + xy[xy.length - 1][0].toFixed(1) + '" cy="' + xy[xy.length - 1][1].toFixed(1) + '" r="3.5"/></svg>' +
      '<div class="mk-chart-scale"><span>' + num(Math.max.apply(null, prices)) + '</span><span>' + num(Math.min.apply(null, prices)) + "</span></div>" +
      '<div class="mk-chart-x fine"><span>' + (hours === 24 ? "24 hours ago" : "7 days ago") + "</span><span>Now</span></div>";
  }
  function loadChart() {
    if (!current) return;
    var key = current.key;
    $("mk-chart-note").textContent = "Loading…";
    call("/api/market/" + encodeURIComponent(key) + "/history?hours=" + hours).then(function (h) {
      if (!current || current.key !== key) return;
      $("mk-chart").innerHTML = chart(h.points);
      $("mk-chart-note").textContent = hours === 24 ? "Last 24 hours" : "Last 7 days";
    }).catch(function () { $("mk-chart-note").textContent = "The chart didn't load."; });
  }
  function renderDetail(keepStatus) {
    var it = current;
    if (!it) return;
    $("mk-d-art").innerHTML = art(it, true);
    $("mk-d-set").textContent = setName(it.set);
    $("mk-d-name").textContent = it.name;
    $("mk-watch").textContent = watch[it.key] ? "★ Watching" : "☆ Watch";
    $("mk-watch").setAttribute("aria-pressed", String(!!watch[it.key]));
    $("mk-d-rarity").className = "mk-rarity r-" + it.rarity;
    $("mk-d-rarity").textContent = it.rarity_name;
    $("mk-d-about").textContent = it.about;
    $("mk-d-price").innerHTML = coins(it.price);
    $("mk-d-change").innerHTML = change(it.change_24h);
    var facts = [["You own", it.owned + " of " + it.max_hold + " allowed"],
                 ["You paid", it.avg_cost != null ? num(it.avg_cost) + " each, on average" : "–"],
                 ["Normal price", num(it.base) + " coins"],
                 ["Left to buy", it.supply == null ? "No limit" : num(it.left) + " of " + num(it.supply)]];
    $("mk-facts").innerHTML = facts.map(function (f) { return "<div><dt>" + f[0] + "</dt><dd>" + esc(f[1]) + "</dd></div>"; }).join("");
    var soldOut = it.supply != null && it.left <= 0, full = it.owned >= it.max_hold, poor = data.coins < it.price, noTrades = data.trades_left <= 0;
    var buy = $("mk-buy"), sell = $("mk-sell");
    buy.innerHTML = soldOut ? "Sold out" : full ? "You have the most allowed" : "Buy for " + coins(it.price);
    buy.disabled = busy || soldOut || full || poor || noTrades;
    buy.title = poor && !soldOut && !full ? "You need " + num(it.price - data.coins) + " more coins" : "";
    sell.innerHTML = "Sell for " + coins(it.sell_price);
    sell.disabled = busy || it.owned < 1 || noTrades;
    if (!keepStatus) { $("mk-status").className = "status"; $("mk-status").textContent = ""; }
  }
  function pick(key, focus) {
    current = data.items.filter(function (i) { return i.key === key; })[0] || data.items[0];
    renderList(); renderDetail(); loadChart();
    if (focus) {
      $("mk-detail").focus({ preventScroll: true });
      if (window.matchMedia("(max-width: 980px)").matches) $("mk-detail").scrollIntoView({ behavior: R.reduceMotion ? "auto" : "smooth", block: "start" });
    }
  }

  /* ---------- the rest ---------- */
  function renderStrip() {
    $("mk-coins").innerHTML = coins(data.coins);
    $("mk-value").innerHTML = coins(data.value);
    var gain = data.value - data.paid;
    $("mk-gain").textContent = !data.paid ? "–" : (gain > 0 ? "+" : gain < 0 ? "−" : "") + num(Math.abs(gain));
    $("mk-gain").className = gain > 0 ? "is-up" : gain < 0 ? "is-down" : "";
    $("mk-left").textContent = data.trades_left + " of " + data.trades_per_day;
    $("mk-strip").hidden = false;
  }
  function renderSets() {
    $("mk-sets").innerHTML = data.sets.map(function (s) {
      var pct = Math.round(s.have / s.of * 100);
      var t = (data.set_titles || []).filter(function (x) { return x.set === s.key; })[0];
      return '<li><div class="mk-set-top"><strong>' + esc(s.name) + '</strong><span class="fine">' + s.have + " of " + s.of + (s.have === s.of ? ", complete" : "") + "</span></div>" +
        (t ? '<p class="fine mk-set-reward">' + (t.owned ? "Earned the " + esc(t.title) + ' title. <a href="rewards.html">Wear it</a>' : "Finish it to earn the " + esc(t.title) + " title.") + "</p>" : "") +
        '<div class="hud-bar" role="progressbar" aria-label="' + esc(s.name) + ' collected" aria-valuemin="0" aria-valuemax="' + s.of + '" aria-valuenow="' + s.have + '"><span style="width:' + pct + '%"></span></div></li>';
    }).join("");
  }
  function renderFeed() {
    $("mk-feed").innerHTML = data.activity.length ? data.activity.map(function (a) {
      return '<li><span class="mk-side-tag is-' + esc(a.side) + '">' + (a.side === "buy" ? "Bought" : "Sold") + "</span><span>" + esc(a.name) + "</span>" +
        "<strong>" + coins(a.price) + '</strong><span class="fine">' + ago(a.at_ms) + "</span></li>";
    }).join("") : '<li class="fine">No trades yet. Yours could be the first.</li>';
  }
  function renderMovers() {
    var moved = data.items.filter(function (i) { return i.change_24h; }).slice().sort(function (a, b) { return Math.abs(b.change_24h) - Math.abs(a.change_24h); }).slice(0, 5);
    $("mk-movers").innerHTML = moved.length ? moved.map(function (i) {
      return '<li><button type="button" data-item="' + esc(i.key) + '">' + art(i) + "<span><strong>" + esc(i.name) + "</strong>" + change(i.change_24h) + "</span><strong>" + coins(i.price) + "</strong></button></li>";
    }).join("") : '<li class="fine">Quiet day. Nothing has moved yet.</li>';
    var mine = data.mine || [];
    $("mk-mine").innerHTML = mine.length ? mine.map(function (a) {
      return '<li><span class="mk-side-tag is-' + esc(a.side) + '">' + (a.side === "buy" ? "Bought" : "Sold") + "</span><span>" + esc(a.name) + "</span>" +
        "<strong>" + coins(a.price) + '</strong><span class="fine">' + ago(a.at_ms) + "</span></li>";
    }).join("") : '<li class="fine">Your trades show up here.</li>';
  }
  function renderHow() {
    var r = data.rules;
    $("mk-how-list").innerHTML = [
      "Every buy raises the price a little for everyone, and every sell lowers it. Rare and legendary collectibles move more.",
      "When nobody trades something, its price drifts back toward normal. Half of any rise or drop fades every " + r.half_life_hours + " hours.",
      "Selling pays " + Math.round(r.spread * 100) + "% less than buying, so buying and selling right away always costs coins. You profit when other students push the price up after you buy.",
      "Prices stay between " + Math.round(r.floor * 100) + "% and " + Math.round(r.ceiling * 100) + "% of normal.",
      "Rare and legendary collectibles have a fixed supply. When they're all owned, they come back only when someone sells.",
      "You can make " + r.trades_per_day + " trades a day. If the price changes while you're deciding, you'll see the new price before anything is bought.",
    ].map(function (t) { return "<li>" + esc(t) + "</li>"; }).join("");
    $("mk-how").hidden = false;
  }
  function render() {
    renderStrip(); renderFilter(); renderSets(); renderFeed(); renderMovers(); renderHow();
    $("mk-loading").hidden = true; $("mk-body").hidden = false;
    var key = current ? current.key : (location.hash.slice(1) || null);
    pick(key);
  }
  function load() {
    return call("/api/market").then(function (o) { data = o; showError(""); render(); })
      .catch(function (err) { $("mk-loading").hidden = true; failed(err, "We couldn't load the market. Try again in a moment."); });
  }

  function status(kind, text) {
    var el = $("mk-status"); el.className = "status is-shown " + kind; el.textContent = text;
  }
  function trade(side) {
    if (!current || busy) return;
    var it = current, shown = side === "buy" ? it.price : it.sell_price;
    busy = true; renderDetail(true);
    call("/api/market/trade", { item: it.key, side: side, price: shown }).then(function (res) {
      busy = false;
      data.items = data.items.map(function (i) { return i.key === res.item.key ? res.item : i; });
      current = res.item;
      // Trades don't earn XP, so only badges pop up (the coins are in the strip and the status line).
      if (res.reward && res.reward.badges && res.reward.badges.length) R.show({ badges: res.reward.badges });
      status("ok", (side === "buy" ? "Bought " : "Sold ") + it.name + " for " + num(res.price) + " coins.");
      if (res.unlocked_title) status("ok", "Set complete! You earned the " + res.unlocked_title + " title. Wear it from your locker.");
      return call("/api/market").then(function (o) { data = o; current = o.items.filter(function (i) { return i.key === it.key; })[0]; renderStrip(); renderList(); renderSets(); renderFeed(); renderMovers(); renderDetail(true); loadChart(); });
    }).catch(function (err) {
      busy = false;
      if (err && err.status === 401) { failed(err); return; }
      if (err && err.status === 409 && err.data && err.data.price) {
        var key = it.key;
        return call("/api/market").then(function (o) {
          data = o; current = o.items.filter(function (i) { return i.key === key; })[0];
          renderStrip(); renderList(); renderFeed(); renderDetail(true); loadChart();
          status("err", "The price just changed to " + num(err.data.price) + " coins because someone else traded. Nothing was " + (side === "buy" ? "bought" : "sold") + ". Check the new price and try again.");
        });
      }
      renderDetail(true);
      status("err", err && err.status ? err.message : "That didn't go through. Check your connection and try again.");
    });
  }

  $("mk-items").addEventListener("click", function (e) {
    var b = e.target.closest("[data-item]");
    if (b) { pick(b.getAttribute("data-item"), true); try { history.replaceState(null, "", "#" + b.getAttribute("data-item")); } catch (x) { /* fine */ } }
  });
  $("mk-filter").addEventListener("change", function (e) { filter = e.target.value; remember(); renderList(); });
  $("mk-sort").addEventListener("change", function (e) { sort = e.target.value; remember(); renderList(); });
  document.querySelectorAll('input[name="mk-range"]').forEach(function (r) { r.addEventListener("change", function () { hours = +r.value; loadChart(); }); });
  $("mk-buy").addEventListener("click", function () { trade("buy"); });
  $("mk-watch").addEventListener("click", function () {
    if (!current) return;
    if (watch[current.key]) delete watch[current.key]; else watch[current.key] = 1;
    saveWatch(); renderDetail(true); renderList();
  });
  $("mk-movers").addEventListener("click", function (e) { var b = e.target.closest("[data-item]"); if (b) pick(b.getAttribute("data-item"), true); });
  $("mk-sell").addEventListener("click", function () { trade("sell"); });
  load();
  // Prices move while the page is open: refresh every minute when the tab is visible.
  setInterval(function () {
    if (document.hidden || busy || !data) return;
    call("/api/market").then(function (o) {
      data = o; if (current) current = o.items.filter(function (i) { return i.key === current.key; })[0];
      renderStrip(); renderList(); renderFeed(); renderDetail(true);
    }).catch(function () { /* try again next minute */ });
  }, 60000);
})();
