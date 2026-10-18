"""Backend tests. Run from the backend folder: python -m unittest discover tests"""
import re
import shutil
import tempfile
import unittest

from app import create_app
from app.services import mailer
from app.services.grading import spr_value
from app.services.planner import build_plan

ORIGIN = {"Origin": "http://localhost"}


class ApiTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.app = create_app({"DATABASE_URL": f"sqlite:///{self.dir}/test.db", "TESTING": True, "PLAN_LIMITS": False, "FORCE_HTTPS": False,
                               "SESSION_COOKIE_SECURE": False, "BASE_URL": "http://localhost"})
        self.client = self.app.test_client()

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    # helpers
    def post(self, url, data=None, **kw):
        return self.client.post(url, json=data or {}, headers=kw.pop("headers", ORIGIN), **kw)

    def register(self, email="sam@school.org", password="password123", **extra):
        data = {"name": "Sam Lee", "email": email, "password": password, "grade": 11, "test_date": "2030-12-07", "target_score": 1450}
        data.update(extra)
        return self.post("/api/auth/register", data)

    # accounts
    def test_register_signs_in_and_hashes_password(self):
        r = self.register()
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json["user"]["first_name"], "Sam")
        self.assertNotIn("password_hash", r.json["user"])
        self.assertEqual(self.client.get("/api/me").status_code, 200)

    def test_duplicate_email_rejected(self):
        self.register()
        r = self.register(email="SAM@school.org")
        self.assertEqual(r.status_code, 409)
        self.assertEqual(r.json["field"], "email")

    def test_validation_messages(self):
        self.assertEqual(self.register(password="short").json["field"], "password")
        self.assertEqual(self.register(email="nope").json["field"], "email")
        self.assertEqual(self.register(target_score=1455).json["field"], "target_score")

    def test_login_logout_and_wrong_password(self):
        self.register()
        self.post("/api/auth/logout")
        self.assertEqual(self.client.get("/api/me").status_code, 401)
        self.assertEqual(self.post("/api/auth/login", {"email": "sam@school.org", "password": "nope-nope"}).status_code, 401)
        self.assertEqual(self.post("/api/auth/login", {"email": "sam@school.org", "password": "password123"}).status_code, 200)

    def test_login_rate_limit(self):
        self.register()
        self.post("/api/auth/logout")
        codes = [self.post("/api/auth/login", {"email": "sam@school.org", "password": "wrong-pass"}).status_code for _ in range(6)]
        self.assertEqual(codes[:5], [401] * 5)
        self.assertEqual(codes[5], 429)

    def test_password_reset_flow(self):
        self.register()
        other = self.app.test_client()
        other.post("/api/auth/login", json={"email": "sam@school.org", "password": "password123"}, headers=ORIGIN)
        self.post("/api/auth/logout")
        mailer.OUTBOX.clear()
        self.assertEqual(self.post("/api/auth/forgot", {"email": "sam@school.org"}).status_code, 200)
        token = re.search(r"reset=([\w-]+)", mailer.OUTBOX[-1]["text"]).group(1)
        self.assertEqual(self.post("/api/auth/reset", {"token": token, "password": "brand-new-pass"}).status_code, 200)
        self.assertEqual(self.post("/api/auth/reset", {"token": token, "password": "another-pass"}).status_code, 400)
        self.assertEqual(other.get("/api/me").status_code, 401, "old sessions end after a reset")

    def test_forgot_does_not_reveal_accounts(self):
        r = self.post("/api/auth/forgot", {"email": "nobody@school.org"})
        self.assertEqual(r.status_code, 200)

    # security
    def test_cross_site_post_blocked(self):
        r = self.client.post("/api/auth/register", json={}, headers={"Origin": "https://evil.example"})
        self.assertEqual(r.status_code, 403)

    def test_form_post_blocked(self):
        r = self.client.post("/api/leads", data={"name": "x"}, headers=ORIGIN)
        self.assertEqual(r.status_code, 415)

    def test_protected_pages_redirect(self):
        r = self.client.get("/dashboard.html")
        self.assertEqual(r.status_code, 302)
        self.assertIn("/signin.html?next=/dashboard.html", r.headers["Location"])
        self.register()
        self.assertEqual(self.client.get("/dashboard.html").status_code, 200)

    def test_path_traversal_blocked(self):
        self.assertEqual(self.client.get("/../backend/app/config.py").status_code, 404)

    def test_security_headers(self):
        r = self.client.get("/")
        self.assertEqual(r.headers["X-Content-Type-Options"], "nosniff")
        self.assertIn("default-src 'self'", r.headers["Content-Security-Policy"])

    # leads
    def test_lead_saved_and_honeypot(self):
        lead = {"name": "Jo", "email": "jo@school.org", "grade": "10", "agree": "on", "test_date": "2027-03"}
        self.assertEqual(self.post("/api/leads", lead).status_code, 201)
        self.assertEqual(self.post("/api/leads", dict(lead, company="spam co")).status_code, 200)
        self.assertEqual(self.post("/api/leads", dict(lead, agree="")).json["field"], "agree")

    # practice tests
    def test_questions_hide_answers(self):
        self.register()
        qs = self.client.get("/api/tests/pt4-math-m1").json["test"]["questions"]
        self.assertEqual(len(qs), 22)
        for q in qs:
            self.assertNotIn("answer", q)
            self.assertNotIn("explain", q)

    def test_grading_and_review_queue(self):
        self.register()
        r = self.post("/api/tests/pt4-math-m1/attempts", {"answers": {"0": 1, "1": "54", "4": "12/2", "10": "7.0", "2": 3}, "seconds_used": 900})
        self.assertEqual(r.status_code, 201)
        result = r.json["result"]
        self.assertEqual(result["correct"], 4)
        self.assertEqual(result["questions"][2]["answer"], "A")
        dash = self.client.get("/api/dashboard").json
        self.assertEqual(len(dash["review"]), 18)
        self.assertEqual(dash["summary"]["latest"]["correct"], 4)
        item = dash["review"][0]["id"]
        self.assertFalse(self.post(f"/api/review/{item}/right").json["cleared"])
        self.assertTrue(self.post(f"/api/review/{item}/right").json["cleared"])
        self.assertEqual(len(self.client.get("/api/dashboard").json["review"]), 17)

    def test_bad_answers_ignored(self):
        self.register()
        r = self.post("/api/tests/pt4-math-m1/attempts", {"answers": {"0": 9, "99": 1, "x": 2, "1": "abc"}, "seconds_used": 99999})
        self.assertEqual(r.json["result"]["correct"], 0)
        self.assertLessEqual(r.json["result"]["seconds_used"], 35 * 60 + 120)

    def test_tests_need_sign_in(self):
        self.assertEqual(self.client.get("/api/tests/pt4-math-m1").status_code, 401)

    def test_update_settings(self):
        self.register()
        r = self.client.patch("/api/me", json={"weekly_goal_hours": 5, "target_score": 1500}, headers=ORIGIN)
        self.assertEqual(r.json["user"]["weekly_goal_hours"], 5)
        bad = self.client.patch("/api/me", json={"weekly_goal_hours": 50}, headers=ORIGIN)
        self.assertEqual(bad.status_code, 400)


class UnitTest(unittest.TestCase):
    def test_spr_values(self):
        self.assertEqual(spr_value("7/2"), 3.5)
        self.assertEqual(spr_value("-.5"), -0.5)
        self.assertIsNone(spr_value("1/0"))
        self.assertIsNone(spr_value("2x"))

    def test_plan_ends_on_test_week(self):
        from datetime import date
        plan = build_plan("2026-12-05", {"Algebra": 40}, today=date(2026, 10, 15))
        self.assertEqual(plan["weeks"][0]["week_of"], "2026-10-12")
        self.assertTrue(plan["weeks"][-1]["focus"].startswith("Test week"))
        self.assertEqual(plan["weeks"][0]["focus"], "Algebra")


if __name__ == "__main__":
    unittest.main()
