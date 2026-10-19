"""Build Graphite SAT into two outputs:
site/      deployable site (linked CSS/JS, root-absolute links, server files)
artifact/  self-contained pages for the hosted preview (inlined CSS/JS/images)
"""
import base64, hashlib, importlib, json, re, shutil, sys, types, urllib.parse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
SRC = ROOT / "src"
DIST = ROOT / "site"
ART = ROOT / "artifact"
SITE = "https://www.graphiteprep.com"
# Lexend (headings, designed for easy reading) and Nunito (body, rounded) keep the site friendly for students.
# IBM Plex Mono is only for the keys a student types into Desmos.
FONTS = ("https://fonts.googleapis.com/css2?family=Lexend:wght@500;600;700"
         "&family=Nunito:wght@400;600;700;800&family=IBM+Plex+Mono:wght@500&display=swap")
# Every page: Newsreader for headlines, IBM Plex Sans and Mono for text and numbers,
# and Kalam for the tutor's red-pen notes.
PAPER_FONTS = ("https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,500;6..72,600;6..72,700"
               "&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=Kalam:wght@400;700"
               "&family=Nunito:wght@400;700;800&display=swap")  # Nunito: the "rounded" font choice in Settings
# The logo: the end of a pencil (yellow paint, wood, graphite core).
FAVICON_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><polygon points="32,3 57,17.5 57,46.5 32,61 7,46.5 7,17.5" fill="#f2c14e"/>'
               '<path d="M32 32L57 17.5V46.5ZM32 32V61L7 46.5ZM32 32L7 17.5L32 3Z" fill="#000" fill-opacity=".12"/>'
               '<circle cx="32" cy="32" r="16" fill="#e9c79a"/><circle cx="32" cy="32" r="8" fill="#2d3136"/></svg>')

header = (SRC / "partials/header.html").read_text()
footer = (SRC / "partials/footer.html").read_text()
app_header = (SRC / "partials/app-header.html").read_text()
parent_header = (SRC / "partials/parent-header.html").read_text()
settings_header = (SRC / "partials/settings-header.html").read_text()
app_footer = (SRC / "partials/app-footer.html").read_text()
banner = (SRC / "partials/cookie-banner.html").read_text()
TOPLINE = ROOT.parent / "topline" / "index.html"

def calculator_html():
    """Topline, adapted for the site: blank on first open, saved separately for each page (the iframe's data-calc), not indexed."""
    t = TOPLINE.read_text()
    swaps = [
        ("const STORE = 'plotline-state-v1';", "const STORE = (window.TOPLINE_EMBED && window.TOPLINE_EMBED.store) || 'plotline-state-v1';"),
        ("if (!load()) rows = exampleRows();", "if (!load()) rows = window.TOPLINE_EMBED ? (colorCounter = 0, [newRow('')]) : exampleRows();"),
        ("<head>\n", "<head>\n<meta name=\"robots\" content=\"noindex\">\n<meta name=\"description\" content=\"Graphite SAT graphing calculator for SAT Math practice.\">\n<script>window.TOPLINE_EMBED = { store: 'graphite-calc-v1-' + ((window.frameElement && frameElement.dataset.calc) || 'page') };</script>\n"),
    ]
    for old, new in swaps:
        assert t.count(old) == 1, "Topline changed; update calculator_html(): " + old[:40]
        t = t.replace(old, new)
    return t
# site.css, then paper.css: the site's look, scoped to html.paper so the other themes in Settings still work.
css = (SRC / "site.css").read_text() + "\n" + (SRC / "paper.css").read_text()
BLOCKED_WORDS = Path(__file__).resolve().parent.parent / "backend" / "app" / "content" / "blocked_words.txt"


def wordfilter_js():
    """The curse-word filter for every page, with the backend's list (still ROT13) filled in."""
    words = [l.strip() for l in BLOCKED_WORDS.read_text().splitlines() if l.strip() and not l.startswith("#")]
    return (SRC / "wordfilter.js").read_text().replace('"__BLOCKED_WORDS__"', json.dumps(words))


js = wordfilter_js() + "\n" + (SRC / "site.js").read_text()

def minify_css(s):
    s = re.sub(r"/\*.*?\*/", "", s, flags=re.S)
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s*([{};:,>])\s*", r"\1", s)
    return s.replace(";}", "}").strip()

def load_pages():
    pages = []
    for p in sorted((SRC / "pages").glob("*.html")):
        text = p.read_text()
        m = re.match(r"<!--(\{.*?\})-->\n", text, flags=re.S)
        meta = json.loads(m.group(1))
        meta["body"] = text[m.end():]
        pages.append(meta)
    return pages

JSONLD = {
    "@context": "https://schema.org", "@type": "EducationalOrganization",
    "name": "Graphite SAT", "url": SITE + "/", "logo": SITE + "/apple-touch-icon.png",
    "email": "hello@graphiteprep.com", "telephone": "+1-954-555-0142",
    "description": "AI SAT tutoring for high school students.",
}

SCORES = [("Diagnostic", "Aug 30", 1180, 600, 580), ("Practice test 2", "Sep 20", 1230, 610, 620),
          ("Practice test 3", "Oct 11", 1290, 640, 650)]
TARGET = 1450

def score_chart():
    """Total score line on one 1100-1600 scale, target as a dashed reference line."""
    W, H, L, R, T, B = 640, 250, 52, 110, 16, 34
    lo, hi = 1100, 1500
    pw, ph = W - L - R, H - T - B
    y = lambda v: T + ph * (hi - v) / (hi - lo)
    n = len(SCORES)
    x = lambda i: L + pw * i / (n - 1)
    out = [f'<div class="chart-wrap"><svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="chart-title chart-desc">',
           '<title id="chart-title">Total practice test score</title>',
           f'<desc id="chart-desc">Total score rose from {SCORES[0][2]} on the diagnostic to {SCORES[-1][2]} on {SCORES[-1][0].lower()}. Target {TARGET}.</desc>']
    for v in range(lo, hi + 1, 100):
        out.append(f'<line class="grid" x1="{L}" x2="{W - R}" y1="{y(v):.1f}" y2="{y(v):.1f}"/>')
        out.append(f'<text class="axis-text" x="{L - 10}" y="{y(v) + 4:.1f}" text-anchor="end">{v}</text>')
    out.append(f'<line class="target" x1="{L}" x2="{W - R}" y1="{y(TARGET):.1f}" y2="{y(TARGET):.1f}"/>')
    out.append(f'<text class="target-text" x="{W - R + 10}" y="{y(TARGET) + 4:.1f}">Target {TARGET}</text>')
    pts = " ".join(f"{x(i):.1f},{y(s[2]):.1f}" for i, s in enumerate(SCORES))
    area = f"M{x(0):.1f},{y(lo):.1f} L" + " L".join(f"{x(i):.1f},{y(s[2]):.1f}" for i, s in enumerate(SCORES)) + f" L{x(n - 1):.1f},{y(lo):.1f} Z"
    out.append(f'<path class="area" d="{area}"/>')
    out.append(f'<polyline class="line" points="{pts}"/>')
    for i, s in enumerate(SCORES):
        anchor = "start" if i == 0 else ("end" if i == n - 1 else "middle")
        out.append(f'<text class="axis-text" x="{x(i):.1f}" y="{H - 8}" text-anchor="{anchor}">{s[1]}</text>')
        out.append(f'<circle class="hit" cx="{x(i):.1f}" cy="{y(s[2]):.1f}" r="18" tabindex="0" data-label="{s[0]}" data-score="{s[2]}" data-detail="R&amp;W {s[3]} · Math {s[4]}" aria-label="{s[0]}, {s[1]}: {s[2]}"/>')
        out.append(f'<circle class="pt" cx="{x(i):.1f}" cy="{y(s[2]):.1f}" r="{6 if i == n - 1 else 5}"/>')
    last = SCORES[-1]
    out.append(f'<text class="end-text" x="{x(n - 1) + 12:.1f}" y="{y(last[2]) + 5:.1f}">{last[2]}</text>')
    out.append('</svg><div class="chart-tip" id="chart-tip" role="status" hidden></div></div>')
    return "\n".join(out)

TESTS_DIR = ROOT.parent / "backend" / "app" / "content" / "tests"
SERVICES = ROOT.parent / "backend" / "app" / "services"
# Preview-only scripts. They carry answer keys, so the live site never serves them: there the backend grades.
PREVIEW_ONLY = {"questions.js", "bank.js", "practice-local.js", "play-local.js"}


def service(name):
    """One of the backend's services, loaded without the Flask app around it. Their database helpers
    (app/db.py) are stand-ins here: the build only reads constants and content, it never touches a database."""
    if "graphite_app.services" not in sys.modules:
        app_pkg = types.ModuleType("graphite_app")
        app_pkg.__path__ = []
        db = types.ModuleType("graphite_app.db")
        for fn in ("execute", "changed", "query", "now_iso", "parse_iso", "local_day", "days_from_today", "today", "connect", "is_postgres", "now", "iso"):
            setattr(db, fn, lambda *a, **k: None)
        svc = types.ModuleType("graphite_app.services")
        svc.__path__ = [str(SERVICES)]
        sys.modules.update({"graphite_app": app_pkg, "graphite_app.db": db, "graphite_app.services": svc})
    return importlib.import_module("graphite_app.services." + name)


def pricing_html():
    """The home page's plans, from backend/app/services/plans.py so prices match billing everywhere.
    Every price is shown per month; the Weekly / Monthly / Yearly switch (site.js) changes what's billed."""
    P = service("plans")
    esc = lambda t: str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    best = max(P.savings(k, "year")["percent"] for k in P.ORDER if k != "free")
    def billed(key, iv):
        cents = P.PLANS[key]["prices"][iv]
        if not cents:
            return "Free forever. No card needed."
        return {"week": f"Billed {P.money(cents)} weekly. Stop anytime.", "month": "Billed monthly. Cancel anytime.",
                "year": f"Billed {P.money(cents)} yearly."}[iv]
    def saving(key, iv):
        sv = P.savings(key, iv)
        if key == "free":
            return ""
        if iv == "year":
            return f"Save {P.money(sv['per_year_cents'])} a year ({sv['percent']}% off)"
        return "No commitment" if iv == "week" else ""
    cards = []
    for i, key in enumerate(P.ORDER):
        p = P.PLANS[key]
        attrs = " ".join(f'data-{iv}-amount="{esc(P.money(P.per_month(key, iv)))}" data-{iv}-billed="{esc(billed(key, iv))}" '
                         f'data-{iv}-save="{esc(saving(key, iv))}"' for iv in P.INTERVALS)
        badge = f'<span class="tier-badge">{esc(p["badge"])}</span>' if p["badge"] else ""
        intro = f'<p class="tier-intro">{esc(p["intro"])}</p>' if p["intro"] else ""
        feats = "".join(f"<li>{esc(f)}</li>" for f in p["features"])
        cta = ('<a class="btn btn-secondary btn-block" href="#start" data-track="plan_free">Start free</a>' if key == "free" else
               f'<a class="btn {"btn-primary" if p["badge"] == "Most popular" else "btn-secondary"} btn-block" href="checkout.html?plan={key}&amp;interval=year" '
               f'data-checkout="{key}" data-track="plan_{key}">Choose {esc(p["name"])}</a>')
        save = saving(key, "year")
        cards.append(f"""<article class="tier tier-{key}{' tier-featured' if p['badge'] == 'Most popular' else ''}" aria-labelledby="tier-{key}" {attrs}>
            <div class="tier-head"><div class="tier-name"><h3 id="tier-{key}">{esc(p["name"])}</h3>{badge}</div><p class="tier-tagline">{esc(p["tagline"])}</p></div>
            <div class="tier-price"><p class="price"><span class="amount" data-amount>{esc(P.money(P.per_month(key, "year")))}</span><span class="per">/month</span></p>
              <p class="tier-billed" data-billed>{esc(billed(key, "year"))}</p><p class="tier-save" data-save{'' if save else ' hidden'}>{esc(save)}</p></div>
            {cta}
            {intro}<ul class="tier-features">{feats}</ul>
          </article>""")
    toggle = f"""<div class="billing-switch" role="radiogroup" aria-label="How you pay">
            <span><input type="radio" name="billing" id="bill-week" value="week"><label for="bill-week">Weekly</label></span>
            <span><input type="radio" name="billing" id="bill-month" value="month"><label for="bill-month">Monthly</label></span>
            <span><input type="radio" name="billing" id="bill-year" value="year" checked><label for="bill-year">Yearly <em>Save up to {best}%</em></label></span>
          </div>"""
    return toggle + '\n          <div class="tiers">' + "\n          ".join(cards) + "</div>"


def compare_html():
    """The "Compare every feature" table under the plans, from COMPARE in plans.py.
    A table on wide screens; on phones each feature becomes a small card with the four plans under it."""
    P = service("plans")
    esc = lambda t: str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    names = [P.PLANS[k]["name"] for k in P.ORDER]
    def cell(v):
        if v is True:
            return '<span class="yes" aria-hidden="true"></span><span class="visually-hidden">Included</span>'
        if v is False:
            return '<span class="no" aria-hidden="true"></span><span class="visually-hidden">Not included</span>'
        return esc(v)
    feat = lambda k: ' class="is-featured"' if P.PLANS[k]["badge"] == "Most popular" else ""
    head = "".join(f'<th scope="col"{feat(k)}>{esc(P.PLANS[k]["name"])}</th>' for k in P.ORDER)
    groups = []
    for title, rows in P.COMPARE:
        body = "".join(
            '<tr><th scope="row">' + esc(label) + "</th>" + "".join(
                f'<td data-plan="{esc(names[i])}"{feat(P.ORDER[i])}>{cell(v)}</td>'
                for i, v in enumerate(vals)) + "</tr>" for label, vals in rows)
        groups.append(f'<tbody><tr class="compare-group"><th scope="colgroup" colspan="5">{esc(title)}</th></tr>{body}</tbody>')
    featured = next(i for i, k in enumerate(P.ORDER) if P.PLANS[k]["badge"] == "Most popular")
    pick = "".join(f'<span><input type="radio" name="compare-show" id="compare-show-{i}" value="{i}"{" checked" if i == featured else ""}>'
                   f'<label for="compare-show-{i}">{esc(n)}</label></span>' for i, n in enumerate(names))
    return (f'''<div class="compare" id="compare" data-show="{featured}">
          <h3 class="compare-title">Compare every feature</h3>
          <div class="compare-pick" role="radiogroup" aria-label="Show plan">{pick}</div>
          <table class="compare-table">
            <caption class="visually-hidden">What each Graphite SAT plan includes</caption>
            <thead><tr><th scope="col"><span class="visually-hidden">Feature</span></th>{head}</tr></thead>
            {"".join(groups)}
          </table>
          <p class="fine compare-more">And more to come: new practice tests, question sets and tutor features are added as they're ready.</p>
        </div>''')


def plans_json():
    """Plans and prices for checkout.html, read by checkout.js. Same numbers as everywhere else."""
    P = service("plans")
    return ('<script type="application/json" id="plans-data">'
            + json.dumps(P.public_plans(), separators=(",", ":")).replace("</", "<\\/") + "</script>")


def bank_js():
    """The question bank for the offline preview, built by the backend's own bank module (same HTML, same keys)."""
    bank, diagnostic, studyplan, levels, plans = (service(n) for n in ("bank", "diagnostic", "studyplan", "levels", "plans"))
    game, speed, focus, lessons = (service(n) for n in ("game", "speed", "focus", "lessons"))
    keep = ("id", "domain_key", "domain", "skill", "skill_key", "difficulty", "type", "stem", "choices",
            "answer", "keys", "answer_text", "explain_html")
    data = {
        "items": [{k: q[k] for k in keep if k in q} for q in bank.all_items().values()],
        "topics": bank.topics(), "mix": bank.MODULE_MIX, "order": bank.DIFFICULTY_ORDER,
        "test": {"questions": sum(bank.MODULE_MIX.values()), "minutes": bank.MODULE_MINUTES},
        "topic_counts": [5, 10, 15, 20],
        "rw": [{k: q[k] for k in ("id", "section", "domain", "skill", "type", "stem", "choices", "answer", "explain_html")}
               for q in diagnostic.rw_items().values()],
        "diagnostic": {"math_slots": diagnostic.MATH_SLOTS, "rw_domains": diagnostic.RW_DOMAINS,
                       "weight": diagnostic.DIFFICULTY_WEIGHT, "sure": diagnostic.SURE, "guess": diagnostic.GUESS,
                       "strong": diagnostic.STRONG, "weak": diagnostic.WEAK, "phases": studyplan.PHASES,
                       "checklist": studyplan.TEST_WEEK_CHECKLIST},
        "levels": {"size": levels.SIZE, "pass": levels.PASS, "count": levels.LEVELS,
                   "tracks": [{"key": t["key"], "name": t["name"], "skills": t["skills"]} for t in levels.tracks()],
                   "rungs": [{"n": n, "tier": levels.tier(n), "mix": levels.mix(n), "mix_label": studyplan.mix_label(levels.mix(n))}
                             for n in range(1, levels.LEVELS + 1)]},
        "parent": {"plans": plans.public_plans(),
                   "alert_days": list(plans.ALERT_DAYS), "pause_days": plans.PAUSE_DAYS,
                   "trial": {"plan": plans.TRIAL_PLAN, "plan_name": plans.PLANS[plans.TRIAL_PLAN]["name"], "days": plans.TRIAL_DAYS},
                   # Plan locks and mock tests: the same rules as services/access.py and services/mock.py.
                   "limits": plans.LIMITS, "order": list(plans.ORDER),
                   "features": {k: {"limit": v[0], "name": v[1], "period": v[2]} for k, v in service("access").FEATURES.items()},
                   "unpaid": service("access").UNPAID, "locked_explanation": service("access").LOCKED_EXPLANATION},
        "mock": {"sections": service("mock").SECTIONS, "break_seconds": service("mock").BREAK_SECONDS,
                 "route_at": service("mock").ROUTE_AT, "mix": service("mock").MIX},
        # Rewards, speed rounds, focus and lessons: the same numbers and content as the server (play-local.js).
        "play": {"rules": game.rules(), "lessons": lessons.all_lessons(), "recall_days": list(lessons.RECALL_DAYS),
                 "recall_pass": lessons.RECALL_PASS, "lesson_formats": lessons.FORMATS, "start_lesson": lessons.START_LESSON, "free_lessons": list(lessons.FREE_LESSONS),
                 "topic_names": lessons.topic_names(),
                 "speed": {"size": speed.SIZE, "penalty_ms": speed.PENALTY_MS, "max_ms": speed.MAX_MS,
                           "lightning_ms": speed.LIGHTNING_MS, "states": [{"code": c, "name": n} for c, n in speed.STATES],
                           "adjectives": speed.ADJECTIVES, "nouns": speed.NOUNS, "domains": sorted(speed.DOMAINS)},
                 "focus": {"lengths": [{"minutes": m, "break": focus.BREAKS[m]} for m in focus.LENGTHS],
                           "labels": [{"key": k, "name": v} for k, v in focus.LABELS.items()],
                           "counted_elsewhere": sorted(focus.COUNTED_ELSEWHERE), "finish_share": focus.FINISH_SHARE,
                           "min_credit": focus.MIN_CREDIT},
                 "market": service("market").rules(), "pet": service("pet").rules()},
    }
    return "window.GRAPHITE_BANK = " + json.dumps(data, separators=(",", ":")).replace("</", "<\\/") + ";"


def script_source(name):
    """Page scripts. questions.js is generated from the backend's test JSON, the single source of questions."""
    if name == "questions.js":
        test = json.loads((TESTS_DIR / "pt4-math-m1.json").read_text())
        return "var GRAPHITE_TEST = " + json.dumps(test) + ";"
    if name == "bank.js":
        return bank_js()
    return (SRC / name).read_text()


# "You are here" trail under the header: the home of that part of the site, then this page.
DASH = ("Dashboard", "dashboard.html")
HOME = ("Home", "./")
CRUMBS = {
    "dashboard.html": [], "plan.html": [DASH], "practice.html": [DASH], "levels.html": [DASH], "lessons.html": [DASH],
    "speed.html": [DASH], "focus.html": [DASH], "rewards.html": [DASH], "market.html": [DASH], "tutor.html": [DASH], "settings.html": [DASH],
    "parent.html": [], "privacy.html": [HOME], "terms.html": [HOME], "cookies.html": [HOME], "checkout.html": [HOME],
    "signin.html": [HOME], "404.html": [HOME],
}
CRUMB_NAMES = {"dashboard.html": "Dashboard", "parent.html": "Parent dashboard", "privacy.html": "Privacy policy",
               "terms.html": "Terms of service", "cookies.html": "Cookie policy", "signin.html": "Sign in",
               "404.html": "Page not found", "plan.html": "Study plan", "levels.html": "Level up"}


def crumbs_html(meta):
    trail = CRUMBS.get(meta["file"])
    if trail is None or meta.get("test"):
        return ""
    name = CRUMB_NAMES.get(meta["file"]) or meta["title"].split(" | ")[0]
    esc = lambda t: str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    items = "".join(f'<li><a href="{href}"{" data-crumb-home" if href == "dashboard.html" else ""}>{esc(label)}</a></li>' for label, href in trail)
    items += f'<li><span aria-current="page" id="crumb-here">{esc(name)}</span></li>'
    return f'<div class="crumbs-bar"><nav class="wrap crumbs" aria-label="You are here"><ol id="crumbs">{items}</ol></nav></div>\n'


KATEX = SRC / "vendor" / "katex"


def katex_css_inline():
    """KaTeX's stylesheet with its fonts as woff2 data URIs, for the self-contained preview."""
    css = (KATEX / "katex.min.css").read_text()
    def font(m):
        name = m.group(1)
        data = base64.b64encode((KATEX / "fonts" / (name + ".woff2")).read_bytes()).decode()
        return "src:url(data:font/woff2;base64," + data + ") format(\"woff2\")"
    out = re.sub(r"src:url\(fonts/([\w-]+)\.woff2\) format\(\"woff2\"\)(?:,url\([^)]*\) format\(\"[a-z]+\"\))*", font, css)
    assert "fonts/" not in out, "KaTeX css changed; update katex_css_inline()"
    return out


def render(meta, mode):
    is_home = meta["file"] == "index.html"
    h = "" if is_home else "./"
    if meta.get("test"):
        head_nav, foot = "", ""
    elif meta.get("parent"):
        head_nav, foot = parent_header, app_footer
    elif meta.get("settings"):
        head_nav, foot = settings_header, app_footer
    elif meta.get("app"):
        head_nav, foot = app_header, app_footer
    else:
        head_nav = header.replace("{{H}}", h).replace("{{SIGNIN_CURRENT}}", ' aria-current="page"' if meta.get("signin") else "")
        foot = footer.replace("{{H}}", h)
    page_body = meta["body"].replace("{{SCORE_CHART}}", score_chart())
    if "{{PRICING}}" in page_body:
        page_body = page_body.replace("{{PRICING}}", pricing_html())
    if "{{COMPARE}}" in page_body:
        page_body = page_body.replace("{{COMPARE}}", compare_html())
    if "{{PLANS_JSON}}" in page_body:
        page_body = page_body.replace("{{PLANS_JSON}}", plans_json())
    body = head_nav + crumbs_html(meta) + page_body + foot + ("" if meta.get("test") else banner)
    # The logo on pages anyone can open: the server's /home sends a signed-in account to its own dashboard and
    # everyone else to the home page. The preview has no server, so there site.js points it at the dashboard.
    body = body.replace("{{LOGO}}", "/home" if mode == "dist" else "./")
    url = SITE + meta["path"]
    robots = meta.get("robots", "index, follow")

    if mode == "dist":
        icons = ('<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
                 '<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">\n'
                 '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n'
                 '<link rel="manifest" href="/site.webmanifest">')
        styles = '<link rel="stylesheet" href="/css/site.css">'
        if meta.get("katex"):
            styles += '<link rel="stylesheet" href="/vendor/katex/katex.min.css">'
        # Served by the backend: site.js first (it sets up the API helper), and never the answer key.
        script = '<script src="/js/site.js" defer></script>' + ('<script src="/vendor/katex/katex.min.js" defer></script>' if meta.get("katex") else "") + "".join(
            f'<script src="/js/{n}" defer></script>' for n in meta.get("scripts", []) if n not in PREVIEW_ONLY)
        canonical = f'<link rel="canonical" href="{url}">' if robots.startswith("index") else ""
        # Root-absolute internal links so pages work from any URL, including the 404 page
        body = re.sub(r'href="\./', 'href="/', body)
        body = re.sub(r'href="([a-z0-9-]+\.html)', r'href="/\1', body)
        body = body.replace('src="assets/', 'src="/assets/')
    else:
        fav = "data:image/svg+xml," + urllib.parse.quote(FAVICON_SVG)
        icons = f'<link rel="icon" href="{fav}" type="image/svg+xml">'
        styles = "<style>" + minify_css(css) + "</style>"
        if meta.get("katex"):
            styles += "<style>" + katex_css_inline() + "</style>"
        script = "<script>" + js + "</script>" + "".join("<script>" + script_source(n) + "</script>" for n in meta.get("scripts", []))
        if meta.get("katex"):
            script = "<script>" + (KATEX / "katex.min.js").read_text() + "</script>" + script
        if meta.get("test") or meta.get("calculator"):
            script = "<script>window.TOPLINE_SRC_B64 = '" + base64.b64encode(calculator_html().encode()).decode() + "';</script>" + script
        canonical = ""
        # The preview is a set of files with no server, so "./" (the home page) must name the file.
        body = re.sub(r'href="\./(#[^"]*)?"', lambda m: 'href="index.html' + (m.group(1) or "") + '"', body)
        svg = (SRC / "assets/hint-ladder.svg").read_text().strip()
        body = body.replace('src="assets/hint-ladder.svg"', 'src="data:image/svg+xml;base64,' + base64.b64encode(svg.encode()).decode() + '"')

    # Every page gets the paper look: the class is on the <html> tag, so it's there before anything is drawn. On
    # signed-in pages theme.js takes it off again when the account has picked another theme in Settings.
    # The preview's home page has no <html> tag of its own (the artifact wraps it), so it adds the class with a script.
    paper_tag = '<script>document.documentElement.classList.add("paper")</script>\n' if is_home and mode == "artifact" else ""
    head = f"""<title>{meta['title']}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{meta['description']}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#f4f1e9">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Graphite SAT">
<meta property="og:title" content="{meta['title']}">
<meta property="og:description" content="{meta['description']}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og-image.png">
<meta property="og:image:alt" content="Graphite SAT: a yellow pencil end beside the line SAT prep that starts with the questions you miss.">
<meta name="twitter:card" content="summary_large_image">
{canonical}
{icons}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{PAPER_FONTS}">
{paper_tag}{styles}"""
    if is_home:
        head += '\n<script type="application/ld+json">' + json.dumps(JSONLD) + "</script>"
    head = "\n".join(l for l in head.split("\n") if l.strip())

    if mode == "artifact" and is_home:
        return head + "\n" + body + script + "\n"
    if mode == "dist":
        head = head.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
    live_meta = '<meta name="graphite-mode" content="live">\n' if mode == "dist" else ""
    # Signed-in pages pick their theme and accent color before anything is drawn (theme.js, not deferred).
    signed_in = any(meta.get(k) for k in ("app", "parent", "test", "settings"))
    theme_tag = ""
    if signed_in:
        theme_tag = ('<script src="/js/theme.js"></script>\n' if mode == "dist"
                     else "<script>" + (SRC / "theme.js").read_text() + "</script>\n")
    classes = ("live paper" if mode == "dist" else "paper") + (" app" if signed_in else "")
    return ('<!doctype html>\n<html lang="en" class="' + classes + '">\n<head>\n<meta charset="utf-8">\n' + live_meta +
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + theme_tag + head + "\n" + (script if mode == "dist" else "") + "\n</head>\n<body>\n" + body
            + (script if mode == "artifact" else "") + "\n</body>\n</html>\n")

def make_images(out):
    out.mkdir(parents=True, exist_ok=True)
    (out / "favicon.svg").write_text(FAVICON_SVG)
    bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    reg = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

    def mark(size, tile=False):
        """The pencil-end logo. tile=True puts it on a dark square (for app icons, which can't be transparent)."""
        s = size * 4
        im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        pad = 0
        if tile:
            d.rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * 0.22), fill="#1c1e21")
            pad = s * 0.16
        u = (s - 2 * pad) / 64

        def P(x, y):
            return (pad + x * u, pad + y * u)
        hexa = [P(32, 3), P(57, 17.5), P(57, 46.5), P(32, 61), P(7, 46.5), P(7, 17.5)]
        d.polygon(hexa, fill="#f2c14e")
        for tri in ([P(32, 32), P(57, 17.5), P(57, 46.5)], [P(32, 32), P(32, 61), P(7, 46.5)], [P(32, 32), P(7, 17.5), P(32, 3)]):
            d.polygon(tri, fill="#d5aa45")
        c = P(32, 32)
        d.ellipse([c[0] - 16 * u, c[1] - 16 * u, c[0] + 16 * u, c[1] + 16 * u], fill="#e9c79a")
        r = 8 * u
        d.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], fill="#2d3136")
        return im.resize((size, size), Image.LANCZOS)

    mark(32).save(out / "favicon-32.png", optimize=True)
    for name, size in [("apple-touch-icon.png", 180), ("icon-512.png", 512)]:
        mark(size, tile=True).convert("RGB").quantize(colors=64, method=Image.FASTOCTREE).save(out / name, optimize=True)

    og = Image.new("RGB", (1200, 630), "#1c1e21")
    d = ImageDraw.Draw(og)
    og.paste(mark(120), (80, 80), mark(120))
    d.text((80, 260), "SAT prep that starts with", font=ImageFont.truetype(bold, 64), fill="#eceef0")
    d.text((80, 340), "the questions you miss.", font=ImageFont.truetype(bold, 64), fill="#f2c14e")
    d.text((80, 470), "Graphite SAT  ·  tutoring for high school students", font=ImageFont.truetype(reg, 30), fill="#b1b6bd")
    og.quantize(colors=32, method=Image.FASTOCTREE).save(out / "og-image.png", optimize=True)

ASSET_LINK = re.compile(r'((?:src|href)="/)((?:js|css)/[\w.-]+\.(?:js|css))"')


def versioned(html):
    """Tags each script and stylesheet link with a hash of the file (/js/site.js?v=1a2b3c4d5e).
    When a file changes, its link changes, so browsers fetch the new version instead of a saved old one."""
    def tag(m):
        f = DIST / m.group(2)
        if not f.is_file():
            return m.group(0)
        return f'{m.group(1)}{m.group(2)}?v={hashlib.sha256(f.read_bytes()).hexdigest()[:10]}"'
    return ASSET_LINK.sub(tag, html)


def build():
    pages = load_pages()
    for d in (DIST, ART):
        shutil.rmtree(d, ignore_errors=True); d.mkdir()

    # Deployable site
    (DIST / "css").mkdir(); (DIST / "js").mkdir(); (DIST / "assets").mkdir()
    (DIST / "css/site.css").write_text(minify_css(css))
    (DIST / "js/site.js").write_text(js)
    shutil.copy(SRC / "assets/hint-ladder.svg", DIST / "assets/hint-ladder.svg")
    shutil.copy(SRC / "practice-test.js", DIST / "js" / "practice-test.js")
    shutil.copy(SRC / "practice.js", DIST / "js" / "practice.js")
    shutil.copy(SRC / "plan.js", DIST / "js" / "plan.js")
    shutil.copy(SRC / "levels.js", DIST / "js" / "levels.js")
    shutil.copy(SRC / "parent.js", DIST / "js" / "parent.js")
    for n in ("effects.js", "theme.js", "settings.js", "checkout.js", "game-ui.js", "rewards.js", "speed.js", "focus.js",
              "lessons.js", "lesson-kit.js", "dash-play.js", "dash-layout.js", "market.js", "qtools.js", "tutor.js", "pets.js", "integrity.js", "subscription.js"):
        shutil.copy(SRC / n, DIST / "js" / n)
    (DIST / "calculator.html").write_text(calculator_html())
    if (DIST / "vendor" / "katex").exists():
        shutil.rmtree(DIST / "vendor" / "katex")
    shutil.copytree(KATEX, DIST / "vendor" / "katex")
    make_images(DIST)
    for p in pages:
        (DIST / p["file"]).write_text(versioned(render(p, "dist")))

    urls = [p for p in pages if not p.get("robots", "").startswith("noindex")]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in urls:
        pr = "1.0" if p["path"] == "/" else ("0.6" if p.get("signin") else "0.3")
        sm.append(f"  <url><loc>{SITE}{p['path']}</loc><lastmod>2026-10-15</lastmod><priority>{pr}</priority></url>")
    sm.append("</urlset>")
    (DIST / "sitemap.xml").write_text("\n".join(sm) + "\n")
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /dashboard.html\nDisallow: /practice-test.html\nDisallow: /practice.html\nDisallow: /plan.html\nDisallow: /levels.html\nDisallow: /parent.html\nDisallow: /settings.html\nDisallow: /checkout.html\nDisallow: /speed.html\nDisallow: /focus.html\nDisallow: /lessons.html\nDisallow: /rewards.html\nDisallow: /market.html\nDisallow: /tutor.html\nDisallow: /calculator.html\n\nSitemap: {SITE}/sitemap.xml\n")
    (DIST / "site.webmanifest").write_text(json.dumps({
        "name": "Graphite SAT", "short_name": "Graphite SAT", "start_url": "/",
        "display": "standalone", "background_color": "#1c1e21", "theme_color": "#1c1e21",
        "icons": [{"src": "/apple-touch-icon.png", "sizes": "180x180", "type": "image/png"},
                  {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=2) + "\n")
    shutil.copy(SRC / "htaccess", DIST / ".htaccess")
    shutil.copy(SRC / "netlify.toml", DIST / "netlify.toml")

    # Artifact preview
    for p in pages:
        (ART / p["file"]).write_text(render(p, "artifact"))
    print("built", len(pages), "pages")

if __name__ == "__main__":
    build()
