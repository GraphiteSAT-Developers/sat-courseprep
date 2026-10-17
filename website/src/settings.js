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
    ["text", "font", "motion", "density"].forEach(function (k) { var r = $("st-" + k + "-" + a[k]); if (r) r.checked = true; });
    if (a.custom_accent) { $("st-custom-color").value = a.custom_accent; $("st-custom-dot").style.background = a.custom_accent; customNote(a.custom_accent); }
    if (!parent) renderPrefs(u.prefs || T.prefs());
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
  ["text", "font", "motion", "density"].forEach(function (k) {
    all('input[name="look-' + k + '"]').forEach(function (r) { r.addEventListener("change", function () { if (r.checked) { var c = {}; c[k] = r.value; changeLook(c); } }); });
  });
  // Any color (from the shop): the page changes as you drag, and saves when you stop.
  function customNote(h) {
    var c = T.contrastWith ? T.contrastWith(h) : 5;
    $("st-custom-note").textContent = c < 3 ? "Hard to see on this theme. Try a lighter or darker shade." : "Good contrast on this theme.";
  }
  $("st-custom-color").addEventListener("input", function () {
    var h = this.value.toLowerCase();
    $("st-custom-dot").style.background = h;
    $("st-accent-custom").checked = true;
    changeLook({ accent: "custom", custom_accent: h });
    customNote(h);
  });

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

  /* ---------- shop colors and the leaderboard (students) ---------- */
  var R = window.GraphiteRewards, playCall = R && R.call();
  var nick = { now: null, picked: null, options: [] };
  function loadPlay() {
    if (!playCall || (user && user.role === "parent")) return;
    playCall("/api/game").then(function (g) {
      owned = {};
      g.shop.forEach(function (it) { if (it.owned) owned[it.key] = true; });
      all("[data-shop]").forEach(function (input) {
        var has = !!owned[input.getAttribute("data-shop")], box = input.closest(".st-accent, .st-theme");
        input.disabled = !has;
        box.classList.toggle("is-locked", !has);
        var lock = box.querySelector(".st-lock"); if (lock) lock.hidden = has;
      });
      $("st-custom").hidden = !owned["accent:custom"];
      drawAvatarParts();
      $("st-shop-note").textContent = "";
      $("st-shop-note").innerHTML = "You have " + R.num(g.coins) + ' coins. Unlock themes, colors, frames, titles and avatar items in the <a href="rewards.html#shop">shop</a>.';
    }).catch(function () { /* the rest of Settings still works */ });
    playCall("/api/speed/states").then(function (r) {
      var sel = $("st-state");
      r.states.forEach(function (st) { var o = document.createElement("option"); o.value = st.code; o.textContent = st.name; sel.appendChild(o); });
      return playCall("/api/speed");
    }).then(function (o) {
      var b = o.board_profile;
      $("st-board-on").checked = b.opt_in;
      $("st-state").value = b.state || "";
      nick.now = b.nickname; nick.picked = b.nickname;
      rollNames();
    }).catch(function () { /* leaderboard settings unavailable */ });
  }
  function drawNames() {
    var box = $("st-nicks"); box.innerHTML = "";
    var list = (nick.now && nick.options.indexOf(nick.now) < 0 ? [nick.now] : []).concat(nick.options);
    list.forEach(function (n, i) {
      var id = "st-nick-" + i, lab = document.createElement("label");
      lab.className = "st-nick"; lab.setAttribute("for", id);
      lab.innerHTML = '<input type="radio" name="nickname" id="' + id + '"><span></span>';
      lab.querySelector("input").value = n; lab.querySelector("input").checked = n === nick.picked;
      lab.querySelector("span").textContent = n + (n === nick.now ? " (yours now)" : "");
      lab.querySelector("input").addEventListener("change", function () { nick.picked = n; $("st-nick-own").value = n; fieldError($("st-nick-own"), ""); });
      box.appendChild(lab);
    });
    $("st-nick-now").textContent = nick.now ? "You're " + nick.now + ". Keep it, type a new one or pick a suggestion." : "Type your own or pick a suggestion.";
    if (!$("st-nick-own").value && nick.now) $("st-nick-own").value = nick.now;
  }
  function rollNames() {
    playCall("/api/speed/nicknames").then(function (r) { nick.options = r.nicknames; drawNames(); });
  }
  $("st-nick-roll").addEventListener("click", rollNames);
  // A nickname typed in: checked here as you type, and again by the server (real name, curse words, taken).
  function nickProblem(v) {
    v = v.trim().replace(/\s+/g, " ");
    if (!v) return "";
    if (v.length < 3 || v.length > 20) return "Nicknames are 3 to 20 characters.";
    if (!/^[A-Za-z0-9][A-Za-z0-9 ._'-]*$/.test(v)) return "Use letters, numbers, spaces and . _ ' - only.";
    if (window.GraphiteWords && !GraphiteWords.isClean(v)) return GraphiteWords.message;
    var squash = function (t) { return String(t || "").toLowerCase().replace(/[^a-z0-9]/g, ""); };
    if (user && user.name && squash(v) === squash(user.name)) return "Leaderboards are public, so pick a nickname that isn't your real name.";
    return "";
  }
  $("st-nick-own").addEventListener("input", function () {
    nick.picked = this.value.trim().replace(/\s+/g, " ") || null;
    all('input[name="nickname"]').forEach(function (r) { r.checked = r.value === nick.picked; });
    fieldError(this, nickProblem(this.value));
  });
  $("st-board-form").addEventListener("submit", function (e) {
    e.preventDefault();
    var st = $("st-board-status"), btn = this.querySelector("button[type=submit]");
    clear(st);
    var data = { opt_in: $("st-board-on").checked, state: $("st-state").value || null };
    var problem = nickProblem($("st-nick-own").value);
    if (problem) { fieldError($("st-nick-own"), problem); $("st-nick-own").focus(); return; }
    if (nick.picked && nick.picked !== nick.now) data.nickname = nick.picked;
    if (data.opt_in && !nick.picked) { status(st, "err", "Pick a nickname first.", "It's what other students see instead of your name."); return; }
    busy(btn, true, "Saving…");
    playCall("/api/speed/profile", data, "PATCH").then(function (r) {
      var b = r.board_profile; nick.now = b.nickname; drawNames();
      status(st, "ok", "Leaderboard settings saved.", b.opt_in ? "You show up as " + b.nickname + (b.state_name ? " on the " + b.state_name + " and national boards." : " on the national board. Add your state to join a state board.")
        : "You're hidden. You'll still see where you'd place.");
    }).catch(function (err) {
      if (err && err.data && err.data.field === "nickname") { fieldError($("st-nick-own"), err.message); $("st-nick-own").focus(); return; }
      status(st, "err", "We couldn't save that.", message(err));
    })
      .then(function () { busy(btn, false); });
  });

  /* ---------- drawn avatar ---------- */
  var owned = {};
  var AV_LABELS = { bg: "Background", skin: "Skin", hair: "Hair", hair_color: "Hair color", eyes: "Eyes", mouth: "Mouth", acc: "Extras", shirt: "Shirt" };
  var AV_NAMES = { none: "None", short: "Short", curly: "Curly", long: "Long", bun: "Bun", buzz: "Buzz", waves: "Waves", ponytail: "Ponytail",
    dots: "Dots", happy: "Happy", wide: "Wide", sleepy: "Sleepy", smile: "Smile", grin: "Grin", flat: "Straight", open: "Surprised",
    glasses: "Glasses", beanie: "Beanie", headphones: "Headphones", sunglasses: "Sunglasses", pencil: "Pencil", gradcap: "Graduation cap", crown: "Crown" };
  var AV_OPTIONS = { bg: ["sky", "mint", "sun", "rose", "lilac", "slate", "peach", "teal"], skin: ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8"],
    hair: ["none", "short", "curly", "long", "bun", "buzz", "waves", "ponytail"], hair_color: ["black", "brown", "auburn", "blonde", "gray", "blue", "pink", "green"],
    eyes: ["dots", "happy", "wide", "sleepy"], mouth: ["smile", "grin", "flat", "open"],
    acc: ["none", "glasses", "beanie", "pencil", "sunglasses", "headphones", "gradcap", "crown"], shirt: ["pencil", "sky", "mint", "coral", "lilac", "slate", "white", "black"] };
  var AV_SHOP = { pencil: ["avatar:pencil", 60], sunglasses: ["avatar:sunglasses", 80], headphones: ["avatar:headphones", 100], gradcap: ["avatar:gradcap", 150], crown: ["avatar:crown", 250] };
  var COLOR_PART = { bg: "bg", skin: "skin", hair_color: "hair_color", shirt: "shirt" };
  var av = { mode: "photo", parts: {} };
  function avLocked(part, v) { return part === "acc" && AV_SHOP[v] && !owned[AV_SHOP[v][0]]; }
  function drawAvatarParts() {
    if (!T.drawAvatar) return;
    $("st-av-preview").innerHTML = T.drawAvatar(av.parts, "Your avatar");
    $("st-av-" + av.mode).checked = true;
    $("st-av-parts").innerHTML = Object.keys(AV_OPTIONS).map(function (part) {
      return '<fieldset class="av-part"><legend>' + AV_LABELS[part] + '</legend><div class="av-opts">' + AV_OPTIONS[part].map(function (v) {
        var id = "av-" + part + "-" + v, locked = avLocked(part, v), color = COLOR_PART[part] && T.avatarParts[part] && T.avatarParts[part][v];
        var name = AV_NAMES[v] || (part === "skin" ? "Tone " + v.slice(1) : v.replace(/_/g, " "));
        var look = color ? '<span class="av-swatch" style="background:' + color + '"></span>'
          : '<span class="av-mini">' + T.drawAvatar(Object.assign({}, av.parts, (function () { var o = {}; o[part] = v; return o; })()), "") + "</span>";
        return '<label class="av-opt' + (locked ? " is-locked" : "") + '" for="' + id + '" title="' + name + (locked ? ", " + AV_SHOP[v][1] + " coins in the shop" : "") + '">' +
          '<input type="radio" name="av-' + part + '" id="' + id + '" value="' + v + '"' + (av.parts[part] === v ? " checked" : "") + (locked ? " disabled" : "") + ">" +
          look + '<span class="' + (color ? "visually-hidden" : "av-name") + '">' + name + (locked ? " · " + AV_SHOP[v][1] : "") + "</span></label>";
      }).join("") + "</div></fieldset>";
    }).join("");
  }
  $("st-av-parts").addEventListener("change", function (e) {
    var r = e.target; if (!r.name || r.name.indexOf("av-") !== 0) return;
    av.parts[r.name.slice(3)] = r.value;
    av.mode = "drawn";
    var keep = r.id;
    drawAvatarParts();
    var again = $(keep); if (again) again.focus();
    $("st-av-saved").textContent = "Not saved yet";
  });
  all('input[name="av-mode"]').forEach(function (r) { r.addEventListener("change", function () { av.mode = r.value; $("st-av-saved").textContent = "Not saved yet"; }); });
  $("st-av-random").addEventListener("click", function () {
    Object.keys(AV_OPTIONS).forEach(function (part) {
      var free = AV_OPTIONS[part].filter(function (v) { return !avLocked(part, v); });
      av.parts[part] = free[Math.floor(Math.random() * free.length)];
    });
    av.mode = "drawn"; drawAvatarParts(); $("st-av-saved").textContent = "Not saved yet";
  });
  $("st-av-save").addEventListener("click", function () {
    var btn = this, st = $("st-av-status"); clear(st);
    savePrefs({ avatar: { mode: av.mode, parts: av.parts } }, btn).then(function () {
      $("st-av-saved").textContent = "Saved";
      status(st, "ok", av.mode === "drawn" ? "Your drawn avatar is on." : "Using your photo or initials.", av.mode === "drawn" ? "It shows next to your email and on leaderboards." : "");
    }).catch(function (err) { status(st, "err", "We couldn't save your avatar.", message(err)); });
  });

  /* ---------- practice defaults ---------- */
  function hourName(h) { return (h % 12 || 12) + (h < 12 ? " am" : " pm"); }
  (function () {
    var sel = $("st-reminder-hour");
    for (var h = 5; h <= 22; h++) { var o = document.createElement("option"); o.value = h; o.textContent = hourName(h); sel.appendChild(o); }
    $("st-set-size").innerHTML = [5, 10, 15, 20].map(function (n) {
      return '<span><input type="radio" name="df-size" id="st-size-' + n + '" value="' + n + '"><label for="st-size-' + n + '">' + n + "</label></span>";
    }).join("");
  })();
  var deviceTz = (function () { try { return Intl.DateTimeFormat().resolvedOptions().timeZone || "America/New_York"; } catch (e) { return "America/New_York"; } })();
  function renderPrefs(p) {
    p = p || T.prefs();
    var s = p.study;
    var r = $("st-size-" + s.set_size); if (r) r.checked = true;
    $("st-timer-" + s.timer).checked = true; $("st-calc-" + s.calculator).checked = true; $("st-colors-" + s.colors).checked = true;
    $("st-sounds").checked = !!s.sounds; $("st-reminder").checked = !!s.reminder;
    $("st-reminder-hour").value = String(s.reminder_hour);
    $("st-reminder-time").hidden = !s.reminder;
    $("st-tz-note").textContent = "Your time zone: " + deviceTz.replace(/_/g, " ") + "." + (LIVE ? "" : " The preview doesn't send emails.");
    av = { mode: p.avatar.mode, parts: Object.assign({}, p.avatar.parts) };
    drawAvatarParts();
    layout = { order: p.dashboard.order.slice(), hidden: p.dashboard.hidden.slice(), pins: p.dashboard.pins.slice() };
    drawLayout();
  }
  $("st-reminder").addEventListener("change", function () { $("st-reminder-time").hidden = !this.checked; });
  function checked(name) { var r = document.querySelector('input[name="' + name + '"]:checked'); return r && r.value; }
  $("st-defaults-form").addEventListener("submit", function (e) {
    e.preventDefault();
    var st = $("st-defaults-status"), btn = this.querySelector("button[type=submit]"); clear(st);
    var study = { set_size: Number(checked("df-size")), timer: checked("df-timer"), calculator: checked("df-calc"), colors: checked("df-colors"),
                  sounds: $("st-sounds").checked, reminder: $("st-reminder").checked, reminder_hour: Number($("st-reminder-hour").value), tz: deviceTz };
    savePrefs({ study: study }, btn).then(function () {
      try { localStorage.setItem("graphite_practice_count", String(study.set_size)); } catch (x) { /* storage blocked */ }
      status(st, "ok", "Practice defaults saved.", study.reminder ? "Reminder on: " + hourName(study.reminder_hour) + " your time, on days you haven't practiced." : "");
    }).catch(function (err) { status(st, "err", "We couldn't save your defaults.", message(err)); });
  });

  /* ---------- dashboard layout ---------- */
  var SECTION_NAMES = { kpis: "Score summary", play: "Play and earn", today: "Today's set", scores: "Practice test scores", domains: "Skill areas",
    review: "Review queue", plan: "Week-by-week plan", account: "Your account" };
  var PIN_NAMES = { levels: "Level up", speed: "Speed round", focus: "Focus timer", lessons: "Lessons", practice_test: "Practice test",
    practice: "Topic practice", review: "Review queue", plan: "Study plan", rewards: "Rewards and shop", calculator: "Graphing calculator" };
  var MAX_PINS = 4, layout = null;
  function drawLayout() {
    if (!layout) return;
    $("st-lay-list").innerHTML = layout.order.map(function (k, i) {
      var shown = layout.hidden.indexOf(k) < 0;
      return '<li class="lay-item' + (shown ? "" : " is-hidden") + '"><label class="lay-show" for="lay-' + k + '"><input type="checkbox" id="lay-' + k + '" data-k="' + k + '"' + (shown ? " checked" : "") + ">" +
        "<span>" + SECTION_NAMES[k] + '</span></label><span class="lay-move">' +
        '<button type="button" class="btn btn-quiet" data-up="' + k + '"' + (i === 0 ? " disabled" : "") + ' aria-label="Move ' + SECTION_NAMES[k] + ' up">Up</button>' +
        '<button type="button" class="btn btn-quiet" data-down="' + k + '"' + (i === layout.order.length - 1 ? " disabled" : "") + ' aria-label="Move ' + SECTION_NAMES[k] + ' down">Down</button></span></li>';
    }).join("");
    var full = layout.pins.length >= MAX_PINS;
    $("st-lay-pins").innerHTML = Object.keys(PIN_NAMES).map(function (k) {
      var on = layout.pins.indexOf(k) > -1;
      return '<label class="st-nick" for="pin-' + k + '"><input type="checkbox" id="pin-' + k + '" data-pin="' + k + '"' + (on ? " checked" : "") + (full && !on ? " disabled" : "") + "><span>" + PIN_NAMES[k] + "</span></label>";
    }).join("");
    $("st-lay-pin-note").textContent = layout.pins.length + " of " + MAX_PINS + " pinned" + (full ? ". Unpin one to pick another." : ".");
  }
  $("st-lay-list").addEventListener("click", function (e) {
    var b = e.target.closest("button"); if (!b) return;
    var k = b.getAttribute("data-up") || b.getAttribute("data-down"), i = layout.order.indexOf(k), j = b.getAttribute("data-up") ? i - 1 : i + 1;
    layout.order.splice(i, 1); layout.order.splice(j, 0, k);
    drawLayout();
    var again = document.querySelector('[data-' + (b.getAttribute("data-up") ? "up" : "down") + '="' + k + '"]');
    if (again && !again.disabled) again.focus(); else { var other = document.querySelector('[data-' + (b.getAttribute("data-up") ? "down" : "up") + '="' + k + '"]'); if (other) other.focus(); }
  });
  $("st-lay-list").addEventListener("change", function (e) {
    var k = e.target.getAttribute("data-k"); if (!k) return;
    if (e.target.checked) layout.hidden = layout.hidden.filter(function (x) { return x !== k; }); else layout.hidden.push(k);
    e.target.closest(".lay-item").classList.toggle("is-hidden", !e.target.checked);
  });
  $("st-lay-pins").addEventListener("change", function (e) {
    var k = e.target.getAttribute("data-pin"); if (!k) return;
    if (e.target.checked) layout.pins.push(k); else layout.pins = layout.pins.filter(function (x) { return x !== k; });
    drawLayout(); var again = $("pin-" + k); if (again) again.focus();
  });
  $("st-lay-reset").addEventListener("click", function () {
    var d = T.defaults.dashboard; layout = { order: d.order.slice(), hidden: [], pins: [] }; drawLayout();
    status($("st-lay-status"), "ok", "Back to the original layout. Press Save layout to keep it.");
  });
  $("st-lay-save").addEventListener("click", function () {
    var btn = this, st = $("st-lay-status"); clear(st);
    savePrefs({ dashboard: layout }, btn).then(function () { status(st, "ok", "Layout saved.", "Your dashboard shows it now."); })
      .catch(function (err) { status(st, "err", "We couldn't save your layout.", message(err)); });
  });

  // Saves prefs: to the account on the live site, in this browser in the preview.
  function savePrefs(change, btn) {
    busy(btn, true, "Saving…");
    var done = function (v) { busy(btn, false); return v; }, fail = function (err) { busy(btn, false); throw err; };
    if (!LIVE) {
      T.setPrefs(change);
      var pr = T.prefs(), me = Object.assign({}, T.me(), { prefs: pr, appearance: T.get(), avatar_drawn: pr.avatar.mode === "drawn" ? pr.avatar.parts : null });
      if (T.setMe) T.setMe(me);
      return Promise.resolve().then(done);
    }
    return API.call("/api/me/prefs", change, "PATCH").then(function (r) { if (T.setMe) T.setMe(r.user); user = Object.assign({}, user, r.user); return r; }).then(done, fail);
  }

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
    API.call("/api/me").then(function (r) { render(r.user); loadPlay(); }, function (err) {
      if (err && err.status === 401) location.href = "/signin.html?next=/settings.html";
    });
  } else {
    $("st-preview-note").hidden = false;
    $("st-export").hidden = true; $("st-export-note").hidden = false;
    render(T.me());
    loadPlay();
  }
})();
