# Graphite backend

A Flask server that runs the whole Graphite site: it serves every page in `website/site/`, keeps student accounts, grades practice tests, and powers the dashboard. Data lives in SQLite on your computer and in Postgres when hosted.

## Run it on your computer

You need Python 3.10 or newer ([python.org](https://www.python.org/downloads/); on Windows, tick "Add python.exe to PATH" in the installer).

1. Get the latest code: `git pull` in the `sat-courseprep` folder (or clone it again).
2. In VS Code, open the **whole `sat-courseprep` folder** (File > Open Folder), not just `backend` or `website`.
3. Start the server, either way:
   - Press **F5** and pick **Start Graphite**, or
   - Open a terminal (Terminal > New Terminal) and run `python start.py` (on a Mac, `python3 start.py`).
4. Wait for the line **Graphite is running. Open http://127.0.0.1:8000** and open that exact address. The port can be 8080 or 5050 if 8000 is busy, so use the one it prints.
5. Keep that terminal open. Closing it, or pressing Ctrl+C, stops the site.

`start.py` installs Flask if it's missing and picks a free port. Emails (welcome, password reset, diagnostic link) are printed in the terminal until you set `SMTP_HOST`.

### If the browser says "refused to connect"

That means no server is running at that address.

- **The terminal shows an error in red:** the server crashed while starting. Copy the last few lines of the error to get help with it.
- **You opened an HTML file directly,** with VS Code's Live Server, "Open in browser", or by double-clicking: those show the pages without the server, so sign-in and the dashboard won't work. Use `start.py` instead.
- **The address doesn't match:** use the exact address `start.py` prints, including the port number.
- **"python is not recognized" or "command not found":** Python isn't installed or isn't on your PATH. Try `python3` or `py`, or reinstall Python.
- **"No such file start.py":** the terminal is in the wrong folder. Run `cd` to the `sat-courseprep` folder first, or open that folder in VS Code.

### Test account

When the site runs on your computer, you can sign in with username **beta** and password **beta**. It's created on every start (and its password reset to "beta"), and every sign-in wipes its practice history, so it always starts fresh with the diagnostic. It never exists on the hosted site: `APP_ENV=production` turns it off, whatever else is set. To turn it off locally too, set `TEST_ACCOUNT=false` in `backend/.env`.

Run the tests:

```bash
cd backend
python -m unittest discover tests
```

## See your users' data

```bash
python export_users.py
```

Run it from the main `sat-courseprep` folder. It saves `users.csv`, `leads.csv`, `test_attempts.csv` and `review_queue.csv` in a new folder under `exports/`, ready to open in Excel or Google Sheets. Passwords are never included. `exports/` is ignored by git, so student data isn't pushed to GitHub. To export from the live site, set `DATABASE_URL` to the live database first.

## What it does

| Area | What's stored or computed |
| --- | --- |
| Accounts | Name, email, grade, SAT date, target score, weekly goal. Passwords are hashed with scrypt and never stored. |
| Sign-in | Session cookie (HttpOnly, SameSite=Lax, Secure on HTTPS). "Keep me signed in" lasts 30 days. A password reset signs out every other device. |
| Password reset | One-time link, valid 30 minutes, emailed to the student. Only a hash of the token is saved. |
| Home page form | Saved to `leads`, with an email to the student and, if `ADMIN_EMAIL` is set, to you. |
| Practice tests | The browser gets questions without answers. The server grades, saves the attempt, and returns explanations. |
| Question bank | 1,000 original questions in `app/content/bank/`, each with a full explanation: best approach, Desmos steps, by-hand steps, why the wrong choices tempt, and how to enter typed answers. |
| Practice sets | Random practice tests (22 questions, 35 minutes, the real test's domain mix) and topic practice (5–20 questions, untimed, checked one at a time). Every answered question goes on the student's done list and isn't drawn again until every question in that pool is done; then the pool starts over. When only a few are left in a topic, the set is just those, so the student can finish it. |
| Finished topics | Answering the last question of a skill or domain records it once per round and returns it (`finished` in check and submit responses), so the page can congratulate the student. |
| Review queue | Every missed question. After the first right answer it comes back in three days; a second right answer clears it. |
| Desmos masterclass | 13 hands-on lessons in `app/content/masterclass/lessons.json`. The page checks each step against the student's calculator; the server stores how far each student got. |
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
| `GET /api/practice` | Topics with progress, and unfinished sets | Yes |
| `POST /api/practice/sessions` | Start a set: `{"mode": "test"}` or `{"mode": "topic", "domain", "skill", "count"}` | Yes |
| `GET /api/practice/sessions/<id>` | A set's questions (no answers) and any checked answers | Yes |
| `POST /api/practice/sessions/<id>/check` | Topic practice: grade one answer and return its explanation | Yes |
| `POST /api/practice/sessions/<id>/submit` | Finish a set; returns graded results | Yes |
| `GET /api/masterclass` | Desmos masterclass progress, and the next lesson | Yes |
| `POST /api/masterclass/progress` | Save how far a student got in a lesson: `{"lesson", "step"}` (it only goes up) | Yes |
| `POST /api/masterclass/quiz` | Save a practice quiz score: `{"lesson", "correct"}` (the best is kept) | Yes |
| `GET /api/dashboard` | Everything the dashboard shows | Yes |
| `POST /api/review/<id>/right` | Mark a review question right | Yes |
| `POST /api/activity` | Log practice time | Yes |
| `GET /api/health` | Health check for the host | No |

## Folder layout

```
backend/
  wsgi.py                 entry point for hosts (gunicorn wsgi:app); locally, use ../start.py
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
