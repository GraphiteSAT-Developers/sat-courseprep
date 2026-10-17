"""Sends today's study reminders. Run it once an hour from a cron job on your host:

    cd backend && python remind.py

Render: add a Cron Job service with this command and the schedule "0 * * * *" (see render.yaml).
Railway: add a cron schedule "0 * * * *" to a service that runs this command.
"""
from app import create_app
from app.services import reminders

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        print(f"Sent {reminders.send_due()} reminder(s).")
