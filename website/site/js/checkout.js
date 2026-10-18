/* Graphite SAT checkout (checkout.html): pick a plan and how to pay, then pay on Stripe.
   Live: /api/checkout sends the parent to Stripe's payment page, or, before Stripe is connected, starts the plan
   without charging. Preview: the plan is saved in this browser, where the parent dashboard preview reads it.
   Links in: checkout.html?plan=sharpened&interval=year&student=12 (all optional). */
(function () {
  "use strict";
  var form = document.getElementById("co-form");
  if (!form) return;
  function $(id) { return document.getElementById(id); }
  var API = window.GraphiteAPI, LIVE = !!(API && API.live);
  var PLANS = JSON.parse($("plans-data").textContent).filter(function (p) { return p.key !== "free"; });
  var FREE_NAME = JSON.parse($("plans-data").textContent)[0].name;
  var IV = ["week", "month", "year"], WORDS = { week: "weekly", month: "monthly", year: "yearly" };
  var EVERY = { week: "week", month: "month", year: "year" };
  var q = new URLSearchParams(location.search);
  var state = {
    plan: PLANS.some(function (p) { return p.key === q.get("plan"); }) ? q.get("plan") : "sharpened",
    interval: IV.indexOf(q.get("interval")) >= 0 ? q.get("interval") : "year",
    student: Number(q.get("student")) || null, info: null, busy: false
  };

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function money(c, cents) { return "$" + (c / 100).toLocaleString("en-US", { minimumFractionDigits: cents || c % 100 ? 2 : 0, maximumFractionDigits: 2 }); }
  function plan() { return PLANS.filter(function (p) { return p.key === state.plan; })[0]; }
  function status(kind, title, detail) {
    var el = $("co-status"); el.className = "status is-shown " + kind; el.innerHTML = "<p>" + esc(title) + "</p>" + (detail ? "<p>" + esc(detail) + "</p>" : "");
    el.focus();
  }
  function clearStatus() { var el = $("co-status"); el.className = "status"; el.textContent = ""; }
  function today() { var d = state.info && state.info.today ? new Date(state.info.today + "T12:00:00") : new Date(); d.setHours(12, 0, 0, 0); return d; }
  function renewal(iv) {
    var d = today();
    if (iv === "week") d.setDate(d.getDate() + 7);
    else { var day = d.getDate(); d.setDate(1); d.setMonth(d.getMonth() + (iv === "month" ? 1 : 12)); d.setDate(Math.min(day, new Date(d.getFullYear(), d.getMonth() + 1, 0).getDate())); }
    return d;
  }
  function niceDay(d) { return d.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" }); }
  function iso(d) { return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0"); }

  /* ---------- the choices ---------- */
  function drawChoices() {
    $("co-plans").innerHTML = PLANS.map(function (p) {
      return '<span class="co-choice"><input type="radio" name="co-plan" id="co-plan-' + p.key + '" value="' + p.key + '"' + (p.key === state.plan ? " checked" : "") + ">" +
        '<label for="co-plan-' + p.key + '"><span class="co-choice-top"><strong>' + esc(p.name) + "</strong>" + (p.badge ? '<span class="tier-badge">' + esc(p.badge) + "</span>" : "") + "</span>" +
        '<span class="co-choice-price">' + money(p.per_month_cents[state.interval]) + '<small>/month</small></span><span class="co-choice-text">' + esc(p.blurb) + "</span></label></span>";
    }).join("");
    var p = plan();
    $("co-intervals").innerHTML = IV.map(function (iv) {
      var sv = p.savings[iv];
      var note = iv === "year" ? "Save " + sv.percent + "%" : iv === "week" ? "No commitment" : "Cancel anytime";
      return '<span class="co-choice co-iv"><input type="radio" name="co-interval" id="co-iv-' + iv + '" value="' + iv + '"' + (iv === state.interval ? " checked" : "") + ">" +
        '<label for="co-iv-' + iv + '"><strong>' + WORDS[iv].charAt(0).toUpperCase() + WORDS[iv].slice(1) + '</strong><span class="co-choice-price">' + money(p.per_month_cents[iv]) + "<small>/month</small></span>" +
        '<span class="co-iv-note' + (iv === "year" ? " is-save" : "") + '">' + note + "</span></label></span>";
    }).join("");
  }
  function drawSummary() {
    var p = plan(), iv = state.interval, cents = p.cents[iv], sv = p.savings[iv];
    $("co-title").textContent = "Get " + p.name;
    $("co-sum-name").innerHTML = "<strong>" + esc(p.name) + "</strong>, billed " + WORDS[iv];
    $("co-sum-amount").textContent = money(p.per_month_cents[iv]);
    $("co-sum-billed").textContent = iv === "month" ? "Billed monthly." : "Billed " + money(cents) + " " + WORDS[iv] + ".";
    $("co-due").textContent = money(cents, true);
    $("co-renews").textContent = niceDay(renewal(iv)) + ", at " + money(cents) + " a " + EVERY[iv];
    $("co-save-row").hidden = !(iv === "year" && sv.per_year_cents > 0);
    $("co-save").textContent = money(sv.per_year_cents) + " a year (" + sv.percent + "% off)";
    $("co-intro").textContent = p.intro || "";
    $("co-feats").innerHTML = p.features.map(function (f) { return "<li>" + esc(f) + "</li>"; }).join("");
    $("co-agree-text").innerHTML = 'I agree to the <a href="terms.html">terms</a>. ' + esc(p.name) + " renews automatically at " + money(cents) + " every " + EVERY[iv] +
      " until I cancel. I can cancel anytime from the parent dashboard.";
    payLabel();
    // Keep the address in step, so a refresh or a shared link shows the same choice.
    var u = new URLSearchParams(location.search); u.set("plan", state.plan); u.set("interval", iv); u.delete("canceled");
    if (state.student) u.set("student", state.student); else u.delete("student");
    try { history.replaceState(null, "", location.pathname + "?" + u.toString()); } catch (e) { /* not allowed in some previews */ }
  }
  function payLabel() {
    var b = $("co-pay"), p = plan();
    if (state.busy) return;
    b.textContent = !canPay() ? "Continue" : state.info && state.info.payments_live ? "Continue to secure payment" : "Start " + p.name;
    b.disabled = !canPay();
  }
  function canPay() { var a = state.info && state.info.account; return !!(a && (a.role === "parent" || (a.students && a.students.length)) && state.student); }
  form.addEventListener("change", function (e) {
    var t = e.target;
    if (t.name === "co-plan") { state.plan = t.value; drawChoices(); $("co-plan-" + state.plan).focus(); }
    else if (t.name === "co-interval") { state.interval = t.value; drawChoices(); $("co-iv-" + state.interval).focus(); }
    else if (t.id === "co-student") { state.student = Number(t.value); drawWho(); }
    else return;
    drawSummary();
  });

  /* ---------- who it's for ---------- */
  function nextHere() { return encodeURIComponent(location.pathname.replace(/^.*\//, "/") + location.search); }
  function drawWho() {
    var info = state.info, a = info && info.account, el = $("co-who");
    if (!a) {
      el.innerHTML = '<p>Plans are bought from a parent account. It\'s free, and it\'s where you follow progress and manage billing.</p>' +
        '<div class="pd-row"><a class="btn btn-primary" href="signin.html?as=parent&amp;next=' + nextHere() + '#create">Create a parent account</a>' +
        '<a class="btn btn-secondary" href="signin.html?as=parent&amp;next=' + nextHere() + '">Sign in</a></div>' +
        '<p class="fine">Student? Send this page to a parent. Your choices stay in the link.</p>';
    } else if (a.role !== "parent") {
      // A student can pay for their own plan, or send the page to a parent.
      var me = (a.students || [])[0], cur = me && me.subscription;
      state.student = me ? me.id : null;
      var nowLine = cur && cur.plan !== "free" ? "Right now: " + cur.plan_name + (cur.status === "canceled" ? " (canceled)" : "") + ", " + cur.price_label + "."
        : "Right now: the free " + FREE_NAME + " plan.";
      el.innerHTML = '<p class="co-for"><strong>' + esc(a.name) + "</strong> (you)</p><p class=\"fine\">" + esc(nowLine) + " You can manage or cancel it any time in Settings, then Subscription.</p>" +
        '<div class="pd-row"><button class="btn btn-quiet" type="button" id="co-copy">Have a parent pay instead: copy a link</button></div>';
      $("co-copy").addEventListener("click", copyLink);
    } else if (!a.students.length) {
      el.innerHTML = "<p>Connect your student first. They open <strong>Account</strong>, then <strong>Parent access</strong>, on their dashboard and give you a code.</p>" +
        '<div class="field co-link"><label for="co-code">Student\'s code</label><div class="co-link-row"><input id="co-code" data-no-filter autocomplete="off" autocapitalize="characters" spellcheck="false" maxlength="12" aria-describedby="co-code-hint">' +
        '<button class="btn btn-secondary" type="button" id="co-link">Connect</button></div><p class="hint" id="co-code-hint">8 letters and numbers, like K7QM-4ZTR.</p><p class="field-error" id="co-code-error" hidden></p></div>';
      $("co-link").addEventListener("click", link);
      $("co-code").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); link(); } });
    } else {
      if (!a.students.some(function (s) { return s.id === state.student; })) state.student = a.students[0].id;
      var s = a.students.filter(function (x) { return x.id === state.student; })[0], sub = s.subscription;
      var now = sub && sub.plan !== "free" ? "Right now: " + sub.plan_name + (sub.status === "canceled" ? " (canceled)" : "") + ", " + sub.price_label + ". " +
        (sub.plan === state.plan && sub.interval === state.interval ? "That's this exact plan already." : "Checking out switches to " + plan().name + " today" + (info.payments_live ? ", and the time left on the old plan is credited to your account." : ".")) : "Right now: the free " + FREE_NAME + " plan.";
      el.innerHTML = (a.students.length > 1
        ? '<div class="field"><label for="co-student">Student</label><select id="co-student">' + a.students.map(function (x) { return '<option value="' + x.id + '"' + (x.id === state.student ? " selected" : "") + ">" + esc(x.name) + "</option>"; }).join("") + "</select></div>"
        : '<p class="co-for"><strong>' + esc(s.name) + "</strong></p>") + '<p class="fine">' + esc(now) + "</p>";
    }
    payLabel();
  }
  function copyLink() {
    var url = location.href.split("#")[0], done = function () { status("ok", "Link copied.", "Send it to a parent. It opens this page with your plan already picked."); };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(url).then(done, function () { status("ok", "Copy this link:", url); });
    else status("ok", "Copy this link:", url);
  }
  function link() {
    var input = $("co-code"), err = $("co-code-error"), code = input.value.trim();
    err.hidden = true; input.removeAttribute("aria-invalid");
    var bad = function (msg) { err.textContent = msg; err.hidden = false; input.setAttribute("aria-invalid", "true"); input.focus(); };
    if (!/^[A-Za-z0-9]{4}[- ]?[A-Za-z0-9]{4}$/.test(code)) { bad("Codes are 8 letters and numbers, like K7QM-4ZTR."); return; }
    var req = LIVE ? API.call("/api/parent/link", { code: code }) : Preview.link(code);
    req.then(function () { return load(); }).then(function () { status("ok", "Connected.", "Now pick the plan and check out."); })
      .catch(function (e) { bad(e && e.message ? e.message : "That didn't work. Check your connection and try again."); });
  }

  /* ---------- paying ---------- */
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (state.busy || !canPay()) return;
    clearStatus();
    var agree = $("co-agree");
    if (!agree.checked) { status("err", "Check the box to agree first.", "It confirms you know the plan renews automatically until you cancel."); agree.focus(); return; }
    var b = $("co-pay"); state.busy = true; b.disabled = true;
    b.textContent = state.info.payments_live ? "Opening secure payment…" : "Starting…";
    var payload = { plan: state.plan, interval: state.interval, student_id: state.student, agree: true };
    (LIVE ? API.call("/api/checkout", payload) : Preview.buy(payload)).then(function (r) {
      if (r.url) { location.href = r.url; return; }  // Stripe's payment page
      state.busy = false;
      done(r.student.name, r.subscription, false);
    }).catch(function (err) {
      state.busy = false; payLabel();
      if (err && err.status === 401) { location.href = "signin.html?as=parent&next=" + nextHere(); return; }
      status("err", "We couldn't start checkout.", err && err.status ? err.message : "Check your connection and try again. Nothing was charged.");
    });
  });
  function done(name, sub, paid) {
    form.hidden = true;
    $("co-title").textContent = "Thank you";
    $("co-lede").textContent = paid ? "Your payment went through." : "Your plan is ready.";
    $("co-done").hidden = false;
    $("co-done-text").textContent = sub.plan_name + " is on for " + name + ": " + sub.price_label + ". " + (sub.renews_on ? "Renews " + niceDay(new Date(sub.renews_on + "T12:00:00")) + "." : "");
    var where = state.info && state.info.account && state.info.account.role !== "parent" ? "Settings, then Subscription" : "the parent dashboard";
    $("co-done-fine").textContent = paid ? "A receipt is on its way to your email. Manage or cancel the plan anytime from " + where + "."
      : "Payments aren't connected yet, so no card was charged. Manage or cancel the plan anytime from " + where + ".";
    $("co-done-title").focus();
  }

  // Back from Stripe: checkout.html?session_id=cs_... Check the payment, a few times if Stripe is still finishing up.
  function confirm(sid, tries) {
    form.hidden = true;
    $("co-title").textContent = "Checking your payment…"; $("co-lede").textContent = "This takes a few seconds.";
    API.call("/api/checkout/session/" + encodeURIComponent(sid)).then(function (r) {
      if (r.paid) { done(r.student.name, r.subscription, true); return; }
      if (tries < 5 && r.status !== "expired") { setTimeout(function () { confirm(sid, tries + 1); }, 2000); return; }
      $("co-title").textContent = "Payment not finished";
      status("err", "We haven't seen the payment go through.", "If you paid, it can take a minute: refresh this page. Otherwise, go back and try again. Nothing is charged until Stripe confirms.");
    }).catch(function (err) {
      $("co-title").textContent = "Payment check failed";
      status("err", "We couldn't check the payment.", err && err.status ? err.message : "Check your connection and refresh this page.");
    });
  }

  /* ---------- preview (no server): same rules, kept in this browser ---------- */
  var Preview = {
    fam: function () { try { return JSON.parse(localStorage.getItem("graphite_family")) || { parents: [] }; } catch (e) { return { parents: [] }; } },
    save: function (f) { try { localStorage.setItem("graphite_family", JSON.stringify(f)); } catch (e) { /* storage blocked */ } },
    who: function () { try { return { email: sessionStorage.getItem("graphite_user"), role: sessionStorage.getItem("graphite_role") }; } catch (e) { return {}; } },
    info: function () {
      var w = Preview.who(), f = Preview.fam(), account = null;
      if (w.email) {
        account = { name: w.email, role: w.role === "parent" ? "parent" : "student" };
        if (account.role !== "parent") {
          var ms = f.sub && f.sub.plan !== "free" ? f.sub : null, mp = ms && PLANS.filter(function (x) { return x.key === ms.plan; })[0];
          account.students = [{ id: 1, name: w.email, self: true, subscription: mp ? { plan: mp.key, plan_name: mp.name, interval: ms.interval, status: ms.status, price_label: label(mp, ms.interval) } : { plan: "free" } }];
        }
        if (account.role === "parent") {
          var sub = f.sub && f.sub.plan !== "free" ? f.sub : null, p = sub && PLANS.filter(function (x) { return x.key === sub.plan; })[0];
          account.students = f.parents.length || w.email === "beta2" ? [{ id: 1, name: "Maya Rivera", subscription: p ? { plan: p.key, plan_name: p.name, interval: sub.interval, status: sub.status,
            price_label: label(p, sub.interval) } : { plan: "free" } }] : [];
        }
      }
      return Promise.resolve({ plans: PLANS, today: iso(new Date()), payments_live: false, account: account });
    },
    link: function (code) {
      var f = Preview.fam(), mine = f.code && f.code.code.replace("-", "");
      if (!mine || code.toUpperCase().replace(/[^A-Z0-9]/g, "") !== mine) return Promise.reject(new Error("That code didn't work. In this preview, make a code on the student dashboard's Account panel in this browser."));
      f.parents = [{ id: 1, name: "Parent", email: Preview.who().email, since: new Date().toISOString() }]; delete f.code; Preview.save(f);
      return Promise.resolve({});
    },
    buy: function (d) {
      var f = Preview.fam(), p = plan(), renews = iso(renewal(d.interval)), price = p.cents[d.interval];
      f.sub = { plan: d.plan, interval: d.interval, status: "active", renews_on: renews, paused_until: null };
      f.billing = [{ at: new Date().toISOString(), kind: "change", detail: p.name + ", billed " + WORDS[d.interval] + " at " + money(price) + ". Renews " + niceDay(renewal(d.interval)) +
        ". No card was charged: payments aren't connected yet.", amount_cents: price }].concat(f.billing || []).slice(0, 20);
      Preview.save(f);
      return new Promise(function (res) { setTimeout(function () {
        res({ done: true, student: { id: 1, name: "Maya Rivera" }, subscription: { plan: p.key, plan_name: p.name, price_label: label(p, d.interval), renews_on: renews } });
      }, 500); });
    }
  };
  function label(p, iv) { var each = money(p.per_month_cents[iv]) + "/month"; return iv === "month" ? each : each + ", billed " + money(p.cents[iv]) + " " + WORDS[iv]; }

  /* ---------- start ---------- */
  function load() {
    return (LIVE ? API.call("/api/checkout") : Preview.info()).then(function (info) {
      state.info = info;
      if (info.plans) {
        PLANS = info.plans.filter(function (p) { return p.key !== "free"; });
        info.plans.forEach(function (p) { if (p.key === "free") FREE_NAME = p.name; });
      }
      $("co-demo").hidden = !!info.payments_live;
      $("co-secure").hidden = !info.payments_live;
      drawChoices(); drawWho(); drawSummary();
    });
  }
  drawChoices(); drawSummary();
  var sid = q.get("session_id");
  if (sid && LIVE) {
    load().then(function () { confirm(sid, 0); });
  } else {
    load().catch(function () { $("co-who").innerHTML = '<p class="fine">We couldn\'t check your account. Refresh the page to try again.</p>'; });
    if (q.get("canceled")) status("ok", "Checkout canceled. Nothing was charged.", "Your choices are still here if you'd like to try again.");
  }
})();
