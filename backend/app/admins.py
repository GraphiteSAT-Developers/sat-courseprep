"""Admin accounts: the emails in ADMIN_ACCOUNTS (app/config.py), set on Render.

An admin is an ordinary account (its role stays student or parent, so every page works as usual) with three extras:
the /admin page, instant plan switching on the subscription page, and "Start over" in Settings > Your data, the
same as the local test account. Nothing is stored: removing an email from ADMIN_ACCOUNTS takes it all away.
"""
from flask import current_app

from . import testaccount


def is_admin(user):
    return bool(user) and str(user["email"] or "").lower() in current_app.config.get("ADMIN_ACCOUNTS", ())


def is_test_student(user):
    """The local test student (beta) or an admin's student account: may switch plans instantly and start over."""
    if not user or user["role"] != "student":
        return False
    return is_admin(user) or (bool(current_app.config.get("TEST_ACCOUNT")) and user["email"] == testaccount.USERNAME)
