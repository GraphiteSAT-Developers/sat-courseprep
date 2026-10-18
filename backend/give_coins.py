"""Gives coins to an account. For the site owner, run on the server (it isn't a web page or API).

    cd backend && python give_coins.py student@example.com 100000

The gift shows in the account's Recent list on the Rewards page as "Gift from Graphite SAT".
"""
import sys
from datetime import date

from app import create_app
from app.db import execute, now_iso, query

if __name__ == "__main__":
    if len(sys.argv) != 3 or not sys.argv[2].lstrip("-").isdigit():
        sys.exit("Usage: python give_coins.py EMAIL AMOUNT")
    email, amount = sys.argv[1].strip().lower(), int(sys.argv[2])
    if not 0 < amount <= 1_000_000:
        sys.exit("Give between 1 and 1,000,000 coins.")
    app = create_app()
    with app.app_context():
        user = query("SELECT id, role FROM users WHERE email = ?", (email,), one=True)
        if not user:
            sys.exit(f"No account with the email {email}.")
        if user["role"] != "student":
            sys.exit("Coins are for student accounts.")
        execute("INSERT INTO xp_events (user_id, kind, xp, coins, detail, day, at) VALUES (?, 'gift', 0, ?, ?, ?, ?)",
                (user["id"], amount, "Gift from Graphite SAT", date.today().isoformat(), now_iso()))
        total = query("SELECT COALESCE(SUM(coins), 0) AS c FROM xp_events WHERE user_id = ?", (user["id"],), one=True)["c"]
        print(f"Gave {amount:,} coins to {email}. They now have {total:,}.")
