"""Admin accounts (ADMIN_ACCOUNTS): the /admin page, instant plan switching and starting over."""
import shutil
import tempfile
import unittest

from app import create_app

ORIGIN = {"Origin": "http://localhost"}


class AdminTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dir, True)
        self.app = create_app({"DATABASE_URL": f"sqlite:///{self.dir}/test.db", "TESTING": True, "PLAN_LIMITS": True,
                               "FORCE_HTTPS": False, "SESSION_COOKIE_SECURE": False, "BASE_URL": "http://localhost",
                               "TEST_ACCOUNT": False, "ADMIN_ACCOUNTS": frozenset({"owner@school.org"})})

    def account(self, email, role="student"):
        c = self.app.test_client()
        data = {"name": "Pat Kim", "email": email, "password": "password123", "role": role}
        if role == "student":
            data["grade"] = 11
        r = c.post("/api/auth/register", json=data, headers=ORIGIN)
        self.assertEqual(r.status_code, 201, r.json)
        return c

    def test_admin_sees_signups_and_accounts(self):
        admin = self.account("Owner@School.org")  # emails match whatever the case
        self.account("sam@school.org")
        self.account("mom@school.org", "parent")
        self.app.test_client().post("/api/leads", json={"name": "Lee Park", "email": "lee@school.org", "grade": 10, "agree": True,
                                                       "message": "Hi"}, headers=ORIGIN)
        self.assertTrue(admin.get("/api/me").json["user"]["admin"])
        d = admin.get("/api/admin").json
        self.assertEqual(d["counts"], {"leads": 1, "students": 2, "parents": 1})
        self.assertEqual(d["leads"][0]["message"], "Hi")
        self.assertEqual({s["email"] for s in d["students"]}, {"owner@school.org", "sam@school.org"})
        self.assertEqual(d["students"][0]["plan_name"], "Sharpened")
        self.assertEqual(admin.get("/admin.html").status_code, 200)

    def test_everyone_else_is_kept_out(self):
        sam = self.account("sam@school.org")
        self.assertFalse(sam.get("/api/me").json["user"]["admin"])
        self.assertEqual(sam.get("/api/admin").status_code, 404)
        self.assertEqual(sam.get("/admin.html").status_code, 404)
        self.assertEqual(sam.post("/api/me/subscription/test", json={"plan": "mechanical"}, headers=ORIGIN).status_code, 403)
        self.assertEqual(sam.post("/api/me/test-reset", json={}, headers=ORIGIN).status_code, 403)
        visitor = self.app.test_client()
        self.assertEqual(visitor.get("/api/admin").status_code, 401)
        self.assertIn("/signin.html", visitor.get("/admin.html").headers["Location"])

    def test_admin_switches_plans_and_starts_over(self):
        admin = self.account("owner@school.org")
        r = admin.post("/api/me/subscription/test", json={"plan": "mechanical"}, headers=ORIGIN)
        self.assertEqual(r.status_code, 200, r.json)
        self.assertEqual(r.json["subscription"]["plan"], "mechanical")
        self.assertTrue(admin.get("/api/me/subscription").json["test_account"])
        admin.post("/api/practice/sessions", json={"mode": "test"}, headers=ORIGIN)
        r = admin.post("/api/me/test-reset", json={}, headers=ORIGIN)
        self.assertEqual(r.status_code, 200, r.json)
        self.assertEqual(admin.get("/api/practice").json["unfinished"], [])
        self.assertEqual(admin.get("/api/me/subscription").json["subscription"]["plan"], "free")
        # The email and password still work after starting over.
        again = self.app.test_client()
        r = again.post("/api/auth/login", json={"email": "owner@school.org", "password": "password123"}, headers=ORIGIN)
        self.assertEqual(r.status_code, 200, r.json)


if __name__ == "__main__":
    unittest.main()
