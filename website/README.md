# Graphite website

Marketing site and dashboard sign-in for Graphite, the AI SAT tutor. Dark graphite gray with a pencil-yellow accent.

## Folders

- `site/`: the finished site. Upload everything in this folder to the root of your web host.
- `src/`: the files you edit.
  - `pages/`: one file per page. The comment on the first line sets that page's title and meta description.
  - `partials/`: the header and footer shared by every page, including the cookie banner.
  - `site.css`: all styles. Colors, fonts and spacing are set at the top.
  - `site.js`: mobile menu, cookie consent, analytics, forms and the practice question on the home page.
  - `htaccess`, `netlify.toml`: server settings for HTTPS, the 404 page, compression and caching.
- `build.py`: rebuilds `site/` from `src/`. Run `python3 build.py` after any edit. Needs Python 3 and Pillow (`pip install pillow`).

## Pages

| Page | File |
| --- | --- |
| Home | `index.html` |
| Sign in | `signin.html` |
| Privacy policy | `privacy.html` |
| Cookie policy | `cookies.html` |
| Terms of service | `terms.html` |
| Not found | `404.html` |

## Before launch

1. Replace the phone number `(954) 555-0142` (fictional), the domain `graphiteprep.com`, the prices and the company name. Search `src/` for each one.
2. Fill in the `CONFIG` block at the top of `src/site.js`:
   - `formEndpoint`: where the diagnostic signup form posts.
   - `authEndpoint` and `dashboardUrl`: sign in.
   - `analytics`: Plausible or GA4. It loads only after a visitor accepts analytics cookies.
3. Have a lawyer review the privacy policy, cookie policy and terms.
4. Run `python3 build.py`, then upload `site/`.

## Hosting

Links use root paths (`/signin.html`), so serve the site from the root of a domain.

- **Apache:** `.htaccess` forces HTTPS, serves the custom 404 and turns on compression.
- **Netlify:** `netlify.toml` does the same.
- **GitHub Pages:** works with a custom domain set on the repository. A project URL such as `username.github.io/sat-courseprep/` would break the root links.
