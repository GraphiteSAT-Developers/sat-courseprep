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
  var BASE = { dark: "dark", light: "light", system: "system", paper: "light", midnight: "dark", contrast: "dark", chalkboard: "dark", nightowl: "dark",
               sunrise: "light", sakura: "light", graph: "light", deepsea: "dark", espresso: "dark", plum: "dark" };
  var THEMES = Object.keys(BASE), SHOP_THEMES = ["chalkboard", "nightowl", "sunrise", "sakura", "graph", "deepsea", "espresso", "plum"];
  var ACCENTS = ["pencil", "sky", "mint", "coral", "lilac", "rose", "blueprint", "ember", "custom"];  // rose onward come from the shop
  var LOOK = { text: ["s", "m", "l", "xl"], font: ["default", "readable", "rounded", "mono"], motion: ["system", "reduce", "full"], density: ["comfortable", "compact"],
               corners: ["round", "soft", "sharp"], effect: ["none", "ripple", "dots", "snow", "constellation", "symbols", "waves", "fireflies", "warp", "springy", "pencil", "magnet", "graphpaper", "bubbles", "gravity"] };
  var FREE_EFFECTS = ["none", "dots"];  // Ripples is bought in the shop
  var DEFAULTS = {
    dashboard: { order: ["kpis", "play", "today", "scores", "domains", "review", "plan", "account"], hidden: [], pins: [] },
    study: { set_size: 10, timer: "show", calculator: "closed", colors: "graphite", sounds: true, reminder: false, reminder_hour: 16, tz: "America/New_York" },
    avatar: { mode: "photo", parts: { bg: "sky", skin: "s3", hair: "short", hair_color: "brown", eyes: "dots", mouth: "smile", acc: "none", shirt: "pencil", hat: "none", face: "none", outfit: "tee", backdrop: "solid" } }
  };
  var root = document.documentElement;
  var state = { theme: "dark", accent: "pencil", ripple: false, text: "m", font: "default", motion: "system", density: "comfortable", custom_accent: "#f2c14e",
                corners: "round", effect: "none" };
  var mq = window.matchMedia ? window.matchMedia("(prefers-color-scheme: light)") : null;
  var mqMotion = window.matchMedia ? window.matchMedia("(prefers-reduced-motion: reduce)") : null;
  var me = null, prefsCache = null;

  function merge(s) {
    if (!s) return;
    if (THEMES.indexOf(s.theme) > -1) state.theme = s.theme;
    if (ACCENTS.indexOf(s.accent) > -1) state.accent = s.accent;
    if (typeof s.ripple === "boolean") { state.ripple = s.ripple; if (!s.effect && !s.ripple) state.effect = "none"; }
    Object.keys(LOOK).forEach(function (k) { if (LOOK[k].indexOf(s[k]) > -1) state[k] = s[k]; });
    state.ripple = state.effect !== "none";
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
    root.setAttribute("data-corners", state.corners);
    root.setAttribute("data-effect", state.effect);
    loadReadableFont();
    try { document.dispatchEvent(new CustomEvent("graphite:appearance", { detail: get() })); } catch (e) { /* old browser */ }
  }
  function set(s) {
    merge(s);
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { /* storage blocked */ }
    apply();
  }

  try { merge(JSON.parse(localStorage.getItem(KEY) || "null")); } catch (e) { /* storage blocked */ }
  // A background bought in the shop shows only while it's owned. The live site's saved look already says so;
  // the preview checks its own shop (play-local.js) here, since Ripples used to be free.
  if (FREE_EFFECTS.indexOf(state.effect) < 0 && !document.querySelector('meta[name="graphite-mode"][content="live"]')) {
    var inv = {};
    try { inv = (JSON.parse(localStorage.getItem("graphite_play_v1") || "{}") || {}).inventory || {}; } catch (e) { /* storage blocked */ }
    if (!inv["effect:" + state.effect]) { state.effect = "none"; state.ripple = false; }
  }
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
    var saved = (p.avatar && p.avatar.parts) || {};
    out.avatar.parts = Object.assign({}, DEFAULTS.avatar.parts, saved);
    // Avatars saved before item slots existed had one accessory; move it to its slot (same as the server).
    var ap = out.avatar.parts;
    if (ap.acc && ap.acc !== "none" && !("hat" in saved) && !("face" in saved)) {
      if (HAT[ap.acc]) ap.hat = ap.acc; else if (FACE[ap.acc]) ap.face = ap.acc;
      ap.acc = "none";
    }
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
  // Item art by slot (backend/app/services/cosmetics.py has the names and prices).
  var HAT = {
    beanie: '<path d="M16.5 26C16.5 9 47.5 9 47.5 26Z" fill="#c94f4f"/><rect x="15.5" y="23" width="33" height="5" rx="2.5" fill="#a83c3c"/><circle cx="32" cy="9.5" r="3" fill="#e9e1d6"/>',
    cap: '<path d="M17.5 25C17.5 11.5 46.5 11.5 46.5 25Z" fill="#3a6fd8"/><path d="M17.5 25C12 25 8.5 26.5 8 28.5 13 28.8 16.5 27.8 19 26.5Z" fill="#2b55ad"/><circle cx="32" cy="12.4" r="1.6" fill="#2b55ad"/><path d="M24 14.5Q32 12 40 14.5" stroke="#5d8ce6" stroke-width="1.2" fill="none"/>',
    pencil: '<g transform="rotate(-35 47 22)"><rect x="44.5" y="10" width="5" height="20" fill="#f2c14e"/><rect x="44.5" y="10" width="5" height="3.5" fill="#ef7fb3"/><path d="M44.5 30h5l-2.5 5Z" fill="#e8c9a0"/><path d="M46.4 33.2h1.2l-.6 1.6Z" fill="' + INK + '"/></g>',
    headphones: '<path d="M16.5 31C16.5 11 47.5 11 47.5 31" fill="none" stroke="#2f3237" stroke-width="3"/><rect x="12.5" y="26" width="6.5" height="11" rx="3" fill="#2f3237"/><rect x="45" y="26" width="6.5" height="11" rx="3" fill="#2f3237"/>',
    gradcap: '<path d="M13 17L32 9.5 51 17 32 24.5Z" fill="#232528"/><path d="M21 20.5v5c6 4 16 4 22 0v-5L32 24.5Z" fill="#2f3237"/><path d="M48 18v9" stroke="#f2c14e" stroke-width="1.4"/><circle cx="48" cy="28" r="1.6" fill="#f2c14e"/>',
    catears: '<path d="M17.5 23L18.5 7 28.5 15.5Z" fill="#2f3237"/><path d="M46.5 23L45.5 7 35.5 15.5Z" fill="#2f3237"/><path d="M20 19.5L20.5 11.5 25.8 15.8Z" fill="#ef7fb3"/><path d="M44 19.5L43.5 11.5 38.2 15.8Z" fill="#ef7fb3"/>',
    flowers: '<g><circle cx="19" cy="21" r="3" fill="#f5a8c8"/><circle cx="24.5" cy="16.8" r="3" fill="#f7d774"/><circle cx="31" cy="15" r="3" fill="#9fe3c1"/><circle cx="37.5" cy="15.8" r="3" fill="#f5a8c8"/><circle cx="43" cy="19.2" r="3" fill="#c9b5f5"/><g fill="#fff8e7"><circle cx="19" cy="21" r="1"/><circle cx="24.5" cy="16.8" r="1"/><circle cx="31" cy="15" r="1"/><circle cx="37.5" cy="15.8" r="1"/><circle cx="43" cy="19.2" r="1"/></g></g>',
    tophat: '<rect x="22" y="1.5" width="20" height="16" rx="1.5" fill="#1f2124"/><rect x="22" y="12.5" width="20" height="3" fill="#c94f4f"/><rect x="14.5" y="16.5" width="35" height="3.6" rx="1.8" fill="#1f2124"/>',
    pirate: '<path d="M11 22C15 11 49 11 53 22 44 18.5 20 18.5 11 22Z" fill="#232528"/><path d="M13 22C22 25.5 42 25.5 51 22 46 27.5 18 27.5 13 22Z" fill="#2f3237"/><circle cx="32" cy="16.5" r="2.3" fill="#f4f4f4"/><path d="M30.6 19.2l2.8 2M33.4 19.2l-2.8 2" stroke="#f4f4f4" stroke-width=".9"/>',
    propeller: '<path d="M17.5 25C17.5 12 46.5 12 46.5 25Z" fill="#3fb87f"/><path d="M17.5 25C17.5 12 32 12 32 25Z" fill="#f2c14e"/><rect x="31.2" y="6" width="1.6" height="7" fill="#2f3237"/><g class="av-spin" style="transform-origin:32px 6px"><ellipse cx="25.5" cy="6" rx="6.5" ry="1.6" fill="#ec6f58"/><ellipse cx="38.5" cy="6" rx="6.5" ry="1.6" fill="#4f9be0"/></g>',
    viking: '<path d="M17 25C17 11 47 11 47 25Z" fill="#9aa6b5"/><rect x="16" y="22.5" width="32" height="4" rx="2" fill="#7b8696"/><path d="M17.5 21C12 19 9 13 10 6 13 12 16 14 20 15Z" fill="#efe6d2"/><path d="M46.5 21C52 19 55 13 54 6 51 12 48 14 44 15Z" fill="#efe6d2"/><circle cx="32" cy="14" r="1.6" fill="#7b8696"/>',
    wizard: '<path d="M18.5 24L34 1 45.5 24Z" fill="#5b3fb5"/><path d="M14 23.5h36a2.5 2.5 0 0 1 0 5H14a2.5 2.5 0 0 1 0-5Z" fill="#46309a"/><path d="M31.5 11l1 2.2 2.4.3-1.8 1.6.6 2.4-2.2-1.3-2.1 1.3.5-2.4-1.8-1.6 2.4-.3Z" fill="#f2c14e"/><circle cx="38" cy="18" r="1" fill="#f7d774"/>',
    halo: '<ellipse cx="32" cy="9.5" rx="12.5" ry="3.4" fill="none" stroke="#f7d774" stroke-width="2.6" class="av-glow"/>',
    astronaut: '<circle cx="32" cy="29" r="19.5" fill="#bfe3ff" fill-opacity=".22" stroke="#e8eef6" stroke-width="2.6"/><path d="M19.5 20.5a14.5 14.5 0 0 1 9-6.5" stroke="#fff" stroke-width="2.2" fill="none" stroke-linecap="round" opacity=".85"/><rect x="15.5" y="44.5" width="33" height="5" rx="2.5" fill="#d7dde6"/>',
    crown: '<path d="M20 19L21.5 8 27 13.5 32 6 37 13.5 42.5 8 44 19Z" fill="#e3a92b" stroke="#a8760f" stroke-width="1"/><circle cx="32" cy="14" r="1.6" fill="#ec6f58"/><circle cx="24.5" cy="16" r="1.1" fill="#4f9be0"/><circle cx="39.5" cy="16" r="1.1" fill="#3fb87f"/>'
  };
  var FACE = {
    glasses: '<g fill="none" stroke="' + INK + '" stroke-width="1.4"><circle cx="26" cy="30" r="4.4"/><circle cx="38" cy="30" r="4.4"/><path d="M30.4 30h3.2M21.6 29.5l-3.4-1M42.4 29.5l3.4-1"/></g>',
    sunglasses: '<g fill="' + INK + '"><rect x="21" y="27" width="9.5" height="6.5" rx="2.5"/><rect x="33.5" y="27" width="9.5" height="6.5" rx="2.5"/><rect x="30" y="28.5" width="4" height="1.4"/></g>',
    monocle: '<circle cx="38" cy="30" r="4.6" fill="#ffffff" fill-opacity=".25" stroke="#c9a227" stroke-width="1.5"/><path d="M42.3 32.5q2.5 6 -1 11" fill="none" stroke="#c9a227" stroke-width=".9"/>',
    starshades: '<g fill="#ef7fb3" stroke="#b0306d" stroke-width=".7"><path d="M26 24.6l1.6 3.4 3.7.4-2.8 2.5.8 3.6-3.3-1.9-3.2 1.9.8-3.6-2.8-2.5 3.7-.4Z"/><path d="M38 24.6l1.6 3.4 3.7.4-2.8 2.5.8 3.6-3.3-1.9-3.2 1.9.8-3.6-2.8-2.5 3.7-.4Z"/></g><path d="M30.5 29h3" stroke="#b0306d" stroke-width="1"/>',
    mask: '<path d="M17.5 26.5C24 24.4 40 24.4 46.5 26.5L45.5 33.4C40 34.6 36 31.2 32 31.2S24 34.6 18.5 33.4Z" fill="#c94f4f"/><ellipse cx="26" cy="29.6" rx="3" ry="1.9" fill="#fff"/><ellipse cx="38" cy="29.6" rx="3" ry="1.9" fill="#fff"/><circle cx="26" cy="29.8" r="1.1" fill="' + INK + '"/><circle cx="38" cy="29.8" r="1.1" fill="' + INK + '"/>',
    visor: '<rect x="16.5" y="25" width="31" height="10" rx="4.5" fill="#111827"/><rect x="18.5" y="27" width="27" height="6" rx="3" fill="#5fd8ea" class="av-glow"/>',
    scanner: '<rect x="16.5" y="27" width="31" height="6" rx="3" fill="#1d1a19"/><rect x="18.5" y="28.6" width="7" height="2.8" rx="1.4" fill="#ff5a5a" class="av-scan"/>'
  };
  // Outfits draw over the shirt (s = the shirt color).
  var OUTFIT = {
    hoodie: function (s) { return '<path d="M19 48.5c3.5-4.5 22.5-4.5 26 0" fill="none" stroke="rgba(0,0,0,.25)" stroke-width="3.2"/><path d="M29.5 50v7.5M34.5 50v7.5" stroke="#f4f4f4" stroke-width="1.2" stroke-linecap="round"/><rect x="24" y="57" width="16" height="7" rx="2" fill="rgba(0,0,0,.14)"/>'; },
    vest: function () { return '<path d="M18 48.5C22 46 26 45.5 28 45.6L32 52 36 45.6C38 45.5 42 46 46 48.5L44 64H20Z" fill="#7a5a3a"/><path d="M22 54l4 4 4-4 4 4 4-4 4 4M22 60l4-4 4 4 4-4 4 4 4-4" stroke="#a37b52" stroke-width="1" fill="none"/>'; },
    jersey: function (s) { return '<path d="M12.5 54C14 50 17 48 20 47M51.5 54C50 50 47 48 44 47" stroke="#f4f4f4" stroke-width="2.4" fill="none"/><text x="32" y="61" text-anchor="middle" font-size="12" font-weight="800" font-family="Arial, sans-serif" fill="#f4f4f4">1</text>'; },
    varsity: function () { return '<path d="M9 64C10.5 54 15 49 21 47L23 64Z" fill="#f4f4f4"/><path d="M55 64C53.5 54 49 49 43 47L41 64Z" fill="#f4f4f4"/><path d="M27.5 46.5L32 53 36.5 46.5" fill="none" stroke="#f4f4f4" stroke-width="1.6"/><text x="32" y="62" text-anchor="middle" font-size="8.5" font-weight="800" font-family="Arial, sans-serif" fill="#f4f4f4">G</text>'; },
    labcoat: function () { return '<path d="M9 64C11 50 21 45.5 32 45.5S53 50 55 64Z" fill="#f4f6f8"/><path d="M27 46l5 9 5-9" fill="none" stroke="#cfd6de" stroke-width="1.6"/><path d="M32 55v9" stroke="#cfd6de" stroke-width="1.2"/><rect x="38" y="56" width="6" height="4" rx="1" fill="#dfe4ea"/><rect x="40.5" y="54" width="1.2" height="4" fill="#4f9be0"/>'; },
    suit: function () { return '<path d="M9 64C11 50 21 45.5 32 45.5S53 50 55 64Z" fill="#2b2f36"/><path d="M27 46h10l-5 10Z" fill="#f4f4f4"/><path d="M31 48.5h2l1.2 10-2.2 2.2-2.2-2.2Z" fill="#c94f4f"/><path d="M27 46l3 10M37 46l-3 10" stroke="#1f2228" stroke-width="1"/>'; },
    cape: function () { return '<g class="av-flutter"><path d="M9 64L12.5 49 19 46.5 15 64Z" fill="#c94f4f"/><path d="M55 64L51.5 49 45 46.5 49 64Z" fill="#c94f4f"/></g><circle cx="22" cy="48" r="1.6" fill="#f2c14e"/><circle cx="42" cy="48" r="1.6" fill="#f2c14e"/>'; },
    spacesuit: function () { return '<path d="M9 64C11 50 21 45.5 32 45.5S53 50 55 64Z" fill="#e8eef6"/><rect x="26" y="53" width="12" height="7" rx="1.5" fill="#c9d3df"/><circle cx="29" cy="56.5" r="1.1" fill="#ec6f58"/><circle cx="32" cy="56.5" r="1.1" fill="#3fb87f"/><circle cx="35" cy="56.5" r="1.1" fill="#4f9be0"/><rect x="15" y="52" width="5" height="3" rx="1" fill="#4f9be0"/>'; },
    armor: function () { return '<path d="M9 64C11 50 21 45.5 32 45.5S53 50 55 64Z" fill="#8f9aa8"/><path d="M14 52c4-4 10-5.5 18-5.5S46 48 50 52" fill="none" stroke="#b8c2ce" stroke-width="2"/><path d="M32 47v17" stroke="#6e7886" stroke-width="1.4"/><path d="M27 56h10l-5 6Z" fill="#e3a92b"/><rect x="18" y="50" width="6" height="12" rx="2" fill="#ffffff" opacity=".22" class="av-shine"/>'; }
  };
  // Backdrops replace the plain background (c = the background color).
  var BACKDROP = {
    graph: function (c) { var g = ""; for (var i = 4; i < 64; i += 6) g += '<path d="M' + i + ' 0V64M0 ' + i + 'H64"/>'; return '<rect width="64" height="64" fill="' + c + '"/><g stroke="#ffffff" stroke-opacity=".45" stroke-width=".6">' + g + "</g>"; },
    confetti: function (c) { var r = ""; [[6,8,"#ec6f58"],[50,6,"#4f9be0"],[12,40,"#3fb87f"],[54,30,"#f7d774"],[8,22,"#9b7be6"],[56,48,"#ef7fb3"],[44,14,"#3fb87f"],[18,54,"#f7d774"]].forEach(function (p, i) { r += '<rect x="' + p[0] + '" y="' + p[1] + '" width="3.2" height="1.6" rx=".6" fill="' + p[2] + '" transform="rotate(' + (i * 37) + " " + p[0] + " " + p[1] + ')"/>'; }); return '<rect width="64" height="64" fill="' + c + '"/>' + r; },
    chalkboard: function () { return '<rect width="64" height="64" fill="#2f4a3a"/><g fill="#e8efe9" fill-opacity=".55" font-family="Arial, sans-serif" font-size="5"><text x="3" y="9">x²+y²</text><text x="44" y="11">πr²</text><text x="2" y="58">a+b</text><text x="48" y="58">√2</text></g>'; },
    waves: function () { return '<rect width="64" height="64" fill="#7fc4e8"/><path d="M0 46q8-4 16 0t16 0 16 0 16 0V64H0Z" fill="#4f9be0"/><path d="M0 54q8-4 16 0t16 0 16 0 16 0V64H0Z" fill="#3a7fc4"/>'; },
    sunset: function () { return '<rect width="64" height="64" fill="#f8bf9a"/><rect y="0" width="64" height="14" fill="#9b7be6"/><rect y="14" width="64" height="12" fill="#ef7fb3"/><rect y="26" width="64" height="12" fill="#ec8f58"/><circle cx="52" cy="40" r="8" fill="#f7d774"/>'; },
    stars: function () { var s = ""; [[8,8],[20,4],[52,10],[58,22],[6,30],[56,40],[12,50],[48,56],[30,6],[40,3]].forEach(function (p, i) { s += '<circle cx="' + p[0] + '" cy="' + p[1] + '" r="' + (i % 3 ? 0.8 : 1.2) + '" fill="#fff" class="' + (i % 2 ? "av-twinkle" : "av-twinkle2") + '"/>'; }); return '<rect width="64" height="64" fill="#1b2340"/>' + s; },
    circuit: function () { return '<rect width="64" height="64" fill="#0f3b3a"/><g stroke="#3fd6b0" stroke-width="1" fill="none" opacity=".7"><path d="M0 12h10l4 4h8M64 18H52l-4-4h-6M0 50h8l5-5h6M64 46h-9l-4 4h-7M10 0v6M54 64v-8"/></g><g fill="#3fd6b0"><circle cx="22" cy="16" r="1.4"/><circle cx="42" cy="14" r="1.4"/><circle cx="19" cy="45" r="1.4"/><circle cx="44" cy="50" r="1.4" class="av-glow"/></g>'; },
    galaxy: function () { return '<rect width="64" height="64" fill="#140f2b"/><g fill="#fff"><circle cx="7" cy="9" r=".9"/><circle cx="57" cy="14" r="1.1" class="av-twinkle"/><circle cx="12" cy="44" r=".8"/><circle cx="50" cy="52" r=".9" class="av-twinkle2"/><circle cx="34" cy="5" r=".7"/></g><circle cx="52" cy="34" r="6" fill="#ec8f58"/><ellipse cx="52" cy="34" rx="10.5" ry="2.6" fill="none" stroke="#f7d774" stroke-width="1.2" transform="rotate(-18 52 34)"/><circle cx="10" cy="24" r="3" fill="#7fcfcf"/>'; },
    fire: function () { return '<rect width="64" height="64" fill="#2a0f0a"/><g class="av-flicker"><path d="M4 64C2 52 10 48 8 38 14 44 16 50 15 56 18 50 18 44 22 40 22 50 28 54 26 64Z" fill="#ec6f58"/><path d="M60 64C62 52 54 48 56 38 50 44 48 50 49 56 46 50 46 44 42 40 42 50 36 54 38 64Z" fill="#ec6f58"/></g><g class="av-flicker2"><path d="M8 64C7 56 12 54 11 48 15 52 17 58 16 64Z" fill="#f7d774"/><path d="M56 64C57 56 52 54 53 48 49 52 47 58 48 64Z" fill="#f7d774"/></g>'; }
  };
  var ACC = Object.assign({}, HAT, FACE);  // the old single-accessory slot, for avatars saved before slots
  function drawAvatar(p, label) {
    p = Object.assign({}, DEFAULTS.avatar.parts, p || {});
    if (p.acc && p.acc !== "none" && (!p.hat || p.hat === "none") && (!p.face || p.face === "none")) { if (HAT[p.acc]) p.hat = p.acc; else if (FACE[p.acc]) p.face = p.acc; }
    var hair = HAIR[p.hair] || ["", ""], hc = HAIR_COLOR[p.hair_color] || HAIR_COLOR.brown, skin = SKIN[p.skin] || SKIN.s3;
    var bg = BG[p.bg] || BG.sky, shirt = SHIRT[p.shirt] || SHIRT.pencil;
    var covered = ["beanie", "gradcap", "cap", "tophat", "pirate", "propeller", "viking", "wizard"].indexOf(p.hat) > -1;
    var outfit = OUTFIT[p.outfit], back = BACKDROP[p.backdrop];
    return '<svg viewBox="0 0 64 64" class="drawn-avatar" role="img" aria-label="' + (label || "Avatar") + '">' +
      (back ? back(bg) : '<rect width="64" height="64" fill="' + bg + '"/>') +
      (hair[0] ? '<g fill="' + hc + '">' + hair[0] + "</g>" : "") +
      '<path d="M9 64C11 50 21 45.5 32 45.5S53 50 55 64Z" fill="' + shirt + '"/>' + (outfit ? outfit(shirt) : "") +
      '<rect x="28" y="38" width="8" height="9" rx="3" fill="' + skin + '"/>' +
      '<circle cx="18.5" cy="31" r="3" fill="' + skin + '"/><circle cx="45.5" cy="31" r="3" fill="' + skin + '"/>' +
      '<circle cx="32" cy="29" r="14" fill="' + skin + '"/>' +
      (hair[1] && !covered ? '<g fill="' + hc + '">' + hair[1] + "</g>" : "") +
      (EYES[p.eyes] || EYES.dots) + (MOUTH[p.mouth] || MOUTH.smile) + (FACE[p.face] || "") + (HAT[p.hat] || "") + "</svg>";
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
    avatarParts: { bg: BG, skin: SKIN, hair_color: HAIR_COLOR, shirt: SHIRT, hair: HAIR, eyes: EYES, mouth: MOUTH, acc: ACC,
                   hat: HAT, face: FACE, outfit: OUTFIT, backdrop: BACKDROP },
    freeEffects: FREE_EFFECTS
  };
})();
