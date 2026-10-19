/* Graphite SAT rewards on screen: the XP / rank / streak / coins strip, and the pop-ups after earning something.
   Used by Level up, the practice test (Level up sets), speed rounds, focus sessions, lessons and the rewards page.
   The numbers come from the server (services/game.py) or, in the preview, from play-local.js. */
(function () {
  "use strict";
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function num(n) { return Number(n || 0).toLocaleString("en-US"); }
  var T = window.GraphiteTheme;
  var reduce = T && T.reduceMotion ? T.reduceMotion() : (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);
  // A soft two-note tone for badges and rank-ups, when Settings > Practice defaults > Sounds is on.
  function tone() {
    if (!T || !T.prefs().study.sounds) return;
    try {
      var A = window.AudioContext || window.webkitAudioContext, ctx = new A();
      [[784, 0], [1047, 0.12]].forEach(function (n) {
        var o = ctx.createOscillator(), g = ctx.createGain();
        o.frequency.value = n[0]; o.connect(g); g.connect(ctx.destination);
        g.gain.setValueAtTime(0.0001, ctx.currentTime + n[1]);
        g.gain.exponentialRampToValueAtTime(0.12, ctx.currentTime + n[1] + 0.02);
        g.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + n[1] + 0.35);
        o.start(ctx.currentTime + n[1]); o.stop(ctx.currentTime + n[1] + 0.4);
      });
    } catch (e) { /* no audio */ }
  }

  /* ---------- the strip ---------- */
  function hud(el, s) {
    if (!el || !s) return;
    var r = s.rank, pct = Math.round((r.progress || 0) * 100);
    var next = r.next_at ? num(r.next_at - s.xp) + " XP to " + esc(r.next_name) : "Top rank";
    var st = s.streak || { days: 0, today: false };
    var streakNote = st.days ? (st.today ? "Done for today" : "Earn XP today to keep it") : "Earn XP today to start one";
    // The weekly streak freeze: one missed day a week is covered on its own.
    var yesterday = new Date(); yesterday.setDate(yesterday.getDate() - 1);
    var y = yesterday.getFullYear() + "-" + ("0" + (yesterday.getMonth() + 1)).slice(-2) + "-" + ("0" + yesterday.getDate()).slice(-2);
    if (st.days && (st.frozen || []).indexOf(y) > -1) streakNote = "Freeze covered yesterday. " + streakNote;
    else if (st.days && st.freeze_ready) streakNote += ". Freeze ready";
    el.innerHTML =
      '<div class="hud-rank"><span class="hud-medal" aria-hidden="true">' + r.n + "</span>" +
        '<div><span class="hud-k">Rank ' + r.n + " of " + r.of + "</span><strong>" + esc(r.name) + "</strong></div></div>" +
      '<div class="hud-xp"><div class="hud-xp-top"><strong>' + num(s.xp) + " XP</strong><span>" + next + "</span></div>" +
        '<div class="hud-bar" role="progressbar" aria-label="Progress to the next rank" aria-valuemin="0" aria-valuemax="100" aria-valuenow="' + pct + '"><span style="width:' + pct + '%"></span></div></div>' +
      '<div class="hud-stat' + (st.days && !st.today ? " is-warn" : "") + '"><strong>' + st.days + "</strong><span>day streak</span><em>" + streakNote + "</em></div>" +
      '<div class="hud-stat"><strong><i class="coin" aria-hidden="true"></i>' + num(s.coins) + "</strong><span>coins</span><em><a href=\"rewards.html#shop\">Spend in the shop</a></em></div>";
    el.hidden = false;
  }

  /* ---------- pop-ups ---------- */
  var stack = null;
  function box() {
    if (stack && document.body.contains(stack)) return stack;
    stack = document.createElement("div");
    stack.className = "reward-stack"; stack.setAttribute("aria-live", "polite"); stack.setAttribute("role", "status");
    document.body.appendChild(stack);
    return stack;
  }
  function pop(html, kind, ms) {
    var p = document.createElement("div");
    p.className = "reward-pop" + (kind ? " is-" + kind : "") + (reduce ? " no-motion" : "");
    p.innerHTML = html;
    var b = box();
    b.appendChild(p);
    while (b.children.length > 3) b.removeChild(b.firstChild);  // answering fast shouldn't bury the page
    setTimeout(function () { p.classList.add("is-leaving"); setTimeout(function () { p.remove(); }, reduce ? 0 : 260); }, ms || 3200);
  }
  // reward: {xp, coins, combo, boss, badges, rank_up, rank, streak}
  function show(rw, opts) {
    if (!rw) return;
    opts = opts || {};
    var bits = [];
    if (rw.boss && rw.correct) bits.push("Boss beaten");
    if (rw.combo > 1) bits.push("Combo ×" + rw.combo);
    if (rw.coins > 0) bits.push("+" + rw.coins + (rw.coins === 1 ? " coin" : " coins"));
    if (rw.xp > 0 || bits.length) {
      pop('<strong class="rp-xp">+' + num(rw.xp) + " XP</strong>" + (bits.length ? "<span>" + esc(bits.join(" · ")) + "</span>" : ""),
          rw.boss && rw.correct ? "boss" : "", opts.quick ? 1800 : 2600);
    }
    if (rw.streak && rw.streak.days) {
      pop("<strong>" + rw.streak.days + "-day streak</strong><span>" + (rw.streak.coins ? "+" + rw.streak.coins + " coins for keeping it going" : "You earned XP today. Come back tomorrow to keep it.") + "</span>", "streak", 4200);
    }
    (rw.badges || []).forEach(function (b) {
      pop('<span class="rp-kicker">Badge earned</span><strong>' + esc(b.name) + "</strong><span>" + esc(b.how) + "</span>", "badge", 5200);
    });
    if ((rw.badges && rw.badges.length) || rw.rank_up) tone();
    if (rw.rank_up && rw.rank) pop('<span class="rp-kicker">New rank</span><strong>' + esc(rw.rank.name) + "</strong><span>Rank " + rw.rank.n + " of " + rw.rank.of + "</span>", "rank", 5600);
  }

  // A finished set's breakdown: [{label, xp, coins}]
  function lines(list) {
    return '<ul class="reward-lines">' + (list || []).filter(function (l) { return l.xp || l.coins; }).map(function (l) {
      return "<li><span>" + esc(l.label) + "</span><strong>+" + num(l.xp) + " XP" + (l.coins ? ' <i class="coin" aria-hidden="true"></i>' + l.coins : "") + "</strong></li>";
    }).join("") + "</ul>";
  }

  // The client for the server or, in the preview, play-local.js.
  function caller() {
    var API = window.GraphiteAPI;
    if (API && API.live) return API.call;
    return window.GraphitePlayLocal && window.GraphitePlayLocal.call;
  }

  window.GraphiteRewards = { hud: hud, show: show, lines: lines, esc: esc, num: num, call: caller, reduceMotion: reduce };
})();
