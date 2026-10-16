"""Practice tests, loaded from app/content/tests/*.json.

To add a test, drop a new JSON file in that folder with the same shape as
pt4-math-m1.json. It shows up in /api/tests automatically.
"""
import json
from functools import lru_cache
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent.parent / "content" / "tests"

MATH_DOMAINS = ["Algebra", "Advanced Math", "Problem-Solving and Data Analysis", "Geometry and Trigonometry"]
RW_DOMAINS = ["Information and Ideas", "Craft and Structure", "Expression of Ideas", "Standard English Conventions"]
LETTERS = "ABCD"


@lru_cache(maxsize=None)
def all_tests():
    tests = {}
    for path in sorted(TESTS_DIR.glob("*.json")):
        data = json.loads(path.read_text())
        tests[data["id"]] = data
    return tests


def get_test(test_id):
    return all_tests().get(test_id)


def public_test(test):
    """The test as the student sees it: no answers, explanations or calculator tips."""
    return {
        "id": test["id"], "title": test["title"], "name": test.get("name"), "minutes": test["minutes"],
        "questions": [
            {k: q[k] for k in ("domain", "type", "stem", "choices") if k in q}
            for q in test["questions"]
        ],
    }


def summary(test):
    return {"id": test["id"], "title": test["title"], "name": test.get("name"), "minutes": test["minutes"],
            "questions": len(test["questions"])}
