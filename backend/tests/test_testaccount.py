"""The local test account (beta / beta)."""
import shutil
import tempfile
import unittest

from app import create_app
from app.config import Config

ORIGIN = {"Origin": "http://localhost"}


class TestAccountTest(unittest.TestCase):
    def make(self, **extra):
        self.dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dir, True)
        cfg = {"DATABASE_URL": f"sqlite:///{self.dir}/test.db", "TESTING": True, "PLAN_LIMITS": False, "FORCE_HTTPS": False,
               "SESSION_COOKIE_SECURE": False, "BASE_URL": "http://localhost"}
        cfg.update(extra)
        return create_app(cfg).test_client()

    def login(self, client, email="beta", password="beta"):
        return client.post("/api/auth/login", json={"email": email, "password": password}, headers=ORIGIN)

    def test_beta_signs_in_locally(self):
        client = self.make()
        r = self.login(client)
        self.assertEqual(r.status_code, 200, r.json)
        self.assertEqual(r.json["user"]["name"], "Beta Tester")
        self.assertEqual(client.get("/api/me").status_code, 200)
        self.assertEqual(self.login(self.make(), password="wrong").status_code, 401)

    def test_progress_is_saved_and_reset_starts_over(self):
        client = self.make()
        self.login(client)
        self.assertTrue(client.get("/api/dashboard").json["start_with_diagnostic"])
        d = client.post("/api/plan/diagnostic", json={"test_date": "2030-12-07"}, headers=ORIGIN).json["diagnostic"]
        client.post(f"/api/plan/diagnostic/{d['id']}/submit", json={"answers": {}, "sure": {}}, headers=ORIGIN)
        client.post("/api/practice/sessions", json={"mode": "test"}, headers=ORIGIN)
        self.assertIsNotNone(client.get("/api/plan").json["plan"])
        self.login(client)  # signing in again keeps everything
        self.assertIsNotNone(client.get("/api/plan").json["plan"])
        coins = client.get("/api/game/summary").json["coins"]
        self.assertEqual(coins, 100_000)
        r = client.post("/api/me/test-reset", json={}, headers=ORIGIN)  # Settings > Your data
        self.assertEqual(r.status_code, 200, r.json)
        self.assertIsNone(client.get("/api/plan").json["plan"])
        self.assertIsNone(client.get("/api/plan").json["diagnostic"])
        self.assertEqual(client.get("/api/practice").json["unfinished"], [])
        self.assertIsNone(client.get("/api/me").json["user"]["test_date"])
        self.assertEqual(client.get("/api/game/summary").json["coins"], 100_000)

    def test_off_when_disabled(self):
        self.assertEqual(self.login(self.make(TEST_ACCOUNT=False)).status_code, 400)

    def test_never_on_in_production(self):
        self.assertFalse(Config.TEST_ACCOUNT and Config.IS_PRODUCTION)

    def test_cannot_register_the_username(self):
        client = self.make()
        r = client.post("/api/auth/register", json={"name": "X", "email": "beta", "password": "password123"}, headers=ORIGIN)
        self.assertEqual(r.status_code, 400)


if __name__ == "__main__":
    unittest.main()
