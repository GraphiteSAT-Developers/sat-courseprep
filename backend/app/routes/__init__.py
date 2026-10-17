"""Every feature's routes, registered in this order. Add new blueprints here.

The pages blueprint stays last: it catches every path that isn't an API route.
"""
from . import account, auth, dashboard, family, leads, pages, plan, practice, settings, tests

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
    # Add new feature blueprints above this line. See routes/_example.py.
    pages.bp,       # the website itself, plus /api/health
]
