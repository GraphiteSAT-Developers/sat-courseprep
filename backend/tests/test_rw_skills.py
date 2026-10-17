"""The Reading and Writing skill list. Run from the backend folder: python -m unittest discover tests"""
import json
import unittest

from app.services import bank, diagnostic

RW = json.loads((bank.BANK_DIR / "rw-skills.json").read_text())


class RwSkillsTest(unittest.TestCase):
    def test_domains_match_the_diagnostic(self):
        self.assertEqual(set(RW["domains"].values()), set(diagnostic.RW_DOMAINS))
        self.assertEqual(set(RW["format"]["domainOrder"]), set(RW["domains"]))

    def test_every_skill_has_a_known_domain_and_testing_points(self):
        for s in RW["skills"]:
            self.assertIn(s["domain"], RW["domains"], s["name"])
            self.assertTrue(s["testingPoints"], s["name"])

    def test_diagnostic_skills_are_listed(self):
        listed = {(RW["domains"][s["domain"]], s["name"]) for s in RW["skills"]}
        for q in diagnostic.rw_items().values():
            self.assertIn((q["domain"], q["skill"]), listed, q["id"])

    def test_distribution_fits_a_54_question_test(self):
        dist = RW["questionDistribution"]
        self.assertAlmostEqual(sum(d["share"] for d in dist.values()), 1.0)
        self.assertLessEqual(sum(d["min"] for d in dist.values()), 54)
        self.assertGreaterEqual(sum(d["max"] for d in dist.values()), 54)


if __name__ == "__main__":
    unittest.main()
