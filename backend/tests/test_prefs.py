"""Customization: look, dashboard layout, study defaults, drawn avatar and reminders.
Run from the backend folder: python -m unittest discover tests"""
import json
import re
from datetime import date, datetime, timezone
from pathlib import Path

from app.db import execute, query
from app.services import mailer, prefs, reminders

from test_practice import ORIGIN, PracticeTest

THEME_JS = Path(__file__).resolve().parents[2] / "website" / "src" / "theme.js"


class PrefsTest(PracticeTest):
    def patch(self, url, data):
        return self.client.patch(url, json=data, headers=ORIGIN)

    def uid(self):
        with self.app.app_context():
            return query("SELECT id FROM users WHERE email = 'sam@school.org'", one=True)["id"]

    def coins(self, n):
        with self.app.app_context():
            execute("INSERT INTO xp_events (user_id, kind, xp, coins, detail, day, at) VALUES (?, 'gift', 0, ?, '', ?, '')",
                    (self.uid(), n, date.today().isoformat()))

    def test_defaults_come_with_the_account(self):
        u = self.client.get("/api/me").json["user"]
        self.assertEqual(u["appearance"]["text"], "m")
        self.assertEqual(u["prefs"]["study"]["set_size"], 10)
        self.assertEqual(u["prefs"]["dashboard"]["order"], list(prefs.SECTIONS))
        self.assertIsNone(u["avatar_drawn"])
        r = self.client.get("/api/me/prefs").json
        self.assertIn("avatar", r["options"])

    def test_free_look_options_and_shop_gated_ones(self):
        r = self.patch("/api/me/appearance", {"theme": "paper", "text": "xl", "font": "readable", "motion": "reduce", "density": "compact"})
        self.assertEqual(r.status_code, 200, r.json)
        a = r.json["user"]["appearance"]
        self.assertEqual((a["theme"], a["text"], a["font"], a["motion"], a["density"]), ("paper", "xl", "readable", "reduce", "compact"))
        self.assertEqual(self.patch("/api/me/appearance", {"text": "huge"}).status_code, 400)
        self.assertEqual(self.patch("/api/me/appearance", {"theme": "chalkboard"}).status_code, 403)
        self.assertEqual(self.patch("/api/me/appearance", {"accent": "custom"}).status_code, 403)
        self.assertEqual(self.patch("/api/me/appearance", {"custom_accent": "#123456"}).status_code, 403)
        self.coins(1000)
        self.post("/api/game/buy", {"item": "theme:chalkboard"})
        self.post("/api/game/buy", {"item": "accent:custom"})
        self.assertEqual(self.patch("/api/me/appearance", {"theme": "chalkboard"}).status_code, 200)
        self.assertEqual(self.patch("/api/me/appearance", {"custom_accent": "nope"}).status_code, 400)
        r = self.patch("/api/me/appearance", {"accent": "custom", "custom_accent": "#12AB56"})
        self.assertEqual(r.status_code, 200, r.json)
        self.assertEqual((r.json["user"]["appearance"]["accent"], r.json["user"]["appearance"]["custom_accent"]), ("custom", "#12ab56"))

    def test_dashboard_layout(self):
        order = list(reversed(prefs.SECTIONS))
        r = self.patch("/api/me/prefs", {"dashboard": {"order": order, "hidden": ["account"], "pins": ["speed", "levels"]}})
        self.assertEqual(r.status_code, 200, r.json)
        d = r.json["user"]["prefs"]["dashboard"]
        self.assertEqual((d["order"], d["hidden"], d["pins"]), (order, ["account"], ["speed", "levels"]))
        self.assertEqual(self.patch("/api/me/prefs", {"dashboard": {"order": order[:-1]}}).status_code, 400)
        self.assertEqual(self.patch("/api/me/prefs", {"dashboard": {"pins": list(prefs.PINS[:5])}}).status_code, 400)
        self.assertEqual(self.patch("/api/me/prefs", {"dashboard": {"hidden": ["nope"]}}).status_code, 400)

    def test_study_defaults(self):
        r = self.patch("/api/me/prefs", {"study": {"set_size": 15, "timer": "hide", "calculator": "open", "colors": "testday",
                                                  "sounds": False, "reminder": True, "reminder_hour": 19, "tz": "America/Chicago"}})
        self.assertEqual(r.status_code, 200, r.json)
        s = r.json["prefs"]["study"]
        self.assertEqual((s["set_size"], s["timer"], s["reminder_hour"], s["tz"]), (15, "hide", 19, "America/Chicago"))
        self.assertEqual(self.patch("/api/me/prefs", {"study": {"set_size": 12}}).status_code, 400)
        self.assertEqual(self.patch("/api/me/prefs", {"study": {"tz": "Mars/Olympus"}}).status_code, 400)
        self.assertEqual(self.patch("/api/me/prefs", {"study": {"reminder_hour": 24}}).status_code, 400)

    def test_drawn_avatar(self):
        parts = {"bg": "mint", "skin": "s6", "hair": "curly", "hair_color": "blue", "eyes": "happy", "mouth": "grin", "acc": "glasses", "shirt": "coral"}
        r = self.patch("/api/me/prefs", {"avatar": {"mode": "drawn", "parts": parts}})
        self.assertEqual(r.status_code, 200, r.json)
        self.assertEqual(r.json["user"]["avatar_drawn"], parts)
        self.assertEqual(self.patch("/api/me/prefs", {"avatar": {"parts": {"acc": "crown"}}}).status_code, 403)
        self.assertEqual(self.patch("/api/me/prefs", {"avatar": {"parts": {"hair": "mohawk9"}}}).status_code, 400)
        self.coins(300)
        self.post("/api/game/buy", {"item": "avatar:crown"})
        self.assertEqual(self.patch("/api/me/prefs", {"avatar": {"parts": {"acc": "crown"}}}).status_code, 200)
        # The drawn avatar (never a photo) shows on the leaderboard.
        nick = self.client.get("/api/speed/nicknames").json["nicknames"][0]
        self.patch("/api/speed/profile", {"nickname": nick, "opt_in": True})
        run = self.post("/api/speed/start").json["run"]
        self.post(f"/api/speed/runs/{run['id']}/finish")
        rows = self.client.get("/api/speed/board?scope=nation&period=today").json["rows"]
        self.assertEqual(rows[0]["avatar"]["acc"], "crown")
        self.patch("/api/me/prefs", {"avatar": {"mode": "photo"}})
        self.assertIsNone(self.client.get("/api/speed/board?scope=nation&period=today").json["rows"][0]["avatar"])

    def test_browser_knows_every_avatar_part(self):
        js = THEME_JS.read_text()
        for part, values in prefs.AVATAR.items():
            for v in values:
                if v != "none":
                    self.assertRegex(js, r"\b" + re.escape(v) + r"\s*:", f"theme.js can't draw {part} {v}")

    def test_reminders_go_out_once_at_the_chosen_hour(self):
        self.patch("/api/me/prefs", {"study": {"reminder": True, "reminder_hour": 19, "tz": "America/New_York"}})
        at7pm = datetime(2030, 3, 5, 0, 5, tzinfo=timezone.utc)  # 7:05 pm in New York (standard time, UTC-5)
        with self.app.app_context():
            mailer.OUTBOX.clear()
            self.assertEqual(reminders.send_due(datetime(2030, 3, 4, 23, 5, tzinfo=timezone.utc)), 0)  # 6 pm
            self.assertEqual(reminders.send_due(at7pm), 1)
            self.assertIn("Turn it off", mailer.OUTBOX[-1]["text"])
            self.assertEqual(reminders.send_due(at7pm), 0)  # once a day
            execute("UPDATE users SET reminder_sent_on = NULL")
            execute("INSERT INTO activity (user_id, kind, seconds, detail, at) VALUES (?, 'x', 60, '', ?)", (self.uid(), "2030-03-04T20:00:00Z"))
            self.assertEqual(reminders.send_due(at7pm), 0)  # already studied today
        self.patch("/api/me/prefs", {"study": {"reminder": False}})
        with self.app.app_context():
            execute("DELETE FROM activity")
            self.assertEqual(reminders.send_due(at7pm), 0)
