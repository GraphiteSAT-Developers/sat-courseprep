# Security

How Graphite SAT handles each item on the security checklist, where it lives in the code, and what to do when you
deploy. `backend/tests/test_security.py` checks most of this automatically, and the Security workflow
(`.github/workflows/security.yml`) runs those tests, a dependency audit and a secret scan on every push.

| Item | Status | How |
| --- | --- | --- |
| Hide API keys | Done | Every key (Stripe, Qwen, email, Turnstile, database) is an environment variable read by the server (`backend/app/config.py`). The browser never gets one. A test fails the build if anything secret-looking appears in `website/site/`. |
| Purge git secrets | Done | The whole history was scanned (all 62+ commits): nothing to purge. Only placeholders like `sk_test_...` and fake test keys appear. `.gitignore` blocks `.env`, keys and database files, and gitleaks scans every push. |
| Use public DB key | Not needed | That's for sites where the browser talks to the database directly (Supabase, Firebase). Here the browser only talks to the Flask server; `DATABASE_URL` never leaves it. |
| Enable row level security | Done the server way | Same reason: there's no public database access for row-level security to guard. Every query is scoped to the signed-in account on the server (`WHERE user_id = ?`), and the tests try to reach another student's sets, rounds, focus sessions, review items and parent pages. |
| Encrypt sensitive data | Done | Profile photos, the parent email students enter and home page messages are encrypted with AES-256-GCM (`backend/app/crypto.py`, key: `DATA_KEY`). Passwords, reset tokens and link codes are only ever stored as one-way hashes. The production database connection requires TLS, and Render and Railway encrypt their databases at rest. |
| Enforce server-side auth | Done | Every API route needs a signed-in account except the public ones listed in `test_security.py`, and that test calls every other route signed out to prove it. Parent and student accounts are kept to their own pages. |
| Lock record access | Done | Records are looked up by id and owner together, so another student's id returns "not found". Parents only see students linked to them. |
| Block field tampering | Done | Updates only accept named fields, so role, plan, email, XP and coins can't be set from the browser. Scores are worked out on the server: tests, Level up, speed rounds (server clock), focus sessions (server clock) and lessons (the server grades the answers). Logged practice time is capped. |
| Secure session cookies | Done | HttpOnly, SameSite=Lax, Secure on HTTPS, with the `__Host-` prefix in production. Signed with `SECRET_KEY`; changing a password signs out other devices. |
| Hash passwords | Done | scrypt (Werkzeug). |
| Rate limit login | Done | 5 wrong passwords per email per 15 minutes, 30 tries per network. Also limited: sign-ups, password resets, the home page form, photo uploads, practice-time logging, and a burst limit of 120 writes a minute on every account. |
| Add bot protection | Done | Hidden honeypot fields, plus a signed, short-lived form token that can't be sent back faster than a person could fill in the form (`backend/app/botcheck.py`). Add Cloudflare Turnstile by setting `TURNSTILE_SITE_KEY` and `TURNSTILE_SECRET_KEY`. |
| Parameterize queries | Done | Every value goes in as a `?` parameter. The few statements that name columns in code go through `set_clause()`, which refuses anything that isn't a plain column name. |
| Validate all input | Done | Every field is checked on the server (types, ranges, lists of allowed values, lengths, the curse-word filter). Writes must be JSON from this site, and requests over 9 MB are refused. |
| Escape user content | Done | Pages put user text in with `textContent` or an escaping function, and the Content Security Policy blocks inline scripts as a backstop. Nicknames only allow letters, numbers, spaces and `. _ ' -`. |
| Restrict file uploads | Done | Only PNG, JPEG, WebP and GIF profile photos, up to 6 MB and 40 megapixels. Each is opened, checked, cropped and re-saved, so nothing but a clean image is stored. |
| Trim API responses | Done | Account data goes out through one function that leaves out password hashes, session versions and Stripe ids. Questions go out without answers until checked. Leaderboards show only nickname, state, time and drawn avatar. Errors never include stack traces. |
| Add security headers | Done | Content-Security-Policy, Strict-Transport-Security (2 years, preload), X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, Cross-Origin-Opener-Policy, Cross-Origin-Resource-Policy, and `no-store` on every API response. |
| Force HTTPS | Done | In production every HTTP request is redirected to HTTPS, HSTS tells browsers to never use HTTP, and `upgrade-insecure-requests` covers anything left. |
| Scan dependencies | Done | pip-audit on every push and every Monday; Dependabot opens update pull requests weekly; minimum versions in `backend/requirements.txt` include the latest known fixes. |

## When you deploy

1. Set `SECRET_KEY` and `DATA_KEY` (Render makes both from `render.yaml`). Keep a copy of `DATA_KEY` somewhere safe:
   without it, encrypted photos and messages can't be read.
2. On GitHub, open the repository's **Settings > Code security** and turn on **Dependabot alerts** and **Secret
   scanning**. (They can't be turned on from code.) This repository is public, so keep every secret out of it.
3. Optional: add Cloudflare Turnstile keys for a stronger bot check.
4. Never set `TEST_ACCOUNT` in production. `APP_ENV=production` already turns the beta accounts off.

## Reporting a problem

Email hello@graphiteprep.com with "Security" in the subject. Please don't open a public issue for it.
