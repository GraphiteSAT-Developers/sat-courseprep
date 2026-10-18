"""Plans and locks, a student's own subscription, adaptive mock tests, copy warnings and analytics.
Run from the backend folder: python -m unittest discover tests"""
import json
import shutil
import tempfile
import unittest
from unittest import mock as umock

from app import create_app
from app.db import execute, query
from app.services import bank
from app.services import mock as mock_svc
from test_practice import ORIGIN, right_answer, wrong_answer


class Base(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.app = create_app({"DATABASE_URL": f"sqlite:///{self.dir}/test.db", "TESTING": True, "FORCE_HTTPS": False,
                               "SESSION_COOKIE_SECURE": False, "BASE_URL": "http://localhost"})
        self.client = self.app.test_client()
        self.post("/api/auth/register", {"name": "Sam Lee", "email": "sam@school.org", "password": "password123", "grade": 11})
        self.uid = self.client.get("/api/me").json["user"]["id"]

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def post(self, url, data=None, client=None):
        return (client or self.client).post(url, json=data or {}, headers=ORIGIN)

    def buy(self, plan="no2", interval="month"):
        r = self.post("/api/me/subscription/plan", {"plan": plan, "interval": interval, "agree": True})
        self.assertEqual(r.status_code, 201, r.json)
        return r.json

    def set_status(self, status):
        with self.app.app_context():
            execute("UPDATE subscriptions SET status = ? WHERE student_id = ?", (status, self.uid))


class LocksTest(Base):
    def test_free_plan_limits(self):
        r = self.post("/api/practice/sessions", {"mode": "topic", "domain": "algebra", "count": 5})
        self.assertEqual(r.status_code, 201)
        # The explanation is swapped for a note; the right answer still shows.
        s = r.json["session"]
        q = bank.all_items()[s["questions"][0]["id"]]
        g = self.post(f"/api/practice/sessions/{s['id']}/check", {"index": 0, "answer": right_answer(q)}).json["question"]
        self.assertIn("xp-locked", g["explain_html"])
        self.assertTrue(g["correct"])
        # One practice set a week on the free plan.
        r = self.post("/api/practice/sessions", {"mode": "topic", "domain": "algebra", "count": 5})
        self.assertEqual((r.status_code, r.json["code"]), (402, "plan_required"))
        self.assertEqual(r.json["lock"]["need"], "no2")
        # No mock tests, Level up or review queue.
        self.assertEqual(self.post("/api/mock-tests", {"section": "math"}).status_code, 402)
        self.assertEqual(self.post("/api/practice/sessions", {"mode": "test"}).status_code, 402)
        self.assertEqual(self.post("/api/levels/start", {"track": "algebra", "level": 1}).status_code, 402)
        dash = self.client.get("/api/dashboard").json
        self.assertFalse(dash["access"]["features"]["review_queue"]["ok"])
        self.assertEqual(dash["review"], [])

    def test_paid_plan_unlocks_and_unpaid_locks_again(self):
        self.buy("no2")
        self.assertEqual(self.post("/api/practice/sessions", {"mode": "topic", "domain": "algebra", "count": 5}).status_code, 201)
        self.assertEqual(self.post("/api/practice/sessions", {"mode": "topic", "domain": "algebra", "count": 5}).status_code, 201)
        # No. 2: two mock tests a month, then locked until next month or an upgrade.
        self.assertEqual(self.post("/api/mock-tests", {"section": "math"}).status_code, 201)
        self.assertEqual(self.post("/api/mock-tests", {"section": "math"}).status_code, 201)
        r = self.post("/api/mock-tests", {"section": "math"})
        self.assertEqual((r.status_code, r.json["lock"]["need"]), (402, "sharpened"))
        # Level up comes with Sharpened.
        self.assertEqual(self.post("/api/levels/start", {"track": "algebra", "level": 1}).status_code, 402)
        self.buy("sharpened")
        self.assertEqual(self.post("/api/mock-tests", {"section": "math"}).status_code, 201)
        self.assertEqual(self.post("/api/levels/start", {"track": "algebra", "level": 1}).status_code, 201)
        # A failed payment locks the paid features until it's paid; the lock asks for the same plan, not an upgrade.
        self.set_status("past_due")
        r = self.post("/api/levels/start", {"track": "algebra", "level": 1})
        self.assertEqual(r.status_code, 402)
        self.assertEqual(r.json["lock"]["need"], "sharpened")
        self.assertIn("payment", r.json["error"].lower())
        sub = self.client.get("/api/me/subscription").json
        self.assertEqual(sub["access"]["unpaid"], "A payment didn't go through")
        self.set_status("active")
        self.assertEqual(self.post("/api/levels/start", {"track": "algebra", "level": 1}).status_code, 201)

    def test_pause_locks_and_resume_unlocks(self):
        self.buy("sharpened")
        out = self.post("/api/me/subscription/pause").json
        self.assertEqual(out["subscription"]["status"], "paused")
        self.assertEqual(self.post("/api/mock-tests", {"section": "math"}).status_code, 402)
        out = self.post("/api/me/subscription/resume").json
        self.assertEqual(out["subscription"]["status"], "active")
        self.assertEqual(self.post("/api/mock-tests", {"section": "math"}).status_code, 201)

    def test_cancel_keeps_the_plan_to_the_end_of_the_period(self):
        self.buy("sharpened", "year")
        out = self.post("/api/me/subscription/cancel").json
        self.assertEqual((out["subscription"]["status"], out["subscription"]["plan"]), ("canceled", "sharpened"))
        self.assertEqual(self.post("/api/mock-tests", {"section": "math"}).status_code, 201)
        self.assertEqual(self.post("/api/me/subscription/resume").json["subscription"]["status"], "active")
        self.assertIn("You", self.client.get("/api/me/subscription").json["payer"]["name"])

    def test_parent_dashboard_locks_progress_but_not_billing(self):
        code = self.post("/api/family/code").json["code"]
        parent = self.app.test_client()
        self.post("/api/auth/register", {"name": "Ana Lee", "email": "ana@home.org", "password": "password123", "role": "parent"}, parent)
        self.post("/api/parent/link", {"code": code}, parent)
        s = parent.get(f"/api/parent/students/{self.uid}").json
        self.assertFalse(s["access"]["ok"])
        self.assertIsNone(s["scores"])
        self.assertEqual(s["subscription"]["plan"], "free")
        self.buy("sharpened")
        s = parent.get(f"/api/parent/students/{self.uid}").json
        self.assertTrue(s["access"]["ok"])
        self.assertIsInstance(s["scores"], list)

    def test_limits_can_be_turned_off(self):
        self.app.config["PLAN_LIMITS"] = False
        for _ in range(3):
            self.assertEqual(self.post("/api/practice/sessions", {"mode": "topic", "domain": "algebra", "count": 5}).status_code, 201)
        self.assertEqual(self.post("/api/mock-tests", {"section": "math"}).status_code, 201)


class MockTestTest(Base):
    def setUp(self):
        super().setUp()
        self.buy("sharpened")

    def answers(self, session, right):
        items = bank.all_items()
        out = {}
        for i, q in enumerate(session["questions"]):
            ok = right(i)
            out[str(i)] = (right_answer if ok else wrong_answer)(items[q["id"]])
        return out

    def run_module(self, session_id, right):
        s = self.client.get(f"/api/practice/sessions/{session_id}").json["session"]
        r = self.post(f"/api/practice/sessions/{session_id}/submit", {"answers": self.answers(s, right), "seconds_used": 1800})
        self.assertEqual(r.status_code, 201, r.json)
        return s, r.json["result"]

    def test_reading_and_writing_is_coming_soon(self):
        r = self.post("/api/mock-tests", {"section": "rw"})
        self.assertEqual((r.status_code, r.json["code"]), (409, "coming_soon"))

    def test_strong_module_1_gets_the_harder_module_2_with_new_questions(self):
        m = self.post("/api/mock-tests", {"section": "math", "with_break": True}).json["mock"]
        self.assertEqual((m["status"], m["break_left"]), ("break", 600))
        s1 = self.client.get(f"/api/practice/sessions/{m['m1_session']}").json["session"]
        self.assertEqual(len(s1["questions"]), 22)
        self.assertEqual((s1["mock"]["module"], s1["minutes"]), (1, 35))
        # The break: started, then ended early.
        self.assertEqual(self.post(f"/api/mock-tests/{m['id']}/break", {"action": "start"}).json["mock"]["status"], "break")
        self.assertEqual(self.post(f"/api/mock-tests/{m['id']}/break", {"action": "end"}).json["mock"]["status"], "module1")
        s1, r1 = self.run_module(m["m1_session"], lambda i: True)
        self.assertIn("next_session", r1["mock"])
        s2 = self.client.get(f"/api/practice/sessions/{r1['mock']['next_session']}").json["session"]
        ids1 = {q["id"] for q in s1["questions"]}
        ids2 = {q["id"] for q in s2["questions"]}
        self.assertEqual((len(ids1), len(ids2), len(ids1 & ids2)), (22, 22, 0))
        hard = sum(1 for i in ids2 if bank.all_items()[i]["difficulty"] == "hard")
        self.assertGreaterEqual(hard, 9)
        _, final = self.run_module(s2["id"], lambda i: i % 2 == 0)
        self.assertEqual((final["total"], final["correct"], final["route"]), (44, 33, "harder"))
        self.assertEqual(final["score"], mock_svc.estimate("harder", 33))
        self.assertEqual([m["n"] for m in final["modules"]], [1, 2])
        # One entry in the score history for the whole section, not one per module.
        dash = self.client.get("/api/dashboard").json
        self.assertEqual(len(dash["history"]), 1)
        self.assertEqual(dash["history"][0]["total"], 44)
        # The next mock test has none of these questions.
        m2 = self.post("/api/mock-tests", {"section": "math"}).json["mock"]
        nxt = {q["id"] for q in self.client.get(f"/api/practice/sessions/{m2['m1_session']}").json["session"]["questions"]}
        self.assertFalse(nxt & (ids1 | ids2))

    def test_weak_module_1_gets_the_easier_module_2(self):
        m = self.post("/api/mock-tests", {"section": "math", "with_break": False}).json["mock"]
        self.assertEqual(m["status"], "module1")
        _, r1 = self.run_module(m["m1_session"], lambda i: i < 5)
        s2 = self.client.get(f"/api/practice/sessions/{r1['mock']['next_session']}").json["session"]
        easy = sum(1 for q in s2["questions"] if bank.all_items()[q["id"]]["difficulty"] == "easy")
        self.assertGreaterEqual(easy, 8)
        _, final = self.run_module(s2["id"], lambda i: True)
        self.assertEqual(final["route"], "easier")
        self.assertLessEqual(final["score"], 610)

    def test_score_estimates_stay_in_range(self):
        self.assertEqual(mock_svc.estimate("harder", 44), 800)
        self.assertEqual(mock_svc.estimate("easier", 0), 200)
        self.assertLess(mock_svc.estimate("easier", 35), mock_svc.estimate("harder", 44))

    def test_break_runs_out_by_itself(self):
        m = self.post("/api/mock-tests", {"section": "math"}).json["mock"]
        self.post(f"/api/mock-tests/{m['id']}/break", {"action": "start"})
        with self.app.app_context():
            execute("UPDATE mock_tests SET break_started_at = '2020-01-01T00:00:00Z' WHERE id = ?", (m["id"],))
        s = self.client.get(f"/api/practice/sessions/{m['m1_session']}").json["session"]
        self.assertEqual((s["mock"]["status"], s["mock"]["break_left"]), ("module1", 0))


class CopyWarningTest(Base):
    def test_warns_then_emails_the_parent(self):
        code = self.post("/api/family/code").json["code"]
        parent = self.app.test_client()
        self.post("/api/auth/register", {"name": "Ana Lee", "email": "ana@home.org", "password": "password123", "role": "parent"}, parent)
        self.post("/api/parent/link", {"code": code}, parent)
        with umock.patch("app.services.integrity.mailer.send") as send:
            first = self.post("/api/integrity/copy", {"kind": "copy", "page": "practice-test", "chars": 80}).json
            self.assertEqual(first["action"], "warned")
            send.assert_not_called()
            second = self.post("/api/integrity/copy", {"kind": "copy", "page": "practice-test", "chars": 80}).json
            self.assertEqual(second["action"], "parent_emailed")
            self.assertEqual(send.call_args[0][0], "ana@home.org")
            # A burst of copies sends one email.
            third = self.post("/api/integrity/copy", {"kind": "paste", "page": "speed"}).json
            self.assertEqual(third["action"], "recorded")
            self.assertEqual(send.call_count, 1)
        alerts = parent.get(f"/api/parent/students/{self.uid}").json["alerts"]
        self.assertTrue(any("copied question text 3 times" in a["text"] for a in alerts))

    def test_without_a_parent_it_is_recorded(self):
        self.assertEqual(self.post("/api/integrity/copy", {"page": "speed"}).json["action"], "warned")
        r = self.post("/api/integrity/copy", {"page": "speed"}).json
        self.assertEqual((r["action"], r["parents"]), ("recorded", 0))
        export = self.client.get("/api/me/export")
        self.assertEqual(export.status_code, 200)
        self.assertIn("integrity_events", export.get_data(as_text=True))


class AnalyticsTest(Base):
    EVENT = {"kind": "pageview", "path": "/practice.html?x=1", "referrer": "https://www.google.com/search?q=sat",
             "utm_source": "newsletter", "screen": "1920x1080", "lang": "en-US", "tz": "America/New_York"}

    def test_nothing_saved_without_consent(self):
        r = self.post("/api/analytics", {"events": [self.EVENT]})
        self.assertEqual(r.json["saved"], 0)

    def test_saved_with_consent_and_tied_to_the_account(self):
        self.client.set_cookie("gs_consent", "analytics")
        self.client.set_cookie("gs_vid", "abcdefghijklmnop1234")
        ua = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Version/17.0 Mobile/15E148 Safari/604.1"}
        r = self.client.post("/api/analytics", json={"events": [self.EVENT, {"kind": "engage", "path": "/practice.html", "duration_ms": 42000,
                                                               "scroll_pct": 80}, {"kind": "nope"}]}, headers=dict(ORIGIN, **ua))
        self.assertEqual(r.json["saved"], 2)
        with self.app.app_context():
            rows = [dict(x) for x in query("SELECT * FROM analytics_events ORDER BY id")]
        self.assertEqual((rows[0]["path"], rows[0]["referrer"], rows[0]["device"], rows[0]["os"], rows[0]["user_id"]),
                         ("/practice.html", "www.google.com", "phone", "iOS", self.uid))
        self.assertEqual(rows[1]["scroll_pct"], 80)

    def test_consent_is_recorded_and_turning_off_clears_anonymous_rows(self):
        anon = self.app.test_client()
        anon.set_cookie("gs_consent", "analytics")
        anon.set_cookie("gs_vid", "zzzzzzzzzzzzzzzz9999")
        self.assertEqual(self.post("/api/consent", {"analytics": True, "version": 1}, anon).status_code, 201)
        self.assertEqual(self.post("/api/analytics", {"events": [self.EVENT]}, anon).json["saved"], 1)
        self.post("/api/consent", {"analytics": False, "version": 1, "gpc": True}, anon)
        with self.app.app_context():
            self.assertEqual(query("SELECT COUNT(*) AS n FROM analytics_events", one=True)["n"], 0)
            log = [dict(r) for r in query("SELECT analytics, gpc FROM consent_log ORDER BY id")]
        self.assertEqual(log, [{"analytics": 1, "gpc": 0}, {"analytics": 0, "gpc": 1}])


if __name__ == "__main__":
    unittest.main()


class BackgroundTest(Base):
    def test_plain_background_by_default_and_ripples_are_bought(self):
        look = self.client.get("/api/me").json["user"]["appearance"]
        self.assertEqual((look["effect"], look["ripple"]), ("none", False))
        r = self.client.patch("/api/me/appearance", json={"effect": "ripple"}, headers=ORIGIN)
        self.assertEqual(r.status_code, 403, r.json)
        with self.app.app_context():
            execute("INSERT INTO xp_events (user_id, kind, xp, coins, detail, day, at) VALUES (?, 'gift', 0, 500, 'test', '2026-10-18', '2026-10-18T00:00:00Z')", (self.uid,))
        self.assertEqual(self.post("/api/game/buy", {"item": "effect:ripple"}).status_code, 200)
        r = self.client.patch("/api/me/appearance", json={"effect": "ripple"}, headers=ORIGIN)
        self.assertEqual(r.status_code, 200, r.json)
        look = self.client.get("/api/me").json["user"]["appearance"]
        self.assertEqual((look["effect"], look["ripple"]), ("ripple", True))
        shop = {i["key"]: i for i in self.client.get("/api/game").json["shop"]}
        self.assertEqual(shop["effect:ripple"]["price"], 120)

    def test_a_saved_ripple_background_needs_the_purchase(self):
        with self.app.app_context():
            execute("UPDATE users SET prefs = ? WHERE id = ?", (json.dumps({"look": {"effect": "ripple"}}), self.uid))
        self.assertEqual(self.client.get("/api/me").json["user"]["appearance"]["effect"], "none")


class TestAccountSwitchTest(Base):
    def test_beta_switches_plans_and_states_instantly(self):
        beta = self.app.test_client()
        self.post("/api/auth/login", {"email": "beta", "password": "beta"}, beta)
        r = beta.get("/api/me/subscription").json
        self.assertTrue(r["test_account"])
        out = self.post("/api/me/subscription/test", {"plan": "sharpened"}, beta).json
        self.assertEqual((out["subscription"]["plan"], out["subscription"]["status"]), ("sharpened", "active"))
        self.assertTrue(out["access"]["features"]["level_up"]["ok"])
        out = self.post("/api/me/subscription/test", {"plan": "sharpened", "status": "past_due"}, beta).json
        self.assertEqual(out["access"]["unpaid"], "A payment didn't go through")
        self.assertFalse(out["access"]["features"]["level_up"]["ok"])
        out = self.post("/api/me/subscription/test", {"plan": "free"}, beta).json
        self.assertEqual(out["subscription"]["plan"], "free")
        self.assertEqual(self.post("/api/me/subscription/test", {"plan": "free", "status": "paused"}, beta).status_code, 400)

    def test_other_accounts_cant(self):
        self.assertFalse(self.client.get("/api/me/subscription").json["test_account"])
        self.assertEqual(self.post("/api/me/subscription/test", {"plan": "sharpened"}).status_code, 403)
