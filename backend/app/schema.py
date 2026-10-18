"""Database tables, as numbered migrations.

To change the database: add a new entry to the end of MIGRATIONS. Never edit
one that has already run on a live site. Each migration runs once, in order,
when the app starts. {pk} becomes the right auto-increment id for the database.
"""
from datetime import datetime, timezone

from .db import connect, is_postgres

MIGRATIONS = [
    (1, "Accounts, leads, practice tests, review queue, resets, rate limits, activity", [
        """CREATE TABLE users (
            id {pk},
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            name TEXT NOT NULL,
            grade INTEGER,
            test_date TEXT,
            target_score INTEGER,
            plan TEXT NOT NULL DEFAULT 'free',
            weekly_goal_hours INTEGER NOT NULL DEFAULT 3,
            parent_email TEXT,
            session_version INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL,
            last_login_at TEXT
        )""",
        """CREATE TABLE leads (
            id {pk},
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            grade INTEGER,
            test_date TEXT,
            target_score INTEGER,
            message TEXT,
            created_at TEXT NOT NULL
        )""",
        """CREATE TABLE test_attempts (
            id {pk},
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            test_id TEXT NOT NULL,
            seconds_used INTEGER NOT NULL,
            correct INTEGER NOT NULL,
            total INTEGER NOT NULL,
            answers TEXT NOT NULL,
            results TEXT NOT NULL,
            submitted_at TEXT NOT NULL
        )""",
        "CREATE INDEX idx_attempts_user ON test_attempts (user_id, submitted_at)",
        """CREATE TABLE review_items (
            id {pk},
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            test_id TEXT NOT NULL,
            question_index INTEGER NOT NULL,
            domain TEXT NOT NULL,
            skill TEXT NOT NULL,
            right_count INTEGER NOT NULL DEFAULT 0,
            due_on TEXT NOT NULL,
            created_at TEXT NOT NULL,
            cleared_at TEXT,
            UNIQUE (user_id, test_id, question_index)
        )""",
        """CREATE TABLE password_resets (
            id {pk},
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            token_hash TEXT NOT NULL UNIQUE,
            expires_at TEXT NOT NULL,
            used_at TEXT
        )""",
        """CREATE TABLE rate_events (
            id {pk},
            bucket TEXT NOT NULL,
            at TEXT NOT NULL
        )""",
        "CREATE INDEX idx_rate_bucket ON rate_events (bucket, at)",
        """CREATE TABLE activity (
            id {pk},
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            kind TEXT NOT NULL,
            seconds INTEGER NOT NULL DEFAULT 0,
            detail TEXT,
            at TEXT NOT NULL
        )""",
        "CREATE INDEX idx_activity_user ON activity (user_id, at)",
    ]),
    (2, "Practice sets from the question bank, and the questions each student has done", [
        """CREATE TABLE practice_sessions (
            id {pk},
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            mode TEXT NOT NULL,
            domain TEXT,
            skill TEXT,
            title TEXT NOT NULL,
            item_ids TEXT NOT NULL,
            minutes INTEGER NOT NULL DEFAULT 0,
            checked TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            submitted_at TEXT,
            seconds_used INTEGER,
            correct INTEGER,
            results TEXT
        )""",
        "CREATE INDEX idx_practice_user ON practice_sessions (user_id, created_at)",
        """CREATE TABLE practice_seen (
            id {pk},
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            item_id TEXT NOT NULL,
            seen_at TEXT NOT NULL,
            UNIQUE (user_id, item_id)
        )""",
    ]),
    (3, "Topics each student has finished in the current round", [
        """CREATE TABLE practice_completions (
            id {pk},
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            topic TEXT NOT NULL,
            completed_at TEXT NOT NULL,
            UNIQUE (user_id, topic)
        )""",
    ]),
    (4, "Diagnostic, study plans, and practice sets that belong to a plan", [
        """CREATE TABLE diagnostics (
            id {pk},
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            item_ids TEXT NOT NULL,
            created_at TEXT NOT NULL,
            submitted_at TEXT,
            answers TEXT,
            results TEXT
        )""",
        "CREATE INDEX idx_diagnostics_user ON diagnostics (user_id, created_at)",
        """CREATE TABLE study_plans (
            id {pk},
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            diagnostic_id INTEGER NOT NULL REFERENCES diagnostics(id) ON DELETE CASCADE,
            plan TEXT NOT NULL,
            created_at TEXT NOT NULL
        )""",
        "CREATE INDEX idx_plans_user ON study_plans (user_id, created_at)",
        "ALTER TABLE practice_sessions ADD COLUMN plan_id INTEGER",
        "ALTER TABLE practice_sessions ADD COLUMN plan_task TEXT",
    ]),
    (5, "When a student was first sent to the diagnostic", [
        "ALTER TABLE users ADD COLUMN diagnostic_prompted_at TEXT",
    ]),
    (6, "Parent accounts: roles, parent-student links, link codes, subscriptions and billing history", [
        "ALTER TABLE users ADD COLUMN role TEXT NOT NULL DEFAULT 'student'",
        """CREATE TABLE family_links (
            id {pk},
            parent_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            student_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            weekly_report INTEGER NOT NULL DEFAULT 1,
            alert_days INTEGER NOT NULL DEFAULT 3,
            created_at TEXT NOT NULL,
            UNIQUE (parent_id, student_id)
        )""",
        "CREATE INDEX idx_family_student ON family_links (student_id)",
        """CREATE TABLE link_codes (
            id {pk},
            student_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            code_hash TEXT NOT NULL UNIQUE,
            expires_at TEXT NOT NULL,
            used_at TEXT
        )""",
        """CREATE TABLE subscriptions (
            student_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
            plan TEXT NOT NULL DEFAULT 'free',
            billing_interval TEXT,
            status TEXT NOT NULL DEFAULT 'active',
            renews_on TEXT,
            paused_until TEXT,
            updated_by INTEGER,
            updated_at TEXT NOT NULL
        )""",
        """CREATE TABLE billing_events (
            id {pk},
            student_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            parent_id INTEGER,
            kind TEXT NOT NULL,
            detail TEXT NOT NULL,
            amount_cents INTEGER NOT NULL DEFAULT 0,
            at TEXT NOT NULL
        )""",
        "CREATE INDEX idx_billing_student ON billing_events (student_id, at)",
    ]),
    (7, "Settings page: theme, accent color, ripple background and profile pictures", [
        "ALTER TABLE users ADD COLUMN theme TEXT NOT NULL DEFAULT 'dark'",
        "ALTER TABLE users ADD COLUMN accent TEXT NOT NULL DEFAULT 'pencil'",
        "ALTER TABLE users ADD COLUMN ripple INTEGER NOT NULL DEFAULT 1",
        "ALTER TABLE users ADD COLUMN avatar_version INTEGER NOT NULL DEFAULT 0",
        """CREATE TABLE avatars (
            user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
            mime TEXT NOT NULL,
            data TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )""",
    ]),
    (8, "New plans: Daily becomes Sharpened and Coached becomes Masterstroke", [
        "UPDATE subscriptions SET plan = 'sharpened' WHERE plan = 'daily'",
        "UPDATE subscriptions SET plan = 'masterstroke' WHERE plan = 'coached'",
        "UPDATE users SET plan = 'sharpened' WHERE plan = 'daily'",
        "UPDATE users SET plan = 'masterstroke' WHERE plan = 'coached'",
    ]),
    (9, "Stripe: customer and subscription ids, and webhook events already handled", [
        "ALTER TABLE users ADD COLUMN stripe_customer_id TEXT",
        "ALTER TABLE subscriptions ADD COLUMN stripe_subscription_id TEXT",
        """CREATE TABLE stripe_events (
            id TEXT PRIMARY KEY,
            kind TEXT NOT NULL,
            received_at TEXT NOT NULL
        )""",
    ]),
    (10, "Rewards (XP, coins, badges, items), speed rounds and leaderboards, focus sessions, lessons", [
        """CREATE TABLE xp_events (
            id {pk},
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            kind TEXT NOT NULL,
            xp INTEGER NOT NULL DEFAULT 0,
            coins INTEGER NOT NULL DEFAULT 0,
            detail TEXT,
            day TEXT NOT NULL,
            at TEXT NOT NULL
        )""",
        "CREATE INDEX idx_xp_user ON xp_events (user_id, day)",
        """CREATE TABLE badges (
            id {pk},
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            badge TEXT NOT NULL,
            earned_at TEXT NOT NULL,
            UNIQUE (user_id, badge)
        )""",
        """CREATE TABLE inventory (
            id {pk},
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            item TEXT NOT NULL,
            bought_at TEXT NOT NULL,
            UNIQUE (user_id, item)
        )""",
        "ALTER TABLE users ADD COLUMN frame TEXT",
        "ALTER TABLE users ADD COLUMN title TEXT",
        "ALTER TABLE users ADD COLUMN state TEXT",
        "ALTER TABLE users ADD COLUMN board_opt_in INTEGER NOT NULL DEFAULT 0",
        "ALTER TABLE users ADD COLUMN nickname TEXT",
        """CREATE TABLE speed_runs (
            id {pk},
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            day TEXT NOT NULL,
            item_ids TEXT NOT NULL,
            answers TEXT NOT NULL DEFAULT '{}',
            started_ms BIGINT NOT NULL,
            finished_ms BIGINT,
            correct INTEGER,
            total INTEGER NOT NULL,
            score_ms BIGINT,
            ranked INTEGER NOT NULL DEFAULT 0,
            state TEXT,
            created_at TEXT NOT NULL
        )""",
        "CREATE INDEX idx_speed_board ON speed_runs (day, ranked, score_ms)",
        "CREATE INDEX idx_speed_user ON speed_runs (user_id, day)",
        """CREATE TABLE focus_sessions (
            id {pk},
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            minutes INTEGER NOT NULL,
            label TEXT NOT NULL,
            started_ms BIGINT NOT NULL,
            finished_at TEXT,
            seconds INTEGER,
            completed INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )""",
        "CREATE INDEX idx_focus_user ON focus_sessions (user_id, created_at)",
        """CREATE TABLE lesson_progress (
            id {pk},
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            lesson_id TEXT NOT NULL,
            completed_at TEXT NOT NULL,
            best INTEGER NOT NULL DEFAULT 0,
            total INTEGER NOT NULL DEFAULT 0,
            stage INTEGER NOT NULL DEFAULT 0,
            due_on TEXT,
            last_recall_at TEXT,
            UNIQUE (user_id, lesson_id)
        )""",
    ]),
    (11, "Customization: saved preferences (look, dashboard layout, study defaults, drawn avatar) and reminders", [
        "ALTER TABLE users ADD COLUMN prefs TEXT NOT NULL DEFAULT '{}'",
        "ALTER TABLE users ADD COLUMN reminder_sent_on TEXT",
    ]),
    (12, "Market: collectibles whose prices move with what students buy and sell", [
        """CREATE TABLE market_items (
            item TEXT PRIMARY KEY,
            demand REAL NOT NULL DEFAULT 0,
            demand_ms BIGINT NOT NULL DEFAULT 0,
            version INTEGER NOT NULL DEFAULT 0
        )""",
        """CREATE TABLE market_holdings (
            id {pk},
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            item TEXT NOT NULL,
            qty INTEGER NOT NULL DEFAULT 0,
            cost INTEGER NOT NULL DEFAULT 0,
            UNIQUE (user_id, item)
        )""",
        """CREATE TABLE market_trades (
            id {pk},
            user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            item TEXT NOT NULL,
            side TEXT NOT NULL,
            price INTEGER NOT NULL,
            demand_after REAL NOT NULL,
            at_ms BIGINT NOT NULL,
            day TEXT NOT NULL
        )""",
        "CREATE INDEX idx_trades_item ON market_trades (item, at_ms)",
        "CREATE INDEX idx_trades_user ON market_trades (user_id, day)",
        "ALTER TABLE users ADD COLUMN market_seq INTEGER NOT NULL DEFAULT 0",
    ]),
    (13, "History: everything each person does on the site, and every question they answer", [
        """CREATE TABLE user_events (
            id {pk},
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            kind TEXT NOT NULL,
            action TEXT NOT NULL,
            status INTEGER NOT NULL,
            detail TEXT,
            day TEXT NOT NULL,
            at TEXT NOT NULL
        )""",
        "CREATE INDEX idx_events_user ON user_events (user_id, id)",
        """CREATE TABLE question_log (
            id {pk},
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            item_id TEXT NOT NULL,
            source TEXT NOT NULL,
            ref TEXT,
            answer TEXT,
            correct INTEGER,
            day TEXT NOT NULL,
            at TEXT NOT NULL
        )""",
        "CREATE INDEX idx_qlog_user ON question_log (user_id, id)",
        "CREATE INDEX idx_qlog_item ON question_log (user_id, item_id)",
    ]),
    (14, "Pets: eggs that hatch from study XP, and the pets they become", [
        """CREATE TABLE pets (
            id {pk},
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            species TEXT,
            name TEXT,
            egg_base INTEGER NOT NULL DEFAULT 0,
            xp_base INTEGER NOT NULL DEFAULT 0,
            banked INTEGER NOT NULL DEFAULT 0,
            active INTEGER NOT NULL DEFAULT 0,
            gear TEXT,
            hatched_at TEXT,
            created_at TEXT NOT NULL
        )""",
        "CREATE INDEX idx_pets_user ON pets (user_id)",
    ]),
    (15, "Mock tests, copy warnings, first-party analytics and cookie consent records", [
        """CREATE TABLE mock_tests (
            id {pk},
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            section TEXT NOT NULL,
            status TEXT NOT NULL,
            with_break INTEGER NOT NULL DEFAULT 1,
            break_started_at TEXT,
            break_ended_at TEXT,
            m1_session INTEGER,
            m2_session INTEGER,
            route TEXT,
            m1_correct INTEGER,
            m2_correct INTEGER,
            score INTEGER,
            created_at TEXT NOT NULL,
            finished_at TEXT
        )""",
        "CREATE INDEX idx_mock_user ON mock_tests (user_id, created_at)",
        """CREATE TABLE integrity_events (
            id {pk},
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            kind TEXT NOT NULL,
            page TEXT,
            item_id TEXT,
            chars INTEGER NOT NULL DEFAULT 0,
            action TEXT NOT NULL,
            at TEXT NOT NULL
        )""",
        "CREATE INDEX idx_integrity_user ON integrity_events (user_id, at)",
        """CREATE TABLE analytics_events (
            id {pk},
            visitor_id TEXT NOT NULL,
            session_id TEXT,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            kind TEXT NOT NULL,
            path TEXT,
            title TEXT,
            referrer TEXT,
            utm_source TEXT,
            utm_medium TEXT,
            utm_campaign TEXT,
            device TEXT,
            browser TEXT,
            os TEXT,
            screen TEXT,
            viewport TEXT,
            lang TEXT,
            tz TEXT,
            label TEXT,
            duration_ms INTEGER,
            scroll_pct INTEGER,
            day TEXT NOT NULL,
            at TEXT NOT NULL
        )""",
        "CREATE INDEX idx_analytics_day ON analytics_events (day, kind)",
        "CREATE INDEX idx_analytics_visitor ON analytics_events (visitor_id, id)",
        "CREATE INDEX idx_analytics_user ON analytics_events (user_id, id)",
        """CREATE TABLE consent_log (
            id {pk},
            visitor_id TEXT NOT NULL,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            analytics INTEGER NOT NULL,
            version INTEGER NOT NULL,
            gpc INTEGER NOT NULL DEFAULT 0,
            path TEXT,
            user_agent TEXT,
            at TEXT NOT NULL
        )""",
        "CREATE INDEX idx_consent_visitor ON consent_log (visitor_id, id)",
    ]),
    # (16, "Describe your change", ["ALTER TABLE users ADD COLUMN ..."]),
]


def migrate(url):
    """Bring the database up to the latest migration. Safe to run on every start."""
    pk = "SERIAL PRIMARY KEY" if is_postgres(url) else "INTEGER PRIMARY KEY AUTOINCREMENT"
    ph = "%s" if is_postgres(url) else "?"
    conn = connect(url)
    try:
        conn.execute("CREATE TABLE IF NOT EXISTS schema_version (version INTEGER PRIMARY KEY, description TEXT, applied_at TEXT)")
        conn.commit()
        row = conn.execute("SELECT MAX(version) AS v FROM schema_version").fetchone()
        current = (row["v"] if row and row["v"] is not None else 0)
        applied = []
        for version, description, statements in MIGRATIONS:
            if version <= current:
                continue
            for stmt in statements:
                conn.execute(stmt.replace("{pk}", pk))
            stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            conn.execute(f"INSERT INTO schema_version (version, description, applied_at) VALUES ({ph}, {ph}, {ph})", (version, description, stamp))
            conn.commit()
            applied.append(version)
        return applied
    finally:
        conn.close()
