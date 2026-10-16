"""Send this week's progress emails to students (and parents who were opted in).

    python send_weekly.py            send them
    python send_weekly.py --dry-run  list who would get one, and send nothing

Run it once a week, for example on Sunday afternoon. Running it twice in a week is safe: each student
gets at most one email every 6 days. Without SMTP_HOST set, emails are printed instead of sent.
On Render, render.yaml runs this as a weekly cron job. To send from your computer to the live site's
students, set DATABASE_URL to the live database first.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "backend"))

from app import create_app  # noqa: E402
from app.services import engagement  # noqa: E402


def main():
    dry = "--dry-run" in sys.argv
    app = create_app()
    with app.app_context():
        result = engagement.send_weekly(dry_run=dry)
    verb = "Would send" if dry else "Sent"
    print(f"\n  {verb} {result['sent']} weekly email{'s' if result['sent'] != 1 else ''}.")
    for e in result["emails"]:
        print(f"    {e['who']:<7} {e['to']:<36} {e['subject']}")
    if result["skipped"]:
        print("  Skipped: " + ", ".join(f"{n} {why}" for why, n in sorted(result["skipped"].items())))
    print()


if __name__ == "__main__":
    main()
