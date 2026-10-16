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
        cfg = {"DATABASE_URL": f"sqlite:///{self.dir}/test.db", "TESTING": True, "FORCE_HTTPS": False,
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
