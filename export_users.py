"""Export everything Graphite has stored about its users to spreadsheet files (CSV).

    python export_users.py        (on Mac, python3)

Works on your computer's local database, or on the live database if DATABASE_URL is set.
Files go into the exports/ folder, which git ignores so student data never gets pushed to GitHub.
Passwords are never exported: only scrambled hashes are stored, and those are left out too.
"""
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "backend"))

from app import create_app  # noqa: E402
from app.db import query  # noqa: E402

USER_COLUMNS = ["id", "name", "email", "grade", "test_date", "target_score", "plan", "weekly_goal_hours",
                "parent_email", "created_at", "last_login_at"]


def write_csv(path, rows, columns):
    # utf-8-sig so Excel opens names with accents correctly
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main():
    app = create_app()
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    out = ROOT / "exports" / stamp
    with app.app_context():
        users = query(f"SELECT {', '.join(USER_COLUMNS)} FROM users ORDER BY id")
        stats = {r["user_id"]: r for r in query(
            "SELECT user_id, COUNT(*) AS tests_taken, MAX(correct) AS best_correct, MAX(total) AS total, MAX(submitted_at) AS last_test_at "
            "FROM test_attempts GROUP BY user_id")}
        open_reviews = {r["user_id"]: r["n"] for r in query(
            "SELECT user_id, COUNT(*) AS n FROM review_items WHERE cleared_at IS NULL GROUP BY user_id")}
        practice = {r["user_id"]: r["s"] for r in query(
            "SELECT user_id, SUM(seconds) AS s FROM activity GROUP BY user_id")}
        for u in users:
            s = stats.get(u["id"], {})
            u["tests_taken"] = s.get("tests_taken", 0)
            u["best_score"] = f"{s['best_correct']}/{s['total']}" if s.get("best_correct") is not None else ""
            u["last_test_at"] = s.get("last_test_at", "")
            u["open_review_questions"] = open_reviews.get(u["id"], 0)
            u["practice_minutes_total"] = round((practice.get(u["id"]) or 0) / 60)

        leads = query("SELECT id, name, email, grade, test_date, target_score, message, created_at FROM leads ORDER BY id")
        attempts = query(
            "SELECT a.id, a.user_id, u.name, u.email, a.test_id, a.correct, a.total, a.seconds_used, a.submitted_at, a.results "
            "FROM test_attempts a JOIN users u ON u.id = a.user_id ORDER BY a.submitted_at")
        for a in attempts:
            a["percent"] = round(a["correct"] / a["total"] * 100)
            a["minutes_used"] = round(a["seconds_used"] / 60, 1)
            by_domain = json.loads(a.pop("results")).get("by_domain", [])
            for d in by_domain:
                a[d["domain"]] = f"{d['right']}/{d['total']}"
        domain_cols = sorted({k for a in attempts for k in a} - {"id", "user_id", "name", "email", "test_id", "correct",
                                                                  "total", "seconds_used", "submitted_at", "percent", "minutes_used"})
        reviews = query(
            "SELECT r.id, r.user_id, u.email, r.test_id, r.question_index, r.domain, r.skill, r.right_count, r.due_on, "
            "r.created_at, r.cleared_at FROM review_items r JOIN users u ON u.id = r.user_id ORDER BY r.user_id, r.id")
        for r in reviews:
            r["question_number"] = r.pop("question_index") + 1

    out.mkdir(parents=True, exist_ok=True)
    write_csv(out / "users.csv", users, USER_COLUMNS + ["tests_taken", "best_score", "last_test_at",
                                                        "open_review_questions", "practice_minutes_total"])
    write_csv(out / "leads.csv", leads, ["id", "name", "email", "grade", "test_date", "target_score", "message", "created_at"])
    write_csv(out / "test_attempts.csv", attempts, ["id", "user_id", "name", "email", "test_id", "correct", "total",
                                                    "percent", "minutes_used", "submitted_at"] + domain_cols)
    write_csv(out / "review_queue.csv", reviews, ["id", "user_id", "email", "test_id", "question_number", "domain",
                                                  "skill", "right_count", "due_on", "created_at", "cleared_at"])

    print(f"\n  Exported from {app.config['DATABASE_URL'].split('@')[-1]}")
    print(f"  {len(users)} accounts, {len(leads)} home page signups, {len(attempts)} test attempts, {len(reviews)} review questions\n")
    for u in users:
        print(f"  {u['id']:>3}  {u['name']:<24} {u['email']:<32} grade {u['grade'] or '-':<3} tests {u['tests_taken']}")
    print(f"\n  Files saved in: {out}\n  Open users.csv in Excel or Google Sheets.\n")


if __name__ == "__main__":
    main()
