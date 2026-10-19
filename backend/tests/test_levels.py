"""Level up: sets that get harder level by level. Run from the backend folder: python -m unittest discover tests"""
from app.services import bank, levels

from test_practice import PracticeTest, right_answer, wrong_answer

DIFF = {"easy": 0, "medium": 1, "hard": 2}


class LevelsTest(PracticeTest):
    def level(self, track, n, status=201):
        r = self.post("/api/levels/start", {"track": track, "level": n})
        self.assertEqual(r.status_code, status, r.json)
        return r.json.get("session")

    def finish(self, session, right):
        """Answers `right` questions correctly and the rest wrong."""
        items = bank.all_items()
        answers = {str(i): (right_answer if i < right else wrong_answer)(items[q["id"]]) for i, q in enumerate(session["questions"])}
        r = self.post(f"/api/practice/sessions/{session['id']}/submit", {"answers": answers, "seconds_used": 300})
        self.assertEqual(r.status_code, 201, r.json)
        return r.json["result"]

    def overview(self):
        r = self.client.get("/api/levels")
        self.assertEqual(r.status_code, 200)
        return {t["key"]: t for t in r.json["tracks"]}

    def test_overview_starts_at_level_one(self):
        t = self.overview()
        self.assertEqual(list(t)[0], "mixed")
        # All of Math and each Math domain, then the same for Reading and Writing.
        self.assertEqual(len(t), 1 + len(bank.topics()) + 1 + len(bank.topics("rw")))
        self.assertEqual(list(t)[1 + len(bank.topics())], "rw-mixed")
        lv = t["algebra"]["levels"]
        self.assertEqual(len(lv), levels.LEVELS)
        self.assertEqual([x["status"] for x in lv[:2]], ["open", "locked"])
        self.assertEqual(lv[0]["tier"], "Warm-up")
        self.assertEqual(lv[-1]["tier"], "Top score")

    def test_levels_get_harder(self):
        avg = [sum(DIFF[k] * v for k, v in levels.mix(n).items()) / levels.SIZE for n in range(1, levels.LEVELS + 1)]
        self.assertEqual(avg, sorted(avg))
        self.assertLess(avg[0], 0.6)
        self.assertGreater(avg[-1], 1.6)
        items = bank.all_items()
        s = self.level("algebra", 1)
        self.assertEqual(len(s["questions"]), levels.SIZE)
        self.assertEqual(s["mode"], "quiz")
        self.assertTrue(all(items[q["id"]]["domain_key"] == "algebra" for q in s["questions"]))
        self.assertNotIn("hard", [items[q["id"]]["difficulty"] for q in s["questions"]])

    def test_passing_unlocks_the_next_level(self):
        self.level("algebra", 2, status=403)
        s = self.level("algebra", 1)
        res = self.finish(s, levels.PASS - 1)
        self.assertFalse(res["level"]["passed"])
        self.assertIsNone(res["level"]["next"])
        self.assertEqual(self.overview()["algebra"]["levels"][0]["best"], levels.PASS - 1)
        self.level("algebra", 2, status=403)

        res = self.finish(self.level("algebra", 1), levels.PASS)
        self.assertTrue(res["level"]["passed"])
        self.assertEqual(res["level"]["next"], 2)
        t = self.overview()["algebra"]
        self.assertEqual(t["unlocked"], 2)
        self.assertEqual([x["status"] for x in t["levels"][:3]], ["passed", "open", "locked"])
        self.assertEqual(t["levels"][0]["best"], levels.PASS)
        self.level("algebra", 2)
        # Tracks are separate.
        self.assertEqual(self.overview()["geometry-trig"]["unlocked"], 1)

    def test_unfinished_level_resumes_and_replay_has_new_questions(self):
        a = self.level("mixed", 1)
        self.assertEqual(self.level("mixed", 1)["id"], a["id"])
        self.assertEqual(self.overview()["mixed"]["levels"][0]["resume_id"], a["id"])
        self.finish(a, levels.SIZE)
        b = self.level("mixed", 1)
        self.assertNotEqual(b["id"], a["id"])
        self.assertFalse({q["id"] for q in a["questions"]} & {q["id"] for q in b["questions"]})

    def test_bad_requests(self):
        self.level("nope", 1, status=400)
        self.level("algebra", 0, status=400)
        self.level("algebra", levels.LEVELS + 1, status=400)
        self.level("algebra", "1", status=400)
        self.post("/api/auth/logout")
        self.assertEqual(self.client.get("/api/levels").status_code, 401)


del PracticeTest  # don't rerun the practice tests from this module
