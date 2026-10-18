/* Graphite pets: the drawings. GraphitePets.draw({ species, stage, gear, mood, egg, progress }) returns an SVG string.
   Species and rules come from backend/app/services/pet.py; gear from services/cosmetics.py (PETGEAR).
   Stages grow the pet (baby → young → teen → grown → legend). Moods: "happy" (studied today) or "sleepy". */
(function () {
  "use strict";
  var INK = "#1d1a19";
  var SCALE = { baby: 0.68, young: 0.8, teen: 0.9, grown: 1, legend: 1 };

  function eyes(x1, x2, y, r, mood) {
    if (mood === "sleepy") {
      return '<path d="M' + (x1 - r) + " " + y + "q" + r + " " + r * 0.9 + " " + 2 * r + " 0M" + (x2 - r) + " " + y + "q" + r + " " + r * 0.9 + " " + 2 * r + ' 0" fill="none" stroke="' + INK + '" stroke-width="2.2" stroke-linecap="round"/>';
    }
    return '<g class="pet-blink" style="transform-origin:60px ' + y + 'px"><circle cx="' + x1 + '" cy="' + y + '" r="' + r + '" fill="' + INK + '"/><circle cx="' + x2 + '" cy="' + y + '" r="' + r + '" fill="' + INK + '"/>' +
      '<circle cx="' + (x1 + r * 0.35) + '" cy="' + (y - r * 0.35) + '" r="' + r * 0.35 + '" fill="#fff"/><circle cx="' + (x2 + r * 0.35) + '" cy="' + (y - r * 0.35) + '" r="' + r * 0.35 + '" fill="#fff"/></g>';
  }
  function smile(x, y, w) { return '<path d="M' + (x - w) + " " + y + "q" + w + " " + w * 0.8 + " " + 2 * w + ' 0" fill="none" stroke="' + INK + '" stroke-width="2" stroke-linecap="round"/>'; }
  function cheeks(x1, x2, y) { return '<circle cx="' + x1 + '" cy="' + y + '" r="3.2" fill="#ef7fb3" opacity=".55"/><circle cx="' + x2 + '" cy="' + y + '" r="3.2" fill="#ef7fb3" opacity=".55"/>'; }

  // Each species: body art, plus where its head top is (for gear).
  var SPECIES = {
    sketch: { top: 34, draw: function (m, st) {
      var big = st === "grown" || st === "legend";
      return '<path d="M84 86C98 84 104 74 102 64L108 61 101 58C99 72 92 78 82 80Z" fill="#e3b23c"/><path d="M101 58l7 3-6 1Z" fill="#3a3d42"/>' +
        '<path d="M40 64C30 50 34 44 30 38 40 42 44 50 46 58Z" fill="#f5a8c8"' + (big ? ' transform="scale(1.15) translate(-6 -6)"' : "") + '/><path d="M80 64C90 50 86 44 90 38 80 42 76 50 74 58Z" fill="#f5a8c8"' + (big ? ' transform="scale(1.15) translate(-10 -6)"' : "") + '/>' +
        '<ellipse cx="60" cy="80" rx="24" ry="20" fill="#f2c14e"/><ellipse cx="60" cy="86" rx="14" ry="11" fill="#fbe6b4"/>' +
        '<circle cx="60" cy="54" r="20" fill="#f2c14e"/><path d="M48 37l-3-8 8 5ZM72 37l3-8-8 5Z" fill="#e3b23c"/>' +
        eyes(52, 68, 53, 3.4, m) + smile(60, 61, 4) + cheeks(46, 74, 60);
    } },
    inky: { top: 30, draw: function (m) {
      var arms = "";
      [[40, 1], [52, 1], [68, -1], [80, -1]].forEach(function (a) { arms += '<path d="M' + a[0] + " 78q" + (-6 * a[1]) + " 14 " + (2 * a[1]) + " 20 q" + (6 * a[1]) + " 4 " + (8 * a[1]) + ' -3" fill="none" stroke="#7b5ce0" stroke-width="7" stroke-linecap="round"/>'; });
      return arms + '<path d="M34 76C30 40 90 40 86 76Z" fill="#9b7be6"/><ellipse cx="60" cy="76" rx="26" ry="6" fill="#8a6ad8"/>' +
        '<circle cx="45" cy="50" r="3" fill="#c9b5f5"/><circle cx="76" cy="46" r="2.2" fill="#c9b5f5"/><path d="M92 40q4 6 0 9-4-3 0-9Z" fill="#2a2140"/>' +
        eyes(51, 69, 60, 3.6, m) + smile(60, 68, 4) + cheeks(44, 76, 67);
    } },
    hoot: { top: 30, draw: function (m) {
      return '<ellipse cx="60" cy="74" rx="27" ry="28" fill="#9b6b43"/><path d="M36 58l-4-16 12 10ZM84 58l4-16-12 10Z" fill="#7a5233"/>' +
        '<ellipse cx="60" cy="84" rx="16" ry="15" fill="#e8d2b4"/><path d="M52 80l4 3 4-3 4 3 4-3M52 88l4 3 4-3 4 3 4-3" fill="none" stroke="#c9ad8a" stroke-width="1.6"/>' +
        '<path d="M33 74q-6 12 4 22l6-18ZM87 74q6 12-4 22l-6-18Z" fill="#7a5233"/>' +
        '<circle cx="50" cy="60" r="10" fill="#fff8e7" stroke="#d6b98f" stroke-width="2"/><circle cx="70" cy="60" r="10" fill="#fff8e7" stroke="#d6b98f" stroke-width="2"/>' +
        '<path d="M50 50v4M50 66v4M40 60h4M56 60h4M70 50v4M70 66v4M60 60h4M76 60h4" stroke="#d6b98f" stroke-width="1.2"/>' +
        eyes(50, 70, 60, 3.6, m) + '<path d="M57 68l3 5 3-5Z" fill="#f2a33c"/>';
    } },
    foxel: { top: 36, draw: function (m) {
      return '<path d="M80 92c16 2 24-8 22-20-2-10-10-12-14-8M88 64h16M94 64v14M100 64v14" fill="none" stroke="#ec8f58" stroke-width="7" stroke-linecap="round"/>' +
        '<ellipse cx="60" cy="82" rx="22" ry="18" fill="#ec8f58"/><ellipse cx="60" cy="88" rx="12" ry="10" fill="#fff4ea"/>' +
        '<path d="M40 44l2-16 12 12ZM80 44l-2-16-12 12Z" fill="#ec8f58"/><path d="M43 41l1.6-9 6.4 6.4ZM77 41l-1.6-9-6.4 6.4Z" fill="#3a2a22"/>' +
        '<circle cx="60" cy="56" r="20" fill="#ec8f58"/><path d="M44 62q16 16 32 0-4 12-16 12T44 62Z" fill="#fff4ea"/><circle cx="60" cy="64" r="2.6" fill="' + INK + '"/>' +
        eyes(51, 69, 54, 3.2, m) + smile(60, 68, 3);
    } },
    axel: { top: 36, draw: function (m) {
      var gills = "";
      [[-1, 0], [-1, 8], [-1, 16], [1, 0], [1, 8], [1, 16]].forEach(function (g) {
        var x = 60 + g[0] * 22, y = 44 + g[1];
        gills += '<path d="M' + x + " " + y + "q" + g[0] * 12 + " -4 " + g[0] * 16 + ' 2" fill="none" stroke="#ec6f8f" stroke-width="5" stroke-linecap="round"/>';
      });
      return '<path d="M78 90q22 4 26-12" fill="none" stroke="#f5a8c8" stroke-width="9" stroke-linecap="round"/>' +
        '<ellipse cx="60" cy="84" rx="22" ry="15" fill="#f5a8c8"/>' + gills + '<ellipse cx="60" cy="58" rx="24" ry="19" fill="#f5b8d2"/>' +
        eyes(49, 71, 56, 3.2, m) + '<path d="M50 66q10 7 20 0" fill="none" stroke="' + INK + '" stroke-width="2" stroke-linecap="round"/>' + cheeks(44, 76, 63) +
        '<circle cx="48" cy="88" r="2" fill="#ef7fb3"/><circle cx="66" cy="92" r="1.6" fill="#ef7fb3"/>';
    } },
    nova: { top: 30, draw: function (m) {
      return '<g class="pet-glow"><circle cx="60" cy="66" r="34" fill="#f7d774" opacity=".18"/></g>' +
        '<path d="M60 30l9 20 22 2-16 15 5 22-20-11-20 11 5-22-16-15 22-2Z" fill="#f7d774" stroke="#e3a92b" stroke-width="2" stroke-linejoin="round"/>' +
        eyes(53, 67, 62, 3, m) + smile(60, 70, 3.5) + cheeks(47, 73, 69) +
        '<path d="M28 40l2 5 5 2-5 2-2 5-2-5-5-2 5-2Z" fill="#fff" class="pet-twinkle"/><path d="M94 86l1.5 3.5 3.5 1.5-3.5 1.5-1.5 3.5-1.5-3.5-3.5-1.5 3.5-1.5Z" fill="#fff" class="pet-twinkle2"/>';
    } }
  };

  var GEAR = {
    bow: function (t) { return '<g transform="translate(70 ' + (t + 2) + ')"><path d="M0 0l-9-5v10ZM0 0l9-5v10Z" fill="#ec6f8f"/><circle r="2.6" fill="#c94f6f"/></g>'; },
    party: function (t) { return '<g transform="translate(60 ' + t + ')"><path d="M-8 2L0-18 8 2Z" fill="#4f9be0"/><path d="M-5-6h10M-3-11h6" stroke="#f7d774" stroke-width="2"/><circle cy="-19" r="2.4" fill="#ec6f58"/></g>'; },
    scarf: function (t) { return '<path d="M40 ' + (t + 34) + 'q20 9 40 0v6q-20 9-40 0Z" fill="#ec6f58"/><path d="M70 ' + (t + 40) + 'l4 12 6-2-4-11Z" fill="#c94f4f"/>'; },
    shades: function (t) { return '<g fill="' + INK + '"><rect x="44" y="' + (t + 16) + '" width="13" height="8" rx="3"/><rect x="63" y="' + (t + 16) + '" width="13" height="8" rx="3"/><rect x="56" y="' + (t + 18) + '" width="8" height="2"/></g>'; },
    tinycrown: function (t) { return '<g transform="translate(60 ' + t + ')"><path d="M-10 2l1-10 5 5 4-8 4 8 5-5 1 10Z" fill="#e3a92b" stroke="#a8760f"/><circle cy="-2" r="1.6" fill="#ec6f58"/></g>'; },
    wings: function () { return '<g class="pet-flap"><path d="M34 70C14 60 10 44 22 40 26 52 32 58 40 62Z" fill="#c9e7ff" opacity=".85"/><path d="M86 70C106 60 110 44 98 40 94 52 88 58 80 62Z" fill="#c9e7ff" opacity=".85"/></g>'; }
  };

  function egg(progress) {
    var crack = progress >= 0.5 ? '<path d="M44 66l6 5 5-6 6 6 5-5 7 6" fill="none" stroke="#8a7a5a" stroke-width="2" stroke-linejoin="round"/>' : "";
    var crack2 = progress >= 0.85 ? '<path d="M52 48l4 4-3 4 4 4" fill="none" stroke="#8a7a5a" stroke-width="2"/>' : "";
    return '<ellipse cx="60" cy="102" rx="22" ry="4" fill="#000" opacity=".18"/><g class="' + (progress >= 1 ? "egg-ready" : "egg-rock") + '" style="transform-origin:60px 100px">' +
      '<path d="M60 26C40 26 32 60 32 74c0 16 12 26 28 26s28-10 28-26C88 60 80 26 60 26Z" fill="#fff4dc" stroke="#e2cfa3" stroke-width="2"/>' +
      '<circle cx="48" cy="58" r="5" fill="#f2c14e" opacity=".7"/><circle cx="70" cy="46" r="4" fill="#9fe3c1" opacity=".8"/><circle cx="72" cy="80" r="6" fill="#9cc9f5" opacity=".7"/>' +
      crack + crack2 + "</g>";
  }

  function draw(o) {
    o = o || {};
    var label = o.label || (o.egg ? "An egg" : (o.name || "Your pet"));
    var inner;
    if (o.egg) inner = egg(o.progress || 0);
    else {
      var sp = SPECIES[o.species] || SPECIES.sketch, st = o.stage || "baby", s = SCALE[st] || 1;
      var gear = GEAR[o.gear] ? GEAR[o.gear](sp.top) : "";
      var aura = st === "legend" ? '<circle cx="60" cy="68" r="44" fill="none" stroke="#f7d774" stroke-width="2" stroke-dasharray="3 6" class="pet-aura"/>' : "";
      var zz = o.mood === "sleepy" ? '<g class="pet-zz" fill="#9aa6b5" font-family="Arial, sans-serif" font-weight="700"><text x="86" y="34" font-size="11">z</text><text x="94" y="24" font-size="8">z</text></g>' : "";
      inner = '<ellipse cx="60" cy="104" rx="' + 26 * s + '" ry="4" fill="#000" opacity=".18"/>' + aura +
        '<g class="pet-bob" style="transform-origin:60px 104px"><g transform="translate(' + (60 - 60 * s) + " " + (104 - 104 * s) + ") scale(" + s + ')">' +
        (o.gear === "wings" ? gear : "") + sp.draw(o.mood, st) + (o.gear !== "wings" ? gear : "") + "</g></g>" + zz;
    }
    return '<svg viewBox="0 0 120 120" class="pet-art" role="img" aria-label="' + String(label).replace(/"/g, "&quot;") + '">' + inner + "</svg>";
  }

  window.GraphitePets = { draw: draw, species: Object.keys(SPECIES), gear: Object.keys(GEAR) };
})();
