"""Reading and Writing: the question bank, practice sets, mock tests, levels and speed rounds, and the
done-list cookies for both sections. Run from the backend folder: python -m unittest discover tests"""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path

from app import create_app
from app.services import bank, donelist

ORIGIN = {"Origin": "http://localhost"}
BACKEND = Path(__file__).resolve().parent.parent


class BankTest(unittest.TestCase):
    def test_compiled_bank_matches_sources(self):
        r = subprocess.run([sys.executable, str(BACKEND / "compile_rw.py"), "--check"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_five_hundred_questions_cover_every_skill(self):
        rw = [q for q in bank.all_items().values() if q["section"] == "rw"]
        self.assertEqual(len(rw), 500)
        skills = Counter(q["skill"] for q in rw)
        self.assertEqual(set(skills), {s["name"] for s in bank.rw_meta()["skills"]})
        for name, n in skills.items():
            self.assertGreaterEqual(n, 30, name)
        domains = Counter(q["domain_key"] for q in rw)
        self.assertEqual(set(domains), set(bank.rw_meta()["domains"]))
        levels = Counter(q["difficulty"] for q in rw)
        for lv in ("easy", "medium", "hard"):
            self.assertGreater(levels[lv], 120, lv)
        answers = Counter(q["answer"] for q in rw)
        for k in range(4):
            self.assertGreater(answers[k], 100)  # right answers spread across A to D

    def test_questions_render(self):
        for q in bank.all_items().values():
            if q["section"] != "rw":
                continue
            self.assertEqual(q["type"], "mc")
            self.assertEqual(len(q["choices"]), 4)
            self.assertIn(q["prompt"], q["stem"])
            self.assertNotIn("[u]", q["stem"])
            self.assertIn("Strategy", q["explain_html"])
            if q["skill_key"] == "command-of-evidence-quantitative":
                self.assertRegex(q["passage"], r"rw-(table|graph)")
            if q["skill_key"] == "cross-text-connections":
                self.assertIn("Text 2", q["passage"])

    def test_module_mix_is_a_real_module(self):
        mix = bank.rw_module_mix()
        self.assertEqual(sum(mix.values()), 27)

    def test_cookie_round_trip(self):
        ids = ["rw-wic-001", "rw-bnd-070", "rw-rs-050"]
        value = donelist.encode(7, "rw", ids)
        self.assertEqual(donelist.decode(value, 7, "rw"), set(ids))
        self.assertEqual(donelist.decode(value, 8, "rw"), set())  # another student's cookie
        self.assertEqual(donelist.decode("garbage", 7, "rw"), set())
        self.assertLess(len(donelist.encode(7, "math", list(bank.pool(section="math")))), 200)


class RWRoutesTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.app = create_app({"DATABASE_URL": f"sqlite:///{self.dir}/test.db", "TESTING": True, "PLAN_LIMITS": False, "FORCE_HTTPS": False,
                               "SESSION_COOKIE_SECURE": False, "BASE_URL": "http://localhost"})
        self.client = self.app.test_client()
        r = self.post("/api/auth/register", {"name": "Ana Ruiz", "email": "ana@school.org", "password": "password123",
                                             "grade": 11, "test_date": "2030-12-07", "target_score": 1450})
        self.uid = r.json["user"]["id"]

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def post(self, url, data=None):
        return self.client.post(url, json=data or {}, headers=ORIGIN)

    def get(self, url):
        return self.client.get(url, headers=ORIGIN)

    def cookie(self, section):
        c = self.client.get_cookie(donelist.NAMES[section])
        return donelist.decode(c.value if c else "", self.uid, section)

    def test_overview_by_section(self):
        r = self.get("/api/practice?section=rw")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json["total"], 500)
        self.assertEqual([d["name"] for d in r.json["domains"]],
                         ["Craft and Structure", "Information and Ideas", "Standard English Conventions", "Expression of Ideas"])
        self.assertEqual(r.json["test"], {"questions": 27, "minutes": 32})
        self.assertEqual(self.get("/api/practice").json["total"], 1000)
        self.assertEqual(self.get("/api/practice?section=french").status_code, 400)

    def test_rw_module_matches_the_real_test(self):
        r = self.post("/api/practice/sessions", {"mode": "test", "section": "rw"})
        self.assertEqual(r.status_code, 201, r.json)
        s = r.json["session"]
        self.assertEqual(len(s["questions"]), 27)
        self.assertEqual(s["minutes"], 32)
        self.assertTrue(all(q["section"] == "rw" and q["passage"] for q in s["questions"]))
        self.assertNotIn("answer", s["questions"][0])
        order = list(bank.rw_module_mix())
        keys = [order.index(bank.slug(q["skill"])) for q in s["questions"]]
        self.assertEqual(keys, sorted(keys))  # grouped by question type, like Bluebook

    def test_topic_practice_marks_done_and_sets_cookie(self):
        r = self.post("/api/practice/sessions", {"mode": "topic", "domain": "conventions", "skill": "boundaries", "count": 5})
        self.assertEqual(r.status_code, 201, r.json)
        s = r.json["session"]
        q = bank.all_items()[s["questions"][0]["id"]]
        r = self.post(f"/api/practice/sessions/{s['id']}/check", {"index": 0, "answer": q["answer"]})
        self.assertEqual(r.status_code, 200, r.json)
        self.assertTrue(r.json["question"]["correct"])
        self.assertEqual(self.cookie("rw"), {q["id"]})
        self.assertEqual(self.cookie("math"), set())

    def test_no_repeats_then_start_over(self):
        # 70 Boundaries questions: four sets of 20 use them all, and the fourth is the 10 left.
        seen = []
        for _ in range(4):
            s = self.post("/api/practice/sessions", {"mode": "topic", "domain": "conventions", "skill": "boundaries", "count": 20}).json["session"]
            ids = [q["id"] for q in s["questions"]]
            self.assertFalse(set(ids) & set(seen))
            seen += ids
            answers = {str(i): 0 for i in range(len(ids))}
            self.post(f"/api/practice/sessions/{s['id']}/submit", {"answers": answers, "seconds_used": 60})
        self.assertEqual(len(seen), 70)
        self.assertEqual(len(self.cookie("rw")), 70)
        # Every question in the topic is done: the list clears and the topic starts over.
        s = self.post("/api/practice/sessions", {"mode": "topic", "domain": "conventions", "skill": "boundaries", "count": 5}).json["session"]
        self.assertEqual(len(s["questions"]), 5)
        self.assertEqual(self.cookie("rw"), set())

    def test_cookie_from_the_browser_counts_as_done(self):
        pool = bank.pool(domain="expression-ideas", skill="transitions")
        done = pool[:45]
        self.client.set_cookie(donelist.NAMES["rw"], donelist.encode(self.uid, "rw", done))
        s = self.post("/api/practice/sessions", {"mode": "topic", "domain": "expression-ideas", "skill": "transitions", "count": 20}).json["session"]
        self.assertEqual({q["id"] for q in s["questions"]}, set(pool[45:]))
        self.assertEqual(self.cookie("rw"), set(done))

    def test_math_cookie_too(self):
        s = self.post("/api/practice/sessions", {"mode": "topic", "domain": "algebra", "count": 5}).json["session"]
        q = bank.all_items()[s["questions"][0]["id"]]
        answer = q["answer"] if q["type"] == "mc" else "1"
        self.post(f"/api/practice/sessions/{s['id']}/check", {"index": 0, "answer": answer})
        self.assertEqual(self.cookie("math"), {q["id"]})

    def test_rw_mock_test(self):
        r = self.post("/api/mock-tests", {"section": "rw", "with_break": False})
        self.assertEqual(r.status_code, 201, r.json)
        m = r.json["mock"]
        s1 = self.get(f"/api/practice/sessions/{m['m1_session']}").json["session"]
        self.assertEqual(s1["title"], "Reading and Writing: Module 1")
        self.assertEqual(len(s1["questions"]), 27)
        items = bank.all_items()
        answers = {str(i): items[q["id"]]["answer"] for i, q in enumerate(s1["questions"])}
        r = self.post(f"/api/practice/sessions/{s1['id']}/submit", {"answers": answers, "seconds_used": 900})
        self.assertEqual(r.status_code, 201, r.json)
        s2_id = r.json["result"]["mock"]["next_session"]
        s2 = self.get(f"/api/practice/sessions/{s2_id}").json["session"]
        self.assertEqual(len(s2["questions"]), 27)
        self.assertFalse({q["id"] for q in s1["questions"]} & {q["id"] for q in s2["questions"]})
        answers = {str(i): items[q["id"]]["answer"] for i, q in enumerate(s2["questions"])}
        r = self.post(f"/api/practice/sessions/{s2_id}/submit", {"answers": answers, "seconds_used": 900})
        res = r.json["result"]
        self.assertEqual(res["total"], 54)
        self.assertEqual(res["route"], "harder")
        self.assertEqual(res["score"], 800)
        self.assertEqual(res["title"], "Reading and Writing mock test")
        self.assertEqual(len(self.cookie("rw")), 54)

    def test_rw_levels(self):
        r = self.get("/api/levels")
        keys = {t["key"]: t for t in r.json["tracks"]}
        self.assertIn("rw-mixed", keys)
        self.assertEqual(keys["rw-mixed"]["section"], "rw")
        r = self.post("/api/levels/start", {"track": "rw-mixed", "level": 1})
        self.assertEqual(r.status_code, 201, r.json)
        self.assertTrue(all(q["section"] == "rw" for q in r.json["session"]["questions"]))

    def test_rw_speed_round(self):
        r = self.post("/api/speed/start", {"section": "rw"})
        self.assertEqual(r.status_code, 201, r.json)
        run = r.json["run"]
        self.assertEqual(run["section"], "rw")
        self.assertTrue(run["ranked"])
        self.assertTrue(all(q["section"] == "rw" for q in run["questions"]))
        m = self.post("/api/speed/start", {"section": "math"}).json["run"]
        self.assertTrue(m["ranked"])  # each section has its own ranked run each day
        self.assertTrue(all(q["section"] == "math" for q in m["questions"]))
        self.assertEqual(self.get("/api/speed?section=rw").json["section"], "rw")
        board = self.get("/api/speed/board?scope=nation&section=rw").json
        self.assertEqual(board["section"], "rw")

    def test_home_sample_is_math(self):
        for _ in range(10):
            q = self.get("/api/sample").json["question"]
            self.assertEqual(q["section"], "math")


if __name__ == "__main__":
    unittest.main()
