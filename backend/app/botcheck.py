"""Bot protection for sign-up, password resets and the home page form, on top of the hidden honeypot fields.

1. A form token: the page asks /api/auth/form-token for a signed, timestamped token when it loads. A form without a
   valid token, or sent back less than FORM_MIN_SECONDS after the page got it, is refused. Scripts that post
   straight to the API, or fill a form in a split second, are stopped.
2. Cloudflare Turnstile, when TURNSTILE_SITE_KEY and TURNSTILE_SECRET_KEY are set: an invisible check that only
   asks a person to click when something looks off. Its answer is verified with Cloudflare here.
"""
import json
import time
import urllib.parse
import urllib.request

from flask import current_app
from itsdangerous import BadSignature, URLSafeSerializer

from .security import ApiError, client_ip

TOKEN_MAX_AGE = 2 * 60 * 60  # seconds a token stays good
VERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"


def _signer():
    return URLSafeSerializer(current_app.config["SECRET_KEY"], salt="graphite-form")


def new_token():
    return _signer().dumps({"t": int(time.time())})  # rounded down, so a token is never "from the future"


def enabled():
    cfg = current_app.config
    return not cfg.get("TESTING") or cfg.get("BOT_CHECK_IN_TESTS")


def check(data):
    """Raises ApiError when the form looks automated. Call before doing anything with the form."""
    if not enabled():
        return
    try:
        issued = float(_signer().loads(str(data.get("form_token") or ""))["t"])
    except (BadSignature, KeyError, TypeError, ValueError):
        raise ApiError(400, "Refresh the page and try again.", code="bot_check")
    age = time.time() - issued
    if age < current_app.config["FORM_MIN_SECONDS"]:
        raise ApiError(400, "One moment. Wait a few seconds and press the button again.", code="bot_check")
    if age > TOKEN_MAX_AGE:
        raise ApiError(400, "This page has been open a while. Refresh it and try again.", code="bot_check")
    secret = current_app.config.get("TURNSTILE_SECRET_KEY")
    if secret and current_app.config.get("TURNSTILE_SITE_KEY"):
        answer = str(data.get("turnstile") or "")
        if not answer or not _turnstile_ok(secret, answer):
            raise ApiError(400, "Please complete the check above the button and try again.", code="bot_check")


def _turnstile_ok(secret, answer):
    body = urllib.parse.urlencode({"secret": secret, "response": answer, "remoteip": client_ip()}).encode()
    try:
        with urllib.request.urlopen(urllib.request.Request(VERIFY_URL, data=body), timeout=8) as r:
            return bool(json.loads(r.read().decode()).get("success"))
    except (OSError, ValueError):
        current_app.logger.warning("Couldn't reach Turnstile to check a form; letting it through.")
        return True  # don't lock everyone out if Cloudflare is down; the other checks still apply
