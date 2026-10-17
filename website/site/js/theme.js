/* Appearance for signed-in pages, applied before anything is drawn so there's no flash of the wrong look:
   theme (dark, light, match my device, paper, midnight, high contrast, and two shop themes), accent color
   (including any custom color from the shop), text size, an easier-to-read font, motion, spacing and the
   ripple background. Also keeps the student's other preferences (dashboard layout, study defaults, drawn
   avatar) so pages can use them right away. The last choices are kept in this browser so they apply
   instantly; on the live site the account's saved choices then take over on every device.
   Also turns the email in the header into a link to Settings, with the profile picture or drawn avatar. */
(function () {
  "use strict";
  var KEY = "graphite_appearance", PREFS_KEY = "graphite_prefs", PROFILE_KEY = "graphite_preview_profile";
  // theme -> the base it builds on. Themes other than dark, light and system are "skins" over a base.
  var BASE = { dark: "dark", light: "light", system: "system", paper: "light", midnight: "dark", contrast: "dark", chalkboard: "dark", nightowl: "dark" };
  var THEMES = Object.keys(BASE), SHOP_THEMES = ["chalkboard", "nightowl"];
  var ACCENTS = ["pencil", "sky", "mint", "coral", "lilac", "rose", "blueprint", "ember", "custom"];  // rose onward come from the shop
  var LOOK = { text: ["s", "m", "l", "xl"], font: ["default", "readable"], motion: ["system", "reduce", "full"], density: ["comfortable", "compact"] };
  var DEFAULTS = {
    dashboard: { order: ["kpis", "play", "today", "scores", "domains", "review", "plan", "account"], hidden: [], pins: [] },
    study: { set_size: 10, timer: "show", calculator: "closed", colors: "graphite", sounds: true, reminder: false, reminder_hour: 16, tz: "America/New_York" },
    avatar: { mode: "photo", parts: { bg: "sky", skin: "s3", hair: "short", hair_color: "brown", eyes: "dots", mouth: "smile", acc: "none", shirt: "pencil" } }
  };
  var root = document.documentElement;
  var state = { theme: "dark", accent: "pencil", ripple: true, text: "m", font: "default", motion: "system", density: "comfortable", custom_accent: "#f2c14e" };
  var mq = window.matchMedia ? window.matchMedia("(prefers-color-scheme: light)") : null;
  var mqMotion = window.matchMedia ? window.matchMedia("(prefers-reduced-motion: reduce)") : null;
  var me = null, prefsCache = null;

  function merge(s) {
    if (!s) return;
    if (THEMES.indexOf(s.theme) > -1) state.theme = s.theme;
    if (ACCENTS.indexOf(s.accent) > -1) state.accent = s.accent;
    if (typeof s.ripple === "boolean") state.ripple = s.ripple;
    Object.keys(LOOK).forEach(function (k) { if (LOOK[k].indexOf(s[k]) > -1) state[k] = s[k]; });
    if (/^#[0-9a-f]{6}$/i.test(s.custom_accent || "")) state.custom_accent = s.custom_accent.toLowerCase();
  }
  function resolved() {
    var b = BASE[state.theme] || "dark";
    return b === "system" ? (mq && mq.matches ? "light" : "dark") : b;
  }
  function reduceMotion() { return state.motion === "reduce" || (state.motion === "system" && !!(mqMotion && mqMotion.matches)); }
  function get() { var o = {}; Object.keys(state).forEach(function (k) { o[k] = state[k]; }); o.resolved = resolved(); o.reduce_motion = reduceMotion(); return o; }

  /* ---------- a custom accent color: hover, text-on-accent and shadow shades worked out from it ---------- */
  function rgb(hex) { return [1, 3, 5].map(function (i) { return parseInt(hex.substr(i, 2), 16); }); }
  function hex(c) { return "#" + c.map(function (v) { return Math.max(0, Math.min(255, Math.round(v))).toString(16).padStart(2, "0"); }).join(""); }
  function mix(c, to, t) { return c.map(function (v, i) { return v + (to[i] - v) * t; }); }
  function lum(c) { var a = c.map(function (v) { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }); return 0.2126 * a[0] + 0.7152 * a[1] + 0.0722 * a[2]; }
  function contrast(a, b) { var x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); }
  function customVars(h) {
    var c = rgb(h), dark = resolved() === "dark", white = [255, 255, 255], black = [0, 0, 0];
    return { "--accent": h, "--accent-hover": hex(mix(c, dark ? white : black, dark ? 0.25 : 0.2)),
             "--accent-ink": contrast(c, black) >= contrast(c, white) ? "#111214" : "#ffffff", "--accent-shadow": hex(mix(c, black, 0.4)) };
  }

  var fontLoaded = false;
  function loadReadableFont() {
    if (fontLoaded || state.font !== "readable") return;
    fontLoaded = true;
    var l = document.createElement("link");
    l.rel = "stylesheet";
    l.href = "https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&display=swap";
    document.head.appendChild(l);
  }
  function apply() {
    root.setAttribute("data-theme", resolved());
    if (BASE[state.theme] && state.theme !== BASE[state.theme] && state.theme !== "system") root.setAttribute("data-skin", state.theme); else root.removeAttribute("data-skin");
    root.setAttribute("data-accent", state.accent);
    var vars = state.accent === "custom" ? customVars(state.custom_accent) : null;
    ["--accent", "--accent-hover", "--accent-ink", "--accent-shadow"].forEach(function (k) { if (vars) root.style.setProperty(k, vars[k]); else root.style.removeProperty(k); });
    root.setAttribute("data-text", state.text);
    root.setAttribute("data-font", state.font);
    root.setAttribute("data-motion", reduceMotion() ? "reduce" : "full");
    root.setAttribute("data-density", state.density);
    loadReadableFont();
    try { document.dispatchEvent(new CustomEvent("graphite:appearance", { detail: get() })); } catch (e) { /* old browser */ }
  }
  function set(s) {
    merge(s);
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { /* storage blocked */ }
    apply();
  }

  try { merge(JSON.parse(localStorage.getItem(KEY) || "null")); } catch (e) { /* storage blocked */ }
  apply();
  [mq, mqMotion].forEach(function (m) {
    if (!m) return;
    var again = function () { apply(); };
    if (m.addEventListener) m.addEventListener("change", again); else if (m.addListener) m.addListener(again);
  });

  /* ---------- other preferences ---------- */
  function withDefaults(p) {
    p = p || {};
    var out = {};
    Object.keys(DEFAULTS).forEach(function (k) {
      out[k] = {};
      Object.keys(DEFAULTS[k]).forEach(function (f) { out[k][f] = p[k] && p[k][f] !== undefined ? p[k][f] : DEFAULTS[k][f]; });
    });
    out.avatar.parts = Object.assign({}, DEFAULTS.avatar.parts, (p.avatar && p.avatar.parts) || {});
    return out;
  }
  function prefs() {
    if (!prefsCache) { try { prefsCache = withDefaults(JSON.parse(localStorage.getItem(PREFS_KEY) || "null")); } catch (e) { prefsCache = withDefaults(null); } }
    return prefsCache;
  }
  function setPrefs(p) {
    prefsCache = withDefaults(Object.assign({}, prefs(), p));
    try { localStorage.setItem(PREFS_KEY, JSON.stringify(prefsCache)); } catch (e) { /* storage blocked */ }
    try { document.dispatchEvent(new CustomEvent("graphite:prefs", { detail: prefsCache })); } catch (e) { /* old browser */ }
    return prefsCache;
  }

  /* ---------- the drawn avatar ---------- */
  var BG = { sky: "#9cc9f5", mint: "#9fe3c1", sun: "#f7d774", rose: "#f5a8c8", lilac: "#c9b5f5", slate: "#9aa6b5", peach: "#f8bf9a", teal: "#7fcfcf" };
  var SKIN = { s1: "#fbe0cc", s2: "#f3caa6", s3: "#e2ac83", s4: "#c98e63", s5: "#a86f47", s6: "#8a5636", s7: "#6b3f26", s8: "#4b2b1a" };
  var HAIR_COLOR = { black: "#1d1a19", brown: "#5a3a22", auburn: "#8e3b1f", blonde: "#e3c16f", gray: "#a9a9a9", blue: "#3f7fe0", pink: "#ef7fb3", green: "#3fae6a" };
  var SHIRT = { pencil: "#f2c14e", sky: "#4f9be0", mint: "#3fb87f", coral: "#ec6f58", lilac: "#9b7be6", slate: "#5b6675", white: "#f4f4f4", black: "#2a2a2a" };
  var INK = "#1d1a19";
  // Hair: [behind the head, in front of it]
  var HAIR = {
    short: ["", '<path d="M17.5 28C17 14 47 14 46.5 28 42 21 34 19 26 21 22 22 19 24 17.5 28Z"/>'],
    curly: ["", '<g><circle cx="20" cy="23" r="5"/><circle cx="25" cy="18" r="5.5"/><circle cx="32" cy="16" r="6"/><circle cx="39" cy="18" r="5.5"/><circle cx="44" cy="23" r="5"/></g>'],
    long: ['<path d="M16.5 30C16.5 14 47.5 14 47.5 30L49 52H15Z"/>', '<path d="M17.5 28C17 14 47 14 46.5 28 40 20 24 20 17.5 28Z"/>'],
    bun: ['<circle cx="32" cy="11" r="6.5"/>', '<path d="M18 26C18 15 46 15 46 26 40 20 24 20 18 26Z"/>'],
    buzz: ["", '<path d="M18.5 25.5C19 15 45 15 45.5 25.5 40 20.5 24 20.5 18.5 25.5Z" opacity=".8"/>'],
    waves: ["", '<path d="M17 29C16 13 48 13 47 29 45 25 43 27 41 23 39 26 36 24 34 21 31 25 28 22 26 24 23 22 20 26 17 29Z"/>'],
    ponytail: ['<ellipse cx="48.5" cy="35" rx="5" ry="11"/>', '<path d="M18 27C18 15 46 15 46 27 41 21 29 18 18 27Z"/>']
  };
  var EYES = {
    dots: '<circle cx="26" cy="30" r="1.9" fill="' + INK + '"/><circle cx="38" cy="30" r="1.9" fill="' + INK + '"/>',
    happy: '<path d="M23.5 31q2.5-3.2 5 0M35.5 31q2.5-3.2 5 0" fill="none" stroke="' + INK + '" stroke-width="1.6" stroke-linecap="round"/>',
    wide: '<circle cx="26" cy="30" r="3" fill="#fff"/><circle cx="38" cy="30" r="3" fill="#fff"/><circle cx="26.4" cy="30.4" r="1.6" fill="' + INK + '"/><circle cx="38.4" cy="30.4" r="1.6" fill="' + INK + '"/>',
    sleepy: '<path d="M23.5 30.5h5M35.5 30.5h5" stroke="' + INK + '" stroke-width="1.6" stroke-linecap="round"/>'
  };
  var MOUTH = {
    smile: '<path d="M27.5 36q4.5 3.6 9 0" fill="none" stroke="' + INK + '" stroke-width="1.6" stroke-linecap="round"/>',
    grin: '<path d="M26.5 35.2q5.5 6.5 11 0Z" fill="#7a2e2e"/><path d="M27.6 35.6h8.8" stroke="#fff" stroke-width="1.2"/>',
    flat: '<path d="M28.5 37h7" stroke="' + INK + '" stroke-width="1.6" stroke-linecap="round"/>',
    open: '<ellipse cx="32" cy="37" rx="2.4" ry="2.9" fill="#7a2e2e"/>'
  };
  var ACC = {
    glasses: '<g fill="none" stroke="' + INK + '" stroke-width="1.4"><circle cx="26" cy="30" r="4.4"/><circle cx="38" cy="30" r="4.4"/><path d="M30.4 30h3.2M21.6 29.5l-3.4-1M42.4 29.5l3.4-1"/></g>',
    beanie: '<path d="M16.5 26C16.5 9 47.5 9 47.5 26Z" fill="#c94f4f"/><rect x="15.5" y="23" width="33" height="5" rx="2.5" fill="#a83c3c"/><circle cx="32" cy="9.5" r="3" fill="#e9e1d6"/>',
    headphones: '<path d="M16.5 31C16.5 11 47.5 11 47.5 31" fill="none" stroke="#2f3237" stroke-width="3"/><rect x="12.5" y="26" width="6.5" height="11" rx="3" fill="#2f3237"/><rect x="45" y="26" width="6.5" height="11" rx="3" fill="#2f3237"/>',
    sunglasses: '<g fill="' + INK + '"><rect x="21" y="27" width="9.5" height="6.5" rx="2.5"/><rect x="33.5" y="27" width="9.5" height="6.5" rx="2.5"/><rect x="30" y="28.5" width="4" height="1.4"/></g>',
    pencil: '<g transform="rotate(-35 47 22)"><rect x="44.5" y="10" width="5" height="20" fill="#f2c14e"/><rect x="44.5" y="10" width="5" height="3.5" fill="#ef7fb3"/><path d="M44.5 30h5l-2.5 5Z" fill="#e8c9a0"/><path d="M46.4 33.2h1.2l-.6 1.6Z" fill="' + INK + '"/></g>',
    gradcap: '<path d="M13 17L32 9.5 51 17 32 24.5Z" fill="#232528"/><path d="M21 20.5v5c6 4 16 4 22 0v-5L32 24.5Z" fill="#2f3237"/><path d="M48 18v9" stroke="#f2c14e" stroke-width="1.4"/><circle cx="48" cy="28" r="1.6" fill="#f2c14e"/>',
    crown: '<path d="M20 19L21.5 8 27 13.5 32 6 37 13.5 42.5 8 44 19Z" fill="#e3a92b" stroke="#a8760f" stroke-width="1"/><circle cx="32" cy="14" r="1.6" fill="#ec6f58"/>'
  };
  function drawAvatar(p, label) {
    p = Object.assign({}, DEFAULTS.avatar.parts, p || {});
    var hair = HAIR[p.hair] || ["", ""], hc = HAIR_COLOR[p.hair_color] || HAIR_COLOR.brown, skin = SKIN[p.skin] || SKIN.s3;
    var covered = p.acc === "beanie" || p.acc === "gradcap";
    return '<svg viewBox="0 0 64 64" class="drawn-avatar" role="img" aria-label="' + (label || "Avatar") + '">' +
      '<rect width="64" height="64" fill="' + (BG[p.bg] || BG.sky) + '"/>' +
      (hair[0] ? '<g fill="' + hc + '">' + hair[0] + "</g>" : "") +
      '<path d="M9 64C11 50 21 45.5 32 45.5S53 50 55 64Z" fill="' + (SHIRT[p.shirt] || SHIRT.pencil) + '"/>' +
      '<rect x="28" y="38" width="8" height="9" rx="3" fill="' + skin + '"/>' +
      '<circle cx="18.5" cy="31" r="3" fill="' + skin + '"/><circle cx="45.5" cy="31" r="3" fill="' + skin + '"/>' +
      '<circle cx="32" cy="29" r="14" fill="' + skin + '"/>' +
      (hair[1] && !covered ? '<g fill="' + hc + '">' + hair[1] + "</g>" : "") +
      (EYES[p.eyes] || EYES.dots) + (MOUTH[p.mouth] || MOUTH.smile) + (ACC[p.acc] || "") + "</svg>";
  }

  /* ---------- profile picture ---------- */
  function initials(name) {
    var parts = String(name || "").trim().split(/\s+/).filter(Boolean);
    return ((parts[0] || "?").charAt(0) + (parts.length > 1 ? parts[parts.length - 1].charAt(0) : "")).toUpperCase();
  }
  // Fills a .avatar element: the drawn avatar if the student chose one, else the photo, else their initials.
  function avatar(el, user) {
    if (!el) return;
    el.textContent = "";
    el.classList.remove("is-drawn");
    if (user && user.frame) el.setAttribute("data-frame", user.frame); else el.removeAttribute("data-frame");  // a frame from the shop
    if (user && user.avatar_drawn) { el.innerHTML = drawAvatar(user.avatar_drawn, ""); el.classList.add("is-drawn"); return; }
    var src = user && user.avatar_url;
    if (src) {
      var img = document.createElement("img");
      img.alt = ""; img.src = src; img.decoding = "async";
      img.onerror = function () { el.textContent = initials(user.name); };
      el.appendChild(img);
    } else {
      el.textContent = initials(user && user.name);
    }
  }

  function previewUser() {
    var p = {}, who = "";
    try { p = JSON.parse(localStorage.getItem(PROFILE_KEY) || "{}") || {}; } catch (e) { /* storage blocked */ }
    try { who = sessionStorage.getItem("graphite_user") || ""; } catch (e) { /* storage blocked */ }
    var role = "student";
    try { role = sessionStorage.getItem("graphite_role") || (who === "beta2" ? "parent" : "student"); } catch (e) { /* storage blocked */ }
    var fallback = who === "beta2" ? "Beta2 Parent" : who === "beta" || !who ? "Beta Tester" : who.split("@")[0];
    var play = {}; try { play = JSON.parse(localStorage.getItem("graphite_play_v1") || "{}") || {}; } catch (e) { /* storage blocked */ }
    var pr = prefs();
    return { name: p.name || fallback, email: p.email || who || "beta", avatar_url: p.avatar || null, role: role,
             frame: play.frame || null, game_title: play.title || null,
             avatar_drawn: pr.avatar.mode === "drawn" ? pr.avatar.parts : null,
             prefs: { dashboard: pr.dashboard, study: pr.study, avatar: pr.avatar },
             appearance: get(), preview: true };
  }

  // The header chip: picture + email, linking to Settings.
  function chip() {
    var email = document.getElementById("account-email");
    if (!email || email.closest(".account-chip")) return;
    var a = document.createElement("a");
    a.className = "account-chip"; a.href = "settings.html"; a.title = "Settings";
    a.setAttribute("aria-label", "Account settings");
    var av = document.createElement("span");
    av.className = "avatar avatar-sm"; av.id = "header-avatar"; av.setAttribute("aria-hidden", "true");
    email.parentNode.insertBefore(a, email);
    a.appendChild(av); a.appendChild(email);
    if (me) { avatar(av, me); if (me.email) email.textContent = me.email; }
  }
  function setMe(user) {
    me = user;
    if (user && user.appearance) set(user.appearance);
    if (user && user.prefs) setPrefs(user.prefs);
    avatar(document.getElementById("header-avatar"), user);
    if (user && user.email) { var e = document.getElementById("account-email"); if (e) e.textContent = user.email; }
    try { document.dispatchEvent(new CustomEvent("graphite:me", { detail: user })); } catch (e) { /* old browser */ }
  }

  var live = !!document.querySelector('meta[name="graphite-mode"][content="live"]');
  if (live && window.fetch) {
    fetch("/api/me", { credentials: "same-origin", headers: { Accept: "application/json" } })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (j) { if (j && j.user) setMe(j.user); })
      .catch(function () { /* offline: keep the saved look */ });
  } else {
    me = previewUser();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", chip); else chip();

  window.GraphiteTheme = {
    get: get, set: set, accents: ACCENTS, themes: THEMES, shopThemes: SHOP_THEMES, avatar: avatar, initials: initials,
    me: function () { return me; }, setMe: setMe, live: live, previewKey: PROFILE_KEY,
    prefs: prefs, setPrefs: setPrefs, defaults: DEFAULTS, drawAvatar: drawAvatar, reduceMotion: reduceMotion,
    contrastWith: function (h) { var c = rgb(h), bg = rgb(getComputedStyle(root).getPropertyValue("--bg").trim() || "#1c1e21"); return contrast(c, bg); },
    avatarParts: { bg: BG, skin: SKIN, hair_color: HAIR_COLOR, shirt: SHIRT, hair: HAIR, eyes: EYES, mouth: MOUTH, acc: ACC }
  };
})();
