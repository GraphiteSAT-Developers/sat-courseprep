"""The AI tutor: what it's told, and how a conversation from the page is checked before it goes to Qwen.

The page keeps the conversation and sends it whole with each question; nothing is stored here except one
rate_events row per answered question, which counts toward the plan's daily limit (services/access.py).
"""
from ..db import execute, query
from ..security import ApiError, check_clean
from .plans import TUTOR_DEMO

MAX_TURNS = 20          # the most recent messages sent along; older ones drop off
MAX_CHARS = 4000        # one message
MAX_TOTAL = 16000       # the whole conversation
PER_MINUTE = 8          # a burst limit on top of the plan's daily one, so a stuck key can't run up the bill


def demo(student_id):
    """The free plan's demo: {left, total}. Used questions are kept on the account, so it never starts over."""
    row = query("SELECT tutor_demo_used FROM users WHERE id = ?", (student_id,), one=True)
    return {"left": max(0, TUTOR_DEMO - (row["tutor_demo_used"] if row else TUTOR_DEMO)), "total": TUTOR_DEMO}


def use_demo(student_id):
    execute("UPDATE users SET tutor_demo_used = tutor_demo_used + 1 WHERE id = ?", (student_id,))

SYSTEM = """You are the Graphite SAT tutor, helping a high school student with Digital SAT Math.

How you teach:
- Hints come one step at a time. Start with a nudge: a short question back that points at the next step.
- If they're still stuck, name the method that fits (by hand or in Desmos) without doing it for them.
- Give the full solution only when they ask for it or have tried twice. Then show every step and say why each tempting wrong choice is wrong.
- When Desmos is faster, say exactly what to type, one expression per line, and what to look for on the graph.
- If they share their work, find the first line that went wrong and ask about that line.
- Keep replies short: a few sentences, or a short list of steps. Write math in plain text, like x^2 + 3x = 10.
- Be warm and direct. Never make them feel slow.

Stay on SAT prep and study habits. If asked about something else, steer back kindly. Never help on a test that's
being timed or graded right now. You can make mistakes, so when you're unsure, say so."""


def _about(context):
    if not isinstance(context, dict):
        return ""
    title = str(context.get("title") or "")[:200].strip()
    detail = str(context.get("detail") or "")[:300].strip()
    if not title:
        return ""
    return f"\n\nThe student picked this to talk about: {title}" + (f" ({detail})" if detail else "") + "."


def conversation(messages, context=None):
    """Checks what the page sent and returns the messages for Qwen, system prompt first."""
    if not isinstance(messages, list) or not messages:
        raise ApiError(400, "Ask the tutor something first.", "messages")
    out, total = [], 0
    for m in messages[-MAX_TURNS:]:
        if not isinstance(m, dict) or m.get("role") not in ("user", "assistant") or not isinstance(m.get("content"), str):
            raise ApiError(400, "Each message needs a role (user or assistant) and some text.", "messages")
        text = m["content"].strip()[:MAX_CHARS]
        if not text:
            continue
        if m["role"] == "user":
            check_clean(text, "message")
        total += len(text)
        out.append({"role": m["role"], "content": text})
    if not out or out[-1]["role"] != "user":
        raise ApiError(400, "Ask the tutor something first.", "messages")
    while total > MAX_TOTAL and len(out) > 1:  # drop the oldest until it fits
        total -= len(out.pop(0)["content"])
    if out[0]["role"] == "assistant":
        out.pop(0)
    return [{"role": "system", "content": SYSTEM + _about(context)}] + out
