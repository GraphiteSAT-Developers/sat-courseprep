"""Sends email over SMTP. Without SMTP settings, emails go to the log so you can see them while developing."""
import smtplib
from email.message import EmailMessage

from flask import current_app

OUTBOX = []  # The last emails sent, kept in memory for tests and local development.


def send(to, subject, text):
    cfg = current_app.config
    msg = EmailMessage()
    msg["From"], msg["To"], msg["Subject"] = cfg["MAIL_FROM"], to, subject
    msg.set_content(text)
    OUTBOX.append({"to": to, "subject": subject, "text": text})
    del OUTBOX[:-50]
    if not cfg["SMTP_HOST"]:
        current_app.logger.info("Email (not sent, no SMTP_HOST) to %s: %s\n%s", to, subject, text)
        return False
    try:
        with smtplib.SMTP(cfg["SMTP_HOST"], cfg["SMTP_PORT"], timeout=10) as smtp:
            smtp.starttls()
            if cfg["SMTP_USER"]:
                smtp.login(cfg["SMTP_USER"], cfg["SMTP_PASSWORD"])
            smtp.send_message(msg)
        return True
    except (OSError, smtplib.SMTPException):
        current_app.logger.exception("Email to %s failed", to)
        return False
