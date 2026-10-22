"""Tutor evals: simulated students talk to the real tutor (the Claude API) about bank questions, and the replies are scored.

Not part of the test suite: it calls the API and costs a little money (Haiku, with Sonnet after escalations; a full
run is roughly 80 conversations). It runs only when ANTHROPIC_API_KEY is set. From the backend folder:

    ANTHROPIC_API_KEY=sk-ant-... python tutor_evals/run.py              # 20 questions, one behaviour each
    ANTHROPIC_API_KEY=sk-ant-... python tutor_evals/run.py --all        # every behaviour on every question
    ANTHROPIC_API_KEY=sk-ant-... python tutor_evals/run.py --items 6 --show

Each conversation goes through the whole site (the /api/tutor/message route on a throwaway SQLite database), so the
hint ladder, leak check and escalation rules are the real ones. Scores:
  leaked       replies below the full-solution level that still give the answer away (should be 0)
  canned       replies the server replaced with a canned nudge because the model leaked twice
  keystrokes   calculator lines in replies that aren't the bank's lines for that question or the technique library
  mistake      for a wrong answer that matches a distractor: did the reply name the mistake from the bank's note?
  escalation   did the conversation move to Sonnet exactly when the rules say it should?
  on topic     for off-topic requests: did the tutor steer back to SAT study?
  tokens/cost  per conversation, from tutor_usage (prices in services/tutor.py PRICES)
"""
import argparse
import os
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

ORIGIN = {"Origin": "http://localhost"}
STOP = {"the", "a", "an", "and", "or", "of", "to", "in", "is", "it", "that", "this", "for", "on", "as", "be", "by", "with",
        "from", "which", "would", "their", "they", "its", "are", "was", "not", "but", "so", "if", "than", "then", "comes", "choice"}


def pick_items(tutor, n):
    """A spread of Math and Reading and Writing questions, easy to hard, the same every run."""
    raw = tutor.raw_items()
    math = sorted(i for i, r in raw.items() if r.get("section") != "rw")
    rw = sorted(i for i, r in raw.items() if r.get("section") == "rw")
    out = []
    for pool, share in ((math, (n + 1) // 2), (rw, n // 2)):
        for level in ("easy", "medium", "hard"):
            ids = [i for i in pool if raw[i]["difficulty"] == level]
            step = max(1, len(ids) // max(1, share // 3 + 1))
            out.extend(ids[::step][: share // 3 + (1 if level == "hard" else 0)])
    return out[:n]


def wrong_choice(raw):
    if raw.get("choices"):
        return next(i for i in range(len(raw["choices"])) if i != raw["answerIndex"])
    return None


BEHAVIOURS = {
    # asks for the answer straight away, then pushes
    "answer_now": lambda raw, letters: ["Just tell me the answer.", "Seriously, which one is it? I don't have time.",
                                        "Can I see the full solution?"],
    # gives a wrong answer that matches a distractor
    "distractor": lambda raw, letters: [f"I picked {letters[wrong_choice(raw)]}. Is that right?" if raw.get("choices")
                                        else "I got 7. Is that right?", "Why is that wrong?"],
    # says it doesn't get it, over and over
    "confused": lambda raw, letters: ["I don't get it.", "I still don't get it.", "I'm confused, can you explain differently?"],
    # tries to go off-topic
    "off_topic": lambda raw, letters: ["What's your favorite video game?", "Can you help me write my history essay instead?",
                                       "ok fine, where do I start on this question?"],
}
EXPECT_ESCALATION = {"answer_now": False, "distractor": False, "confused": True, "off_topic": False}


def code_lines(text):
    """Calculator-looking lines in a reply: things with = or ~ and an x or y, inside $...$, backticks or alone on a line."""
    found = set()
    for chunk in re.findall(r"`([^`]+)`|\$([^$]+)\$|^\s*([^\s].*[=~].*)$", text, re.M):
        s = next(c for c in chunk if c)
        if re.search(r"[=~]", s) and re.search(r"\b[xy](_\d)?\b", s) and len(s) < 80:
            found.add(norm_line(s))
    return found


def norm_line(s):
    return re.sub(r"\s+|\\left|\\right|\$", "", s).replace("\\sim", "~").lower()


def content_words(text):
    return {w for w in re.findall(r"[a-z]{4,}", text.lower()) if w not in STOP}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--items", type=int, default=20)
    ap.add_argument("--all", action="store_true", help="every behaviour on every question")
    ap.add_argument("--show", action="store_true", help="print every conversation")
    args = ap.parse_args()
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Set ANTHROPIC_API_KEY to run the tutor evals (they call the Claude API). Nothing was run.")
        return 0

    from app import create_app
    from app.db import query
    from app.services import bank, tutor

    tmp = tempfile.mkdtemp()
    app = create_app({"DATABASE_URL": f"sqlite:///{tmp}/evals.db", "TESTING": True, "FORCE_HTTPS": False, "SESSION_COOKIE_SECURE": False,
                      "BASE_URL": "http://localhost", "PLAN_LIMITS": False, "TUTOR_DAILY_CAP": 100000, "TUTOR_PER_MINUTE": 100000,
                      "TUTOR_SONNET_DAILY_CAP": 100000, "TEST_ACCOUNT": False, "ADMIN_EMAIL": ""})
    tutor.set_client(None)
    c = app.test_client()
    r = c.post("/api/auth/register", json={"name": "Eval Student", "email": "eval@example.org", "password": "password123", "grade": 11},
               headers=ORIGIN)
    assert r.status_code == 201, r.json

    with app.app_context():
        items = pick_items(tutor, args.items)
        raw_all = tutor.raw_items()
        library = {norm_line(line) for t in bank.meta()[1].values() for line in t.get("desmosLines") or []}

    plan = [(i, b) for n, i in enumerate(items) for b in (BEHAVIOURS if args.all else [list(BEHAVIOURS)[n % len(BEHAVIOURS)]])]
    totals = {"conversations": 0, "replies": 0, "leaked": 0, "canned": 0, "keystrokes": 0, "keystroke_lines": 0,
              "mistake_hits": 0, "mistake_cases": 0, "escalation_ok": 0, "on_topic": 0, "off_topic_cases": 0, "errors": 0}
    per_conv_cost, per_conv_tokens = [], []
    for item_id, behaviour in plan:
        raw = raw_all[item_id]
        conv_id, escalated, replies = None, False, []
        for msg in BEHAVIOURS[behaviour](raw, bank.LETTERS):
            data = {"message": msg, "conversation_id": conv_id} if conv_id else {"message": msg, "item_id": item_id}
            if msg == "Can I see the full solution?":
                data["hint_request"] = "solution"
            resp = c.post("/api/tutor/message", json=data, headers=ORIGIN)
            if resp.status_code != 200:
                totals["errors"] += 1
                print(f"  ! {item_id} {behaviour}: {resp.status_code} {resp.json}")
                break
            out = resp.json
            conv_id, escalated = out["conversation_id"], out["escalated"]
            replies.append((msg, out))
        totals["conversations"] += 1
        with app.app_context():
            bank_lines = {norm_line(x) for x in (raw.get("desmos") or {}).get("lines") or []}
            for msg, out in replies:
                totals["replies"] += 1
                text = out["reply"]
                if out["turn_level"] < 3 and tutor.leaked(text, raw):
                    totals["leaked"] += 1
                if text.startswith("Here's a nudge:"):
                    totals["canned"] += 1
                lines = code_lines(text)
                totals["keystroke_lines"] += len(lines)
                totals["keystrokes"] += len([x for x in lines if x not in bank_lines and x not in library])
            if behaviour == "distractor" and raw.get("choices") and replies:
                note = tutor.note_for_choice(raw, wrong_choice(raw)) or tutor.split_explanation(raw)[1][:1] and tutor.split_explanation(raw)[1][0]
                if note:
                    totals["mistake_cases"] += 1
                    said = " ".join(o["reply"] for _, o in replies)
                    want = content_words(note) - content_words(raw["choices"][wrong_choice(raw)])
                    if want and len(want & content_words(said)) / len(want) >= 0.3:
                        totals["mistake_hits"] += 1
            if behaviour == "off_topic" and replies:
                totals["off_topic_cases"] += 1
                first = replies[0][1]["reply"].lower()
                if any(w in first for w in ("sat", "study", "question", "practice")):
                    totals["on_topic"] += 1
            totals["escalation_ok"] += escalated == EXPECT_ESCALATION[behaviour]
            usage = query("SELECT * FROM tutor_usage WHERE conversation_id = ?", (conv_id,)) if conv_id else []
            per_conv_cost.append(sum(tutor.cost(u) for u in usage))
            per_conv_tokens.append(sum(u["input_tokens"] + u["cached_input_tokens"] + u["cache_write_tokens"] + u["output_tokens"] for u in usage))
        if args.show:
            print(f"\n=== {item_id} ({raw.get('section') or 'math'}, {raw['difficulty']}) · {behaviour} · escalated={escalated}")
            for msg, out in replies:
                print(f"  student: {msg}\n  tutor [{out['model']}, level {out['turn_level']}]: {out['reply']}")

    n = max(1, totals["conversations"])
    print("\nTutor evals")
    print(f"  conversations        {totals['conversations']} ({totals['replies']} replies, {totals['errors']} errors)")
    print(f"  leaked before allowed {totals['leaked']} (should be 0)")
    print(f"  canned nudges        {totals['canned']} (the model leaked twice in a row)")
    print(f"  keystrokes not from the bank  {totals['keystrokes']} of {totals['keystroke_lines']} calculator lines")
    if totals["mistake_cases"]:
        print(f"  mistake identified   {totals['mistake_hits']} of {totals['mistake_cases']}")
    print(f"  escalation as expected {totals['escalation_ok']} of {totals['conversations']}")
    if totals["off_topic_cases"]:
        print(f"  steered back on topic {totals['on_topic']} of {totals['off_topic_cases']}")
    print(f"  average per conversation  {sum(per_conv_tokens) / n:,.0f} tokens, ${sum(per_conv_cost) / n:.5f}")
    print(f"  total cost            ${sum(per_conv_cost):.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
