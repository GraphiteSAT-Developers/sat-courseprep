"""Build Graphite into two outputs:
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
FAVICON_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="#2d3136"/>'
               '<ellipse cx="16" cy="16" rx="10" ry="7" fill="#f2c14e"/></svg>')

header = (SRC / "partials/header.html").read_text()
footer = (SRC / "partials/footer.html").read_text()
app_header = (SRC / "partials/app-header.html").read_text()
parent_header = (SRC / "partials/parent-header.html").read_text()
app_footer = (SRC / "partials/app-footer.html").read_text()
banner = (SRC / "partials/cookie-banner.html").read_text()
TOPLINE = ROOT.parent / "topline" / "index.html"

def calculator_html():
    """Topline, adapted for the test: blank on first open, its own saved state, not indexed."""
    t = TOPLINE.read_text()
    swaps = [
        ("const STORE = 'plotline-state-v1';", "const STORE = (window.TOPLINE_EMBED && window.TOPLINE_EMBED.store) || 'plotline-state-v1';"),
        ("if (!load()) rows = exampleRows();", "if (!load()) rows = window.TOPLINE_EMBED ? (colorCounter = 0, [newRow('')]) : exampleRows();"),
        ("<head>\n", "<head>\n<meta name=\"robots\" content=\"noindex\">\n<meta name=\"description\" content=\"Graphite graphing calculator for SAT Math practice.\">\n<script>window.TOPLINE_EMBED = { store: 'graphite-test-calc-v1' };</script>\n"),
    ]
    for old, new in swaps:
        assert t.count(old) == 1, "Topline changed; update calculator_html(): " + old[:40]
        t = t.replace(old, new)
    return t
css = (SRC / "site.css").read_text()
js = (SRC / "site.js").read_text()

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
    "name": "Graphite", "url": SITE + "/", "logo": SITE + "/apple-touch-icon.png",
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
PREVIEW_ONLY = {"questions.js", "bank.js", "practice-local.js"}


def bank_js():
    """The question bank for the offline preview, built by the backend's own bank module (same HTML, same keys)."""
    # Load the backend's services as a package of their own, without the Flask app around them.
    if "graphite_services" not in sys.modules:
        pkg = types.ModuleType("graphite_services")
        pkg.__path__ = [str(SERVICES)]
        sys.modules["graphite_services"] = pkg
    bank = importlib.import_module("graphite_services.bank")
    diagnostic = importlib.import_module("graphite_services.diagnostic")
    studyplan = importlib.import_module("graphite_services.studyplan")
    levels = importlib.import_module("graphite_services.levels")
    plans = importlib.import_module("graphite_services.plans")
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
        "parent": {"plans": [{"key": k, "name": p["name"], "blurb": p["blurb"], "month_cents": p["month"], "year_cents": p["year"]}
                             for k, p in plans.PLANS.items()],
                   "alert_days": list(plans.ALERT_DAYS), "pause_days": plans.PAUSE_DAYS},
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


def render(meta, mode):
    is_home = meta["file"] == "index.html"
    h = "" if is_home else "./"
    if meta.get("test"):
        head_nav, foot = "", ""
    elif meta.get("parent"):
        head_nav, foot = parent_header, app_footer
    elif meta.get("app"):
        head_nav, foot = app_header, app_footer
    else:
        head_nav = header.replace("{{H}}", h).replace("{{SIGNIN_CURRENT}}", ' aria-current="page"' if meta.get("signin") else "")
        foot = footer.replace("{{H}}", h)
    body = head_nav + meta["body"].replace("{{SCORE_CHART}}", score_chart()) + foot + ("" if meta.get("test") else banner)
    url = SITE + meta["path"]
    robots = meta.get("robots", "index, follow")

    if mode == "dist":
        icons = ('<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
                 '<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">\n'
                 '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n'
                 '<link rel="manifest" href="/site.webmanifest">')
        styles = '<link rel="stylesheet" href="/css/site.css">'
        # Served by the backend: site.js first (it sets up the API helper), and never the answer key.
        script = '<script src="/js/site.js" defer></script>' + "".join(
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
        script = "<script>" + js + "</script>" + "".join("<script>" + script_source(n) + "</script>" for n in meta.get("scripts", []))
        if meta.get("test") or meta.get("calculator"):
            script = "<script>window.TOPLINE_SRC_B64 = '" + base64.b64encode(calculator_html().encode()).decode() + "';</script>" + script
        canonical = ""
        # The preview is a set of files with no server, so "./" (the home page) must name the file.
        body = re.sub(r'href="\./(#[^"]*)?"', lambda m: 'href="index.html' + (m.group(1) or "") + '"', body)
        svg = (SRC / "assets/hint-ladder.svg").read_text().strip()
        body = body.replace('src="assets/hint-ladder.svg"', 'src="data:image/svg+xml;base64,' + base64.b64encode(svg.encode()).decode() + '"')

    head = f"""<title>{meta['title']}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{meta['description']}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#1c1e21">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Graphite">
<meta property="og:title" content="{meta['title']}">
<meta property="og:description" content="{meta['description']}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og-image.png">
<meta property="og:image:alt" content="Graphite: AI SAT tutoring. A yellow answer bubble on a graphite gray background.">
<meta name="twitter:card" content="summary_large_image">
{canonical}
{icons}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
{styles}"""
    if is_home:
        head += '\n<script type="application/ld+json">' + json.dumps(JSONLD) + "</script>"
    head = "\n".join(l for l in head.split("\n") if l.strip())

    if mode == "artifact" and is_home:
        return head + "\n" + body + script + "\n"
    if mode == "dist":
        head = head.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
    live_meta = '<meta name="graphite-mode" content="live">\n' if mode == "dist" else ""
    return ('<!doctype html>\n<html lang="en"' + (' class="live"' if mode == "dist" else "") + '>\n<head>\n<meta charset="utf-8">\n' + live_meta +
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + head + "\n" + (script if mode == "dist" else "") + "\n</head>\n<body>\n" + body
            + (script if mode == "artifact" else "") + "\n</body>\n</html>\n")

def make_images(out):
    out.mkdir(parents=True, exist_ok=True)
    (out / "favicon.svg").write_text(FAVICON_SVG)
    bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    reg = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

    def mark(size):
        s = size * 4
        im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * 7 / 32), fill="#2d3136")
        d.ellipse([s * 6 / 32, s * 9 / 32, s * 26 / 32, s * 23 / 32], fill="#f2c14e")
        return im.resize((size, size), Image.LANCZOS)

    for name, size in [("favicon-32.png", 32), ("apple-touch-icon.png", 180), ("icon-512.png", 512)]:
        mark(size).quantize(colors=64, method=Image.FASTOCTREE).save(out / name, optimize=True)

    og = Image.new("RGB", (1200, 630), "#1c1e21")
    d = ImageDraw.Draw(og)
    og.paste(mark(120), (80, 80), mark(120))
    d.text((80, 260), "SAT prep that starts with", font=ImageFont.truetype(bold, 64), fill="#eceef0")
    d.text((80, 340), "the questions you miss.", font=ImageFont.truetype(bold, 64), fill="#f2c14e")
    d.text((80, 470), "Graphite  ·  AI SAT tutoring for high school students", font=ImageFont.truetype(reg, 30), fill="#b1b6bd")
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
    (DIST / "calculator.html").write_text(calculator_html())
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
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /dashboard.html\nDisallow: /practice-test.html\nDisallow: /practice.html\nDisallow: /plan.html\nDisallow: /levels.html\nDisallow: /parent.html\nDisallow: /calculator.html\n\nSitemap: {SITE}/sitemap.xml\n")
    (DIST / "site.webmanifest").write_text(json.dumps({
        "name": "Graphite SAT Tutoring", "short_name": "Graphite", "start_url": "/",
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
