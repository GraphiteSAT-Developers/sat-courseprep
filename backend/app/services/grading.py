"""Grades a submitted practice test on the server, so answers never reach the browser early."""
import re

from .content import LETTERS

SPR_PATTERN = re.compile(r"^-?(\d+\.?\d*|\.\d+|\d+/\d+)$")


def spr_value(raw):
    """Turns a typed answer like '7/2', '-3.5' or '.6' into a number. Returns None if it isn't one."""
    if raw is None:
        return None
    text = re.sub(r"\s+", "", str(raw))
    if not text or not SPR_PATTERN.match(text):
        return None
    neg = text.startswith("-")
    if "/" in text:
        top, bottom = text.lstrip("-").split("/")
        if float(bottom) == 0:
            return None
        value = float(top) / float(bottom)
        return -value if neg else value
    return float(text)


def clean_answers(raw, test):
    """Keeps only well-formed answers: {question index: choice index or typed text}."""
    answers = {}
    if not isinstance(raw, dict):
        return answers
    for key, value in raw.items():
        try:
            i = int(key)
        except (TypeError, ValueError):
            continue
        if not 0 <= i < len(test["questions"]) or value is None or value == "":
            continue
        q = test["questions"][i]
        if q["type"] == "mc":
            if isinstance(value, int) and not isinstance(value, bool) and 0 <= value < len(q["choices"]):
                answers[i] = value
        else:
            text = re.sub(r"\s+", "", str(value))[:6]
            if text:
                answers[i] = text
    return answers


def is_correct(q, answer):
    if answer is None:
        return False
    if q["type"] == "mc":
        return answer == q["answer"]
    value = spr_value(answer)
    return value is not None and abs(value - q["answer"]) < 1e-9


def display_answer(q, answer):
    if answer is None:
        return None
    return LETTERS[answer] if q["type"] == "mc" else str(answer)


def correct_display(q):
    if q["type"] == "mc":
        return LETTERS[q["answer"]]
    value = q["answer"]
    return str(int(value)) if float(value).is_integer() else str(value)


def grade(test, answers):
    """Returns the full result: totals, per-domain counts and every question with its explanation."""
    questions, by_domain, correct = [], {}, 0
    mc = {"right": 0, "total": 0}
    spr = {"right": 0, "total": 0}
    for i, q in enumerate(test["questions"]):
        ans = answers.get(i)
        ok = is_correct(q, ans)
        correct += ok
        bucket = mc if q["type"] == "mc" else spr
        bucket["total"] += 1
        bucket["right"] += ok
        d = by_domain.setdefault(q["domain"], {"domain": q["domain"], "right": 0, "total": 0})
        d["total"] += 1
        d["right"] += ok
        item = {
            "index": i, "type": q["type"], "domain": q["domain"], "skill": q.get("skill"),
            "stem": q["stem"], "correct": ok, "answered": ans is not None,
            "your_answer": display_answer(q, ans), "answer": correct_display(q),
            "explain": q.get("explain"), "calc": q.get("calc"),
        }
        if q["type"] == "mc":
            item["choices"] = q["choices"]
            item["answer_index"] = q["answer"]
        questions.append(item)
    return {
        "test_id": test["id"], "correct": correct, "total": len(test["questions"]),
        "multiple_choice": mc, "student_produced": spr,
        "by_domain": list(by_domain.values()), "questions": questions,
    }
