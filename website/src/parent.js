/* Graphite SAT parent dashboard: a linked student's progress, alerts, activity, plan and settings.
   Live: talks to /api/parent. Preview: the same requests go to GraphitePracticeLocal (practice-local.js),
   which treats the practice done in this browser as the student's. */
(function () {
  "use strict";
  var root = document.getElementById("pd-main");
  if (!root) return;
  function $(id) { return document.getElementById(id); }
  var API = window.GraphiteAPI;
  var LIVE = !!(API && API.live);
  var Local = window.GraphitePracticeLocal;
  function call(path, data, method) { return LIVE ? API.call(path, data, method) : Local.call(path, data, method); }
  var STUDENT_KEY = "graphite_parent_student";
  var home = null, current = null, S = null, busy = false;

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function showError(msg) { var e = $("pd-error"); e.textContent = msg || ""; e.hidden = !msg; }
  function status(id, kind, msg) { var s = $(id); s.className = "status is-shown " + kind; s.textContent = msg; }
  function clearStatus(id) { var s = $(id); s.className = "status"; s.textContent = ""; }
  function failed(err, fallback) {
    if (err && err.status === 401) { location.href = "/signin.html?as=parent&next=/parent.html"; return ""; }
    return err && err.status ? err.message : fallback;
  }
  function money(cents) { return "$" + (cents / 100).toLocaleString("en-US", { minimumFractionDigits: cents % 100 ? 2 : 0 }); }
  function day(iso) {
    if (!iso) return "";
    var d = new Date(iso.length === 10 ? iso + "T12:00:00" : iso);
    return d.toLocaleDateString("en-US", { month: "short", day: "numeric", year: d.getFullYear() !== new Date().getFullYear() ? "numeric" : undefined });
  }
  function ago(iso) {
    if (!iso) return "Not yet";
    var then = new Date(iso.slice(0, 10) + "T12:00:00"), now = new Date();
    var n = Math.round((new Date(now.getFullYear(), now.getMonth(), now.getDate(), 12) - then) / 86400000);
    return n <= 0 ? "Today" : n === 1 ? "Yesterday" : n + " days ago";
  }
  function plural(n, one, many) { return n + " " + (n === 1 ? one : many); }

  if (!LIVE) $("pd-preview-note").hidden = false;

  /* ---------- loading ---------- */
  function load() {
    call("/api/parent").then(function (h) {
      home = h;
      $("account-email").textContent = h.parent.email;
      $("pd-hello").textContent = "Hi, " + h.parent.name.split(" ")[0];
      $("pd-pay-note").hidden = !!h.payments_live;
      var save = Math.max.apply(null, h.plans.map(function (p) { return p.savings ? p.savings.year.percent : 0; }));
      if (save > 0) document.querySelector('label[for="pd-int-year"]').textContent = "Yearly · save " + save + "%";
      fillSelects();
      $("pd-loading").hidden = true;
      if (!h.students.length) { showConnect(false); return; }
      var saved = null; try { saved = Number(localStorage.getItem(STUDENT_KEY)); } catch (e) { /* storage blocked */ }
      var pick = h.students.filter(function (s) { return s.id === saved; })[0] || h.students[0];
      renderSwitch(pick.id);
      openStudent(pick.id);
    }).catch(function (err) { $("pd-loading").textContent = failed(err, "We couldn't load your dashboard. Check your connection and refresh."); });
  }
  function renderSwitch(id) {
    var sel = $("pd-student"); sel.innerHTML = "";
    home.students.forEach(function (s) { var o = document.createElement("option"); o.value = s.id; o.textContent = s.name; o.selected = s.id === id; sel.appendChild(o); });
    $("pd-switch").hidden = home.students.length < 2;
  }
  $("pd-student").addEventListener("change", function () { openStudent(Number(this.value)); });
  function openStudent(id) {
    current = id;
    try { localStorage.setItem(STUDENT_KEY, String(id)); } catch (e) { /* storage blocked */ }
    call("/api/parent/students/" + id).then(function (s) {
      $("pd-connect").hidden = true; root.hidden = false; render(s);
    }).catch(function (err) { showError(failed(err, "We couldn't load your student's progress.")); });
  }

  /* ---------- connect a student ---------- */
  function showConnect(cancelable) {
    $("pd-connect").hidden = false; $("pd-code-cancel").hidden = !cancelable;
    if (!cancelable) root.hidden = true;
    $("pd-code").focus();
  }
  $("pd-add").addEventListener("click", function () { showConnect(true); $("pd-connect").scrollIntoView({ block: "start" }); });
  $("pd-code-cancel").addEventListener("click", function () { $("pd-connect").hidden = true; });
  $("pd-code").addEventListener("input", function () {
    var v = this.value.toUpperCase().replace(/[^A-Z0-9]/g, "").slice(0, 8);
    this.value = v.length > 4 ? v.slice(0, 4) + "-" + v.slice(4) : v;
  });
  $("pd-code-form").addEventListener("submit", function (e) {
    e.preventDefault();
    if (busy) return;
    var code = $("pd-code").value.trim();
    if (code.replace(/[^A-Z0-9]/gi, "").length !== 8) { status("pd-code-status", "err", "Codes are 8 letters and numbers, like K7QM-4ZTR."); return; }
    busy = true; clearStatus("pd-code-status");
    call("/api/parent/link", { code: code }).then(function (r) {
      busy = false; $("pd-code").value = "";
      home.students = home.students.filter(function (s) { return s.id !== r.student.id; }).concat([r.student]);
      renderSwitch(r.student.id); openStudent(r.student.id);
    }).catch(function (err) { busy = false; status("pd-code-status", "err", failed(err, "We couldn't connect. Check your connection and try again.")); });
  });

  /* ---------- render ---------- */
  // The student's progress comes with Mechanical. Without it (or while a plan isn't paid), the parent still
  // sees alerts, settings, and the plan and billing, so they can pay or upgrade.
  function lockedView(s) {
    var locked = !!(s.access && !s.access.ok);
    $("overview").querySelector(".pd-kpis").hidden = locked;
    $("progress").hidden = locked; $("activity").hidden = locked;
    var old = document.getElementById("pd-lock"); if (old) old.remove();
    if (locked && window.GraphiteLock) {
      var card = GraphiteLock.card(s.access);
      card.id = "pd-lock";
      card.querySelector("strong").textContent = s.access.reason ? s.access.reason : "Progress reports come with " + s.access.need_name;
      card.querySelector("p").textContent = s.access.reason ? s.student.first_name + "'s progress is locked until the plan is paid. Update the card under Plan and billing."
        : "Scores, skills, study time and weekly emails are part of " + s.access.need_name + ". Copy alerts and billing always show here.";
      card.querySelector("a").setAttribute("href", "#billing");
      $("overview").insertAdjacentElement("afterend", card);
    }
    return locked;
  }
  function render(s) {
    S = s;
    var st = s.student, o = s.overview;
    $("pd-name").textContent = st.name;
    $("pd-student-meta").textContent = [st.grade ? st.grade + "th grade" : null, st.target_score ? "Target " + st.target_score : null,
      st.test_date ? "SAT on " + day(st.test_date) : "No SAT date yet"].filter(Boolean).join(" · ");
    if (lockedView(s)) {
      $("pd-countdown").hidden = true;
      $("pd-alerts").innerHTML = s.alerts.map(function (a) {
        return '<li class="pd-alert ' + a.level + '"><span class="pd-alert-dot" aria-hidden="true"></span>' + esc(a.text) + "</li>";
      }).join("");
      renderBilling(); renderSettings(); renderFamily();
      return;
    }
    var cd = $("pd-countdown");
    cd.hidden = o.days_to_test == null;
    if (o.days_to_test != null) cd.textContent = o.days_to_test === 0 ? "SAT today" : plural(o.days_to_test, "day", "days") + " to the SAT";

    $("pd-minutes").textContent = o.minutes_week + " min";
    $("pd-goal").textContent = "of a " + (o.goal_minutes / 60) + "-hour goal";
    $("pd-goal-meter").style.width = Math.min(100, Math.round(o.minutes_week / Math.max(1, o.goal_minutes) * 100)) + "%";
    var days = o.study_days_week.filter(Boolean).length;
    $("pd-days").textContent = days + " of 7";
    $("pd-week").innerHTML = ["M", "T", "W", "T", "F", "S", "S"].map(function (d, i) { return '<i class="' + (o.study_days_week[i] ? "on" : "") + '">' + d + "</i>"; }).join("");
    $("pd-streak").textContent = plural(o.streak_days, "day", "days");
    $("pd-last").textContent = "Last practiced: " + ago(o.last_active);
    $("pd-questions").textContent = String(o.questions_week);
    $("pd-accuracy").textContent = o.accuracy_week == null ? "No finished sets yet" : o.accuracy_week + "% right in finished sets";

    $("pd-alerts").innerHTML = s.alerts.length ? s.alerts.map(function (a) {
      return '<li class="pd-alert ' + a.level + '"><span class="pd-alert-dot" aria-hidden="true"></span>' + esc(a.text) + "</li>";
    }).join("") : '<li class="pd-alert good"><span class="pd-alert-dot" aria-hidden="true"></span>All on track. Nothing needs your attention.</li>';

    // Progress
    $("pd-scores-meta").textContent = s.scores.length ? plural(s.scores.length, "test", "tests") : "";
    $("pd-scores").innerHTML = s.scores.length ? s.scores.slice(-8).map(function (x) {
      return '<li><span class="bar-name">' + esc(x.label) + " · " + x.correct + " of " + x.total + '</span><span class="bar-track"><span style="width:' + x.pct + '%"></span></span><span class="bar-val">' + x.pct + "%</span></li>";
    }).join("") : '<li class="pd-empty">No practice tests yet. Scores show up here after the first one.</li>';
    var measured = s.domains.filter(function (d) { return d.pct != null; });
    $("pd-skills").innerHTML = measured.length ? s.domains.map(function (d) {
      return '<li><span class="bar-name">' + esc(d.name) + (d.focus ? ' <span class="chip">Focus</span>' : "") + '</span><span class="bar-track' + (d.pct == null ? " is-empty" : "") +
        '"><span style="width:' + (d.pct || 0) + '%"></span></span><span class="bar-val">' + (d.pct == null ? "–" : d.pct + "%") + "</span></li>";
    }).join("") : '<li class="pd-empty">Skill scores appear after a practice test.</li>';
    var dg = s.diagnostic;
    $("pd-diag-meta").textContent = dg ? day(dg.at) : "";
    $("pd-diag").innerHTML = dg ? '<p class="pd-big">' + dg.correct + " of " + dg.total + ' right</p>' +
      (dg.strengths.length ? '<h3 class="pd-small">Strongest</h3><ul class="pl-tags">' + dg.strengths.map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("") + "</ul>" : "") +
      (dg.focus.length ? '<h3 class="pd-small">Easiest points to gain</h3><ul class="pl-tags pl-tags-focus">' + dg.focus.map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("") + "</ul>" : "")
      : '<p class="pd-empty">Not taken yet. The 10-question diagnostic builds your student\'s study plan.</p>';
    var pl = s.plan;
    $("pd-plan-meta").textContent = pl ? "Week " + pl.week + " of " + pl.weeks : "";
    $("pd-plan").innerHTML = pl ? '<p class="pd-big">' + pl.done + " of " + pl.tasks + ' tasks done</p><span class="meter"><span style="width:' + Math.round(pl.done / Math.max(1, pl.tasks) * 100) + '%"></span></span>' +
      '<p class="fine">' + esc(pl.phase) + (pl.focus.length ? ": " + esc(pl.focus.join(" and ")) : "") + (pl.difficulty ? ". " + esc(pl.difficulty) : "") + "</p>"
      : '<p class="pd-empty">The plan is built after the diagnostic.</p>';
    $("pd-levels").innerHTML = s.levels.map(function (t) {
      return '<li><span>' + esc(t.name) + '</span><span class="pd-lv"><span class="pd-lv-bar"><span style="width:' + Math.round(t.passed / t.levels * 100) + '%"></span></span><strong>Level ' + t.unlocked + "</strong></span></li>";
    }).join("");
    $("pd-review").textContent = s.review.total ? plural(s.review.total, "question", "questions") + " to review" + (s.review.due ? ", " + s.review.due + " due now" : "") : "Nothing waiting";

    // Activity
    $("pd-activity").innerHTML = s.activity.length ? s.activity.map(function (a) {
      var pct = a.total ? Math.round(a.correct / a.total * 100) : 0;
      return '<li><span class="pd-act-day">' + day(a.at) + '</span><span class="pd-act-main"><strong>' + esc(a.title) + '</strong><span class="fine">' + esc(a.kind) +
        (a.minutes != null ? " · " + plural(a.minutes, "minute", "minutes") : "") + '</span></span><span class="pd-act-score ' + (pct >= 70 ? "ok" : pct >= 50 ? "" : "low") + '">' + a.correct + "/" + a.total + "</span></li>";
    }).join("") : '<li class="pd-empty">No finished practice yet.</li>';

    renderBilling();
    renderSettings();
    renderFamily();
  }

  /* ---------- plan and billing ---------- */
  function interval() { return $("pd-int-week").checked ? "week" : $("pd-int-month").checked ? "month" : "year"; }
  function renderBilling() {
    var sub = S.subscription;
    var state = sub.status === "paused" ? "Paused until " + day(sub.paused_until) + ". Next bill " + day(sub.renews_on) + "."
      : sub.status === "trial" ? "Free trial, no card. Ends " + day(sub.renews_on) + ", then the plan goes back to free by itself."
      : sub.status === "canceled" ? "Canceled. Stays on until " + day(sub.renews_on) + ", then switches to the free plan."
      : sub.plan === "free" ? "The free plan. Upgrade any time." : "Renews " + day(sub.renews_on) + ".";
    $("pd-current").innerHTML = '<div><p class="label">Current plan</p><p class="pd-plan-name">' + esc(sub.plan_name) + ' <span class="pd-price">' + esc(sub.price_label) + "</span></p>" +
      '<p class="fine">' + esc(state) + "</p></div>" + '<span class="chip pd-status-' + sub.status + '">' + (sub.status === "active" ? "Active" : sub.status === "paused" ? "Paused" : sub.status === "past_due" ? "Payment failed" : sub.status === "trial" ? "Trial" : "Canceled") + "</span>";
    if (sub.interval && $("pd-int-" + sub.interval)) $("pd-int-" + sub.interval).checked = true;
    closeConfirm();
    drawPlans();
    var acts = [];
    if (sub.status === "active" && sub.plan !== "free") acts.push(["pause", "btn-secondary", "Pause for 30 days"], ["cancel", "btn-quiet", "Cancel plan"]);
    if (sub.status === "paused") acts.push(["resume", "btn-primary", "Resume now"], ["cancel", "btn-quiet", "Cancel plan"]);
    if (sub.status === "canceled") acts.push(["resume", "btn-primary", "Keep " + sub.plan_name]);
    if (sub.status === "trial") acts.push(["cancel", "btn-quiet", "Cancel the trial"]);
    if (sub.status === "past_due") acts.push(["portal", "btn-primary", "Update card and pay"], ["cancel", "btn-quiet", "Cancel plan"]);
    else if (home.payments_live && sub.plan !== "free") acts.push(["portal", "btn-quiet", "Card and receipts"]);
    $("pd-plan-actions").innerHTML = acts.map(function (a) { return '<button class="btn ' + a[1] + '" type="button" data-act="' + a[0] + '">' + a[2] + "</button>"; }).join("");
    $("pd-history").innerHTML = S.billing.length ? S.billing.map(function (b) {
      return '<li><span class="pd-act-day">' + day(b.at) + "</span><span>" + esc(b.detail) + "</span></li>";
    }).join("") : '<li class="pd-empty">No changes yet.</li>';
  }
  function drawPlans() {
    var sub = S.subscription, iv = interval();
    $("pd-plans").innerHTML = home.plans.map(function (p) {
      // Always shown per month; the small line under it says what's actually billed.
      var cents = p.cents ? p.cents[iv] : (iv === "year" ? p.year_cents : p.month_cents);
      var each = p.per_month_cents ? p.per_month_cents[iv] : (iv === "year" ? Math.round(cents / 12) : cents);
      // A student still paying an older plan's price (sub.legacy) can switch to the same plan at today's price.
      var here = p.key === sub.plan && (p.key === "free" || (sub.interval === iv && !sub.legacy));
      var price = p.key === "free" ? "Free" : money(each) + "/month";
      var save = p.savings && p.savings[iv] && iv === "year" && p.savings[iv].percent > 0 ? " Saves " + money(p.savings[iv].per_year_cents) + " a year." : "";
      var billedLine = p.key === "free" ? "" : iv === "month" ? "Billed monthly." : "Billed " + money(cents) + (iv === "week" ? " weekly." : " yearly.") + save;
      var sub2 = billedLine ? '<span class="pd-billed">' + esc(billedLine) + "</span>" : "";
      var action;
      if (here) action = '<span class="chip">Current plan</span>';
      else if (p.key === "free" && sub.status === "canceled") action = '<span class="chip chip-quiet">Starts ' + esc(day(sub.renews_on)) + "</span>";
      else if (p.key === "free") action = '<button class="btn btn-quiet" type="button" data-free>Switch to free</button>';
      else action = '<a class="btn btn-secondary" href="checkout.html?plan=' + p.key + "&amp;interval=" + iv + "&amp;student=" + current + '">' +
        (p.key === sub.plan && !sub.legacy ? "Switch to " + (iv === "week" ? "weekly" : iv === "month" ? "monthly" : "yearly") : "Choose " + esc(p.name)) + "</a>";
      return '<article class="pd-plan' + (here ? " is-current" : "") + '"><h3>' + esc(p.name) + '</h3><p class="pd-plan-price">' + price + "</p>" + sub2 +
        '<p class="fine">' + esc(p.blurb) + "</p>" + action + "</article>";
    }).join("");
  }
  $("pd-interval").addEventListener("change", drawPlans);
  var confirmArmed = null;
  function planRequest(path, data, done, btn) {
    if (busy) return;
    busy = true; clearStatus("pd-plan-status");
    var label = btn.textContent; btn.disabled = true; btn.textContent = "Saving…";
    call(path, data || {}).then(function (r) {
      busy = false; S.subscription = r.subscription; S.billing = r.billing; closeConfirm(); renderBilling();
      status("pd-plan-status", "ok", done(r.subscription));
      $("pd-plan-status").focus();
    }).catch(function (err) { busy = false; btn.disabled = false; btn.textContent = label; status("pd-plan-status", "err", failed(err, "That didn't save. Try again.")); });
  }
  // Disconnecting a student asks for a second press. Only one button is armed at a time.
  function confirmFirst(btn, key, text) {
    if (confirmArmed === key) { confirmArmed = null; return true; }
    confirmArmed = key; btn.textContent = text;
    setTimeout(function () { if (confirmArmed === key) { confirmArmed = null; renderFamily(); } }, 5000);
    return false;
  }

  // Switching to free and canceling are the same thing: the paid plan runs to the end of the time paid for,
  // then the free plan starts. One clear question instead of a button that changes its label.
  var confirmFrom = null;
  function openConfirm(from) {
    var sub = S.subscription, free = home.plans[0], first = S.student.first_name || "your student";
    confirmFrom = from;
    $("pd-confirm").innerHTML = '<h3 id="pd-confirm-title" tabindex="-1">Switch to ' + esc(free.name) + "?</h3>" +
      "<p>" + esc(sub.plan_name) + " stays on until " + esc(day(sub.renews_on)) + ", the end of the time already paid for. Then " + esc(first) +
      " moves to the free plan: " + esc(free.blurb.charAt(0).toLowerCase() + free.blurb.slice(1)) + "</p>" +
      '<p class="fine">Nothing else is charged. You can undo this any time before ' + esc(day(sub.renews_on)) + ".</p>" +
      '<div class="pd-row"><button class="btn btn-primary" type="button" data-confirm="yes">Yes, switch to free</button>' +
      '<button class="btn btn-secondary" type="button" data-confirm="no">Keep ' + esc(sub.plan_name) + "</button></div>";
    $("pd-confirm").hidden = false;
    $("pd-confirm-title").focus();
  }
  function closeConfirm(refocus) {
    $("pd-confirm").hidden = true; $("pd-confirm").innerHTML = "";
    if (refocus && confirmFrom) { var b = document.querySelector(confirmFrom); if (b) b.focus(); }
    confirmFrom = null;
  }
  $("pd-confirm").addEventListener("click", function (e) {
    var b = e.target.closest("[data-confirm]"); if (!b) return;
    if (b.getAttribute("data-confirm") === "no") { closeConfirm(true); return; }
    planRequest("/api/parent/students/" + current + "/plan/cancel", null, function (sub) {
      return "Done. " + sub.plan_name + " stays on until " + day(sub.renews_on) + ", then the free plan starts.";
    }, b);
  });
  $("pd-confirm").addEventListener("keydown", function (e) { if (e.key === "Escape") closeConfirm(true); });
  $("pd-plans").addEventListener("click", function (e) {
    if (e.target.closest("[data-free]")) openConfirm("[data-free]");
  });
  $("pd-plan-actions").addEventListener("click", function (e) {
    var b = e.target.closest("[data-act]"); if (!b) return;
    var act = b.getAttribute("data-act");
    if (act === "cancel") { openConfirm('[data-act="cancel"]'); return; }
    if (act === "portal") {
      b.disabled = true;
      call("/api/parent/billing-portal", {}).then(function (r) { location.href = r.url; })
        .catch(function (err) { b.disabled = false; status("pd-plan-status", "err", failed(err, "We couldn't open the billing page. Try again.")); });
      return;
    }
    planRequest("/api/parent/students/" + current + "/plan/" + act, null, function (sub) {
      return act === "pause" ? "Paused until " + day(sub.paused_until) + "." : "The plan is active again.";
    }, b);
  });

  /* ---------- settings ---------- */
  function fillSelects() {
    var g = $("pd-goal-hours"); g.innerHTML = "";
    for (var h = 1; h <= 20; h++) { var o = document.createElement("option"); o.value = h; o.textContent = plural(h, "hour", "hours") + " a week"; g.appendChild(o); }
    var a = $("pd-alert-days"); a.innerHTML = "";
    home.alert_days.forEach(function (d) { var o = document.createElement("option"); o.value = d; o.textContent = d ? plural(d, "day", "days") : "Never (no alerts)"; a.appendChild(o); });
  }
  function renderSettings() {
    var st = S.student;
    $("pd-goal-hours").value = String(st.weekly_goal_hours);
    $("pd-test-date").value = st.test_date || "";
    $("pd-target").value = st.target_score || "";
    $("pd-weekly").checked = S.settings.weekly_report;
    $("pd-alert-days").value = String(S.settings.alert_days);
  }
  $("pd-settings-form").addEventListener("submit", function (e) {
    e.preventDefault();
    if (busy) return;
    var tv = $("pd-target").value.trim();
    if (tv && (!(Number(tv) >= 400 && Number(tv) <= 1600) || Number(tv) % 10)) { status("pd-settings-status", "err", "Target scores run from 400 to 1600 in steps of 10."); return; }
    var data = { weekly_goal_hours: Number($("pd-goal-hours").value), test_date: $("pd-test-date").value || null, target_score: tv ? Number(tv) : null,
                 weekly_report: $("pd-weekly").checked, alert_days: Number($("pd-alert-days").value) };
    busy = true; clearStatus("pd-settings-status");
    call("/api/parent/students/" + current + "/settings", data, "PATCH").then(function (s) {
      busy = false; render(s); status("pd-settings-status", "ok", "Saved. " + s.student.first_name + " sees the new goal and test date too.");
    }).catch(function (err) { busy = false; status("pd-settings-status", "err", failed(err, "That didn't save. Try again.")); });
  });
  $("pd-report").addEventListener("click", function () {
    var b = this; if (busy) return;
    busy = true; b.disabled = true; clearStatus("pd-settings-status");
    call("/api/parent/students/" + current + "/report", {}).then(function (r) {
      busy = false; b.disabled = false; status("pd-settings-status", "ok", "Sent this week's report to " + r.to + ".");
    }).catch(function (err) { busy = false; b.disabled = false; status("pd-settings-status", "err", failed(err, "We couldn't send the report.")); });
  });

  /* ---------- connected students ---------- */
  function renderFamily() {
    $("pd-family").innerHTML = home.students.map(function (s) {
      return '<li><div><strong>' + esc(s.name) + "</strong>" + (s.id === current ? '<p class="fine">Showing now</p>' : "") + '</div><button class="btn btn-quiet" type="button" data-unlink="' + s.id + '">Disconnect</button></li>';
    }).join("");
  }
  $("pd-family").addEventListener("click", function (e) {
    var b = e.target.closest("[data-unlink]"); if (!b) return;
    var id = Number(b.getAttribute("data-unlink"));
    if (!confirmFirst(b, "unlink" + id, "Press again to disconnect")) return;
    call("/api/parent/students/" + id, {}, "DELETE").then(function () {
      home.students = home.students.filter(function (s) { return s.id !== id; });
      if (!home.students.length) { root.hidden = true; showConnect(false); $("pd-switch").hidden = true; return; }
      renderSwitch(home.students[0].id); openStudent(home.students[0].id);
    }).catch(function (err) { showError(failed(err, "We couldn't disconnect. Try again.")); });
  });

  load();
})();
