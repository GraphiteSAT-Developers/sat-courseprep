"""Reading and Writing lessons. Run from the backend folder: python -m unittest discover tests"""
import shutil
import tempfile
import unittest

from app import create_app
from app.services import lessons


class LessonsTest(unittest.TestCase):
    def test_every_skill_has_one_lesson(self):
        skills = {(s["domain"], s["name"]) for s in lessons.skills()["skills"]}
        taught = [(l["domain"], l["skill"]) for l in lessons.lessons() if l["domain"]]
        self.assertEqual(sorted(taught), sorted(skills))

    def test_overview_comes_first_then_test_order(self):
        order = lessons.skills()["format"]["domainOrder"]
        items = lessons.lessons()
        self.assertIsNone(items[0]["domain"])
        domains = [l["domain"] for l in items[1:]]
        self.assertEqual(domains, sorted(domains, key=order.index))

    def test_examples_explain_every_choice(self):
        for l in lessons.lessons():
            if l["domain"]:
                self.assertEqual(len(l["example"]["why"]), 4, l["id"])
                self.assertEqual(len(l["tryIt"]), 2, l["id"])

    def test_page_html_has_every_lesson(self):
        page = lessons.page_html()
        for l in lessons.lessons():
            self.assertIn(f'id="{l["id"]}"', page)
            self.assertIn(f'href="#{l["id"]}"', page)


class LessonsPageTest(unittest.TestCase):
    def test_needs_sign_in(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        app = create_app({"DATABASE_URL": f"sqlite:///{tmp}/test.db", "TESTING": True, "FORCE_HTTPS": False})
        r = app.test_client().get("/lessons.html")
        self.assertEqual(r.status_code, 302)
        self.assertIn("/signin.html?next=/lessons.html", r.headers["Location"])


if __name__ == "__main__":
    unittest.main()
