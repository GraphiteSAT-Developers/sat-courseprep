# Graphite website

Marketing site and dashboard sign-in for Graphite, the AI SAT tutor. Dark graphite gray with a pencil-yellow accent.

## Folders

- `site/`: the finished site. Upload everything in this folder to the root of your web host.
- `src/`: the files you edit.
  - `pages/`: one file per page. The comment on the first line sets that page's title and meta description.
  - `partials/`: the shared header, footer and cookie banner. The dashboard uses `app-header.html` and `app-footer.html`.
  - `site.css`: all styles. Colors, fonts and spacing are set at the top.
  - `site.js`: mobile menu, cookie consent, analytics, forms and the practice question on the home page.
  - `questions.js`: the 22 questions, answers and explanations for the math practice test.
  - `practice-test.js`: the test interface: timer, calculator panel, reference sheet, mark for review, answer elimination, question navigator, review page and results.
  - `htaccess`, `netlify.toml`: server settings for HTTPS, the 404 page, compression and caching.
- `build.py`: rebuilds `site/` from `src/`. Run `python3 build.py` after any edit. Needs Python 3 and Pillow (`pip install pillow`).

## Pages

| Page | File |
| --- | --- |
| Home | `index.html` |
| Sign in | `signin.html` |
| Dashboard (signed-in students) | `dashboard.html` |
| Math practice test with graphing calculator | `practice-test.html` |
| Privacy policy | `privacy.html` |
| Cookie policy | `cookies.html` |
| Terms of service | `terms.html` |
| Not found | `404.html` |

## Before launch

1. Replace the phone number `(954) 555-0142` (fictional), the domain `graphiteprep.com`, the prices and the company name. Search `src/` for each one.
2. Fill in the `CONFIG` block at the top of `src/site.js`:
   - `formEndpoint`: where the diagnostic signup form posts.
   - `authEndpoint` and `dashboardUrl`: sign in. Signing in opens `dashboard.html`.
   - The dashboard shows a sample student until it's connected to your account data. Its sample scores live in `build.py` (`SCORES`, `TARGET`) and `src/pages/dashboard.html`. Protect `dashboard.html` behind sign in on your server.
   - `analytics`: Plausible or GA4. It loads only after a visitor accepts analytics cookies.
3. Have a lawyer review the privacy policy, cookie policy and terms.
4. Run `python3 build.py`, then upload `site/`.

## Practice test calculator

The calculator on the practice test is Topline, from `../topline/`. `build.py` copies it to `site/calculator.html`, starting blank and saving separately from the standalone Topline. Rebuild after changing Topline.

To use the real Desmos calculator instead, you need a paid Desmos API key. See `docs/desmos-integration.md`.

## Hosting

Links use root paths (`/signin.html`), so serve the site from the root of a domain.

- **Apache:** `.htaccess` forces HTTPS, serves the custom 404 and turns on compression.
- **Netlify:** `netlify.toml` does the same.
- **GitHub Pages:** works with a custom domain set on the repository. A project URL such as `username.github.io/sat-courseprep/` would break the root links.
