"""Small database layer that runs on SQLite locally and Postgres in production.

Write SQL with ? placeholders. On Postgres they are converted to %s.
Use query() to read rows as dicts, and execute() to write (it commits).
"""
import re
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
        # Encrypt the connection to the database unless it's on this machine or the URL says otherwise.
        local = any(h in url for h in ("@localhost", "@127.0.0.1", "@[::1]"))
        extra = {} if local or "sslmode=" in url else {"sslmode": "require"}
        return psycopg.connect(url, row_factory=dict_row, **extra)
    path = url.replace("sqlite:///", "", 1)
    if path != ":memory:":
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


IDENT = re.compile(r"^[a-z_][a-z0-9_]*$")


def set_clause(fields):
    """'a = ?, b = ?' for an UPDATE. Column names come from code, never from a request, and this refuses
    anything that isn't a plain identifier, so a mistake can't turn into SQL injection. Values stay ? parameters."""
    for k in fields:
        if not IDENT.match(k):
            raise ValueError(f"Not a column name: {k!r}")
    return ", ".join(f"{k} = ?" for k in fields)


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


def changed(sql, params=()):
    """Run a write and commit. Returns how many rows it changed (0 means a WHERE guard didn't match)."""
    conn = get_db()
    cur = conn.execute(_sql(sql), params)
    n = cur.rowcount
    conn.commit()
    return n


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
