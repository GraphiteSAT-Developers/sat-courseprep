"""Builds the week-by-week plan from the student's test date and weakest domains."""
from datetime import date, timedelta

from .content import MATH_DOMAINS, RW_DOMAINS

MAX_WEEKS = 16
DEFAULT_WEEKS = 8


def focus_order(domain_pct):
    """Math domains from weakest to strongest (unmeasured ones in the middle), alternating with Reading and Writing."""
    math = sorted(MATH_DOMAINS, key=lambda d: domain_pct.get(d) if domain_pct.get(d) is not None else 70)
    order = []
    for m, r in zip(math, RW_DOMAINS):
        order += [m, r]
    return order


def build_plan(test_date, domain_pct, today=None):
    today = today or date.today()
    monday = today - timedelta(days=today.weekday())
    exam = date.fromisoformat(test_date) if test_date else None
    if exam and exam >= today:
        weeks = min(MAX_WEEKS, (exam - monday).days // 7 + 1)
    else:
        exam, weeks = None, DEFAULT_WEEKS
    order = focus_order(domain_pct)
    plan = []
    for w in range(weeks):
        start = monday + timedelta(weeks=w)
        last = exam is not None and w == weeks - 1
        if last:
            focus = "Test week: pacing, sleep and logistics"
        else:
            focus = order[w % len(order)]
            if w % 3 == 2:
                saturday = start + timedelta(days=5)
                focus += f". Practice test on {saturday.strftime('%b')} {saturday.day}"
        plan.append({"week_of": start.isoformat(), "focus": focus, "is_now": w == 0})
    return {"weeks": plan, "fits_test_date": exam is not None}
