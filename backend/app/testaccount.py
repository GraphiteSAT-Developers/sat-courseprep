"""The local test accounts: student "beta" / "beta", and its parent "beta2" / "beta2".

It exists only when the app isn't running in production (Config.TEST_ACCOUNT). On every start
its password is set back to "beta", so it always works. Its progress is kept between sign-ins
like any account; Settings > Your data > "Start the test account over" (reset below) clears it.
"""
from datetime import datetime, timezone

from werkzeug.security import check_password_hash, generate_password_hash

from .db import connect, is_postgres

USERNAME = "beta"
PASSWORD = "beta"
NAME = "Beta Tester"
# A parent account linked to the test student, to try the parent dashboard: "beta2" / "beta2".
PARENT_USERNAME = "beta2"
PARENT_PASSWORD = "beta2"
PARENT_NAME = "Beta2 Parent"
OLD_PARENT_USERNAMES = ("parent",)  # earlier name for the test parent; renamed to beta2 on start, keeping its link
# The passwords are published above, so a slow hash protects nothing here. A fast one keeps every app start
# (and so every backend test) from spending most of its time hashing "beta".
HASH_METHOD = "pbkdf2:sha256:1000"


def ensure(url):
    ph = "%s" if is_postgres(url) else "?"
    conn = connect(url)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def account(email, password, name, role):
        row = conn.execute(f"SELECT id, password_hash FROM users WHERE email = {ph}", (email,)).fetchone()
        if not row:
            conn.execute(f"INSERT INTO users (email, password_hash, name, role, created_at) VALUES ({ph}, {ph}, {ph}, {ph}, {ph})",
                         (email, generate_password_hash(password, HASH_METHOD), name, role, stamp))
            row = conn.execute(f"SELECT id, password_hash FROM users WHERE email = {ph}", (email,)).fetchone()
            conn.execute(f"UPDATE users SET theme = 'paper' WHERE id = {ph}", (row["id"],))  # the site's look, as for new accounts
        else:
            conn.execute(f"UPDATE users SET name = {ph}, role = {ph} WHERE id = {ph}", (name, role, row["id"]))
        if not check_password_hash(row["password_hash"], password):
            conn.execute(f"UPDATE users SET password_hash = {ph} WHERE id = {ph}", (generate_password_hash(password, HASH_METHOD), row["id"]))
        return row["id"]

    try:
        # Rename the old test parent instead of making a second one, so its link to beta carries over.
        if not conn.execute(f"SELECT 1 FROM users WHERE email = {ph}", (PARENT_USERNAME,)).fetchone():
            for old in OLD_PARENT_USERNAMES:
                conn.execute(f"UPDATE users SET email = {ph}, name = {ph} WHERE email = {ph} AND role = 'parent'",
                             (PARENT_USERNAME, PARENT_NAME, old))
        student = account(USERNAME, PASSWORD, NAME, "student")
        parent = account(PARENT_USERNAME, PARENT_PASSWORD, PARENT_NAME, "parent")
        if not conn.execute(f"SELECT 1 FROM family_links WHERE parent_id = {ph} AND student_id = {ph}", (parent, student)).fetchone():
            conn.execute(f"INSERT INTO family_links (parent_id, student_id, created_at) VALUES ({ph}, {ph}, {ph})", (parent, student, stamp))
        conn.commit()
    finally:
        conn.close()


# Everything a student's practice leaves behind. study_plans goes before diagnostics, which it points to.
STUDENT_TABLES = ["practice_sessions", "practice_seen", "practice_completions", "study_plans", "diagnostics",
                  "review_items", "test_attempts", "activity", "xp_events", "badges", "inventory", "speed_runs",
                  "focus_sessions", "lesson_progress", "market_holdings",
                  "user_events", "question_log", "pets", "mock_tests", "integrity_events", "tutor_usage", "tutor_messages",
                  "tutor_conversations"]
TEST_COINS = 100_000  # so everything in the shop can be tried right away
STUDENT_ID_TABLES = ["subscriptions", "billing_events"]  # keyed by student_id


def was_set_up(user_id):
    from .db import query
    return query("SELECT 1 FROM xp_events WHERE user_id = ? AND kind = 'gift' AND detail = 'Test account coins'", (user_id,), one=True) is not None


def reset(user_id):
    """Clears the test account back to a brand-new student. Runs inside a request."""
    from .db import execute
    for table in STUDENT_TABLES:
        execute(f"DELETE FROM {table} WHERE user_id = ?", (user_id,))  # table names come from the fixed list above
    for table in STUDENT_ID_TABLES:
        execute(f"DELETE FROM {table} WHERE student_id = ?", (user_id,))
    # Market trades stay (they're the price history everyone sees) but stop pointing at the account.
    execute("UPDATE market_trades SET user_id = NULL WHERE user_id = ?", (user_id,))
    execute("UPDATE users SET plan = 'free' WHERE id = ?", (user_id,))
    execute("UPDATE users SET frame = NULL, title = NULL, board_opt_in = 0, nickname = NULL, state = NULL, accent = 'pencil', "
            "theme = 'paper', prefs = '{}', reminder_sent_on = NULL "
            "WHERE id = ?", (user_id,))
    from .db import now_iso
    from datetime import date
    execute("INSERT INTO xp_events (user_id, kind, xp, coins, detail, day, at) VALUES (?, 'gift', 0, ?, ?, ?, ?)",
            (user_id, TEST_COINS, "Test account coins", date.today().isoformat(), now_iso()))
    execute("UPDATE users SET diagnostic_prompted_at = NULL, test_date = NULL, target_score = NULL, "
            "weekly_goal_hours = 3 WHERE id = ?", (user_id,))


def is_test_login(app, email):
    return bool(app.config.get("TEST_ACCOUNT")) and str(email or "").strip().lower() in (USERNAME, PARENT_USERNAME)
