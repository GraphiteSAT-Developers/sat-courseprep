"""Rewards, speed rounds, leaderboards, focus sessions and lessons. Run from the backend folder: python -m unittest discover tests"""
import json
from datetime import date, timedelta

from app.db import execute, query
from app.services import bank, game, levels, lessons, speed

from test_practice import ORIGIN, PracticeTest, right_answer, wrong_answer


class PlayTest(PracticeTest):
    def uid(self, email="sam@school.org"):
        with self.app.app_context():
            return query("SELECT id FROM users WHERE email = ?", (email,), one=True)["id"]

    def give_coins(self, n):
        with self.app.app_context():
            execute("INSERT INTO xp_events (user_id, kind, xp, coins, detail, day, at) VALUES (?, 'gift', 0, ?, '', ?, '')",
                    (self.uid(), n, date.today().isoformat()))

    def patch(self, url, data):
        return self.client.patch(url, json=data, headers=ORIGIN)

    def check(self, session, i, right):
        q = bank.all_items()[session["questions"][i]["id"]]
        r = self.post(f"/api/practice/sessions/{session['id']}/check", {"index": i, "answer": (right_answer if right else wrong_answer)(q)})
        self.assertEqual(r.status_code, 200, r.json)
        return r.json["question"]["game"]

    # ---------- Level up ----------
    def test_level_answers_pay_xp_with_combos_and_a_boss(self):
        s = self.post("/api/levels/start", {"track": "algebra", "level": 1}).json["session"]
        self.assertEqual(s["level"]["boss"], levels.SIZE - 1)
        items = bank.all_items()
        diffs = [levels.HARDNESS[items[q["id"]]["difficulty"]] for q in s["questions"]]
        self.assertEqual(diffs[-1], max(diffs))  # the hardest question is the boss, at the end

        g = self.check(s, 0, True)
        self.assertEqual((g["xp"], g["combo"], g["coins"]), (game.XP_RIGHT, 1, game.COINS_RIGHT))
        self.assertEqual(g["streak"]["days"], 1)
        g = self.check(s, 1, True)
        self.assertEqual((g["xp"], g["combo"]), (game.XP_RIGHT + game.COMBO_STEP, 2))
        g = self.check(s, 2, False)
        self.assertEqual((g["xp"], g["combo"], g["coins"]), (game.XP_MISS, 0, 0))
        for i in range(3, 8):
            g = self.check(s, i, True)
        self.assertEqual(g["combo"], 5)
        self.assertEqual(g["xp"], game.XP_RIGHT + game.COMBO_CAP - 2)  # 2 * 4 = 8, under the cap
        self.assertIn("on_a_roll", [b["key"] for b in g["badges"]])
        self.check(s, 8, True)
        g = self.check(s, 9, True)
        self.assertTrue(g["boss"])
        self.assertEqual(g["xp"], game.XP_RIGHT + game.COMBO_CAP + game.XP_BOSS)
        self.assertEqual(g["coins"], game.COINS_RIGHT + game.COINS_BOSS)
        self.assertIn("boss_slayer", [b["key"] for b in g["badges"]])

        # Checking the same question again pays nothing more.
        before = g["total_xp"]
        q = items[s["questions"][9]["id"]]
        self.post(f"/api/practice/sessions/{s['id']}/check", {"index": 9, "answer": right_answer(q)})
        self.assertEqual(self.client.get("/api/game/summary").json["xp"], before)

        res = self.post(f"/api/practice/sessions/{s['id']}/submit", {"answers": {}, "seconds_used": 300}).json["result"]
        rw = res["game"]
        self.assertTrue(res["level"]["passed"])
        self.assertEqual(rw["xp"], game.XP_LEVEL_DONE + game.XP_LEVEL_PASS + game.XP_FIRST_CLEAR)
        self.assertEqual(rw["coins"], game.COINS_FIRST_CLEAR * 1)
        self.assertEqual(rw["lines"][0]["label"], "Answers, combos and the boss")
        self.assertIn("first_steps", [b["key"] for b in rw["badges"]])

        # Passing the same level again: no first-clear bonus.
        s2 = self.post("/api/levels/start", {"track": "algebra", "level": 1}).json["session"]
        answers = {str(i): right_answer(items[q["id"]]) for i, q in enumerate(s2["questions"])}
        rw = self.post(f"/api/practice/sessions/{s2['id']}/submit", {"answers": answers, "seconds_used": 300}).json["result"]["game"]
        self.assertEqual(rw["xp"], game.XP_LEVEL_DONE + game.XP_LEVEL_PASS + game.XP_PERFECT)
        self.assertEqual(rw["coins"], 0)
        self.assertIn("flawless", [b["key"] for b in rw["badges"]])

    def test_ranks_and_streaks(self):
        self.assertEqual(game.rank_for(0)["name"], "Blank Page")
        r = game.rank_for(200)
        self.assertEqual((r["name"], r["next_name"]), ("Doodler", "Sketcher"))
        self.assertAlmostEqual(r["progress"], (200 - 150) / (400 - 150), places=3)
        self.assertIsNone(game.rank_for(10 ** 6)["next_at"])
        uid = self.uid()
        today = date.today()
        with self.app.app_context():
            for back in (1, 2, 4):
                execute("INSERT INTO xp_events (user_id, kind, xp, coins, detail, day, at) VALUES (?, 'x', 5, 0, '', ?, '')",
                        (uid, (today - timedelta(days=back)).isoformat()))
            self.assertEqual(game.streak(uid), {"days": 2, "today": False})  # alive until tonight
            s = game.award(uid, "x", 5)
            self.assertEqual(s["days"], 3)
            self.assertEqual(s["coins"], game.STREAK_COINS[3])
            self.assertEqual([b["key"] for b in s["badges"]], ["streak_3"])
            self.assertIsNone(game.award(uid, "x", 5))  # only the first XP of the day counts
            self.assertEqual(game.streak(uid), {"days": 3, "today": True})

    # ---------- shop ----------
    def test_shop_and_equipping(self):
        r = self.post("/api/game/buy", {"item": "frame:gold"})
        self.assertEqual(r.status_code, 400)
        self.assertIn("more coins", r.json["error"])
        r = self.post("/api/game/equip", {"kind": "frame", "value": "gold"})
        self.assertEqual(r.status_code, 400)
        r = self.patch("/api/me/appearance", {"accent": "rose"})
        self.assertEqual(r.status_code, 403)

        self.give_coins(500)
        r = self.post("/api/game/buy", {"item": "frame:gold"})
        self.assertEqual(r.status_code, 200, r.json)
        self.assertEqual(r.json["profile"]["coins"], 200)
        self.assertIn("fresh_look", [b["key"] for b in r.json["reward"]["badges"]])
        self.assertEqual(self.post("/api/game/buy", {"item": "frame:gold"}).status_code, 400)
        r = self.post("/api/game/equip", {"kind": "frame", "value": "gold"})
        self.assertEqual(r.json["profile"]["frame"], "gold")
        self.assertEqual(self.client.get("/api/me").json["user"]["frame"], "gold")
        self.post("/api/game/buy", {"item": "accent:rose"})
        self.assertEqual(self.patch("/api/me/appearance", {"accent": "rose"}).status_code, 200)
        self.assertEqual(self.post("/api/game/equip", {"kind": "frame", "value": None}).json["profile"]["frame"], None)
        self.assertEqual(self.post("/api/game/buy", {"item": "nope"}).status_code, 400)

    # ---------- speed rounds ----------
    def run_round(self, right):
        run = self.post("/api/speed/start").json["run"]
        items = bank.all_items()
        out = None
        for i, q in enumerate(run["questions"]):
            item = items[q["id"]]
            r = self.post(f"/api/speed/runs/{run['id']}/answer", {"index": i, "answer": right_answer(item) if i < right else wrong_answer(item)})
            self.assertEqual(r.status_code, 200, r.json)
            out = r.json
        return run, out

    def test_speed_round_is_the_same_for_everyone_and_scored_by_the_server(self):
        run, out = self.run_round(8)
        self.assertEqual(len(run["questions"]), speed.SIZE)
        items = bank.all_items()
        self.assertTrue(all(items[q["id"]]["type"] == "mc" and items[q["id"]]["difficulty"] != "hard" for q in run["questions"]))
        self.assertTrue(out["finished"])
        res = out["result"]
        self.assertEqual((res["correct"], res["misses"], res["ranked"]), (8, 2, True))
        self.assertEqual(res["score_ms"], res["raw_ms"] + 2 * speed.PENALTY_MS)
        self.assertEqual(out["reward"]["xp"], game.XP_SPEED_DONE + 8 * game.XP_SPEED_RIGHT)
        self.assertIn("off_the_line", [b["key"] for b in out["reward"]["badges"]])
        self.assertEqual(self.post(f"/api/speed/runs/{run['id']}/answer", {"index": 0, "answer": 0}).status_code, 409)

        run2, out2 = self.run_round(10)
        self.assertFalse(out2["result"]["ranked"])  # only the first round of the day is ranked
        self.assertEqual([q["id"] for q in run2["questions"]], [q["id"] for q in run["questions"]])

        self.post("/api/auth/logout")
        self.post("/api/auth/register", {"name": "Ana Cruz", "email": "ana@school.org", "password": "password123", "grade": 11})
        run3 = self.post("/api/speed/start").json["run"]
        self.assertEqual([q["id"] for q in run3["questions"]], [q["id"] for q in run["questions"]])

    def test_leaderboard_shows_only_opted_in_nicknames_by_state(self):
        r = self.client.get("/api/speed/board?scope=state&period=today")
        self.assertTrue(r.json["needs_state"])
        self.run_round(10)
        board = self.client.get("/api/speed/board?scope=nation&period=today").json
        self.assertEqual(board["rows"], [])
        self.assertEqual((board["you"]["rank"], board["you"]["visible"]), (1, False))

        self.assertEqual(self.patch("/api/speed/profile", {"opt_in": True}).status_code, 400)  # needs a nickname
        self.assertEqual(self.patch("/api/speed/profile", {"nickname": "Sam Lee"}).status_code, 400)
        self.assertEqual(self.patch("/api/speed/profile", {"state": "ZZ"}).status_code, 400)
        nick = self.client.get("/api/speed/nicknames").json["nicknames"][0]
        self.assertTrue(speed.valid_nickname(nick))
        r = self.patch("/api/speed/profile", {"nickname": nick, "opt_in": True, "state": "FL"})
        self.assertEqual(r.status_code, 200, r.json)
        board = self.client.get("/api/speed/board?scope=state&period=week").json
        self.assertEqual(board["state_name"], "Florida")
        self.assertEqual([(x["rank"], x["nickname"], x["you"]) for x in board["rows"]], [(1, nick, True)])
        self.assertNotIn("email", board["rows"][0])
        self.assertNotIn("name", board["rows"][0])

        # Someone in another state isn't on Florida's board, but is on the national one.
        self.post("/api/auth/logout")
        self.post("/api/auth/register", {"name": "Ana Cruz", "email": "ana@school.org", "password": "password123", "grade": 11})
        self.patch("/api/speed/profile", {"nickname": "Calm Vertex 42", "opt_in": True, "state": "TX"})
        self.run_round(10)
        uid = self.uid("ana@school.org")
        with self.app.app_context():  # make Ana slower
            execute("UPDATE speed_runs SET score_ms = score_ms + 60000 WHERE user_id = ?", (uid,))
        nation = self.client.get("/api/speed/board?scope=nation&period=today").json
        self.assertEqual([x["nickname"] for x in nation["rows"]], [nick, "Calm Vertex 42"])
        self.assertEqual(nation["you"]["rank"], 2)
        texas = self.client.get("/api/speed/board?scope=state&period=today").json
        self.assertEqual([x["nickname"] for x in texas["rows"]], ["Calm Vertex 42"])

    # ---------- focus ----------
    def test_focus_sessions_credit_real_time(self):
        self.assertEqual(self.post("/api/focus/start", {"minutes": 7, "label": "notes"}).status_code, 400)
        s = self.post("/api/focus/start", {"minutes": 25, "label": "notes"}).json["session"]
        r = self.post(f"/api/focus/{s['id']}/finish", {"completed": True}).json
        self.assertFalse(r["session"]["completed"])  # it hasn't really run 25 minutes
        self.assertIsNone(r["reward"])

        s = self.post("/api/focus/start", {"minutes": 25, "label": "notes"}).json["session"]
        with self.app.app_context():
            execute("UPDATE focus_sessions SET started_ms = started_ms - ? WHERE id = ?", (25 * 60 * 1000, s["id"]))
        r = self.post(f"/api/focus/{s['id']}/finish", {"completed": True}).json
        self.assertTrue(r["session"]["completed"])
        self.assertEqual(r["reward"]["xp"], 25 * game.XP_FOCUS_MINUTE)
        self.assertIn("deep_focus", [b["key"] for b in r["reward"]["badges"]])
        self.assertEqual(r["overview"]["week_focus_seconds"], 25 * 60)
        self.assertGreaterEqual(r["overview"]["week_seconds"], 25 * 60)

        # Practice time already counts from the sets, so a "practice" session doesn't add study time again.
        s = self.post("/api/focus/start", {"minutes": 15, "label": "practice"}).json["session"]
        with self.app.app_context():
            execute("UPDATE focus_sessions SET started_ms = started_ms - ? WHERE id = ?", (15 * 60 * 1000, s["id"]))
            before = query("SELECT COUNT(*) AS n FROM activity WHERE kind = 'focus'", one=True)["n"]
        r = self.post(f"/api/focus/{s['id']}/finish", {"completed": True}).json
        self.assertTrue(r["session"]["completed"])
        with self.app.app_context():
            self.assertEqual(query("SELECT COUNT(*) AS n FROM activity WHERE kind = 'focus'", one=True)["n"], before)

    # ---------- lessons ----------
    def test_lessons_and_spaced_recall(self):
        ov = self.client.get("/api/lessons").json
        self.assertEqual(len(ov["lessons"]), len(lessons.all_lessons()))
        first = ov["lessons"][0]
        l = self.client.get(f"/api/lessons/{first['id']}").json["lesson"]
        self.assertTrue(all(s["type"] in lessons.STEP_TYPES for s in l["steps"]))
        self.assertEqual(self.post(f"/api/lessons/{first['id']}/complete", {"kind": "recall", "score": 3}).status_code, 400)

        r = self.post(f"/api/lessons/{first['id']}/complete", {"kind": "lesson", "score": 5}).json
        self.assertEqual((r["xp"], r["coins"]), (game.XP_LESSON_FIRST, game.COINS_LESSON_FIRST))
        self.assertEqual(r["progress"]["due_on"], (date.today() + timedelta(days=1)).isoformat())
        self.assertIn("recall_rookie", [b["key"] for b in r["badges"]])
        r = self.post(f"/api/lessons/{first['id']}/complete", {"kind": "lesson", "score": 7}).json
        self.assertEqual(r["xp"], 0)  # a replay the same day
        self.assertEqual(r["progress"]["best"], 7)

        r = self.post(f"/api/lessons/{first['id']}/complete", {"kind": "recall", "score": 3}).json
        self.assertEqual((r["xp"], r["progress"]["stage"]), (0, 0))  # not due yet: practice only
        uid = self.uid()
        for stage in range(len(lessons.RECALL_DAYS)):
            with self.app.app_context():
                execute("UPDATE lesson_progress SET due_on = ? WHERE user_id = ?", (date.today().isoformat(), uid))
            self.assertIn(first["id"], self.client.get("/api/lessons").json["due"])
            r = self.post(f"/api/lessons/{first['id']}/complete", {"kind": "recall", "score": 2}).json
            self.assertTrue(r["passed"])
            self.assertEqual((r["xp"], r["progress"]["stage"]), (game.XP_RECALL_PASS, stage + 1))
        self.assertTrue(r["progress"]["mastered"])
        self.assertIsNone(r["progress"]["due_on"])

    def test_lesson_content_is_complete(self):
        for l in lessons.all_lessons():
            self.assertTrue(l["keys"] and l["recall"], l["id"])
            for s in l["steps"] + l["recall"]:
                if s["type"] == "predict":
                    self.assertLess(s["answer"], len(s["choices"]), l["id"])
                if s["type"] == "spot":
                    self.assertLess(s["wrong"], len(s["lines"]), l["id"])
                if s["type"] == "fill":
                    self.assertTrue(s["accept"] and any("___" in x for x in s["lines"]), l["id"])
                self.assertTrue(s.get("why") or s["type"] == "recall", (l["id"], s["prompt"]))

    def test_parents_cant_play_and_data_export_includes_it(self):
        self.post("/api/focus/start", {"minutes": 15, "label": "notes"})
        data = json.loads(self.client.get("/api/me/export").data)
        for table in ("xp_events", "badges", "inventory", "speed_runs", "focus_sessions", "lesson_progress"):
            self.assertIn(table, data)
        self.assertEqual(len(data["focus_sessions"]), 1)
        self.post("/api/auth/logout")
        self.post("/api/auth/register", {"name": "Pat Lee", "email": "pat@home.org", "password": "password123", "role": "parent"})
        if self.client.get("/api/me").json["user"]["role"] == "parent":
            self.assertEqual(self.client.get("/api/game").status_code, 403)
