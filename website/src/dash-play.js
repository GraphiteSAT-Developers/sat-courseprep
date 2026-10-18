/* The dashboard's "Play and earn" panel: rank and coins, then today's speed round, lessons, focus and Level up.
   Live: /api/game/summary, /api/speed, /api/lessons, /api/focus, /api/levels. Preview: play-local.js. */
(function () {
  "use strict";
  var box = document.getElementById("dash-play");
  if (!box) return;
  var R = window.GraphiteRewards, call = R && R.call();
  if (!call) return;
  var esc = R.esc;
  function clock(ms) { var s = Math.floor(ms / 1000); return Math.floor(s / 60) + ":" + String(s % 60).padStart(2, "0") + "." + Math.floor((ms % 1000) / 100); }
  function soft(p) { return p.catch(function () { return null; }); }
  Promise.all([call("/api/game/summary"), soft(call("/api/speed")), soft(call("/api/lessons")), soft(call("/api/focus")), soft(call("/api/levels")), soft(call("/api/pet"))]).then(function (r) {
    var g = r[0], sp = r[1], ls = r[2], fo = r[3], lv = r[4], pt = r[5], rank = g.rank, pct = Math.round((rank.progress || 0) * 100);
    // The pet, if there's one (or the egg): a little card that links to it.
    var petBox = document.getElementById("dash-pet"), P = window.GraphitePets;
    if (petBox && pt && P) {
      var a = pt.active, e = pt.egg;
      petBox.innerHTML = a ? P.draw({ species: a.species, stage: a.stage, gear: a.gear, mood: pt.mood, name: a.name }) + '<span><strong>' + esc(a.name) + '</strong><span class="fine">Level ' + a.level + (pt.mood === "happy" ? ", awake and happy" : ", napping until you study") + "</span></span>"
        : e ? P.draw({ egg: true, progress: e.progress / e.need }) + "<span><strong>" + (e.ready ? "Your egg is ready to hatch!" : "Your egg") + '</strong><span class="fine">' + R.num(e.progress) + " of " + R.num(e.need) + " XP to hatch</span></span>" : "";
      petBox.hidden = !(a || e);
    }
    document.getElementById("dash-play-rank").innerHTML =
      '<span class="hud-medal" aria-hidden="true">' + rank.n + '</span><div class="dash-play-xp"><div class="hud-xp-top"><strong>' + esc(rank.name) + " · " + R.num(g.xp) + " XP</strong><span>" +
      (rank.next_at ? R.num(rank.next_at - g.xp) + " XP to " + esc(rank.next_name) : "Top rank") + '</span></div><div class="hud-bar" role="progressbar" aria-label="Progress to the next rank" aria-valuemin="0" aria-valuemax="100" aria-valuenow="' + pct + '"><span style="width:' + pct + '%"></span></div></div>' +
      '<span class="dash-play-coins"><i class="coin" aria-hidden="true"></i><strong>' + R.num(g.coins) + "</strong> coins</span>";
    var rows = [];
    if (sp) {
      var t = sp.ranked_today;
      rows.push(["Speed round", !t ? "Today's 10 questions are waiting. Your first round counts for the leaderboard." : t.open ? "You started today's round. Finish it." : "Today: " + clock(t.score_ms) + ", " + t.correct + " of " + t.total + " right.",
                 "speed.html", !t || t.open ? "Play" : "Leaderboard"]);
    }
    if (ls) {
      var due = ls.lessons.filter(function (l) { return l.progress.due; }), fresh = ls.start_with ? ls.lessons.filter(function (l) { return l.id === ls.start_with; })[0] : ls.lessons.filter(function (l) { return !l.progress.done; })[0];
      if (due.length) rows.push(["Recall check", due.length + (due.length === 1 ? " lesson is" : " lessons are") + " due: " + due[0].title + (due.length > 1 ? " and more" : "") + ".", "lessons.html?lesson=" + encodeURIComponent(due[0].id) + "&mode=recall", "Recall it"]);
      else if (fresh) rows.push(["Lesson", fresh.title + ". " + fresh.minutes + " minutes" + (ls.start_with ? ". Every other lesson opens after it." : ", hands-on the whole way."), "lessons.html?lesson=" + encodeURIComponent(fresh.id), "Start"]);
    }
    if (lv) {
      var m = lv.tracks[0];
      rows.push(["Level up", m.name + ": level " + m.unlocked + " of " + lv.levels + ". Beat the boss question for bonus coins.", "levels.html", "Climb"]);
    }
    if (fo) rows.push(["Focus", Math.round(fo.today_focus_seconds / 60) + " focus minutes today. A 25-minute block earns 25 XP.", "focus.html", "Focus"]);
    document.getElementById("dash-play-list").innerHTML = rows.map(function (x) {
      return '<li><span class="label">' + esc(x[0]) + "</span><span>" + esc(x[1]) + '</span><a class="btn btn-quiet" href="' + esc(x[2]) + '">' + esc(x[3]) + "</a></li>";
    }).join("");
    box.hidden = false;
  }).catch(function () { /* the rest of the dashboard works without it */ });
})();
