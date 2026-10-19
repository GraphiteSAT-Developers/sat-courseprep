"""The checkout page and Stripe. Run from the backend folder: python -m unittest discover tests

Stripe itself is never called: FakeStripe stands in for stripe_api.request and answers like Stripe does.
"""
import json
import shutil
import tempfile
import time
import unittest

from app import create_app
from app.services import billing, stripe_api

ORIGIN = {"Origin": "http://localhost"}


class FakeStripe:
    def __init__(self):
        self.calls, self.sessions, self.prices = [], {}, {}

    def __call__(self, method, path, data=None):
        self.calls.append((method, path, data))
        if path == "/prices" and method == "GET":
            key = data["lookup_keys"][0]
            return {"data": [{"id": self.prices[key]}] if key in self.prices else []}
        if path == "/prices":
            self.prices[data["lookup_key"]] = f"price_{len(self.prices) + 1}"
            return {"id": self.prices[data["lookup_key"]]}
        if path == "/checkout/sessions":
            sid = f"cs_test_{len(self.sessions) + 1}"
            self.sessions[sid] = {"id": sid, "url": f"https://checkout.stripe.com/c/pay/{sid}", "metadata": data["metadata"],
                                  "status": "open", "payment_status": "unpaid", "customer": None, "subscription": None,
                                  "amount_total": None, "mode": "subscription"}
            return self.sessions[sid]
        if path.startswith("/checkout/sessions/"):
            return self.sessions[path.rsplit("/", 1)[1]]
        if path.startswith("/billing_portal/sessions"):
            return {"url": "https://billing.stripe.com/p/session/test"}
        return {"id": path.rsplit("/", 1)[1], "status": "active"}

    def pay(self, sid, amount):
        """What happens when the parent pays on Stripe's page."""
        n = sid.rsplit("_", 1)[1]
        self.sessions[sid].update(status="complete", payment_status="paid", customer="cus_test", amount_total=amount,
                                  subscription={"id": f"sub_{n}", "current_period_end": int(time.time()) + 365 * 86400})


class CheckoutTest(unittest.TestCase):
    live = False

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        cfg = {"DATABASE_URL": f"sqlite:///{self.dir}/test.db", "TESTING": True, "PLAN_LIMITS": False, "FORCE_HTTPS": False,
               "SESSION_COOKIE_SECURE": False, "BASE_URL": "http://localhost"}
        if self.live:
            cfg.update(STRIPE_SECRET_KEY="sk_test_fake", STRIPE_WEBHOOK_SECRET="whsec_fake")
        self.app = create_app(cfg)
        self.fake = FakeStripe()
        self._real = stripe_api.request
        stripe_api.request = self.fake
        billing._price_ids.clear()
        self.student, self.parent = self.app.test_client(), self.app.test_client()
        r = self.post(self.student, "/api/auth/register", {"name": "Maya Rivera", "email": "maya@school.org", "password": "password123", "grade": 11})
        self.student_id = r.json["user"]["id"]
        self.post(self.parent, "/api/auth/register", {"name": "Ana Rivera", "email": "ana@home.org", "password": "password123", "role": "parent"})
        code = self.post(self.student, "/api/family/code").json["code"]
        self.assertEqual(self.post(self.parent, "/api/parent/link", {"code": code}).status_code, 201)

    def tearDown(self):
        stripe_api.request = self._real
        shutil.rmtree(self.dir, ignore_errors=True)

    def post(self, client, url, data=None):
        return client.post(url, json=data or {}, headers=ORIGIN)

    def buy(self, plan="mechanical", interval="year", **extra):
        return self.post(self.parent, "/api/checkout", {"plan": plan, "interval": interval, "student_id": self.student_id, "agree": True, **extra})

    def sub(self):
        return self.parent.get(f"/api/parent/students/{self.student_id}").json["subscription"]


class WithoutStripe(CheckoutTest):
    def test_visitors_see_plans_and_who_is_signed_in(self):
        r = self.app.test_client().get("/api/checkout").json
        self.assertIsNone(r["account"])
        self.assertFalse(r["payments_live"])
        self.assertEqual([p["key"] for p in r["plans"]], ["free", "mechanical"])
        acct = self.parent.get("/api/checkout").json["account"]
        self.assertEqual((acct["role"], acct["students"][0]["name"]), ("parent", "Maya Rivera"))
        self.assertEqual(self.student.get("/api/checkout").json["account"]["role"], "student")

    def test_checks_before_buying(self):
        # A student can buy a plan for themselves, but not for another student.
        self.assertEqual(self.post(self.student, "/api/checkout", {"plan": "mechanical", "interval": "year", "student_id": self.student_id + 999, "agree": True}).status_code, 404)
        self.assertEqual(self.buy(agree=False).status_code, 400)
        self.assertEqual(self.buy(plan="free").status_code, 400)
        for old in ("no2", "sharpened", "masterstroke", "daily"):  # older plans can't be bought any more
            self.assertEqual(self.buy(plan=old).status_code, 400)
        self.assertEqual(self.buy(interval="decade").status_code, 400)
        self.assertEqual(self.buy(student_id=99999).status_code, 404)
        self.assertEqual(self.app.test_client().post("/api/checkout", json={}, headers=ORIGIN).status_code, 401)

    def test_starts_the_plan_without_charging(self):
        r = self.buy("mechanical", "week")
        self.assertEqual(r.status_code, 201, r.json)
        self.assertTrue(r.json["done"])
        self.assertEqual(r.json["subscription"]["price_label"], "$8.62/month, billed $1.99 weekly")
        self.assertEqual(self.fake.calls, [], "Stripe isn't called until it's connected")
        hist = self.parent.get(f"/api/parent/students/{self.student_id}").json["billing"]
        self.assertIn("No card was charged", hist[0]["detail"])

    def test_live_site_never_starts_paid_plans_without_payments(self):
        # Locally, plans start without a charge. On the live site that would give paid plans away.
        self.app.config["IS_PRODUCTION"] = True
        self.assertEqual(self.buy("mechanical", "year").json["code"], "payments_off")
        self.assertEqual(self.post(self.student, "/api/me/subscription/plan", {"plan": "mechanical", "interval": "month", "agree": True}).status_code, 503)
        self.assertEqual(self.post(self.parent, f"/api/parent/students/{self.student_id}/plan", {"plan": "mechanical", "interval": "week"}).status_code, 503)
        self.assertEqual(self.sub()["plan"], "free")

    def test_switching_to_free_without_payments_is_immediate(self):
        # Payments aren't connected, so nothing was charged and there's no paid time to wait out.
        self.buy("mechanical", "month")
        url = f"/api/parent/students/{self.student_id}/plan"
        r = self.post(self.parent, url, {"plan": "free"}).json
        self.assertEqual((r["subscription"]["plan"], r["subscription"]["status"]), ("free", "active"))
        again = self.post(self.parent, url, {"plan": "free"})  # pressing twice changes nothing
        self.assertEqual(again.status_code, 200)
        self.assertEqual(len([b for b in again.json["billing"] if "free" in b["detail"].lower() and b["kind"] == "change"]), 1)
        # Canceling a paid plan still keeps it to the end of the period.
        self.buy("mechanical", "month")
        r = self.post(self.parent, url + "/cancel").json
        self.assertEqual((r["subscription"]["plan"], r["subscription"]["status"]), ("mechanical", "canceled"))


class WithStripe(CheckoutTest):
    live = True

    def test_sends_the_parent_to_stripe_then_starts_the_plan(self):
        r = self.buy("mechanical", "year")
        self.assertEqual(r.status_code, 200, r.json)
        self.assertTrue(r.json["url"].startswith("https://checkout.stripe.com/"))
        made = [c for c in self.fake.calls if c[:2] == ("POST", "/prices")][0][2]
        self.assertEqual((made["unit_amount"], made["recurring"]["interval"]), (7200, "year"))
        self.assertEqual((made["lookup_key"], made["product_data"]["name"]), ("graphite_mechanical_year_7200", "Graphite SAT Mechanical"))
        params = [c for c in self.fake.calls if c[1] == "/checkout/sessions"][0][2]
        self.assertEqual(params["customer_email"], "ana@home.org")
        self.assertTrue(params["allow_promotion_codes"])
        self.assertEqual(self.sub()["plan"], "free", "nothing starts before the payment")
        # The same price is reused for the next checkout.
        self.buy("mechanical", "year")
        self.assertEqual(len([c for c in self.fake.calls if c[:2] == ("POST", "/prices")]), 1)

        self.fake.pay("cs_test_1", 7200)
        r = self.parent.get("/api/checkout/session/cs_test_1").json
        self.assertTrue(r["paid"])
        self.assertEqual((r["subscription"]["plan"], r["student"]["name"]), ("mechanical", "Maya Rivera"))
        self.assertEqual(r["subscription"]["price_label"], "$6/month, billed $72 yearly")
        self.parent.get("/api/checkout/session/cs_test_1")  # a refresh doesn't start it twice
        hist = self.parent.get(f"/api/parent/students/{self.student_id}").json["billing"]
        self.assertEqual(len(hist), 1)
        self.assertIn("Mechanical, billed yearly. Paid $72.", hist[0]["detail"])
        self.assertNotIn("No card", hist[0]["detail"])
        # Someone else can't read this checkout.
        other = self.app.test_client()
        self.post(other, "/api/auth/register", {"name": "Sam Lee", "email": "sam@home.org", "password": "password123", "role": "parent"})
        self.assertEqual(other.get("/api/checkout/session/cs_test_1").status_code, 404)

    def test_dashboard_changes_go_to_stripe(self):
        self.buy("mechanical", "month"); self.fake.pay("cs_test_1", 800)
        self.parent.get("/api/checkout/session/cs_test_1")
        url = f"/api/parent/students/{self.student_id}/plan"
        self.assertEqual(self.post(self.parent, url, {"plan": "mechanical", "interval": "year"}).json["code"], "checkout_required")
        self.post(self.parent, url + "/cancel")
        self.assertEqual(self.fake.calls[-1][1:], ("/subscriptions/sub_1", {"cancel_at_period_end": True}))
        self.post(self.parent, url + "/resume")
        self.assertEqual(self.fake.calls[-1][2]["cancel_at_period_end"], False)
        self.post(self.parent, url + "/pause")
        self.assertEqual(self.fake.calls[-1][2]["pause_collection"]["behavior"], "void")
        self.assertTrue(self.post(self.parent, "/api/parent/billing-portal").json["url"].startswith("https://billing.stripe.com/"))
        # Switching how it's billed ends the old subscription.
        self.post(self.parent, url + "/resume")
        self.buy("mechanical", "year"); self.fake.pay("cs_test_2", 7200)
        self.parent.get("/api/checkout/session/cs_test_2")
        self.assertIn(("DELETE", "/subscriptions/sub_1"), [c[:2] for c in self.fake.calls])
        self.assertEqual((self.sub()["plan"], self.sub()["interval"]), ("mechanical", "year"))

    def webhook(self, event, secret="whsec_fake"):
        payload = json.dumps(event).encode()
        return self.app.test_client().post("/api/stripe/webhook", data=payload, content_type="application/json",
                                           headers={"Stripe-Signature": stripe_api.sign_for_tests(payload, secret)})

    def test_webhook(self):
        self.buy("mechanical", "month")
        meta = {"student_id": str(self.student_id), "plan": "mechanical", "interval": "month", "payer_id": "2"}
        done = {"id": "evt_1", "type": "checkout.session.completed", "data": {"object": {
            "mode": "subscription", "payment_status": "paid", "metadata": meta, "customer": "cus_9", "amount_total": 800,
            "subscription": {"id": "sub_9", "current_period_end": int(time.time()) + 30 * 86400}}}}
        self.assertEqual(self.webhook(done, secret="whsec_wrong").status_code, 400, "unsigned events are refused")
        self.assertEqual(self.webhook(done).status_code, 200)
        self.assertEqual(self.webhook(done).status_code, 200)  # Stripe retries; it's handled once
        self.assertEqual(self.sub()["plan"], "mechanical")
        self.assertEqual(len(self.parent.get(f"/api/parent/students/{self.student_id}").json["billing"]), 1)
        self.webhook({"id": "evt_2", "type": "customer.subscription.updated", "data": {"object": {
            "id": "sub_9", "status": "active", "cancel_at_period_end": True, "current_period_end": int(time.time()) + 30 * 86400}}})
        self.assertEqual(self.sub()["status"], "canceled")
        self.webhook({"id": "evt_3", "type": "customer.subscription.deleted", "data": {"object": {"id": "sub_9", "status": "canceled"}}})
        self.assertEqual((self.sub()["plan"], self.sub()["status"]), ("free", "active"))

    def paid_earlier(self, plan, interval, cents, sub_id="sub_9"):
        """A checkout for one of the October 2026 plans, finished through the webhook: the student is still billed that price."""
        meta = {"student_id": str(self.student_id), "plan": plan, "interval": interval, "payer_id": "2"}
        self.assertEqual(self.webhook({"id": f"evt_{sub_id}", "type": "checkout.session.completed", "data": {"object": {
            "mode": "subscription", "payment_status": "paid", "metadata": meta, "customer": "cus_9", "amount_total": cents,
            "subscription": {"id": sub_id, "current_period_end": int(time.time()) + 300 * 86400}}}}).status_code, 200)

    def test_older_plan_keeps_its_price_until_the_switch(self):
        self.paid_earlier("sharpened", "year", 34800)
        sub = self.sub()
        self.assertEqual((sub["plan"], sub["plan_name"], sub["legacy"]), ("mechanical", "Mechanical", True))
        self.assertEqual((sub["price_cents"], sub["price_label"]), (34800, "$29/month, billed $348 yearly (earlier price)"))
        hist = self.parent.get(f"/api/parent/students/{self.student_id}").json["billing"]
        self.assertIn("Mechanical, billed yearly. Paid $348.", hist[0]["detail"])
        # Everything Mechanical includes is open.
        self.app.config["PLAN_LIMITS"] = True
        acc = self.student.get("/api/me/subscription").json["access"]
        self.assertTrue(all(f["ok"] for f in acc["features"].values()), acc)
        # Checking out Mechanical moves them to today's price, and ends the old subscription.
        self.buy("mechanical", "year"); self.fake.pay("cs_test_1", 7200)
        self.parent.get("/api/checkout/session/cs_test_1")
        self.assertIn(("DELETE", "/subscriptions/sub_9"), [c[:2] for c in self.fake.calls])
        sub = self.sub()
        self.assertEqual((sub["price_label"], sub["legacy"]), ("$6/month, billed $72 yearly", False))

    def test_moving_a_subscription_to_another_price_in_stripe(self):
        self.paid_earlier("no2", "month", 1900)
        self.assertEqual((self.sub()["price_label"], self.sub()["legacy"]), ("$19/month (earlier price)", True))
        def moved(evt, price):
            self.webhook({"id": evt, "type": "customer.subscription.updated", "data": {"object": {
                "id": "sub_9", "status": "active", "current_period_end": int(time.time()) + 30 * 86400,
                "items": {"data": [{"price": price}]}}}})
        # Moved in Stripe to the Mechanical price this site made (its metadata names the plan).
        moved("evt_m1", {"id": "price_1", "metadata": {"plan": "mechanical", "interval": "month"}, "recurring": {"interval": "month"}})
        self.assertEqual((self.sub()["plan"], self.sub()["price_label"], self.sub()["legacy"]), ("mechanical", "$8/month", False))
        # A price with only our lookup key works too.
        moved("evt_m2", {"id": "price_2", "lookup_key": "graphite_mechanical_year_7200", "recurring": {"interval": "year"}})
        self.assertEqual((self.sub()["interval"], self.sub()["price_label"]), ("year", "$6/month, billed $72 yearly"))
        # A price that isn't one of ours changes nothing.
        moved("evt_m3", {"id": "price_x", "lookup_key": "someone_else", "recurring": {"interval": "week"}})
        self.assertEqual((self.sub()["interval"], self.sub()["price_label"]), ("year", "$6/month, billed $72 yearly"))

    def test_old_signatures_are_refused(self):
        payload = b'{"id": "evt_x"}'
        old = stripe_api.sign_for_tests(payload, "whsec_fake", stamp=int(time.time()) - 3600)
        with self.assertRaises(stripe_api.StripeError):
            stripe_api.verify_webhook(payload, old, "whsec_fake")


if __name__ == "__main__":
    unittest.main()
