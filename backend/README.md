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

When the site runs on your computer, you can sign in with username **beta** and password **beta**. It's created on every start (and its password reset to "beta"), and every sign-in wipes its practice history, so it always starts fresh with the diagnostic. It also starts with 500 coins (and no XP, badges or items) so you can try the shop. It never exists on the hosted site: `APP_ENV=production` turns it off, whatever else is set. To turn it off locally too, set `TEST_ACCOUNT=false` in `backend/.env`.

There's also a test **parent** account: username **beta2**, password **beta2**, already connected to the beta student as its parent. Choose "I'm a parent" on the sign-in page first, then sign in; it opens the parent dashboard. (Before October 2026 this account was called "parent"; it's renamed to beta2 the next time the site starts, keeping its link.) It follows the same rules: local only, never on the hosted site.

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
| `GET /api/dashboard` | Everything the dashboard shows | Yes |
| `POST /api/review/<id>/right` | Mark a review question right | Yes |
| `POST /api/activity` | Log practice time | Yes |
| `PATCH /api/me/appearance` | Theme (dark, light, system), accent color, ripple on or off | Yes |
| `POST /api/me/avatar`, `GET`, `DELETE` | Upload (as a data URL), view or remove the profile picture. Uploads are checked, cropped to a 256px square and re-encoded. | Yes |
| `POST /api/me/email` | Change email (needs the current password; both addresses are emailed) | Yes |
| `POST /api/me/password` | Change password (needs the current one; signs out other devices) | Yes |
| `POST /api/me/sign-out-others` | Sign out every other device | Yes |
| `GET /api/me/export` | Download the account's data as JSON (no passwords) | Yes |
| `POST /api/me/delete` | Delete the account and everything tied to it (needs the password and "DELETE") | Yes |
| `GET /api/checkout` | Plans, prices and the parent's students, for the checkout page | No |
| `POST /api/checkout` | Buy a plan: `{"plan", "interval", "student_id"}`. Returns Stripe's payment page, or starts the plan when Stripe isn't connected | Parent |
| `GET /api/checkout/session/<id>` | After paying on Stripe: confirm the payment and start the plan | Parent |
| `POST /api/parent/billing-portal` | Stripe's page for the parent's card and receipts | Parent |
| `POST /api/stripe/webhook` | Stripe's payment updates (checked with the webhook signature) | Stripe |
| `GET /api/game`, `GET /api/game/summary` | Rewards page data, or just rank, XP, coins and streak | Yes |
| `POST /api/game/buy`, `POST /api/game/equip` | Buy a shop item `{"item"}`; wear or take off a frame or title `{"kind", "value"}` | Yes |
| `GET /api/speed`, `POST /api/speed/start` | Today's round and your results; start (or resume) a round | Yes |
| `POST /api/speed/runs/<id>/answer`, `.../finish` | Answer one question `{"index", "answer"}`; end the round | Yes |
| `GET /api/speed/board?scope=state\|nation&period=today\|week` | A leaderboard, plus where you'd place | Yes |
| `GET /api/speed/nicknames`, `PATCH /api/speed/profile` | Suggested nicknames; leaderboard on or off, nickname, state | Yes |
| `GET /api/focus`, `POST /api/focus/start`, `POST /api/focus/<id>/finish` | Focus timer | Yes |
| `GET /api/lessons`, `GET /api/lessons/<id>`, `POST /api/lessons/<id>/complete` | Lessons and recall checks | Yes |
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

## Plans and prices

Every plan, price and feature list lives in `app/services/plans.py`. The home page pricing section, the parent dashboard and the preview all read from it, so a change there shows up everywhere after `python website/build.py` and a restart.

| Plan | Weekly | Monthly | Yearly |
| --- | --- | --- | --- |
| Scratch Paper (free) | $0 | $0 | $0 |
| No. 2 | $4.99 ($21.62/month) | $19 | $180 ($15/month, 21% off) |
| Sharpened | $9.99 ($43.29/month) | $39 | $348 ($29/month, 26% off) |
| Masterstroke | $34.99 ($151.62/month) | $129 | $1,188 ($99/month, 23% off) |

Prices are always shown per month. The feature lists and the "Compare every feature" table on the home page come from the same file. `LIMITS` there says what each plan allows, but limits aren't enforced yet: every account can use everything. Masterstroke promises a weekly coach check-in, a monthly parent call and priority 24/7 support, and Sharpened promises 24/7 support and video explanations; someone has to deliver those.

## Rewards, speed rounds, focus and lessons

| Feature | Where the rules live | What it does |
| --- | --- | --- |
| Rewards | `app/services/game.py` | XP, 9 ranks, coins, a daily streak (any day with XP), 18 badges and a shop (profile frames, leaderboard titles, 3 extra accent colors). Every reward is a row in `xp_events`, so totals are sums. |
| Level up game layer | `game.level_check`, `game.level_finish` | Each checked answer earns XP; right answers in a row build a combo; the last question of every level is the hardest one (the boss) and pays bonus XP and coins. Finishing, passing, a first clear and a perfect set pay out at the end. |
| Speed round | `app/services/speed.py` | The same 10 quick questions for everyone each day, timed by the server. Each miss adds 15 seconds. The first round of the day is ranked; later ones are practice. Leaderboards for the student's state and nationwide, today and this week. |
| Leaderboard privacy | `speed.py`, Settings > Leaderboard | Off until the student turns it on. Students appear only by a nickname built from math word lists (no free text), their state and their time. Never a name, email, school or photo. |
| Focus timer | `app/services/focus.py` | 15, 25 or 50-minute sessions with a break after. The server keeps the clock and credits only real time. Focus time counts toward the weekly goal, except sessions labeled practice or review, whose time already counts from the sets. |
| Lessons | `app/services/lessons.py`, `app/content/lessons/` | 8 active recall lessons. Every step asks first: answer from memory, predict, fill in a step, put steps in order, or find the mistake. Recall checks come back after 1, 3 and 7 days; passing all three masters the lesson. |

To change a number (XP, prices, ranks, badges), edit `game.py` and rebuild the site (`python website/build.py`) so the preview matches. To add a lesson, add a JSON file to `app/content/lessons/` shaped like the others; the tests check its answers line up.

Lesson scores are sent by the browser (the answers ship with the lesson), so a determined student could fake a lesson score. That only affects their own XP, and XP for repeating a lesson is limited to once a day.

## Curse-word filter

Every free-text box goes through `app/services/wordfilter.py`: names, emails (the part before the @), the home page form's message and anything added later with `clean_name` or `clean_text`. It catches look-alikes (sh1t, $hit, f*ck), stretched letters (fuuuck) and spaced letters (f u c k), but matches whole words, so innocent words like class, Dickens, Scunthorpe and Matsushita are fine. The browser runs the same check (`website/src/wordfilter.js`) to show the message as students type; the server's check is the one that counts. Signing in never runs it, so no existing account can be locked out.

The list is `app/content/blocked_words.txt`, stored in ROT13 so the file isn't a wall of curse words (the file explains how to read and edit it). Rebuild the site after editing it.

## Checkout and Stripe

`checkout.html` is where a parent picks a plan and how to pay (weekly, monthly or yearly). Students and visitors are asked to sign in or create a parent account first; their choices stay in the link. Plan buttons on the home page and the parent dashboard lead there.

Until Stripe is connected, checkout starts the plan right away and the billing history says "No card was charged". To connect Stripe:

1. Create a Stripe account and copy the **test** secret key (Developers > API keys, starts with `sk_test_`).
2. Set `STRIPE_SECRET_KEY` to it (in `backend/.env` on your computer, or in Render or Railway's environment settings).
3. In Stripe, go to Developers > Webhooks and add the endpoint `https://your-site/api/stripe/webhook` with these events: `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted`, `invoice.paid`, `invoice.payment_failed`. Copy its signing secret (`whsec_...`) into `STRIPE_WEBHOOK_SECRET`.
4. Restart the server, then buy a plan with Stripe's test card `4242 4242 4242 4242` (any future date, any CVC).
5. In Stripe, turn on the customer portal (Settings > Billing > Customer portal) so the "Card and receipts" button on the parent dashboard works.
6. When it all works, switch to the live key (`sk_live_...`) and add a live webhook the same way.

No products need to be made in Stripe: the server creates each price from `plans.py` the first time someone buys it. If you change a price, the new price is created automatically and people already paying keep their old price. Canceling, pausing and resuming on the parent dashboard are sent to Stripe too.

On your own computer, Stripe can't reach `127.0.0.1` for webhooks. Checkout still works, because the plan is also started when the parent comes back from Stripe. To test webhooks locally, use the Stripe CLI: `stripe listen --forward-to localhost:8000/api/stripe/webhook`.

## Not built yet

- Plan limits (see `LIMITS` in `app/services/plans.py`)
- Email verification for new accounts
- Sending the weekly progress email to parents
- An admin page to see leads and students (for now, query the `leads` and `users` tables)
- Reading and Writing practice tests, and the tutor's AI explanations
