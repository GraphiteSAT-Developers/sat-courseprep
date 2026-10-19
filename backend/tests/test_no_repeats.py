"""No question repeats across activities, and no duplicate questions in the bank.
Run from the backend folder: python -m unittest discover tests"""
import json
import re
import unittest
from datetime import date

from app.db import query
from app.services import bank, mock, practice, speed

from test_practice import PracticeTest, right_answer


def shingles(*parts):
    """Every run of three words or numbers in the text, for comparing two questions."""
    words = re.findall(r"[a-z]+|\d+(?:\.\d+)?|[=+\-^/<>]", " ".join(parts).lower())
    return {tuple(words[i:i + 3]) for i in range(max(1, len(words) - 2))}


def overlap(a, b):
    return len(a & b) / len(a | b) if a | b else 0


class NoRepeatsTest(PracticeTest):
    def uid(self):
        with self.app.app_context():
            return query("SELECT id FROM users WHERE email = ?", ("sam@school.org",), one=True)["id"]

    def speed_round(self):
        run = self.post("/api/speed/start").json["run"]
        items = bank.all_items()
        for i, q in enumerate(run["questions"]):
            self.post(f"/api/speed/runs/{run['id']}/answer", {"index": i, "answer": right_answer(items[q["id"]])})
        return [q["id"] for q in run["questions"]]

    def test_speed_round_questions_go_on_the_done_list(self):
        ids = self.speed_round()
        with self.app.app_context():
            self.assertTrue(set(ids) <= practice.seen_ids(self.uid()))
            m1 = mock.build_module(self.uid(), mock.MIX["m1"])
        self.assertFalse(set(ids) & set(m1))

    def test_practice_speed_rounds_are_new_questions(self):
        first = self.speed_round()
        second = self.speed_round()
        self.assertEqual(len(second), speed.SIZE)
        self.assertFalse(set(first) & set(second))

    def test_ranked_round_swaps_questions_already_done_elsewhere(self):
        day = date.today().isoformat()
        with self.app.app_context():
            shared = speed.day_items(day)
            practice.mark_seen(self.uid(), shared[:3])  # done earlier in a practice set
        run = self.post("/api/speed/start").json["run"]
        ids = [q["id"] for q in run["questions"]]
        self.assertTrue(run["ranked"])
        self.assertEqual(ids[3:], shared[3:])  # the rest of the day's questions are the same as everyone's
        items = bank.all_items()
        for old, new in zip(shared[:3], ids[:3]):
            self.assertNotIn(new, shared)
            self.assertEqual((items[new]["domain_key"], items[new]["difficulty"]), (items[old]["domain_key"], items[old]["difficulty"]))

    def test_level_and_practice_questions_stay_out_of_a_mock(self):
        level = self.post("/api/levels/start", {"track": "mixed", "level": 1}).json["session"]
        self.answer_all(level)
        topic = self.start(mode="topic", domain="algebra", count=20)
        self.answer_all(topic)
        done = {q["id"] for q in level["questions"] + topic["questions"]}
        with self.app.app_context():
            m = mock.create(self.uid())
            m1 = json.loads(practice.get(self.uid(), m["m1_session"])["item_ids"])
        self.assertFalse(done & set(m1))
        test = self.start(mode="test")
        self.assertFalse((done | set(m1)) & {q["id"] for q in test["questions"]})

    def test_bank_has_no_duplicate_questions(self):
        """No two questions match after normalizing, or share most of their wording and numbers,
        or reuse a Reading and Writing passage."""
        raw = {}
        with open(bank.BANK_DIR / "items.jsonl") as f:
            for line in f:
                q = json.loads(line)
                raw[q["id"]] = q
        exact = {}
        for q in raw.values():
            key = re.sub(r"\s+", " ", json.dumps([q.get("passage"), q["stem"], q.get("choices")]).lower())
            self.assertNotIn(key, exact, f"{q['id']} repeats {exact.get(key)}")
            exact[key] = q["id"]
        full = {i: shingles(json.dumps(q.get("passage") or ""), q["stem"], json.dumps(q.get("choices") or "")) for i, q in raw.items()}
        passages = {i: shingles(json.dumps(q["passage"])) for i, q in raw.items() if q.get("passage")}
        ids = sorted(raw)
        for n, a in enumerate(ids):
            for b in ids[n + 1:]:
                if raw[a].get("section") != raw[b].get("section"):
                    continue
                self.assertLess(overlap(full[a], full[b]), 0.75, f"{a} and {b} are near duplicates")
                if a in passages and b in passages:
                    self.assertLess(overlap(passages[a], passages[b]), 0.6, f"{a} and {b} share a passage")


def load_tests(loader, tests, pattern):
    """Only this file's tests: the practice tests it builds on already run from test_practice.py."""
    return unittest.TestSuite(NoRepeatsTest(name) for name in loader.getTestCaseNames(NoRepeatsTest)
                              if name in NoRepeatsTest.__dict__)
