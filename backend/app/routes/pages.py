"""Serves the built website from website/site, with sign-in required for student pages."""
from pathlib import Path

from flask import Blueprint, abort, current_app, jsonify, redirect, request, send_from_directory

from ..security import current_user

bp = Blueprint("pages", __name__)

# Pages that need a signed-in student. Visitors are sent to sign in first.
PROTECTED = {"dashboard.html", "practice-test.html", "practice.html", "plan.html", "levels.html"}
PARENT_PAGES = {"parent.html"}
ANY_ACCOUNT_PAGES = {"settings.html"}  # need a signed-in account of either kind


def home_for(user):
    return "/parent.html" if user["role"] == "parent" else "/dashboard.html"

API_VERSION = "1"


@bp.get("/api/health")
def health():
    return jsonify({"ok": True, "version": API_VERSION})


@bp.get("/", defaults={"path": "index.html"})
@bp.get("/<path:path>")
def page(path):
    if path.startswith("api/"):
        abort(404)
    site = Path(current_app.config["SITE_DIR"])
    target = (site / path).resolve()
    if site.resolve() not in target.parents and target != site.resolve():
        abort(404)
    if target.is_dir():
        path, target = f"{path.rstrip('/')}/index.html", target / "index.html"
    if not target.exists() and (site / f"{path}.html").exists():
        path, target = f"{path}.html", site / f"{path}.html"  # /dashboard works as well as /dashboard.html
    if not target.is_file():
        abort(404)
    user = current_user()
    if (path in PROTECTED or path in PARENT_PAGES or path in ANY_ACCOUNT_PAGES) and not user:
        return redirect(f"/signin.html?next=/{path}")
    # A page for the other kind of account: offer to sign in with that kind, instead of bouncing to your own
    # dashboard (a student who opens the parent dashboard wants to sign in as the parent, not be sent back).
    if user and user["role"] == "parent" and path in PROTECTED:
        return redirect(f"/signin.html?as=student&next=/{path}")
    if user and user["role"] != "parent" and path in PARENT_PAGES:
        return redirect(f"/signin.html?as=parent&next=/{path}")
    wants = request.args.get("as")
    if path == "signin.html" and user and not request.args.get("reset") and wants in (None, user["role"]):
        return redirect(home_for(user))
    response = send_from_directory(site, path)
    if path.endswith(".html"):
        response.headers["Cache-Control"] = "no-cache"
    else:
        response.cache_control.max_age = 3600
        response.cache_control.public = True
    return response
