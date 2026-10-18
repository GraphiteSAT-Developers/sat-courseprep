"""The lesson library: every SAT Math skill, the memory lessons and the Desmos course. Run: python -m unittest discover tests"""
import json
import unittest
from collections import Counter

from app.services import bank, lessons


class LessonLibraryTest(unittest.TestCase):
    def test_every_sat_math_skill_has_lessons(self):
        have = Counter((l["domain"], l["skill"]) for l in lessons.all_lessons())
        for d in bank.topics():
            for s in d["skills"]:
                self.assertGreaterEqual(have[(d["key"], s["key"])], 1, f"{d['key']}/{s['key']} has no lesson")

    def test_memory_and_desmos_groups(self):
        by = Counter(l["domain"] for l in lessons.all_lessons())
        self.assertGreaterEqual(by["memory"], 4)
        self.assertGreaterEqual(by["desmos"], 13)
        skills = {l["skill"] for l in lessons.all_lessons() if l["domain"] == "memory"}
        self.assertTrue({"active-recall", "memory-palace", "storytelling"} <= skills)
        # The Desmos course shows keystrokes, and never claims a practice skill that isn't in the bank.
        desmos = [l for l in lessons.all_lessons() if l["domain"] == "desmos"]
        self.assertTrue(any(s.get("desmos") for l in desmos for s in l["steps"]))
        names = lessons.topic_names()
        self.assertEqual(names["desmos"], "The Desmos course")
        self.assertEqual(names["memory/memory-palace"], "Memory palace")

    def test_order_and_shape(self):
        ls = lessons.all_lessons()
        self.assertEqual(ls[0]["domain"], "memory")  # how to learn comes first
        self.assertEqual(len({l["id"] for l in ls}), len(ls))
        for l in ls:
            self.assertEqual(len(l["recall"]), 3, l["id"])
            self.assertGreaterEqual(len(l["steps"]), 5, l["id"])
            for s in l["steps"] + l["recall"]:
                if s["type"] == "order":
                    self.assertGreaterEqual(len(s["items"]), 3, l["id"])
                if s["type"] == "predict":
                    self.assertEqual(len(set(s["choices"])), len(s["choices"]), (l["id"], s["prompt"]))
            text = json.dumps(l, ensure_ascii=False)
            self.assertNotIn("—", text, l["id"])  # no em dashes


if __name__ == "__main__":
    unittest.main()
