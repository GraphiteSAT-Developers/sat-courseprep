/* Appearance for signed-in pages: theme (dark, light or match my device), accent color and the ripple
   background. Loaded at the top of the page, before anything is drawn, so there's no flash of the wrong
   colors. The last choice is kept in this browser so it applies instantly; on the live site the account's
   saved choice then takes over, so it follows the student to every device.
   Also turns the email in the header into a link to Settings, with the profile picture beside it. */
(function () {
  "use strict";
  var KEY = "graphite_appearance", PROFILE_KEY = "graphite_preview_profile";
  var THEMES = ["dark", "light", "system"], ACCENTS = ["pencil", "sky", "mint", "coral", "lilac", "rose", "blueprint", "ember"];  // the last three are bought in the shop
  var root = document.documentElement;
  var state = { theme: "dark", accent: "pencil", ripple: true };
  var mq = window.matchMedia ? window.matchMedia("(prefers-color-scheme: light)") : null;
  var me = null;

  function merge(s) {
    if (!s) return;
    if (THEMES.indexOf(s.theme) > -1) state.theme = s.theme;
    if (ACCENTS.indexOf(s.accent) > -1) state.accent = s.accent;
    if (typeof s.ripple === "boolean") state.ripple = s.ripple;
  }
  function resolved() { return state.theme === "system" ? (mq && mq.matches ? "light" : "dark") : state.theme; }
  function get() { return { theme: state.theme, accent: state.accent, ripple: state.ripple, resolved: resolved() }; }
  function apply() {
    root.setAttribute("data-theme", resolved());
    root.setAttribute("data-accent", state.accent);
    try { document.dispatchEvent(new CustomEvent("graphite:appearance", { detail: get() })); } catch (e) { /* old browser */ }
  }
  function set(s) {
    merge(s);
    try { localStorage.setItem(KEY, JSON.stringify({ theme: state.theme, accent: state.accent, ripple: state.ripple })); } catch (e) { /* storage blocked */ }
    apply();
  }

  try { merge(JSON.parse(localStorage.getItem(KEY) || "null")); } catch (e) { /* storage blocked */ }
  apply();
  if (mq) {
    var onSystem = function () { if (state.theme === "system") apply(); };
    if (mq.addEventListener) mq.addEventListener("change", onSystem); else if (mq.addListener) mq.addListener(onSystem);
  }

  /* ---------- profile picture ---------- */
  function initials(name) {
    var parts = String(name || "").trim().split(/\s+/).filter(Boolean);
    return ((parts[0] || "?").charAt(0) + (parts.length > 1 ? parts[parts.length - 1].charAt(0) : "")).toUpperCase();
  }
  // Fills a .avatar element with the photo, or the person's initials when there isn't one.
  function avatar(el, user) {
    if (!el) return;
    el.textContent = "";
    if (user && user.frame) el.setAttribute("data-frame", user.frame); else el.removeAttribute("data-frame");  // a frame from the shop
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
    return { name: p.name || fallback, email: p.email || who || "beta", avatar_url: p.avatar || null, role: role,
             frame: play.frame || null, game_title: play.title || null,
             appearance: get(), preview: true };
  }

  // The header chip: photo + email, linking to Settings.
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
    get: get, set: set, accents: ACCENTS, themes: THEMES, avatar: avatar, initials: initials,
    me: function () { return me; }, setMe: setMe, live: live, previewKey: PROFILE_KEY
  };
})();
