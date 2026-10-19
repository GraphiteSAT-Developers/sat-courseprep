"""Keeping students going: the streak freeze, the free trial and the Math estimate. Run from the backend folder:
python -m unittest discover tests"""
import shutil
import tempfile
import unittest
from datetime import date, timedelta

from app import create_app
from app.services import game, parent as parent_svc

ORIGIN = {"Origin": "http://localhost"}


class StreakFreezeTest(unittest.TestCase):
    def days(self, *isos):
        return set(isos)

    def test_one_missed_day_a_week_is_covered(self):
        on = date(2026, 10, 16)  # a Friday
        st = game.streak_from(self.days("2026-10-12", "2026-10-13", "2026-10-15", "2026-10-16"), on)  # missed Wednesday
        self.assertEqual((st["days"], st["today"], st["frozen"]), (4, True, ["2026-10-14"]))
        self.assertFalse(st["freeze_ready"])  # used this week

    def test_a_second_miss_in_the_same_week_ends_it(self):
        on = date(2026, 10, 17)  # Saturday
        st = game.streak_from(self.days("2026-10-12", "2026-10-14", "2026-10-16", "2026-10-17"), on)
        self.assertEqual(st["days"], 3)  # Sat, Fri, then Wed after the frozen Thursday; Tuesday ends it

    def test_two_days_in_a_row_off_ends_it(self):
        on = date(2026, 10, 16)
        st = game.streak_from(self.days("2026-10-12", "2026-10-13", "2026-10-16"), on)
        self.assertEqual(st["days"], 1)
        self.assertTrue(st["freeze_ready"])

    def test_yesterday_missed_keeps_the_streak_until_today_ends(self):
        on = date(2026, 10, 16)
        st = game.streak_from(self.days("2026-10-13", "2026-10-14"), on)  # nothing yesterday or today yet
        self.assertEqual((st["days"], st["today"], st["frozen"]), (2, False, ["2026-10-15"]))

    def test_freezes_reset_each_week(self):
        on = date(2026, 10, 21)  # Wednesday of the next week
        st = game.streak_from(self.days("2026-10-15", "2026-10-17", "2026-10-18", "2026-10-20", "2026-10-21"), on)
        self.assertEqual(st["days"], 5)
        self.assertEqual(st["frozen"], ["2026-10-19", "2026-10-16"])


class TrialTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.app = create_app({"DATABASE_URL": f"sqlite:///{self.dir}/test.db", "TESTING": True, "FORCE_HTTPS": False,
                               "SESSION_COOKIE_SECURE": False, "BASE_URL": "http://localhost"})
        self.c = self.app.test_client()
        r = self.c.post("/api/auth/register", json={"name": "Maya Rivera", "email": "maya@school.org", "password": "password123",
                                                     "grade": 11, "test_date": (date.today() + timedelta(days=60)).isoformat()}, headers=ORIGIN)
        self.id = r.json["user"]["id"]

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def post(self, url):
        return self.c.post(url, json={}, headers=ORIGIN)

    def test_trial_once_no_card_then_back_to_free(self):
        d = self.c.get("/api/me/subscription").json
        self.assertTrue(d["subscription"]["trial_available"])
        self.assertEqual(d["trial"], {"plan": "mechanical", "plan_name": "Mechanical", "days": 7})
        r = self.post("/api/me/subscription/trial")
        self.assertEqual(r.status_code, 201, r.json)
        sub = r.json["subscription"]
        self.assertEqual((sub["plan"], sub["status"], sub["price_label"], sub["legacy"]), ("mechanical", "trial", "Free trial", False))
        self.assertEqual(r.json["access"]["counts_as"], "mechanical")
        self.assertTrue(r.json["access"]["features"]["level_up"]["ok"])
        self.assertIn("No card", r.json["billing"][0]["detail"])
        self.assertEqual(self.post("/api/me/subscription/trial").status_code, 409)
        self.assertEqual(self.post("/api/me/subscription/pause").status_code, 409)  # nothing billed to pause
        with self.app.app_context():
            later = parent_svc.subscription(self.id, date.today() + timedelta(days=8))
            self.assertEqual((later["plan"], later["status"], later["trial_available"]), ("free", "active", False))
            self.assertIn("nothing was charged", parent_svc.billing_history(self.id)[0]["detail"])

    def test_cancel_and_restart_a_trial(self):
        self.post("/api/me/subscription/trial")
        r = self.post("/api/me/subscription/cancel").json
        self.assertEqual(r["subscription"]["status"], "canceled")
        self.assertIn("Nothing is charged", r["billing"][0]["detail"])
        r = self.post("/api/me/subscription/resume").json
        self.assertEqual(r["subscription"]["status"], "trial")

    def test_buying_a_plan_ends_the_trial(self):
        self.post("/api/me/subscription/trial")
        r = self.c.post("/api/me/subscription/plan", json={"plan": "mechanical", "interval": "month", "agree": True}, headers=ORIGIN)
        self.assertEqual((r.json["subscription"]["plan"], r.json["subscription"]["status"]), ("mechanical", "active"))
        self.assertFalse(r.json["subscription"]["trial_available"])

    def test_dashboard_has_no_estimate_before_a_mock_test(self):
        self.assertIsNone(self.c.get("/api/dashboard").json["summary"]["math_estimate"])


if __name__ == "__main__":
    unittest.main()
