"""Small database layer that runs on SQLite locally and Postgres in production.

Write SQL with ? placeholders. On Postgres they are converted to %s.
Use query() to read rows as dicts, and execute() to write (it commits).
"""
import sqlite3
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from flask import current_app, g


def is_postgres(url):
    return url.startswith(("postgres://", "postgresql://"))


def connect(url):
    if is_postgres(url):
        import psycopg  # installed from requirements.txt on the host
        from psycopg.rows import dict_row
        return psycopg.connect(url, row_factory=dict_row)
    path = url.replace("sqlite:///", "", 1)
    if path != ":memory:":
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def get_db():
    if "db" not in g:
        g.db = connect(current_app.config["DATABASE_URL"])
    return g.db


def close_db(_exc=None):
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()


def _sql(text):
    if is_postgres(current_app.config["DATABASE_URL"]):
        return text.replace("?", "%s")
    return text


def query(sql, params=(), one=False):
    cur = get_db().execute(_sql(sql), params)
    rows = [dict(r) for r in cur.fetchall()] if cur.description else []
    return (rows[0] if rows else None) if one else rows


def execute(sql, params=()):
    """Run a write and commit. Add RETURNING id to get the new row's id back."""
    conn = get_db()
    cur = conn.execute(_sql(sql), params)
    row = cur.fetchone() if cur.description else None
    conn.commit()
    return dict(row) if row else None


# Time helpers. Times are stored as ISO 8601 text in UTC so both databases agree.
def now():
    return datetime.now(timezone.utc)


def now_iso():
    return now().strftime("%Y-%m-%dT%H:%M:%SZ")


def iso(dt):
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_iso(text):
    return datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def today():
    return date.today()


def days_from_today(n):
    return (date.today() + timedelta(days=n)).isoformat()
