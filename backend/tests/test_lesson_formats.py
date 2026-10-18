"""Lesson formats and hands-on steps: every lesson plays differently, every answer key is right, the math in the
graphs checks out, and Desmos hacks opens first. Run from the backend folder: python -m unittest discover tests"""
import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path

from app.services import lessons, mathexpr

import shutil as _sh
import tempfile

from app import create_app

from test_practice import ORIGIN

KIT = Path(__file__).resolve().parents[2] / "website" / "src" / "lesson-kit.js"


def near(a, b):
    return a is not None and abs(a - b) < 1e-6


class LessonContentTest(unittest.TestCase):
    def test_no_two_lessons_play_the_same(self):
        seen_shape, seen_types = {}, {}
        for l in lessons.all_lessons():
            types = tuple(s["type"] for s in l["steps"])
            shape = (l["format"], types)
            self.assertNotIn(shape, seen_shape, f"{l['id']} plays like {seen_shape.get(shape)}")
            self.assertNotIn(types, seen_types, f"{l['id']} has the same steps as {seen_types.get(types)}")
            seen_shape[shape] = seen_types[types] = l["id"]
            hands_on = {"slider", "plot", "graph", "sort", "match", "line", "build", "grid", "flash"}
            self.assertTrue(hands_on & set(types), f"{l['id']} has no hands-on step")
        formats = {l["format"] for l in lessons.all_lessons()}
        self.assertEqual(formats, set(lessons.FORMATS))

    def test_format_details(self):
        for l in lessons.all_lessons():
            f, steps = l["format"], l["steps"]
            if f == "cold-open":
                self.assertTrue(steps[0].get("cold") and steps[-1].get("rematch"), l["id"])
            if f == "path":
                self.assertTrue(steps[0].get("gate"), l["id"])
                self.assertTrue(any(s.get("skip_if") == 0 for s in steps), l["id"])
            if f in ("story", "case", "teach"):
                self.assertTrue(l.get("intro"), l["id"])
            if f == "race":
                lanes = {s.get("lane") for s in steps}
                self.assertTrue({"hand", "desmos"} <= lanes, l["id"])
            if f == "timed":
                self.assertGreaterEqual(l.get("seconds", 0), 20, l["id"])
            for s in steps:
                if s.get("skip_if") is not None:
                    self.assertFalse(s.get("gate"), l["id"])

    def test_answer_keys_and_math(self):
        for l in lessons.all_lessons():
            for i, s in enumerate(l["steps"] + l["recall"]):
                tag, t = (l["id"], i, s["type"]), s["type"]
                self.assertTrue(lessons.right(s, lessons.key(s)), tag)
                self.assertTrue(s.get("why") or t == "recall", tag)
                if t == "slider":
                    p, a = s["param"], s["answer"]
                    self.assertTrue(p["min"] <= a <= p["max"], tag)
                    self.assertAlmostEqual((a - p["min"]) / p["step"], round((a - p["min"]) / p["step"]), 6, msg=tag)
                    self.assertNotEqual(p["start"], a, tag)
                    for x, y in s.get("points", []):
                        self.assertTrue(any(near(mathexpr.value(c, x, **{p["name"]: a}), y) for c in s["curves"]), tag)
                    self.assertTrue(s.get("curves") or s.get("dots") or s.get("pie"), tag)
                if t == "plot":
                    x, y = s["answer"]
                    self.assertTrue(s["window"]["x"][0] < x < s["window"]["x"][1] and s["window"]["y"][0] < y < s["window"]["y"][1], tag)
                    if not s.get("center"):
                        on = [c for c in s["curves"] if near(mathexpr.value(c, x), y)]
                        self.assertEqual(len(on), len(s["curves"]), tag)  # a crossing point is on every curve
                if t == "graph":
                    for x, y in s.get("points", []):
                        self.assertTrue(near(mathexpr.value(s["accept"][0], x), y), tag)
                    for f in s.get("fixed", []):
                        if not s.get("forbid"):  # with forbid, the point is to type the same graph a new way
                            self.assertFalse(mathexpr.same(s["accept"][0], f), tag)
                if t == "build":
                    for ans in s["answers"]:
                        self.assertTrue(all(0 <= k < len(s["tiles"]) for k in ans) and len(set(ans)) == len(ans), tag)
                if t == "grid":
                    self.assertEqual(sum(c.count("___") for r in s["rows"] for c in r), len(s["accept"]), tag)
                if t == "match":
                    self.assertEqual(len(set(s["right"])), len(s["right"]), tag)
                if t == "sort":
                    self.assertGreater(len({c["bucket"] for c in s["cards"]}), 1, tag)
                if t == "line":
                    self.assertTrue(s["min"] < s["answer"]["at"] < s["max"], tag)
            self.assertNotIn("—", json.dumps(l, ensure_ascii=False), l["id"])

    def test_grading_new_steps(self):
        slider = {"type": "slider", "answer": 1.2, "tol": 0.001}
        self.assertTrue(lessons.right(slider, 1.2004))
        self.assertFalse(lessons.right(slider, 1.25))
        self.assertFalse(lessons.right(slider, True))
        plot = {"type": "plot", "answer": [3, -4]}
        self.assertTrue(lessons.right(plot, [3, -4]))
        self.assertFalse(lessons.right(plot, [3, 4]))
        self.assertFalse(lessons.right(plot, "3,-4"))
        graph = {"type": "graph", "accept": ["(x-2)^2+3"]}
        for ok in ("y = (x - 2)^2 + 3", "x^2-4x+7", "x²−4x+7", "f(x)=(x−2)(x−2)+3"):
            self.assertTrue(lessons.right(graph, ok), ok)
        for bad in ("(x+2)^2+3", "x^2", "import os", "x" * 80, "(x-2", 5):
            self.assertFalse(lessons.right(graph, bad), bad)
        self.assertTrue(lessons.right({"type": "line", "answer": {"at": -4, "closed": False, "dir": "left"}},
                                      {"at": -4, "closed": False, "dir": "left"}))
        self.assertFalse(lessons.right({"type": "line", "answer": {"at": -4, "closed": False, "dir": "left"}},
                                       {"at": -4, "closed": True, "dir": "left"}))
        self.assertTrue(lessons.right({"type": "build", "answers": [[0, 1], [1, 0]]}, [1, 0]))
        self.assertTrue(lessons.right({"type": "grid", "accept": [["0.8", ".8"], ["40"]]}, [".80", "40"]))
        self.assertFalse(lessons.right({"type": "grid", "accept": [["0.8"], ["40"]]}, ["0.8"]))

    def test_path_skips(self):
        steps = [{"type": "predict", "answer": 1, "gate": True}, {"type": "predict", "answer": 0, "skip_if": 0},
                 {"type": "predict", "answer": 2}]
        self.assertEqual(lessons.grade(steps, [1, "skip", 2]), 3)
        self.assertEqual(lessons.grade(steps, [0, "skip", 2]), 1)  # can't skip after missing the gate
        self.assertEqual(lessons.grade(steps, [1, "skip", "skip"]), 2)  # only marked steps can be skipped

    def test_expression_reader(self):
        self.assertEqual(mathexpr.value("2x+3", 2), 7)
        self.assertAlmostEqual(mathexpr.value("100*b^x", 2, b=1.2), 144)
        self.assertIsNone(mathexpr.value("1/x", 0))
        self.assertIsNone(mathexpr.value("sqrt(x)", -4))
        self.assertTrue(mathexpr.same("2(x+1)", "2x+2"))
        self.assertTrue(mathexpr.same("sqrt(x^2)", "abs(x)"))
        self.assertFalse(mathexpr.same("x", "abs(x)"))
        with self.assertRaises(mathexpr.ExprError):
            mathexpr.parse("__import__('os')")

    @unittest.skipUnless(shutil.which("node"), "node isn't installed")
    def test_browser_reader_matches(self):
        """lesson-kit.js grades the same way, so the preview never disagrees with the server."""
        cases = []
        for l in lessons.all_lessons():
            for s in l["steps"] + l["recall"]:
                cases.append([s, lessons.key(s), True])
                if s["type"] == "graph":
                    cases.append([s, s["accept"][0] + "+1", False])
        cases += [[{"type": "graph", "accept": ["(x-2)^2+3"]}, "x²−4x+7", True], [{"type": "graph", "accept": ["x"]}, "abs(x)", False]]
        script = ("global.window = {}; require(%s); var K = window.GraphiteLessonKit;"
                  "var cases = JSON.parse(require('fs').readFileSync(0, 'utf8'));"
                  "process.stdout.write(JSON.stringify(cases.map(function (c) { return K.right(c[0], c[1]) === c[2]; })));"
                  % json.dumps(str(KIT)))
        out = json.loads(subprocess.run(["node", "-e", script], input=json.dumps(cases), capture_output=True, text=True, check=True).stdout)
        bad = [cases[i] for i, ok in enumerate(out) if not ok]
        self.assertEqual(bad, [])


SHOWN = ("title", "hook", "intro", "keys", "prompt", "why", "scene", "choices", "lines", "items", "show", "buckets", "left", "right",
         "cards", "text", "tiles", "head", "rows", "caption", "table", "steps", "recall", "readout")
MATH = re.compile(r"(?<!\\)\$((?:\\.|[^$\\])+)\$|`[^`]*`")
KATEX = Path(__file__).resolve().parents[2] / "website" / "src" / "vendor" / "katex" / "katex.min.js"


def shown_text(o, key=None):
    """Every string a student sees in a lesson."""
    if isinstance(o, str):
        if key in SHOWN or key is None:
            yield o
    elif isinstance(o, list):
        for x in o:
            yield from shown_text(x, key)
    elif isinstance(o, dict):
        for k, v in o.items():
            if k in SHOWN or (k == "answer" and isinstance(v, str)):
                yield from shown_text(v, k if k not in ("steps", "recall", "cards", "table") else None)


class LatexTest(unittest.TestCase):
    def test_all_math_is_latex(self):
        for l in lessons.all_lessons():
            self.assertTrue(l.get("tex"), l["id"])
            for t in shown_text(l):
                outside = MATH.sub(" ", t).replace("\\$", "")
                self.assertNotRegex(outside, r"[=+−×÷^²³√π≤≥°₁₂⁻~±$]", (l["id"], t))

    @unittest.skipUnless(shutil.which("node"), "node isn't installed")
    def test_every_formula_renders(self):
        spans = sorted({m.group(1) for l in lessons.all_lessons() for t in shown_text(l) for m in MATH.finditer(t) if m.group(1)})
        self.assertGreater(len(spans), 1000)
        js = ("const k = require(%s); const a = JSON.parse(require('fs').readFileSync(0, 'utf8')); const bad = [];"
              "for (const s of a) { try { k.renderToString(s.replace(/\\{=[^}]*\\}/g, '1').replace(/\\{[a-z]\\}/g, '1'), { throwOnError: true, strict: 'ignore' }); }"
              " catch (e) { bad.push([s, e.message]); } } process.stdout.write(JSON.stringify(bad));" % json.dumps(str(KATEX)))
        out = subprocess.run(["node", "-e", js], input=json.dumps(spans), capture_output=True, text=True, check=True).stdout
        self.assertEqual(json.loads(out), [])


class StartFirstTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.app = create_app({"DATABASE_URL": f"sqlite:///{self.dir}/test.db", "TESTING": True, "PLAN_LIMITS": False, "FORCE_HTTPS": False,
                               "SESSION_COOKIE_SECURE": False, "BASE_URL": "http://localhost"})
        self.client = self.app.test_client()
        self.post("/api/auth/register", {"name": "Sam Lee", "email": "sam@school.org", "password": "password123", "grade": 11})

    def tearDown(self):
        _sh.rmtree(self.dir, ignore_errors=True)

    def post(self, url, data=None):
        return self.client.post(url, json=data or {}, headers=ORIGIN)

    def test_desmos_hacks_opens_first(self):
        ov = self.client.get("/api/lessons").json
        self.assertEqual(ov["start_with"], lessons.START_LESSON)
        other = next(l["id"] for l in ov["lessons"] if l["id"] != lessons.START_LESSON)
        r = self.client.get(f"/api/lessons/{other}")
        self.assertEqual((r.status_code, r.json["code"]), (409, "start_first"))
        L = lessons.lesson(other)
        self.assertEqual(self.post(f"/api/lessons/{other}/complete", {"kind": "lesson", "answers": [lessons.key(s) for s in L["steps"]]}).status_code, 409)
        hacks = lessons.lesson(lessons.START_LESSON)
        self.assertEqual(self.client.get(f"/api/lessons/{lessons.START_LESSON}").status_code, 200)
        r = self.post(f"/api/lessons/{lessons.START_LESSON}/complete", {"kind": "lesson", "answers": [lessons.key(s) for s in hacks["steps"]]})
        self.assertEqual(r.json["score"], len(hacks["steps"]))
        self.assertIsNone(self.client.get("/api/lessons").json["start_with"])
        self.assertEqual(self.client.get(f"/api/lessons/{other}").status_code, 200)


if __name__ == "__main__":
    unittest.main()
