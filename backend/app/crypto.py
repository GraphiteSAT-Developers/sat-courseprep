"""Encryption for the most sensitive things the database keeps: profile photos, the parent email a student
enters, and messages sent through the home page form. AES-256-GCM, so anything changed in the database is
caught instead of decrypted wrongly.

The key is DATA_KEY: 32 random bytes, base64-encoded. Make one with
    python -c "import base64, os; print(base64.b64encode(os.urandom(32)).decode())"
and keep it somewhere safe. If it's lost, encrypted data can't be read back. Without DATA_KEY a key is
derived from SECRET_KEY (fine on your computer; in production set DATA_KEY so changing SECRET_KEY, which signs
everyone out, doesn't also lock away the data).

Values stored before encryption was added (no "enc1:" prefix) are read as they are, and encrypted the
next time they're saved.
"""
import base64
import hashlib
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from flask import current_app

PREFIX = "enc1:"


def _key():
    raw = current_app.config.get("DATA_KEY") or ""
    if raw:
        key = base64.b64decode(raw)
        if len(key) != 32:
            raise RuntimeError("DATA_KEY must be 32 bytes, base64-encoded.")
        return key
    return hashlib.sha256(b"graphite-data-key:" + current_app.config["SECRET_KEY"].encode()).digest()


def seal(text):
    """Encrypts a string. None and empty strings stay as they are."""
    if text is None or text == "":
        return text
    nonce = os.urandom(12)
    ct = AESGCM(_key()).encrypt(nonce, str(text).encode("utf-8"), None)
    return PREFIX + base64.b64encode(nonce + ct).decode("ascii")


def unseal(value):
    """Decrypts a value from seal(). Older plain values pass through unchanged."""
    if not isinstance(value, str) or not value.startswith(PREFIX):
        return value
    blob = base64.b64decode(value[len(PREFIX):])
    return AESGCM(_key()).decrypt(blob[:12], blob[12:], None).decode("utf-8")
