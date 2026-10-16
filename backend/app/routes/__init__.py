"""Every feature's routes, registered in this order. Add new blueprints here.

The pages blueprint stays last: it catches every path that isn't an API route.
"""
from . import account, auth, dashboard, leads, pages, plan, practice, tests

BLUEPRINTS = [
    auth.bp,        # /api/auth/...  create account, sign in and out, password reset
    account.bp,     # /api/me        the student's own account
    leads.bp,       # /api/leads     the home page signup form
    tests.bp,       # /api/tests     practice tests and grading
    practice.bp,    # /api/practice  random practice tests and topic practice from the question bank
    plan.bp,        # /api/plan      the diagnostic and the study plan
    dashboard.bp,   # /api/dashboard, /api/review, /api/activity
    # Add new feature blueprints above this line. See routes/_example.py.
    pages.bp,       # the website itself, plus /api/health
]
