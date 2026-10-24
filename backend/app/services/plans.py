"""Plans, prices and what each plan includes. The single source for the home page pricing section,
the parent dashboard's billing, and the site build (so the preview shows the same prices).

There are two plans: Sharpened, which is free, and Mechanical, which has everything. (The free plan's key
is still "free"; "sharpened" as a key is one of the older paid plans in LEGACY below.)

Prices are in cents, for each way of paying. Everything shown to people is the price per month:
weekly and yearly billing show what they work out to each month, plus what's actually billed.

Each plan's features, COMPARE (the home page's feature table) and LIMITS describe what it includes.
services/access.py enforces LIMITS (turn it off with PLAN_LIMITS=false), and locks the paid features
while a plan isn't paid: a failed payment (past_due) or a pause.
"""
from datetime import timedelta

ORDER = ("free", "mechanical")
FEATURED = "mechanical"  # the plan the home page highlights and checkout picks first
INTERVALS = ("week", "month", "year")
WEEKS_PER_MONTH = 52 / 12

PLANS = {
    "free": {
        "name": "Sharpened",
        "tagline": "Try Graphite SAT before you pay.",
        "blurb": "The diagnostic, 1 practice test a month, 3 topic sets a week, 3 starter lessons and the first 2 levels of Practice Sets.",
        "badge": None,
        "prices": {"week": 0, "month": 0, "year": 0},
        "intro": None,
        "features": [
            "The 10-question diagnostic",
            "Your strongest and weakest skill areas",
            "1 full practice test a month, with your score breakdown",
            "3 topic sets a week",
            "3 starter lessons",
            "Practice Sets: the first 2 levels of every topic",
            "A review queue that brings back every miss",
            "30 tutor credits a month (tutor coming soon)",
            "Built-in graphing calculator",
        ],
    },
    "mechanical": {
        "name": "Mechanical",
        "tagline": "Everything Graphite SAT has, in one plan.",
        "blurb": "Everything: unlimited practice tests, every lesson and explanation, your study plan, and the parent dashboard.",
        "badge": "Everything included",
        "prices": {"week": 199, "month": 800, "year": 7200},
        "intro": "Everything in Sharpened, plus:",
        "features": [
            "Unlimited full practice tests in the real test layout",
            "Unlimited topic sets, picked from your weakest skills",
            "Every lesson, including the full Desmos course",
            "Practice Sets: every level of every topic",
            "Step-by-step explanations for every answer",
            "A study plan built around your test date",
            "Unlimited tutor help, any time of day (coming soon)",
            "In-depth video explanations (coming soon)",
            "Parent dashboard with weekly progress emails",
            "Your study plan reviewed after every practice test",
            "A test-week plan for pacing, sleep and logistics",
            "A monthly call with your parent",
            "Priority 24/7 support",
        ],
    },
}

# The "Compare every feature" table on the home page, in plan order (Sharpened, Mechanical).
# True shows a check mark, False a dash, and text shows as written.
COMPARE = [
    ("Practice", [
        ("10-question diagnostic with your strong and weak areas", [True, True]),
        ("Full practice tests in the real test layout", ["1 a month", "Unlimited"]),
        ("Topic sets picked from your weakest skills", ["3 a week", "Unlimited"]),
        ("Practice Sets that get harder level by level", ["First 2 levels of each topic", "Every level"]),
        ("Review queue that brings back every miss", [True, True]),
        ("Hands-on lessons, including the Desmos course", ["3 starter lessons", "All"]),
        ("Built-in graphing calculator", [True, True]),
    ]),
    ("Help when you're stuck", [
        ("Tutor (coming soon)", ["30 credits a month", "Unlimited"]),
        ("Step-by-step written explanations", ["Diagnostic only", True]),
        ("In-depth video explanations (coming soon)", [False, True]),
        ("Support", ["Help center", "24/7, priority"]),
    ]),
    ("Planning and progress", [
        ("Study plan built around your test date", [False, True]),
        ("Score history and skill breakdown", [True, True]),
        ("Parent dashboard and weekly progress emails", [False, True]),
        ("Study plan reviewed by a coach", [False, True]),
        ("Test-week plan for pacing, sleep and logistics", [False, True]),
        ("Monthly call with your parent", [False, True]),
    ]),
]

# What each plan allows, for when limits are switched on (None means unlimited). A tutor credit is one
# question to the tutor; the tutor isn't built yet, so nothing counts them so far.
LIMITS = {
    "free": {"practice_sets_per_week": 3, "practice_tests_per_month": 1, "tutor_credits_per_month": 30, "video_explanations": False,
             "level_up": False, "study_plan": False, "parent_dashboard": False, "review_queue": True,
             "explanations": False, "score_history": True, "all_lessons": False},
    "mechanical": {"practice_sets_per_week": None, "practice_tests_per_month": None, "tutor_credits_per_month": None, "video_explanations": True,
                   "level_up": True, "study_plan": True, "parent_dashboard": True, "review_queue": True,
                   "explanations": True, "score_history": True, "all_lessons": True},
}
# Practice Sets levels every plan can play, in every track. The levels above them need level_up (every level).
FREE_LEVELS = 2

# Plan names used before, mapped to the plan that replaced them: Daily and Coached (until early October 2026),
# then No. 2, Sharpened and Masterstroke (until October 19, 2026). Every one of them gets what Mechanical includes.
LEGACY = {"daily": "mechanical", "coached": "mechanical", "no2": "mechanical", "sharpened": "mechanical", "masterstroke": "mechanical"}
# What the October 2026 plans cost. A Stripe subscription keeps the price it started with, so anyone still paying
# for one of them is shown that price (not Mechanical's) until they switch to Mechanical at checkout.
LEGACY_PRICES = {
    "no2": {"week": 499, "month": 1900, "year": 18000},
    "sharpened": {"week": 999, "month": 3900, "year": 34800},
    "masterstroke": {"week": 3499, "month": 12900, "year": 118800},
}

PAUSE_DAYS = 30
# A free trial of TRIAL_PLAN: once per student, no card, and it goes back to the free plan by itself.
TRIAL_PLAN = "mechanical"
TRIAL_DAYS = 7
ALERT_DAYS = (0, 2, 3, 5, 7)  # quiet days before a parent gets an inactivity alert; 0 turns alerts off


def key_for(plan):
    plan = LEGACY.get(plan, plan)
    return plan if plan in PLANS else "free"


def plan_limits(plan):
    return LIMITS[key_for(plan)]


def money(cents):
    return f"${cents / 100:,.2f}".replace(".00", "")


def _per_month(cents, interval):
    if interval == "week":
        return round(cents * WEEKS_PER_MONTH)
    if interval == "year":
        return round(cents / 12)
    return cents


def per_month(plan, interval):
    """What a plan works out to each month when paid weekly, monthly or yearly, in cents."""
    return _per_month(PLANS[key_for(plan)]["prices"][interval], interval)


def billed_cents(plan, interval):
    """What a subscription on this plan is billed each week, month or year: the plan's price, or for a plan in
    LEGACY_PRICES, the older price that subscriber still pays."""
    if plan in LEGACY_PRICES:
        return LEGACY_PRICES[plan][interval]
    return PLANS[key_for(plan)]["prices"][interval]


def savings(plan, interval):
    """How much cheaper than paying monthly, as a whole percent and in cents over a year."""
    p = PLANS[key_for(plan)]["prices"]
    if not p["month"]:
        return {"percent": 0, "per_year_cents": 0}
    diff = p["month"] * 12 - per_month(plan, interval) * 12
    return {"percent": round(diff / (p["month"] * 12) * 100), "per_year_cents": diff}


def next_renewal(today, interval, add_months):
    if interval == "week":
        return today + timedelta(days=7)
    return add_months(today, 1 if interval == "month" else 12)


def interval_words(interval):
    return {"week": "weekly", "month": "monthly", "year": "yearly"}[interval]


def price_label(plan, interval):
    """For the parent dashboard: '$6/month, billed $72 yearly'. An older plan's price says so."""
    cents = billed_cents(plan, interval) if interval else 0
    if not cents:
        return "Free"
    each = money(_per_month(cents, interval)) + "/month"
    label = each if interval == "month" else f"{each}, billed {money(cents)} {interval_words(interval)}"
    return label + (" (earlier price)" if plan in LEGACY_PRICES else "")


def public_plans():
    """Everything the pages need to show the plans, in order from free to the top plan."""
    out = []
    for key in ORDER:
        p = PLANS[key]
        out.append({
            "key": key, "name": p["name"], "tagline": p["tagline"], "blurb": p["blurb"], "badge": p["badge"],
            "intro": p["intro"], "features": list(p["features"]),
            "cents": dict(p["prices"]),
            "per_month_cents": {iv: per_month(key, iv) for iv in INTERVALS},
            "savings": {iv: savings(key, iv) for iv in INTERVALS},
            # kept for older pages
            "month_cents": p["prices"]["month"], "year_cents": p["prices"]["year"], "week_cents": p["prices"]["week"],
        })
    return out
