"""Reading and Writing strategy lessons from content/lessons/rw.json, rendered as HTML.

One lesson per skill in content/bank/rw-skills.json, plus an overview of the section. Lesson text
is our own trusted HTML (like the diagnostic's stems), so passages and steps go in as written;
titles and labels are escaped.

No database access here, so website/build.py renders the Lessons page from it at build time.
"""
import html
import json
from functools import lru_cache
from pathlib import Path

CONTENT = Path(__file__).resolve().parent.parent / "content"
LESSONS_FILE = CONTENT / "lessons" / "rw.json"
SKILLS_FILE = CONTENT / "bank" / "rw-skills.json"
LETTERS = "ABCD"


@lru_cache(maxsize=None)
def skills():
    return json.loads(SKILLS_FILE.read_text())


@lru_cache(maxsize=None)
def lessons():
    """Lessons in course order: the overview, then the skills in test order."""
    listed = json.loads(LESSONS_FILE.read_text())["lessons"]
    meta = skills()
    known = {(s["domain"], s["name"]) for s in meta["skills"]}
    for lesson in listed:
        if lesson["domain"] is not None and (lesson["domain"], lesson["skill"]) not in known:
            raise ValueError(f"lesson {lesson['id']}: unknown skill {lesson['domain']} / {lesson['skill']}")
        for q in [lesson.get("example")] + lesson.get("tryIt", []):
            if q and not (len(q["choices"]) == 4 and 0 <= q["answer"] < 4):
                raise ValueError(f"lesson {lesson['id']}: each question needs 4 choices and an answer index")
    order = {key: i for i, key in enumerate(meta["format"]["domainOrder"])}
    skill_order = {s["name"]: i for i, s in enumerate(meta["skills"])}
    return sorted(listed, key=lambda l: (-1, 0) if l["domain"] is None else (order[l["domain"]], skill_order[l["skill"]]))


def domain_name(key):
    return skills()["domains"][key] if key else "Start here"


# ---------- HTML ----------

def _question(q, label, worked):
    """A passage, its question and four choices. Worked examples show the answer and why each choice is right or
    wrong; quick checks are buttons that lessons.js grades in the browser."""
    out = [f'<div class="qcard ls-q"><div class="qcard-top"><span class="label">{label}</span></div>',
           f'<div class="qcard-body"><div class="ls-passage">{q["passage"]}</div>',
           f'<p class="ls-ask"><strong>{q["question"]}</strong></p>']
    if worked:
        out.append('<ol class="ls-worked">')
        for i, (choice, why) in enumerate(zip(q["choices"], q["why"])):
            right = i == q["answer"]
            mark = '<span class="ls-tag ls-tag-ok">Answer</span>' if right else ""
            out.append(f'<li class="{"is-right" if right else ""}"><span class="bubble" aria-hidden="true">{LETTERS[i]}</span>'
                       f'<div><p class="ls-choice"><span class="visually-hidden">{LETTERS[i]}. </span>{choice} {mark}</p>'
                       f'<p class="ls-why">{why}</p></div></li>')
        out.append("</ol>")
        if q.get("think"):
            out.append(f'<div class="xp-desmos ls-think"><h4 class="ls-mini">How to think about it</h4><p>{q["think"]}</p></div>')
    else:
        out.append(f'<div class="choices ls-check" role="group" aria-label="Answer choices" data-answer="{q["answer"]}">')
        for i, choice in enumerate(q["choices"]):
            out.append(f'<button type="button" class="choice" data-choice="{i}"><span class="bubble" aria-hidden="true">{LETTERS[i]}</span>'
                       f'<span class="choice-text"><span class="visually-hidden">{LETTERS[i]}. </span>{choice}</span></button>')
        out.append("</div>")
        out.append(f'<div class="ls-feedback" aria-live="polite"><p class="ls-verdict"></p>'
                   f'<details class="ls-explain"><summary>Show the explanation</summary>'
                   f'<p><strong>Answer: {LETTERS[q["answer"]]}.</strong> {q["explain"]}</p></details></div>')
    out.append("</div></div>")
    return "".join(out)


def _reference(ref):
    head = "".join(f"<th scope=\"col\">{html.escape(h)}</th>" for h in ref["head"])
    rows = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in ref["rows"])
    note = f'<p class="fine">{ref["note"]}</p>' if ref.get("note") else ""
    return (f'<section class="ls-sec"><h3>{html.escape(ref["title"])}</h3>'
            f'<div class="ls-table-wrap"><table class="ls-table"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>{note}</section>')


def lesson_html(lesson, prev=None, nxt=None):
    lid = lesson["id"]
    out = [f'<article class="panel ls-lesson" id="{lid}" data-lesson aria-labelledby="{lid}-title">',
           f'<header class="ls-head"><p class="label">{html.escape(domain_name(lesson["domain"]))} · {lesson["minutes"]} min</p>',
           f'<h2 id="{lid}-title">{html.escape(lesson["title"])}</h2></header>',
           '<div class="ls-intro prose">' + "".join(f"<p>{p}</p>" for p in lesson["intro"]) + "</div>"]
    if lesson.get("spot"):
        out.append('<section class="ls-sec"><h3>How to spot it</h3><p class="fine">The question will read like this:</p><ul class="ls-spot">'
                   + "".join(f"<li>{s}</li>" for s in lesson["spot"]) + "</ul></section>")
    out.append('<section class="ls-sec"><h3>How to do it</h3><ol class="xp-steps ls-steps">'
               + "".join(f"<li>{s}</li>" for s in lesson["steps"]) + "</ol></section>")
    out.append('<section class="ls-sec"><h3>Traps to avoid</h3><dl class="ls-traps">'
               + "".join(f"<div><dt>{t['name']}</dt><dd>{t['text']}</dd></div>" for t in lesson["traps"]) + "</dl></section>")
    if lesson.get("reference"):
        out.append(_reference(lesson["reference"]))
    if lesson.get("example"):
        out.append('<section class="ls-sec"><h3>Worked example</h3>' + _question(lesson["example"], "Example", True) + "</section>")
    if lesson.get("tryIt"):
        n = len(lesson["tryIt"])
        out.append('<section class="ls-sec"><h3>Try it</h3>'
                   + "".join(_question(q, f"Quick check {i + 1} of {n}", False) for i, q in enumerate(lesson["tryIt"])) + "</section>")
    links = []
    if prev:
        links.append(f'<a class="btn btn-secondary" href="#{prev["id"]}" rel="prev">← {html.escape(prev["title"])}</a>')
    links.append('<a class="btn btn-quiet" href="#lessons">All lessons</a>')
    if nxt:
        links.append(f'<a class="btn btn-primary" href="#{nxt["id"]}" rel="next">Next: {html.escape(nxt["title"])} →</a>')
    out.append('<nav class="ls-pager" aria-label="More lessons">' + "".join(links) + "</nav></article>")
    return "".join(out)


def index_html():
    """The lesson list, grouped by domain in test order."""
    groups = {}
    for lesson in lessons():
        groups.setdefault(lesson["domain"], []).append(lesson)
    out = ['<div class="ls-index">']
    for key, items in groups.items():
        out.append(f'<section class="ls-group"><h2 class="ls-group-title">{html.escape(domain_name(key))}</h2><ol class="ls-cards">')
        for lesson in items:
            out.append(f'<li><a class="ls-card" href="#{lesson["id"]}"><span class="ls-card-title">{html.escape(lesson["title"])}</span>'
                       f'<span class="ls-card-sum">{html.escape(lesson["summary"])}</span>'
                       f'<span class="label">{lesson["minutes"]} min</span></a></li>')
        out.append("</ol></section>")
    out.append("</div>")
    return "".join(out)


def page_html():
    """Everything the Lessons page shows: the index, then every lesson."""
    items = lessons()
    body = [index_html(), '<div class="ls-lessons">']
    for i, lesson in enumerate(items):
        body.append(lesson_html(lesson, items[i - 1] if i else None, items[i + 1] if i + 1 < len(items) else None))
    body.append("</div>")
    return "".join(body)
