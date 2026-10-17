/* Page background: a faint grid of dots, on every main page (the pages that load this script: home, dashboard,
   practice, plan, Level up, lessons, speed round, focus, rewards and the parent dashboard; not Settings, sign-in,
   checkout, tests or the legal pages). Clicking or tapping anywhere sends a ripple out
   through the dots from that point: they light up pencil-yellow, swell and push outward, then settle.
   It sits behind the panels, never blocks clicks, only animates while a ripple is moving, and stays
   still for people who've asked their device to reduce motion. */
(function () {
  "use strict";
  var host = document.querySelector("main");
  if (!host || !window.requestAnimationFrame) return;

  var SPACING = 26;        // px between dots
  var DOT = 1.1;           // resting dot radius
  var SPEED = 0.62;        // ring growth, px per ms
  var WIDTH = 46;          // ring thickness, px
  var LIFE = 1500;         // ms until a ripple has faded
  var PUSH = 7;            // px a dot moves outward at the ring's peak
  var MAX_RIPPLES = 6;

  var canvas = document.createElement("canvas");
  canvas.className = "ripple-bg";
  canvas.setAttribute("aria-hidden", "true");
  document.body.insertBefore(canvas, document.body.firstChild);
  var ctx = canvas.getContext("2d");
  if (!ctx) return;

  var reduce = window.matchMedia ? window.matchMedia("(prefers-reduced-motion: reduce)") : { matches: false };
  var ripples = [], frame = 0, w = 0, h = 0, dpr = 1, base = [62, 67, 74], hot = [242, 193, 78];
  // The Settings page can turn the effect off (theme.js keeps the choice).
  function enabled() { return !(window.GraphiteTheme && window.GraphiteTheme.get().ripple === false); }

  function rgb(token, fallback) {
    var v = getComputedStyle(document.documentElement).getPropertyValue(token).trim();
    var m = /^#([0-9a-f]{6})$/i.exec(v);
    if (!m) return fallback;
    var n = parseInt(m[1], 16);
    return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
  }

  function size() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    w = window.innerWidth; h = window.innerHeight;
    canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr);
    canvas.style.width = w + "px"; canvas.style.height = h + "px";
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    base = rgb("--line", base); hot = rgb("--accent", hot);
    if (frame) { cancelAnimationFrame(frame); frame = 0; }
    draw(performance.now());
  }

  function draw(now) {
    ctx.clearRect(0, 0, w, h);
    canvas.hidden = !enabled();
    if (canvas.hidden) { ripples = []; frame = 0; return; }
    ripples = ripples.filter(function (r) { return now - r.t < LIFE; });
    var live = ripples.map(function (r) {
      var age = now - r.t;
      return { x: r.x, y: r.y, ring: age * SPEED, fade: 1 - age / LIFE };
    });
    for (var y = SPACING / 2; y < h; y += SPACING) {
      for (var x = SPACING / 2; x < w; x += SPACING) {
        var glow = 0, dx = 0, dy = 0;
        for (var i = 0; i < live.length; i++) {
          var r = live[i], ox = x - r.x, oy = y - r.y, d = Math.sqrt(ox * ox + oy * oy) || 1;
          var off = d - r.ring;
          var k = Math.exp(-(off * off) / (2 * WIDTH * WIDTH / 4)) * r.fade * r.fade;
          if (k < 0.01) continue;
          glow = Math.max(glow, k);
          dx += (ox / d) * k * PUSH; dy += (oy / d) * k * PUSH;
        }
        var c = glow > 0
          ? "rgb(" + Math.round(base[0] + (hot[0] - base[0]) * glow) + "," + Math.round(base[1] + (hot[1] - base[1]) * glow) + "," + Math.round(base[2] + (hot[2] - base[2]) * glow) + ")"
          : "rgb(" + base[0] + "," + base[1] + "," + base[2] + ")";
        ctx.fillStyle = c;
        ctx.globalAlpha = 0.55 + 0.45 * glow;
        ctx.beginPath();
        ctx.arc(x + dx, y + dy, DOT + glow * 1.6, 0, Math.PI * 2);
        ctx.fill();
      }
    }
    ctx.globalAlpha = 1;
    frame = ripples.length ? requestAnimationFrame(draw) : 0;
  }

  document.addEventListener("pointerdown", function (e) {
    var less = window.GraphiteTheme && GraphiteTheme.reduceMotion ? GraphiteTheme.reduceMotion() : reduce.matches;  // Settings > Motion
    if (less || document.hidden || !enabled()) return;
    ripples.push({ x: e.clientX, y: e.clientY, t: performance.now() });
    if (ripples.length > MAX_RIPPLES) ripples.shift();
    if (!frame) frame = requestAnimationFrame(draw);
  }, { passive: true });

  var resizeTimer = 0;
  window.addEventListener("resize", function () { clearTimeout(resizeTimer); resizeTimer = setTimeout(size, 120); });
  // New theme or accent: pick up the new colors (and show or hide the dots).
  document.addEventListener("graphite:appearance", function () { size(); });
  size();
})();
