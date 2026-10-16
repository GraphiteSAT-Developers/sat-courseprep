/* Graphite site script. Edit CONFIG to connect real services. */
(function () {
  "use strict";

  var CONFIG = {
    // POST endpoint for the "Start free diagnostic" form. When null, the form validates and shows the success message without sending.
    formEndpoint: null,
    // POST endpoint for sign in. When null, any well-formed email and 8+ character password signs in.
    authEndpoint: null,
    // Where to send students after a successful sign in. When null, the page stays put.
    dashboardUrl: null,
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

  function send(endpoint, data) {
    if (!endpoint) return new Promise(function (resolve) { setTimeout(resolve, 600); });
    return fetch(endpoint, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data), credentials: "same-origin" })
      .then(function (r) { if (!r.ok) throw new Error(String(r.status)); return r; });
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
        .catch(function () {
          showStatus(sStatus, "err", "We couldn't send your request.", "Check your connection and try again. If it keeps failing, email hello@graphiteprep.com.");
        })
        .then(function () { btn.disabled = false; btn.textContent = "Send my diagnostic link"; });
    });
  }

  /* 7b. Sign in */
  var signin = $("#signin-form");
  if (signin) {
    var aStatus = $("#signin-status");
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
      var emMsg = !em ? "Enter your email address." : (!EMAIL.test(em) ? "Enter an email like name@school.org." : "");
      setError(email.parentNode, emMsg);
      var pMsg = !pw.value ? "Enter your password." : (pw.value.length < 8 ? "Passwords are at least 8 characters." : "");
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
      send(CONFIG.authEndpoint, { email: em, password: pw.value, remember: $("#signin-remember").checked })
        .then(function () {
          showStatus(aStatus, "ok", "Signed in as " + em + ".", CONFIG.dashboardUrl ? "Opening your dashboard." : "Your dashboard is ready.");
          Analytics.track("sign_in");
          if (CONFIG.dashboardUrl) setTimeout(function () { location.href = CONFIG.dashboardUrl; }, 700);
        })
        .catch(function () {
          attempts++;
          showStatus(aStatus, "err", "That email and password don't match.", "Check both and try again, or reset your password.");
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
      showStatus(rs, "ok", "Check your inbox.", "If an account exists for " + em + ", a reset link is on its way. It expires in 30 minutes.");
    });
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
    render();
  }
})();
