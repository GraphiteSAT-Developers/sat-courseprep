/* Graphite word filter: no curse words in any text box. The same rules as backend/app/services/wordfilter.py,
   from the same list (backend/app/content/blocked_words.txt, ROT13). build.py fills in WORDS.
   Every text box and text area is checked as you type and before its form sends. Boxes where it doesn't
   apply (passwords, sign-in emails, codes, answers) carry data-no-filter. The server checks again. */
(function () {
  "use strict";
  var WORDS = ["*shpx", "*zbgures", "*avttre", "*avttn", "*snttbg", "*pbpxfhpx", "*qvyqb", "*wvmm", "~fuvg", "~ovgpu", "~onfgneq", "~nffubyr", "~nffung", "~qvpxurnq", "~wnpxnff", "~qhzonff", "~juber", "~fyhg", "~ergneq", "~cbea", "~qbhpur", "~tbqqnza", "~gjng", "~phag", "~obyybpx", "~fxnax", "nff", "nefr", "qvpx", "pbpx", "cvff", "cevpx", "qnza", "gvgf", "gvggl", "obbof", "snt", "xlf", "fcvp", "puvax", "xvxr", "jrgonpx", "genaal", "jnax", "chffl", "gubg", "cravf", "intvan", "frk", "frkl", "ahqr", "ahqrf", "penc"];
  var MESSAGE = "Please keep it clean. That has a word we don't allow.";
  var LEET = { "0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "7": "t", "@": "a", "$": "s", "!": "i", "|": "i" };
  var ENDINGS = ["ings", "ing", "ers", "er", "ed", "es", "s", "y", "ier", "iest", "in"];

  function rot13(s) { return s.replace(/[a-z]/gi, function (c) { var b = c <= "Z" ? 65 : 97; return String.fromCharCode((c.charCodeAt(0) - b + 13) % 26 + b); }); }
  function esc(c) { return c.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }
  function pattern(w) { return w.split("").map(function (c) { return "aeiou".indexOf(c) > -1 ? "[" + c + "*]" : esc(c); }).join(""); }
  var LIST = (Array.isArray(WORDS) ? WORDS : []).map(function (line) {
    var mode = line[0] === "*" ? "any" : line[0] === "~" ? "edge" : "word";
    var p = pattern(rot13(line.replace(/^[*~]/, "")).toLowerCase());
    return { mode: mode, any: new RegExp(p), whole: new RegExp("^" + p + "$"), start: new RegExp("^" + p), end: new RegExp(p + "$") };
  });

  function squeeze(t, atLeast) { return t.replace(new RegExp("(.)\\1{" + (atLeast - 1) + ",}", "g"), "$1"); }
  function tokens(text) {
    var t = String(text || "").normalize ? String(text || "").normalize("NFKD") : String(text || "");
    t = t.replace(/[̀-ͯ]/g, "").toLowerCase().replace(/[013457@$!|]/g, function (c) { return LEET[c]; });
    var parts = t.match(/[a-z*]+/g) || [], out = [], run = [];
    parts.concat([""]).forEach(function (p) {
      if (p.length === 1) { run.push(p); return; }      // f u c k, f.u.c.k
      if (run.length > 1) out.push(run.join("")); else out = out.concat(run);
      run = [];
      if (p) out.push(p);
    });
    return out;
  }
  function stems(t) {
    var out = [t];
    ENDINGS.forEach(function (e) { if (t.length - e.length >= 2 && t.slice(-e.length) === e) out.push(t.slice(0, -e.length)); });
    return out;
  }
  function hit(token) {
    var stretched = squeeze(token, 3);
    return LIST.some(function (w) {
      if (w.mode === "any") return [token, stretched, squeeze(token, 2)].some(function (t) { return w.any.test(t); });
      return [token, stretched].some(function (t) {
        return stems(t).some(function (s) { return w.mode === "word" ? w.whole.test(s) : (w.start.test(s) || w.end.test(s)); });
      });
    });
  }
  function isClean(text) { return !tokens(text).some(hit); }
  window.GraphiteWords = { isClean: isClean, message: MESSAGE };

  /* ---------- every text box ---------- */
  var SKIP = '[data-no-filter], [type="password"], [aria-hidden="true"], .hp input, [tabindex="-1"]';
  function checkable(el) {
    if (!el || !el.matches) return false;
    var text = el.tagName === "TEXTAREA" || (el.tagName === "INPUT" && /^(text|email|search|)$/.test(el.type || ""));
    return text && !el.matches(SKIP) && !el.closest("[data-no-filter]");
  }
  function errorEl(el) {
    var id = (el.id || el.name || "field") + "-clean", e = document.getElementById(id);
    if (!e) {
      e = document.createElement("p"); e.id = id; e.className = "field-error wf-error"; e.setAttribute("role", "alert"); e.hidden = true;
      var box = el.closest(".field") || el.parentNode;
      if (box === el.parentNode) el.insertAdjacentElement("afterend", e); else box.appendChild(e);
    }
    return e;
  }
  function value(el) { return el.type === "email" ? String(el.value).split("@")[0] : el.value; }
  function check(el) {
    var bad = !isClean(value(el)), e = document.getElementById((el.id || el.name || "field") + "-clean");
    if (!bad && !e) return true;
    e = e || errorEl(el);
    e.textContent = bad ? MESSAGE : ""; e.hidden = !bad;
    if (el.setCustomValidity) el.setCustomValidity(bad ? MESSAGE : "");
    var d = (el.getAttribute("aria-describedby") || "").split(" ").filter(function (x) { return x && x !== e.id; });
    if (bad) { d.push(e.id); el.setAttribute("aria-invalid", "true"); } else if (el.getAttribute("aria-invalid") === "true" && !el.validationMessage) el.removeAttribute("aria-invalid");
    if (d.length) el.setAttribute("aria-describedby", d.join(" ")); else el.removeAttribute("aria-describedby");
    return !bad;
  }
  var timer = null;
  document.addEventListener("input", function (ev) {
    var el = ev.target; if (!checkable(el)) return;
    clearTimeout(timer); timer = setTimeout(function () { check(el); }, 250);
  });
  document.addEventListener("blur", function (ev) { if (checkable(ev.target)) check(ev.target); }, true);
  // Before any form's own submit handler: stop it if a box has a blocked word.
  document.addEventListener("submit", function (ev) {
    var form = ev.target, first = null;
    Array.prototype.forEach.call(form.querySelectorAll("input, textarea"), function (el) { if (checkable(el) && !check(el) && !first) first = el; });
    if (first) { ev.preventDefault(); ev.stopImmediatePropagation(); first.focus(); }
  }, true);
})();

/* Graphite site script. Edit CONFIG to connect real services. */
(function () {
  "use strict";

  // Live mode: pages served by the Graphite backend (backend/) carry <meta name="graphite-mode" content="live">
  // and talk to its API. Without it (a static preview), forms behave as a demo and nothing is sent.
  var LIVE = !!document.querySelector('meta[name="graphite-mode"][content="live"]');

  var CONFIG = {
    // POST endpoint for the "Start free diagnostic" form. When null, the form validates and shows the success message without sending.
    formEndpoint: LIVE ? "/api/leads" : null,
    // POST endpoint for sign in. When null, any well-formed email and 8+ character password signs in.
    authEndpoint: LIVE ? "/api/auth/login" : null,
    // Where to send students after a successful sign in. Set to null to stay on the sign-in page.
    dashboardUrl: "dashboard.html",
    // Analytics loads only after the visitor accepts analytics cookies.
    // provider: "plausible" (set domain) or "ga4" (set measurementId), or null for none.
    analytics: { provider: null, domain: "", measurementId: "", endpoint: null },
    consentKey: "graphite_consent",
    consentVersion: 1
  };

  /* 1. Force HTTPS outside local development */
  var host = location.hostname;
  var isLocal = /^(localhost|127\.0\.0\.1|\[::1\]|.*\.localhost|.*\.test)$/.test(host) || host === "";
  if (location.protocol === "http:" && !isLocal) {
    location.replace("https:" + location.href.slice(location.protocol.length));
    return;
  }

  /* Storage helpers that never throw */
  var store = {
    get: function (k) { try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* storage blocked */ } }
  };

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $all(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

  /* 2. Copyright year */
  $all("[data-year]").forEach(function (el) { el.textContent = String(new Date().getFullYear()); });

  /* 3. Mobile menu */
  var toggle = $(".menu-toggle");
  var nav = $("#site-nav");
  // Mark the app tab for this page (Practice, Level up); the dashboard's tabs are sections of one page.
  if (nav) {
    var here = location.pathname.split("/").pop() || "index.html";
    $all("a", nav).forEach(function (a) { if ((a.getAttribute("href") || "").replace(/^.*\//, "") === here) a.setAttribute("aria-current", "page"); });
  }
  function closeMenu() {
    if (!toggle || !nav) return;
    toggle.setAttribute("aria-expanded", "false");
    toggle.querySelector(".menu-label").textContent = "Menu";
    nav.classList.remove("is-open");
  }
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      toggle.querySelector(".menu-label").textContent = open ? "Menu" : "Close";
      nav.classList.toggle("is-open", !open);
    });
    $all("a", nav).forEach(function (a) { a.addEventListener("click", closeMenu); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) { closeMenu(); toggle.focus(); }
    });
    window.matchMedia("(min-width: 901px)").addEventListener("change", function (m) { if (m.matches) closeMenu(); });
  }

  /* 4. Analytics (consent-gated) */
  var Analytics = {
    on: false,
    enable: function () {
      if (this.on) return;
      this.on = true;
      var a = CONFIG.analytics, s;
      if (a.provider === "plausible" && a.domain) {
        s = document.createElement("script");
        s.defer = true; s.src = "https://plausible.io/js/script.js"; s.setAttribute("data-domain", a.domain);
        document.head.appendChild(s);
      } else if (a.provider === "ga4" && a.measurementId) {
        s = document.createElement("script");
        s.async = true; s.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(a.measurementId);
        document.head.appendChild(s);
        window.dataLayer = window.dataLayer || [];
        window.gtag = function () { window.dataLayer.push(arguments); };
        window.gtag("js", new Date());
        window.gtag("config", a.measurementId, { anonymize_ip: true });
      }
      this.track("pageview", { path: location.pathname });
    },
    track: function (name, props) {
      if (!this.on) return;
      props = props || {};
      if (window.plausible) window.plausible(name, { props: props });
      if (window.gtag) window.gtag("event", name, props);
      if (CONFIG.analytics.endpoint && navigator.sendBeacon) {
        navigator.sendBeacon(CONFIG.analytics.endpoint, JSON.stringify({ event: name, props: props, t: Date.now() }));
      }
    }
  };
  document.addEventListener("click", function (e) {
    var t = e.target.closest && e.target.closest("[data-track]");
    if (t) Analytics.track(t.getAttribute("data-track"), { label: (t.textContent || "").trim().slice(0, 60) });
  });

  /* 5. Cookie consent banner */
  var banner = $("#cookie-banner");
  function applyConsent(c) { if (c && c.analytics) Analytics.enable(); }
  function saveConsent(analytics) {
    var c = { v: CONFIG.consentVersion, analytics: !!analytics, at: new Date().toISOString() };
    store.set(CONFIG.consentKey, c);
    applyConsent(c);
    if (banner) banner.hidden = true;
    var live = $("#cookie-live");
    if (live) live.textContent = analytics ? "Saved. Analytics cookies are on." : "Saved. Only essential cookies are on.";
  }
  if (banner) {
    var existing = store.get(CONFIG.consentKey);
    if (existing && existing.v === CONFIG.consentVersion) { applyConsent(existing); }
    else { banner.hidden = false; }
    var prefs = $("#cookie-prefs", banner);
    var analyticsBox = $("#consent-analytics", banner);
    $("#cookie-accept", banner).addEventListener("click", function () { saveConsent(true); });
    $("#cookie-reject", banner).addEventListener("click", function () { saveConsent(false); });
    $("#cookie-choose", banner).addEventListener("click", function () {
      prefs.hidden = !prefs.hidden;
      this.setAttribute("aria-expanded", String(!prefs.hidden));
    });
    $("#cookie-save", banner).addEventListener("click", function () { saveConsent(analyticsBox.checked); });
    $all("[data-cookie-settings]").forEach(function (b) {
      b.addEventListener("click", function () {
        var c = store.get(CONFIG.consentKey);
        analyticsBox.checked = !!(c && c.analytics);
        banner.hidden = false; prefs.hidden = false;
        $("#cookie-choose", banner).setAttribute("aria-expanded", "true");
        analyticsBox.focus();
      });
    });
  }

  /* 6. Copy buttons (phone, email) */
  $all("[data-copy]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var text = btn.getAttribute("data-copy");
      var done = function (msg) { var old = btn.textContent; btn.textContent = msg; setTimeout(function () { btn.textContent = old; }, 1600); };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function () { done("Copied"); }, function () { selectText(btn); done("Select + copy"); });
      } else { selectText(btn); done("Select + copy"); }
    });
  });
  function selectText(btn) {
    var target = btn.parentNode.querySelector("a");
    if (!target || !window.getSelection) return;
    var r = document.createRange(); r.selectNodeContents(target);
    var sel = window.getSelection(); sel.removeAllRanges(); sel.addRange(r);
  }

  /* 7. Form helpers: validation, spam protection, status messages */
  var EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  var TEST_USERNAME = "beta", TEST_PARENT = "beta2";  // local test accounts (backend/app/testaccount.py)

  function setError(field, msg) {
    var input = field.querySelector("input, select, textarea");
    var err = field.querySelector(".field-error");
    if (!err) { err = document.createElement("p"); err.className = "field-error"; err.id = input.id + "-error"; field.appendChild(err); }
    err.textContent = msg || "";
    err.hidden = !msg;
    input.setAttribute("aria-invalid", msg ? "true" : "false");
    var described = (input.getAttribute("aria-describedby") || "").split(" ").filter(function (x) { return x && x !== err.id; });
    if (msg) described.push(err.id);
    if (described.length) input.setAttribute("aria-describedby", described.join(" ")); else input.removeAttribute("aria-describedby");
  }
  function showStatus(el, kind, title, detail) {
    el.className = "status is-shown " + kind;
    el.innerHTML = "";
    var p = document.createElement("p"); p.textContent = title; el.appendChild(p);
    if (detail) { var d = document.createElement("p"); d.textContent = detail; el.appendChild(d); }
    el.focus();
  }
  function clearStatus(el) { el.className = "status"; el.textContent = ""; }

  // Spam checks: a hidden honeypot field, a minimum fill time, and a per-browser rate limit.
  function spamCheck(form, key, maxPerWindow, windowMs) {
    var hp = form.querySelector(".hp input");
    if (hp && hp.value) return "blocked";
    var started = Number(form.getAttribute("data-started") || 0);
    if (Date.now() - started < 3000) return "too-fast";
    var log = (store.get(key) || []).filter(function (t) { return Date.now() - t < windowMs; });
    if (log.length >= maxPerWindow) return "rate";
    log.push(Date.now()); store.set(key, log);
    return null;
  }
  $all("form[data-guard]").forEach(function (f) {
    f.setAttribute("data-started", String(Date.now()));
  });

  /* Bot protection for sign-up, password resets and the home page form (backend: app/botcheck.py).
     A short-lived token from the server goes with each one, and the server refuses forms sent back faster than a
     person could fill them in. When the site has Cloudflare Turnstile keys, its check is added to those forms too. */
  var BOT = { token: null, site: null, widgets: {} };
  var BOT_FORMS = { "/api/auth/register": "#create-form", "/api/leads": "#start-form", "/api/auth/forgot": "#reset-form" };
  function loadBotCheck() {
    if (!LIVE || !Object.keys(BOT_FORMS).some(function (k) { return document.querySelector(BOT_FORMS[k]); })) return;
    fetch("/api/auth/form-token", { credentials: "same-origin", headers: { Accept: "application/json" } }).then(function (r) { return r.json(); }).then(function (j) {
      BOT.token = j.token; BOT.site = j.turnstile_site_key;
      if (!BOT.site) return;
      window.graphiteTurnstile = function () {
        Object.keys(BOT_FORMS).forEach(function (path) {
          var form = document.querySelector(BOT_FORMS[path]); if (!form || !window.turnstile) return;
          var box = document.createElement("div"); box.className = "turnstile-box";
          var btn = form.querySelector('button[type="submit"]'); (btn ? btn.parentNode : form).insertBefore(box, btn || null);
          BOT.widgets[path] = window.turnstile.render(box, { sitekey: BOT.site, theme: "dark", appearance: "interaction-only" });
        });
      };
      var sc = document.createElement("script");
      sc.src = "https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit&onload=graphiteTurnstile"; sc.async = true;
      document.head.appendChild(sc);
    }).catch(function () { /* the server says what's missing if a form is sent without it */ });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", loadBotCheck); else loadBotCheck();

  // Calls the backend. Resolves with the JSON body; rejects with an Error carrying .status and the server's message.
  function api(path, data, method) {
    if (data && BOT_FORMS[path]) {
      data = Object.assign({}, data, { form_token: BOT.token });
      if (BOT.widgets[path] !== undefined && window.turnstile) {
        data.turnstile = window.turnstile.getResponse(BOT.widgets[path]) || "";
        try { window.turnstile.reset(BOT.widgets[path]); } catch (e) { /* widget gone */ }
      }
    }
    var opts = { method: method || (data ? "POST" : "GET"), headers: { "Accept": "application/json" }, credentials: "same-origin" };
    if (data) { opts.headers["Content-Type"] = "application/json"; opts.body = JSON.stringify(data); }
    return fetch(path, opts).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (j) {
        if (!r.ok) { var err = new Error(j.error || "Request failed."); err.status = r.status; err.data = j; throw err; }
        return j;
      });
    });
  }
  window.GraphiteAPI = { live: LIVE, call: api };
  // Signed-in pages note that they were opened, for the student's own history (Settings > History).
  if (LIVE && document.querySelector('.site-nav[aria-label="Dashboard"]')) {
    api("/api/me/history/view", { page: location.pathname }).catch(function () { /* not signed in, or offline: nothing to save */ });
  }

  function send(endpoint, data) {
    if (!endpoint) return new Promise(function (resolve) { setTimeout(function () { resolve({}); }, 600); });
    return api(endpoint, data);
  }
  function networkMessage(err) {
    return err && err.status ? err.message : "We couldn't reach Graphite. Check your connection and try again.";
  }
  // Puts a server-side field error next to the matching input. fieldMap: { serverField: inputId }.
  function showFieldError(err, fieldMap) {
    var field = err && err.data && err.data.field;
    var id = field && fieldMap[field];
    var input = id && document.getElementById(id);
    if (input) { setError(input.closest(".field"), err.message); input.focus(); }
  }
  function safeNext() {
    var next = new URLSearchParams(location.search).get("next") || "";
    // A page on this site, optionally with simple settings after "?" (checkout.html?plan=sharpened&interval=year).
    if (!/^\/[a-z0-9-]+\.html(\?[a-z0-9=&_%.-]*)?$/i.test(next)) return CONFIG.dashboardUrl;
    return LIVE ? next : next.slice(1);  // the preview's pages sit side by side, so links there are relative
  }

  /* 7a. Diagnostic signup form */
  var signup = $("#start-form");
  if (signup) {
    var sStatus = $("#start-status");
    signup.addEventListener("submit", function (e) {
      e.preventDefault();
      clearStatus(sStatus);
      var ok = true;
      var name = $("#start-name"), email = $("#start-email"), grade = $("#start-grade"), target = $("#start-target"), agree = $("#start-agree");
      setError(name.parentNode, name.value.trim() ? "" : "Enter the student's first name.") ;
      if (!name.value.trim()) ok = false;
      var em = email.value.trim();
      var emMsg = !em ? "Enter an email address." : (!EMAIL.test(em) ? "Enter an email like name@school.org." : "");
      setError(email.parentNode, emMsg); if (emMsg) ok = false;
      setError(grade.parentNode, grade.value ? "" : "Choose a grade."); if (!grade.value) ok = false;
      var tv = target.value.trim();
      var tMsg = "";
      if (tv) {
        var n = Number(tv);
        if (!isFinite(n) || n < 400 || n > 1600) tMsg = "Target scores run from 400 to 1600.";
        else if (n % 10 !== 0) tMsg = "SAT totals move in steps of 10. Try " + (Math.round(n / 10) * 10) + ".";
      }
      setError(target.parentNode, tMsg); if (tMsg) ok = false;
      var agreeField = agree.closest(".field");
      setError(agreeField, agree.checked ? "" : "Check this box to continue."); if (!agree.checked) ok = false;

      if (!ok) {
        showStatus(sStatus, "err", "Some fields need attention.", "Fix the highlighted fields, then send again.");
        var first = signup.querySelector('[aria-invalid="true"]'); if (first) first.focus();
        return;
      }
      var spam = spamCheck(signup, "graphite_form_log", 3, 10 * 60 * 1000);
      if (spam === "too-fast") { showStatus(sStatus, "err", "That was quicker than we expected.", "Wait a few seconds and press Send again."); return; }
      if (spam === "rate") { showStatus(sStatus, "err", "You've sent this form three times in ten minutes.", "Wait ten minutes, or email us directly."); return; }
      if (spam === "blocked") { showStatus(sStatus, "ok", "Thanks. We got your request."); signup.reset(); return; }

      var btn = signup.querySelector('button[type="submit"]');
      btn.disabled = true; btn.textContent = "Sending…";
      send(CONFIG.formEndpoint, Object.fromEntries(new FormData(signup)))
        .then(function () {
          showStatus(sStatus, "ok", "You're in, " + name.value.trim() + ".", "Your diagnostic link is on its way to " + em + ". It usually arrives within five minutes.");
          Analytics.track("diagnostic_signup", { grade: grade.value });
          signup.reset(); signup.setAttribute("data-started", String(Date.now()));
        })
        .catch(function (err) {
          showFieldError(err, { name: "start-name", email: "start-email", grade: "start-grade", target: "start-target", agree: "start-agree" });
          showStatus(sStatus, "err", "We couldn't send your request.", err && err.status ? err.message : "Check your connection and try again. If it keeps failing, email hello@graphiteprep.com.");
        })
        .then(function () { btn.disabled = false; btn.textContent = "Send my diagnostic link"; });
    });
  }

  /* 7b. Sign in */
  var signin = $("#signin-form");
  if (signin) {
    var aStatus = $("#signin-status");
    try {
      if (sessionStorage.getItem("graphite_signed_out")) {
        sessionStorage.removeItem("graphite_signed_out");
        aStatus.className = "status is-shown ok"; aStatus.textContent = "You've signed out. See you next session.";
      }
    } catch (err) { /* storage blocked */ }
    // Student or parent: changes the headings, the create-account form and where sign-in lands.
    var ROLE = "student";
    try { ROLE = localStorage.getItem("graphite_role_pick") === "parent" ? "parent" : "student"; } catch (err) { /* storage blocked */ }
    if (/[?&]as=parent\b/.test(location.search) || location.hash === "#parent") ROLE = "parent";
    if (/[?&]as=student\b/.test(location.search)) ROLE = "student";
    var roleBtns = $all(".role-pick [data-role]");
    function setRole(r, focus) {
      ROLE = r;
      try { localStorage.setItem("graphite_role_pick", r); } catch (err) { /* storage blocked */ }
      roleBtns.forEach(function (b) {
        var on = b.getAttribute("data-role") === r;
        b.setAttribute("aria-checked", String(on)); b.tabIndex = on ? 0 : -1;
        if (on && focus) b.focus();
      });
      var parent = r === "parent", creating = !$("#create-form").hidden;
      $all(".student-only").forEach(function (el) { el.hidden = parent; });
      $all(".parent-only").forEach(function (el) { el.hidden = !parent; });
      $("#signin-title").textContent = creating ? (parent ? "Create a parent account" : "Create your Graphite account")
        : (parent ? "Sign in to your parent dashboard" : "Sign in to your dashboard");
      $("#create-name-label").textContent = parent ? "Your name" : "Student's name";
      $("#create-lede").textContent = parent ? "Follow your student's progress, study time and plan. You'll connect to your student with a code from their dashboard."
        : "Free to start. Your practice test results and study plan save here.";
    }
    roleBtns.forEach(function (b, i) {
      b.addEventListener("click", function () { setRole(b.getAttribute("data-role")); });
      b.addEventListener("keydown", function (e) {
        var d = e.key === "ArrowRight" || e.key === "ArrowDown" ? 1 : e.key === "ArrowLeft" || e.key === "ArrowUp" ? -1 : 0;
        if (!d) return; e.preventDefault();
        setRole(roleBtns[(i + d + roleBtns.length) % roleBtns.length].getAttribute("data-role"), true);
      });
    });
    function landing(role) {
      var next = safeNext();
      if (role === "parent") return /^\/?(parent|checkout)\.html/.test(next) ? next : "parent.html";
      return /^\/?parent\.html/.test(next) ? CONFIG.dashboardUrl : next;
    }
    var pw = $("#signin-password");
    var pwBtn = $("#pw-toggle");
    pwBtn.addEventListener("click", function () {
      var show = pw.type === "password";
      pw.type = show ? "text" : "password";
      pwBtn.textContent = show ? "Hide" : "Show";
      pwBtn.setAttribute("aria-pressed", String(show));
    });
    var attempts = 0, lockUntil = 0, lockTimer = null;
    function lockCountdown() {
      var btn = signin.querySelector('button[type="submit"]');
      clearInterval(lockTimer);
      lockTimer = setInterval(function () {
        var left = Math.ceil((lockUntil - Date.now()) / 1000);
        if (left <= 0) { clearInterval(lockTimer); btn.disabled = false; btn.textContent = "Sign in"; attempts = 0; return; }
        btn.disabled = true; btn.textContent = "Try again in " + left + "s";
      }, 250);
    }
    signin.addEventListener("submit", function (e) {
      e.preventDefault();
      clearStatus(aStatus);
      if (Date.now() < lockUntil) return;
      var email = $("#signin-email"), em = email.value.trim();
      // The test account (beta / beta) has no email and a short password. The server only accepts it when
      // it runs locally, never on the hosted site (backend/app/testaccount.py).
      var testAccount = em.toLowerCase() === TEST_USERNAME || em.toLowerCase() === TEST_PARENT;
      var emMsg = !em ? "Enter your email address." : (!testAccount && !EMAIL.test(em) ? "Enter an email like name@school.org." : "");
      setError(email.parentNode, emMsg);
      var pMsg = !pw.value ? "Enter your password." : (!testAccount && pw.value.length < 8 ? "Passwords are at least 8 characters." : "");
      setError(pw.closest(".field"), pMsg);
      if (emMsg || pMsg) {
        attempts++;
        if (attempts >= 5) {
          lockUntil = Date.now() + 60000;
          showStatus(aStatus, "err", "Too many attempts.", "Sign in is paused for 60 seconds to protect your account.");
          lockCountdown(); return;
        }
        showStatus(aStatus, "err", "We couldn't sign you in.", "Fix the highlighted fields and try again.");
        (emMsg ? email : pw).focus();
        return;
      }
      var hp = signin.querySelector(".hp input");
      if (hp && hp.value) return;
      var btn = signin.querySelector('button[type="submit"]');
      btn.disabled = true; btn.textContent = "Signing in…";
      // The preview has no accounts, but its test accounts keep to the same rule as the server's.
      var previewRole = !LIVE && (em.toLowerCase() === TEST_USERNAME ? "student" : em.toLowerCase() === TEST_PARENT ? "parent" : null);
      var signedIn = previewRole && previewRole !== ROLE
        ? Promise.reject({ status: 403, message: previewRole === "parent" ? "That's a parent account. Choose \"I'm a parent\" above to sign in."
            : "That's a student account. Choose \"I'm a student\" to sign in, or create a parent account to follow a student's progress.", data: { code: "wrong_role" } })
        : send(CONFIG.authEndpoint, { email: em, password: pw.value, remember: $("#signin-remember").checked, role: ROLE });
      signedIn
        .then(function (res) {
          // The account decides where to go; the preview has no accounts, so it follows the switch.
          var role = res && res.user && res.user.role ? res.user.role : (LIVE ? "student" : (em.toLowerCase() === TEST_PARENT ? "parent" : ROLE));
          // Preview: the test account starts fresh on every sign-in, as it does on the server.
          if (em.toLowerCase() === TEST_USERNAME && !LIVE) {
            try {
              Object.keys(localStorage).filter(function (k) { return k.indexOf("graphite_") === 0 && k !== CONFIG.consentKey; })
                .forEach(function (k) { localStorage.removeItem(k); });
            } catch (err) { /* storage blocked */ }
          }
          var note = role !== ROLE ? (role === "parent" ? "This is a parent account, so we're opening the parent dashboard." : "This is a student account, so we're opening the student dashboard.")
            : (role === "parent" ? "Opening your parent dashboard." : "Opening your dashboard.");
          showStatus(aStatus, "ok", "Signed in as " + em + ".", note);
          Analytics.track("sign_in");
          try { sessionStorage.setItem("graphite_user", em); sessionStorage.setItem("graphite_role", role); } catch (err) { /* storage blocked */ }
          if (CONFIG.dashboardUrl) setTimeout(function () { location.href = landing(role); }, role !== ROLE ? 1400 : 500);
        })
        .catch(function (err) {
          attempts++;
          if (err && err.status === 401) showStatus(aStatus, "err", err.message, "Check both and try again, or reset your password.");
          else if (err && err.data && err.data.code === "wrong_role") { attempts--; showStatus(aStatus, "err", "Wrong kind of account.", err.message); }
          else showStatus(aStatus, "err", "We couldn't sign you in.", networkMessage(err));
        })
        .then(function () { if (Date.now() >= lockUntil) { btn.disabled = false; btn.textContent = "Sign in"; } });
    });

    var reset = $("#reset-form"), resetOpen = $("#reset-open"), resetCancel = $("#reset-cancel");
    resetOpen.addEventListener("click", function () {
      reset.hidden = false; signin.hidden = true;
      $("#reset-email").value = $("#signin-email").value; $("#reset-email").focus();
    });
    resetCancel.addEventListener("click", function () { reset.hidden = true; signin.hidden = false; resetOpen.focus(); });
    reset.addEventListener("submit", function (e) {
      e.preventDefault();
      var rs = $("#reset-status"); clearStatus(rs);
      var email = $("#reset-email"), em = email.value.trim();
      var msg = !em ? "Enter the email you signed up with." : (!EMAIL.test(em) ? "Enter an email like name@school.org." : "");
      setError(email.parentNode, msg);
      if (msg) { showStatus(rs, "err", "We need a valid email to send a reset link."); return; }
      var spam = spamCheck(reset, "graphite_reset_log", 3, 15 * 60 * 1000);
      if (spam === "rate") { showStatus(rs, "err", "Reset links are limited to three per 15 minutes.", "Check your inbox and spam folder for the earlier emails."); return; }
      if (spam === "too-fast") { showStatus(rs, "err", "One moment.", "Wait a few seconds and press Send again."); return; }
      var done = function () { showStatus(rs, "ok", "Check your inbox.", "If an account exists for " + em + ", a reset link is on its way. It expires in 30 minutes."); };
      if (!LIVE) { done(); return; }
      api("/api/auth/forgot", { email: em }).then(done, function (err) { showStatus(rs, "err", "We couldn't send a reset link.", networkMessage(err)); });
    });

    /* 7c. Create an account */
    var create = $("#create-form"), createOpen = $("#create-open"), createPrompt = $("#create-prompt");
    function showCreate(open) {
      create.hidden = !open; signin.hidden = open; reset.hidden = true; createPrompt.hidden = open;
      setRole(ROLE);
      if (open) $("#create-name").focus();
    }
    createOpen.addEventListener("click", function () { showCreate(true); });
    $("#create-cancel").addEventListener("click", function () { showCreate(false); $("#signin-email").focus(); });
    if (location.hash === "#create") showCreate(true);
    setRole(ROLE);
    // Sent here from a page for the other kind of account (for example a student opening the parent dashboard).
    if (LIVE && /[?&]as=(parent|student)\b/.test(location.search)) {
      api("/api/me").then(function (r) {
        var u = r.user; if (!u || u.role === ROLE) return;
        showStatus(aStatus, "ok", "You're signed in as " + u.name + " (" + (u.role === "parent" ? "parent" : "student") + " account).",
          ROLE === "parent" ? "Sign in with a parent account below to open the parent dashboard." : "Sign in with a student account below to open the student dashboard.");
      }, function () { /* not signed in: nothing to say */ });
    }
    create.addEventListener("submit", function (e) {
      e.preventDefault();
      var cs = $("#create-status"); clearStatus(cs);
      var name = $("#create-name"), email = $("#create-email"), pass = $("#create-password"), target = $("#create-target"), agree = $("#create-agree");
      var em = email.value.trim(), ok = true;
      setError(name.closest(".field"), name.value.trim() ? "" : (ROLE === "parent" ? "Enter your name." : "Enter the student's name.")); if (!name.value.trim()) ok = false;
      var emMsg = !em ? "Enter an email address." : (!EMAIL.test(em) ? "Enter an email like name@school.org." : "");
      setError(email.closest(".field"), emMsg); if (emMsg) ok = false;
      var pMsg = pass.value.length < 8 ? "Passwords need at least 8 characters." : "";
      setError(pass.closest(".field"), pMsg); if (pMsg) ok = false;
      var tv = ROLE === "parent" ? "" : target.value.trim(), tMsg = "";
      if (tv && (!(Number(tv) >= 400 && Number(tv) <= 1600) || Number(tv) % 10)) tMsg = "Target scores run from 400 to 1600 in steps of 10.";
      setError(target.closest(".field"), tMsg); if (tMsg) ok = false;
      setError(agree.closest(".field"), agree.checked ? "" : "Check this box to continue."); if (!agree.checked) ok = false;
      if (!ok) { showStatus(cs, "err", "Some fields need attention."); var f = create.querySelector('[aria-invalid="true"]'); if (f) f.focus(); return; }
      if (create.querySelector(".hp input").value) return;
      var btn = create.querySelector('button[type="submit"]');
      btn.disabled = true; btn.textContent = "Creating…";
      var payload = ROLE === "parent" ? { name: name.value, email: em, password: pass.value, role: "parent" }
        : { name: name.value, email: em, password: pass.value, grade: $("#create-grade").value, test_date: $("#create-date").value, target_score: tv, role: "student" };
      (LIVE ? api("/api/auth/register", payload) : send(null))
        .then(function () {
          var hasNext = !!new URLSearchParams(location.search).get("next");
          var parent = ROLE === "parent";
          showStatus(cs, "ok", "Your account is ready.", parent && /^\/?checkout\.html/.test(safeNext()) ? "Taking you back to checkout." : parent ? "Opening your parent dashboard." : hasNext ? "Taking you back." : "Opening your 10-question diagnostic.");
          Analytics.track(parent ? "parent_account_created" : "account_created");
          try { sessionStorage.setItem("graphite_user", em); sessionStorage.setItem("graphite_role", ROLE); } catch (err) { /* storage blocked */ }
          var goCheckout = parent && /^\/?checkout\.html/.test(safeNext());
          setTimeout(function () { location.href = goCheckout ? safeNext() : parent ? "parent.html" : hasNext ? safeNext() : "plan.html"; }, 500);
        })
        .catch(function (err) {
          showFieldError(err, { name: "create-name", email: "create-email", password: "create-password", grade: "create-grade", test_date: "create-date", target_score: "create-target" });
          showStatus(cs, "err", "We couldn't create your account.", networkMessage(err));
          btn.disabled = false; btn.textContent = "Create account";
        });
    });

    /* 7d. Choose a new password from an emailed reset link (signin.html?reset=TOKEN) */
    var resetToken = new URLSearchParams(location.search).get("reset");
    var newpw = $("#newpw-form");
    if (resetToken) {
      newpw.hidden = false; signin.hidden = true; createPrompt.hidden = true;
      $("#signin-title").textContent = "Reset your password";
    }
    newpw.addEventListener("submit", function (e) {
      e.preventDefault();
      var ns = $("#newpw-status"); clearStatus(ns);
      var np = $("#newpw-password");
      var msg = np.value.length < 8 ? "Passwords need at least 8 characters." : "";
      setError(np.closest(".field"), msg);
      if (msg) { np.focus(); return; }
      if (!LIVE) { showStatus(ns, "ok", "Password saved."); return; }
      api("/api/auth/reset", { token: resetToken, password: np.value })
        .then(function () { showStatus(ns, "ok", "Password saved.", "Opening your dashboard."); setTimeout(function () { location.href = CONFIG.dashboardUrl; }, 500); })
        .catch(function (err) { showStatus(ns, "err", "We couldn't save that password.", networkMessage(err)); });
    });
  }

  /* 7e. Home page calculator: the 3D device leans toward the pointer */
  var tilt = $("#c3-tilt"), stage = $("#calc3d");
  if (tilt && stage && window.matchMedia("(prefers-reduced-motion: no-preference)").matches) {
    stage.addEventListener("pointermove", function (e) {
      var r = stage.getBoundingClientRect();
      var px = (e.clientX - r.left) / r.width - 0.5, py = (e.clientY - r.top) / r.height - 0.5;
      tilt.style.setProperty("--ry", (-22 + px * 26).toFixed(1) + "deg");
      tilt.style.setProperty("--rx", (12 - py * 18).toFixed(1) + "deg");
    });
    stage.addEventListener("pointerleave", function () { tilt.style.removeProperty("--ry"); tilt.style.removeProperty("--rx"); });
  }
  // The keys press in time with the screen: x² − 2x − 1 is typed as the parabola appears, then x + 3 before the line.
  var calcFront = $(".c3-front.nsp"), firstRow = $(".c3-e1");
  if (calcFront && firstRow && firstRow.getAnimations && window.matchMedia("(prefers-reduced-motion: no-preference)").matches) {
    var faceOf = function (test) {
      var found = $all(".nk, .ak", calcFront).filter(function (k) { return test(k.textContent.replace(/\s+/g, " ").trim(), k); })[0];
      return found ? (found.querySelector(".nk-face") || found.querySelector("span")) : null;
    };
    var keyX = faceOf(function (t, k) { return k.classList.contains("ak") && t === "X"; });
    var keySq = faceOf(function (t) { return /\^ ?x²$/.test(t.replace(/^\S+ \S+ /, "")) || t.indexOf("x²") > -1 && t.indexOf("^") > -1; });
    var keyPM = faceOf(function (t) { return t.indexOf("+") > -1 && t.indexOf("−") > -1 && t.indexOf("(") < 0; });
    var digit = function (d) { return faceOf(function (t, k) { return k.classList.contains("nk-num") && t === d; }); };
    var keyEnter = faceOf(function (t, k) { return k.classList.contains("nk-enter"); });
    // [ms into the 9-second loop, key]
    var script = [[60, keyX], [140, keySq], [220, keyPM], [300, digit("2")], [380, keyX], [460, keyPM], [540, digit("1")], [640, keyEnter],
                  [2560, keyX], [2650, keyPM], [2740, digit("3")], [2840, keyEnter]];
    var lastT = 0;
    var tick = function () {
      var anim = firstRow.getAnimations()[0];
      if (anim && anim.currentTime != null) {
        var t = anim.currentTime % 9000;
        script.forEach(function (step) {
          var crossed = lastT <= t ? (step[0] > lastT && step[0] <= t) : (step[0] > lastT || step[0] <= t);
          if (crossed && step[1]) {
            step[1].classList.add("is-pressed");
            setTimeout(function () { step[1].classList.remove("is-pressed"); }, 110);
          }
        });
        lastT = t;
      }
      requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }

  // Click the calculator (or the button) to flip it over and see the back.
  var flipBtn = $("#c3-flip");
  if (tilt && flipBtn) {
    var flip = function () {
      var on = !tilt.classList.contains("is-flipped");
      tilt.classList.toggle("is-flipped", on);
      flipBtn.setAttribute("aria-pressed", String(on));
      flipBtn.textContent = on ? "Flip it back" : "Flip it over";
    };
    flipBtn.addEventListener("click", flip);
    tilt.addEventListener("click", flip);
  }

  /* 8. Hero practice question */
  var qcard = $("#qcard");
  if (qcard) {
    var QUESTIONS = [
      {
        meta: "Math · Module 1", num: "Question 7 of 22",
        stem: "If 3x + 7 = 25, what is the value of 6x − 4?",
        choices: ["14", "32", "36", "40"], answer: 1,
        why: [
          "14 is 3x − 4. The question asks about 6x, so double 3x first: 3x = 18, so 6x = 36.",
          "3x = 18, so 6x = 36, and 36 − 4 = 32. Doubling the equation is faster than solving for x.",
          "36 is 6x. You stopped one step early. Subtract 4 to get 32.",
          "40 is 6x + 4. Check the sign: the question asks for 6x − 4."
        ]
      },
      {
        meta: "Reading and Writing · Module 1", num: "Question 19 of 27",
        stem: "Maya's first experiment produced no crystals. ____, her second attempt, which used a slower cooling rate, produced dozens. Which choice completes the text with the most logical transition?",
        choices: ["Similarly", "However", "For example", "Therefore"], answer: 1,
        why: [
          "Similarly signals the same result. The two attempts had opposite results.",
          "The second attempt worked where the first failed. However marks that contrast.",
          "For example would make the second attempt an instance of the first. It's a contrast instead.",
          "Therefore says the failure caused the success. The text only sets the two results side by side."
        ]
      },
      {
        meta: "Math · Module 2", num: "Question 4 of 22",
        stem: "A line passes through the points (2, 5) and (6, 13). What is the slope of the line?",
        choices: ["1/2", "2", "3", "8"], answer: 1,
        why: [
          "1/2 is run over rise. Slope is rise over run: (13 − 5) ÷ (6 − 2).",
          "Rise is 13 − 5 = 8 and run is 6 − 2 = 4, so the slope is 8 ÷ 4 = 2.",
          "3 comes from adding the y-values. Slope uses differences: (13 − 5) ÷ (6 − 2).",
          "8 is the rise alone. Divide it by the run, 6 − 2 = 4."
        ]
      }
    ];
    var qi = 0;
    var fs = $("#qchoices"), note = $("#qnote"), nextBtn = $("#qnext");
    // Live: the home page's question comes from the question bank (/api/sample) and is checked there,
    // with the full explanation. The dashboard's Today's set opens real practice sets instead (section 9).
    var onDash = !!$(".dash");
    if (LIVE && !onDash) {
      var current = null;
      var loadSample = function () {
        nextBtn.disabled = true;
        api("/api/sample").then(function (r) {
          current = r.question;
          $("#qmeta").textContent = "Math · " + current.domain; $("#qnum").textContent = "Try one";
          $("#qstem").innerHTML = current.stem;
          fs.innerHTML = '<legend class="visually-hidden">Answer choices</legend>';
          current.choices.forEach(function (c, i) {
            var letter = "ABCD"[i];
            var lab = document.createElement("label"); lab.className = "choice";
            lab.innerHTML = '<input type="radio" name="q" value="' + i + '" id="q-s-' + letter + '"><span class="bubble" aria-hidden="true">' + letter +
              '</span><span class="visually-hidden">Choice ' + letter + ': </span><span class="choice-text">' + c + "</span>";
            fs.appendChild(lab);
          });
          note.hidden = true; note.innerHTML = "";
        }).catch(function () { /* keep the built-in question */ }).then(function () { nextBtn.disabled = false; });
      };
      fs.addEventListener("change", function (e) {
        if (!current) return;
        var pick = Number(e.target.value);
        $all("input", fs).forEach(function (i) { i.disabled = true; });
        api("/api/sample/check", { id: current.id, answer: pick }).then(function (r) {
          $all(".choice", fs).forEach(function (l, i) {
            l.classList.toggle("is-right", i === r.answer_index);
            l.classList.toggle("is-wrong", i === pick && !r.correct);
          });
          note.innerHTML = '<p class="verdict ' + (r.correct ? "ok" : "no") + '">' + (r.correct ? "Correct. Choice " + "ABCD"[pick] + "." : "Not quite. The answer is " + r.answer + ".") + "</p>" +
            '<div class="tutor-xp">' + r.explain_html + "</div>";
          note.hidden = false;
          Analytics.track("demo_answer", { correct: r.correct });
        }).catch(function () { $all("input", fs).forEach(function (i) { i.disabled = false; }); });
      }, true);
      nextBtn.addEventListener("click", function (e) { e.stopImmediatePropagation(); loadSample(); }, true);
      loadSample();
    }
    function render() {
      var q = QUESTIONS[qi];
      $("#qmeta").textContent = q.meta; $("#qnum").textContent = q.num; $("#qstem").textContent = q.stem;
      fs.innerHTML = "";
      var lg = document.createElement("legend"); lg.className = "visually-hidden"; lg.textContent = "Answer choices"; fs.appendChild(lg);
      q.choices.forEach(function (c, i) {
        var letter = "ABCD"[i];
        var lab = document.createElement("label"); lab.className = "choice";
        var inp = document.createElement("input"); inp.type = "radio"; inp.name = "q"; inp.value = String(i); inp.id = "q-" + qi + "-" + letter;
        var b = document.createElement("span"); b.className = "bubble"; b.setAttribute("aria-hidden", "true"); b.textContent = letter;
        var t = document.createElement("span"); t.className = "choice-text"; t.textContent = c;
        var sr = document.createElement("span"); sr.className = "visually-hidden"; sr.textContent = "Choice " + letter + ": ";
        lab.appendChild(inp); lab.appendChild(b); lab.appendChild(sr); lab.appendChild(t);
        fs.appendChild(lab);
      });
      note.hidden = true; note.innerHTML = "";
    }
    fs.addEventListener("change", function (e) {
      if (LIVE && !onDash) return;
      var q = QUESTIONS[qi], pick = Number(e.target.value);
      $all(".choice", fs).forEach(function (l, i) {
        l.classList.toggle("is-right", i === q.answer);
        l.classList.toggle("is-wrong", i === pick && pick !== q.answer);
      });
      note.innerHTML = "";
      var v = document.createElement("p");
      v.className = "verdict " + (pick === q.answer ? "ok" : "no");
      v.textContent = pick === q.answer ? "Correct. Choice " + "ABCD"[pick] + "." : "Not quite. The answer is " + "ABCD"[q.answer] + ".";
      var w = document.createElement("p"); w.textContent = "Tutor: " + q.why[pick];
      note.appendChild(v); note.appendChild(w); note.hidden = false;
      Analytics.track("demo_answer", { q: qi, correct: pick === q.answer });
    });
    nextBtn.addEventListener("click", function () { qi = (qi + 1) % QUESTIONS.length; render(); fs.querySelector("input").focus(); });
    if (!(LIVE && !onDash)) render();
  }
  /* 8b. Pricing: the Weekly / Monthly / Yearly switch. Prices stay per month; what's billed changes. */
  $all('.billing-switch input[name="billing"]').forEach(function (r) {
    r.addEventListener("change", function () {
      if (!r.checked) return;
      var iv = r.value;
      $all(".tier").forEach(function (card) {
        var cta = card.querySelector("[data-checkout]");  // the plan's button opens checkout with this billing option picked
        if (cta) cta.setAttribute("href", "checkout.html?plan=" + cta.getAttribute("data-checkout") + "&interval=" + iv);
        card.querySelector("[data-amount]").textContent = card.getAttribute("data-" + iv + "-amount");
        card.querySelector("[data-billed]").textContent = card.getAttribute("data-" + iv + "-billed");
        var save = card.querySelector("[data-save]"), text = card.getAttribute("data-" + iv + "-save");
        save.textContent = text; save.hidden = !text;
      });
      Analytics.track("pricing_interval", { interval: iv });
    });
  });

  // Phones show one plan's column of the feature table at a time.
  var compare = $("#compare");
  if (compare) $all('input[name="compare-show"]', compare).forEach(function (r) {
    r.addEventListener("change", function () { if (r.checked) compare.setAttribute("data-show", r.value); });
  });

  /* 9. Dashboard */
  /* Parent access (dashboard Account panel): a one-time code for a parent, and the parents already connected.
     Preview: kept in this browser (graphite_family), where the parent dashboard preview reads it too. */
  var pa = $("#parent-access");
  if (pa) {
    var FKEY = "graphite_family";
    var famLocal = function (path, data, method) {
      var f = store.get(FKEY) || { parents: [] };
      if (path === "/api/family/code") {
        var A = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789", c = "";
        for (var i = 0; i < 8; i++) c += A.charAt(Math.floor(Math.random() * A.length));
        f.code = { code: c.slice(0, 4) + "-" + c.slice(4), expires_at: new Date(Date.now() + 7 * 86400000).toISOString() };
        store.set(FKEY, f);
        return Promise.resolve(f.code);
      }
      if (method === "DELETE") { f.parents = []; store.set(FKEY, f); return Promise.resolve({ ok: true }); }
      return Promise.resolve({ parents: f.parents, code_expires_at: f.code ? f.code.expires_at : null });
    };
    var fam = function (path, data, method) { return LIVE ? api(path, data, method) : famLocal(path, data, method); };
    var paStatus = $("#pa-status");
    var paEsc = function (t) { return String(t == null ? "" : t).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
    var drawParents = function (list) {
      var ul = $("#pa-list");
      ul.hidden = !list.length;
      ul.innerHTML = list.map(function (p) {
        return '<li><div><strong>' + paEsc(p.name) + '</strong><p class="fine">' + paEsc(p.email) + "</p></div>" +
          '<button class="btn btn-quiet" type="button" data-remove-parent="' + p.id + '">Remove</button></li>';
      }).join("");
    };
    var expiry = function (iso) { var d = new Date(iso); return "Works once, until " + d.toLocaleDateString("en-US", { month: "short", day: "numeric" }) + "."; };
    fam("/api/family").then(function (r) { drawParents(r.parents); }).catch(function () { /* the card still offers a code */ });
    $("#pa-make").addEventListener("click", function () {
      var b = this; b.disabled = true; clearStatus(paStatus);
      fam("/api/family/code", {}).then(function (r) {
        b.disabled = false; b.textContent = "Get a new code";
        $("#pa-code").hidden = false; $("#pa-code-val").textContent = r.code; $("#pa-code-exp").textContent = expiry(r.expires_at);
        showStatus(paStatus, "ok", "Send this code to your parent.", "They enter it on their parent dashboard. Making a new code cancels this one.");
      }).catch(function (err) { b.disabled = false; showStatus(paStatus, "err", "We couldn't make a code.", networkMessage(err)); });
    });
    $("#pa-copy").addEventListener("click", function () {
      var v = $("#pa-code-val").textContent, b = this;
      var done = function () { b.textContent = "Copied"; setTimeout(function () { b.textContent = "Copy"; }, 1500); };
      if (navigator.clipboard) navigator.clipboard.writeText(v).then(done, function () { /* select it instead */ }); else done();
    });
    $("#pa-list").addEventListener("click", function (e) {
      var b = e.target.closest("[data-remove-parent]"); if (!b) return;
      if (b.textContent !== "Press again to remove") { b.textContent = "Press again to remove"; return; }
      fam("/api/family/parents/" + b.getAttribute("data-remove-parent"), {}, "DELETE").then(function () {
        return fam("/api/family");
      }).then(function (r) { drawParents(r.parents); showStatus(paStatus, "ok", "Removed. They can't see your progress anymore."); })
        .catch(function (err) { showStatus(paStatus, "err", "We couldn't remove that parent.", networkMessage(err)); });
    });
  }

  $all("[data-sign-out]").forEach(function (b) {
    b.addEventListener("click", function () {
      var go = function () {
        try { sessionStorage.removeItem("graphite_user"); sessionStorage.removeItem("graphite_role"); sessionStorage.setItem("graphite_signed_out", "1"); } catch (err) { /* storage blocked */ }
        location.href = "signin.html";
      };
      if (LIVE) api("/api/auth/logout", {}).then(go, go); else go();
    });
  });

  if ($(".dash")) {
    var now = new Date();
    var hr = now.getHours();
    var part = hr < 12 ? "Good morning" : (hr < 18 ? "Good afternoon" : "Good evening");
    $("#today-date").textContent = now.toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric" });

    var esc = function (t) { return String(t == null ? "" : t).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
    var fmtMinutes = function (m) { var h = Math.floor(m / 60), mm = m % 60; return h ? h + " h " + mm + " m" : mm + " min"; };
    var niceDate = function (iso, opts) { return new Date(iso + "T12:00:00").toLocaleDateString("en-US", opts || { month: "short", day: "numeric" }); };
    var minutesThisWeek = 110, setTotal = 12;

    function applyGoal(h) {
      // A parent can set any goal from 1 to 20 hours; make sure the menu has it.
      var gsel = $("#goal-hours");
      if (!gsel.querySelector('option[value="' + h + '"]')) {
        var o = document.createElement("option"); o.value = String(h); o.textContent = h + (h === 1 ? " hour" : " hours");
        var after = Array.prototype.filter.call(gsel.options, function (x) { return Number(x.value) > h; })[0];
        gsel.insertBefore(o, after || null);
      }
      gsel.value = String(h);
      $("#goal-sub").textContent = "of your " + h + " h goal";
      $("#goal-meter").style.width = Math.min(100, Math.round(minutesThisWeek / (h * 60) * 100)) + "%";
    }

    // Score chart tooltip (sample chart from the build, or the live chart drawn below)
    function bindChart() {
      var wrap = $(".chart-wrap"), tip = $("#chart-tip");
      if (!wrap || !tip) return;
      var vb = wrap.querySelector("svg").viewBox.baseVal;
      var showTip = function (el) {
        tip.innerHTML = "";
        var t = document.createElement("span"); t.textContent = el.getAttribute("data-label") + " · ";
        var s2 = document.createElement("strong"); s2.textContent = el.getAttribute("data-score");
        var d = document.createElement("div"); d.textContent = el.getAttribute("data-detail");
        tip.appendChild(t); tip.appendChild(s2); tip.appendChild(d);
        tip.style.left = (Number(el.getAttribute("cx")) / vb.width * 100) + "%";
        tip.style.top = (Number(el.getAttribute("cy")) / vb.height * 100) + "%";
        tip.hidden = false;
      };
      $all(".hit", wrap).forEach(function (h) {
        h.addEventListener("mouseenter", function () { showTip(h); });
        h.addEventListener("focus", function () { showTip(h); });
        h.addEventListener("mouseleave", function () { tip.hidden = true; });
        h.addEventListener("blur", function () { tip.hidden = true; });
      });
    }

    // Percent correct on each practice test, on one 0-100% scale.
    function drawChart(history) {
      var W = 640, H = 250, L = 52, R = 70, T = 16, B = 34, pw = W - L - R, ph = H - T - B, n = history.length;
      var y = function (v) { return T + ph * (100 - v) / 100; };
      var x = function (i) { return n === 1 ? L + pw / 2 : L + pw * i / (n - 1); };
      var out = ['<div class="chart-wrap"><svg viewBox="0 0 ' + W + " " + H + '" role="img" aria-labelledby="chart-title chart-desc">',
        '<title id="chart-title">Percent correct on each practice test</title>',
        '<desc id="chart-desc">' + esc(history.map(function (h) { return h.label + ": " + h.pct + "%"; }).join(", ")) + "</desc>"];
      [0, 25, 50, 75, 100].forEach(function (v) {
        out.push('<line class="grid" x1="' + L + '" x2="' + (W - R) + '" y1="' + y(v) + '" y2="' + y(v) + '"/>');
        out.push('<text class="axis-text" x="' + (L - 10) + '" y="' + (y(v) + 4) + '" text-anchor="end">' + v + "%</text>");
      });
      var pts = history.map(function (h, i) { return x(i).toFixed(1) + "," + y(h.pct).toFixed(1); });
      if (n > 1) {
        out.push('<path class="area" d="M' + x(0).toFixed(1) + "," + y(0) + " L" + pts.join(" L") + " L" + x(n - 1).toFixed(1) + "," + y(0) + ' Z"/>');
        out.push('<polyline class="line" points="' + pts.join(" ") + '"/>');
      }
      var step = Math.max(1, Math.ceil(n / 6));
      history.forEach(function (h, i) {
        if (i % step === 0 || i === n - 1) {
          var anchor = n === 1 ? "middle" : (i === 0 ? "start" : (i === n - 1 ? "end" : "middle"));
          out.push('<text class="axis-text" x="' + x(i).toFixed(1) + '" y="' + (H - 8) + '" text-anchor="' + anchor + '">' + esc(h.label) + "</text>");
        }
        out.push('<circle class="hit" cx="' + x(i).toFixed(1) + '" cy="' + y(h.pct).toFixed(1) + '" r="18" tabindex="0" data-label="' + esc(h.label) + '" data-score="' + h.correct + "/" + h.total +
          '" data-detail="' + h.pct + '% correct" aria-label="' + esc(h.label) + ": " + h.correct + " of " + h.total + '"/>');
        out.push('<circle class="pt" cx="' + x(i).toFixed(1) + '" cy="' + y(h.pct).toFixed(1) + '" r="' + (i === n - 1 ? 6 : 5) + '"/>');
      });
      var last = history[n - 1];
      out.push('<text class="end-text" x="' + (x(n - 1) + 12).toFixed(1) + '" y="' + (y(last.pct) + 5).toFixed(1) + '">' + last.pct + "%</text>");
      out.push('</svg><div class="chart-tip" id="chart-tip" role="status" hidden></div></div>');
      return out.join("");
    }

    // Today's set
    var startBtn = $("#set-start"), runner = $("#set-runner"), prog = $("#set-progress");
    var done = 0, answeredThis = false, shownAt = Date.now();
    var todaySource = null;
    startBtn.addEventListener("click", function (e) {
      if (LIVE) {
        e.preventDefault();
        if (todaySource === "none") { location.href = "plan.html"; return; }
        startBtn.disabled = true; startBtn.textContent = "Building your set…";
        var t = new Date(), day = t.getFullYear() + "-" + String(t.getMonth() + 1).padStart(2, "0") + "-" + String(t.getDate()).padStart(2, "0");
        api("/api/today?today=" + day, {}).then(function (r) {
          location.href = r.redirect ? r.redirect : "practice-test.html?session=" + r.session.id;
        }).catch(function (err) {
          startBtn.disabled = false; startBtn.textContent = "Start today's set";
          prog.textContent = networkMessage(err);
        });
        return;
      }
      runner.hidden = false;
      startBtn.setAttribute("aria-expanded", "true");
      startBtn.textContent = "Keep going";
      shownAt = Date.now();
      var first = runner.querySelector("input"); if (first) first.focus();
    });
    $("#qchoices").addEventListener("change", function () {
      if (answeredThis) return;
      answeredThis = true; done = Math.min(done + 1, setTotal);
      prog.textContent = done + " of " + setTotal + " done";
      if (LIVE) api("/api/activity", { kind: "practice_question", seconds: Math.round((Date.now() - shownAt) / 1000) }).catch(function () { /* not critical */ });
    });
    $("#qnext").addEventListener("click", function () { answeredThis = false; shownAt = Date.now(); });

    // Review queue
    var queue = $("#queue"), qStatus = $("#queue-status");
    function updateCount() {
      var n = queue.children.length;
      $("#review-count").textContent = n === 1 ? "1 question" : n + " questions";
      $("#queue-empty").hidden = n !== 0;
    }
    function bindReview(li) {
      var btn = li.querySelector("button");
      btn.addEventListener("click", function () {
        if (LIVE && btn.getAttribute("data-practice")) {
          btn.disabled = true;
          api("/api/review/" + li.getAttribute("data-id") + "/practice", {})
            .then(function (r) { location.href = "practice-test.html?session=" + r.session.id; })
            .catch(function (err) { btn.disabled = false; showStatus(qStatus, "err", "We couldn't open that question.", networkMessage(err)); });
          return;
        }
        var apply = function (right, cleared) {
          if (cleared) {
            li.remove();
            showStatus(qStatus, "ok", "Cleared from your review queue.", "Right twice means it stuck.");
            updateCount(); Analytics.track("review_cleared");
            return;
          }
          li.setAttribute("data-right", String(right));
          li.querySelector(".queue-score").textContent = right + " of 2";
          var due = li.querySelector(".due"); due.textContent = "Due in 3 days"; due.classList.remove("due-now");
          showStatus(qStatus, "ok", "Nice. One more right answer clears it.", "It comes back in 3 days.");
        };
        if (!LIVE) { var r = Number(li.getAttribute("data-right")) + 1; apply(r, r >= 2); return; }
        btn.disabled = true;
        api("/api/review/" + li.getAttribute("data-id") + "/right", {})
          .then(function (res) { apply(res.right_count, res.cleared); })
          .catch(function (err) { showStatus(qStatus, "err", "We couldn't update that question.", networkMessage(err)); })
          .then(function () { btn.disabled = false; });
      });
    }

    // Account settings
    var goalForm = $("#goal-form"), gStatus = $("#goal-status");
    goalForm.addEventListener("submit", function (e) {
      e.preventDefault();
      var h = Number($("#goal-hours").value);
      if (!h) { showStatus(gStatus, "err", "Choose a weekly goal first."); return; }
      if (!LIVE) { store.set("graphite_goal", h); applyGoal(h); showStatus(gStatus, "ok", "Weekly goal saved: " + h + " hours."); return; }
      var payload = { weekly_goal_hours: h, test_date: $("#acct-test-date").value, target_score: $("#acct-target").value };
      api("/api/me", payload, "PATCH")
        .then(function () { showStatus(gStatus, "ok", "Settings saved."); return loadDashboard(); })
        .catch(function (err) {
          showFieldError(err, { test_date: "acct-test-date", target_score: "acct-target", weekly_goal_hours: "goal-hours" });
          showStatus(gStatus, "err", "We couldn't save your settings.", networkMessage(err));
        });
    });

    // The welcome card: what to do next, the countdown, and which days this week had practice.
    function renderHello(d) {
      var s = d.summary, items = d.today.items || [];
      var next = items.filter(function (i) { return !i.done; })[0];
      var src = d.today.source || (items.length ? "domains" : "none");
      if (src === "none") {
        $("#up-next-title").textContent = "Your 10-question diagnostic";
        $("#up-next-meta").textContent = "About 15 minutes · builds your study plan";
        $("#up-next-start").textContent = "Start the diagnostic";
        $("#hello-sub").textContent = "Let's find out where you're strong and where the easy points are.";
      } else if (d.today.all_done) {
        $("#up-next-title").textContent = "This week's plan is done";
        $("#up-next-meta").textContent = "Take an extra quiz, or rest up. You earned it.";
        $("#up-next-start").textContent = "Extra quiz";
        $("#hello-sub").textContent = "You finished everything planned for this week. Nice work.";
      } else if (next) {
        $("#up-next-title").textContent = next.domain;
        $("#up-next-meta").textContent = next.count + " questions · about " + Math.max(10, Math.round(next.count * 1.5)) + " min";
        $("#up-next-start").textContent = "Let's go";
        $("#hello-sub").textContent = src === "plan" ? "Here's the next step in your plan. Short and focused." : "A short set on the area where you have the most points to gain.";
      }
      var days = s.study_days_week || [];
      var studied = days.filter(Boolean).length, dow = (now.getDay() + 6) % 7, letters = "MTWTFSS";
      $("#chip-study-days").textContent = String(studied);
      $("#chip-streak").lastChild.lastChild.nodeValue = studied === 1 ? " study day this week" : " study days this week";
      $("#week-dots").innerHTML = letters.split("").map(function (l, i) {
        return '<li class="' + (days[i] ? "on" : "") + (i === dow ? " is-today" : "") + '"><span>' + l + "</span></li>";
      }).join("");
      if (s.test_date) {
        $("#chip-days-left").textContent = String(s.days_to_test);
        $("#chip-countdown").lastChild.lastChild.nodeValue = (s.days_to_test === 1 ? " day" : " days") + " to your SAT";
        $("#chip-countdown").hidden = false;
      } else {
        $("#chip-countdown").hidden = true;
      }
    }
    $("#up-next-start").addEventListener("click", function () {
      $("#set-start").click();
      if (!LIVE) $("#today").scrollIntoView({ block: "start" });
    });

    function renderDashboard(d) {
      if (d.start_with_diagnostic) { location.replace("plan.html?welcome=1"); return; }
      var s = d.summary, u = d.user;
      // Label each attempt in the student's own time zone.
      d.history.forEach(function (h) { if (h.submitted_at) h.label = new Date(h.submitted_at).toLocaleDateString("en-US", { month: "short", day: "numeric" }); });
      if (s.latest) s.latest.label = d.history[d.history.length - 1].label;
      $("#sample-note").hidden = true;
      $("#greeting").textContent = part + ", " + u.first_name;
      renderHello(d);
      $("#account-email").textContent = u.email;

      if (s.latest) {
        $("#kpi-latest-label").textContent = "Latest practice test";
        $("#kpi-latest").textContent = s.latest.correct + " / " + s.latest.total;
        $("#kpi-latest-sub").textContent = s.latest.pct + "% correct" + (s.change_pct_points != null ? ", " + (s.change_pct_points >= 0 ? "up " : "down ") + Math.abs(s.change_pct_points) + " from your first test" : " on " + s.latest.label);
      } else {
        $("#kpi-latest-label").textContent = "Latest practice test";
        $("#kpi-latest").textContent = "None yet";
        $("#kpi-latest-sub").textContent = "Take a practice test from Practice";
      }
      $("#kpi-target").textContent = s.target_score || "Not set";
      $("#kpi-target-sub").textContent = s.target_score ? "Your goal score" : "Add one in Account";
      minutesThisWeek = s.practice_minutes_week;
      $("#kpi-week").textContent = fmtMinutes(minutesThisWeek);
      applyGoal(s.weekly_goal_hours);
      if (s.test_date) {
        $("#kpi-test-label").textContent = "SAT on " + niceDate(s.test_date, { month: "short", day: "numeric", year: "numeric" });
        $("#kpi-test-num").innerHTML = '<span id="days-left">' + s.days_to_test + "</span> " + (s.days_to_test === 1 ? "day" : "days");
        $("#kpi-test-sub").textContent = d.plan.weeks.length + (d.plan.weeks.length === 1 ? " week" : " weeks") + " of plan left";
      } else {
        $("#kpi-test-label").textContent = "SAT date";
        $("#kpi-test-num").textContent = "Not set";
        $("#kpi-test-sub").textContent = "Add it in Account to fit your plan";
      }

      var setList = $("#set-list");
      setTotal = d.today.questions || 12;
      todaySource = d.today.source || (d.today.items.length ? "domains" : "none");
      if (d.today.items.length) {
        $("#today-meta").textContent = d.today.all_done ? "This week is done" : d.today.questions + " questions · about " + d.today.minutes + " min";
        $("#today-lede").textContent = todaySource === "plan"
          ? (d.today.all_done ? "You've finished this week's plan. Start an extra quiz on this week's topics, or rest up." : "This week's tasks from your study plan. Today's set starts the next one.")
          : "Built from the domains costing you the most points right now.";
        setList.innerHTML = d.today.items.map(function (it) {
          return '<li class="' + (it.done ? "is-done" : "") + '"><span>' + esc(it.domain) + '</span><span class="mono">' + (it.done ? "Done" : it.count + " questions") + '</span><span class="set-why">' + esc(it.why) + "</span></li>";
        }).join("");
        setList.hidden = false;
        startBtn.textContent = d.today.all_done ? "Start an extra quiz" : "Start today's set";
        prog.textContent = todaySource === "plan" ? d.today.items.filter(function (i) { return i.done; }).length + " of " + d.today.items.length + " tasks done this week" : "";
      } else {
        $("#today-meta").textContent = "Start here";
        $("#today-lede").textContent = "Take the 10-question diagnostic. It finds your strengths and weak spots and builds your study plan, and your daily sets come from it.";
        setList.innerHTML = ""; setList.hidden = true;
        startBtn.textContent = "Take the diagnostic"; prog.textContent = "";
      }

      var test = d.tests[0];
      if (test) {
        $("#next-test-text").innerHTML = "<strong>Math practice test</strong><span>" + test.questions + " new questions every time · " + test.minutes + " minutes · or practice one topic</span>";
      }
      $("#scores-meta").textContent = d.history.length ? d.history.length + (d.history.length === 1 ? " test taken" : " tests taken") : "No tests yet";
      if (d.history.length) {
        $("#score-chart").innerHTML = drawChart(d.history);
        $("#scores-thead").innerHTML = '<tr><th scope="col">Test</th><th scope="col">Date</th><th scope="col" class="num">Correct</th><th scope="col" class="num">Percent</th><th scope="col" class="num">Time</th></tr>';
        $("#scores-tbody").innerHTML = d.history.map(function (h, i) {
          return '<tr><th scope="row">Attempt ' + (i + 1) + "</th><td>" + esc(h.label) + '</td><td class="num">' + h.correct + "/" + h.total + '</td><td class="num">' + h.pct + '%</td><td class="num">' + Math.round(h.seconds_used / 60) + " min</td></tr>";
        }).join("");
        $("#scores-table").hidden = false;
        bindChart();
      } else {
        $("#score-chart").innerHTML = '<div class="chart-empty"><p>Your scores appear here after your first practice test.</p></div>';
        $("#scores-table").hidden = true;
      }

      var groups = { "Math": [], "Reading and Writing": [] };
      d.domains.forEach(function (dm) { groups[dm.section].push(dm); });
      $("#domains-meta").textContent = d.history.length ? "% correct on your latest test" : "No test yet";
      $("#domains-lede").textContent = d.domains.some(function (x) { return x.focus; })
        ? "The ones marked Focus have the most points left to gain. Your daily sets lean toward them."
        : "Take a practice test to see where your points are. Reading and Writing results appear once that section's practice tests are added.";
      $("#bar-groups").innerHTML = Object.keys(groups).map(function (name) {
        return '<div><h3 class="bar-group-title">' + esc(name) + '</h3><ul class="bars">' + groups[name].map(function (dm) {
          var has = dm.pct != null;
          return '<li><span class="bar-name">' + esc(dm.name) + (dm.focus ? ' <span class="chip">Focus</span>' : "") + '</span><span class="bar-track' + (has ? "" : " is-empty") + '"><span style="width: ' + (has ? dm.pct : 0) + '%"></span></span><span class="bar-val">' + (has ? dm.pct + "%" : "–") + "</span></li>";
        }).join("") + "</ul></div>";
      }).join("");

      queue.innerHTML = d.review.map(function (it) {
        return '<li data-id="' + it.id + '" data-right="' + it.right_count + '"><div><span class="label">' + esc(it.section) + " · " + esc(it.domain) + "</span><p>" + esc(it.skill) +
          '</p></div><span class="queue-meta"><span class="mono queue-score">' + it.right_count + ' of 2</span><span class="due' + (it.due_now ? " due-now" : "") + '">' + esc(it.due_label) +
          '</span></span><button class="btn btn-quiet" type="button"' + (it.practice ? ' data-practice="1">Practice it again' : ">I got it right") + "</button></li>";
      }).join("");
      $all("li", queue).forEach(bindReview);
      updateCount();

      $("#plan-title").textContent = d.plan.fits_test_date ? "Your plan to " + niceDate(s.test_date) : "Your next " + d.plan.weeks.length + " weeks";
      $("#plan-meta").textContent = d.plan.weeks.length + (d.plan.weeks.length === 1 ? " week" : " weeks");
      $("#plan-link").textContent = d.plan.study_plan ? "Open your study plan" : "Take the diagnostic for a personal plan";
      $("#weeks").innerHTML = d.plan.weeks.map(function (w) {
        return "<li" + (w.is_now ? ' class="is-now"' : "") + '><span class="mono">' + esc(niceDate(w.week_of)) + "</span><span>" + esc(w.focus) + (w.is_now ? ' <em class="now-tag">This week</em>' : "") + "</span></li>";
      }).join("");

      $("#account-list").innerHTML =
        "<div><dt>Student</dt><dd>" + esc(u.name) + (u.grade ? ", " + u.grade + "th grade" : "") + "</dd></div>" +
        "<div><dt>Email</dt><dd>" + esc(u.email) + "</dd></div>" +
        "<div><dt>Plan</dt><dd>" + esc(u.plan.charAt(0).toUpperCase() + u.plan.slice(1)) + "</dd></div>" +
        "<div><dt>Parent email</dt><dd>" + (u.parent_email ? esc(u.parent_email) : "Not added") + "</dd></div>";
      $all(".live-only").forEach(function (f) { f.hidden = false; });
      $("#acct-test-date").value = u.test_date || "";
      $("#acct-target").value = u.target_score || "";
      $("#goal-save").textContent = "Save settings";
      $(".dash").classList.add("is-ready");
    }

    function loadDashboard() {
      var t = new Date(), localDay = t.getFullYear() + "-" + String(t.getMonth() + 1).padStart(2, "0") + "-" + String(t.getDate()).padStart(2, "0");
      return api("/api/dashboard?today=" + localDay).then(renderDashboard).catch(function (err) {
        if (err && err.status === 401) { location.href = "/signin.html?next=/dashboard.html"; return; }
        var note = $("#sample-note");
        note.hidden = false; note.classList.add("is-error"); note.textContent = "We couldn't load your dashboard. Refresh the page to try again.";
      });
    }

    if (LIVE) {
      $("#greeting").textContent = part;
      loadDashboard();
    } else {
      // Preview: the first dashboard visit goes to the diagnostic once, as the live site does.
      if (!store.get("graphite_diag_prompted")) { store.set("graphite_diag_prompted", true); location.replace("plan.html?welcome=1"); }
      $("#greeting").textContent = part + ", Maya";
      try { var who = sessionStorage.getItem("graphite_user"); if (who) $("#account-email").textContent = who; } catch (err) { /* storage blocked */ }
      var dl = $("#days-left");
      var test0 = new Date(dl.getAttribute("data-test-date") + "T08:00:00");
      var today0 = new Date(now.getFullYear(), now.getMonth(), now.getDate());
      var days = Math.round((new Date(test0.getFullYear(), test0.getMonth(), test0.getDate()) - today0) / 86400000);
      if (isFinite(days)) dl.textContent = String(Math.max(days, 0));
      $all("li", queue).forEach(bindReview);
      var savedGoal = store.get("graphite_goal");
      if (savedGoal) applyGoal(savedGoal);
      bindChart();
    }
  }
})();

/* Floating calculator window: drag it by its title bar, resize it from the corner, expand it, and it
   remembers where it was. On phones it opens small (about 30% of the screen, above the test's bottom bar)
   and can be moved and resized the same way. Used by the practice test and the diagnostic. */
window.GraphiteFloat = function (win, o) {
  "use strict";
  var phone = window.matchMedia("(max-width: 860px)");
  var saved = {}, restore = null;
  function key() { return o.key + (phone.matches ? "_phone" : ""); }
  function below() { return o.bottomEl ? o.bottomEl.getBoundingClientRect().height : 0; }
  function defaults() {
    var vw = window.innerWidth, vh = window.innerHeight;
    if (!phone.matches) return { w: 460, h: Math.min(720, vh - 110), x: 24, y: 84 };
    var h = Math.round(Math.max(220, vh * 0.3));
    return { w: vw - 16, h: h, x: 8, y: vh - below() - h - 8 };
  }
  function state() {
    var k = key();
    if (!saved[k]) {
      try { saved[k] = JSON.parse(localStorage.getItem(k)); } catch (e) { saved[k] = null; }
      if (!saved[k] || typeof saved[k].w !== "number") saved[k] = defaults();
    }
    return saved[k];
  }
  function store() { try { localStorage.setItem(key(), JSON.stringify(state())); } catch (e) { /* storage blocked */ } }
  function place() {
    var st = state(), vw = window.innerWidth, vh = window.innerHeight;
    var minW = phone.matches ? 240 : 320, minH = phone.matches ? 200 : 340;
    st.w = Math.round(Math.max(Math.min(minW, vw - 16), Math.min(st.w, vw - 16)));
    st.h = Math.round(Math.max(Math.min(minH, vh - 16), Math.min(st.h, vh - 16)));
    st.x = Math.round(Math.max(8, Math.min(st.x, vw - st.w - 8)));
    st.y = Math.round(Math.max(8, Math.min(st.y, vh - st.h - 8)));
    win.style.left = st.x + "px"; win.style.top = st.y + "px";
    win.style.width = st.w + "px"; win.style.height = st.h + "px";
    // Room for the page to scroll clear of the window when it sits low on a phone.
    document.documentElement.style.setProperty("--calc-sheet", phone.matches ? Math.max(0, vh - st.y) + "px" : "0px");
  }
  function drag(el, onMove) {
    var start = null;
    el.addEventListener("pointerdown", function (e) {
      if (e.button > 0 || (el === o.handle && e.target.closest("button"))) return;
      var st = state();
      e.preventDefault(); el.setPointerCapture(e.pointerId);
      start = { px: e.clientX, py: e.clientY, x: st.x, y: st.y, w: st.w, h: st.h };
      win.classList.add("is-moving");
    });
    el.addEventListener("pointermove", function (e) {
      if (!start) return;
      onMove(state(), e.clientX - start.px, e.clientY - start.py, start); place();
    });
    function end() { if (!start) return; start = null; win.classList.remove("is-moving"); restore = null; syncExpand(); store(); }
    el.addEventListener("pointerup", end); el.addEventListener("pointercancel", end);
  }
  drag(o.handle, function (st, dx, dy, s) { st.x = s.x + dx; st.y = s.y + dy; });
  drag(o.grip, function (st, dx, dy, s) { st.w = s.w + dx; st.h = s.h + dy; });
  // Keyboard: arrow keys on the title bar move the window, on the corner grip they resize it.
  function keys(el, move) {
    el.addEventListener("keydown", function (e) {
      var d = { ArrowLeft: [-1, 0], ArrowRight: [1, 0], ArrowUp: [0, -1], ArrowDown: [0, 1] }[e.key];
      if (!d || e.target !== el) return;
      e.preventDefault();
      var st = state();
      if (move) { st.x += d[0] * 32; st.y += d[1] * 32; } else { st.w += d[0] * 32; st.h += d[1] * 32; }
      place(); store();
    });
  }
  keys(o.handle, true); keys(o.grip, false);
  function syncExpand() {
    if (!o.expand) return;
    o.expand.setAttribute("aria-pressed", String(!!restore));
    o.expand.textContent = restore ? (phone.matches ? "Smaller" : "Restore") : "Expand";
  }
  function toggleExpand() {
    var st = state();
    if (restore) { saved[key()] = restore; restore = null; }
    else {
      restore = { x: st.x, y: st.y, w: st.w, h: st.h };
      var vw = window.innerWidth, vh = window.innerHeight;
      saved[key()] = phone.matches ? { x: 8, y: 8, w: vw - 16, h: vh - below() - 16 }
        : { w: Math.round(vw * 0.72), h: vh - 96, x: Math.round(vw * 0.14), y: 72 };
    }
    place(); store(); syncExpand();
  }
  if (o.expand) o.expand.addEventListener("click", toggleExpand);
  o.handle.addEventListener("dblclick", function (e) { if (!e.target.closest("button")) toggleExpand(); });
  window.addEventListener("resize", function () { if (!win.hidden) place(); });
  if (phone.addEventListener) phone.addEventListener("change", function () { restore = null; if (!win.hidden) { place(); syncExpand(); } });
  return { place: function () { place(); syncExpand(); } };
};
