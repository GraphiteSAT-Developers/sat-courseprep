"""Extra Desmos hacks in explanations: each one fits the question it's attached to."""
import json
import re
import unittest

from app.services import bank


def raw_items():
    return {it["id"]: it for it in map(json.loads, filter(str.strip, (bank.BANK_DIR / "items.jsonl").read_text().splitlines()))}


class HackLibraryTest(unittest.TestCase):
    def test_every_hack_is_used_and_sourced(self):
        used = {h["key"] for it in raw_items().values() for h, _ in bank.extra_hacks(it)}
        for h in bank.hacks():
            self.assertIn(h["key"], used, h["id"])
            self.assertTrue(h["sources"], h["id"])
            self.assertFalse(h["verified"], "mark a hack verified only after trying it in the College Board calculator")

    def test_at_most_two_and_never_repeating_the_main_technique(self):
        for it in raw_items().values():
            picks = bank.extra_hacks(it)
            self.assertLessEqual(len(picks), bank.MAX_HACKS)
            for hack, _ in picks:
                self.assertFalse(set(it.get("techniques", [])) & set(hack["match"].get("withoutTechniques", [])), it["id"])


class HackExamplesTest(unittest.TestCase):
    def setUp(self):
        self.items = raw_items()

    def example(self, item_id, key):
        return dict((h["key"], ex) for h, ex in bank.extra_hacks(self.items[item_id])).get(key)

    def test_equation_typed_as_written(self):
        self.assertEqual(self.example("sample-positive-root", "as-written"), {"lines": ["6x^2-x-2=0"]})
        self.assertEqual(self.example("adv-sqrt-extraneous-root", "as-written"), {"lines": ["\\sqrt{2x+11}=x-2"]})

    def test_regression_lists_the_points(self):
        ex = self.example("alg-slope-two-points", "regression-line")
        self.assertEqual(ex["lines"], ["y_1\\sim mx_1+b"])
        self.assertEqual(ex["note"], "Put $(2, 7)$ and $(6, -1)$ in the table.")

    def test_restriction_renames_the_variable(self):
        ex = self.example("alg-lf-calf-weight-shifted-input", "restrict")
        self.assertEqual(bank.keystrokes(ex["lines"][0]).replace(" ", ""), "{5<=x<=20}")
        self.assertIn("in place of $t$", ex["note"])

    def test_no_hack_where_it_would_mislead(self):
        for it in self.items.values():
            keys = {h["key"] for h, _ in bank.extra_hacks(it)}
            if "constant" in it["stem"]:
                self.assertFalse(keys & {"as-written", "rename", "key-points", "implicit"}, it["id"])
            if "rename" in keys:
                self.assertNotRegex(it["stem"], r"value of \$y\$")

    def test_explanation_shows_the_section(self):
        q = bank.all_items()["alg-slope-two-points"]
        self.assertIn('<section class="xp-sec xp-hacks"><h4>More Desmos hacks</h4>', q["explain_html"])
        self.assertIn('<code class="keys">y_1~mx_1+b</code>', q["explain_html"])
        self.assertIn("quick way to check your answer", q["explain_html"])
        plain = bank.all_items()["geo-cos-to-tan-nontriple"]["explain_html"]
        self.assertEqual("xp-hacks" in plain, bool(bank.extra_hacks(self.items["geo-cos-to-tan-nontriple"])))
        self.assertFalse(re.search(r"\$", q["explain_html"]))


if __name__ == "__main__":
    unittest.main()
