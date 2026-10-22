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
    # Encrypts profile photos, parent emails and home page messages (app/crypto.py). Set it in production.
    DATA_KEY = os.environ.get("DATA_KEY", "")
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
    MAIL_FROM = os.environ.get("MAIL_FROM", "Graphite SAT <hello@graphiteprep.com>")
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "")
    # Accounts with admin access (app/admins.py): the /admin page, instant plan switching and wiping their own data.
    # Comma-separated emails. Each person signs up normally first; matching the email is what makes them admin.
    ADMIN_ACCOUNTS = frozenset(e.strip().lower() for e in os.environ.get("ADMIN_ACCOUNTS", "").split(",") if e.strip())

    # Payments. Without STRIPE_SECRET_KEY, checkout starts plans without charging (handy for trying the site).
    # Use test keys (sk_test_...) first. STRIPE_WEBHOOK_SECRET (whsec_...) comes from the webhook you add in Stripe.
    STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")
    STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")

    # Requests bigger than this are refused before they're read (profile photos are the largest thing sent).
    MAX_CONTENT_LENGTH = 9 * 1024 * 1024

    # Bot protection on sign-up, the home page form and password resets. Every form needs a short-lived token
    # from /api/form-token and can't be sent back faster than a person could fill it in. Cloudflare Turnstile
    # adds a check on top when both keys are set (free at dash.cloudflare.com > Turnstile).
    TURNSTILE_SITE_KEY = os.environ.get("TURNSTILE_SITE_KEY", "")
    TURNSTILE_SECRET_KEY = os.environ.get("TURNSTILE_SECRET_KEY", "")
    FORM_MIN_SECONDS = 3

    # Sessions. On HTTPS the cookie gets the __Host- prefix: browsers then only accept it from this exact
    # site over HTTPS, never set by a subdomain or over plain HTTP.
    SESSION_COOKIE_NAME = "__Host-graphite_session" if FORCE_HTTPS else "graphite_session"
    SESSION_COOKIE_PATH = "/"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = FORCE_HTTPS
    REMEMBER_DAYS = 30

    TESTING = False

    # A test account, username "beta" and password "beta", for trying the site locally.
    # Never on in production, whatever the environment says: anyone could sign in with it.
    TEST_ACCOUNT = _bool("TEST_ACCOUNT", True) and not IS_PRODUCTION
    # Plan limits (services/access.py): what each plan includes, and paid features locked when a plan isn't paid.
    PLAN_LIMITS = _bool("PLAN_LIMITS", True)
    # First-party analytics (services/analytics.py), only for visitors who accept analytics cookies.
    ANALYTICS = _bool("ANALYTICS", True)
    ANALYTICS_DAYS = int(os.environ.get("ANALYTICS_DAYS", "395"))  # about 13 months, then rows are deleted

    # The AI tutor (services/tutor.py), on Anthropic's Claude API. Off until ANTHROPIC_API_KEY is set; TUTOR_ENABLED=false
    # turns it off again with the key still in place. Off, the tutor shows its "coming soon" state.
    ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
    TUTOR_ENABLED = _bool("TUTOR_ENABLED", True)
    TUTOR_DAILY_CAP = int(os.environ.get("TUTOR_DAILY_CAP", "150"))          # fair-use messages a day, any plan
    TUTOR_SONNET_DAILY_CAP = int(os.environ.get("TUTOR_SONNET_DAILY_CAP", "20"))  # Sonnet replies a day per student
    TUTOR_PER_MINUTE = int(os.environ.get("TUTOR_PER_MINUTE", "8"))          # burst limit per student
    TUTOR_RETENTION_DAYS = int(os.environ.get("TUTOR_RETENTION_DAYS", "90"))  # conversations are deleted after this
