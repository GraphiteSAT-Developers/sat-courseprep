/* Page background effects, behind the panels on the main pages (home, dashboard, practice, plan, Level up, lessons,
   speed round, focus, rewards, market, tutor and the parent dashboard; never Settings, sign-in, checkout, tests or
   the legal pages). Settings > Appearance > Background picks one (theme.js puts it on <html data-effect>):
     none           nothing
     ripple         a faint dot grid; a click sends a ripple through it (the original)
     dots           the same dot grid, still
     snow, constellation, symbols, waves, fireflies, warp   from the shop
   Everything is drawn on one canvas that never takes clicks. It runs at about 30 frames a second, stops while the
   tab is hidden, and holds a still frame for anyone who has asked for less motion. */
(function () {
  "use strict";
  var host = document.querySelector("main");
  if (!host || !window.requestAnimationFrame) return;

  var canvas = document.createElement("canvas");
  canvas.className = "ripple-bg";
  canvas.setAttribute("aria-hidden", "true");
  document.body.insertBefore(canvas, document.body.firstChild);
  var ctx = canvas.getContext("2d");
  if (!ctx) return;

  var root = document.documentElement;
  var mq = window.matchMedia ? window.matchMedia("(prefers-reduced-motion: reduce)") : { matches: false };
  var w = 0, h = 0, dpr = 1, frame = 0, last = 0, effect = "", fx = null;
  var base = [62, 67, 74], hot = [242, 193, 78], pointer = { x: -999, y: -999 };

  function which() {
    var e = root.getAttribute("data-effect");
    if (!e && window.GraphiteTheme && GraphiteTheme.get().ripple === false) e = "none";
    return EFFECTS[e] ? e : "ripple";
  }
  function still() { return window.GraphiteTheme && GraphiteTheme.reduceMotion ? GraphiteTheme.reduceMotion() : mq.matches; }
  function rgb(token, fallback) {
    var v = getComputedStyle(root).getPropertyValue(token).trim(), m = /^#([0-9a-f]{6})$/i.exec(v);
    if (!m) return fallback;
    var n = parseInt(m[1], 16);
    return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
  }
  function col(c, a) { return "rgba(" + c[0] + "," + c[1] + "," + c[2] + "," + a + ")"; }
  function mixc(a, b, t) { return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t].map(Math.round); }
  function rnd(a, b) { return a + Math.random() * (b - a); }
  function count(per, max) { return Math.min(max, Math.round(w * h / per)); }

  /* ---------- the dot grid, with click ripples ---------- */
  var SPACING = 26, ripples = [];
  function dotGrid(now, withRipples) {
    var live = [];
    if (withRipples) {
      ripples = ripples.filter(function (r) { return now - r.t < 1500; });
      live = ripples.map(function (r) { var age = now - r.t; return { x: r.x, y: r.y, ring: age * 0.62, fade: 1 - age / 1500 }; });
    }
    for (var y = SPACING / 2; y < h; y += SPACING) {
      for (var x = SPACING / 2; x < w; x += SPACING) {
        var glow = 0, dx = 0, dy = 0;
        for (var i = 0; i < live.length; i++) {
          var r = live[i], ox = x - r.x, oy = y - r.y, d = Math.sqrt(ox * ox + oy * oy) || 1, off = d - r.ring;
          var k = Math.exp(-(off * off) / 1058) * r.fade * r.fade;
          if (k < 0.01) continue;
          glow = Math.max(glow, k); dx += (ox / d) * k * 7; dy += (oy / d) * k * 7;
        }
        ctx.fillStyle = col(mixc(base, hot, glow), 0.55 + 0.45 * glow);
        ctx.beginPath(); ctx.arc(x + dx, y + dy, 1.1 + glow * 1.6, 0, 6.2832); ctx.fill();
      }
    }
    return withRipples && ripples.length > 0;
  }

  var GLYPHS = ["π", "Σ", "√", "∞", "θ", "Δ", "x²", "≠", "≤", "∫", "%", "÷"];
  var EFFECTS = {
    none: { draw: function () { return false; } },
    ripple: { draw: function (now) { return dotGrid(now, true); } },
    dots: { draw: function (now) { dotGrid(now, false); return false; } },
    snow: {
      init: function () { this.p = []; for (var i = 0; i < count(9000, 140); i++) this.p.push({ x: rnd(0, w), y: rnd(0, h), r: rnd(0.8, 2.4), s: rnd(8, 22), o: rnd(0, 6.28) }); },
      draw: function (now, dt) {
        this.p.forEach(function (f) {
          f.y += f.s * dt; f.x += Math.sin(now / 1400 + f.o) * 0.25;
          if (f.y > h + 4) { f.y = -4; f.x = rnd(0, w); }
          ctx.fillStyle = col(mixc(base, [255, 255, 255], 0.6), 0.55);
          ctx.beginPath(); ctx.arc(f.x, f.y, f.r, 0, 6.2832); ctx.fill();
        });
        return true;
      }
    },
    constellation: {
      init: function () { this.p = []; for (var i = 0; i < count(16000, 90); i++) this.p.push({ x: rnd(0, w), y: rnd(0, h), vx: rnd(-6, 6), vy: rnd(-6, 6) }); },
      draw: function (now, dt) {
        var p = this.p, i, j;
        p.forEach(function (s) {
          s.x += s.vx * dt; s.y += s.vy * dt;
          if (s.x < 0 || s.x > w) s.vx *= -1;
          if (s.y < 0 || s.y > h) s.vy *= -1;
        });
        ctx.lineWidth = 1;
        for (i = 0; i < p.length; i++) {
          for (j = i + 1; j < p.length; j++) {
            var dx = p[i].x - p[j].x, dy = p[i].y - p[j].y, d = dx * dx + dy * dy;
            if (d < 12100) { ctx.strokeStyle = col(base, 0.9 * (1 - d / 12100)); ctx.beginPath(); ctx.moveTo(p[i].x, p[i].y); ctx.lineTo(p[j].x, p[j].y); ctx.stroke(); }
          }
          var px = p[i].x - pointer.x, py = p[i].y - pointer.y, pd = px * px + py * py;
          if (pd < 32400) { ctx.strokeStyle = col(hot, 0.5 * (1 - pd / 32400)); ctx.beginPath(); ctx.moveTo(p[i].x, p[i].y); ctx.lineTo(pointer.x, pointer.y); ctx.stroke(); }
          ctx.fillStyle = col(pd < 32400 ? hot : base, 0.9);
          ctx.beginPath(); ctx.arc(p[i].x, p[i].y, 1.6, 0, 6.2832); ctx.fill();
        }
        return true;
      }
    },
    symbols: {
      init: function () { this.p = []; for (var i = 0; i < count(26000, 40); i++) this.p.push({ x: rnd(0, w), y: rnd(0, h), g: GLYPHS[i % GLYPHS.length], s: rnd(5, 14), size: rnd(14, 30), a: rnd(-0.4, 0.4), spin: rnd(-0.15, 0.15) }); },
      draw: function (now, dt) {
        ctx.textAlign = "center"; ctx.textBaseline = "middle";
        this.p.forEach(function (g) {
          g.y -= g.s * dt; g.a += g.spin * dt;
          if (g.y < -30) { g.y = h + 30; g.x = rnd(0, w); }
          ctx.save(); ctx.translate(g.x, g.y); ctx.rotate(g.a);
          ctx.font = "700 " + Math.round(g.size) + "px system-ui, sans-serif";
          ctx.fillStyle = col(base, 0.75); ctx.fillText(g.g, 0, 0); ctx.restore();
        });
        return true;
      }
    },
    waves: {
      draw: function (now) {
        var layers = [[0.62, 0.00055, 36, 0.35], [0.72, 0.0008, 26, 0.5], [0.82, 0.0011, 18, 0.7]];
        layers.forEach(function (L, k) {
          ctx.beginPath();
          for (var x = 0; x <= w; x += 8) {
            var y = h * L[0] + Math.sin(x * 0.006 + now * L[1] + k) * L[2] + Math.sin(x * 0.013 - now * L[1] * 0.7) * L[2] * 0.4;
            if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
          }
          ctx.strokeStyle = col(k === 2 ? mixc(base, hot, 0.35) : base, L[3]); ctx.lineWidth = 2; ctx.stroke();
        });
        return true;
      }
    },
    fireflies: {
      init: function () { this.p = []; for (var i = 0; i < count(30000, 36); i++) this.p.push({ x: rnd(0, w), y: rnd(0, h), a: rnd(0, 6.28), v: rnd(10, 22), ph: rnd(0, 6.28), sp: rnd(0.0012, 0.0026) }); },
      draw: function (now, dt) {
        this.p.forEach(function (f) {
          f.a += rnd(-1.2, 1.2) * dt; f.x += Math.cos(f.a) * f.v * dt; f.y += Math.sin(f.a) * f.v * dt;
          if (f.x < -10) f.x = w + 10; if (f.x > w + 10) f.x = -10; if (f.y < -10) f.y = h + 10; if (f.y > h + 10) f.y = -10;
          var glow = 0.25 + 0.75 * Math.max(0, Math.sin(now * f.sp + f.ph));
          ctx.fillStyle = col(hot, 0.12 * glow); ctx.beginPath(); ctx.arc(f.x, f.y, 9, 0, 6.2832); ctx.fill();
          ctx.fillStyle = col(hot, 0.85 * glow); ctx.beginPath(); ctx.arc(f.x, f.y, 1.8, 0, 6.2832); ctx.fill();
        });
        return true;
      }
    },
    warp: {
      init: function () { this.p = []; for (var i = 0; i < count(9000, 160); i++) this.p.push(this.star(true)); },
      star: function (anywhere) { return { a: rnd(0, 6.2832), d: anywhere ? rnd(0, Math.max(w, h) * 0.7) : rnd(0, 40), v: rnd(14, 40) }; },
      draw: function (now, dt) {
        var cx = w / 2, cy = h / 2, self = this;
        this.p.forEach(function (s, i) {
          var d0 = s.d; s.d += s.v * dt * (1 + s.d / 260);
          if (s.d > Math.max(w, h) * 0.75) { self.p[i] = self.star(false); return; }
          var c = Math.cos(s.a), n = Math.sin(s.a);
          ctx.strokeStyle = col(mixc(base, [255, 255, 255], Math.min(1, s.d / 500)), Math.min(0.9, 0.2 + s.d / 400));
          ctx.lineWidth = 1 + s.d / 500;
          ctx.beginPath(); ctx.moveTo(cx + c * d0, cy + n * d0); ctx.lineTo(cx + c * s.d, cy + n * s.d); ctx.stroke();
        });
        return true;
      }
    }
  };

  function tick(now) {
    frame = 0;
    if (document.hidden) return;
    var dt = Math.min(0.1, (now - (last || now)) / 1000);
    if (now - last < 30 && fx !== EFFECTS.ripple) { frame = requestAnimationFrame(tick); return; }  // about 30 fps
    last = now;
    ctx.clearRect(0, 0, w, h);
    var more = fx.draw(now, still() ? 0 : dt);
    if (more && !still()) frame = requestAnimationFrame(tick);
  }
  function kick() { if (!frame) { last = 0; frame = requestAnimationFrame(tick); } }
  function setup() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    w = window.innerWidth; h = window.innerHeight;
    canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr);
    canvas.style.width = w + "px"; canvas.style.height = h + "px";
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    base = rgb("--line", base); hot = rgb("--accent", hot);
    effect = which(); fx = EFFECTS[effect];
    canvas.hidden = effect === "none";
    if (fx.init) fx.init();
    if (frame) { cancelAnimationFrame(frame); frame = 0; }
    kick();
  }

  document.addEventListener("pointerdown", function (e) {
    if (effect !== "ripple" || still() || document.hidden) return;
    ripples.push({ x: e.clientX, y: e.clientY, t: performance.now() });
    if (ripples.length > 6) ripples.shift();
    kick();
  }, { passive: true });
  document.addEventListener("pointermove", function (e) { pointer.x = e.clientX; pointer.y = e.clientY; }, { passive: true });
  document.addEventListener("visibilitychange", function () { if (!document.hidden) kick(); });
  var resizeTimer = 0;
  window.addEventListener("resize", function () { clearTimeout(resizeTimer); resizeTimer = setTimeout(setup, 150); });
  document.addEventListener("graphite:appearance", setup);  // a new background, theme or accent
  setup();
  window.GraphiteEffects = { list: Object.keys(EFFECTS), refresh: setup };
})();
