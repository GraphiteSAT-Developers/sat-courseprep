"""The local test account: username "beta", password "beta".

It exists only when the app isn't running in production (Config.TEST_ACCOUNT). On every start
its password is set back to "beta", so it always works. Its practice history is kept between
starts; delete it with `DELETE FROM users WHERE email = 'beta'` to start fresh.
"""
from datetime import datetime, timezone

from werkzeug.security import check_password_hash, generate_password_hash

from .db import connect, is_postgres

USERNAME = "beta"
PASSWORD = "beta"
NAME = "Beta Tester"


def ensure(url):
    ph = "%s" if is_postgres(url) else "?"
    conn = connect(url)
    try:
        row = conn.execute(f"SELECT id, password_hash FROM users WHERE email = {ph}", (USERNAME,)).fetchone()
        if not row:
            stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            conn.execute(f"INSERT INTO users (email, password_hash, name, created_at) VALUES ({ph}, {ph}, {ph}, {ph})",
                         (USERNAME, generate_password_hash(PASSWORD), NAME, stamp))
        elif not check_password_hash(row["password_hash"], PASSWORD):
            conn.execute(f"UPDATE users SET password_hash = {ph} WHERE id = {ph}", (generate_password_hash(PASSWORD), row["id"]))
        conn.commit()
    finally:
        conn.close()


def is_test_login(app, email):
    return bool(app.config.get("TEST_ACCOUNT")) and str(email or "").strip().lower() == USERNAME
