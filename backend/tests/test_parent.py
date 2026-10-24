"""Parent accounts and the parent dashboard. Run from the backend folder: python -m unittest discover tests"""
import shutil
import tempfile
import unittest
from datetime import date, timedelta

from app import create_app
from app.db import execute
from app.services import bank, mailer, parent as parent_svc

from test_practice import right_answer

ORIGIN = {"Origin": "http://localhost"}


class ParentTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.app = create_app({"DATABASE_URL": f"sqlite:///{self.dir}/test.db", "TESTING": True, "PLAN_LIMITS": False, "FORCE_HTTPS": False,
                               "SESSION_COOKIE_SECURE": False, "BASE_URL": "http://localhost"})
        self.student = self.app.test_client()
        self.parent = self.app.test_client()
        r = self.post(self.student, "/api/auth/register", {"name": "Maya Rivera", "email": "maya@school.org", "password": "password123",
                                                            "grade": 11, "test_date": (date.today() + timedelta(days=60)).isoformat()})
        self.student_id = r.json["user"]["id"]
        r = self.post(self.parent, "/api/auth/register", {"name": "Ana Rivera", "email": "ana@home.org", "password": "password123", "role": "parent"})
        self.assertEqual(r.status_code, 201, r.json)
        self.assertEqual(r.json["user"]["role"], "parent")

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def post(self, client, url, data=None):
        return client.post(url, json=data or {}, headers=ORIGIN)

    def code(self):
        r = self.post(self.student, "/api/family/code")
        self.assertEqual(r.status_code, 201, r.json)
        return r.json["code"]

    def link(self):
        r = self.post(self.parent, "/api/parent/link", {"code": self.code()})
        self.assertEqual(r.status_code, 201, r.json)
        return f"/api/parent/students/{self.student_id}"

    def test_parent_sign_up_needs_only_name_email_password(self):
        self.assertIsNone(self.parent.get("/api/me").json["user"]["grade"])
        self.assertEqual(self.parent.get("/api/parent").json["students"], [])
        self.assertIn("Parent access", mailer.OUTBOX[-1]["text"])

    def test_link_with_a_code_from_the_student(self):
        code = self.code()
        self.assertRegex(code, r"^[A-Z2-9]{4}-[A-Z2-9]{4}$")
        self.assertEqual(self.post(self.parent, "/api/parent/link", {"code": "nope"}).status_code, 400)
        r = self.post(self.parent, "/api/parent/link", {"code": code.lower().replace("-", " ")})  # forgiving about case and spacing
        self.assertEqual(r.status_code, 201, r.json)
        self.assertEqual(self.parent.get("/api/parent").json["students"], [{"id": self.student_id, "name": "Maya Rivera"}])
        self.assertEqual([p["name"] for p in self.student.get("/api/family").json["parents"]], ["Ana Rivera"])
        # A code works once.
        other = self.app.test_client()
        self.post(other, "/api/auth/register", {"name": "Lee", "email": "lee@home.org", "password": "password123", "role": "parent"})
        self.assertEqual(self.post(other, "/api/parent/link", {"code": code}).status_code, 400)

    def test_new_code_cancels_old_and_codes_expire(self):
        old = self.code()
        new = self.code()
        self.assertEqual(self.post(self.parent, "/api/parent/link", {"code": old}).status_code, 400)
        with self.app.app_context():
            execute("UPDATE link_codes SET expires_at = '2000-01-01T00:00:00Z'")
        self.assertEqual(self.post(self.parent, "/api/parent/link", {"code": new}).status_code, 400)

    def test_privacy_and_roles(self):
        url = f"/api/parent/students/{self.student_id}"
        self.assertEqual(self.parent.get(url).status_code, 404)  # not linked yet
        self.link()
        self.assertEqual(self.parent.get(url).status_code, 200)
        # Parents can't use student endpoints, and students can't use the parent dashboard.
        self.assertEqual(self.parent.get("/api/dashboard").status_code, 403)
        self.assertEqual(self.post(self.parent, "/api/practice/sessions", {"mode": "test"}).status_code, 403)
        self.assertEqual(self.student.get("/api/parent").status_code, 403)
        # Pages for the other kind of account offer to sign in as that kind, instead of bouncing back.
        self.assertTrue(self.student.get("/parent.html").headers["Location"].endswith("/signin.html?as=parent&next=/parent.html"))
        self.assertTrue(self.parent.get("/dashboard.html").headers["Location"].endswith("/signin.html?as=student&next=/dashboard.html"))
        self.assertTrue(self.parent.get("/signin.html").headers["Location"].endswith("/parent.html"))
        self.assertEqual(self.student.get("/signin.html?as=parent").status_code, 200)  # signed in as a student, can still sign in as a parent
        # The student can remove the parent.
        parent_id = self.student.get("/api/family").json["parents"][0]["id"]
        self.assertEqual(self.student.delete(f"/api/family/parents/{parent_id}", json={}, headers=ORIGIN).status_code, 200)
        self.assertEqual(self.parent.get(url).status_code, 404)

    def test_logo_goes_to_each_accounts_dashboard(self):
        # /home is where the logo links: each account's own dashboard, the home page when signed out. Nobody gets signed out.
        self.assertTrue(self.student.get("/home").headers["Location"].endswith("/dashboard.html"))
        self.assertTrue(self.parent.get("/home").headers["Location"].endswith("/parent.html"))
        self.assertEqual(self.app.test_client().get("/home").headers["Location"], "/")
        self.assertEqual(self.student.get("/api/me").status_code, 200)
        self.assertEqual(self.parent.get("/api/me").status_code, 200)

    def test_summary_tracks_progress(self):
        url = self.link()
        s = self.parent.get(url).json
        self.assertEqual(s["student"]["first_name"], "Maya")
        self.assertIsNone(s["overview"]["last_active"])
        self.assertIn("hasn't started practicing", s["alerts"][0]["text"])
        # The student practices: a 5-question topic set, all right.
        items = bank.all_items()
        sess = self.post(self.student, "/api/practice/sessions", {"mode": "topic", "domain": "algebra", "count": 5}).json["session"]
        answers = {str(i): right_answer(items[q["id"]]) for i, q in enumerate(sess["questions"])}
        self.post(self.student, f"/api/practice/sessions/{sess['id']}/submit", {"answers": answers, "seconds_used": 600})
        s = self.parent.get(url).json
        o = s["overview"]
        self.assertIsNotNone(o["last_active"])
        self.assertEqual(o["streak_days"], 1)
        self.assertEqual(o["questions_week"], 5)
        self.assertEqual(o["accuracy_week"], 100)
        self.assertEqual(o["minutes_week"], 10)
        self.assertEqual(s["activity"][0]["kind"], "Topic practice")
        self.assertEqual((s["activity"][0]["correct"], s["activity"][0]["total"]), (5, 5))
        self.assertEqual(len(s["levels"]), 10)  # five Math tracks and five Reading and Writing tracks
        self.assertFalse(any("hasn't" in a["text"] for a in s["alerts"]))

    def test_settings(self):
        url = self.link()
        r = self.parent.patch(url + "/settings", json={"weekly_goal_hours": 6, "target_score": 1400, "weekly_report": False, "alert_days": 5},
                              headers=ORIGIN)
        self.assertEqual(r.status_code, 200, r.json)
        self.assertEqual(r.json["student"]["weekly_goal_hours"], 6)
        self.assertEqual(r.json["settings"], {"weekly_report": False, "alert_days": 5})
        self.assertEqual(self.student.get("/api/me").json["user"]["weekly_goal_hours"], 6)  # the student sees the new goal
        self.assertEqual(self.parent.patch(url + "/settings", json={"weekly_goal_hours": 40}, headers=ORIGIN).status_code, 400)
        self.assertEqual(self.parent.patch(url + "/settings", json={"alert_days": 4}, headers=ORIGIN).status_code, 400)

    def test_plans_and_billing(self):
        url = self.link()
        self.assertEqual(self.parent.get(url).json["subscription"]["plan"], "free")
        self.assertEqual(self.post(self.parent, url + "/plan", {"plan": "mechanical"}).status_code, 400)  # needs a billing option
        for old in ("daily", "no2", "sharpened", "masterstroke"):  # older plans can't be bought any more
            self.assertEqual(self.post(self.parent, url + "/plan", {"plan": old, "interval": "month"}).status_code, 400)
        r = self.post(self.parent, url + "/plan", {"plan": "mechanical", "interval": "month"}).json
        sub = r["subscription"]
        self.assertEqual((sub["plan"], sub["plan_name"], sub["price_label"], sub["legacy"]), ("mechanical", "Mechanical", "$15/month", False))
        self.assertIn("No card was charged", r["billing"][0]["detail"])
        self.assertEqual(self.student.get("/api/me").json["user"]["plan"], "mechanical")
        r = self.post(self.parent, url + "/plan", {"plan": "mechanical", "interval": "week"}).json
        self.assertEqual(r["subscription"]["price_label"], "$8.62/month, billed $1.99 weekly")
        self.assertEqual(date.fromisoformat(r["subscription"]["renews_on"]) - date.today(), timedelta(days=7))
        self.assertIn("billed weekly at $1.99", r["billing"][0]["detail"])
        r = self.post(self.parent, url + "/plan", {"plan": "mechanical", "interval": "year"}).json
        self.assertEqual(r["subscription"]["price_label"], "$6/month, billed $72 yearly")
        renews = r["subscription"]["renews_on"]
        r = self.post(self.parent, url + "/plan/pause").json
        self.assertEqual(r["subscription"]["status"], "paused")
        self.assertGreater(r["subscription"]["renews_on"], renews)
        self.assertEqual(self.post(self.parent, url + "/plan/pause").status_code, 409)
        self.post(self.parent, url + "/plan/resume")
        r = self.post(self.parent, url + "/plan/cancel").json
        self.assertEqual((r["subscription"]["status"], r["subscription"]["plan"]), ("canceled", "mechanical"))  # runs to the end of the period
        with self.app.app_context():
            self.assertEqual(parent_svc.subscription(self.student_id, date.fromisoformat(r["subscription"]["renews_on"]) + timedelta(days=1))["plan"], "free")
        self.assertEqual(self.post(self.parent, url + "/plan/explode").status_code, 404)

    def test_parent_sees_every_plan_with_monthly_prices(self):
        plans = self.parent.get("/api/parent").json["plans"]
        self.assertEqual([p["key"] for p in plans], ["free", "mechanical"])
        self.assertEqual([p["name"] for p in plans], ["Sharpened", "Mechanical"])
        mech = plans[1]
        self.assertEqual(mech["cents"], {"week": 199, "month": 1500, "year": 7200})
        self.assertEqual(mech["per_month_cents"], {"week": 862, "month": 1500, "year": 600})
        self.assertEqual(mech["savings"]["year"], {"percent": 60, "per_year_cents": 10800})
        prices = [p["per_month_cents"]["month"] for p in plans]
        self.assertEqual(prices, sorted(prices), "plans go from free to the top plan")

    def test_old_plan_names_carry_over(self):
        import sqlite3
        from app.schema import MIGRATIONS
        db = self.app.config["DATABASE_URL"].replace("sqlite:///", "")
        con = sqlite3.connect(db)
        con.execute("UPDATE users SET plan = 'coached' WHERE id = ?", (self.student_id,))
        con.execute("INSERT INTO subscriptions (student_id, plan, billing_interval, status, updated_at) VALUES (?, 'daily', 'month', 'active', 'x')", (self.student_id,))
        for stmt in next(m for m in MIGRATIONS if m[0] == 8)[2]:  # the renaming migration, run again on old data
            con.execute(stmt)
        con.commit()
        self.assertEqual(con.execute("SELECT plan FROM users WHERE id = ?", (self.student_id,)).fetchone()[0], "masterstroke")
        self.assertEqual(con.execute("SELECT plan FROM subscriptions WHERE student_id = ?", (self.student_id,)).fetchone()[0], "sharpened")
        con.close()
        # Those October 2026 plans count as Mechanical now, still at the price they were bought at.
        with self.app.app_context():
            sub = parent_svc.subscription(self.student_id)
        self.assertEqual((sub["plan"], sub["plan_name"], sub["legacy"]), ("mechanical", "Mechanical", True))
        self.assertEqual((sub["price_cents"], sub["price_label"]), (3900, "$39/month (earlier price)"))
        self.assertEqual(self.student.get("/api/me").json["user"]["plan"], "mechanical")

    def test_older_plan_price_until_switching(self):
        url = self.link()
        with self.app.app_context():
            parent_svc._save(self.student_id, {"plan": "no2", "billing_interval": "week", "status": "active",
                                               "renews_on": (date.today() + timedelta(days=5)).isoformat(), "paused_until": None}, None)
        sub = self.parent.get(url).json["subscription"]
        self.assertEqual((sub["plan"], sub["price_label"], sub["legacy"]), ("mechanical", "$21.62/month, billed $4.99 weekly (earlier price)", True))
        r = self.post(self.parent, url + "/plan/cancel").json  # canceling keeps the plan, at its price, to the end
        self.assertEqual((r["subscription"]["status"], r["subscription"]["legacy"]), ("canceled", True))
        self.assertIn("Mechanical stays on until", r["billing"][0]["detail"])
        r = self.post(self.parent, url + "/plan", {"plan": "mechanical", "interval": "week"}).json  # today's price
        self.assertEqual((r["subscription"]["price_label"], r["subscription"]["legacy"], r["subscription"]["status"]),
                         ("$8.62/month, billed $1.99 weekly", False, "active"))

    def test_report_email(self):
        url = self.link()
        r = self.post(self.parent, url + "/report")
        self.assertEqual(r.status_code, 200, r.json)
        mail = mailer.OUTBOX[-1]
        self.assertEqual(mail["to"], "ana@home.org")
        self.assertIn("Maya's week", mail["subject"])
        self.assertIn("Study time", mail["text"])

    def test_sign_in_switch_must_match_the_account(self):
        c = self.app.test_client()
        r = self.post(c, "/api/auth/login", {"email": "maya@school.org", "password": "password123", "role": "parent"})
        self.assertEqual((r.status_code, r.json["code"]), (403, "wrong_role"))
        self.assertIn("student account", r.json["error"])
        self.assertEqual(c.get("/api/me").status_code, 401)  # not signed in
        r = self.post(c, "/api/auth/login", {"email": "ana@home.org", "password": "password123", "role": "student"})
        self.assertEqual(r.status_code, 403)
        self.assertEqual(self.post(c, "/api/auth/login", {"email": "ana@home.org", "password": "password123", "role": "parent"}).status_code, 200)
        self.assertEqual(self.post(c, "/api/auth/login", {"email": "maya@school.org", "password": "password123"}).status_code, 200)  # no switch: any account

    def test_test_parent_account_is_linked_to_beta(self):
        c = self.app.test_client()
        r = self.post(c, "/api/auth/login", {"email": "beta2", "password": "beta2"})
        self.assertEqual(r.status_code, 200, r.json)
        self.assertEqual(r.json["user"]["role"], "parent")
        self.assertEqual([s["name"] for s in c.get("/api/parent").json["students"]], ["Beta Tester"])

    def test_old_test_parent_is_renamed_to_beta2(self):
        import sqlite3
        from app import testaccount
        db = self.app.config["DATABASE_URL"].replace("sqlite:///", "")
        con = sqlite3.connect(db)
        con.execute("UPDATE users SET email = 'parent', name = 'Pat Tester' WHERE email = 'beta2'")
        con.commit(); con.close()
        testaccount.ensure(self.app.config["DATABASE_URL"])
        con = sqlite3.connect(db)
        rows = con.execute("SELECT email, name FROM users WHERE role = 'parent' AND email IN ('parent', 'beta2')").fetchall()
        links = con.execute("SELECT COUNT(*) FROM family_links f JOIN users p ON p.id = f.parent_id WHERE p.email = 'beta2'").fetchone()[0]
        con.close()
        self.assertEqual(rows, [("beta2", "Beta2 Parent")])
        self.assertEqual(links, 1)
        c = self.app.test_client()
        self.assertEqual(self.post(c, "/api/auth/login", {"email": "parent", "password": "parent"}).status_code, 400)


if __name__ == "__main__":
    unittest.main()
