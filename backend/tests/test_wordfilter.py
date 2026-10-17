"""The curse-word filter on every text box. Run from the backend folder: python -m unittest discover tests"""
import unittest

from app.services import wordfilter

from test_practice import ORIGIN, PracticeTest

BAD = ["fuck you", "F U C K", "f.u.c.k", "sh1t", "$hit", "bullshit", "shithead", "fuuuuck", "f*ck", "sh*t",
       "motherfucker", "asshole", "ass", "dumb ass", "Damn it", "p0rn", "shiiiiit", "a$$", "d!ck", "Pissed off", "b*tch"]
GOOD = ["Sam Lee", "class", "Dickens", "Scunthorpe", "Matsushita", "Cassandra", "Hancock", "assistant", "Essex",
        "passing grades", "I need help with math", "cocktail", "shiitake", "hello", "Hannah Glass", "analysis",
        "Massachusetts", "Sussex", "bass", "Peacock", "Dickson", "therapist", "Hitchcock", "Lisa Cummings", "Mississippi",
        "embassy", "assume", "magna cum laude", "Ashley", "scrap", "Zoë Nguyễn", ""]


class FilterRulesTest(unittest.TestCase):
    def test_catches_curse_words_and_tricks(self):
        self.assertEqual([b for b in BAD if wordfilter.is_clean(b)], [])

    def test_leaves_innocent_words_alone(self):
        self.assertEqual([g for g in GOOD if not wordfilter.is_clean(g)], [])

    def test_list_loads(self):
        modes = {m for m, _ in wordfilter.entries()}
        self.assertEqual(modes, {"any", "edge", "word"})


class FilterRoutesTest(PracticeTest):
    def patch(self, url, data):
        return self.client.patch(url, json=data, headers=ORIGIN)

    def test_every_text_box_is_checked(self):
        r = self.patch("/api/me", {"name": "Big Sh1t"})
        self.assertEqual((r.status_code, r.json["field"], r.json["code"]), (400, "name", "blocked_word"))
        self.assertEqual(self.patch("/api/me", {"name": "Sam Hancock"}).status_code, 200)
        self.assertEqual(self.patch("/api/me", {"parent_email": "fuckoff@mail.com"}).status_code, 400)

        r = self.post("/api/leads", {"name": "Ana", "email": "ana@school.org", "grade": 11, "agree": True, "message": "this is bullshit"})
        self.assertEqual((r.status_code, r.json["field"]), (400, "message"))
        r = self.post("/api/leads", {"name": "Ana", "email": "ana@school.org", "grade": 11, "agree": True, "message": "My son needs help with class work."})
        self.assertIn(r.status_code, (200, 201), r.json)

        self.post("/api/auth/logout")
        r = self.post("/api/auth/register", {"name": "a$$ hat", "email": "x@school.org", "password": "password123", "grade": 11})
        self.assertEqual((r.status_code, r.json["field"]), (400, "name"))
        r = self.post("/api/auth/register", {"name": "Kim", "email": "shithead@school.org", "password": "password123", "grade": 11})
        self.assertEqual((r.status_code, r.json["field"]), (400, "email"))
        # Signing in never runs the filter, so no existing account can be locked out by it.
        r = self.post("/api/auth/login", {"email": "shithead@school.org", "password": "password123"})
        self.assertNotEqual(r.json.get("code"), "blocked_word")
