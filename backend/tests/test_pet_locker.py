"""Pets and the locker (wearing every kind of item). Run: python -m unittest discover tests"""
from datetime import date

from app.db import execute, query
from app.services import cosmetics, pet

from test_play import PlayTest


class PetLockerTest(PlayTest):
    def xp(self, n):
        with self.app.app_context():
            execute("INSERT INTO xp_events (user_id, kind, xp, coins, detail, day, at) VALUES (?, 'gift', ?, 0, '', ?, '')",
                    (self.uid(), n, date.today().isoformat()))

    def test_egg_hatches_from_study_xp_and_grows(self):
        o = self.client.get("/api/pet").json
        egg = o["egg"]
        self.assertEqual((egg["progress"], egg["need"], egg["ready"]), (0, pet.EGG_XP, False))
        self.assertEqual(self.post(f"/api/pet/{egg['id']}/hatch").status_code, 400)
        self.xp(pet.EGG_XP)
        r = self.post(f"/api/pet/{egg['id']}/hatch")
        self.assertEqual(r.status_code, 200, r.json)
        p = r.json["pet"]
        self.assertIn(p["species"], [s[0] for s in pet.SPECIES])
        self.assertTrue(p["active"])
        self.assertEqual((p["level"], p["xp"]), (1, 0))
        self.assertIn("first_hatch", [b["key"] for b in r.json["reward"]["badges"]])
        self.xp(60)  # level 2 needs 60
        self.assertEqual(self.client.get("/api/pet").json["active"]["level"], 2)

    def test_treats_names_eggs_and_active_pet(self):
        egg = self.client.get("/api/pet").json["egg"]
        self.xp(pet.EGG_XP); self.give_coins(5000)
        self.assertEqual(self.post("/api/pet/treat").status_code, 400)  # nothing hatched yet
        self.post(f"/api/pet/{egg['id']}/hatch")
        r = self.post("/api/pet/treat").json
        self.assertEqual(r["pet"]["xp"], pet.TREAT_XP)
        self.assertEqual(r["reward"]["coins"], -pet.TREAT_PRICE)
        for _ in range(pet.TREATS_PER_DAY - 1):
            self.post("/api/pet/treat")
        self.assertEqual(self.post("/api/pet/treat").status_code, 400)
        self.assertEqual(self.post(f"/api/pet/{egg['id']}/name", {"name": "Pencil Jr"}).json["active"]["name"], "Pencil Jr")
        self.assertEqual(self.post(f"/api/pet/{egg['id']}/name", {"name": "<b>"}).status_code, 400)
        # a second egg, hatched, can become the active pet; the first keeps its XP
        self.assertEqual(self.post("/api/pet/egg").status_code, 200)
        self.assertEqual(self.post("/api/pet/egg").status_code, 400)  # one egg at a time
        egg2 = self.client.get("/api/pet").json["egg"]
        self.xp(pet.EGG_XP)
        self.post(f"/api/pet/{egg2['id']}/hatch")
        o = self.post(f"/api/pet/{egg2['id']}/active").json
        first = next(p for p in o["pets"] if p["id"] == egg["id"])
        self.assertFalse(first["active"])
        self.assertEqual(first["xp"], pet.EGG_XP + pet.TREAT_XP * pet.TREATS_PER_DAY)
        self.assertEqual(o["active"]["id"], egg2["id"])

    def test_levels_get_further_apart(self):
        self.assertEqual(pet.level_for(0)[0], 1)
        self.assertEqual(pet.level_for(59)[0], 1)
        self.assertEqual(pet.level_for(60)[0], 2)
        self.assertEqual(pet.level_for(60 + 80)[0], 3)
        self.assertEqual(pet.stage_for(12), "teen")
        self.assertEqual(pet.level_for(10 ** 7)[0], pet.MAX_LEVEL)

    def test_locker_wears_every_kind(self):
        self.give_coins(100000)
        def equip(kind, value, slot=None):
            d = {"kind": kind, "value": value}
            if slot: d["slot"] = slot
            return self.post("/api/game/equip", d)
        # free items work without buying, and wearing one switches to the drawn avatar
        r = equip("avatar", "beanie")
        self.assertEqual(r.status_code, 200, r.json)
        self.assertEqual(r.json["user"]["avatar_drawn"]["hat"], "beanie")
        # shop items need buying first
        self.assertEqual(equip("avatar", "wizard").status_code, 400)
        self.post("/api/game/buy", {"item": "avatar:wizard"})
        self.assertEqual(equip("avatar", "wizard").json["user"]["avatar_drawn"]["hat"], "wizard")
        self.assertTrue(next(i for i in equip("avatar", "wizard").json["profile"]["shop"] if i["key"] == "avatar:wizard")["worn"])
        self.assertEqual(equip("avatar", None, "hat").json["user"]["avatar_drawn"]["hat"], "none")
        for key, kind, value in (("frame:orbit", "frame", "orbit"), ("effect:fireflies", "effect", "fireflies"), ("theme:plum", "theme", "plum"),
                                 ("accent:ember", "accent", "ember")):
            self.assertEqual(equip(kind, value).status_code, 400, key)
            self.post("/api/game/buy", {"item": key})
            self.assertEqual(equip(kind, value).status_code, 200, key)
        u = self.client.get("/api/me").json["user"]
        self.assertEqual((u["appearance"]["theme"], u["appearance"]["accent"], u["appearance"]["effect"], u["frame"]), ("plum", "ember", "fireflies", "orbit"))
        self.assertEqual(equip("effect", "none").status_code, 200)
        self.assertEqual(equip("bogus", "x").status_code, 400)

    def test_old_single_accessory_moves_to_its_slot(self):
        with self.app.app_context():
            execute("UPDATE users SET prefs = ? WHERE id = ?", ('{"avatar": {"mode": "drawn", "parts": {"acc": "sunglasses"}}}', self.uid()))
        u = self.client.get("/api/me").json["user"]
        self.assertEqual(u["avatar_drawn"]["face"], "sunglasses")
        self.assertEqual(u["avatar_drawn"]["acc"], "none")

    def test_catalog_is_complete(self):
        for slot, items in cosmetics.AVATAR.items():
            self.assertTrue(any(p == 0 for _, _, p, _, _ in items), slot)
            for v, name, price, rarity, about in items:
                self.assertIn(rarity, cosmetics.RARITY)
