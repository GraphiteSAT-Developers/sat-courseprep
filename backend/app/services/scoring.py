"""The SAT score calculator: an estimated section score, 200 to 800, from the right answers on a test.

The digital SAT is scored with item response theory, so College Board publishes no fixed raw-to-scaled
chart. These curves follow the ranges score calculators report from Bluebook's practice tests: Math 44 of
44 is 800, 41 is about 740, 38 about 690, 35 about 640. The harder Module 2 opens the top of the scale;
after the easier Module 2 a section tops out near 590, as on the real test.

A full mock test (both modules) gets a score from its real route. A single module is projected: its
Module 1 score picks the route, and the student's accuracy at each difficulty is carried over to that
Module 2's mix of easy, medium and hard questions. A projection is less certain, so its range is wider.

No database access here, so the static preview's practice-local.js can mirror it exactly.
"""

SECTIONS = {"math": {"questions": 22, "route_at": 14}, "rw": {"questions": 27, "route_at": 17}}

# (right answers in both modules, section score) points; scores between points are read off the line.
CURVES = {
    ("math", "harder"): [(14, 430), (20, 480), (24, 510), (28, 540), (32, 590), (35, 640), (38, 690), (41, 740), (44, 800)],
    ("math", "easier"): [(0, 200), (6, 280), (12, 360), (18, 420), (24, 480), (30, 540), (35, 590)],
    ("rw", "harder"): [(17, 430), (25, 500), (30, 540), (35, 580), (40, 620), (45, 670), (50, 730), (52, 760), (54, 800)],
    ("rw", "easier"): [(0, 200), (8, 280), (16, 360), (24, 430), (32, 500), (38, 550), (43, 590)],
}

# Module 2's difficulty mix after each route (services/mock.py builds modules from this too).
MIX = {
    "m1": {"easy": 7, "medium": 8, "hard": 7},
    "harder": {"easy": 3, "medium": 8, "hard": 11},
    "easier": {"easy": 10, "medium": 9, "hard": 3},
}
# Plus or minus, in points: one test is a sample. The score check (services/scorecheck.py) has only 10
# questions a section; its 1600 total adds two sections' errors, which partly cancel out.
SPREAD = {"full": 30, "projected": 50, "check": 70, "check_total": 100}
PRIOR = 2  # questions' worth of the overall accuracy blended into each difficulty's accuracy


def section_key(section):
    return "rw" if section in ("rw", "Reading and Writing") else "math"


def section_score(section, route, raw):
    """The estimated section score for raw right answers out of both modules, rounded to 10."""
    points = CURVES[(section_key(section), "harder" if route == "harder" else "easier")]
    if raw <= points[0][0]:
        score = points[0][1] if route == "harder" else 200
    elif raw >= points[-1][0]:
        score = points[-1][1]
    else:
        for (x0, y0), (x1, y1) in zip(points, points[1:]):
            if x0 <= raw <= x1:
                score = y0 + (y1 - y0) * (raw - x0) / (x1 - x0)
                break
    return int(round(score / 10.0) * 10)


def _result(section, route, raw, kind):
    score = section_score(section, route, raw)
    spread = SPREAD[kind]
    return {"score": score, "low": max(200, score - spread), "high": min(800, score + spread),
            "section": section_key(section), "route": route, "projected": kind != "full"}


def full(section, route, raw):
    """A mock test's estimate: both modules taken, on the route the student really got."""
    return _result(section, route, raw, "full")


def split(n, mix):
    """n questions in the proportions of mix, summing exactly to n."""
    total = sum(mix.values())
    raw = {d: n * c / total for d, c in mix.items()}
    out = {d: int(v) for d, v in raw.items()}
    for d in sorted(raw, key=lambda d: raw[d] - out[d], reverse=True)[:n - sum(out.values())]:
        out[d] += 1
    return out


def project(section, questions, kind="projected"):
    """One module's graded questions projected to a full section: the route its score earns, then
    Module 2 answered at the student's own accuracy for each difficulty. None for an empty test.
    kind picks the range: "projected" for a practice module, "check" for the score check's 10 questions."""
    key = section_key(section)
    per, route_at = SECTIONS[key]["questions"], SECTIONS[key]["route_at"]
    if not questions:
        return None
    right = sum(1 for q in questions if q.get("correct"))
    overall = right / len(questions)
    m1 = round(overall * per)  # a short or long module counts as a full one
    route = "harder" if m1 >= route_at else "easier"
    by = {}
    for q in questions:
        d = by.setdefault(q.get("difficulty") or "", [0, 0])
        d[0] += 1 if q.get("correct") else 0
        d[1] += 1
    m2 = 0.0
    for difficulty, n in split(per, MIX[route]).items():
        r, total = by.get(difficulty, (0, 0))
        m2 += n * (r + PRIOR * overall) / (total + PRIOR)
    out = _result(key, route, m1 + round(m2), kind)
    out["module2_right"] = round(m2)
    return out
