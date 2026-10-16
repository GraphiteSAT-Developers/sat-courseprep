"""The local test account: username "beta", password "beta".

It exists only when the app isn't running in production (Config.TEST_ACCOUNT). On every start
its password is set back to "beta", so it always works. Every sign-in wipes its practice
history, so it starts fresh with the diagnostic each time, like a brand-new student.
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


# Everything a student's practice leaves behind. study_plans goes before diagnostics, which it points to.
STUDENT_TABLES = ["practice_sessions", "practice_seen", "practice_completions", "study_plans", "diagnostics",
                  "review_items", "test_attempts", "activity", "masterclass_progress"]


def reset(user_id):
    """Clears the test account back to a brand-new student. Runs inside a request."""
    from .db import execute
    for table in STUDENT_TABLES:
        execute(f"DELETE FROM {table} WHERE user_id = ?", (user_id,))  # table names come from the fixed list above
    execute("UPDATE users SET diagnostic_prompted_at = NULL, test_date = NULL, target_score = NULL, "
            "weekly_goal_hours = 3 WHERE id = ?", (user_id,))


def is_test_login(app, email):
    return bool(app.config.get("TEST_ACCOUNT")) and str(email or "").strip().lower() == USERNAME
