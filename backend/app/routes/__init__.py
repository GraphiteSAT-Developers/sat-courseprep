"""Every feature's routes, registered in this order. Add new blueprints here.

The pages blueprint stays last: it catches every path that isn't an API route.
"""
from . import account, auth, checkout, dashboard, family, history, leads, pages, plan, play, practice, settings, tests

BLUEPRINTS = [
    auth.bp,        # /api/auth/...  create account, sign in and out, password reset
    account.bp,     # /api/me        the student's own account
    leads.bp,       # /api/leads     the home page signup form
    tests.bp,       # /api/tests     practice tests and grading
    practice.bp,    # /api/practice  random practice tests and topic practice from the question bank
    plan.bp,        # /api/plan      the diagnostic and the study plan
    practice.sample_bp,  # /api/sample  the home page's sample question
    practice.levels_bp,  # /api/levels  Level up: sets that get harder level by level
    dashboard.bp,   # /api/dashboard, /api/review, /api/activity
    family.student_bp,  # /api/family  a student's Parent access: link codes and connected parents
    family.bp,      # /api/parent  the parent dashboard
    settings.bp,    # /api/me/...    the settings page: appearance, photo, email, password, data, delete
    checkout.bp,    # /api/checkout  the checkout page: buy a plan (Stripe, once connected)
    checkout.webhook_bp,  # /api/stripe/webhook  payments, renewals and cancellations from Stripe
    play.game_bp,     # /api/game     rewards: XP, coins, ranks, streak, badges and the shop
    play.speed_bp,    # /api/speed    the daily speed round and leaderboards
    play.focus_bp,    # /api/focus    the focus timer
    play.lessons_bp,  # /api/lessons  active recall lessons
    play.market_bp,   # /api/market   the collectibles market
    history.bp,       # /api/me/history  everything done on the site, and every answered question
    # Add new feature blueprints above this line. See routes/_example.py.
    pages.bp,       # the website itself, plus /api/health
]
