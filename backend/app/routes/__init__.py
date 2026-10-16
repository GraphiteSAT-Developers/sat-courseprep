"""Every feature's routes, registered in this order. Add new blueprints here.

The pages blueprint stays last: it catches every path that isn't an API route.
"""
from . import account, auth, dashboard, email, leads, masterclass, pages, plan, practice, tests

BLUEPRINTS = [
    auth.bp,        # /api/auth/...  create account, sign in and out, password reset
    account.bp,     # /api/me        the student's own account
    leads.bp,       # /api/leads     the home page signup form
    tests.bp,       # /api/tests     practice tests and grading
    practice.bp,    # /api/practice  random practice tests and topic practice from the question bank
    plan.bp,        # /api/plan      the diagnostic and the study plan
    practice.sample_bp,  # /api/sample  the home page's sample question
    dashboard.bp,   # /api/dashboard, /api/review, /api/activity
    masterclass.bp, # /api/masterclass  Desmos masterclass progress
    email.bp,       # /api/email      one-click unsubscribe from the weekly email
    # Add new feature blueprints above this line. See routes/_example.py.
    pages.bp,       # the website itself, plus /api/health
]
