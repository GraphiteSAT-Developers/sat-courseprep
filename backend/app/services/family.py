"""Linking parent accounts to students.

A student makes a one-time code (Account, Parent access) and gives it to a parent, who enters it on
their dashboard. Codes are stored hashed, work once, and expire after CODE_DAYS. Making a new code
cancels the student's earlier unused ones. A student can remove a parent, and a parent can remove a
student, at any time.
"""
import secrets
from datetime import timedelta

from ..db import execute, iso, now, now_iso, parse_iso, query
from ..security import hash_text

CODE_DAYS = 7
ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # no 0/O or 1/I, so codes read out loud cleanly


def clean_code(value):
    """The code as typed (any case, with or without the dash), or None if it can't be a code."""
    code = "".join(ch for ch in str(value or "").upper() if ch.isalnum())
    return code if len(code) == 8 and all(ch in ALPHABET for ch in code) else None


def new_code(student_id):
    code = "".join(secrets.choice(ALPHABET) for _ in range(8))
    stamp = now_iso()
    execute("UPDATE link_codes SET used_at = ? WHERE student_id = ? AND used_at IS NULL", (stamp, student_id))
    expires = iso(now() + timedelta(days=CODE_DAYS))
    execute("INSERT INTO link_codes (student_id, code_hash, expires_at) VALUES (?, ?, ?)", (student_id, hash_text(code), expires))
    return {"code": code[:4] + "-" + code[4:], "expires_at": expires}


def redeem(parent_id, code):
    """Links the parent to the code's student. Returns the student, or None for an unknown, used or expired code."""
    row = query("SELECT * FROM link_codes WHERE code_hash = ?", (hash_text(code),), one=True)
    if not row or row["used_at"] or parse_iso(row["expires_at"]) < now():
        return None
    student = query("SELECT * FROM users WHERE id = ? AND role = 'student'", (row["student_id"],), one=True)
    if not student:
        return None
    execute("UPDATE link_codes SET used_at = ? WHERE id = ?", (now_iso(), row["id"]))
    execute("INSERT INTO family_links (parent_id, student_id, created_at) VALUES (?, ?, ?) "
            "ON CONFLICT (parent_id, student_id) DO NOTHING", (parent_id, student["id"], now_iso()))
    return student


def link(parent_id, student_id):
    return query("SELECT * FROM family_links WHERE parent_id = ? AND student_id = ?", (parent_id, student_id), one=True)


def students_of(parent_id):
    return query("SELECT u.id, u.name, u.grade, u.test_date FROM family_links f JOIN users u ON u.id = f.student_id "
                 "WHERE f.parent_id = ? ORDER BY f.created_at, f.id", (parent_id,))


def parents_of(student_id):
    return query("SELECT u.id, u.name, u.email, f.created_at FROM family_links f JOIN users u ON u.id = f.parent_id "
                 "WHERE f.student_id = ? ORDER BY f.created_at, f.id", (student_id,))


def unlink(parent_id, student_id):
    execute("DELETE FROM family_links WHERE parent_id = ? AND student_id = ?", (parent_id, student_id))


def pending_code(student_id):
    """The student's newest unused, unexpired code's expiry (the code itself is only shown when it's made)."""
    row = query("SELECT expires_at FROM link_codes WHERE student_id = ? AND used_at IS NULL ORDER BY id DESC LIMIT 1",
                (student_id,), one=True)
    return row["expires_at"] if row and parse_iso(row["expires_at"]) >= now() else None
