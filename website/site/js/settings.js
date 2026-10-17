/* The Settings page. Live: every change goes to /api/me/... and the header updates right away.
   Preview (no server): appearance and the profile picture are kept in this browser, and the
   email, password and account forms check what you typed and say they work on the live site. */
(function () {
  "use strict";
  var page = document.querySelector(".settings-page");
  if (!page) return;
  var T = window.GraphiteTheme, API = window.GraphiteAPI;
  var LIVE = !!(API && API.live);
  var EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  var TEST_USERS = ["beta", "beta2"];
  var user = null;

  function $(id) { return document.getElementById(id); }
  function all(sel) { return Array.prototype.slice.call(document.querySelectorAll(sel)); }

  function status(el, kind, title, detail) {
    el.className = "status is-shown " + kind;
    el.textContent = "";
    var p = document.createElement("p"); p.textContent = title; el.appendChild(p);
    if (detail) { var d = document.createElement("p"); d.textContent = detail; el.appendChild(d); }
  }
  function clear(el) { el.className = "status"; el.textContent = ""; }
  function fieldError(input, msg) {
    var field = input.closest(".field");
    var err = field.querySelector(".field-error");
    if (!err) { err = document.createElement("p"); err.className = "field-error"; err.id = input.id + "-error"; field.appendChild(err); }
    err.textContent = msg || ""; err.hidden = !msg;
    input.setAttribute("aria-invalid", msg ? "true" : "false");
    if (msg) input.setAttribute("aria-describedby", err.id); else input.removeAttribute("aria-describedby");
    return !msg;
  }
  function serverFieldError(err, map) {
    var f = err && err.data && err.data.field, id = f && map[f];
    if (id && $(id)) { fieldError($(id), err.message); $(id).focus(); return true; }
    return false;
  }
  function message(err) { return err && err.status ? err.message : "We couldn't reach Graphite. Check your connection and try again."; }
  function busy(btn, on, label) {
    if (!btn) return;
    if (on) { btn.dataset.label = btn.textContent; btn.textContent = label; btn.disabled = true; }
    else { btn.textContent = btn.dataset.label || btn.textContent; btn.disabled = false; }
  }

  /* ---------- preview storage ---------- */
  function previewProfile() { try { return JSON.parse(localStorage.getItem(T.previewKey) || "{}") || {}; } catch (e) { return {}; } }
  function savePreviewProfile(p) { try { localStorage.setItem(T.previewKey, JSON.stringify(p)); return true; } catch (e) { return false; } }

  /* ---------- fill the page ---------- */
  function render(u) {
    user = u;
    var parent = u.role === "parent";
    all("[data-student-only]").forEach(function (el) { el.hidden = parent; });
    all("[data-role-home]").forEach(function (a) { a.href = parent ? "parent.html" : "dashboard.html"; a.textContent = "Back to " + (parent ? "parent dashboard" : "dashboard"); });
    T.avatar($("st-avatar"), u);
    $("st-photo-remove").hidden = !u.avatar_url;
    $("st-name").value = u.name || "";
    $("st-current-email").textContent = u.email;
    $("st-username").value = u.email;
    var a = Object.assign({}, T.get(), u.appearance || {});
    var th = $("st-theme-" + a.theme); if (th) th.checked = true;
    var ac = $("st-accent-" + a.accent); if (ac) ac.checked = true;
    $("st-ripple").checked = a.ripple !== false;
    if (!parent) {
      $("st-grade").value = u.grade ? String(u.grade) : "";
      var goal = String(u.weekly_goal_hours || 3);
      if (!$("st-goal").querySelector('option[value="' + goal + '"]')) {
        var o = document.createElement("option"); o.value = goal; o.textContent = goal + " hours a week"; $("st-goal").appendChild(o);
      }
      $("st-goal").value = goal;
      $("st-date").value = u.test_date || "";
      $("st-target").value = u.target_score || "";
    }
    var test = TEST_USERS.indexOf(String(u.email).toLowerCase()) > -1;
    $("st-test-note").hidden = !test;
    ["st-email-form", "st-password-form", "st-delete-form"].forEach(function (id) {
      all("#" + id + " input, #" + id + " button").forEach(function (el) { if (el.id !== "st-username") el.disabled = test; });
    });
  }

  function updateMe(u) {
    if (!LIVE) {
      var p = previewProfile();
      u = Object.assign({}, user, p.name ? { name: p.name } : {}, { avatar_url: p.avatar || null });
    }
    u = Object.assign({}, u, { appearance: T.get() });  // keep any look change that's still saving
    render(u);
    if (T.setMe) T.setMe(u);
    var h = $("header-avatar"); if (h) T.avatar(h, u);
  }

  /* ---------- profile picture ---------- */
  // Center-crops to a square and shrinks it in the browser, so uploads are small and quick.
  function squareImage(file, size) {
    return new Promise(function (resolve, reject) {
      var reader = new FileReader();
      reader.onerror = function () { reject(new Error("read")); };
      reader.onload = function () {
        var img = new Image();
        img.onerror = function () { reject(new Error("decode")); };
        img.onload = function () {
          var side = Math.min(img.naturalWidth, img.naturalHeight);
          var c = document.createElement("canvas"); c.width = c.height = size;
          var ctx = c.getContext("2d");
          ctx.imageSmoothingQuality = "high";
          ctx.drawImage(img, (img.naturalWidth - side) / 2, (img.naturalHeight - side) / 2, side, side, 0, 0, size, size);
          var url = c.toDataURL("image/webp", 0.86);
          if (url.indexOf("data:image/webp") !== 0) url = c.toDataURL("image/jpeg", 0.88);
          resolve(url);
        };
        img.src = reader.result;
      };
      reader.readAsDataURL(file);
    });
  }

  $("st-photo-input").addEventListener("change", function () {
    var file = this.files && this.files[0], st = $("st-photo-status");
    this.value = "";
    if (!file) return;
    clear(st);
    if (!/^image\/(png|jpeg|webp|gif)$/.test(file.type)) { status(st, "err", "That file isn't a PNG, JPEG, WebP or GIF image."); return; }
    if (file.size > 15 * 1024 * 1024) { status(st, "err", "That image is over 15 MB.", "Choose a smaller photo."); return; }
    status(st, "ok", "Uploading your photo…");
    squareImage(file, LIVE ? 512 : 192).then(function (url) {
      if (!LIVE) {
        var p = previewProfile(); p.avatar = url;
        if (!savePreviewProfile(p)) throw new Error("storage");
        updateMe(user); status(st, "ok", "Photo updated."); return;
      }
      return API.call("/api/me/avatar", { image: url }).then(function (r) { updateMe(r.user); status(st, "ok", "Photo updated."); });
    }).catch(function (err) {
      status(st, "err", "We couldn't use that photo.", err && err.status ? err.message : (err && err.message === "storage" ? "This browser won't save it. Try a smaller photo." : "Try a different image."));
    });
  });

  $("st-photo-remove").addEventListener("click", function () {
    var st = $("st-photo-status"), btn = this;
    if (!LIVE) { var p = previewProfile(); delete p.avatar; savePreviewProfile(p); updateMe(user); status(st, "ok", "Photo removed."); return; }
    busy(btn, true, "Removing…");
    API.call("/api/me/avatar", {}, "DELETE")
      .then(function (r) { updateMe(r.user); status(st, "ok", "Photo removed."); })
      .catch(function (err) { status(st, "err", "We couldn't remove your photo.", message(err)); })
      .then(function () { busy(btn, false); });
  });

  /* ---------- name ---------- */
  $("st-name-form").addEventListener("submit", function (e) {
    e.preventDefault();
    var st = $("st-name-status"), name = $("st-name").value.replace(/\s+/g, " ").trim(), btn = this.querySelector("button[type=submit]");
    clear(st);
    if (!fieldError($("st-name"), name ? "" : "Enter your name.")) { $("st-name").focus(); return; }
    if (!LIVE) { var p = previewProfile(); p.name = name; savePreviewProfile(p); updateMe(user); status(st, "ok", "Name saved."); return; }
    busy(btn, true, "Saving…");
    API.call("/api/me", { name: name }, "PATCH")
      .then(function (r) { updateMe(Object.assign({}, user, r.user)); status(st, "ok", "Name saved."); })
      .catch(function (err) { if (!serverFieldError(err, { name: "st-name" })) status(st, "err", "We couldn't save your name.", message(err)); })
      .then(function () { busy(btn, false); });
  });

  /* ---------- appearance: applies at once, saves in the background ---------- */
  var saveTimer = 0, pending = {};
  function changeLook(change) {
    T.set(change);
    Object.assign(pending, change);
    var saved = $("st-look-saved"), st = $("st-look-status");
    clear(st);
    if (!LIVE) { saved.textContent = "Saved in this browser"; return; }
    saved.textContent = "Saving…";
    clearTimeout(saveTimer);
    saveTimer = setTimeout(function () {
      var body = pending; pending = {};
      API.call("/api/me/appearance", body, "PATCH")
        .then(function () { saved.textContent = "Saved"; })
        .catch(function (err) { saved.textContent = ""; status(st, "err", "We couldn't save your appearance.", message(err)); });
    }, 350);
  }
  all('input[name="theme"]').forEach(function (r) { r.addEventListener("change", function () { if (r.checked) changeLook({ theme: r.value }); }); });
  all('input[name="accent"]').forEach(function (r) { r.addEventListener("change", function () { if (r.checked) changeLook({ accent: r.value }); }); });
  $("st-ripple").addEventListener("change", function () { changeLook({ ripple: this.checked }); });

  /* ---------- study ---------- */
  $("st-study-form").addEventListener("submit", function (e) {
    e.preventDefault();
    var st = $("st-study-status"), btn = this.querySelector("button[type=submit]"), tv = $("st-target").value.trim();
    clear(st);
    var ok = fieldError($("st-target"), tv && (!(Number(tv) >= 400 && Number(tv) <= 1600) || Number(tv) % 10) ? "Target scores run from 400 to 1600 in steps of 10." : "");
    if (!ok) { $("st-target").focus(); return; }
    var data = { grade: $("st-grade").value || null, weekly_goal_hours: Number($("st-goal").value), test_date: $("st-date").value || null, target_score: tv ? Number(tv) : null };
    if (!LIVE) { status(st, "ok", "Study settings saved.", "In the preview they aren't kept. On the live site they shape your study plan."); return; }
    busy(btn, true, "Saving…");
    API.call("/api/me", data, "PATCH")
      .then(function (r) { user = Object.assign({}, user, r.user); status(st, "ok", "Study settings saved."); })
      .catch(function (err) {
        if (!serverFieldError(err, { grade: "st-grade", weekly_goal_hours: "st-goal", test_date: "st-date", target_score: "st-target" }))
          status(st, "err", "We couldn't save your study settings.", message(err));
      })
      .then(function () { busy(btn, false); });
  });

  /* ---------- email ---------- */
  $("st-email-form").addEventListener("submit", function (e) {
    e.preventDefault();
    var st = $("st-email-status"), btn = this.querySelector("button[type=submit]");
    var em = $("st-new-email").value.trim(), pw = $("st-email-password").value;
    clear(st);
    var ok = fieldError($("st-new-email"), !em ? "Enter your new email." : !EMAIL.test(em) ? "Enter an email like name@school.org." : em.toLowerCase() === String(user.email).toLowerCase() ? "That's already your email." : "");
    ok = fieldError($("st-email-password"), pw ? "" : "Enter your current password.") && ok;
    if (!ok) { this.querySelector('[aria-invalid="true"]').focus(); return; }
    if (!LIVE) { status(st, "ok", "Looks good.", "In the preview your email doesn't change. On the live site you'd sign in with " + em + " from now on."); return; }
    busy(btn, true, "Saving…");
    API.call("/api/me/email", { email: em, password: pw })
      .then(function (r) {
        updateMe(r.user); $("st-email-form").reset();
        var h = $("account-email"); if (h) h.textContent = r.user.email;
        status(st, "ok", "Email changed.", "You'll sign in with " + r.user.email + " from now on. We let your old address know.");
      })
      .catch(function (err) { if (!serverFieldError(err, { email: "st-new-email", password: "st-email-password" })) status(st, "err", "We couldn't change your email.", message(err)); })
      .then(function () { busy(btn, false); });
  });

  /* ---------- password ---------- */
  $("st-password-form").addEventListener("submit", function (e) {
    e.preventDefault();
    var st = $("st-password-status"), btn = this.querySelector("button[type=submit]");
    var cur = $("st-current-password").value, nw = $("st-new-password").value, again = $("st-confirm-password").value;
    clear(st);
    var ok = fieldError($("st-current-password"), cur ? "" : "Enter your current password.");
    ok = fieldError($("st-new-password"), nw.length < 8 ? "Passwords need at least 8 characters." : nw === cur ? "Choose a password you haven't been using." : "") && ok;
    ok = fieldError($("st-confirm-password"), again !== nw ? "The two new passwords don't match." : "") && ok;
    if (!ok) { this.querySelector('[aria-invalid="true"]').focus(); return; }
    if (!LIVE) { status(st, "ok", "Looks good.", "In the preview your password doesn't change."); this.reset(); return; }
    busy(btn, true, "Saving…");
    API.call("/api/me/password", { current_password: cur, new_password: nw })
      .then(function () { $("st-password-form").reset(); status(st, "ok", "Password changed.", "Other devices were signed out. You're still signed in here."); })
      .catch(function (err) { if (!serverFieldError(err, { current_password: "st-current-password", new_password: "st-new-password" })) status(st, "err", "We couldn't change your password.", message(err)); })
      .then(function () { busy(btn, false); });
  });

  /* ---------- devices ---------- */
  $("st-sign-out-others").addEventListener("click", function () {
    var st = $("st-devices-status"), btn = this;
    clear(st);
    if (!LIVE) { status(st, "ok", "Done.", "On the live site this signs out every other device."); return; }
    busy(btn, true, "Signing out…");
    API.call("/api/me/sign-out-others", {})
      .then(function () { status(st, "ok", "Other devices are signed out.", "You're still signed in here."); })
      .catch(function (err) { status(st, "err", "We couldn't sign out your other devices.", message(err)); })
      .then(function () { busy(btn, false); });
  });

  /* ---------- delete ---------- */
  $("st-delete-form").addEventListener("submit", function (e) {
    e.preventDefault();
    var st = $("st-delete-status"), btn = this.querySelector("button[type=submit]");
    var conf = $("st-delete-confirm").value.trim(), pw = $("st-delete-password").value;
    clear(st);
    var ok = fieldError($("st-delete-confirm"), conf.toUpperCase() === "DELETE" ? "" : "Type DELETE to confirm.");
    ok = fieldError($("st-delete-password"), pw ? "" : "Enter your current password.") && ok;
    if (!ok) { this.querySelector('[aria-invalid="true"]').focus(); return; }
    if (!LIVE) { status(st, "ok", "Nothing was deleted.", "This is the preview. On the live site your account would be deleted now."); return; }
    busy(btn, true, "Deleting…");
    API.call("/api/me/delete", { confirm: conf, password: pw })
      .then(function () {
        try { sessionStorage.clear(); localStorage.removeItem("graphite_appearance"); } catch (err) { /* storage blocked */ }
        status(st, "ok", "Your account was deleted.", "Taking you to the home page.");
        setTimeout(function () { location.href = "/"; }, 1500);
      })
      .catch(function (err) {
        busy(btn, false);
        if (!serverFieldError(err, { confirm: "st-delete-confirm", password: "st-delete-password" })) status(st, "err", "We couldn't delete your account.", message(err));
      });
  });

  // theme.js may load the account's saved look after this page has drawn: keep the choices in step.
  document.addEventListener("graphite:appearance", function (e) {
    var a = e.detail || {};
    var th = $("st-theme-" + a.theme); if (th && !th.checked) th.checked = true;
    var ac = $("st-accent-" + a.accent); if (ac && !ac.checked) ac.checked = true;
    if (typeof a.ripple === "boolean") $("st-ripple").checked = a.ripple;
  });

  /* ---------- start ---------- */
  if (LIVE) {
    API.call("/api/me").then(function (r) { render(r.user); }, function (err) {
      if (err && err.status === 401) location.href = "/signin.html?next=/settings.html";
    });
  } else {
    $("st-preview-note").hidden = false;
    $("st-export").hidden = true; $("st-export-note").hidden = false;
    render(T.me());
  }
})();
