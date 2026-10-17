"""Security checks across the whole app. Run from the backend folder: python -m unittest discover tests

Covers: sign-in required on every API route that should need it, nobody reaching another student's records,
fields that can't be set from the browser, bot protection, upload limits, encryption at rest, headers,
cookies, write limits, and that no secrets ship with the website."""
import base64
import io
import json
import re
import time
from pathlib import Path

from app import create_app, crypto
from app.db import query, set_clause
from app.services import bank

from test_practice import ORIGIN, PracticeTest, right_answer

REPO = Path(__file__).resolve().parents[2]
# API routes anyone may call without signing in, and why.
PUBLIC = {
    "/api/health",                     # the host's health check
    "/api/sample", "/api/sample/check",  # the home page's sample question
    "/api/auth/login", "/api/auth/logout", "/api/auth/register", "/api/auth/forgot", "/api/auth/reset",
    "/api/auth/form-token",            # bot protection token for the public forms
    "/api/leads",                      # the home page form
    "/api/checkout",                   # plan list on the checkout page (account details only when signed in)
    "/api/speed/states",               # the list of US states
    "/api/stripe/webhook",             # Stripe's servers, checked by signature instead
}


class SecurityTest(PracticeTest):
    def patch(self, url, data):
        return self.client.patch(url, json=data, headers=ORIGIN)

    def uid(self, email):
        with self.app.app_context():
            return query("SELECT id FROM users WHERE email = ?", (email,), one=True)["id"]

    # ---------- enforce server-side auth ----------
    def test_every_private_route_needs_sign_in(self):
        anon = self.app.test_client()
        checked = 0
        for rule in self.app.url_map.iter_rules():
            if not rule.rule.startswith("/api/") or rule.rule in PUBLIC:
                continue
            url = re.sub(r"<(?:int:)?[^>]+>", "1", rule.rule)
            for method in sorted(rule.methods - {"HEAD", "OPTIONS"}):
                r = anon.open(url, method=method, json={}, headers=ORIGIN)
                self.assertIn(r.status_code, (401, 403), f"{method} {rule.rule} answered {r.status_code} without sign-in")
                checked += 1
        self.assertGreater(checked, 60)

    # ---------- lock record access ----------
    def test_students_cant_reach_each_others_records(self):
        # Sam (signed in from setUp) makes one of everything.
        s = self.post("/api/practice/sessions", {"mode": "topic", "domain": "algebra", "count": 5}).json["session"]
        run = self.post("/api/speed/start").json["run"]
        focus = self.post("/api/focus/start", {"minutes": 15, "label": "notes"}).json["session"]
        q = bank.all_items()[s["questions"][0]["id"]]
        self.post(f"/api/practice/sessions/{s['id']}/check", {"index": 0, "answer": "9999" if q["type"] == "spr" else (q["answer"] + 1) % 4})
        review = self.client.get("/api/dashboard").json
        self.post("/api/auth/logout")
        self.post("/api/auth/register", {"name": "Eve Ray", "email": "eve@school.org", "password": "password123", "grade": 11})
        for method, url, data in [
            ("GET", f"/api/practice/sessions/{s['id']}", None),
            ("POST", f"/api/practice/sessions/{s['id']}/check", {"index": 0, "answer": 0}),
            ("POST", f"/api/practice/sessions/{s['id']}/submit", {"answers": {}}),
            ("GET", f"/api/speed/runs/{run['id']}", None),
            ("POST", f"/api/speed/runs/{run['id']}/answer", {"index": 0, "answer": 0}),
            ("POST", f"/api/focus/{focus['id']}/finish", {"completed": True}),
            ("GET", f"/api/parent/students/{self.uid('sam@school.org')}", None),
        ]:
            r = self.client.open(url, method=method, json=data, headers=ORIGIN)
            self.assertIn(r.status_code, (403, 404), f"Eve reached Sam's {url}: {r.status_code}")
        # Eve's own review queue is empty: she can't see or clear Sam's.
        with self.app.app_context():
            sams = query("SELECT id FROM review_items WHERE user_id = ?", (self.uid("sam@school.org"),))
        for row in sams:
            self.assertEqual(self.post(f"/api/review/{row['id']}/right").status_code, 404)

    # ---------- block field tampering ----------
    def test_browser_cant_set_protected_fields(self):
        self.patch("/api/me", {"name": "Sam Lee", "role": "parent", "plan": "masterstroke", "id": 99, "email": "x@y.org",
                               "password_hash": "x", "board_opt_in": 1, "frame": "gold"})
        me = self.client.get("/api/me").json["user"]
        self.assertEqual((me["role"], me["plan"], me["email"], me["frame"]), ("student", "free", "sam@school.org", None))
        r = self.post("/api/auth/register", {"name": "Al", "email": "al@school.org", "password": "password123", "role": "admin"})
        self.assertEqual(r.status_code, 400)
        # Practice time is capped, and logging it over and over is limited.
        for _ in range(30):
            self.post("/api/activity", {"kind": "practice_question", "seconds": 99999})
        self.assertEqual(self.post("/api/activity", {"kind": "practice_question", "seconds": 60}).status_code, 429)
        with self.app.app_context():
            self.assertEqual(query("SELECT MAX(seconds) AS m FROM activity", one=True)["m"], 300)

    def test_identifier_check(self):
        self.assertEqual(set_clause({"name": 1, "grade": 2}), "name = ?, grade = ?")
        with self.assertRaises(ValueError):
            set_clause({"name = 'x' --": 1})

    # ---------- secure session cookies ----------
    def test_session_cookie_flags(self):
        r = self.post("/api/auth/login", {"email": "sam@school.org", "password": "password123", "remember": True})
        cookie = r.headers.get("Set-Cookie", "")
        self.assertIn("HttpOnly", cookie)
        self.assertIn("SameSite=Lax", cookie)
        prod = create_app({"DATABASE_URL": f"sqlite:///{self.dir}/p.db", "TESTING": True, "FORCE_HTTPS": True,
                           "SESSION_COOKIE_SECURE": True, "SESSION_COOKIE_NAME": "__Host-graphite_session"})
        c = prod.test_client()
        c.post("/api/auth/register", json={"name": "Pat Kim", "email": "pat@school.org", "password": "password123", "grade": 10},
               headers={"Origin": "https://localhost"}, base_url="https://localhost")
        r = c.post("/api/auth/login", json={"email": "pat@school.org", "password": "password123"},
                   headers={"Origin": "https://localhost"}, base_url="https://localhost")
        cookie = r.headers.get("Set-Cookie", "")
        self.assertTrue(cookie.startswith("__Host-graphite_session="), cookie)
        self.assertIn("Secure", cookie)
        self.assertNotIn("Domain=", cookie)

    # ---------- hash passwords ----------
    def test_passwords_are_hashed(self):
        with self.app.app_context():
            h = query("SELECT password_hash FROM users WHERE email = 'sam@school.org'", one=True)["password_hash"]
        self.assertTrue(h.startswith(("scrypt:", "pbkdf2:")))
        self.assertNotIn("password123", h)

    # ---------- bot protection ----------
    def test_forms_need_a_fresh_token_and_a_human_pace(self):
        app = create_app({"DATABASE_URL": f"sqlite:///{self.dir}/b.db", "TESTING": True, "FORCE_HTTPS": False,
                          "SESSION_COOKIE_SECURE": False, "BOT_CHECK_IN_TESTS": True})
        c = app.test_client()
        form = {"name": "Ana Cruz", "email": "ana@school.org", "password": "password123", "grade": 11}
        r = c.post("/api/auth/register", json=form, headers=ORIGIN)
        self.assertEqual((r.status_code, r.json["code"]), (400, "bot_check"))
        token = c.get("/api/auth/form-token").json["token"]
        r = c.post("/api/auth/register", json=dict(form, form_token=token), headers=ORIGIN)
        self.assertEqual((r.status_code, r.json["code"]), (400, "bot_check"))  # too fast for a person
        app.config["FORM_MIN_SECONDS"] = 0
        self.assertEqual(c.post("/api/auth/register", json=dict(form, form_token=token + "x"), headers=ORIGIN).status_code, 400)
        r = c.post("/api/auth/register", json=dict(form, form_token=token), headers=ORIGIN)
        self.assertEqual(r.status_code, 201, r.json)
        lead = {"name": "Ana", "email": "ana@school.org", "grade": 11, "agree": True}
        self.assertEqual(c.post("/api/leads", json=lead, headers=ORIGIN).json["code"], "bot_check")
        # The hidden honeypot field still quietly drops bots.
        self.assertEqual(c.post("/api/leads", json=dict(lead, company="Spam Co"), headers=ORIGIN).json, {"ok": True})

    def test_rate_limits(self):
        for _ in range(5):
            self.post("/api/auth/login", {"email": "sam@school.org", "password": "wrong-password"})
        self.assertEqual(self.post("/api/auth/login", {"email": "sam@school.org", "password": "password123"}).status_code, 429)
        self.app.config["TEST_WRITE_LIMIT"] = 5
        codes = [self.patch("/api/me", {"grade": 11}).status_code for _ in range(7)]
        self.assertEqual(codes[-1], 429)
        self.app.config["TEST_WRITE_LIMIT"] = None

    # ---------- restrict file uploads ----------
    def test_uploads_are_checked(self):
        from PIL import Image
        too_big = "data:image/png;base64," + "A" * (10 * 1024 * 1024)
        self.assertEqual(self.post("/api/me/avatar", {"image": too_big}).status_code, 413)
        svg = "data:image/svg+xml;base64," + base64.b64encode(b"<svg onload='alert(1)'/>").decode()
        self.assertEqual(self.post("/api/me/avatar", {"image": svg}).status_code, 400)
        fake = "data:image/png;base64," + base64.b64encode(b"<?php echo 1; ?>" * 10).decode()
        self.assertEqual(self.post("/api/me/avatar", {"image": fake}).status_code, 400)
        buf = io.BytesIO(); Image.new("RGB", (300, 200), "red").save(buf, "PNG")
        ok = self.post("/api/me/avatar", {"image": "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()})
        self.assertEqual(ok.status_code, 201, ok.json)

    # ---------- encrypt sensitive data ----------
    def test_sensitive_data_is_encrypted_at_rest(self):
        from PIL import Image
        buf = io.BytesIO(); Image.new("RGB", (64, 64), "blue").save(buf, "PNG")
        self.post("/api/me/avatar", {"image": "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()})
        self.patch("/api/me", {"parent_email": "mom@home.org"})
        self.post("/api/leads", {"name": "Ana", "email": "ana@school.org", "grade": 11, "agree": True, "message": "My daughter needs help."})
        with self.app.app_context():
            row = query("SELECT data FROM avatars", one=True)
            user = query("SELECT parent_email FROM users WHERE email = 'sam@school.org'", one=True)
            lead = query("SELECT message FROM leads", one=True)
            for v in (row["data"], user["parent_email"], lead["message"]):
                self.assertTrue(v.startswith(crypto.PREFIX), v[:20])
            self.assertEqual(crypto.unseal(lead["message"]), "My daughter needs help.")
            tampered = lead["message"][:-4] + ("AAAA" if not lead["message"].endswith("AAAA") else "BBBB")
            with self.assertRaises(Exception):
                crypto.unseal(tampered)
            self.assertEqual(crypto.unseal("plain old value"), "plain old value")
        self.assertEqual(self.client.get("/api/me").json["user"]["parent_email"], "mom@home.org")
        img = self.client.get(self.client.get("/api/me").json["user"]["avatar_url"])
        self.assertEqual(img.status_code, 200)

    # ---------- trim API responses ----------
    def test_responses_never_include_secrets(self):
        bodies = [self.client.get(u).data.decode() for u in ("/api/me", "/api/dashboard", "/api/game", "/api/me/prefs", "/api/speed")]
        bodies.append(self.client.get("/api/me/export").data.decode())
        for b in bodies:
            for word in ("password_hash", "session_version", "token_hash", "code_hash", "stripe_customer_id", "scrypt:"):
                self.assertNotIn(word, b)
        s = self.post("/api/practice/sessions", {"mode": "test"}).json["session"]
        q = s["questions"][0]
        self.assertNotIn("answer", q)
        self.assertNotIn("explain_html", q)
        r = self.client.get("/api/does-not-exist")
        self.assertNotIn("Traceback", r.data.decode())

    # ---------- security headers, HTTPS ----------
    def test_security_headers(self):
        r = self.client.get("/")
        h = r.headers
        for name in ("Content-Security-Policy", "X-Content-Type-Options", "Referrer-Policy", "X-Frame-Options",
                     "Permissions-Policy", "Cross-Origin-Opener-Policy"):
            self.assertIn(name, h)
        self.assertIn("frame-ancestors 'self'", h["Content-Security-Policy"])
        self.assertIn("object-src 'none'", h["Content-Security-Policy"])
        self.assertEqual(self.client.get("/api/me").headers["Cache-Control"], "no-store")
        prod = create_app({"DATABASE_URL": f"sqlite:///{self.dir}/h.db", "TESTING": True, "FORCE_HTTPS": True})
        r = prod.test_client().get("/pricing", base_url="http://graphiteprep.com")
        self.assertEqual(r.status_code, 301)
        self.assertTrue(r.headers["Location"].startswith("https://"))
        r = prod.test_client().get("/", base_url="https://graphiteprep.com")
        self.assertIn("max-age=63072000", r.headers["Strict-Transport-Security"])
        self.assertIn("upgrade-insecure-requests", r.headers["Content-Security-Policy"])

    # ---------- validate input ----------
    def test_bad_input_is_refused_cleanly(self):
        for url, data in [("/api/auth/register", ["not", "an", "object"]), ("/api/me/prefs", {"study": {"set_size": "10; DROP TABLE users"}}),
                          ("/api/practice/sessions", {"mode": "topic", "domain": "../../etc"}), ("/api/speed/profile", {"state": "<b>"})]:
            r = self.client.open(url, method="PATCH" if "prefs" in url or "profile" in url else "POST", json=data, headers=ORIGIN)
            self.assertEqual(r.status_code, 400, url)
        r = self.client.post("/api/leads", data="name=x", headers=dict(ORIGIN, **{"Content-Type": "application/x-www-form-urlencoded"}))
        self.assertEqual(r.status_code, 415)
        r = self.client.post("/api/leads", json={}, headers={"Origin": "https://evil.example"})
        self.assertEqual(r.status_code, 403)

    # ---------- hide API keys / no DB key in the browser ----------
    def test_no_secrets_ship_with_the_website(self):
        pattern = re.compile(r"(sk_live_|sk_test_[0-9A-Za-z]{8}|whsec_[0-9A-Za-z]{8}|postgres(ql)?://|DATABASE_URL|SECRET_KEY|DATA_KEY|SMTP_PASSWORD|TURNSTILE_SECRET)")
        site = REPO / "website" / "site"
        for f in list(site.rglob("*.html")) + list(site.rglob("*.js")):
            self.assertIsNone(pattern.search(f.read_text(errors="ignore")), f"{f.name} contains something secret-looking")
        for f in (REPO / "backend" / ".env", REPO / ".env"):
            if f.exists():
                self.assertIn(".env", (REPO / ".gitignore").read_text())
