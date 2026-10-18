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

    def buy(self, plan="sharpened", interval="year", **extra):
        return self.post(self.parent, "/api/checkout", {"plan": plan, "interval": interval, "student_id": self.student_id, "agree": True, **extra})

    def sub(self):
        return self.parent.get(f"/api/parent/students/{self.student_id}").json["subscription"]


class WithoutStripe(CheckoutTest):
    def test_visitors_see_plans_and_who_is_signed_in(self):
        r = self.app.test_client().get("/api/checkout").json
        self.assertIsNone(r["account"])
        self.assertFalse(r["payments_live"])
        self.assertEqual([p["key"] for p in r["plans"]], ["free", "no2", "sharpened", "masterstroke"])
        acct = self.parent.get("/api/checkout").json["account"]
        self.assertEqual((acct["role"], acct["students"][0]["name"]), ("parent", "Maya Rivera"))
        self.assertEqual(self.student.get("/api/checkout").json["account"]["role"], "student")

    def test_checks_before_buying(self):
        # A student can buy a plan for themselves, but not for another student.
        self.assertEqual(self.post(self.student, "/api/checkout", {"plan": "sharpened", "interval": "year", "student_id": self.student_id + 999, "agree": True}).status_code, 404)
        self.assertEqual(self.buy(agree=False).status_code, 400)
        self.assertEqual(self.buy(plan="free").status_code, 400)
        self.assertEqual(self.buy(interval="decade").status_code, 400)
        self.assertEqual(self.buy(student_id=99999).status_code, 404)
        self.assertEqual(self.app.test_client().post("/api/checkout", json={}, headers=ORIGIN).status_code, 401)

    def test_starts_the_plan_without_charging(self):
        r = self.buy("no2", "week")
        self.assertEqual(r.status_code, 201, r.json)
        self.assertTrue(r.json["done"])
        self.assertEqual(r.json["subscription"]["price_label"], "$21.62/month, billed $4.99 weekly")
        self.assertEqual(self.fake.calls, [], "Stripe isn't called until it's connected")
        hist = self.parent.get(f"/api/parent/students/{self.student_id}").json["billing"]
        self.assertIn("No card was charged", hist[0]["detail"])

    def test_switching_to_free_waits_for_the_paid_time_to_run_out(self):
        self.buy("sharpened", "month")
        url = f"/api/parent/students/{self.student_id}/plan"
        r = self.post(self.parent, url, {"plan": "free"}).json
        self.assertEqual((r["subscription"]["plan"], r["subscription"]["status"]), ("sharpened", "canceled"))
        again = self.post(self.parent, url, {"plan": "free"})  # pressing twice changes nothing
        self.assertEqual(again.status_code, 200)
        self.assertEqual(len([b for b in again.json["billing"] if b["kind"] == "cancel"]), 1)


class WithStripe(CheckoutTest):
    live = True

    def test_sends_the_parent_to_stripe_then_starts_the_plan(self):
        r = self.buy("sharpened", "year")
        self.assertEqual(r.status_code, 200, r.json)
        self.assertTrue(r.json["url"].startswith("https://checkout.stripe.com/"))
        made = [c for c in self.fake.calls if c[:2] == ("POST", "/prices")][0][2]
        self.assertEqual((made["unit_amount"], made["recurring"]["interval"]), (34800, "year"))
        params = [c for c in self.fake.calls if c[1] == "/checkout/sessions"][0][2]
        self.assertEqual(params["customer_email"], "ana@home.org")
        self.assertTrue(params["allow_promotion_codes"])
        self.assertEqual(self.sub()["plan"], "free", "nothing starts before the payment")
        # The same price is reused for the next checkout.
        self.buy("sharpened", "year")
        self.assertEqual(len([c for c in self.fake.calls if c[:2] == ("POST", "/prices")]), 1)

        self.fake.pay("cs_test_1", 34800)
        r = self.parent.get("/api/checkout/session/cs_test_1").json
        self.assertTrue(r["paid"])
        self.assertEqual((r["subscription"]["plan"], r["student"]["name"]), ("sharpened", "Maya Rivera"))
        self.parent.get("/api/checkout/session/cs_test_1")  # a refresh doesn't start it twice
        hist = self.parent.get(f"/api/parent/students/{self.student_id}").json["billing"]
        self.assertEqual(len(hist), 1)
        self.assertIn("Paid $348", hist[0]["detail"])
        self.assertNotIn("No card", hist[0]["detail"])
        # Someone else can't read this checkout.
        other = self.app.test_client()
        self.post(other, "/api/auth/register", {"name": "Sam Lee", "email": "sam@home.org", "password": "password123", "role": "parent"})
        self.assertEqual(other.get("/api/checkout/session/cs_test_1").status_code, 404)

    def test_dashboard_changes_go_to_stripe(self):
        self.buy("no2", "month"); self.fake.pay("cs_test_1", 1900)
        self.parent.get("/api/checkout/session/cs_test_1")
        url = f"/api/parent/students/{self.student_id}/plan"
        self.assertEqual(self.post(self.parent, url, {"plan": "sharpened", "interval": "month"}).json["code"], "checkout_required")
        self.post(self.parent, url + "/cancel")
        self.assertEqual(self.fake.calls[-1][1:], ("/subscriptions/sub_1", {"cancel_at_period_end": True}))
        self.post(self.parent, url + "/resume")
        self.assertEqual(self.fake.calls[-1][2]["cancel_at_period_end"], False)
        self.post(self.parent, url + "/pause")
        self.assertEqual(self.fake.calls[-1][2]["pause_collection"]["behavior"], "void")
        self.assertTrue(self.post(self.parent, "/api/parent/billing-portal").json["url"].startswith("https://billing.stripe.com/"))
        # Buying a different plan ends the old subscription.
        self.post(self.parent, url + "/resume")
        self.buy("masterstroke", "year"); self.fake.pay("cs_test_2", 118800)
        self.parent.get("/api/checkout/session/cs_test_2")
        self.assertIn(("DELETE", "/subscriptions/sub_1"), [c[:2] for c in self.fake.calls])
        self.assertEqual(self.sub()["plan"], "masterstroke")

    def webhook(self, event, secret="whsec_fake"):
        payload = json.dumps(event).encode()
        return self.app.test_client().post("/api/stripe/webhook", data=payload, content_type="application/json",
                                           headers={"Stripe-Signature": stripe_api.sign_for_tests(payload, secret)})

    def test_webhook(self):
        self.buy("sharpened", "month")
        meta = {"student_id": str(self.student_id), "plan": "sharpened", "interval": "month", "payer_id": "2"}
        done = {"id": "evt_1", "type": "checkout.session.completed", "data": {"object": {
            "mode": "subscription", "payment_status": "paid", "metadata": meta, "customer": "cus_9", "amount_total": 3900,
            "subscription": {"id": "sub_9", "current_period_end": int(time.time()) + 30 * 86400}}}}
        self.assertEqual(self.webhook(done, secret="whsec_wrong").status_code, 400, "unsigned events are refused")
        self.assertEqual(self.webhook(done).status_code, 200)
        self.assertEqual(self.webhook(done).status_code, 200)  # Stripe retries; it's handled once
        self.assertEqual(self.sub()["plan"], "sharpened")
        self.assertEqual(len(self.parent.get(f"/api/parent/students/{self.student_id}").json["billing"]), 1)
        self.webhook({"id": "evt_2", "type": "customer.subscription.updated", "data": {"object": {
            "id": "sub_9", "status": "active", "cancel_at_period_end": True, "current_period_end": int(time.time()) + 30 * 86400}}})
        self.assertEqual(self.sub()["status"], "canceled")
        self.webhook({"id": "evt_3", "type": "customer.subscription.deleted", "data": {"object": {"id": "sub_9", "status": "canceled"}}})
        self.assertEqual((self.sub()["plan"], self.sub()["status"]), ("free", "active"))

    def test_old_signatures_are_refused(self):
        payload = b'{"id": "evt_x"}'
        old = stripe_api.sign_for_tests(payload, "whsec_fake", stamp=int(time.time()) - 3600)
        with self.assertRaises(stripe_api.StripeError):
            stripe_api.verify_webhook(payload, old, "whsec_fake")


if __name__ == "__main__":
    unittest.main()
