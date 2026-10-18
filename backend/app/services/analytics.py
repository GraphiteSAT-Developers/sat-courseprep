"""First-party analytics: how people use the site, kept on our own server.

What's saved, and only after the visitor accepts analytics cookies (the gs_consent cookie says
"analytics"): page views with the page and the site they came from, campaign tags (utm_source,
utm_medium, utm_campaign), the kind of device, browser and operating system, screen and window size,
language and time zone, how long each page stayed open and how far down it was scrolled, and clicks on
the site's main buttons. A random visitor id (the gs_vid cookie, 13 months) ties a visitor's pages together;
when they're signed in, the rows are tied to their account, show up in their data export, and are deleted
with it. Rows older than ANALYTICS_DAYS are deleted.

What's never saved: what people do on other websites, precise location, IP addresses, fingerprints, or
anything sold or shared for advertising. The site is used by teenagers, and student-privacy laws limit
what an education site may collect from them and what it may do with it.

consent_log keeps every cookie choice (accept, essential only, or a change later), even without analytics,
as the record that consent was asked and given.
"""
import re
import secrets
from datetime import datetime, timedelta, timezone

from flask import current_app, request

from ..db import execute, now_iso, query, today

KINDS = {"pageview", "engage", "click"}
VISITOR = re.compile(r"^[A-Za-z0-9_-]{16,64}$")
MAX_BATCH = 20


def _text(v, n=200):
    if v is None:
        return None
    v = str(v).strip()
    return v[:n] or None


def _int(v, lo, hi):
    try:
        v = int(v)
    except (TypeError, ValueError):
        return None
    return max(lo, min(hi, v))


def consented():
    return request.cookies.get("gs_consent") == "analytics"


def visitor_id():
    v = request.cookies.get("gs_vid") or ""
    return v if VISITOR.match(v) else None


def parse_agent(ua):
    """(device, browser, os) from a user agent string, in plain words."""
    ua = ua or ""
    device = "tablet" if re.search(r"iPad|Tablet|Nexus 7|SM-T", ua) else "phone" if re.search(r"Mobi|iPhone|Android", ua) else "computer"
    if re.search(r"bot|crawl|spider|HeadlessChrome", ua, re.I):
        device = "bot"
    browser = ("Edge" if "Edg/" in ua else "Opera" if "OPR/" in ua else "Samsung Internet" if "SamsungBrowser" in ua
               else "Chrome" if "Chrome/" in ua or "CriOS" in ua else "Firefox" if "Firefox/" in ua or "FxiOS" in ua
               else "Safari" if "Safari/" in ua else "Other")
    system = ("iOS" if re.search(r"iPhone|iPad|iPod", ua) else "Android" if "Android" in ua else "ChromeOS" if "CrOS" in ua
              else "Windows" if "Windows" in ua else "macOS" if "Mac OS X" in ua else "Linux" if "Linux" in ua else "Other")
    return device, browser, system


def _path(v):
    v = _text(v, 300)
    if not v:
        return None
    # Keep the page, drop anything after ? except campaign tags, which are saved in their own columns.
    return v.split("?")[0].split("#")[0]


def _referrer(v):
    v = _text(v, 300)
    if not v:
        return None
    m = re.match(r"^https?://([^/?#]+)", v)
    host = m.group(1).lower() if m else None
    base = current_app.config.get("BASE_URL", "")
    if host and base and host in base:
        return None  # our own pages
    return host


def collect(events, user_id=None):
    """Saves a batch of events from the page. Returns how many were saved."""
    if not current_app.config.get("ANALYTICS", True) or not consented():
        return 0
    vid = visitor_id()
    if not vid:
        return 0
    device, browser, system = parse_agent(request.headers.get("User-Agent"))
    if device == "bot":
        return 0
    saved, stamp, day = 0, now_iso(), today()
    for e in (events or [])[:MAX_BATCH]:
        if not isinstance(e, dict) or e.get("kind") not in KINDS:
            continue
        execute(
            "INSERT INTO analytics_events (visitor_id, session_id, user_id, kind, path, title, referrer, utm_source, utm_medium, "
            "utm_campaign, device, browser, os, screen, viewport, lang, tz, label, duration_ms, scroll_pct, day, at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (vid, _text(e.get("session"), 64), user_id, e["kind"], _path(e.get("path")), _text(e.get("title"), 120),
             _referrer(e.get("referrer")), _text(e.get("utm_source"), 80), _text(e.get("utm_medium"), 80),
             _text(e.get("utm_campaign"), 80), device, browser, system, _text(e.get("screen"), 20), _text(e.get("viewport"), 20),
             _text(e.get("lang"), 20), _text(e.get("tz"), 60), _text(e.get("label"), 80),
             _int(e.get("duration_ms"), 0, 6 * 3600 * 1000), _int(e.get("scroll_pct"), 0, 100), day, stamp))
        saved += 1
    return saved


def log_consent(analytics, version, gpc, path, user_id=None):
    vid = visitor_id() or secrets.token_urlsafe(16)
    execute("INSERT INTO consent_log (visitor_id, user_id, analytics, version, gpc, path, user_agent, at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (vid, user_id, 1 if analytics else 0, version, 1 if gpc else 0, _path(path), _text(request.headers.get("User-Agent"), 300), now_iso()))
    if not analytics:
        # Turning analytics off deletes what this browser sent before it was signed in to an account.
        execute("DELETE FROM analytics_events WHERE visitor_id = ? AND user_id IS NULL", (vid,))
    return vid


def prune():
    days = int(current_app.config.get("ANALYTICS_DAYS", 395))
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    execute("DELETE FROM analytics_events WHERE at < ?", (cutoff,))


def report(days=30):
    """A quick summary for the site owner: python -m flask --app wsgi analytics-report"""
    since = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    one = lambda sql: query(sql, (since,))  # noqa: E731
    return {
        "visitors": query("SELECT COUNT(DISTINCT visitor_id) AS n FROM analytics_events WHERE at >= ?", (since,), one=True)["n"],
        "pageviews": query("SELECT COUNT(*) AS n FROM analytics_events WHERE kind = 'pageview' AND at >= ?", (since,), one=True)["n"],
        "pages": [dict(r) for r in one("SELECT path, COUNT(*) AS views FROM analytics_events WHERE kind = 'pageview' AND at >= ? "
                                       "GROUP BY path ORDER BY views DESC LIMIT 15")],
        "referrers": [dict(r) for r in one("SELECT referrer, COUNT(*) AS n FROM analytics_events WHERE kind = 'pageview' AND referrer IS NOT NULL "
                                           "AND at >= ? GROUP BY referrer ORDER BY n DESC LIMIT 10")],
        "devices": [dict(r) for r in one("SELECT device, COUNT(DISTINCT visitor_id) AS n FROM analytics_events WHERE at >= ? GROUP BY device")],
        "clicks": [dict(r) for r in one("SELECT label, COUNT(*) AS n FROM analytics_events WHERE kind = 'click' AND at >= ? "
                                        "GROUP BY label ORDER BY n DESC LIMIT 15")],
        "consent": [dict(r) for r in one("SELECT analytics, COUNT(*) AS n FROM consent_log WHERE at >= ? GROUP BY analytics")],
    }
