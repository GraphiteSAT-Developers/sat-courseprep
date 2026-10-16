"""The Desmos masterclass. Run from the backend folder: python -m unittest discover tests

Each lesson's steps are checked against the real calculator by website/verify_masterclass.mjs.
"""
import shutil
import tempfile
import unittest

from app import create_app
from app.services import masterclass

ORIGIN = {"Origin": "http://localhost"}


class MasterclassContentTest(unittest.TestCase):
    def test_every_lesson_is_complete(self):
        units = {u["id"] for u in masterclass.content()["units"]}
        for lesson in masterclass.content()["lessons"]:
            with self.subTest(lesson=lesson["id"]):
                self.assertIn(lesson["unit"], units)
                for key in ("title", "summary", "goal", "minutes", "intro"):
                    self.assertTrue(lesson.get(key), key)
                if lesson.get("kind") == "drill":
                    self.assertTrue(lesson["items"])
                    self.assertTrue(all(i["answer"] in ("desmos", "hand") for i in lesson["items"]))
                    continue
                self.assertTrue(lesson["steps"])
                for step in lesson["steps"]:
                    for key in ("do", "check", "hint", "done"):
                        self.assertIn(key, step)
                self.assertEqual(len(lesson["quiz"]), 3)
                for q in lesson["quiz"]:
                    self.assertIn("check", q)
                    self.assertTrue(q.get("use"))
                # The SAT-style question opens only after the student does the work in the calculator.
                self.assertIn("check", lesson["try"])
                self.assertTrue(lesson["try"].get("use"))
                for q in lesson.get("reads", []) + [lesson["try"]] + lesson["quiz"]:
                    if "choices" in q:
                        self.assertIn(q["answer"], range(len(q["choices"])))
                    else:
                        self.assertIsInstance(q["answer"], str)

    def test_every_bank_topic_has_a_lesson(self):
        from app.services import bank
        skills = {(d["key"], s["key"]) for d in bank.topics() for s in d["skills"]}
        topics = masterclass.content()["topics"]
        self.assertEqual({(t["domain"], t["skill"]) for t in topics}, skills)
        for t in topics:
            with self.subTest(topic=t["id"]):
                self.assertEqual(t["id"], "topic-" + t["skill"])
                for key in ("title", "summary", "goal", "minutes", "intro", "rules", "example", "try"):
                    self.assertTrue(t.get(key), key)
                self.assertEqual(len(t["quiz"]), 3)
                for q in [t["try"]] + t["quiz"]:
                    if "choices" in q:
                        self.assertIn(q["answer"], range(len(q["choices"])))
                    if "check" in q:
                        self.assertTrue(q.get("use"))
                for r in t.get("related", []):
                    self.assertIn(r, masterclass.lessons())

    def test_ids_are_unique(self):
        ids = [lesson["id"] for lesson in masterclass.content()["lessons"] + masterclass.content()["topics"]]
        self.assertEqual(len(ids), len(set(ids)))


class MasterclassApiTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.app = create_app({"DATABASE_URL": f"sqlite:///{self.dir}/test.db", "TESTING": True, "FORCE_HTTPS": False,
                               "SESSION_COOKIE_SECURE": False, "BASE_URL": "http://localhost"})
        self.client = self.app.test_client()
        self.post("/api/auth/register", {"name": "Sam Lee", "email": "sam@school.org", "password": "password123"})

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def post(self, url, data=None):
        return self.client.post(url, json=data or {}, headers=ORIGIN)

    def test_needs_sign_in(self):
        self.post("/api/auth/logout")
        self.assertEqual(self.client.get("/api/masterclass").status_code, 401)
        self.assertEqual(self.post("/api/masterclass/progress", {"lesson": "basics", "step": 1}).status_code, 401)

    def test_progress_only_goes_up_and_completes(self):
        n = masterclass.total(masterclass.lessons()["basics"])
        r = self.post("/api/masterclass/progress", {"lesson": "basics", "step": 2})
        self.assertEqual(r.status_code, 200, r.json)
        self.assertEqual(r.json["progress"], {"step": 2, "total": n, "completed": False, "quiz_best": None, "quiz_total": 3})
        r = self.post("/api/masterclass/progress", {"lesson": "basics", "step": 1})
        self.assertEqual(r.json["progress"]["step"], 2)
        r = self.post("/api/masterclass/progress", {"lesson": "basics", "step": 999})
        self.assertEqual(r.json["progress"]["step"], n)
        self.assertTrue(r.json["progress"]["completed"])

        data = self.client.get("/api/masterclass").json
        self.assertTrue(data["progress"]["basics"]["completed"])
        self.assertEqual(data["summary"]["completed"], 1)
        self.assertEqual(data["summary"]["next"]["id"], masterclass.content()["lessons"][1]["id"])
        self.assertEqual(self.client.get("/api/dashboard").json["masterclass"]["completed"], 1)

    def test_topic_lessons_save_but_dont_count_toward_the_masterclass(self):
        lesson = "topic-percentages"
        n = masterclass.total(masterclass.lessons()[lesson])
        r = self.post("/api/masterclass/progress", {"lesson": lesson, "step": n})
        self.assertTrue(r.json["progress"]["completed"])
        self.assertEqual(self.post("/api/masterclass/quiz", {"lesson": lesson, "correct": 2}).json["progress"]["quiz_best"], 2)
        data = self.client.get("/api/masterclass").json
        self.assertTrue(data["progress"][lesson]["completed"])
        self.assertEqual(data["summary"]["completed"], 0)

    def test_quiz_keeps_the_best_score(self):
        r = self.post("/api/masterclass/quiz", {"lesson": "tilde", "correct": 2})
        self.assertEqual(r.status_code, 200, r.json)
        self.assertEqual((r.json["progress"]["quiz_best"], r.json["progress"]["quiz_total"]), (2, 3))
        self.assertEqual(self.post("/api/masterclass/quiz", {"lesson": "tilde", "correct": 1}).json["progress"]["quiz_best"], 2)
        self.assertEqual(self.post("/api/masterclass/quiz", {"lesson": "tilde", "correct": 3}).json["progress"]["quiz_best"], 3)
        self.assertEqual(self.client.get("/api/masterclass").json["progress"]["tilde"]["quiz_best"], 3)
        self.assertEqual(self.post("/api/masterclass/quiz", {"lesson": "tilde", "correct": 4}).status_code, 400)
        self.assertEqual(self.post("/api/masterclass/quiz", {"lesson": "choose", "correct": 1}).status_code, 404)

    def test_rejects_unknown_lessons_and_bad_steps(self):
        self.assertEqual(self.post("/api/masterclass/progress", {"lesson": "nope", "step": 1}).status_code, 404)
        self.assertEqual(self.post("/api/masterclass/progress", {"lesson": "basics", "step": "2"}).status_code, 400)
        self.assertEqual(self.post("/api/masterclass/progress", {"lesson": "basics", "step": True}).status_code, 400)

    def test_page_needs_sign_in(self):
        self.post("/api/auth/logout")
        r = self.client.get("/masterclass.html")
        self.assertEqual(r.status_code, 302)
        self.assertIn("/signin.html?next=/masterclass.html", r.headers["Location"])


if __name__ == "__main__":
    unittest.main()
