"""Copy warnings, first-party analytics and cookie consent records.

POST /api/integrity/copy   a student copied a question or pasted into one: warn, or email their parent
POST /api/analytics        page views, time on page, scroll depth and button clicks (only with analytics consent)
POST /api/consent          the visitor's cookie choice, kept as the record of consent
"""
import random

from flask import Blueprint, jsonify

from ..security import ApiError, body, current_user, login_required, rate_limited, record_event
from ..services import analytics, integrity

bp = Blueprint("integrity", __name__, url_prefix="/api")


@bp.post("/integrity/copy")
@login_required
def copied():
    me = current_user()
    if me["role"] == "parent":
        return jsonify({"action": "none"})
    data = body()
    kind = data.get("kind") if data.get("kind") in integrity.KINDS else "copy"
    page = str(data.get("page") or "")[:40]
    item = str(data.get("item_id") or "")[:80] or None
    try:
        chars = max(0, min(int(data.get("chars") or 0), 100000))
    except (TypeError, ValueError):
        chars = 0
    bucket = f"integrity:{me['id']}"
    if rate_limited(bucket, 60, 60):
        return jsonify({"action": "recorded"})
    record_event(bucket)
    return jsonify(integrity.record(me, kind, page, item, chars)), 201


@bp.post("/analytics")
def collect():
    data = body()
    events = data.get("events") if isinstance(data.get("events"), list) else []
    me = current_user()
    bucket = f"analytics:{analytics.visitor_id() or 'none'}"
    if rate_limited(bucket, 300, 60):
        return jsonify({"saved": 0}), 202
    record_event(bucket)
    saved = analytics.collect(events, me["id"] if me else None)
    if random.random() < 0.01:
        analytics.prune()
    return jsonify({"saved": saved}), 202


@bp.post("/consent")
def consent():
    data = body()
    if not isinstance(data.get("analytics"), bool):
        raise ApiError(400, "Say whether analytics cookies are on.", "analytics")
    try:
        version = int(data.get("version") or 1)
    except (TypeError, ValueError):
        version = 1
    me = current_user()
    vid = analytics.log_consent(data["analytics"], version, data.get("gpc") is True, data.get("path"), me["id"] if me else None)
    return jsonify({"ok": True, "visitor": vid}), 201
