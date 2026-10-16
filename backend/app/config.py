"""Settings, read from environment variables. Copy .env.example to .env for local development."""
import os
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
REPO_DIR = BACKEND_DIR.parent


def _load_dotenv():
    """Read backend/.env into the environment without overriding real variables."""
    env_file = BACKEND_DIR / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_dotenv()


def _bool(name, default=False):
    return os.environ.get(name, str(default)).strip().lower() in ("1", "true", "yes", "on")


class Config:
    ENV = os.environ.get("APP_ENV", "development")
    IS_PRODUCTION = ENV == "production"

    SECRET_KEY = os.environ.get("SECRET_KEY") or ("dev-only-change-me" if not IS_PRODUCTION else None)
    DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{BACKEND_DIR / 'instance' / 'graphite.db'}")
    SITE_DIR = Path(os.environ.get("SITE_DIR", REPO_DIR / "website" / "site"))
    CONTENT_DIR = Path(__file__).resolve().parent / "content"

    BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:8000").rstrip("/")
    FORCE_HTTPS = _bool("FORCE_HTTPS", IS_PRODUCTION)

    # Email. Without SMTP_HOST, emails are written to the log instead of sent.
    SMTP_HOST = os.environ.get("SMTP_HOST", "")
    SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
    SMTP_USER = os.environ.get("SMTP_USER", "")
    SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
    MAIL_FROM = os.environ.get("MAIL_FROM", "Graphite <hello@graphiteprep.com>")
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "")

    # Sessions
    SESSION_COOKIE_NAME = "graphite_session"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = FORCE_HTTPS
    REMEMBER_DAYS = 30

    TESTING = False
