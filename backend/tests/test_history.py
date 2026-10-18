"""History: every change and every answered question is saved to the account. Run: python -m unittest discover tests"""
import json

from app import crypto
from app.db import query
from app.services import bank

from test_play import PlayTest
from test_practice import ORIGIN, right_answer, wrong_answer


class HistoryTest(PlayTest):
    def rows(self, table):
        with self.app.app_context():
            return query(f"SELECT * FROM {table} WHERE user_id = ? ORDER BY id", (self.uid(),))

    def test_sign_up_and_sign_in_are_saved(self):
        kinds = [r["kind"] for r in self.rows("user_events")]
        self.assertEqual(kinds[0], "auth.register")
        self.post("/api/auth/logout")
        self.post("/api/auth/login", {"email": "sam@school.org", "password": "password123"})
        kinds = [r["kind"] for r in self.rows("user_events")]
        self.assertEqual(kinds[-2:], ["auth.logout", "auth.login"])

    def test_passwords_never_saved_and_details_are_encrypted(self):
        with self.app.app_context():
            for r in self.rows("user_events"):
                self.assertTrue(r["detail"].startswith(crypto.PREFIX))
                self.assertNotIn("password123", crypto.unseal(r["detail"]))

    def test_profile_changes_record_before_and_after(self):
        r = self.patch("/api/me", {"name": "Sam Rivera"})
        self.assertEqual(r.status_code, 200, r.json)
        self.patch("/api/me/appearance", {"theme": "light"})
        ev = self.client.get("/api/me/history/events").json["items"]
        self.assertEqual(ev[0]["label"], "Changed the look")
        self.assertEqual(ev[0]["detail"]["changes"]["theme"], {"from": "dark", "to": "light"})
        self.assertEqual(ev[1]["detail"]["changes"]["name"], {"from": "Sam Lee", "to": "Sam Rivera"})

    def test_failed_changes_are_saved_with_the_error(self):
        self.patch("/api/me/appearance", {"theme": "nope"})
        ev = self.client.get("/api/me/history/events").json["items"][0]
        self.assertFalse(ev["ok"])
        self.assertTrue(ev["detail"]["error"])

    def test_every_answered_question_is_saved(self):
        s = self.start(mode="topic", domain=bank.topics()[0]["key"], count=5)
        items = bank.all_items()
        q0 = items[s["questions"][0]["id"]]
        self.post(f"/api/practice/sessions/{s['id']}/check", {"index": 0, "answer": right_answer(q0)})
        q1 = items[s["questions"][1]["id"]]
        self.post(f"/api/practice/sessions/{s['id']}/submit", {"answers": {"1": wrong_answer(q1)}, "seconds_used": 60})
        log = self.client.get("/api/me/history/questions").json["items"]
        self.assertEqual([(q["item_id"], q["correct"]) for q in log], [(q1["id"], False), (q0["id"], True)])
        self.assertEqual(log[0]["source_name"], "Topic practice")
        st = self.client.get("/api/me/history").json["stats"]
        self.assertEqual((st["answered"], st["right"], st["different_questions"]), (2, 1, 2))

    def test_speed_and_lessons_are_saved(self):
        run = self.post("/api/speed/start").json["run"]
        q = bank.all_items()[run["questions"][0]["id"]]
        self.post(f"/api/speed/runs/{run['id']}/answer", {"index": 0, "answer": right_answer(q)})
        self.post(f"/api/speed/runs/{run['id']}/answer", {"index": 0, "answer": wrong_answer(q)})  # repeats don't count twice
        sources = [r["source"] for r in self.rows("question_log")]
        self.assertEqual(sources, ["speed"])

    def test_page_views(self):
        self.assertEqual(self.post("/api/me/history/view", {"page": "/market.html"}).status_code, 204)
        self.assertEqual(self.post("/api/me/history/view", {"page": "https://evil.example"}).status_code, 400)
        ev = self.client.get("/api/me/history/events").json["items"]
        self.assertEqual(ev[1]["label"], "Opened a page")
        self.assertEqual(ev[1]["detail"]["sent"], {"page": "/market.html"})

    def test_paging_privacy_and_export(self):
        for _ in range(45):
            self.post("/api/me/history/view", {"page": "/dashboard.html"})
        first = self.client.get("/api/me/history/events").json
        self.assertTrue(first["more"])
        nxt = self.client.get(f"/api/me/history/events?before={first['items'][-1]['id']}").json
        self.assertLess(nxt["items"][0]["id"], first["items"][-1]["id"])
        self.assertEqual(self.client.get("/api/me/history/events?before=x").status_code, 400)
        self.assertEqual(self.app.test_client().get("/api/me/history").status_code, 401)
        data = self.client.get("/api/me/export").json
        self.assertGreater(len(data["user_events"]), 40)
        self.assertIsInstance(data["user_events"][0]["detail"], dict)  # decrypted for the owner

    def test_deleting_the_account_deletes_the_history(self):
        uid = self.uid()
        r = self.post("/api/me/delete", {"password": "password123", "confirm": "DELETE"})
        self.assertIn(r.status_code, (200, 204), r.json)
        with self.app.app_context():
            self.assertEqual(query("SELECT COUNT(*) AS n FROM user_events WHERE user_id = ?", (uid,), one=True)["n"], 0)
