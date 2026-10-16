# Graphite backend

A Flask server that runs the whole Graphite site: it serves every page in `website/site/`, keeps student accounts, grades practice tests, and powers the dashboard. Data lives in SQLite on your computer and in Postgres when hosted.

## Run it on your computer

You need Python 3.10 or newer.

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env        # optional, the defaults work locally
python wsgi.py
```

Open http://localhost:5000. Create an account from the sign-in page, take the practice test, then open the dashboard.

Emails (welcome, password reset, diagnostic link) are printed in the terminal until you set `SMTP_HOST`.

Run the tests:

```bash
cd backend
python -m unittest discover tests
```

## What it does

| Area | What's stored or computed |
| --- | --- |
| Accounts | Name, email, grade, SAT date, target score, weekly goal. Passwords are hashed with scrypt and never stored. |
| Sign-in | Session cookie (HttpOnly, SameSite=Lax, Secure on HTTPS). "Keep me signed in" lasts 30 days. A password reset signs out every other device. |
| Password reset | One-time link, valid 30 minutes, emailed to the student. Only a hash of the token is saved. |
| Home page form | Saved to `leads`, with an email to the student and, if `ADMIN_EMAIL` is set, to you. |
| Practice tests | The browser gets questions without answers. The server grades, saves the attempt, and returns explanations. |
| Review queue | Every missed question. After the first right answer it comes back in three days; a second right answer clears it. |
| Dashboard | Latest score, score history, domain breakdown, today's set, review queue and a week-by-week plan to the test date, all from the student's own data. |

## Security built in

- Same-site check on every API write (blocks cross-site request forgery), and writes must be JSON.
- Rate limits on sign-in (5 wrong passwords per email per 15 minutes), account creation, password resets and the home page form.
- Honeypot fields on forms to catch bots.
- Sign-in required for `dashboard.html` and `practice-test.html`; visitors are sent to sign in and back.
- HTTPS redirect, HSTS, a Content Security Policy and other security headers in production.

## API

All routes return JSON. Writes need `Content-Type: application/json` and must come from the site itself.

| Method and path | Purpose | Sign-in |
| --- | --- | --- |
| `POST /api/auth/register` | Create an account and sign in | No |
| `POST /api/auth/login` | Sign in | No |
| `POST /api/auth/logout` | Sign out | No |
| `POST /api/auth/forgot` | Email a reset link | No |
| `POST /api/auth/reset` | Set a new password from a reset link | No |
| `GET /api/me`, `PATCH /api/me` | Read or update the student's account | Yes |
| `POST /api/leads` | Home page diagnostic form | No |
| `GET /api/tests` | List practice tests | Yes |
| `GET /api/tests/<id>` | Questions, without answers | Yes |
| `POST /api/tests/<id>/attempts` | Submit answers; returns graded results | Yes |
| `GET /api/tests/<id>/attempts[/<attempt>]` | Past attempts and their results | Yes |
| `GET /api/dashboard` | Everything the dashboard shows | Yes |
| `POST /api/review/<id>/right` | Mark a review question right | Yes |
| `POST /api/activity` | Log practice time | Yes |
| `GET /api/health` | Health check for the host | No |

## Folder layout

```
backend/
  wsgi.py                 entry point (python wsgi.py, or gunicorn wsgi:app)
  app/
    __init__.py           builds the app: security headers, HTTPS, error pages
    config.py             settings from environment variables
    db.py                 database helpers that work on SQLite and Postgres
    schema.py             tables, as numbered migrations
    security.py           sessions, sign-in checks, rate limits, input validation
    routes/               one file per feature (the URLs)
      _example.py         template for a new feature
    services/             the logic behind the routes
    content/tests/        practice tests as JSON
  tests/                  automated tests
```

## Adding to it

**A new feature (for example flashcards or parent accounts):**

1. Copy `app/routes/_example.py` to `app/routes/flashcards.py` and rename the blueprint.
2. Register it in `BLUEPRINTS` in `app/routes/__init__.py`.
3. Put the logic in `app/services/flashcards.py`.
4. Add tests in `tests/`.

**A database change:** add a new entry at the end of `MIGRATIONS` in `app/schema.py`, for example `(2, "Add parent accounts", ["ALTER TABLE users ADD COLUMN ..."])`. It runs once on the next start. Don't edit a migration that has already run on the live site.

**A new practice test:** add a JSON file to `app/content/tests/` shaped like `pt4-math-m1.json`. It appears in `/api/tests` and on the dashboard. The website's offline preview reads the same file when you run `python website/build.py`.

**A new page:** add it to `website/src/pages/`, run `python website/build.py`, and the server serves it automatically. To require sign-in, add its file name to `PROTECTED` in `app/routes/pages.py`.

## Deploying

### Render

1. In Render, choose **New > Blueprint** and pick this repository. `render.yaml` creates the web service and a Postgres database.
2. Set `BASE_URL` to the address Render gives you (or your own domain), and the `SMTP_*` settings from an email provider such as Postmark, Resend or SendGrid.

Two things to know about Render's free plan:

- The free web service sleeps after 15 minutes without visitors and takes about a minute to wake.
- The free Postgres database is deleted 30 days after it's created, after a 14-day grace period. Change `plan: free` under `databases` in `render.yaml` to a paid plan before real students sign up.

Don't run production on SQLite there: the server's disk is wiped on every restart or redeploy.

### Railway

1. Create a project from this repository. Railway reads `requirements.txt` and `Procfile`.
2. Add a Postgres database to the project, then set the web service's `DATABASE_URL` variable to reference it.
3. Set `APP_ENV=production`, a long random `SECRET_KEY`, `BASE_URL`, and the `SMTP_*` settings.

## Not built yet

- Payments (Stripe Checkout and webhooks would go in a new `billing` feature)
- Email verification for new accounts
- Parent accounts and the weekly progress email
- An admin page to see leads and students (for now, query the `leads` and `users` tables)
- Reading and Writing practice tests, and the tutor's AI explanations
