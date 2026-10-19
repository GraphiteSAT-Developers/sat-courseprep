"""Gzip for text responses (pages, CSS, JS, JSON), so a page downloads about a quarter of the bytes.

Uses only the standard library. Static files are compressed once per version and kept in memory.
"""
import gzip
from collections import OrderedDict

TYPES = ("text/html", "text/css", "text/plain", "text/javascript", "application/javascript", "application/json",
         "image/svg+xml", "application/manifest+json", "application/xml", "text/xml")
MIN_BYTES = 1024
_cache = OrderedDict()  # (path, etag) -> gzipped bytes, for static files
_CACHE_FILES = 64


def gzip_response(resp, request):
    if (resp.status_code != 200 or "Content-Encoding" in resp.headers or resp.mimetype not in TYPES
            or "gzip" not in request.headers.get("Accept-Encoding", "").lower() or request.method == "HEAD"):
        return resp
    resp.headers.add("Vary", "Accept-Encoding")
    etag = resp.headers.get("ETag")
    key = (request.path, etag) if etag else None
    data = _cache.get(key) if key else None
    if data is None:
        resp.direct_passthrough = False
        raw = resp.get_data()
        if len(raw) < MIN_BYTES:
            return resp
        data = gzip.compress(raw, compresslevel=6)
        if key:
            _cache[key] = data
            while len(_cache) > _CACHE_FILES:
                _cache.popitem(last=False)
    else:
        _cache.move_to_end(key)
    resp.direct_passthrough = False
    resp.set_data(data)
    resp.headers["Content-Encoding"] = "gzip"  # the ETag stays the file's, so If-None-Match still gets 304s
    return resp
