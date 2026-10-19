"""A small Stripe client: just the calls Graphite SAT needs, with no extra packages to install.

Payments switch on when STRIPE_SECRET_KEY is set (see backend/README.md, "Connect Stripe"). Until then,
is_live() is False and checkout starts plans without charging anyone, except on the live site
(APP_ENV=production), where paid plans can't be started until payments are connected (payments_off()).
"""
import hashlib
import hmac
import json
import time
import urllib.error
import urllib.parse
import urllib.request

from flask import current_app

API = "https://api.stripe.com/v1"


class StripeError(Exception):
    pass


def secret_key():
    return current_app.config.get("STRIPE_SECRET_KEY") or ""


def is_live():
    """True once a Stripe key is set. Test keys (sk_test_...) count: they let you try checkout with test cards."""
    return bool(secret_key())


def payments_off():
    """True on the live site before Stripe is connected. Locally, plans start without a charge so the site can be
    tried; on the live site that would hand out paid plans for free, so paid plans wait for payments instead."""
    return not is_live() and bool(current_app.config.get("IS_PRODUCTION"))


def _flatten(data, prefix=""):
    """Stripe takes form fields, with nested values as a[b][c] and lists as a[0][b]."""
    out = []
    items = data.items() if isinstance(data, dict) else enumerate(data)
    for k, v in items:
        key = f"{prefix}[{k}]" if prefix else str(k)
        if isinstance(v, (dict, list, tuple)):
            out.extend(_flatten(v, key))
        elif v is None:
            continue
        elif isinstance(v, bool):
            out.append((key, "true" if v else "false"))
        else:
            out.append((key, str(v)))
    return out


def request(method, path, data=None):
    """Calls the Stripe API and returns its JSON. Tests replace this function."""
    in_url = method in ("GET", "DELETE")  # Stripe reads these requests' fields from the address
    body = None if in_url else urllib.parse.urlencode(_flatten(data or {})).encode()
    url = API + path
    if in_url and data:
        url += "?" + urllib.parse.urlencode(_flatten(data))
    req = urllib.request.Request(url, data=body, method=method, headers={
        "Authorization": f"Bearer {secret_key()}", "Stripe-Version": "2024-06-20",
        "Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as err:
        try:
            message = json.loads(err.read().decode())["error"]["message"]
        except Exception:  # noqa: BLE001  (any unreadable error body)
            message = f"Stripe answered {err.code}."
        current_app.logger.warning("Stripe %s %s failed: %s", method, path, message)
        raise StripeError(message) from err
    except urllib.error.URLError as err:
        current_app.logger.warning("Couldn't reach Stripe: %s", err)
        raise StripeError("We couldn't reach the payment service.") from err


def verify_webhook(payload, signature_header, secret, tolerance=300, now=None):
    """Checks the Stripe-Signature header and returns the event. Raises StripeError if it doesn't match."""
    if not secret:
        raise StripeError("STRIPE_WEBHOOK_SECRET isn't set.")
    parts = {}
    for piece in (signature_header or "").split(","):
        k, _, v = piece.partition("=")
        parts.setdefault(k.strip(), []).append(v.strip())
    try:
        stamp = int(parts.get("t", [""])[0])
    except ValueError:
        raise StripeError("The signature has no timestamp.") from None
    if abs((now or time.time()) - stamp) > tolerance:
        raise StripeError("The signature is too old.")
    expected = hmac.new(secret.encode(), f"{stamp}.".encode() + payload, hashlib.sha256).hexdigest()
    if not any(hmac.compare_digest(expected, sig) for sig in parts.get("v1", [])):
        raise StripeError("The signature doesn't match.")
    return json.loads(payload.decode())


def sign_for_tests(payload, secret, stamp=None):
    """The Stripe-Signature header Stripe would send for this payload. Used by the tests."""
    stamp = stamp or int(time.time())
    sig = hmac.new(secret.encode(), f"{stamp}.".encode() + payload, hashlib.sha256).hexdigest()
    return f"t={stamp},v1={sig}"
