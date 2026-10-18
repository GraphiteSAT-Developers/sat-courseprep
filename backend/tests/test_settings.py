"""The settings page API: appearance, profile picture, email, password, devices, data download and deletion."""
import base64
import io
import json
import shutil
import tempfile
import unittest

from PIL import Image

from app import create_app
from app.db import connect

ORIGIN = {"Origin": "http://localhost"}


def image_data_url(fmt="PNG", size=(640, 400), color=(242, 193, 78)):
    buf = io.BytesIO()
    Image.new("RGB", size, color).save(buf, fmt)
    mime = {"PNG": "png", "JPEG": "jpeg", "WEBP": "webp", "GIF": "gif"}[fmt]
    return f"data:image/{mime};base64," + base64.b64encode(buf.getvalue()).decode()


class SettingsTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dir, True)
        self.db = f"sqlite:///{self.dir}/test.db"
        self.app = create_app({"DATABASE_URL": self.db, "TESTING": True, "PLAN_LIMITS": False, "FORCE_HTTPS": False,
                               "SESSION_COOKIE_SECURE": False, "BASE_URL": "http://localhost"})
        self.c = self.app.test_client()
        r = self.post("/api/auth/register", {"name": "Sam Lee", "email": "sam@school.org", "password": "password123",
                                             "grade": 11})
        self.assertEqual(r.status_code, 201, r.json)

    def post(self, url, data=None, client=None):
        return (client or self.c).post(url, json=data if data is not None else {}, headers=ORIGIN)

    def patch(self, url, data):
        return self.c.patch(url, json=data, headers=ORIGIN)

    # appearance
    def test_appearance_defaults_and_saves(self):
        basics = lambda a: {k: a[k] for k in ("theme", "accent", "ripple")}
        me = self.c.get("/api/me").json["user"]
        self.assertEqual(basics(me["appearance"]), {"theme": "dark", "accent": "pencil", "ripple": False})
        self.assertEqual((me["appearance"]["text"], me["appearance"]["font"]), ("m", "default"))  # reading options, see test_prefs
        r = self.patch("/api/me/appearance", {"theme": "light", "accent": "mint", "ripple": False})
        self.assertEqual(r.status_code, 200, r.json)
        self.assertEqual(basics(self.c.get("/api/me").json["user"]["appearance"]), {"theme": "light", "accent": "mint", "ripple": False})
        self.assertEqual(self.patch("/api/me/appearance", {"theme": "neon"}).json["field"], "theme")
        self.assertEqual(self.patch("/api/me/appearance", {"accent": "#ff00ff"}).json["field"], "accent")

    # profile picture
    def test_avatar_upload_is_square_and_served(self):
        r = self.post("/api/me/avatar", {"image": image_data_url("PNG", (640, 400))})
        self.assertEqual(r.status_code, 201, r.json)
        url = r.json["user"]["avatar_url"]
        self.assertTrue(url.startswith("/api/me/avatar?v="))
        img = self.c.get(url)
        self.assertEqual(img.status_code, 200)
        self.assertIn(img.mimetype, ("image/webp", "image/jpeg"))
        self.assertEqual(Image.open(io.BytesIO(img.data)).size, (256, 256))
        again = self.post("/api/me/avatar", {"image": image_data_url("JPEG", (300, 900))}).json["user"]["avatar_url"]
        self.assertNotEqual(again, url, "a new photo gets a new address so browsers don't show the old one")
        removed = self.c.delete("/api/me/avatar", json={}, headers=ORIGIN)
        self.assertIsNone(removed.json["user"]["avatar_url"])
        self.assertEqual(self.c.get("/api/me/avatar").status_code, 404)

    def test_avatar_rejects_non_images(self):
        fake = "data:image/png;base64," + base64.b64encode(b"<script>alert(1)</script>").decode()
        self.assertEqual(self.post("/api/me/avatar", {"image": fake}).status_code, 400)
        svg = "data:image/svg+xml;base64," + base64.b64encode(b"<svg/>").decode()
        self.assertEqual(self.post("/api/me/avatar", {"image": svg}).status_code, 400)
        self.assertEqual(self.post("/api/me/avatar", {"image": "not a data url"}).status_code, 400)

    def test_avatar_is_private(self):
        self.post("/api/me/avatar", {"image": image_data_url()})
        other = self.app.test_client()
        self.assertEqual(other.get("/api/me/avatar").status_code, 401)

    # email and password
    def test_change_email_needs_password_and_unique(self):
        self.assertEqual(self.post("/api/me/email", {"email": "new@school.org", "password": "wrong-pass"}).json["field"], "password")
        other = self.app.test_client()
        self.post("/api/auth/register", {"name": "Jo", "email": "jo@school.org", "password": "password123"}, client=other)
        self.assertEqual(self.post("/api/me/email", {"email": "jo@school.org", "password": "password123"}).status_code, 409)
        r = self.post("/api/me/email", {"email": "New@School.org", "password": "password123"})
        self.assertEqual(r.json["user"]["email"], "new@school.org")
        self.post("/api/auth/logout")
        self.assertEqual(self.post("/api/auth/login", {"email": "new@school.org", "password": "password123"}).status_code, 200)

    def test_change_password_signs_out_other_devices_only(self):
        laptop = self.app.test_client()
        self.post("/api/auth/login", {"email": "sam@school.org", "password": "password123"}, client=laptop)
        self.assertEqual(laptop.get("/api/me").status_code, 200)
        bad = self.post("/api/me/password", {"current_password": "nope-nope", "new_password": "brand-new-pass"})
        self.assertEqual(bad.json["field"], "current_password")
        self.assertEqual(self.post("/api/me/password", {"current_password": "password123", "new_password": "short"}).json["field"], "new_password")
        r = self.post("/api/me/password", {"current_password": "password123", "new_password": "brand-new-pass"})
        self.assertEqual(r.status_code, 200, r.json)
        self.assertEqual(self.c.get("/api/me").status_code, 200, "still signed in here")
        self.assertEqual(laptop.get("/api/me").status_code, 401, "signed out elsewhere")
        self.post("/api/auth/logout")
        self.assertEqual(self.post("/api/auth/login", {"email": "sam@school.org", "password": "brand-new-pass"}).status_code, 200)

    def test_wrong_password_limit(self):
        for _ in range(5):
            self.post("/api/me/email", {"email": "x@school.org", "password": "wrong-pass"})
        self.assertEqual(self.post("/api/me/email", {"email": "x@school.org", "password": "password123"}).status_code, 429)

    def test_sign_out_other_devices(self):
        phone = self.app.test_client()
        self.post("/api/auth/login", {"email": "sam@school.org", "password": "password123"}, client=phone)
        self.assertEqual(self.post("/api/me/sign-out-others").status_code, 200)
        self.assertEqual(phone.get("/api/me").status_code, 401)
        self.assertEqual(self.c.get("/api/me").status_code, 200)

    # data
    def test_export_has_data_but_no_secrets(self):
        self.post("/api/tests/pt4-math-m1/attempts", {"answers": {"0": 1}, "seconds_used": 600})
        r = self.c.get("/api/me/export")
        self.assertEqual(r.status_code, 200)
        self.assertIn("attachment", r.headers["Content-Disposition"])
        data = json.loads(r.data)
        self.assertEqual(data["account"]["email"], "sam@school.org")
        self.assertEqual(len(data["test_attempts"]), 1)
        self.assertNotIn("password_hash", r.data.decode())

    def test_delete_account_removes_everything(self):
        self.post("/api/tests/pt4-math-m1/attempts", {"answers": {"0": 1}, "seconds_used": 600})
        self.post("/api/me/avatar", {"image": image_data_url()})
        self.assertEqual(self.post("/api/me/delete", {"confirm": "nope", "password": "password123"}).json["field"], "confirm")
        self.assertEqual(self.post("/api/me/delete", {"confirm": "DELETE", "password": "wrong-pass"}).json["field"], "password")
        r = self.post("/api/me/delete", {"confirm": "DELETE", "password": "password123"})
        self.assertEqual(r.status_code, 200, r.json)
        self.assertEqual(self.c.get("/api/me").status_code, 401)
        conn = connect(self.db)
        for table in ("users", "test_attempts", "review_items", "avatars", "activity"):
            n = conn.execute(f"SELECT COUNT(*) AS n FROM {table} WHERE {'id' if table == 'users' else 'user_id'} IN "
                             "(SELECT id FROM users WHERE email = 'sam@school.org') OR "
                             f"{'id' if table == 'users' else 'user_id'} NOT IN (SELECT id FROM users)").fetchone()["n"]
            self.assertEqual(n, 0, table)
        conn.close()

    def test_delete_after_diagnostic_and_plan(self):
        d = self.post("/api/plan/diagnostic", {"test_date": "2030-12-07"}).json["diagnostic"]
        self.post(f"/api/plan/diagnostic/{d['id']}/submit", {"answers": {}, "sure": {}})
        r = self.post("/api/me/delete", {"confirm": "delete", "password": "password123"})
        self.assertEqual(r.status_code, 200, r.json)

    # test accounts and parents
    def test_test_accounts_cannot_change_sign_in_or_delete(self):
        beta = self.app.test_client()
        self.post("/api/auth/login", {"email": "beta", "password": "beta"}, client=beta)
        self.assertEqual(self.post("/api/me/password", {"current_password": "beta", "new_password": "something-else"}, client=beta).status_code, 403)
        self.assertEqual(self.post("/api/me/email", {"email": "b@school.org", "password": "beta"}, client=beta).status_code, 403)
        self.assertEqual(self.post("/api/me/delete", {"confirm": "DELETE", "password": "beta"}, client=beta).status_code, 403)
        ok = beta.patch("/api/me/appearance", json={"accent": "coral"}, headers=ORIGIN)
        self.assertEqual(ok.status_code, 200, "test accounts can still change appearance")

    def test_parent_can_use_settings(self):
        parent = self.app.test_client()
        self.post("/api/auth/login", {"email": "beta2", "password": "beta2", "role": "parent"}, client=parent)
        r = parent.patch("/api/me/appearance", json={"theme": "light"}, headers=ORIGIN)
        self.assertEqual(r.status_code, 200, r.json)
        self.assertEqual(self.post("/api/me/avatar", {"image": image_data_url()}, client=parent).status_code, 201)

    def test_settings_page_needs_sign_in(self):
        anon = self.app.test_client()
        r = anon.get("/settings.html")
        self.assertEqual(r.status_code, 302)
        self.assertIn("/signin.html?next=/settings.html", r.headers["Location"])


if __name__ == "__main__":
    unittest.main()
