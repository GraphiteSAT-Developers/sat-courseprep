"""The diagnostic and study plan. Run from the backend folder: python -m unittest discover tests"""
import shutil
import tempfile
import unittest
from collections import Counter
from datetime import date, timedelta

from app import create_app
from app.services import bank, diagnostic, studyplan
from tests.test_practice import right_answer, wrong_answer

ORIGIN = {"Origin": "http://localhost"}


def key_for(item_id, right=True):
    q = diagnostic.item(item_id)
    if q.get("section") == "Reading and Writing":
        return q["answer"] if right else (q["answer"] + 1) % 4
    return right_answer(q) if right else wrong_answer(q)


class PlanTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.app = create_app({"DATABASE_URL": f"sqlite:///{self.dir}/test.db", "TESTING": True, "PLAN_LIMITS": False, "FORCE_HTTPS": False,
                               "SESSION_COOKIE_SECURE": False, "BASE_URL": "http://localhost"})
        self.client = self.app.test_client()
        self.post("/api/auth/register", {"name": "Sam Lee", "email": "sam@school.org", "password": "password123"})
        self.test_date = (date.today() + timedelta(days=60)).isoformat()

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def post(self, url, data=None):
        return self.client.post(url, json=data or {}, headers=ORIGIN)

    def take_diagnostic(self, right=lambda i: i % 3 != 1):
        r = self.post("/api/plan/diagnostic", {"test_date": self.test_date, "weekly_goal_hours": 4})
        self.assertEqual(r.status_code, 201, r.json)
        d = r.json["diagnostic"]
        answers = {str(i): key_for(q["id"], right(i)) for i, q in enumerate(d["questions"])}
        sure = {str(i): True for i in range(len(d["questions"]))}
        r = self.post(f"/api/plan/diagnostic/{d['id']}/submit", {"answers": answers, "sure": sure})
        self.assertEqual(r.status_code, 201, r.json)
        return d, r.json

    def test_diagnostic_has_ten_questions_without_keys(self):
        d = self.post("/api/plan/diagnostic", {}).json["diagnostic"]
        self.assertEqual(len(d["questions"]), 10)
        self.assertEqual(Counter(q["section"] for q in d["questions"]), {"Math": 6, "Reading and Writing": 4})
        self.assertEqual(len({q["domain"] for q in d["questions"]}), 8, "every domain of both sections")
        for q in d["questions"]:
            self.assertNotIn("answer", q)
            self.assertNotIn("explain_html", q)
        again = self.post("/api/plan/diagnostic", {}).json["diagnostic"]
        self.assertEqual(again["id"], d["id"], "an unfinished diagnostic resumes")

    def test_results_and_plan(self):
        d, out = self.take_diagnostic()
        results, plan = out["results"], out["plan"]
        self.assertEqual(results["total"], 10)
        self.assertEqual(len(results["domains"]), 8)
        self.assertTrue(all("explain_html" in q for q in results["questions"]))
        self.assertEqual(plan["test_date"], self.test_date)
        self.assertEqual(plan["weeks"][-1]["phase"], "test")
        study = [w for w in plan["weeks"] if w["phase"] != "test"]
        diffs = [w["difficulty"] for w in study]
        self.assertEqual(diffs, sorted(diffs), "quizzes get harder as the test gets closer")
        self.assertGreater(study[-1]["mix"]["hard"], study[0]["mix"]["hard"])
        for w in plan["weeks"]:
            self.assertEqual(sum(w["mix"].values()), 10)
        # The plan comes back on the plan page and on the dashboard.
        over = self.client.get("/api/plan").json
        self.assertEqual(over["plan"]["current_week"], 0)
        self.assertTrue(over["diagnostic"]["submitted"])
        dash = self.client.get("/api/dashboard").json
        self.assertTrue(dash["plan"]["study_plan"])
        self.assertTrue(dash["plan"]["weeks"][0]["is_now"])

    def test_weakest_skills_come_first(self):
        _, out = self.take_diagnostic(right=lambda i: i not in (0, 1))  # both Algebra questions wrong
        first = out["plan"]["weeks"][0]["focus"]
        self.assertTrue(all(f["domain"] == "algebra" for f in first), first)
        self.assertIn("Algebra", out["results"]["focus"])

    def test_quiz_task_draws_from_the_week_and_adapts(self):
        _, out = self.take_diagnostic()
        week = out["plan"]["weeks"][0]
        r = self.post("/api/plan/tasks", {"week": 0, "task": "w1-quiz"})
        self.assertEqual(r.status_code, 201, r.json)
        s = r.json["session"]
        self.assertEqual((s["mode"], s["plan_task"], len(s["questions"])), ("quiz", "w1-quiz", 10))
        allowed = {f["name"] for f in week["focus"]} | ({week["review"]["name"]} if week["review"] else set())
        self.assertTrue({q["skill"] for q in s["questions"]} <= allowed)
        self.assertEqual(self.post("/api/plan/tasks", {"week": 0, "task": "w1-quiz"}).json["session"]["id"], s["id"], "resumes")
        # Checking works like topic practice.
        items = bank.all_items()
        c = self.post(f"/api/practice/sessions/{s['id']}/check", {"index": 0, "answer": right_answer(items[s["questions"][0]["id"]])})
        self.assertEqual(c.status_code, 200)
        # A perfect quiz makes the next one harder than the week's plan.
        answers = {str(i): right_answer(items[q["id"]]) for i, q in enumerate(s["questions"])}
        self.post(f"/api/practice/sessions/{s['id']}/submit", {"answers": answers, "seconds_used": 300})
        tasks = self.client.get("/api/plan").json["plan"]["tasks"]
        self.assertTrue(tasks["w1-quiz"]["done"])
        nxt = self.post("/api/plan/tasks", {"week": 0, "task": "w1-drill-1"}).json["session"]
        hard = sum(items[q["id"]]["difficulty"] == "hard" for q in nxt["questions"])
        self.assertGreaterEqual(hard, studyplan.mix_for(min(0.95, week["difficulty"] + 0.1))["hard"] - 1)

    def test_practice_test_task_and_bad_tasks(self):
        self.take_diagnostic()
        plan = self.client.get("/api/plan").json["plan"]
        week, task = next((i, t) for i, w in enumerate(plan["weeks"]) for t in w["tasks"] if t["kind"] == "test")
        s = self.post("/api/plan/tasks", {"week": week, "task": task["key"]}).json["session"]
        self.assertEqual((s["mode"], len(s["questions"]), s["minutes"]), ("test", 22, 35))
        self.assertEqual(self.post("/api/plan/tasks", {"week": 0, "task": "nope"}).status_code, 400)
        self.assertEqual(self.post("/api/plan/tasks", {"week": 99, "task": "w1-quiz"}).status_code, 400)

    def test_rebuild_with_new_date(self):
        self.take_diagnostic()
        soon = (date.today() + timedelta(days=12)).isoformat()
        plan = self.post("/api/plan/rebuild", {"test_date": soon}).json["plan"]
        self.assertLessEqual(len(plan["weeks"]), 3)
        self.assertEqual(plan["test_date"], soon)

    def move_plan_back(self, weeks):
        """Pretend the plan started `weeks` weeks ago, so this week is week weeks + 1."""
        import json
        from app.db import execute, query
        with self.app.app_context():
            row = query("SELECT id, plan FROM study_plans ORDER BY id DESC LIMIT 1", one=True)
            plan = json.loads(row["plan"])
            plan["start"] = (date.fromisoformat(plan["start"]) - timedelta(weeks=weeks)).isoformat()
            execute("UPDATE study_plans SET plan = ? WHERE id = ?", (json.dumps(plan), row["id"]))

    def test_missed_week_carries_over_into_this_week(self):
        self.take_diagnostic()
        self.move_plan_back(1)
        plan = self.client.get("/api/plan").json["plan"]
        self.assertEqual(plan["current_week"], 1)
        carried = plan["catch_up"]
        self.assertTrue(1 <= len(carried) <= studyplan.CATCH_UP_LIMIT)
        self.assertTrue(all(c["week"] == 0 and c["task"]["kind"] != "quiz" for c in carried))
        # A carried task starts from its own week, and once it's done it stops being carried.
        first = carried[0]
        s = self.post("/api/plan/tasks", {"week": first["week"], "task": first["task"]["key"]}).json["session"]
        self.post(f"/api/practice/sessions/{s['id']}/submit", {"answers": {}, "seconds_used": 30})
        after = self.client.get("/api/plan").json["plan"]["catch_up"]
        self.assertNotIn(first["task"]["key"], [c["task"]["key"] for c in after])

    def test_todays_set_reaches_carried_work_after_this_weeks(self):
        self.take_diagnostic()
        self.move_plan_back(1)
        today = self.client.get("/api/dashboard").json["today"]
        carried = [i for i in today["items"] if i["why"].startswith("Carried over from week 1")]
        self.assertTrue(carried)
        self.assertFalse(today["items"][0]["why"].startswith("Carried"), "this week's tasks come first")

    def test_tasks_need_a_plan(self):
        self.assertEqual(self.post("/api/plan/tasks", {"week": 0, "task": "w1-quiz"}).status_code, 400)
        self.assertIsNone(self.client.get("/api/plan").json["plan"])


class PlanUnitTest(unittest.TestCase):
    def test_mix_always_sums_and_ramps(self):
        prev_hard = -1
        for d in [i / 20 for i in range(1, 20)]:
            mix = studyplan.mix_for(d)
            self.assertEqual(sum(mix.values()), 10)
            self.assertGreaterEqual(mix["hard"], prev_hard)
            prev_hard = mix["hard"]

    def test_strong_students_start_harder(self):
        self.assertGreater(studyplan.difficulty_at(0.9, 0), studyplan.difficulty_at(0.2, 0))

    def test_catch_up_rules(self):
        results = {"level": 0.5, "skills": {}, "strengths": [], "focus": [],
                   "domains": [{"section": "Math", "domain": t["name"], "domain_key": t["key"], "score": 0.5} for t in bank.topics()]}
        plan = studyplan.build(results, None, 4, date(2026, 10, 16))
        self.assertEqual(studyplan.catch_up(plan, 0, {}), [], "nothing to carry in week 1")
        carried = studyplan.catch_up(plan, 3, {})
        self.assertLessEqual(len(carried), studyplan.CATCH_UP_LIMIT)
        self.assertEqual(carried[0]["week"], 2, "the most recent week first")
        this_week = {t["skill"]["skill"] for t in plan["weeks"][3]["tasks"] if t.get("skill")}
        for c in carried:
            self.assertNotEqual(c["task"]["kind"], "quiz")
            if c["task"]["kind"] == "drill":
                self.assertNotIn(c["task"]["skill"]["skill"], this_week)
        done = {t["key"]: {"done": True} for w in plan["weeks"][:3] for t in w["tasks"]}
        self.assertEqual(studyplan.catch_up(plan, 3, done), [], "nothing left over")

    def test_no_test_date_gives_eight_weeks(self):
        results = {"level": 0.5, "skills": {}, "strengths": [], "focus": [],
                   "domains": [{"section": "Math", "domain": t["name"], "domain_key": t["key"], "score": 0.5} for t in bank.topics()]}
        plan = studyplan.build(results, None, 3, date(2026, 10, 16))
        self.assertEqual(len(plan["weeks"]), 8)
        self.assertNotEqual(plan["weeks"][-1]["phase"], "test")


if __name__ == "__main__":
    unittest.main()
