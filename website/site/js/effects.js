/* Page background effects, behind the panels on the main pages (home, dashboard, practice, plan, Level up, lessons,
   speed round, focus, rewards, market, tutor and the parent dashboard; never Settings, sign-in, checkout, tests or
   the legal pages). Settings > Appearance > Background picks one (theme.js puts it on <html data-effect>):
     none           nothing
     ripple         a faint dot grid; a click sends a ripple through it (the original)
     dots           the same dot grid, still
     snow, constellation, symbols, waves, fireflies, warp   from the shop
     magnet, springy, pencil, graphpaper, bubbles, gravity  interactive ones from the shop: they follow the pointer
                                                           (or a finger) and react to clicks and taps
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
  var base = [62, 67, 74], hot = [242, 193, 78], pointer = { x: -999, y: -999, t: 0 }, taps = [];
  function here() { return pointer.x > -900; }
  function tapped(since) { return taps.filter(function (t) { return t.t > since; }); }

  function which() {
    var e = root.getAttribute("data-effect");
    if (!e && window.GraphiteTheme && GraphiteTheme.get().ripple === false) e = "none";
    return EFFECTS[e] ? e : "none";
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
    /* ---------- interactive ---------- */
    magnet: {  // iron filings: short strokes that turn to point at the pointer; a tap sends a pulse
      draw: function (now) {
        var S = 34, R = 260, idle = !here() || now - pointer.t > 6000;
        var pulses = tapped(now - 1200).map(function (t) { return { x: t.x, y: t.y, ring: (now - t.t) * 0.55, fade: 1 - (now - t.t) / 1200 }; });
        ctx.lineCap = "round";
        for (var y = S / 2; y < h; y += S) {
          for (var x = S / 2; x < w; x += S) {
            var dx = pointer.x - x, dy = pointer.y - y, d = Math.sqrt(dx * dx + dy * dy) || 1;
            var a = idle ? Math.sin(x * 0.01 + now * 0.0004) + Math.cos(y * 0.012 - now * 0.0003) : Math.atan2(dy, dx);
            var near = idle ? 0 : Math.max(0, 1 - d / R), boost = 0;
            pulses.forEach(function (p) { var o = Math.abs(Math.sqrt((x - p.x) * (x - p.x) + (y - p.y) * (y - p.y)) - p.ring); if (o < 40) boost = Math.max(boost, (1 - o / 40) * p.fade); });
            var len = 5 + near * 7 + boost * 8, c = Math.cos(a) * len, n = Math.sin(a) * len;
            ctx.strokeStyle = col(mixc(base, hot, Math.max(near, boost)), 0.5 + 0.5 * Math.max(near, boost));
            ctx.lineWidth = 1.4 + near;
            ctx.beginPath(); ctx.moveTo(x - c, y - n); ctx.lineTo(x + c, y + n); ctx.stroke();
          }
        }
        return true;
      }
    },
    springy: {  // a dot grid that bends away from the pointer and springs back; a tap pushes everything outward
      init: function () {
        var S = 28; this.p = [];
        for (var y = S / 2; y < h; y += S) for (var x = S / 2; x < w; x += S) this.p.push({ hx: x, hy: y, x: x, y: y, vx: 0, vy: 0 });
        this.seen = performance.now();
      },
      draw: function (now, dt) {
        var hits = tapped(this.seen); this.seen = now;
        var on = here() && now - pointer.t < 4000;
        this.p.forEach(function (q) {
          var ax = (q.hx - q.x) * 60, ay = (q.hy - q.y) * 60;
          if (on) {
            var dx = q.x - pointer.x, dy = q.y - pointer.y, d = Math.sqrt(dx * dx + dy * dy) || 1;
            if (d < 130) { var f = (1 - d / 130) * 2600; ax += dx / d * f; ay += dy / d * f; }
          }
          hits.forEach(function (t) {
            var dx = q.x - t.x, dy = q.y - t.y, d = Math.sqrt(dx * dx + dy * dy) || 1;
            if (d < 260) { var k = (1 - d / 260) * 520; q.vx += dx / d * k; q.vy += dy / d * k; }
          });
          q.vx = (q.vx + ax * dt) * Math.pow(0.02, dt); q.vy = (q.vy + ay * dt) * Math.pow(0.02, dt);
          q.x += q.vx * dt; q.y += q.vy * dt;
          var off = Math.min(1, Math.sqrt((q.x - q.hx) * (q.x - q.hx) + (q.y - q.hy) * (q.y - q.hy)) / 24);
          ctx.fillStyle = col(mixc(base, hot, off), 0.55 + 0.45 * off);
          ctx.beginPath(); ctx.arc(q.x, q.y, 1.2 + off * 1.6, 0, 6.2832); ctx.fill();
        });
        return true;
      }
    },
    pencil: {  // the pointer leaves a graphite line that fades
      init: function () { this.trail = []; },
      draw: function (now) {
        var t = this.trail, life = 2600;
        if (here() && (!t.length || t[t.length - 1].x !== pointer.x || t[t.length - 1].y !== pointer.y)) t.push({ x: pointer.x, y: pointer.y, t: now });
        while (t.length && now - t[0].t > life) t.shift();
        if (t.length > 220) t.splice(0, t.length - 220);
        ctx.lineCap = "round"; ctx.lineJoin = "round";
        var lead = mixc(base, [235, 238, 242], 0.55);
        for (var i = 1; i < t.length; i++) {
          var age = (now - t[i].t) / life;
          ctx.strokeStyle = col(lead, 0.85 * (1 - age)); ctx.lineWidth = 2.6 * (1 - age * 0.6);
          ctx.beginPath(); ctx.moveTo(t[i - 1].x, t[i - 1].y); ctx.lineTo(t[i].x, t[i].y); ctx.stroke();
        }
        tapped(now - 900).forEach(function (p) {  // a tap leaves a little smudge
          var k = 1 - (now - p.t) / 900;
          ctx.fillStyle = col(lead, 0.25 * k); ctx.beginPath(); ctx.arc(p.x, p.y, 10 + (1 - k) * 18, 0, 6.2832); ctx.fill();
        });
        if (t.length) { var e = t[t.length - 1]; ctx.fillStyle = col(hot, 0.9); ctx.beginPath(); ctx.arc(e.x, e.y, 2.4, 0, 6.2832); ctx.fill(); }
        return true;
      }
    },
    graphpaper: {  // graph paper lights up around the pointer and shows its coordinates; a tap plots a point
      draw: function (now) {
        var U = 32, cx = Math.round(w / 2 / U) * U, cy = Math.round(h / 2 / U) * U, x, y;
        function lines(style, width) {
          ctx.strokeStyle = style; ctx.lineWidth = width; ctx.beginPath();
          for (x = cx % U; x < w; x += U) { ctx.moveTo(x + 0.5, 0); ctx.lineTo(x + 0.5, h); }
          for (y = cy % U; y < h; y += U) { ctx.moveTo(0, y + 0.5); ctx.lineTo(w, y + 0.5); }
          ctx.stroke();
        }
        lines(col(base, 0.28), 1);
        ctx.strokeStyle = col(base, 0.8); ctx.lineWidth = 1.5; ctx.beginPath();
        ctx.moveTo(cx + 0.5, 0); ctx.lineTo(cx + 0.5, h); ctx.moveTo(0, cy + 0.5); ctx.lineTo(w, cy + 0.5); ctx.stroke();
        var fmt = function (v) { v = Math.round(v * 10) / 10; return (v < 0 ? "\u2212" : "") + Math.abs(v); };
        ctx.font = "700 12px system-ui, sans-serif"; ctx.textBaseline = "bottom";
        this.pts = (this.pts || []).concat(tapped(this.seen || 0).map(function (t) { return { x: t.x, y: t.y, t: t.t }; }));
        this.seen = now;
        this.pts = this.pts.filter(function (q) { return now - q.t < 7000; }).slice(-8);
        this.pts.forEach(function (q) {
          var k = 1 - (now - q.t) / 7000, gx = Math.round((q.x - cx) / U * 2) / 2, gy = Math.round((cy - q.y) / U * 2) / 2;
          var X = cx + gx * U, Y = cy - gy * U;
          ctx.fillStyle = col(hot, 0.9 * k); ctx.beginPath(); ctx.arc(X, Y, 4.5, 0, 6.2832); ctx.fill();
          ctx.fillStyle = col(hot, 0.75 * k); ctx.fillText("(" + fmt(gx) + ", " + fmt(gy) + ")", X + 8, Y - 6);
        });
        if (here() && now - pointer.t < 5000) {
          var g = ctx.createRadialGradient(pointer.x, pointer.y, 0, pointer.x, pointer.y, 170);
          g.addColorStop(0, col(hot, 0.55)); g.addColorStop(1, col(hot, 0));
          lines(g, 1.2);
          ctx.fillStyle = col(hot, 0.85);
          ctx.fillText("(" + fmt((pointer.x - cx) / U) + ", " + fmt((cy - pointer.y) / U) + ")", pointer.x + 14, pointer.y + 24);
        }
        return true;
      }
    },
    bubbles: {  // number bubbles float up; tap to blow more, move over one to pop it
      init: function () { this.b = []; this.pops = []; this.next = 0; this.seen = performance.now(); },
      spawn: function (x, y, burst) {
        var L = ["7", "\u03c0", "x\u00b2", "\u221a2", "12", "\u2153", "3x", "e", "0", "\u221e", "9", "y"];
        this.b.push({ x: x, y: y, r: rnd(12, 24), vy: rnd(18, 36), vx: burst ? rnd(-40, 40) : rnd(-4, 4), ph: rnd(0, 6.28), g: L[Math.floor(Math.random() * L.length)] });
      },
      draw: function (now, dt) {
        var self = this;
        if (now > this.next && this.b.length < count(60000, 14)) { this.spawn(rnd(0, w), h + 30, false); this.next = now + rnd(900, 1800); }
        tapped(this.seen).forEach(function (t) { for (var i = 0; i < 3; i++) self.spawn(t.x + rnd(-10, 10), t.y + rnd(-10, 10), true); });
        this.seen = now;
        ctx.textAlign = "center"; ctx.textBaseline = "middle";
        this.b = this.b.filter(function (q) {
          q.y -= q.vy * dt; q.x += (q.vx + Math.sin(now / 900 + q.ph) * 8) * dt; q.vx *= Math.pow(0.3, dt);
          var dx = q.x - pointer.x, dy = q.y - pointer.y;
          if (here() && dx * dx + dy * dy < q.r * q.r) { self.pops.push({ x: q.x, y: q.y, r: q.r, t: now }); return false; }
          if (q.y < -40) return false;
          ctx.strokeStyle = col(mixc(base, hot, 0.35), 0.7); ctx.lineWidth = 1.4;
          ctx.fillStyle = col(hot, 0.06); ctx.beginPath(); ctx.arc(q.x, q.y, q.r, 0, 6.2832); ctx.fill(); ctx.stroke();
          ctx.fillStyle = col(mixc(base, [235, 238, 242], 0.5), 0.8); ctx.font = "700 " + Math.round(q.r * 0.8) + "px system-ui, sans-serif";
          ctx.fillText(q.g, q.x, q.y + 1);
          return true;
        });
        this.pops = this.pops.filter(function (q) {
          var k = (now - q.t) / 320; if (k > 1) return false;
          ctx.strokeStyle = col(hot, 0.8 * (1 - k)); ctx.lineWidth = 2;
          ctx.beginPath(); ctx.arc(q.x, q.y, q.r * (1 + k * 0.8), 0, 6.2832); ctx.stroke();
          return true;
        });
        return true;
      }
    },
    gravity: {  // specks fall toward the pointer and swing around it; a tap flings them away
      init: function () { this.p = []; for (var i = 0; i < count(7000, 180); i++) this.p.push({ x: rnd(0, w), y: rnd(0, h), vx: rnd(-10, 10), vy: rnd(-10, 10) }); this.seen = performance.now(); },
      draw: function (now, dt) {
        var on = here() && now - pointer.t < 5000, hits = tapped(this.seen); this.seen = now;
        this.p.forEach(function (q) {
          var x0 = q.x, y0 = q.y;
          if (on) {
            var dx = pointer.x - q.x, dy = pointer.y - q.y, d2 = dx * dx + dy * dy + 900, d = Math.sqrt(d2), f = 90000 / d2;
            q.vx += dx / d * f * dt * 6; q.vy += dy / d * f * dt * 6;
          } else { q.vx += rnd(-6, 6) * dt; q.vy += rnd(-6, 6) * dt; }
          hits.forEach(function (t) { var dx = q.x - t.x, dy = q.y - t.y, d = Math.sqrt(dx * dx + dy * dy) || 1; if (d < 300) { q.vx += dx / d * 420 * (1 - d / 300); q.vy += dy / d * 420 * (1 - d / 300); } });
          var sp = Math.sqrt(q.vx * q.vx + q.vy * q.vy), top = 320;
          if (sp > top) { q.vx *= top / sp; q.vy *= top / sp; }
          q.vx *= Math.pow(0.55, dt); q.vy *= Math.pow(0.55, dt);
          q.x += q.vx * dt; q.y += q.vy * dt;
          if (q.x < -20) q.x = w + 20; if (q.x > w + 20) q.x = -20; if (q.y < -20) q.y = h + 20; if (q.y > h + 20) q.y = -20;
          var k = Math.min(1, sp / 260);
          ctx.strokeStyle = col(mixc(base, hot, k), 0.35 + 0.55 * k); ctx.lineWidth = 1.6;
          ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(q.x + (q.x - x0) * 0.01, q.y + (q.y - y0) * 0.01); ctx.lineTo(q.x, q.y); ctx.stroke();
          ctx.fillStyle = col(mixc(base, hot, k), 0.9); ctx.beginPath(); ctx.arc(q.x, q.y, 1.3, 0, 6.2832); ctx.fill();
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
    if (still() || document.hidden) return;
    taps.push({ x: e.clientX, y: e.clientY, t: performance.now() });
    if (taps.length > 12) taps.shift();
    pointer.x = e.clientX; pointer.y = e.clientY; pointer.t = performance.now();
    if (effect !== "ripple") return;
    ripples.push({ x: e.clientX, y: e.clientY, t: performance.now() });
    if (ripples.length > 6) ripples.shift();
    kick();
  }, { passive: true });
  document.addEventListener("pointermove", function (e) { pointer.x = e.clientX; pointer.y = e.clientY; pointer.t = performance.now(); }, { passive: true });
  document.addEventListener("pointerleave", function () { pointer.x = pointer.y = -999; }, { passive: true });
  document.documentElement.addEventListener("mouseleave", function () { pointer.x = pointer.y = -999; });
  document.addEventListener("visibilitychange", function () { if (!document.hidden) kick(); });
  var resizeTimer = 0;
  window.addEventListener("resize", function () { clearTimeout(resizeTimer); resizeTimer = setTimeout(setup, 150); });
  document.addEventListener("graphite:appearance", setup);  // a new background, theme or accent
  setup();
  window.GraphiteEffects = { list: Object.keys(EFFECTS), refresh: setup };
})();
