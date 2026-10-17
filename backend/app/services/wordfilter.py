"""Keeps curse words out of every text box: names, emails, the home page form and anything added later.

The list is content/blocked_words.txt (ROT13-encoded; the file explains how each entry matches). Text is
lowercased, accents and look-alike characters are undone (sh1t, $hit, @ss), stretched letters are squeezed
(fuuuck), spaced-out letters are joined (f u c k), and * stands in for any vowel (f*ck). Matching is by
word, so innocent words that merely contain a short bad word (class, Dickens, Scunthorpe) are fine.

website/src/wordfilter.js does the same in the browser so students see the problem as they type; the server
check here is the one that counts.
"""
import codecs
import re
import unicodedata
from functools import lru_cache
from pathlib import Path

LIST = Path(__file__).resolve().parent.parent / "content" / "blocked_words.txt"
LEET = str.maketrans({"0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "7": "t", "@": "a", "$": "s", "!": "i", "|": "i"})
ENDINGS = ("ings", "ing", "ers", "er", "ed", "es", "s", "y", "ier", "iest", "in")
MESSAGE = "Please keep it clean. That has a word we don't allow."


@lru_cache(maxsize=1)
def entries():
    """[(mode, word)] where mode is 'any', 'edge' or 'word'."""
    out = []
    for line in LIST.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        mode = {"*": "any", "~": "edge"}.get(line[0], "word")
        word = codecs.decode(line.lstrip("*~"), "rot13").lower()
        out.append((mode, word))
    return out


def raw_list():
    """The list as stored (still ROT13), for the browser check."""
    return [l.strip() for l in LIST.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]


@lru_cache(maxsize=None)
def _pattern(word):
    return "".join(f"[{c}*]" if c in "aeiou" else re.escape(c) for c in word)  # * can hide a vowel


def _squeeze(token, at_least):
    """Runs of `at_least` or more of the same letter cut down to one (fuuuuck to fuck)."""
    return re.sub(r"(.)\1{%d,}" % (at_least - 1), r"\1", token)


def tokens(text):
    text = unicodedata.normalize("NFKD", str(text or "")).encode("ascii", "ignore").decode().lower().translate(LEET)
    parts = re.findall(r"[a-z*]+", text)
    out, run = [], []
    for p in parts + [""]:
        if len(p) == 1:  # f u c k, f.u.c.k
            run.append(p)
            continue
        if len(run) > 1:
            out.append("".join(run))
        out.extend(run if len(run) == 1 else [])
        run = []
        if p:
            out.append(p)
    return out


def _stems(token):
    yield token
    for e in ENDINGS:
        if token.endswith(e) and len(token) - len(e) >= 2:
            yield token[: -len(e)]


def _hit(token):
    stretched = _squeeze(token, 3)  # shiiiit, but not shiitake
    for mode, word in entries():
        pat = _pattern(word)
        if mode == "any":
            if any(re.search(pat, t) for t in (token, stretched, _squeeze(token, 2))):
                return True
            continue
        for t in (token, stretched):
            for s in _stems(t):
                if mode == "word" and re.fullmatch(pat, s):
                    return True
                if mode == "edge" and (re.match(pat, s) or re.search(pat + "$", s)):
                    return True
    return False


def is_clean(text):
    return not any(_hit(t) for t in tokens(text))
