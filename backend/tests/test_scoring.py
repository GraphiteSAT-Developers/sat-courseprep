"""The SAT score calculator (services/scoring.py) and where its estimate shows up. Run from the backend folder:
python -m unittest discover tests"""
import shutil
import tempfile
import unittest

from app import create_app
from app.services import scorecheck, scoring

ORIGIN = {"Origin": "http://localhost"}


def module(right, n=22, difficulty="medium"):
    return [{"correct": i < right, "difficulty": difficulty} for i in range(n)]


class CurveTest(unittest.TestCase):
    def test_curves_rise_with_right_answers_and_stay_in_range(self):
        for (section, route), points in scoring.CURVES.items():
            top = points[-1][0]
            scores = [scoring.section_score(section, route, raw) for raw in range(top + 1)]
            self.assertEqual(scores, sorted(scores), (section, route))
            self.assertTrue(all(200 <= s <= 800 and s % 10 == 0 for s in scores))

    def test_only_the_harder_module_reaches_800(self):
        self.assertEqual(scoring.section_score("math", "harder", 44), 800)
        self.assertEqual(scoring.section_score("rw", "harder", 54), 800)
        self.assertLessEqual(scoring.section_score("math", "easier", 44), 600)
        self.assertEqual(scoring.section_score("Reading and Writing", "easier", 0), 200)

    def test_score_calculator_anchor_points(self):
        self.assertEqual(scoring.section_score("math", "harder", 41), 740)
        self.assertEqual(scoring.section_score("math", "harder", 35), 640)

    def test_full_estimate_has_a_range(self):
        e = scoring.full("math", "harder", 44)
        self.assertEqual((e["score"], e["high"], e["low"]), (800, 800, 770))
        self.assertFalse(e["projected"])


class ProjectionTest(unittest.TestCase):
    def test_strong_module_projects_through_the_harder_module(self):
        e = scoring.project("math", module(20))
        self.assertEqual(e["route"], "harder")
        self.assertTrue(e["projected"])
        self.assertGreater(e["score"], scoring.project("math", module(12))["score"])
        self.assertEqual(e["high"] - e["low"], 2 * scoring.SPREAD["projected"])

    def test_weak_module_projects_through_the_easier_module(self):
        e = scoring.project("rw", module(10, 27))
        self.assertEqual(e["route"], "easier")
        self.assertLessEqual(e["score"], 590)

    def test_missing_hard_questions_lowers_the_projection(self):
        # The same 15 of 22 right, but one student misses only hard questions and the other misses easy ones.
        hard_misses = [{"correct": True, "difficulty": "easy"}] * 8 + [{"correct": True, "difficulty": "medium"}] * 7 + \
                      [{"correct": False, "difficulty": "hard"}] * 7
        easy_misses = [{"correct": False, "difficulty": "easy"}] * 7 + [{"correct": True, "difficulty": "medium"}] * 8 + \
                      [{"correct": True, "difficulty": "hard"}] * 7
        self.assertLess(scoring.project("math", hard_misses)["score"], scoring.project("math", easy_misses)["score"])

    def test_empty_and_unlabeled_modules(self):
        self.assertIsNone(scoring.project("math", []))
        self.assertEqual(scoring.project("Math", [{"correct": True}] * 22)["score"], 800)


class ResultsShowTheEstimateTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.app = create_app({"DATABASE_URL": f"sqlite:///{self.dir}/test.db", "TESTING": True, "PLAN_LIMITS": False, "FORCE_HTTPS": False,
                               "SESSION_COOKIE_SECURE": False, "BASE_URL": "http://localhost"})
        self.c = self.app.test_client()
        self.c.post("/api/auth/register", json={"name": "Sam Lee", "email": "sam@school.org", "password": "password123", "grade": 11,
                                                "test_date": "2030-12-07", "target_score": 1450}, headers=ORIGIN)

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def test_fixed_practice_test_gets_a_projected_score(self):
        r = self.c.post("/api/tests/pt4-math-m1/attempts", json={"answers": {"0": 1}, "seconds_used": 60}, headers=ORIGIN)
        e = r.json["result"]["estimate"]
        self.assertTrue(e["projected"])
        self.assertEqual(e["section"], "math")
        self.assertTrue(200 <= e["low"] <= e["score"] <= e["high"] <= 800)

    def test_practice_test_set_gets_a_projected_score(self):
        s = self.c.post("/api/practice/sessions", json={"mode": "test"}, headers=ORIGIN).json["session"]
        r = self.c.post(f"/api/practice/sessions/{s['id']}/submit", json={"answers": {}, "seconds_used": 60}, headers=ORIGIN)
        e = r.json["result"]["estimate"]
        self.assertEqual((e["score"], e["route"]), (200, "easier"))


class ScoreCheckTest(unittest.TestCase):
    """The score check: 20 questions without an account (routes/scorecheck.py, services/scorecheck.py)."""

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.app = create_app({"DATABASE_URL": f"sqlite:///{self.dir}/test.db", "TESTING": True, "PLAN_LIMITS": False, "FORCE_HTTPS": False,
                               "SESSION_COOKIE_SECURE": False, "BASE_URL": "http://localhost"})
        self.c = self.app.test_client()

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def start(self):
        r = self.c.get("/api/score-check")
        self.assertEqual(r.status_code, 200)
        return r.json

    def grade(self, token, answers, sure=None):
        return self.c.post("/api/score-check/grade", json={"token": token, "answers": answers, "sure": sure or {}}, headers=ORIGIN)

    def test_twenty_questions_in_test_order_without_answers(self):
        from app.services import bank
        qs = self.start()["questions"]
        self.assertEqual(len(qs), scorecheck.QUESTIONS)
        self.assertEqual([q["section"] for q in qs], ["rw"] * 10 + ["math"] * 10)
        self.assertEqual(sum(q["type"] == "spr" for q in qs), 2)
        self.assertEqual(len({q["id"] for q in qs}), 20)
        for q in qs:
            self.assertNotIn("answer", q)
            self.assertNotIn("explain_html", q)
        math = [bank.DIFFICULTY_ORDER[q["difficulty"]] for q in qs[10:]]
        self.assertEqual(math, sorted(math))

    def test_all_right_scores_1600_and_lists_no_skills(self):
        from app.services import bank
        r = self.start()
        items = bank.all_items()
        answers = {}
        for i, q in enumerate(r["questions"]):
            item = items[q["id"]]
            answers[str(i)] = item["answer"] if item["type"] == "mc" else item["answer_text"].split(" or ")[0]
        res = self.grade(r["token"], answers, {str(i): 1 for i in range(20)}).json["result"]
        self.assertEqual(res["total"]["score"], 1600)
        self.assertEqual(res["correct"], 20)
        self.assertEqual(res["skills"], [])
        self.assertTrue(all(q["explain_html"] for q in res["questions"]))

    def test_blank_check_scores_low_and_ranks_skills(self):
        res = self.grade(self.start()["token"], {}).json["result"]
        self.assertEqual(res["total"]["score"], 400)
        self.assertEqual(res["total"]["low"], 400)
        self.assertEqual(len(res["skills"]), scorecheck.TOP_SKILLS)
        points = [s["points"] for s in res["skills"]]
        self.assertEqual(points, sorted(points, reverse=True))
        self.assertEqual([s["name"] for s in res["sections"]], ["Reading and Writing", "Math"])

    def test_lucky_guesses_still_count_but_show_as_skills(self):
        from app.services import bank
        r = self.start()
        items = bank.all_items()
        answers = {str(i): items[q["id"]]["answer"] for i, q in enumerate(r["questions"]) if q["type"] == "mc"}
        sure = self.grade(r["token"], answers, {str(i): 1 for i in range(20)}).json["result"]
        r2 = self.start()
        answers2 = {str(i): items[q["id"]]["answer"] for i, q in enumerate(r2["questions"]) if q["type"] == "mc"}
        guessed = self.grade(r2["token"], answers2, {}).json["result"]
        self.assertTrue(any(s["guessed"] for s in guessed["skills"]))
        self.assertFalse(any(s["guessed"] for s in sure["skills"]))

    def test_a_check_can_be_scored_once_and_tokens_cant_be_forged(self):
        token = self.start()["token"]
        self.assertEqual(self.grade(token, {}).status_code, 200)
        self.assertEqual(self.grade(token, {}).status_code, 409)
        self.assertEqual(self.grade("not-a-token", {}).status_code, 400)
        self.assertEqual(self.grade(token + "x", {}).status_code, 400)

    def test_starting_checks_is_rate_limited(self):
        for _ in range(10):
            self.assertEqual(self.c.get("/api/score-check").status_code, 200)
        self.assertEqual(self.c.get("/api/score-check").status_code, 429)

    def test_the_page_is_open_to_everyone(self):
        r = self.c.get("/score-check.html")
        self.assertIn(r.status_code, (200, 404))  # 404 only when the site hasn't been built
        self.assertNotEqual(r.status_code, 302)
