"""Graphite backend. create_app() builds the Flask app; wsgi.py runs it."""
import logging
import random
from datetime import timedelta

from flask import Flask, jsonify, redirect, request, send_from_directory
from werkzeug.exceptions import HTTPException
from werkzeug.middleware.proxy_fix import ProxyFix

from .config import Config
from .db import close_db
from .routes import BLUEPRINTS
from . import testaccount
from .schema import migrate
from .security import ApiError, check_same_origin, error_response, prune_events

CSP = ("default-src 'self'; script-src 'self' https://plausible.io https://www.googletagmanager.com; "
       "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; "
       "img-src 'self' data:; connect-src 'self' https://plausible.io https://www.google-analytics.com; "
       "frame-src 'self'; frame-ancestors 'self'; base-uri 'self'; form-action 'self'")
# The calculator is one self-contained file with inline scripts.
CSP_CALCULATOR = CSP.replace("script-src 'self'", "script-src 'self' 'unsafe-inline'")


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
        app.logger.info('Test account ready: sign in with username "beta" and password "beta".')
    for bp in BLUEPRINTS:
        app.register_blueprint(bp)
    app.teardown_appcontext(close_db)

    @app.before_request
    def before():
        if app.config["FORCE_HTTPS"] and request.scheme == "http":
            return redirect(request.url.replace("http://", "https://", 1), code=301)
        if request.path.startswith("/api/"):
            check_same_origin()
            if random.random() < 0.01:
                prune_events()

    @app.after_request
    def headers(resp):
        resp.headers.setdefault("X-Content-Type-Options", "nosniff")
        resp.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        resp.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
        resp.headers.setdefault("Content-Security-Policy", CSP_CALCULATOR if request.path == "/calculator.html" else CSP)
        if app.config["FORCE_HTTPS"]:
            resp.headers.setdefault("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
        if request.path.startswith("/api/"):
            resp.headers["Cache-Control"] = "no-store"
        return resp

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
