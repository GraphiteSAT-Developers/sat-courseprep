"""The AI tutor: prompt building, the hint ladder, the leak check, timed tests, escalation, credits, safety and errors.
The Anthropic client is a fake, so nothing goes over the network. Run from the backend folder:
python -m unittest discover tests"""
import json
import shutil
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from fractions import Fraction
from types import SimpleNamespace

import anthropic
import httpx2

from app import create_app
from app.db import execute, now_iso, query
from app.services import mailer, tutor
from test_practice import ORIGIN

MATH_MC = "sample-tangent-system"     # B. Exactly one
MATH_SPR = "sample-positive-root"     # 2/3
RW = "rw-bnd-001"                     # B. food. The


def response(text="What did you try first?", stop="end_turn", usage=(1200, 3000, 0, 60)):
    return SimpleNamespace(content=[SimpleNamespace(type="text", text=text)], stop_reason=stop, model="x",
                           usage=SimpleNamespace(input_tokens=usage[0], cache_read_input_tokens=usage[1],
                                                 cache_creation_input_tokens=usage[2], output_tokens=usage[3]))


class FakeClient:
    """Stands in for anthropic.Anthropic(): replies come from a queue (the last one repeats)."""

    def __init__(self, *replies):
        self.replies = list(replies) or [response()]
        self.calls = []
        self.messages = self

    def create(self, **kwargs):
        self.calls.append(kwargs)
        r = self.replies.pop(0) if len(self.replies) > 1 else self.replies[0]
        if isinstance(r, Exception):
            raise r
        return r

    def instruction(self, i=-1):
        return self.calls[i]["messages"][-1]["content"]


class Base(unittest.TestCase):
    config = {}

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        cfg = {"DATABASE_URL": f"sqlite:///{self.dir}/test.db", "TESTING": True, "FORCE_HTTPS": False,
               "SESSION_COOKIE_SECURE": False, "BASE_URL": "http://localhost", "ANTHROPIC_API_KEY": "test-key",
               "ADMIN_EMAIL": "admin@example.com"}
        cfg.update(self.config)
        self.app = create_app(cfg)
        self.client = self.app.test_client()
        self.fake = FakeClient()
        tutor.set_client(self.fake)
        r = self.post("/api/auth/register", {"name": "Maya Rivera", "email": "maya@school.org", "password": "password123", "grade": 11})
        self.assertEqual(r.status_code, 201, r.json)
        self.uid = r.json["user"]["id"]

    def tearDown(self):
        tutor.set_client(None)
        shutil.rmtree(self.dir, ignore_errors=True)

    def post(self, url, data=None):
        return self.client.post(url, json=data or {}, headers=ORIGIN)

    def ask(self, message="I'm not sure where to start", **kw):
        return self.post("/api/tutor/message", dict(kw, message=message))

    def sql(self, text, params=()):
        with self.app.app_context():
            return execute(text, params)

    def rows(self, text, params=()):
        with self.app.app_context():
            return query(text, params)

    def submit_answer(self, item_id, answer, correct):
        self.sql("INSERT INTO question_log (user_id, item_id, source, ref, answer, correct, day, at) VALUES (?, ?, 'practice', 'p', ?, ?, ?, ?)",
                 (self.uid, item_id, answer, 1 if correct else 0, now_iso()[:10], now_iso()))


class OffSwitchTest(Base):
    config = {"ANTHROPIC_API_KEY": ""}

    def test_no_key_keeps_coming_soon(self):
        r = self.client.get("/api/tutor")
        self.assertEqual(r.status_code, 200)
        self.assertFalse(r.json["enabled"])
        r = self.ask()
        self.assertEqual((r.status_code, r.json["code"]), (503, "tutor_off"))
        self.assertEqual(self.fake.calls, [])

    def test_switch_off_with_a_key(self):
        self.app.config.update(ANTHROPIC_API_KEY="k", TUTOR_ENABLED=False)
        self.assertFalse(self.client.get("/api/tutor").json["enabled"])
        self.assertEqual(self.ask().status_code, 503)

    def test_signed_out(self):
        self.post("/api/auth/logout")
        self.assertEqual(self.client.get("/api/tutor").status_code, 401)


class PromptTest(Base):
    def test_math_prompt(self):
        r = self.ask("I got exactly two", item_id=MATH_MC, calculator=["y=x^2-6x+11", "y=2x-5"])
        self.assertEqual(r.status_code, 200, r.json)
        call = self.fake.calls[0]
        self.assertEqual(call["model"], tutor.HAIKU)
        self.assertEqual(call["output_config"], {"effort": "low"})
        self.assertLessEqual(call["max_tokens"], 1024)
        stable, item = call["system"]
        self.assertEqual(stable["cache_control"], {"type": "ephemeral"})
        self.assertEqual(item["cache_control"], {"type": "ephemeral"})
        self.assertIn("CALCULATOR RULES", stable["text"])
        self.assertIn("T1 Graph both sides", stable["text"])
        self.assertIn("988", stable["text"])
        self.assertIn("VERIFIED ANSWER KEY (never reveal below the full-solution level): B. Exactly one", item["text"])
        self.assertIn("y=x^2-6x+11\ny=2x-5", item["text"])
        self.assertIn("TECHNIQUE T2", item["text"])
        self.assertIn("Exactly two assumes a line always crosses a parabola twice", item["text"])
        # The student's message, then their calculator, then the server's turn instruction.
        user, sysmsg = call["messages"][-2:]
        self.assertEqual(user["role"], "user")
        self.assertEqual(user["content"][0]["text"], "I got exactly two")
        self.assertIn("y=2x-5", user["content"][1]["text"])
        self.assertEqual(sysmsg["role"], "system")
        self.assertIn("NUDGE", sysmsg["content"])
        self.assertIn("The bank's note on that choice: Exactly two assumes", sysmsg["content"])
        # Nothing identifying goes to the API.
        blob = json.dumps(call, default=str)
        self.assertNotIn("Maya", blob)
        self.assertNotIn("maya@school.org", blob)
        # Both prompts stay the same across turns, so they're cached.
        self.ask("ok what next?", conversation_id=r.json["conversation_id"])
        self.assertEqual(self.fake.calls[1]["system"], call["system"])
        self.assertEqual([m["role"] for m in self.fake.calls[1]["messages"]], ["user", "assistant", "user", "system"])

    def test_reading_and_writing_prompt(self):
        self.ask("help", item_id=RW)
        item = self.fake.calls[0]["system"][1]["text"]
        self.assertIn("Reading and Writing", item)
        self.assertIn("Honeybees perform a \"waggle dance\"", item)
        self.assertIn("SKILL TIP: Find the subject and verb", item)
        self.assertIn("SKILL TRAP:", item)
        self.assertIn("B. food. The", item)
        self.assertNotIn("DESMOS", item)

    def test_free_form_stays_on_sat(self):
        r = self.ask("How should I plan my week?")
        self.assertEqual(r.status_code, 200)
        self.assertIn("NO BANK QUESTION", self.fake.calls[0]["system"][1]["text"])
        self.assertIn("Stay on SAT and school study", self.fake.calls[0]["system"][0]["text"])

    def test_unknown_item(self):
        self.assertEqual(self.ask(item_id="not-a-question").json["code"], "unknown_item")

    def test_conversation_continues_and_is_private(self):
        cid = self.ask("hi", item_id=MATH_MC).json["conversation_id"]
        self.ask("and then?", conversation_id=cid)
        conv = self.client.get(f"/api/tutor/conversations/{cid}").json["conversation"]
        self.assertEqual([m["role"] for m in conv["messages"]], ["user", "assistant", "user", "assistant"])
        self.assertEqual(self.client.get(f"/api/tutor?item_id={MATH_MC}").json["conversation"]["id"], cid)
        # stored encrypted
        raw = self.rows("SELECT content FROM tutor_messages WHERE conversation_id = ?", (cid,))
        self.assertTrue(all(r["content"].startswith("enc1:") for r in raw))
        # another student can't read it
        self.post("/api/auth/logout")
        self.post("/api/auth/register", {"name": "Other Kid", "email": "other@school.org", "password": "password123", "grade": 10})
        self.assertEqual(self.client.get(f"/api/tutor/conversations/{cid}").status_code, 404)
        self.assertEqual(self.ask("hi", conversation_id=cid).status_code, 404)


class HintLadderTest(Base):
    def test_solution_waits_for_the_method_or_a_submission(self):
        r = self.ask(hint_request="solution", message="", item_id=MATH_MC)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json["turn_level"], 2)  # the method instead
        self.assertIn("METHOD", self.fake.instruction())
        self.assertIn("unlocks only after", self.fake.instruction())
        self.assertTrue(r.json["solution_allowed"])  # had the method, so asking again opens it
        cid = r.json["conversation_id"]
        r = self.ask(hint_request="solution", message="", conversation_id=cid)
        self.assertEqual((r.json["turn_level"], r.json["hint_level"]), (3, 3))
        self.assertIn("FULL SOLUTION", self.fake.instruction())

    def test_nudge_then_method(self):
        r = self.ask(hint_request="nudge", message="", item_id=MATH_SPR)
        self.assertEqual(r.json["hint_level"], 1)
        self.assertFalse(r.json["solution_allowed"])
        r = self.ask(hint_request="method", message="", conversation_id=r.json["conversation_id"])
        self.assertEqual(r.json["hint_level"], 2)

    def test_submitted_answer_opens_the_solution(self):
        self.submit_answer(MATH_MC, "2", False)  # stored as the choice index
        r = self.ask(hint_request="solution", message="", item_id=MATH_MC)
        self.assertEqual(r.json["turn_level"], 3)
        self.assertIn("They submitted C (Exactly two) on the site, which was wrong", self.fake.instruction())

    def test_bad_hint(self):
        self.assertEqual(self.ask(hint_request="everything").json["code"], "bad_hint")


class LeakCheckTest(Base):
    def test_multiple_choice_letter_and_text(self):
        with self.app.app_context():
            raw = tutor.raw_items()[MATH_MC]
            for text in ("The answer is B.", "It's B!", "(B) is right", "B is correct", "Go with choice B",
                         "There's exactly one solution.", "Pick $B$"):
                self.assertTrue(tutor.leaked(text, raw), text)
            for text in ("What happens when you set the equations equal?", "Choice A says zero. Why might that be?",
                         "Zoom out to see every crossing.", "A line can cross a parabola how many times?"):
                self.assertFalse(tutor.leaked(text, raw), text)
            rw = tutor.raw_items()[RW]
            self.assertTrue(tutor.leaked("So it should read food. The direction...", rw))
            self.assertFalse(tutor.leaked("Can each side of the blank stand alone as a sentence?", rw))

    def test_typed_answer_forms(self):
        with self.app.app_context():
            raw = tutor.raw_items()[MATH_SPR]
            for text in ("x = 2/3", "The answer is $\\frac{2}{3}$", "It's \\dfrac{2}{3}", "about 0.667", "enter .6667",
                         "x is .67", "so x = 0.6666"):
                self.assertTrue(tutor.leaked(text, raw), text)
            for text in ("Factor $6x^2 - x - 2$. What two numbers multiply to $-12$?", "Click the positive x-intercept."):
                self.assertFalse(tutor.leaked(text, raw), text)
            neg = tutor.raw_items()["sample-tilde-constants"]  # b = -1
            self.assertTrue(tutor.leaked("so b = -1", neg))
            self.assertFalse(tutor.leaked("Match the x terms: -6 + c. What must c be?", neg))
            self.assertEqual(tutor.number_forms(Fraction(-15, 2)), ["-15/2", "-7.5"])

    def test_leaky_reply_is_rewritten_then_replaced(self):
        self.fake.replies = [response("The answer is B."), response("What does the discriminant tell you?")]
        r = self.ask("help me", item_id=MATH_MC)
        self.assertEqual(r.json["reply"], "What does the discriminant tell you?")
        self.assertEqual(len(self.fake.calls), 2)
        self.assertIn("your last draft gave the answer away", self.fake.instruction())
        self.fake.replies = [response("It's B."), response("Definitely exactly one.")]
        r = self.ask("help me", conversation_id=r.json["conversation_id"])
        self.assertTrue(r.json["reply"].startswith("Here's a nudge:"))
        self.assertNotIn("Exactly one", r.json["reply"])
        conv = self.rows("SELECT leak_failures FROM tutor_conversations")[0]
        self.assertEqual(conv["leak_failures"], 3)
        usage = self.rows("SELECT calls, input_tokens, output_tokens FROM tutor_usage ORDER BY id")
        self.assertEqual([u["calls"] for u in usage], [2, 2])
        self.assertEqual(usage[0]["input_tokens"], 2400)

    def test_full_solution_is_not_checked(self):
        self.submit_answer(MATH_MC, "0", False)
        self.fake.replies = [response("The answer is B: exactly one solution.")]
        r = self.ask(hint_request="solution", message="", item_id=MATH_MC)
        self.assertEqual(r.json["reply"], "The answer is B: exactly one solution.")
        self.assertEqual(len(self.fake.calls), 1)


class TimedTestTest(Base):
    def session(self, ids, created, minutes=35, submitted=None):
        self.sql("INSERT INTO practice_sessions (user_id, mode, title, item_ids, minutes, created_at, submitted_at) "
                 "VALUES (?, 'test', 'Math', ?, ?, ?, ?)", (self.uid, json.dumps(ids), minutes, created, submitted))

    def test_running_test_blocks_everything(self):
        self.session([MATH_MC], now_iso())
        r = self.ask("what's the answer", item_id=MATH_SPR)
        self.assertEqual((r.status_code, r.json["code"]), (403, "timed_test"))
        self.assertEqual(self.ask("free-form question").status_code, 403)
        self.assertEqual(self.fake.calls, [])

    def test_unsubmitted_test_blocks_its_questions(self):
        old = (datetime.now(timezone.utc) - timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
        self.session([MATH_MC], old)
        self.assertEqual(self.ask("help", item_id=MATH_MC).json["code"], "timed_test")
        self.assertEqual(self.ask("help", item_id=MATH_SPR).status_code, 200)
        self.sql("UPDATE practice_sessions SET submitted_at = ?", (now_iso(),))
        self.assertEqual(self.ask("help", item_id=MATH_MC).status_code, 200)

    def test_mock_test_waits_for_module_2(self):
        self.session([MATH_MC], now_iso(), submitted=now_iso())  # module 1 done
        sid = self.rows("SELECT id FROM practice_sessions")[0]["id"]
        self.sql("INSERT INTO mock_tests (user_id, section, status, m1_session, created_at) VALUES (?, 'math', 'break', ?, ?)",
                 (self.uid, sid, now_iso()))
        self.assertEqual(self.ask("help", item_id=MATH_MC).json["code"], "timed_test")
        self.sql("UPDATE mock_tests SET status = 'done'")
        self.assertEqual(self.ask("help", item_id=MATH_MC).status_code, 200)

    def test_speed_round(self):
        ms = int(datetime.now(timezone.utc).timestamp() * 1000)
        self.sql("INSERT INTO speed_runs (user_id, day, item_ids, started_ms, total, created_at) VALUES (?, ?, ?, ?, 10, ?)",
                 (self.uid, now_iso()[:10], json.dumps([MATH_MC]), ms, now_iso()))
        self.assertEqual(self.ask("help", item_id=MATH_MC).json["code"], "timed_test")


class EscalationTest(Base):
    def models(self):
        return [c["model"] for c in self.fake.calls]

    def test_stuck_twice(self):
        cid = self.ask("I'm stuck", item_id=MATH_MC).json["conversation_id"]
        r = self.ask("I still don't get it", conversation_id=cid)
        self.assertEqual(self.models(), [tutor.HAIKU, tutor.SONNET])
        self.assertTrue(r.json["escalated"])
        self.assertEqual(r.json["model"], tutor.SONNET)
        self.ask("ok thanks", conversation_id=cid)
        self.assertEqual(self.models()[-1], tutor.SONNET)  # stays on Sonnet
        models = self.rows("SELECT model FROM tutor_messages WHERE role = 'assistant' ORDER BY id")
        self.assertEqual([m["model"] for m in models], [tutor.HAIKU, tutor.SONNET, tutor.SONNET])

    def test_wrong_after_the_method(self):
        cid = self.ask(hint_request="method", message="", item_id=MATH_MC).json["conversation_id"]
        self.ask("Is it C?", conversation_id=cid)
        self.assertEqual(self.models(), [tutor.HAIKU, tutor.SONNET])

    def test_right_after_the_method_stays_on_haiku(self):
        cid = self.ask(hint_request="method", message="", item_id=MATH_MC).json["conversation_id"]
        self.ask("Is it B?", conversation_id=cid)
        self.assertEqual(self.models(), [tutor.HAIKU, tutor.HAIKU])

    def test_long_conversation(self):
        self.app.config["TUTOR_PER_MINUTE"] = 20
        cid = self.ask("hi", item_id=MATH_MC).json["conversation_id"]
        for _ in range(7):
            self.ask("next step?", conversation_id=cid)
        self.assertEqual(set(self.models()), {tutor.HAIKU})
        self.ask("next step?", conversation_id=cid)  # turn 9
        self.assertEqual(self.models()[-1], tutor.SONNET)

    def test_leak_failures(self):
        self.fake.replies = [response("It's B."), response("The answer is B.")]
        cid = self.ask("help", item_id=MATH_MC).json["conversation_id"]
        self.fake.replies = [response("What do you notice?")]
        self.ask("ok", conversation_id=cid)
        self.assertEqual(self.models()[-1], tutor.SONNET)

    def test_daily_sonnet_cap(self):
        self.app.config["TUTOR_SONNET_DAILY_CAP"] = 1
        cid = self.ask("I'm stuck", item_id=MATH_MC).json["conversation_id"]
        self.ask("I'm confused", conversation_id=cid)
        r = self.ask("still lost", conversation_id=cid)
        self.assertEqual(self.models(), [tutor.HAIKU, tutor.SONNET, tutor.HAIKU])
        self.assertTrue(r.json["escalated"])
        self.assertEqual(r.json["model"], tutor.HAIKU)


class CreditsTest(Base):
    def fill(self, n, model=tutor.HAIKU, at=None):
        for _ in range(n):
            self.sql("INSERT INTO tutor_usage (user_id, model, charged, day, at) VALUES (?, ?, 1, ?, ?)",
                     (self.uid, model, now_iso()[:10], at or now_iso()))

    def test_free_plan_has_30_a_month(self):
        r = self.ask("hi")
        self.assertEqual((r.json["credits"]["left"], r.json["credits"]["limit"]), (29, 30))
        self.fill(29)
        r = self.ask("hi")
        self.assertEqual((r.status_code, r.json["code"]), (402, "plan_required"))
        self.assertEqual(r.json["error"], "You've used all 30 of your tutor credits this month. Mechanical includes more.")
        self.assertEqual(r.json["lock"]["need"], "mechanical")
        self.assertFalse(self.client.get("/api/tutor").json["credits"]["ok"])

    def test_last_month_does_not_count(self):
        old = (datetime.now(timezone.utc).replace(day=1) - timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
        self.fill(30, at=old)
        self.assertEqual(self.ask("hi").status_code, 200)

    def test_mechanical_is_unlimited_with_a_daily_cap(self):
        self.post("/api/me/subscription/plan", {"plan": "mechanical", "interval": "month", "agree": True})
        self.fill(40)
        r = self.ask("hi")
        self.assertEqual(r.status_code, 200, r.json)
        self.assertTrue(r.json["credits"]["unlimited"])
        self.app.config["TUTOR_DAILY_CAP"] = 41
        r = self.ask("hi")
        self.assertEqual((r.status_code, r.json["code"]), (429, "tutor_daily_cap"))

    def test_burst_limit(self):
        self.app.config["TUTOR_PER_MINUTE"] = 2
        self.ask("one")
        self.ask("two")
        self.assertEqual(self.ask("three").json["code"], "rate_limited")

    def test_errors_and_refusals_are_free(self):
        self.fake.replies = [anthropic.APIConnectionError(request=httpx2.Request("POST", "https://api.anthropic.com/v1/messages"))]
        r = self.ask("hi", item_id=MATH_MC)
        self.assertEqual((r.status_code, r.json["code"]), (503, "tutor_unavailable"))
        self.assertIn("try again", r.json["error"])
        self.assertNotIn("Traceback", r.get_data(as_text=True))
        self.assertEqual(self.rows("SELECT COUNT(*) AS n FROM tutor_messages")[0]["n"], 0)
        self.fake.replies = [response("", stop="refusal")]
        r = self.ask(hint_request="method", message="", item_id=MATH_MC)
        self.assertEqual(r.json["reply"], tutor.REFUSAL_MESSAGE)
        self.assertEqual(r.json["credits"]["used"], 0)
        self.assertEqual(r.json["hint_level"], 0)  # a refusal doesn't count as having had the method
        self.assertFalse(r.json["solution_allowed"])
        self.fake.replies = [RuntimeError("boom")]
        self.assertEqual(self.ask("hi").status_code, 503)


class SafetyTest(Base):
    def test_crisis_message_is_not_tutored(self):
        mailer.OUTBOX.clear()
        r = self.ask("honestly i want to kill myself", item_id=MATH_MC)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json["safety"])
        self.assertIn("988", r.json["reply"])
        self.assertEqual(self.fake.calls, [])
        conv = self.rows("SELECT flagged, flag_reason FROM tutor_conversations")[0]
        self.assertEqual((conv["flagged"], conv["flag_reason"]), (1, "safety"))
        self.assertEqual(mailer.OUTBOX[-1]["to"], "admin@example.com")
        self.assertNotIn("Maya", mailer.OUTBOX[-1]["text"])
        self.assertEqual(r.json["credits"]["used"], 0)

    def test_everyday_math_words_are_fine(self):
        for text in ("This question is killing me lol", "How do I cut the passage down to the main idea?"):
            self.assertIsNone(tutor.CRISIS.search(text), text)
        for text in ("I don't want to live anymore", "my dad hits me", "I've been cutting myself"):
            self.assertIsNotNone(tutor.CRISIS.search(text), text)

    def test_curse_words(self):
        r = self.ask("this is shit")
        self.assertEqual((r.status_code, r.json["code"]), (400, "blocked_word"))

    def test_long_messages(self):
        self.assertEqual(self.ask("x" * 1501).json["code"], "too_long")


class DataTest(Base):
    def test_retention_export_and_delete(self):
        cid = self.ask("hi", item_id=MATH_MC).json["conversation_id"]
        data = json.loads(self.client.get("/api/me/export").get_data(as_text=True))
        self.assertEqual(data["tutor_messages"][0]["content"], "hi")  # decrypted in the export
        self.assertEqual(len(data["tutor_usage"]), 1)
        old = (datetime.now(timezone.utc) - timedelta(days=91)).strftime("%Y-%m-%dT%H:%M:%SZ")
        self.sql("UPDATE tutor_conversations SET updated_at = ? WHERE id = ?", (old, cid))
        with self.app.app_context():
            tutor.prune()
        self.assertEqual(self.rows("SELECT COUNT(*) AS n FROM tutor_conversations")[0]["n"], 0)
        self.assertEqual(self.rows("SELECT COUNT(*) AS n FROM tutor_messages")[0]["n"], 0)
        self.assertEqual(self.rows("SELECT COUNT(*) AS n FROM tutor_usage")[0]["n"], 1)  # credits still count this month
        self.ask("hi again", item_id=MATH_MC)
        r = self.post("/api/me/delete", {"confirm": "DELETE", "password": "password123"})
        self.assertEqual(r.status_code, 200, r.json)
        for table in ("tutor_conversations", "tutor_messages", "tutor_usage"):
            self.assertEqual(self.rows(f"SELECT COUNT(*) AS n FROM {table}")[0]["n"], 0, table)

    def test_report(self):
        self.ask("hi")
        with self.app.app_context():
            out = tutor.report()
        self.assertEqual(out["by_model"][tutor.HAIKU]["messages"], 1)
        self.assertGreater(out["by_model"][tutor.HAIKU]["cost_usd"], 0)


if __name__ == "__main__":
    unittest.main()
