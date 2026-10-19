"""Builds a week-by-week study plan from the diagnostic and the student's test date.

How it works:
- Every Math skill gets an estimate: the diagnostic score for the skills it tested, blended
  with the domain's score; untested skills take their domain's score.
- Each study week focuses on the two skills with the highest priority. Weak skills start with
  high priority and regain it quickly, so they come back often (spaced practice); strong
  skills still come around, less often. Each week also re-tests one skill from earlier weeks.
- Difficulty ramps with time: early weeks are mostly easy and medium, the last weeks mostly
  hard. Where the ramp starts and ends depends on the diagnostic level, so a strong student
  starts harder. Quizzes also nudge up or down from the student's recent quiz scores
  (services/practice.py, adjusted_mix).
- Practice tests come every other week once the foundation phase is over, and every week at the end.
- With a test date, the last week is test week: a light review quiz and test-day prep.

website/src/practice-local.js has a JavaScript copy of this for the offline preview. Keep them in step.
"""
from datetime import date, timedelta

from . import bank

DEFAULT_WEEKS = 8
MAX_WEEKS = 26
QUIZ_SIZE = 10
DRILL_SIZE = 10
PHASES = {"foundation": "Foundation", "build": "Build", "sharpen": "Sharpen", "test": "Test week"}
RW_DOMAINS = ["Information and Ideas", "Craft and Structure", "Expression of Ideas", "Standard English Conventions"]
TEST_WEEK_CHECKLIST = [
    "Take the warm-up quiz early in the week, then rest your brain.",
    "Check your admission ticket and photo ID, and charge your device.",
    "Open Bluebook and run its exam setup before test day.",
    "Sleep well the two nights before. Eat breakfast on the morning of the test.",
]


def difficulty_at(level, p):
    """Target difficulty from 0 (all easy) to 1 (all hard), p of the way through the plan."""
    start = 0.2 + 0.3 * level
    end = 0.75 + 0.2 * level
    return round(min(0.95, max(0.05, start + (end - start) * p)), 2)


def mix_for(d, n=QUIZ_SIZE):
    """Question counts by difficulty for a target difficulty d, summing to n."""
    hard = min(1.0, max(0.0, (d - 0.3) / 0.7)) * 0.8
    easy = min(1.0, max(0.0, (0.5 - d) / 0.5)) * 0.6
    shares = {"easy": easy, "medium": max(0.0, 1 - easy - hard), "hard": hard}
    counts = {k: int(v * n) for k, v in shares.items()}
    for k in sorted(shares, key=lambda k: shares[k] * n - counts[k], reverse=True)[:n - sum(counts.values())]:
        counts[k] += 1
    return counts


def mix_label(mix):
    parts = sorted(((v, k) for k, v in mix.items() if v), reverse=True)
    if not parts:
        return ""
    label = "Mostly " + parts[0][1]
    if len(parts) > 1:
        label += ", some " + parts[1][1]
    return label


def estimates(results):
    """Every Math skill's estimated mastery from 0 to 1, from the diagnostic."""
    domain_score = {d["domain_key"]: d["score"] for d in results["domains"] if d["section"] == "Math"}
    out = []
    for d in bank.topics():
        for s in d["skills"]:
            base = domain_score.get(d["key"], 0.5)
            tested = results["skills"].get(s["key"])
            est = 0.7 * tested + 0.3 * base if tested is not None else base
            out.append({"domain": d["key"], "skill": s["key"], "name": s["name"], "est": round(est, 2)})
    return out


def build(results, test_date, hours, today):
    monday = today - timedelta(days=today.weekday())
    exam = date.fromisoformat(test_date) if test_date else None
    if exam and exam < today:
        exam = None
    total = min(MAX_WEEKS, (exam - monday).days // 7 + 1) if exam else DEFAULT_WEEKS
    has_test_week = exam is not None and total >= 2
    study = total - 1 if has_test_week else total
    level = results["level"]
    hours = hours or 3

    skills = estimates(results)
    priority = {s["skill"]: (1 - s["est"]) + 0.05 for s in skills}
    growth = {s["skill"]: 0.06 + 0.12 * (1 - s["est"]) for s in skills}
    by_key = {s["skill"]: s for s in skills}
    order = {s["skill"]: i for i, s in enumerate(skills)}
    focused = []  # (week index, skill key)
    last_seen = {}  # skill key: the last week it was a focus or the review
    rw = sorted((d for d in results["domains"] if d["section"] == "Reading and Writing"), key=lambda d: d["score"])
    rw_order = [d["domain"] for d in rw] or RW_DOMAINS

    weeks = []
    for w in range(study):
        p = w / (study - 1) if study > 1 else 1.0
        phase = "sharpen" if p >= 0.75 else ("build" if p >= 0.34 or study < 3 else "foundation")
        d = difficulty_at(level, p)
        mix = mix_for(d)
        picks = sorted(priority, key=lambda k: (-priority[k], order[k]))[:2]
        for k in priority:
            priority[k] += growth[k]
        for k in picks:
            priority[k] = (1 - by_key[k]["est"]) * 0.25
        # Re-test a skill from at least two weeks back: the one left longest, weakest first on ties.
        earlier = {k for wk, k in focused if wk <= w - 2 and k not in picks}
        review_key = min(earlier, key=lambda k: (last_seen[k], by_key[k]["est"], order[k])) if earlier else None
        focused += [(w, k) for k in picks]
        for k in picks + ([review_key] if review_key else []):
            last_seen[k] = w
        focus = [{"domain": by_key[k]["domain"], "skill": k, "name": by_key[k]["name"]} for k in picks]
        review = {"domain": by_key[review_key]["domain"], "skill": review_key, "name": by_key[review_key]["name"]} if review_key else None

        n = w + 1
        tasks = [{"key": f"w{n}-drill-1", "kind": "drill", "title": focus[0]["name"], "skill": focus[0], "count": DRILL_SIZE}]
        if hours >= 2:
            tasks.append({"key": f"w{n}-drill-2", "kind": "drill", "title": focus[1]["name"], "skill": focus[1], "count": DRILL_SIZE})
        tasks.append({"key": f"w{n}-quiz", "kind": "quiz", "title": f"Week {n} quiz", "count": QUIZ_SIZE})
        # Reading and Writing gets a drill too: the week's focus domain, one of its skills in turn.
        rw_focus = rw_order[w % len(rw_order)]
        rw = rw_skill(rw_focus, w // len(rw_order))
        tasks.append({"key": f"w{n}-rw", "kind": "drill", "title": rw["name"], "skill": rw, "count": DRILL_SIZE})
        if phase != "foundation" and (phase == "sharpen" or w % 2 == 1):
            tasks.append({"key": f"w{n}-test", "kind": "test", "title": "Math practice test"})
        weeks.append({
            "n": n, "week_of": (monday + timedelta(weeks=w)).isoformat(), "phase": phase, "phase_label": PHASES[phase],
            "difficulty": d, "mix": mix, "difficulty_label": mix_label(mix),
            "focus": focus, "review": review, "rw_focus": rw_focus, "tasks": tasks,
        })

    if has_test_week:
        n = study + 1
        best = sorted(skills, key=lambda s: (-s["est"], order[s["skill"]]))[:1]
        worst = sorted(skills, key=lambda s: (s["est"], order[s["skill"]]))[:1]
        focus = [{"domain": s["domain"], "skill": s["skill"], "name": s["name"]} for s in worst + best]
        mix = {"easy": 5, "medium": 5, "hard": 0}
        weeks.append({
            "n": n, "week_of": (monday + timedelta(weeks=study)).isoformat(), "phase": "test", "phase_label": PHASES["test"],
            "difficulty": 0.3, "mix": mix, "difficulty_label": "Easy and medium, to build confidence",
            "focus": focus, "review": None, "rw_focus": None,
            "tasks": [{"key": f"w{n}-quiz", "kind": "quiz", "title": "Warm-up quiz", "count": QUIZ_SIZE}],
            "checklist": TEST_WEEK_CHECKLIST,
        })

    math = [d for d in results["domains"] if d["section"] == "Math"]
    strongest = sorted(math, key=lambda d: -d["score"])
    weakest = sorted(skills, key=lambda s: (s["est"], order[s["skill"]]))
    return {
        "version": 1, "created": today.isoformat(), "start": monday.isoformat(),
        "test_date": exam.isoformat() if exam else None, "hours": hours, "level": level,
        "summary": summary(results, strongest, weakest, weeks, exam),
        "strengths": results["strengths"], "focus_areas": results["focus"], "weeks": weeks,
    }


def summary(results, strongest, weakest, weeks, exam):
    parts = []
    if results["strengths"]:
        parts.append("Your strongest area is " + results["strengths"][0] + ".")
    elif strongest:
        parts.append("Your strongest Math area right now is " + strongest[0]["domain"] + ".")
    parts.append(f"Your plan opens with {weakest[0]['name']} and {weakest[1]['name']}, where you have the most points to gain, "
                 "and brings every Math topic back around before test day.")
    study = [w for w in weeks if w["phase"] != "test"] or weeks
    first, last = study[0]["difficulty_label"].lower(), study[-1]["difficulty_label"].lower()
    if last != first:
        parts.append(f"Quizzes start {first} and build to {last}" + (f" by {exam.strftime('%B')} {exam.day}." if exam else "."))
    else:
        parts.append(f"Quizzes run {first}.")
    return " ".join(parts)


def rw_skill(domain_name, turn):
    """The turn-th Reading and Writing skill of a domain (by name), as a plan skill: {domain, skill, name}."""
    d = next(t for t in bank.topics("rw") if t["name"] == domain_name)
    s = d["skills"][turn % len(d["skills"])]
    return {"domain": d["key"], "skill": s["key"], "name": s["name"]}


def current_week(plan, today):
    """Index of this week in the plan, kept within the plan."""
    start = date.fromisoformat(plan["start"])
    return max(0, min(len(plan["weeks"]) - 1, (today - start).days // 7))
