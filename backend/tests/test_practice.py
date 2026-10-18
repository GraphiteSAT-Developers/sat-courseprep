"""Practice from the question bank. Run from the backend folder: python -m unittest discover tests"""
import shutil
import tempfile
import unittest
from collections import Counter
from fractions import Fraction

from app import create_app
from app.services import bank

ORIGIN = {"Origin": "http://localhost"}


def right_answer(q):
    """The key for a bank question, as a student would enter it."""
    if q["type"] == "mc":
        return q["answer"]
    n, d = q["keys"][0]
    return bank.fraction_text(Fraction(n, d))


def wrong_answer(q):
    return (q["answer"] + 1) % len(q["choices"]) if q["type"] == "mc" else "9999"


class PracticeTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.app = create_app({"DATABASE_URL": f"sqlite:///{self.dir}/test.db", "TESTING": True, "PLAN_LIMITS": False, "FORCE_HTTPS": False,
                               "SESSION_COOKIE_SECURE": False, "BASE_URL": "http://localhost"})
        self.client = self.app.test_client()
        self.post("/api/auth/register", {"name": "Sam Lee", "email": "sam@school.org", "password": "password123",
                                         "grade": 11, "test_date": "2030-12-07", "target_score": 1450})

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def post(self, url, data=None):
        return self.client.post(url, json=data or {}, headers=ORIGIN)

    def start(self, **data):
        r = self.post("/api/practice/sessions", data)
        self.assertEqual(r.status_code, 201, r.json)
        return r.json["session"]

    def answer_all(self, session, right=True):
        items = bank.all_items()
        answers = {str(i): (right_answer if right else wrong_answer)(items[q["id"]]) for i, q in enumerate(session["questions"])}
        r = self.post(f"/api/practice/sessions/{session['id']}/submit", {"answers": answers, "seconds_used": 600})
        self.assertEqual(r.status_code, 201, r.json)
        return r.json["result"]

    def test_bank_loads_with_explanations(self):
        items = bank.all_items()
        self.assertEqual(len(items), 1000)
        for q in items.values():
            self.assertIn("Solve it by hand", q["explain_html"], q["id"])
            self.assertNotRegex(q["explain_html"], r"\bT\d+\b", q["id"])

    def test_practice_test_mix_and_no_keys(self):
        s = self.start(mode="test")
        self.assertEqual(len(s["questions"]), 22)
        self.assertEqual(s["minutes"], 35)
        mix = Counter(q["domain"] for q in s["questions"])
        self.assertEqual(mix["Algebra"], 8)
        self.assertEqual(mix["Advanced Math"], 8)
        self.assertEqual(mix["Problem-Solving and Data Analysis"], 3)
        self.assertEqual(mix["Geometry and Trigonometry"], 3)
        self.assertEqual(len({q["id"] for q in s["questions"]}), 22)
        for q in s["questions"]:
            self.assertNotIn("answer", q)
            self.assertNotIn("explain_html", q)
        order = [bank.DIFFICULTY_ORDER[q["difficulty"]] for q in s["questions"]]
        self.assertEqual(order, sorted(order))

    def test_submitted_questions_do_not_repeat(self):
        first = self.start(mode="test")
        result = self.answer_all(first)
        self.assertEqual(result["correct"], 22)
        self.assertIn("Answer", result["questions"][0]["explain_html"])
        second = self.start(mode="test")
        self.assertFalse({q["id"] for q in first["questions"]} & {q["id"] for q in second["questions"]})
        self.assertEqual(self.client.get("/api/practice").json["done"], 22)
        # Practice tests count toward the dashboard's score history.
        self.assertEqual(len(self.client.get("/api/dashboard").json["history"]), 1)

    def test_unanswered_questions_stay_in_the_pool(self):
        s = self.start(mode="topic", domain="psda", skill="percentages", count=5)
        r = self.post(f"/api/practice/sessions/{s['id']}/submit", {"answers": {}, "seconds_used": 30})
        self.assertEqual(r.status_code, 201)
        self.assertEqual(self.client.get("/api/practice").json["done"], 0)

    def test_finishing_a_topic_congratulates_then_starts_over(self):
        skill = "evaluating-statistical-claims-observational-studies-and-experiments"
        pool = set(bank.pool("psda", skill))
        self.assertEqual(len(pool), 14)
        a = self.start(mode="topic", domain="psda", skill=skill, count=10)
        self.assertEqual(self.answer_all(a)["finished"], [])
        # Only 4 are left, so the next set is just those 4: no repeats before the topic is finished.
        b = self.start(mode="topic", domain="psda", skill=skill, count=10)
        self.assertEqual({q["id"] for q in b["questions"]}, pool - {q["id"] for q in a["questions"]})
        items = bank.all_items()
        for i, q in enumerate(b["questions"][:-1]):
            r = self.post(f"/api/practice/sessions/{b['id']}/check", {"index": i, "answer": right_answer(items[q["id"]])})
            self.assertEqual(r.json["finished"], [])
        last = len(b["questions"]) - 1
        r = self.post(f"/api/practice/sessions/{b['id']}/check", {"index": last, "answer": wrong_answer(items[b["questions"][last]["id"]])})
        self.assertEqual(r.json["finished"], [{"kind": "skill", "name": "Evaluating statistical claims: observational studies and experiments"}])
        self.assertEqual(self.answer_all(b)["finished"], [], "congratulated once")
        # The next set starts the topic over, and it can be finished again.
        c = self.start(mode="topic", domain="psda", skill=skill, count=10)
        self.assertEqual(len(c["questions"]), 10)
        topic = next(s for d in self.client.get("/api/practice").json["domains"] for s in d["skills"] if s["key"] == skill)
        self.assertEqual(topic["done"], 0)

    def test_finishing_a_domain(self):
        with self.app.app_context():
            from app.services import practice
            user = 1
            psda = bank.pool("psda")
            practice.mark_seen(user, psda[:-1])
            finished = practice.mark_seen(user, psda[-1:])
        self.assertIn({"kind": "domain", "name": "Problem-Solving and Data Analysis"}, finished)
        self.assertEqual(finished[0]["kind"], "skill", "the skill is named first")

    def test_practice_test_keeps_full_size_when_a_domain_runs_low(self):
        with self.app.app_context():
            from app.services import practice
            practice.mark_seen(1, bank.pool("geometry-trig")[:-1])
        s = self.start(mode="test")
        self.assertEqual(len(s["questions"]), 22)

    def test_topic_check_gives_feedback_and_locks(self):
        s = self.start(mode="topic", domain="algebra", count=5)
        items = bank.all_items()
        q0 = items[s["questions"][0]["id"]]
        r = self.post(f"/api/practice/sessions/{s['id']}/check", {"index": 0, "answer": wrong_answer(q0)})
        self.assertEqual(r.status_code, 200)
        self.assertFalse(r.json["question"]["correct"])
        self.assertIn("xp", r.json["question"]["explain_html"])
        again = self.post(f"/api/practice/sessions/{s['id']}/check", {"index": 0, "answer": right_answer(q0)})
        self.assertFalse(again.json["question"]["correct"], "a checked answer is locked")
        self.assertEqual(self.client.get(f"/api/practice/sessions/{s['id']}").json["session"]["checked"]["0"]["correct"], False)
        result = self.answer_all(s)
        self.assertEqual(result["correct"], 4)
        dash = self.client.get("/api/dashboard").json
        self.assertEqual(len(dash["review"]), 1)
        self.assertEqual(dash["history"], [], "topic practice doesn't count as a test score")

    def test_check_not_allowed_on_tests_and_bad_input(self):
        s = self.start(mode="test")
        self.assertEqual(self.post(f"/api/practice/sessions/{s['id']}/check", {"index": 0, "answer": 0}).status_code, 400)
        self.assertEqual(self.post("/api/practice/sessions", {"mode": "topic", "domain": "nope"}).status_code, 400)
        self.assertEqual(self.post("/api/practice/sessions", {"mode": "topic", "domain": "algebra", "count": 7}).status_code, 400)
        self.assertEqual(self.post("/api/practice/sessions", {"mode": "x"}).status_code, 400)

    def test_sessions_are_private(self):
        s = self.start(mode="test")
        self.post("/api/auth/logout")
        self.assertEqual(self.client.get(f"/api/practice/sessions/{s['id']}").status_code, 401)
        self.post("/api/auth/register", {"name": "Ana Ruiz", "email": "ana@school.org", "password": "password123"})
        self.assertEqual(self.client.get(f"/api/practice/sessions/{s['id']}").status_code, 404)


class EntryRulesTest(unittest.TestCase):
    def test_spr_entry_rules(self):
        two_thirds = Fraction(2, 3)
        for ok in ("2/3", ".6666", ".6667", "0.666", "0.667", "4/6"):
            self.assertTrue(bank.spr_matches(ok, two_thirds), ok)
        for no in ("0.67", ".667", "0.6", "-2/3", "2/3x"):
            self.assertFalse(bank.spr_matches(no, two_thirds), no)
        self.assertTrue(bank.spr_matches("-.6667", Fraction(-2, 3)))
        self.assertTrue(bank.spr_matches("1.75", Fraction(7, 4)))
        self.assertEqual(bank.accepted_entries(Fraction(7, 4)), ["7/4", "1.75"])

    def test_math_rendering(self):
        self.assertEqual(bank.math_html(r"\frac{1}{2}x"), '<span class="frac"><span>1</span><span>2</span></span><var>x</var>')
        self.assertEqual(bank.keystrokes(r"y=\frac{x-3}{x+2}"), "y=(x-3)/(x+2)")
        self.assertEqual(bank.keystrokes(r"T=2\pi\sqrt{\frac{L}{g}}"), "T=2pi sqrt(L/g)")


if __name__ == "__main__":
    unittest.main()
