"""The score check: 20 questions without an account, scored like the SAT (services/scorecheck.py).

The questions come with a signed token that names them, so grading can only reveal the answers to a
check someone was actually given, once. Each address can start a few checks an hour.
"""
import time

from flask import Blueprint, current_app, jsonify
from itsdangerous import BadSignature, URLSafeSerializer

from ..security import ApiError, body, client_ip, hash_text, rate_limited, record_event
from ..services import scorecheck

bp = Blueprint("score_check", __name__, url_prefix="/api/score-check")

CHECKS_PER_HOUR = 10
TOKEN_MAX_AGE = 3 * 60 * 60  # seconds to finish a check


def _signer():
    return URLSafeSerializer(current_app.config["SECRET_KEY"], salt="graphite-score-check")


@bp.get("")
def start():
    bucket = "score-check:" + hash_text(client_ip())
    if rate_limited(bucket, CHECKS_PER_HOUR, 60):
        raise ApiError(429, "That's a lot of score checks in an hour. Try again later, or make a free account to keep practicing.",
                       code="rate_limited")
    record_event(bucket)
    ids = scorecheck.pick()
    return jsonify({"token": _signer().dumps({"ids": ids, "t": int(time.time())}), "questions": scorecheck.questions(ids)})


def _keyed(raw, n):
    out = {}
    for k, v in (raw if isinstance(raw, dict) else {}).items():
        try:
            i = int(k)
        except (TypeError, ValueError):
            continue
        if 0 <= i < n:
            out[i] = v
    return out


@bp.post("/grade")
def grade():
    data = body()
    try:
        token = _signer().loads(str(data.get("token") or ""))
    except BadSignature:
        raise ApiError(400, "That score check has expired. Start a new one.", code="expired")
    if not isinstance(token, dict) or time.time() - token.get("t", 0) > TOKEN_MAX_AGE:
        raise ApiError(400, "That score check has expired. Start a new one.", code="expired")
    done = "score-check-graded:" + hash_text(str(data.get("token")))
    if rate_limited(done, 1, TOKEN_MAX_AGE // 60):
        raise ApiError(409, "This score check was already scored. Start a new one to try again.", code="already_graded")
    ids = token["ids"]
    items = scorecheck.bank.all_items()
    if not ids or any(i not in items for i in ids):
        raise ApiError(400, "That score check has expired. Start a new one.", code="expired")
    answers = {}
    for i, v in _keyed(data.get("answers"), len(ids)).items():
        a = scorecheck.bank.clean_answer(items[ids[i]], v)
        if a is not None:
            answers[i] = a
    sure = {i: bool(v) for i, v in _keyed(data.get("sure"), len(ids)).items()}
    record_event(done)
    return jsonify({"result": scorecheck.grade(ids, answers, sure)})
