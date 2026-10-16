"""Pages that now run on the backend: the home sample question, Today's set and reopening review questions."""
import shutil
import tempfile
import unittest
from datetime import date, timedelta

from app import create_app
from app.services import bank
from tests.test_practice import right_answer, wrong_answer
from tests.test_plan import PlanTest

ORIGIN = {"Origin": "http://localhost"}


class ConnectionsTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.app = create_app({"DATABASE_URL": f"sqlite:///{self.dir}/test.db", "TESTING": True, "FORCE_HTTPS": False,
                               "SESSION_COOKIE_SECURE": False, "BASE_URL": "http://localhost"})
        self.client = self.app.test_client()

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def post(self, url, data=None):
        return self.client.post(url, json=data or {}, headers=ORIGIN)

    def register(self):
        self.post("/api/auth/register", {"name": "Sam Lee", "email": "sam@school.org", "password": "password123"})

    def test_sample_question_needs_no_account_and_hides_the_key(self):
        q = self.client.get("/api/sample").json["question"]
        self.assertEqual(q["type"], "mc")
        self.assertNotIn("answer", q)
        item = bank.all_items()[q["id"]]
        r = self.post("/api/sample/check", {"id": q["id"], "answer": item["answer"]}).json
        self.assertTrue(r["correct"])
        self.assertIn("Solve it by hand", r["explain_html"])
        self.assertEqual(self.post("/api/sample/check", {"id": "nope", "answer": 0}).status_code, 404)

    def test_today_sends_new_students_to_the_diagnostic(self):
        self.register()
        self.assertEqual(self.post("/api/today").json, {"redirect": "plan.html"})
        self.assertEqual(self.client.get("/api/dashboard").json["today"]["source"], "none")

    def test_today_follows_the_study_plan(self):
        self.register()
        self.test_date = (date.today() + timedelta(days=60)).isoformat()
        PlanTest.take_diagnostic(self)
        dash = self.client.get("/api/dashboard").json["today"]
        self.assertEqual(dash["source"], "plan")
        self.assertFalse(dash["items"][0]["done"])
        s = self.post("/api/today").json["session"]
        self.assertEqual(s["plan_task"], "w1-drill-1")
        items = bank.all_items()
        self.post(f"/api/practice/sessions/{s['id']}/submit",
                  {"answers": {str(i): right_answer(items[q["id"]]) for i, q in enumerate(s["questions"])}, "seconds_used": 60})
        self.assertTrue(self.client.get("/api/dashboard").json["today"]["items"][0]["done"])
        self.assertEqual(self.post("/api/today").json["session"]["plan_task"], "w1-drill-2", "moves on to the next task")

    def test_today_without_a_plan_uses_the_weakest_domain(self):
        self.register()
        s = self.post("/api/practice/sessions", {"mode": "test"}).json["session"]
        items = bank.all_items()
        answers = {str(i): (wrong_answer if q["domain"] == "Geometry and Trigonometry" else right_answer)(items[q["id"]])
                   for i, q in enumerate(s["questions"])}
        self.post(f"/api/practice/sessions/{s['id']}/submit", {"answers": answers, "seconds_used": 600})
        today = self.post("/api/today").json["session"]
        self.assertEqual({q["domain"] for q in today["questions"]}, {"Geometry and Trigonometry"})

    def test_review_questions_reopen_and_clear(self):
        self.register()
        s = self.post("/api/practice/sessions", {"mode": "topic", "domain": "algebra", "count": 5}).json["session"]
        items = bank.all_items()
        q0 = items[s["questions"][0]["id"]]
        self.post(f"/api/practice/sessions/{s['id']}/check", {"index": 0, "answer": wrong_answer(q0)})
        item = self.client.get("/api/dashboard").json["review"][0]
        self.assertTrue(item["practice"])
        for expect_cleared in (False, True):
            r = self.post(f"/api/review/{item['id']}/practice").json["session"]
            self.assertEqual([q["id"] for q in r["questions"]], [q0["id"]])
            c = self.post(f"/api/practice/sessions/{r['id']}/check", {"index": 0, "answer": right_answer(q0)}).json
            self.assertEqual(c["question"]["review"]["cleared"], expect_cleared)
        self.assertEqual(self.client.get("/api/dashboard").json["review"], [])
        self.assertEqual(self.post(f"/api/review/{item['id']}/practice").status_code, 404)

    def test_review_miss_resets_progress(self):
        self.register()
        s = self.post("/api/practice/sessions", {"mode": "topic", "domain": "algebra", "count": 5}).json["session"]
        q0 = bank.all_items()[s["questions"][0]["id"]]
        self.post(f"/api/practice/sessions/{s['id']}/check", {"index": 0, "answer": wrong_answer(q0)})
        rid = self.client.get("/api/dashboard").json["review"][0]["id"]
        r = self.post(f"/api/review/{rid}/practice").json["session"]
        self.post(f"/api/practice/sessions/{r['id']}/check", {"index": 0, "answer": right_answer(q0)})
        r = self.post(f"/api/review/{rid}/practice").json["session"]
        self.post(f"/api/practice/sessions/{r['id']}/check", {"index": 0, "answer": wrong_answer(q0)})
        self.assertEqual(self.client.get("/api/dashboard").json["review"][0]["right_count"], 0)


    def test_first_dashboard_visit_goes_to_the_diagnostic_once(self):
        self.register()
        self.assertTrue(self.client.get("/api/dashboard").json["start_with_diagnostic"])
        self.assertFalse(self.client.get("/api/dashboard").json["start_with_diagnostic"], "only once, so skipping is allowed")

    def test_no_redirect_once_the_plan_page_was_seen(self):
        self.register()
        self.client.get("/api/plan")
        self.assertFalse(self.client.get("/api/dashboard").json["start_with_diagnostic"])


if __name__ == "__main__":
    unittest.main()
