"""Build Graphite into two outputs:
site/      deployable site (linked CSS/JS, root-absolute links, server files)
artifact/  self-contained pages for the hosted preview (inlined CSS/JS/images)
"""
import base64, json, re, shutil, urllib.parse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
SRC = ROOT / "src"
DIST = ROOT / "site"
ART = ROOT / "artifact"
SITE = "https://www.graphiteprep.com"
FONTS = ("https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,500..800"
         "&family=Atkinson+Hyperlegible+Next:wght@400;700&family=IBM+Plex+Mono:wght@500&display=swap")
FAVICON_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="#2d3136"/>'
               '<ellipse cx="16" cy="16" rx="10" ry="7" fill="#f2c14e"/></svg>')

header = (SRC / "partials/header.html").read_text()
footer = (SRC / "partials/footer.html").read_text()
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

def render(meta, mode):
    is_home = meta["file"] == "index.html"
    h = "" if is_home else "./"
    head_nav = header.replace("{{H}}", h).replace("{{SIGNIN_CURRENT}}", ' aria-current="page"' if meta.get("signin") else "")
    foot = footer.replace("{{H}}", h)
    body = head_nav + meta["body"] + foot
    url = SITE + meta["path"]
    robots = meta.get("robots", "index, follow")

    if mode == "dist":
        icons = ('<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
                 '<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">\n'
                 '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n'
                 '<link rel="manifest" href="/site.webmanifest">')
        styles = '<link rel="stylesheet" href="/css/site.css">'
        script = '<script src="/js/site.js" defer></script>'
        canonical = f'<link rel="canonical" href="{url}">' if robots.startswith("index") else ""
        # Root-absolute internal links so pages work from any URL, including the 404 page
        body = re.sub(r'href="\./', 'href="/', body)
        body = re.sub(r'href="([a-z0-9-]+\.html)', r'href="/\1', body)
        body = body.replace('src="assets/', 'src="/assets/')
    else:
        fav = "data:image/svg+xml," + urllib.parse.quote(FAVICON_SVG)
        icons = f'<link rel="icon" href="{fav}" type="image/svg+xml">'
        styles = "<style>" + minify_css(css) + "</style>"
        script = "<script>" + js + "</script>"
        canonical = ""
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
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
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

def build():
    pages = load_pages()
    for d in (DIST, ART):
        shutil.rmtree(d, ignore_errors=True); d.mkdir()

    # Deployable site
    (DIST / "css").mkdir(); (DIST / "js").mkdir(); (DIST / "assets").mkdir()
    (DIST / "css/site.css").write_text(minify_css(css))
    (DIST / "js/site.js").write_text(js)
    shutil.copy(SRC / "assets/hint-ladder.svg", DIST / "assets/hint-ladder.svg")
    make_images(DIST)
    for p in pages:
        (DIST / p["file"]).write_text(render(p, "dist"))

    urls = [p for p in pages if not p.get("robots", "").startswith("noindex")]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in urls:
        pr = "1.0" if p["path"] == "/" else ("0.6" if p.get("signin") else "0.3")
        sm.append(f"  <url><loc>{SITE}{p['path']}</loc><lastmod>2026-10-15</lastmod><priority>{pr}</priority></url>")
    sm.append("</urlset>")
    (DIST / "sitemap.xml").write_text("\n".join(sm) + "\n")
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /dashboard/\n\nSitemap: {SITE}/sitemap.xml\n")
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
