"""Plans, prices and what each plan includes. The single source for the home page pricing section,
the parent dashboard's billing, and the site build (so the preview shows the same prices).

Prices are in cents, for each way of paying. Everything shown to people is the price per month:
weekly and yearly billing show what they work out to each month, plus what's actually billed.

FEATURES and LIMITS describe each plan. LIMITS aren't enforced yet: every account can use every
feature until real payments are connected. To enforce them, check plan_limits(user["plan"]) in the
routes that start practice sets, practice tests and Level up.
"""
from datetime import timedelta

ORDER = ("free", "no2", "sharpened", "masterstroke")
INTERVALS = ("week", "month", "year")
WEEKS_PER_MONTH = 52 / 12

PLANS = {
    "free": {
        "name": "Scratch Paper",
        "tagline": "Try Graphite before you commit.",
        "blurb": "The diagnostic and one practice set a week.",
        "badge": None,
        "prices": {"week": 0, "month": 0, "year": 0},
        "intro": None,
        "features": [
            "The 10-question diagnostic",
            "Your strongest and weakest skill areas",
            "1 practice set a week",
            "Built-in graphing calculator",
        ],
    },
    "no2": {
        "name": "No. 2",
        "tagline": "The pencil every SAT needs. Steady practice, every week.",
        "blurb": "Unlimited practice, daily sets and a study plan to your test date.",
        "badge": None,
        "prices": {"week": 499, "month": 1900, "year": 18000},
        "intro": "Everything in Scratch Paper, plus:",
        "features": [
            "Unlimited practice in all 8 skill areas",
            "Daily sets picked from your weakest skills",
            "A study plan built around your test date",
            "Step-by-step explanations for every answer",
            "A review queue that brings back every miss",
        ],
    },
    "sharpened": {
        "name": "Sharpened",
        "tagline": "Everything you need to raise your score.",
        "blurb": "Unlimited timed practice tests, Level up, score tracking and the parent dashboard.",
        "badge": "Most popular",
        "prices": {"week": 999, "month": 3900, "year": 34800},
        "intro": "Everything in No. 2, plus:",
        "features": [
            "Unlimited timed practice tests in the real test layout",
            "Level up: sets that get harder level by level",
            "Score history and a skill breakdown after every test",
            "Calculator shortcuts on every question where a graph is faster",
            "Parent dashboard with weekly progress emails",
            "Alerts when practice stops",
        ],
    },
    "masterstroke": {
        "name": "Masterstroke",
        "tagline": "Our most hands-on plan, with a coach in your corner.",
        "blurb": "Everything in Sharpened, plus a weekly 1-on-1 check-in with a human coach.",
        "badge": "Best results",
        "prices": {"week": 3499, "month": 12900, "year": 118800},
        "intro": "Everything in Sharpened, plus:",
        "features": [
            "A weekly 30-minute 1-on-1 video check-in with a coach",
            "Your study plan reviewed after every practice test",
            "A test-week plan for pacing, sleep and logistics",
            "A monthly call with your parent",
            "Priority help, answered within one school day",
        ],
    },
}

# What each plan allows, for when limits are switched on (None means unlimited).
LIMITS = {
    "free": {"practice_sets_per_week": 1, "practice_tests": 0, "level_up": False, "study_plan": False, "parent_dashboard": False},
    "no2": {"practice_sets_per_week": None, "practice_tests": 0, "level_up": False, "study_plan": True, "parent_dashboard": False},
    "sharpened": {"practice_sets_per_week": None, "practice_tests": None, "level_up": True, "study_plan": True, "parent_dashboard": True},
    "masterstroke": {"practice_sets_per_week": None, "practice_tests": None, "level_up": True, "study_plan": True, "parent_dashboard": True},
}

# Plan names used before October 2026, mapped to the plan that replaced them.
LEGACY = {"daily": "sharpened", "coached": "masterstroke"}

PAUSE_DAYS = 30
ALERT_DAYS = (0, 2, 3, 5, 7)  # quiet days before a parent gets an inactivity alert; 0 turns alerts off


def key_for(plan):
    plan = LEGACY.get(plan, plan)
    return plan if plan in PLANS else "free"


def plan_limits(plan):
    return LIMITS[key_for(plan)]


def money(cents):
    return f"${cents / 100:,.2f}".replace(".00", "")


def per_month(plan, interval):
    """What a plan works out to each month when paid weekly, monthly or yearly, in cents."""
    cents = PLANS[key_for(plan)]["prices"][interval]
    if interval == "week":
        return round(cents * WEEKS_PER_MONTH)
    if interval == "year":
        return round(cents / 12)
    return cents


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
    """For the parent dashboard: '$29/month, billed $348 yearly'."""
    if not interval or not PLANS[key_for(plan)]["prices"][interval]:
        return "Free"
    each = money(per_month(plan, interval)) + "/month"
    if interval == "month":
        return each
    return f"{each}, billed {money(PLANS[key_for(plan)]['prices'][interval])} {interval_words(interval)}"


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
