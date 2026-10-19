"""The done list in the browser: one cookie per section with every question the student has finished.

When a student checks or submits an answer, the question goes on their done list (practice_seen,
services/practice.py). Every practice response also writes that list into a cookie for its section:

    graphite_done_math   the Math questions they've done
    graphite_done_rw     the Reading and Writing questions they've done

New sets never draw a question on the list. When every question in a pool has been done, the pool's
questions come off the list (in the database and, on the same response, in the cookie) and the
student starts over.

The cookie is "1.<user id>.<bits>": bit n is set when the nth question of that section's bank
(in file order, items.jsonl or rw_items.jsonl) is done, as unpadded base64url, so all 1,000 Math
questions fit in about 170 characters. On the next request, questions in the cookie that the
database doesn't have yet (say, finished in another tab before a reload) are added to the list.
A cookie for a different user id is ignored, so a shared computer can't mix two students' lists.
website/src/site.js (GraphiteDone) reads and writes the same format for the offline preview.
"""
import base64
from functools import lru_cache

from ..db import execute, now_iso, query
from . import bank

VERSION = "1"
NAMES = {"math": "graphite_done_math", "rw": "graphite_done_rw"}
MAX_AGE = 400 * 24 * 3600  # the longest browsers keep a cookie (about 13 months)
# Requests that draw, check or submit questions: these read the cookies and write them back.
PATHS = ("/api/practice", "/api/mock-tests", "/api/levels", "/api/today", "/api/plan", "/api/review")


@lru_cache(maxsize=None)
def order(section):
    """Every question id in the section, in bank order, and each id's position."""
    ids = [q["id"] for q in bank.all_items().values() if q["section"] == section]
    return ids, {i: n for n, i in enumerate(ids)}


def encode(user_id, section, done):
    ids, pos = order(section)
    bits = bytearray((len(ids) + 7) // 8)
    for item_id in done:
        n = pos.get(item_id)
        if n is not None:
            bits[n // 8] |= 1 << (n % 8)
    body = base64.urlsafe_b64encode(bytes(bits)).decode().rstrip("=")
    return f"{VERSION}.{user_id}.{body}"


def decode(value, user_id, section):
    """The question ids in a cookie value, or an empty set if it's missing, malformed or another user's."""
    parts = (value or "").split(".")
    if len(parts) != 3 or parts[0] != VERSION or parts[1] != str(user_id):
        return set()
    try:
        bits = base64.urlsafe_b64decode(parts[2] + "=" * (-len(parts[2]) % 4))
    except (ValueError, TypeError):
        return set()
    ids, _ = order(section)
    return {ids[n] for n in range(min(len(ids), len(bits) * 8)) if bits[n // 8] >> (n % 8) & 1}


def wanted(path):
    return path.startswith(PATHS)


def absorb(user_id, cookies):
    """Adds questions the browser's cookies list as done, but the database doesn't, to the done list."""
    from_cookies = set()
    for section, name in NAMES.items():
        from_cookies |= decode(cookies.get(name), user_id, section)
    if not from_cookies:
        return 0
    have = {r["item_id"] for r in query("SELECT item_id FROM practice_seen WHERE user_id = ?", (user_id,))}
    stamp = now_iso()
    added = 0
    for item_id in sorted(from_cookies - have):
        execute("INSERT INTO practice_seen (user_id, item_id, seen_at) VALUES (?, ?, ?) "
                "ON CONFLICT (user_id, item_id) DO NOTHING", (user_id, item_id, stamp))
        added += 1
    return added


def attach(resp, user_id, secure):
    """Writes the student's current done list into both cookies on the response."""
    done = {r["item_id"] for r in query("SELECT item_id FROM practice_seen WHERE user_id = ?", (user_id,))}
    for section, name in NAMES.items():
        resp.set_cookie(name, encode(user_id, section, done), max_age=MAX_AGE, path="/", secure=secure,
                        httponly=False, samesite="Lax")
    return resp
