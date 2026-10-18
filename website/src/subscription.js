/* subscription.html: the student's own plan, on its own page. Every locked feature on the site sends students here
   (subscription.html?feature=mock_test&from=practice.html), with the plan that unlocks it already picked. See what's included and what's locked, switch plans,
   pause, cancel or undo a cancellation, fix a failed payment and see the billing history.
   Live: /api/me/subscription (backend routes/subscription.py). Preview: practice-local.js answers the same
   requests in this browser, sharing the plan with the parent dashboard preview. */
(function () {
  "use strict";
  var panel = document.getElementById("subscription");
  if (!panel) return;
  var API = window.GraphiteAPI;
  var LIVE = !!(API && API.live);
  var call = LIVE ? API.call : (window.GraphitePracticeLocal && window.GraphitePracticeLocal.call);
  if (!call) return;
  function $(id) { return document.getElementById(id); }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function money(c) { return "$" + (c / 100).toLocaleString("en-US", { maximumFractionDigits: 2 }); }
  function day(iso) { if (!iso) return ""; var p = iso.slice(0, 10).split("-"); return new Date(+p[0], p[1] - 1, +p[2]).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" }); }
  function status(kind, text) {
    var el = $("sub-status");
    el.className = "status" + (text ? " is-shown " + kind : "");
    el.textContent = text || "";
    if (text) el.focus();
  }
  var D = null, pick = null;
  $("sub-preview-note").hidden = LIVE;
  var Q = new URLSearchParams(location.search);
  var FEATURE = Q.get("feature"), FROM = safeFrom(Q.get("from")), preset = false;
  // Only pages on this site, like practice.html?session=4, so the link can't send anyone elsewhere.
  function safeFrom(f) { return f && /^[a-z0-9-]+\.html([?#][A-Za-z0-9=&#%._-]*)?$/.test(f) ? f : null; }
  function backLink(text) {
    if (!FROM) return null;
    var a = document.createElement("a"); a.className = "btn btn-secondary"; a.href = FROM; a.textContent = text || "Go back to what you were doing";
    return a;
  }
  function context(d) {
    var box = $("sub-context"), f = FEATURE && d.access.features[FEATURE];
    box.hidden = !f;
    if (!f) return;
    box.innerHTML = "";
    box.className = "sub-context" + (f.ok ? " is-open" : f.reason ? " is-unpaid" : "");
    var head = document.createElement("strong"), p = document.createElement("p");
    if (f.ok) {
      head.textContent = f.name + " " + (/s$/.test(f.name) ? "are" : "is") + " unlocked.";
      p.textContent = "Your plan includes it now.";
    } else {
      var t = window.GraphiteLock ? GraphiteLock.text(f) : { title: f.name + " is locked", text: "" };
      head.textContent = t.title;
      p.textContent = f.reason ? t.text : t.text + " " + f.need_name + " is picked for you below.";
      $("sub-h1").textContent = f.reason ? "Fix your payment" : "Unlock " + f.name.toLowerCase();
    }
    box.appendChild(head); box.appendChild(p);
    var back = backLink(f.ok ? "Go back to " + f.name.toLowerCase() : "Not now, go back");
    if (back) { var row = document.createElement("div"); row.className = "pd-row"; row.appendChild(back); box.appendChild(row); }
  }

  var STATUS = {
    active: function (s) { return s.plan === "free" ? "Free plan" : "Active · renews " + day(s.renews_on); },
    canceled: function (s) { return "Canceled · stays on until " + day(s.renews_on); },
    paused: function (s) { return "Paused until " + day(s.paused_until); },
    past_due: function () { return "Payment didn't go through"; }
  };
  var FEATURE_ORDER = ["mock_test", "practice_set", "explanations", "review_queue", "study_plan", "level_up", "score_history", "parent_dashboard"];

  function includes(acc) {
    var ul = $("sub-includes"); ul.innerHTML = "";
    FEATURE_ORDER.forEach(function (k) {
      var f = acc.features[k]; if (!f) return;
      var li = document.createElement("li");
      li.className = f.ok ? "is-on" : "is-off";
      var detail = "";
      if (f.limit === 0 || (!f.ok && !f.period)) detail = f.reason ? "Locked until paid" : "With " + f.need_name;
      else if (f.period && f.limit != null) detail = (f.left || 0) + " of " + f.limit + " left this " + f.period;
      else if (f.period && f.ok) detail = "Unlimited";
      else if (!f.ok) detail = f.reason ? "Locked until paid" : "With " + f.need_name;
      li.innerHTML = '<span class="sub-mark" aria-hidden="true">' + (f.ok ? "✓" : "–") + '</span><span class="sub-feat"></span><span class="sub-detail"></span>';
      li.querySelector(".sub-feat").textContent = f.name;
      li.querySelector(".sub-detail").textContent = detail;
      ul.appendChild(li);
    });
  }

  function now(d) {
    var s = d.subscription, box = $("sub-now");
    var chip = s.status === "past_due" ? "chip chip-due" : s.plan === "free" ? "chip chip-quiet" : "chip";
    var payer = d.payer ? (d.payer.you ? "You pay for this plan." : esc(d.payer.name) + " (parent) pays for this plan.") : "";
    box.innerHTML = '<div class="sub-card"><div><p class="label">Your plan</p><h3 class="sub-name"></h3><p class="sub-price"></p></div>' +
      '<span class="' + chip + '" id="sub-chip"></span></div><p class="fine sub-payer">' + payer + "</p>";
    box.querySelector(".sub-name").textContent = s.plan_name;
    box.querySelector(".sub-price").textContent = s.price_label;
    box.querySelector("#sub-chip").textContent = (STATUS[s.status] || STATUS.active)(s);
    if (d.access.unpaid) {
      var warn = document.createElement("div");
      warn.className = "lock-card is-unpaid";
      warn.innerHTML = '<div class="lock-copy"><strong></strong><p></p></div>';
      warn.querySelector("strong").textContent = d.access.unpaid + ".";
      warn.querySelector("p").textContent = s.status === "paused"
        ? "Paid features are locked while the plan is paused. Resume it to unlock everything."
        : "Paid features are locked until the bill is paid. Update the card and pay below, and everything unlocks right away.";
      box.appendChild(warn);
    }
  }

  function plans(d) {
    var box = $("sub-plans"), iv = (document.querySelector('input[name="sub-iv"]:checked') || {}).value || "month";
    var cur = d.subscription.plan;
    if (!pick) pick = cur === "free" ? "no2" : cur;
    box.innerHTML = "";
    d.plans.forEach(function (p) {
      var id = "sub-plan-" + p.key, price = p.cents[iv] ? money(p.per_month_cents[iv]) + "/month" + (iv === "month" ? "" : ", billed " + money(p.cents[iv]) + " " + { week: "weekly", year: "yearly" }[iv]) : "Free";
      var lab = document.createElement("label");
      lab.className = "sub-plan" + (p.key === cur ? " is-current" : "");
      lab.setAttribute("for", id);
      lab.innerHTML = '<input type="radio" name="sub-plan" id="' + id + '" value="' + p.key + '"' + (p.key === pick ? " checked" : "") + ">" +
        '<span class="sub-plan-name"></span><span class="sub-plan-price"></span><span class="fine sub-plan-blurb"></span>' +
        (p.key === cur ? '<span class="chip chip-quiet">Current</span>' : "");
      lab.querySelector(".sub-plan-name").textContent = p.name;
      lab.querySelector(".sub-plan-price").textContent = price;
      lab.querySelector(".sub-plan-blurb").textContent = p.blurb;
      lab.querySelector("input").addEventListener("change", function () { pick = p.key; label(); });
      box.appendChild(lab);
    });
    label();
  }
  function label() {
    var b = $("sub-change-go"), cur = D.subscription.plan;
    var iv = (document.querySelector('input[name="sub-iv"]:checked') || {}).value;
    var same = pick === cur && (cur === "free" || D.subscription.interval === iv);
    var name = (D.plans.filter(function (p) { return p.key === pick; })[0] || {}).name;
    b.disabled = same;
    b.textContent = same ? "This is your plan" : pick === "free" ? "Switch to the free plan" : (D.payments_live ? "Continue to payment" : "Switch to " + name);
    $("sub-agree").closest(".sub-agree").hidden = pick === "free";
  }

  function manage(d) {
    var s = d.subscription, box = $("sub-actions"); box.innerHTML = "";
    function btn(text, cls, fn) {
      var b = document.createElement("button"); b.type = "button"; b.className = "btn " + cls; b.textContent = text;
      b.addEventListener("click", function () { fn(b); }); box.appendChild(b); return b;
    }
    var paid = s.plan !== "free";
    var notes = [];
    if (s.status === "past_due" || (paid && d.payments_live && d.has_card)) {
      btn(s.status === "past_due" ? "Update card and pay" : "Card and receipts", s.status === "past_due" ? "btn-primary" : "btn-secondary", portal);
    }
    if (paid && s.status === "active") btn("Pause for " + d.pause_days + " days", "btn-secondary", function (b) { act("pause", b); });
    if (s.status === "paused") btn("Resume now", "btn-primary", function (b) { act("resume", b); });
    if (s.status === "canceled") btn("Keep my plan", "btn-primary", function (b) { act("resume", b); });
    if (paid && s.status !== "canceled") {
      var armed = false;
      btn("Cancel plan", "btn-quiet", function (b) {
        if (!armed) { armed = true; b.textContent = "Tap again to cancel"; setTimeout(function () { armed = false; b.textContent = "Cancel plan"; }, 4000); return; }
        act("cancel", b);
      });
      notes.push("Canceling keeps " + s.plan_name + " until " + day(s.renews_on) + ", then you're on the free plan. Pausing stops billing for " + d.pause_days + " days, and paid features are locked while it's paused.");
    }
    if (!paid) notes.push("You're on the free plan. Pick a plan above to unlock more.");
    if (d.payer && !d.payer.you) notes.push("A parent pays for this plan, so the card is on their parent dashboard.");
    if (!d.payments_live) notes.push("Payments aren't connected on this site yet, so plan changes take effect without charging a card.");
    $("sub-manage-note").textContent = notes.join(" ");
  }

  function billing(d) {
    var ul = $("sub-billing"); ul.innerHTML = "";
    if (!d.billing.length) { ul.innerHTML = '<li><p class="fine">No billing yet.</p></li>'; return; }
    d.billing.forEach(function (b) {
      var li = document.createElement("li");
      li.innerHTML = '<div><strong></strong><p class="fine"></p></div><span class="mono"></span>';
      li.querySelector("strong").textContent = day(b.at);
      li.querySelector(".fine").textContent = b.detail;
      li.querySelector(".mono").textContent = b.amount_cents ? money(b.amount_cents) : "";
      ul.appendChild(li);
    });
  }

  // The test account (beta) switches plans and payment states with one click.
  function testBox(d) {
    var box = $("sub-test");
    box.hidden = !d.test_account;
    if (!d.test_account) return;
    var s = d.subscription;
    function button(text, on, fn) {
      var b = document.createElement("button");
      b.type = "button"; b.className = "btn " + (on ? "btn-primary" : "btn-secondary");
      b.textContent = text; b.setAttribute("aria-pressed", String(!!on));
      b.addEventListener("click", function () { if (!on) fn(b); });
      return b;
    }
    var plansRow = $("sub-test-plans"); plansRow.innerHTML = "";
    d.plans.forEach(function (p) {
      plansRow.appendChild(button(p.name, p.key === s.plan, function (b) { testSwitch(p.key, "active", b); }));
    });
    var states = $("sub-test-states"); states.innerHTML = "";
    if (s.plan !== "free") {
      [["active", "Paid"], ["past_due", "Payment failed"], ["paused", "Paused"], ["canceled", "Canceled"]].forEach(function (x) {
        states.appendChild(button(x[1], s.status === x[0], function (b) { testSwitch(s.plan, x[0], b); }));
      });
    }
    states.hidden = s.plan === "free";
  }
  function testSwitch(plan, state, b) {
    b.disabled = true;
    call("/api/me/subscription/test", { plan: plan, status: state }).then(function (d) {
      pick = null; render(d);
      status("success", "Test account: now " + d.subscription.plan_name + (state === "active" ? "" : " (" + state.replace("_", " ") + ")") + ". Every page uses it right away.");
    }).catch(function (err) { b.disabled = false; fail(err); });
  }

  function render(d) {
    D = d;
    testBox(d);
    var f = FEATURE && d.access.features[FEATURE];
    if (f && !f.ok && f.need && !preset) { pick = f.need; preset = true; }
    now(d); includes(d.access); plans(d); manage(d); billing(d); context(d);
  }
  function fail(err) {
    if (err && err.status === 401) { location.href = "signin.html?next=" + encodeURIComponent("/subscription.html" + location.search); return; }
    if (err && err.data && err.data.code === "parent_account") { location.href = "parent.html#billing"; return; }
    status("error", err && err.status ? err.message : "We couldn't reach Graphite SAT. Check your connection and try again.");
  }
  function load() { return call("/api/me/subscription").then(render).catch(fail); }

  function act(action, b) {
    b.disabled = true;
    call("/api/me/subscription/" + action, {}).then(function (d) {
      render(d);
      status("success", { pause: "Paused. Billing stops for " + d.pause_days + " days.", resume: "Your plan is active again.",
        cancel: "Canceled. Your plan stays on until " + day(d.subscription.renews_on) + "." }[action]);
    }).catch(function (err) { b.disabled = false; fail(err); });
  }
  function portal(b) {
    b.disabled = true;
    call("/api/me/subscription/portal", {}).then(function (r) { location.href = r.url; })
      .catch(function (err) { b.disabled = false; fail(err); });
  }

  Array.prototype.forEach.call(document.querySelectorAll('input[name="sub-iv"]'), function (r) {
    r.addEventListener("change", function () { if (D) plans(D); });
  });
  $("sub-change").addEventListener("submit", function (e) {
    e.preventDefault();
    if (!D) return;
    var iv = (document.querySelector('input[name="sub-iv"]:checked') || {}).value;
    if (pick !== "free" && !$("sub-agree").checked) { status("error", "Check the box to agree to the terms and automatic renewal."); $("sub-agree").focus(); return; }
    var b = $("sub-change-go"); b.disabled = true; b.textContent = "Saving…";
    call("/api/me/subscription/plan", { plan: pick, interval: iv, agree: $("sub-agree").checked }).then(function (d) {
      if (d.checkout_url) { location.href = d.checkout_url; return; }
      pick = null; $("sub-agree").checked = false;
      render(d);
      status("success", d.subscription.status === "canceled" ? "Your plan stays on until " + day(d.subscription.renews_on) + ", then you're on the free plan."
        : d.subscription.plan === "free" ? "You're on the free plan now. The list shows what's included and what's locked."
        : "You're on " + d.subscription.plan_name + ". Everything it includes is unlocked.");
    }).catch(function (err) { label(); fail(err); });
  });
  load();
})();
