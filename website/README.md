# Graphite website

Marketing site, sign-in, student dashboard and math practice test for Graphite, the AI SAT tutor. Dark graphite gray with a pencil-yellow accent.

The pages run in two modes:

- **Live**, served by the Flask server in `../backend/`. Accounts, test grading and the dashboard use real data. This is how the site runs when hosted. See `../backend/README.md`.
- **Preview**, opened without the server (the files in `artifact/`). Forms show their messages without sending anything, the dashboard shows a sample student, and the test is graded in the browser.

`build.py` writes both: `site/` for the server, `artifact/` for the preview. The practice test questions live in `../backend/app/content/tests/`.

## Folders

- `site/`: the finished site. Upload everything in this folder to the root of your web host.
- `src/`: the files you edit.
  - `pages/`: one file per page. The comment on the first line sets that page's title and meta description.
  - `partials/`: the shared header, footer and cookie banner. The dashboard uses `app-header.html` and `app-footer.html`.
  - `site.css`: all styles. Colors, fonts and spacing are set at the top.
  - `site.js`: mobile menu, cookie consent, analytics, forms and the practice question on the home page.
  - `practice-test.js`: the test interface: timer, calculator panel, reference sheet, mark for review, answer elimination, question navigator, review page and results. With `?session=<id>` it runs a set from the question bank: a timed random practice test, or untimed topic practice with a Check answer button.
  - `practice.js`: the practice page: start a random practice test or practice one topic.
  - `theme.js`: signed-in pages only. Applies the theme and accent color before the page draws, and adds the profile picture to the header.
  - `settings.js`: the Settings page.
  - `checkout.js`: the checkout page.
  - `game-ui.js`: the rank/XP/streak/coins strip and the reward pop-ups, shared by the pages below.
  - `rewards.js`, `speed.js`, `focus.js`, `lessons.js`, `dash-play.js`: the Rewards, Speed round, Focus and Lessons pages, and the dashboard's "Play and earn" panel.
  - `dash-layout.js`: the dashboard's layout and pinned shortcuts from Settings.
  - `theme.js` also keeps the student's other preferences (`GraphiteTheme.prefs()`) and draws the drawn avatar (`GraphiteTheme.drawAvatar(parts)`).
  - `wordfilter.js`: the curse-word check on every text box. `build.py` fills in the list from the backend and puts it at the start of `site.js`.
  - `play-local.js`: preview only. Runs rewards, speed rounds, focus and lessons in the browser when there's no server, with sample players on the leaderboards.
  - `ripple.js`: the dashboard's ripple background.
  - `practice-local.js`: preview only. Runs the practice requests in the browser when there's no server.
  - `htaccess`, `netlify.toml`: server settings for HTTPS, the 404 page, compression and caching.
- `build.py`: rebuilds `site/` from `src/`. Run `python3 build.py` after any edit. Needs Python 3 and Pillow (`pip install pillow`).

## Pages

| Page | File |
| --- | --- |
| Home | `index.html` |
| Sign in | `signin.html` |
| Dashboard (signed-in students) | `dashboard.html` |
| Practice: random practice test or one topic | `practice.html` |
| Math practice test with graphing calculator | `practice-test.html` |
| Settings: profile picture or drawn avatar, name, themes, colors, text size and font, study goals, practice defaults, dashboard layout, leaderboard, email, password, data | `settings.html` |
| Checkout: pick a plan and how to pay, then pay on Stripe | `checkout.html` |
| Lessons: active recall lessons and recall checks | `lessons.html` |
| Speed round and leaderboards | `speed.html` |
| Focus timer | `focus.html` |
| Rewards: rank, badges and the shop | `rewards.html` |
| Privacy policy | `privacy.html` |
| Cookie policy | `cookies.html` |
| Terms of service | `terms.html` |
| Not found | `404.html` |

## Before launch

1. Replace the phone number `(954) 555-0142` (fictional), the domain `graphiteprep.com` and the company name. Search `src/` for each one. Plans and prices are set in `../backend/app/services/plans.py`; the home page's `{{PRICING}}` block is built from it.
2. In the `CONFIG` block at the top of `src/site.js`, set `analytics` to Plausible or GA4. It loads only after a visitor accepts analytics cookies. The form and sign-in endpoints are already set to the backend's API in live mode.
3. Set up the backend's environment variables, including email. See `../backend/README.md`.
4. Have a lawyer review the privacy policy, cookie policy and terms.
5. Run `python3 build.py` and deploy the repository with the backend.

## Practice test calculator

The calculator on the practice test is Topline, from `../topline/`. `build.py` copies it to `site/calculator.html`, starting blank and saving separately from the standalone Topline. Rebuild after changing Topline.

To use the real Desmos calculator instead, you need a paid Desmos API key. See `docs/desmos-integration.md`.

## Hosting

Deploy the whole repository with the backend (Render or Railway). Instructions are in `../backend/README.md`.

`.htaccess` and `netlify.toml` in `site/` are for hosting the pages alone without the backend. In that case the forms, sign-in, dashboard and practice test won't work, because they need the server.
