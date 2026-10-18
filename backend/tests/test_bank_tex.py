"""Practice questions: every formula is LaTeX that KaTeX can typeset, and the exam page keeps its styles."""
import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path

from app.services import bank

ROOT = Path(__file__).resolve().parents[2]
KATEX = ROOT / "website" / "src" / "vendor" / "katex" / "katex.min.js"
MATH = re.compile(r"(?<!\\)\$([^$]*)\$")


def raw_items():
    return [json.loads(line) for line in (bank.BANK_DIR / "items.jsonl").read_text().splitlines() if line.strip()]


def shown_text():
    """Every piece of bank text a student reads, as (id, text)."""
    out = []
    for it in raw_items():
        out.append((it["id"], it["stem"]))
        out += [(it["id"], c) for c in it.get("choices") or []]
        if it.get("byHand"):
            out.append((it["id"], it["byHand"]))
        if (it.get("desmos") or {}).get("read"):
            out.append((it["id"], it["desmos"]["read"]))
    _, techniques = bank.meta()
    for t in techniques.values():
        out.append((t["id"], t["summary"]))
        out += [(t["id"], p) for p in t.get("pitfalls", [])]
    return out


class BankLatexTest(unittest.TestCase):
    def test_math_is_latex(self):
        for id_, text in shown_text():
            outside = MATH.sub(" ", re.sub(r"`[^`]*`", " ", text))
            # plain-text math (x^2, sqrt(...), 7 = 3 + 4, <=, √) means a formula never became LaTeX
            self.assertNotRegex(outside, r"\^|√|≤|≥|≠|π|\bsqrt\(|<=|>=|\\frac|\d ?[=+×÷] ?\d", (id_, text))

    def test_rendered_html_carries_tex(self):
        q = bank.all_items()["geo-cos-to-tan-nontriple"]
        self.assertIn('data-tex="\\cos P = \\frac{3}{7}"', q["stem"])
        self.assertIn('data-tex="\\frac{2\\sqrt{10}}{3}"', q["explain_html"])
        self.assertNotIn("$", q["explain_html"])

    @unittest.skipUnless(shutil.which("node"), "node isn't installed")
    def test_every_formula_renders(self):
        spans = sorted({m.group(1) for _, t in shown_text() for m in MATH.finditer(t)} |
                       {line for it in raw_items() for line in (it.get("desmos") or {}).get("lines", [])})
        self.assertGreater(len(spans), 3000)
        js = ("const k = require(%s); const a = JSON.parse(require('fs').readFileSync(0, 'utf8')); const bad = [];"
              "for (const s of a) { try { k.renderToString(s, { throwOnError: true, strict: 'ignore' }); }"
              " catch (e) { bad.push([s, e.message]); } } process.stdout.write(JSON.stringify(bad));" % json.dumps(str(KATEX)))
        out = subprocess.run(["node", "-e", js], input=json.dumps(spans), capture_output=True, text=True, check=True).stdout
        self.assertEqual(json.loads(out), [])


class ExamStylesTest(unittest.TestCase):
    def test_exam_page_rules_exist(self):
        css = (ROOT / "website" / "src" / "site.css").read_text()
        for rule in (".q-stem {", ".mc-choice {", ".mc-letter {", ".q-head {", ".exam-bottom {", ".res-item summary {", ".frac {"):
            self.assertIn("\n" + rule, css, rule)

    def test_question_pages_load_katex(self):
        for page in ("practice-test", "speed", "plan"):
            head = (ROOT / "website" / "src" / "pages" / f"{page}.html").read_text().split("\n", 1)[0]
            self.assertIn('"katex": true', head, page)


if __name__ == "__main__":
    unittest.main()
