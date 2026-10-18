"""The collectibles market. Run from the backend folder: python -m unittest discover tests"""
from unittest import mock

from app.db import execute, query
from app.services import market

from test_play import PlayTest
from test_practice import ORIGIN


class MarketTest(PlayTest):
    def trade(self, item, side, price=None, client=None):
        data = {"item": item, "side": side}
        if price is not None:
            data["price"] = price
        return (client or self.client).post("/api/market/trade", json=data, headers=ORIGIN)

    def item(self, key, client=None):
        return next(i for i in (client or self.client).get("/api/market").json["items"] if i["key"] == key)

    def second_student(self):
        c = self.app.test_client()
        c.post("/api/auth/register", json={"name": "Ana Ruiz", "email": "ana@school.org", "password": "password123",
                                           "grade": 11, "test_date": "2030-12-07", "target_score": 1400}, headers=ORIGIN)
        with self.app.app_context():
            uid = query("SELECT id FROM users WHERE email = 'ana@school.org'", one=True)["id"]
            execute("INSERT INTO xp_events (user_id, kind, xp, coins, detail, day, at) VALUES (?, 'gift', 0, 5000, '', '2026-01-01', '')", (uid,))
        return c

    def test_overview_lists_every_collectible_at_base_price(self):
        o = self.client.get("/api/market").json
        self.assertEqual(len(o["items"]), len(market.ITEMS))
        for i in o["items"]:
            self.assertEqual(i["price"], i["base"])
            self.assertEqual(i["sell_price"], market.sell_price(i["base"]))
            self.assertEqual(i["owned"], 0)
        self.assertEqual(o["trades_left"], market.TRADES_PER_DAY)
        self.assertEqual([s["have"] for s in o["sets"]], [0] * len(market.SETS))
        self.assertEqual(o["mine"], [])

    def test_buying_raises_the_price_for_everyone_and_selling_lowers_it(self):
        self.give_coins(5000)
        other = self.second_student()
        pi = self.item("pi")
        r = self.trade("pi", "buy", pi["price"])
        self.assertEqual(r.status_code, 200, r.json)
        self.assertEqual(r.json["price"], 20)
        self.assertEqual(r.json["reward"]["coins"], -20)
        self.assertIn("market_debut", [b["key"] for b in r.json["reward"]["badges"]])
        after = self.item("pi", other)  # another student sees the higher price
        self.assertGreater(after["price"], pi["price"])
        self.assertEqual(self.item("pi")["owned"], 1)
        # The other student sells nothing (they don't have one) but can buy, pushing it higher still.
        self.assertEqual(self.trade("pi", "sell", client=other).status_code, 400)
        self.trade("pi", "buy", after["price"], client=other)
        higher = self.item("pi")
        self.assertGreater(higher["price"], after["price"])
        r = self.trade("pi", "sell", higher["sell_price"])
        self.assertEqual(r.status_code, 200, r.json)
        self.assertLess(self.item("pi")["price"], higher["price"])

    def test_buying_then_selling_right_away_never_makes_coins(self):
        self.give_coins(100000)
        for key in ("pi", "infinity", "midnight", "golden"):
            with self.app.app_context():
                start = __import__("app.services.game", fromlist=["totals"]).totals(self.uid())[1]
            for _ in range(2):
                self.assertEqual(self.trade(key, "buy").status_code, 200)
            for _ in range(2):
                self.assertEqual(self.trade(key, "sell").status_code, 200)
            with self.app.app_context():
                end = __import__("app.services.game", fromlist=["totals"]).totals(self.uid())[1]
            self.assertLess(end, start, key)

    def test_prices_drift_back_to_base(self):
        self.give_coins(5000)
        for _ in range(5):
            self.trade("pi", "buy")
        high = self.item("pi")["price"]
        self.assertGreater(high, 20)
        later = market.now_ms() + 5 * market.HALF_LIFE_MS
        with mock.patch.object(market, "now_ms", return_value=later):
            self.assertLessEqual(self.item("pi")["price"], 21)
            pts = self.client.get("/api/market/pi/history?hours=168").json["points"]
        self.assertEqual(len(pts), market.HISTORY_POINTS)
        self.assertGreater(max(p["price"] for p in pts), 22)  # the spike shows on the week chart...
        self.assertLessEqual(pts[-1]["price"], 21)            # ...and so does the drift back

    def test_stale_price_is_refused_with_the_new_one(self):
        self.give_coins(5000)
        self.trade("pi", "buy")
        r = self.trade("pi", "buy", 20)
        self.assertEqual(r.status_code, 409)
        self.assertEqual(r.json["price"], self.item("pi")["price"])

    def test_limits_hold_supply_and_coins(self):
        r = self.trade("golden", "buy")
        self.assertEqual(r.status_code, 400)
        self.assertIn("more coins", r.json["error"])
        self.give_coins(100000)
        for _ in range(market.RARITIES["legendary"]["max_hold"]):
            self.assertEqual(self.trade("golden", "buy").status_code, 200)
        r = self.trade("golden", "buy")
        self.assertIn("hold up to", r.json["error"])
        self.second_student()
        with self.app.app_context():
            # Another account owns the whole supply.
            oid = self.uid("ana@school.org")
            execute("INSERT INTO market_holdings (user_id, item, qty, cost) VALUES (?, 'phi', ?, 0)",
                    (oid, market.RARITIES["legendary"]["supply"]))
        r = self.trade("phi", "buy")
        self.assertEqual(r.status_code, 409)
        self.assertIn("Sold out", r.json["error"])
        self.assertEqual(self.item("phi")["left"], 0)

    def test_daily_trade_limit(self):
        self.give_coins(100000)
        with mock.patch.object(market, "TRADES_PER_DAY", 3):
            for _ in range(3):
                self.assertEqual(self.trade("pi", "buy").status_code, 200)
            r = self.trade("pi", "buy")
            self.assertEqual(r.status_code, 429)

    def test_collector_and_buy_low_badges(self):
        self.give_coins(100000)
        for i in market.ITEMS:
            if i["set"] == "symbols":
                r = self.trade(i["key"], "buy")
        self.assertIn("collector", [b["key"] for b in r.json["reward"]["badges"]])
        self.assertEqual(r.json["unlocked_title"], "Symbol Collector")
        prof = self.client.get("/api/game").json
        title = next(i for i in prof["shop"] if i["key"] == "title:set-symbols")
        self.assertTrue(title["owned"])
        self.assertEqual(self.post("/api/game/buy", {"item": "title:set-pencils"}).status_code, 400)  # earned, never sold
        self.assertEqual(self.post("/api/game/equip", {"kind": "title", "value": "Symbol Collector"}).status_code, 200)
        self.assertEqual(len(self.client.get("/api/market").json["mine"]), 6)
        self.assertEqual(next(s for s in self.client.get("/api/market").json["sets"] if s["key"] == "symbols")["have"], 6)
        other = self.second_student()
        for _ in range(8):
            self.trade("theta", "buy", client=other)  # others push the price up
        r = self.trade("theta", "sell")
        self.assertGreater(r.json["price"], market.BY_KEY["theta"]["base"])
        self.assertIn("buy_low", [b["key"] for b in r.json["reward"]["badges"]])

    def test_activity_feed_has_no_names(self):
        self.give_coins(500)
        self.trade("pi", "buy")
        feed = self.client.get("/api/market").json["activity"]
        self.assertEqual(feed[0]["item"], "pi")
        self.assertEqual(set(feed[0]), {"item", "name", "side", "price", "at_ms"})

    def test_bad_requests_and_parents(self):
        self.assertEqual(self.trade("nope", "buy").status_code, 400)
        self.assertEqual(self.trade("pi", "steal").status_code, 400)
        self.assertEqual(self.trade("pi", "buy", "20").status_code, 400)
        self.assertEqual(self.client.get("/api/market/pi/history?hours=5").status_code, 400)
        self.assertEqual(self.client.get("/api/market/nope/history").status_code, 404)
        anon = self.app.test_client()
        self.assertEqual(anon.get("/api/market").status_code, 401)

    def test_two_trades_at_once_cannot_reuse_a_price(self):
        self.give_coins(5000)
        with self.app.test_request_context():
            uid = self.uid()
            row = market._row("pi")
            execute("UPDATE market_items SET version = version + 1 WHERE item = 'pi'")  # someone else got in first
            with self.assertRaises(market.MarketError) as ctx:
                market._move(market.BY_KEY["pi"], row, 1, market.now_ms())
            self.assertEqual(ctx.exception.status, 409)
            seq = market._claim_user(uid)
            execute("UPDATE users SET market_seq = market_seq + 1 WHERE id = ?", (uid,))
            with self.assertRaises(market.MarketError):
                market._commit_user(uid, seq)

    def test_export_and_test_reset(self):
        self.give_coins(500)
        self.trade("pi", "buy")
        data = self.client.get("/api/me/export").json
        self.assertEqual(len(data["market_holdings"]), 1)
        self.assertEqual(len(data["market_trades"]), 1)
