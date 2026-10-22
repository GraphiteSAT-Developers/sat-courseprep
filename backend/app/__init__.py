"""Graphite SAT backend. create_app() builds the Flask app; wsgi.py runs it."""
import logging
import random
from datetime import timedelta

from flask import Flask, jsonify, redirect, request, send_from_directory
from werkzeug.exceptions import HTTPException
from werkzeug.middleware.proxy_fix import ProxyFix

from .compress import gzip_response
from .config import Config
from .db import close_db
from .routes import BLUEPRINTS
from . import testaccount
from .schema import migrate
from .security import ApiError, check_same_origin, current_user, error_response, prune_events, write_flood
from .services import donelist

CSP = ("default-src 'self'; script-src 'self' https://plausible.io https://www.googletagmanager.com https://challenges.cloudflare.com; "
       "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; "
       "img-src 'self' data:; connect-src 'self' https://plausible.io https://www.google-analytics.com https://challenges.cloudflare.com; "
       "frame-src 'self' https://challenges.cloudflare.com; frame-ancestors 'self'; base-uri 'self'; form-action 'self'; "
       "object-src 'none'")
# The calculator is one self-contained file with inline scripts.
CSP_CALCULATOR = CSP.replace("script-src 'self'", "script-src 'self' 'unsafe-inline'")
PARENT_APIS = ("/api/parent", "/api/auth", "/api/me", "/api/health", "/api/checkout")
# Stripe posts here from its own servers: it proves who it is with a signature instead of the same-site check.
WEBHOOKS = ("/api/stripe/webhook",)


def create_app(overrides=None):
    app = Flask(__name__, static_folder=None)
    app.config.from_object(Config)
    if overrides:
        app.config.update(overrides)
    if not app.config["SECRET_KEY"]:
        raise RuntimeError("Set the SECRET_KEY environment variable before running in production.")
    app.permanent_session_lifetime = timedelta(days=app.config["REMEMBER_DAYS"])
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
    logging.basicConfig(level=logging.INFO)

    if app.config["IS_PRODUCTION"] and app.config["DATABASE_URL"].startswith("sqlite"):
        app.logger.warning("Running in production on SQLite. On hosts without a persistent disk (like Render's free "
                           "plan) the database is wiped on every restart. Set DATABASE_URL to a Postgres database.")
    migrate(app.config["DATABASE_URL"])
    if app.config["TEST_ACCOUNT"]:
        testaccount.ensure(app.config["DATABASE_URL"])
        app.logger.info('Test accounts ready: student "beta" / "beta", and parent "beta2" / "beta2".')
    for bp in BLUEPRINTS:
        app.register_blueprint(bp)
    app.teardown_appcontext(close_db)

    @app.before_request
    def before():
        if app.config["FORCE_HTTPS"] and request.scheme == "http":
            return redirect(request.url.replace("http://", "https://", 1), code=301)
        if request.path in WEBHOOKS:
            return None
        if request.path.startswith("/api/"):
            check_same_origin()
            if request.method not in ("GET", "HEAD", "OPTIONS") and write_flood():
                raise ApiError(429, "That's a lot of requests at once. Wait a minute and try again.", code="rate_limited")
            if random.random() < 0.01:
                prune_events()
                from .services import tutor
                tutor.prune()  # conversations older than TUTOR_RETENTION_DAYS
            # Parents see a student only through the parent dashboard; students can't use it.
            user = current_user()
            if request.method not in ("GET", "HEAD", "OPTIONS"):
                from .services import history
                history.before(user)  # what the account looked like, so the change can be saved
            if user and user["role"] == "parent" and not request.path.startswith(PARENT_APIS):
                raise ApiError(403, "Parent accounts see their student's progress on the parent dashboard.", code="parent_account")
            if user and user["role"] != "parent" and request.path.startswith("/api/parent"):
                raise ApiError(403, "The parent dashboard is for parent accounts.", code="student_account")
            if user and user["role"] != "parent" and donelist.wanted(request.path):
                donelist.absorb(user["id"], request.cookies)  # questions the browser's done-list cookies have

    @app.cli.command("analytics-report")
    def analytics_report():
        """The last 30 days of site analytics: flask --app wsgi analytics-report"""
        import json as _json
        from .services import analytics
        print(_json.dumps(analytics.report(), indent=2))

    @app.cli.command("tutor-report")
    def tutor_report():
        """The tutor's last 30 days: messages, tokens and cost by model, and flagged conversations."""
        import json as _json
        from .services import tutor
        tutor.prune()
        print(_json.dumps(tutor.report(), indent=2))

    @app.cli.command("send-weekly-reports")
    def weekly_reports():
        """Email each parent their student's week. Schedule it weekly (for example Sunday evening)."""
        from .routes.family import send_weekly_reports
        print(f"Sent {send_weekly_reports()} reports")

    @app.after_request
    def save_history(resp):
        if request.path.startswith("/api/") and request.method not in ("GET", "HEAD", "OPTIONS") and request.path not in WEBHOOKS:
            from .services import history
            history.after(resp)
        return resp

    @app.after_request
    def done_cookies(resp):
        """Practice responses carry the student's done list, one cookie per section (services/donelist.py)."""
        if request.path.startswith("/api/") and donelist.wanted(request.path) and resp.status_code < 500:
            user = current_user()
            if user and user["role"] != "parent":
                donelist.attach(resp, user["id"], app.config["SESSION_COOKIE_SECURE"])
        return resp

    @app.after_request
    def headers(resp):
        resp.headers.setdefault("X-Content-Type-Options", "nosniff")
        resp.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        resp.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
        resp.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=(), payment=(), usb=(), interest-cohort=()")
        resp.headers.setdefault("Cross-Origin-Opener-Policy", "same-origin")
        resp.headers.setdefault("Cross-Origin-Resource-Policy", "same-origin")
        resp.headers.setdefault("X-Permitted-Cross-Domain-Policies", "none")
        csp = CSP_CALCULATOR if request.path == "/calculator.html" else CSP
        resp.headers.setdefault("Content-Security-Policy", csp + ("; upgrade-insecure-requests" if app.config["FORCE_HTTPS"] else ""))
        if app.config["FORCE_HTTPS"]:
            resp.headers.setdefault("Strict-Transport-Security", "max-age=63072000; includeSubDomains; preload")
        if request.path.startswith("/api/"):
            resp.headers["Cache-Control"] = "no-store"
        return gzip_response(resp, request)

    @app.errorhandler(ApiError)
    def api_error(err):
        return error_response(err)

    @app.errorhandler(HTTPException)
    def http_error(err):
        if request.path.startswith("/api/"):
            return jsonify({"error": err.description or err.name}), err.code
        if err.code == 404:
            return send_from_directory(app.config["SITE_DIR"], "404.html"), 404
        return err

    @app.errorhandler(Exception)
    def server_error(err):
        app.logger.exception("Unhandled error")
        if request.path.startswith("/api/"):
            return jsonify({"error": "Something went wrong on our side. Try again in a moment."}), 500
        return "Something went wrong on our side. Try again in a moment.", 500

    return app
