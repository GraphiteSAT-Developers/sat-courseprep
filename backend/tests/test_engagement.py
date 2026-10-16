"""Retention, the weekly progress email, and the daily warm-up. Run from the backend folder: python -m unittest discover tests"""
import json
import shutil
import tempfile
import unittest
from datetime import date, timedelta
from urllib.parse import parse_qs, urlparse

from app import create_app
from app.db import execute, query
from app.services import bank, engagement, mailer, warmup
from tests.test_practice import right_answer, wrong_answer

ORIGIN = {"Origin": "http://localhost"}


class EngagementTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.app = create_app({"DATABASE_URL": f"sqlite:///{self.dir}/test.db", "TESTING": True, "FORCE_HTTPS": False,
                               "SESSION_COOKIE_SECURE": False, "BASE_URL": "http://localhost", "TEST_ACCOUNT": False})
        self.client = self.app.test_client()
        self.post("/api/auth/register", {"name": "Sam Lee", "email": "sam@school.org", "password": "password123"})
        with self.app.app_context():
            self.uid = query("SELECT id FROM users WHERE email = 'sam@school.org'", one=True)["id"]
        mailer.OUTBOX.clear()

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def post(self, url, data=None):
        return self.client.post(url, json=data or {}, headers=ORIGIN)

    def backdate_signup(self, days):
        with self.app.app_context():
            execute("UPDATE users SET created_at = ? WHERE id = ?", ((date.today() - timedelta(days=days)).isoformat() + "T12:00:00Z", self.uid))

    def study_on(self, day, seconds=600):
        with self.app.app_context():
            execute("INSERT INTO activity (user_id, kind, seconds, detail, at) VALUES (?, 'topic_practice', ?, '', ?)",
                    (self.uid, seconds, day.isoformat() + "T15:00:00Z"))

    # ---------- retention ----------
    def test_retention_counts_only_finished_windows(self):
        self.backdate_signup(30)
        signup = date.today() - timedelta(days=30)
        self.study_on(signup + timedelta(days=1))
        self.study_on(signup + timedelta(days=24))
        with self.app.app_context():
            rows, summary, weekly = engagement.retention()
        row = rows[0]
        self.assertEqual((row["day1"], row["week1"], row["week4"]), ("yes", "yes", "yes"))
        self.assertEqual(row["study_days"], 2)
        self.assertEqual([s["percent"] for s in summary], [100, 100, 100])
        self.assertEqual(len(weekly), 8)

        # A brand-new student isn't counted in windows that haven't ended yet.
        self.post("/api/auth/logout")
        self.post("/api/auth/register", {"name": "New Kid", "email": "new@school.org", "password": "password123"})
        with self.app.app_context():
            rows, summary, _ = engagement.retention()
        self.assertEqual(rows[1]["week4"], "")
        self.assertEqual(summary[2]["students"], 1)

    def test_lessons_count_as_study_days(self):
        self.post("/api/masterclass/progress", {"lesson": "basics", "step": 1})
        with self.app.app_context():
            self.assertIn(date.today().isoformat(), engagement.active_days(self.uid)[self.uid])

    # ---------- weekly email ----------
    def test_weekly_email_reports_the_week_and_respects_settings(self):
        self.backdate_signup(10)
        self.study_on(date.today() - timedelta(days=1))
        self.study_on(date.today() - timedelta(days=3))
        with self.app.app_context():
            result = engagement.send_weekly()
        self.assertEqual(result["sent"], 1)
        mail = mailer.OUTBOX[-1]
        self.assertEqual(mail["to"], "sam@school.org")
        self.assertIn("2 study days", mail["subject"])
        self.assertIn("Studied on 2 of 7 days, about 20 minutes", mail["text"])

        # Running it again the same week sends nothing.
        with self.app.app_context():
            self.assertEqual(engagement.send_weekly()["sent"], 0)

        # A parent copy goes out only once the student adds the address and turns it on.
        r = self.client.patch("/api/me", json={"parent_weekly": True}, headers=ORIGIN)
        self.assertEqual(r.status_code, 400)
        r = self.client.patch("/api/me", json={"parent_email": "parent@home.org", "parent_weekly": True}, headers=ORIGIN)
        self.assertEqual(r.status_code, 200, r.json)
        self.assertTrue(r.json["user"]["parent_weekly"])
        with self.app.app_context():
            execute("UPDATE users SET weekly_sent_at = NULL WHERE id = ?", (self.uid,))
            result = engagement.send_weekly()
        self.assertEqual(sorted(e["who"] for e in result["emails"]), ["parent", "student"])
        parent_mail = next(m for m in mailer.OUTBOX if m["to"] == "parent@home.org")
        self.assertIn("Sam's week on Graphite", parent_mail["subject"])
        self.assertIn("Sam added your email", parent_mail["text"])

        # The unsubscribe link in the parent's email turns off just the parent copy, with no sign-in.
        link = [line for line in parent_mail["text"].splitlines() if "/api/email/unsubscribe" in line][0].split(": ", 1)[1]
        token = parse_qs(urlparse(link).query)["t"][0]
        self.post("/api/auth/logout")
        r = self.client.get("/api/email/unsubscribe?t=" + token)
        self.assertEqual(r.status_code, 200)
        self.assertIn(b"unsubscribed", r.data)
        with self.app.app_context():
            user = query("SELECT weekly_email, parent_weekly FROM users WHERE id = ?", (self.uid,), one=True)
        self.assertEqual((user["weekly_email"], user["parent_weekly"]), (1, 0))
        self.assertEqual(self.client.get("/api/email/unsubscribe?t=forged").status_code, 400)

    def test_no_weekly_email_for_inactive_or_new_students(self):
        self.study_on(date.today())
        with self.app.app_context():
            self.assertEqual(engagement.send_weekly(dry_run=True)["skipped"], {"new account": 1})
            execute("DELETE FROM activity WHERE user_id = ?", (self.uid,))
        self.backdate_signup(60)
        self.study_on(date.today() - timedelta(days=40))
        with self.app.app_context():
            self.assertEqual(engagement.send_weekly(dry_run=True)["skipped"], {"inactive": 1})

    def test_a_quiet_week_gets_a_kind_nudge(self):
        self.backdate_signup(20)
        self.study_on(date.today() - timedelta(days=12))
        with self.app.app_context():
            engagement.send_weekly()
        mail = mailer.OUTBOX[-1]
        self.assertEqual(mail["subject"], "A 5-minute way back in")
        self.assertIn("No practice this week. That happens.", mail["text"])

    # ---------- daily warm-up ----------
    def test_warmup_mixes_review_weak_topic_and_desmos(self):
        # Miss two questions in a topic set so it lands in the review queue, due today.
        r = self.post("/api/practice/sessions", {"mode": "topic", "domain": "psda", "skill": "percentages", "count": 5})
        sid = r.json["session"]["id"]
        with self.app.app_context():
            ids = json.loads(query("SELECT item_ids FROM practice_sessions WHERE id = ?", (sid,), one=True)["item_ids"])
            first, missed = ids[0], bank.all_items()[ids[0]]
            second = bank.all_items()[ids[1]]
        self.post(f"/api/practice/sessions/{sid}/check", {"index": 0, "answer": wrong_answer(missed)})
        self.post(f"/api/practice/sessions/{sid}/check", {"index": 1, "answer": wrong_answer(second)})

        r = self.post("/api/warmup")
        self.assertEqual(r.status_code, 201, r.json)
        s = r.json["session"]
        self.assertEqual((s["mode"], len(s["questions"])), ("warmup", 3))
        self.assertEqual(s["questions"][0]["id"], first)
        with self.app.app_context():
            items = bank.all_items()
            self.assertTrue(any(items[q["id"]]["route"] == "desmos-primary" for q in s["questions"][1:]))
            self.assertEqual(warmup.weakest_skill(self.uid), ("psda", "percentages"))

        # Asking again before finishing picks up the same warm-up.
        self.assertEqual(self.post("/api/warmup").json["session"]["id"], s["id"])

        # A right answer on the review question counts toward clearing it.
        r = self.post(f"/api/practice/sessions/{s['id']}/check", {"index": 0, "answer": right_answer(missed)})
        self.assertEqual(r.json["question"]["review"]["right_count"], 1)
        with self.app.app_context():
            for i, q in enumerate(s["questions"][1:], 1):
                self.post(f"/api/practice/sessions/{s['id']}/check", {"index": i, "answer": right_answer(items[q["id"]])})
        w = self.client.get("/api/dashboard").json["warmup"]
        self.assertTrue(w["done_today"])
        self.assertEqual(w["days_this_week"], 1)
        # Another one after finishing is a fresh set.
        self.assertNotEqual(self.post("/api/warmup").json["session"]["id"], s["id"])


if __name__ == "__main__":
    unittest.main()
