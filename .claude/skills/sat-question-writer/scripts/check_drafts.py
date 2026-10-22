#!/usr/bin/env python3
"""Checks a drafts file of new SAT questions before they go anywhere near the bank.

    python check_drafts.py question-drafts/batch.jsonl [--repo PATH] [--export OUT.jsonl] [--export-passing]

Every draft must pass: the bank's format rules (the same ones the backend tests use), the LaTeX rule,
a near-duplicate check against the bank and the rest of the batch, the blind-solver agreement, and for
Math the SymPy and Topline checks in its "check" block. --export writes the batch with "check" removed
and desmos.verified set where Topline produced the key; it refuses while anything fails, unless
--export-passing is given, which exports only the passing questions.
"""
import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
MATH_DOMAINS = {"algebra", "advanced-math", "psda", "geometry-trig"}
DIFFICULTIES = {"easy", "medium", "hard"}
ROUTES = {"desmos-primary", "hand-primary", "either"}
ID_PREFIX = {"algebra": "alg-", "advanced-math": "adv-", "psda": "psda-", "geometry-trig": "geo-"}
BLOCK_KINDS = {"intro", "p", "text1", "text2", "notes", "table", "graph"}
# Same rule as backend/tests/test_bank_tex.py: math outside $...$ means a formula never became LaTeX.
MATH = re.compile(r"(?<!\\)\$([^$]*)\$")
BARE_MATH = re.compile(r"\^|√|≤|≥|≠|π|\bsqrt\(|<=|>=|\\frac|\d ?[=+×÷] ?\d")


def shingles(*parts):
    """Same as backend/tests/test_no_repeats.py: every run of three words or numbers."""
    words = re.findall(r"[a-z]+|\d+(?:\.\d+)?|[=+\-^/<>]", " ".join(parts).lower())
    return {tuple(words[i:i + 3]) for i in range(max(1, len(words) - 2))}


def overlap(a, b):
    return len(a & b) / len(a | b) if a | b else 0


def find_repo(start):
    for p in [start, *start.parents]:
        if (p / "backend/app/content/bank/items.jsonl").exists():
            return p
    sys.exit("Can't find the repo (no backend/app/content/bank/items.jsonl above here). Pass --repo.")


def to_fraction(v):
    if isinstance(v, bool) or v is None:
        return None
    if isinstance(v, (int, float)):
        return Fraction(v).limit_denominator(10**9)
    if isinstance(v, str):
        try:
            return Fraction(v.strip())
        except (ValueError, ZeroDivisionError):
            return None
    if isinstance(v, dict) and "num" in v and "den" in v:
        return Fraction(v["num"], v["den"])
    return None


def close(a, b, tol=1e-6):
    return a is not None and b is not None and abs(float(a) - float(b)) <= tol * max(1, abs(float(b)))


def spr_fits(fr):
    """Can a student enter this in Bluebook (5 characters, 6 if negative)?"""
    room = 6 if fr < 0 else 5
    as_frac = f"{fr.numerator}/{fr.denominator}" if fr.denominator != 1 else str(fr.numerator)
    if len(as_frac) <= room:
        return True
    whole = str(abs(int(fr))) if abs(fr) >= 1 else ""
    return len(whole) + (1 if fr < 0 else 0) + (0 if fr.denominator == 1 else 2) <= room


def tex_problems(text):
    outside = MATH.sub(" ", re.sub(r"`[^`]*`", " ", text))
    m = BARE_MATH.search(outside)
    probs = [f"math outside $...$ near '{outside[max(0, m.start() - 15):m.end() + 15].strip()}'"] if m else []
    if text.replace("\\$", "").count("$") % 2:
        probs.append("unbalanced $")
    return probs


def words_in(passage):
    n = 0
    for b in passage:
        for t in b.get("paras", []) + b.get("items", []) + ([b["text"]] if "text" in b else []):
            n += len(re.sub(r"\[/?[ui]\]", "", t).split())
    return n


def run_sympy(code):
    prog = ("from sympy import *\nimport json\n" + code +
            "\n_g = globals()\n_out = {}\n"
            "if 'answer' in _g:\n    _a = nsimplify(_g['answer'])\n    _out['answer'] = str(_a) if _a.is_Rational else float(N(_a, 30))\n"
            "if 'answer_index' in _g:\n    _out['answer_index'] = int(_g['answer_index'])\n"
            "print(json.dumps(_out))\n")
    try:
        r = subprocess.run([sys.executable, "-c", prog], capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        return None, "SymPy check timed out"
    if r.returncode:
        err = (r.stderr.strip().splitlines() or ["unknown error"])[-1]
        if "No module named 'sympy'" in err:
            return None, "SymPy isn't installed: pip install sympy"
        return None, f"SymPy code failed: {err}"
    try:
        return json.loads(r.stdout.strip().splitlines()[-1]), None
    except (ValueError, IndexError):
        return None, "SymPy code printed nothing usable"


def run_topline(repo, jobs):
    if not jobs:
        return []
    html = repo / "topline/index.html"
    try:
        r = subprocess.run(["node", str(HERE / "topline_eval.mjs"), str(html)], input=json.dumps(jobs),
                           capture_output=True, text=True, timeout=120)
    except FileNotFoundError:
        return [{"error": "node isn't installed, so the Topline check can't run"}] * len(jobs)
    if r.returncode:
        return [{"error": "Topline engine failed: " + r.stderr.strip()[-300:]}] * len(jobs)
    return json.loads(r.stdout)


def katex_problems(repo, spans):
    """Formulas KaTeX can't render (the bank test test_every_formula_renders runs the same check). {span: error}"""
    katex = repo / "website/src/vendor/katex/katex.min.js"
    if not spans or not katex.exists():
        return {}
    js = ("const k = require(%s); const a = JSON.parse(require('fs').readFileSync(0, 'utf8')); const bad = {};"
          "for (const s of a) { try { k.renderToString(s, { throwOnError: true, strict: 'ignore' }); }"
          " catch (e) { bad[s] = e.message; } } process.stdout.write(JSON.stringify(bad));" % json.dumps(str(katex)))
    try:
        r = subprocess.run(["node", "-e", js], input=json.dumps(sorted(spans)), capture_output=True, text=True, timeout=120)
        return json.loads(r.stdout) if r.returncode == 0 else {}
    except (FileNotFoundError, ValueError):
        return {}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("drafts")
    ap.add_argument("--repo")
    ap.add_argument("--export")
    ap.add_argument("--export-passing", action="store_true")
    args = ap.parse_args()

    repo = Path(args.repo).resolve() if args.repo else find_repo(Path.cwd().resolve())
    bank_dir = repo / "backend/app/content/bank"
    bank = [json.loads(l) for l in (bank_dir / "items.jsonl").read_text().splitlines() if l.strip()]
    math_skills = {(s["domain"], s["name"]) for s in json.loads((bank_dir / "skills.json").read_text())["skills"]}
    rw_meta = json.loads((bank_dir / "rw_skills.json").read_text())
    rw_skills = {s["name"]: s for s in rw_meta["skills"]}
    techniques = {t["id"] for t in json.loads((bank_dir / "techniques.json").read_text())["techniques"]}

    lines = [l for l in Path(args.drafts).read_text().splitlines() if l.strip()]
    drafts, fails, warns = [], {}, {}
    for n, line in enumerate(lines, 1):
        try:
            drafts.append(json.loads(line))
        except ValueError as e:
            sys.exit(f"Line {n} isn't valid JSON: {e}")

    def fail(it, msg):
        fails.setdefault(it.get("id", "?"), []).append(msg)

    def warn(it, msg):
        warns.setdefault(it.get("id", "?"), []).append(msg)

    bank_ids = {q["id"] for q in bank}
    seen = Counter(d.get("id") for d in drafts)
    topline_jobs, topline_for = [], []

    for it in drafts:
        iid = it.get("id")
        rw = it.get("section") == "rw"
        chk = it.get("check") or {}
        if not iid:
            fail(it, "no id")
        elif iid in bank_ids:
            fail(it, "id already used in the bank")
        elif seen[iid] > 1:
            fail(it, "id used twice in this batch")
        for f in ("domain", "skill", "difficulty", "format", "stem", "byHand", "provenance", "status"):
            if not it.get(f):
                fail(it, f"missing {f}")
        if it.get("difficulty") not in DIFFICULTIES:
            fail(it, f"difficulty must be one of {sorted(DIFFICULTIES)}")
        if it.get("status") != "draft":
            fail(it, 'status must be "draft"')
        prov = it.get("provenance") or {}
        if not (prov.get("author") and prov.get("created")):
            fail(it, "provenance needs author and created")
        if "blind" not in chk:
            fail(it, "check.blind missing: have a separate agent answer the question without the key")

        texts = [it.get("stem", "")] + list(it.get("choices") or []) + [it.get("byHand", "")]

        if it.get("format") == "mc":
            ch = it.get("choices")
            if not (isinstance(ch, list) and len(ch) == 4 and all(isinstance(c, str) and c.strip() for c in ch)):
                fail(it, "mc needs exactly four non-empty choices")
            elif len({re.sub(r"\s+", " ", c.strip().lower()) for c in ch}) < 4:
                fail(it, "choices aren't all different")
            if it.get("answerIndex") not in range(4) or isinstance(it.get("answerIndex"), bool):
                fail(it, "answerIndex must be 0-3")
            if "Distractors:" not in it.get("byHand", ""):
                fail(it, "byHand needs a 'Distractors:' part explaining each wrong choice")
            if "blind" in chk and chk["blind"] != it.get("answerIndex"):
                fail(it, f"blind solver chose {chk['blind']!r}, key is {it.get('answerIndex')!r}: the question is wrong or ambiguous")

        if rw:
            sk = rw_skills.get(it.get("skill"))
            if not sk:
                fail(it, "skill isn't a name in rw_skills.json")
            else:
                if it.get("domain") != sk["domain"]:
                    fail(it, f"skill {sk['name']!r} belongs to domain {sk['domain']!r}")
                if iid and not re.fullmatch(rf"rw-{sk['code']}-\d{{3,}}", iid):
                    fail(it, f"id should look like rw-{sk['code']}-NNN")
            if it.get("format") != "mc":
                fail(it, 'Reading and Writing questions are "mc"')
            for f in ("tex", "desmos", "techniques", "route", "answers"):
                if f in it:
                    fail(it, f"Reading and Writing items don't have {f}")
            pas = it.get("passage")
            if not (isinstance(pas, list) and pas):
                fail(it, "passage must be a non-empty list of blocks")
                pas = []
            for b in pas:
                k = b.get("kind")
                if k not in BLOCK_KINDS:
                    fail(it, f"unknown passage block kind {k!r}")
                elif k in ("p", "text1", "text2") and not (isinstance(b.get("paras"), list) and b["paras"]):
                    fail(it, f"{k} block needs paras")
                elif k == "notes" and not (isinstance(b.get("items"), list) and len(b["items"]) >= 3):
                    fail(it, "notes block needs at least 3 items")
                elif k in ("table", "graph") and not (b.get("header") and b.get("rows") and all(len(r) == len(b["header"]) for r in b["rows"])):
                    fail(it, f"{k} needs a header and rows of the same width")
                elif k == "intro" and not b.get("text"):
                    fail(it, "intro block needs text")
            blob = json.dumps(it)
            for tag in ("u", "i"):
                if blob.count(f"[{tag}]") != blob.count(f"[/{tag}]"):
                    fail(it, f"unbalanced [{tag}] tags")
            if "completes the text" in it.get("stem", "") and "______" not in json.dumps(pas):
                fail(it, "a 'completes the text' question needs ______ in the passage")
            if it.get("skill") == "Cross-text connections" and not {b.get("kind") for b in pas} >= {"text1", "text2"}:
                fail(it, "cross-text questions need text1 and text2 blocks")
            nw = words_in(pas)
            if nw < 15 or nw > 170:
                warn(it, f"passage is {nw} words (SAT texts run about 25-150)")
        else:
            if it.get("domain") not in MATH_DOMAINS:
                fail(it, f"domain must be one of {sorted(MATH_DOMAINS)}")
            elif (it["domain"], it.get("skill")) not in math_skills:
                fail(it, "skill isn't a name in skills.json for this domain")
            elif iid and not iid.startswith(ID_PREFIX[it["domain"]]):
                fail(it, f"id should start with {ID_PREFIX[it['domain']]}")
            if it.get("tex") is not True:
                fail(it, "Math items need tex: true")
            if it.get("route") not in ROUTES:
                fail(it, f"route must be one of {sorted(ROUTES)}")
            bad = [t for t in it.get("techniques", []) if t not in techniques]
            if bad or not isinstance(it.get("techniques"), list):
                fail(it, f"techniques must be ids from techniques.json (bad: {bad})")
            ds = it.get("desmos")
            if ds is not None:
                if not (isinstance(ds.get("lines"), list) and ds["lines"] and isinstance(ds.get("read"), str) and ds["read"]):
                    fail(it, "desmos needs lines and read (or set desmos to null for hand-only items)")
                else:
                    texts.append(ds["read"])
            elif it.get("route") == "desmos-primary":
                fail(it, "a desmos-primary item needs desmos lines")

            key = None
            if it.get("format") == "spr":
                ans = it.get("answers")
                if not (isinstance(ans, list) and ans and all(isinstance(a, dict) and isinstance(a.get("num"), int) and isinstance(a.get("den"), int) and a["den"] > 0 for a in ans)):
                    fail(it, "spr needs answers: [{num, den}] with integer num and positive den")
                else:
                    keys = [Fraction(a["num"], a["den"]) for a in ans]
                    key = keys[0]
                    for k in keys:
                        if not spr_fits(k):
                            fail(it, f"answer {k} can't be entered in 5 characters (6 if negative)")
                    b = to_fraction(chk.get("blind"))
                    if "blind" in chk and not any(close(b, k) for k in keys):
                        fail(it, f"blind solver got {chk['blind']!r}, key is {', '.join(map(str, keys))}: the question is wrong or ambiguous")
            elif it.get("format") != "mc":
                fail(it, 'format must be "mc" or "spr"')
            if chk.get("value") is not None:
                v = to_fraction(chk["value"])
                if v is None:
                    fail(it, "check.value isn't a number or p/q")
                elif key is not None and not close(v, key):
                    fail(it, f"check.value {chk['value']} doesn't match the SPR key {key}")
                key = key if key is not None else v

            if not chk.get("sympy"):
                fail(it, "check.sympy missing: compute the answer independently")
            else:
                res, err = run_sympy(chk["sympy"])
                if err:
                    fail(it, err)
                else:
                    if it.get("format") == "mc" and "answer_index" in res and res["answer_index"] != it.get("answerIndex"):
                        fail(it, f"SymPy says choice {res['answer_index']}, key is {it.get('answerIndex')}")
                    if "answer" in res and key is not None and not close(to_fraction(res["answer"]) if isinstance(res["answer"], str) else res["answer"], key):
                        fail(it, f"SymPy got {res['answer']}, key is {key}")
                    if it.get("format") == "mc" and "answer_index" not in res and not ("answer" in res and key is not None):
                        fail(it, "SymPy code must set answer_index (testing each choice) or answer plus check.value")
                    if it.get("format") == "spr" and "answer" not in res:
                        fail(it, "SymPy code must set answer")

            tl = chk.get("topline") or {}
            tl_lines = tl.get("lines") or (ds or {}).get("lines")
            if tl_lines:
                topline_jobs.append({"lines": tl_lines, "degrees": bool(tl.get("degrees"))})
                topline_for.append((it, tl, key))

        for t in texts:
            for p in tex_problems(t) if not rw else []:
                fail(it, p)
        if not rw:
            it["_spans"] = {m.group(1) for t in texts for m in MATH.finditer(t)} | set((it.get("desmos") or {}).get("lines") or [])

    # Every formula and calculator line must render in KaTeX, or the bank's tests fail
    bad_tex = katex_problems(repo, set().union(*[d.get("_spans", set()) for d in drafts]))
    for it in drafts:
        for s in sorted(it.pop("_spans", set()) & set(bad_tex)):
            fail(it, f"KaTeX can't render ${s}$: {bad_tex[s][:120]}")

    # Topline: every line runs, and the expected line or regression parameter equals the key
    verified = set()
    for (it, tl, key), res in zip(topline_for, run_topline(repo, topline_jobs)):
        if res.get("error"):
            fail(it, res["error"])
            continue
        rows = res["rows"]
        errs = [f"line {i + 1}: {r['error']}" for i, r in enumerate(rows) if r["kind"] == "err"]
        if errs:
            fail(it, "Topline can't run the calculator lines: " + "; ".join(errs))
            continue
        exp = tl.get("expect")
        if not exp:
            warn(it, "lines run, but check.topline.expect is missing, so Topline didn't confirm the answer")
            continue
        target = to_fraction(exp["value"]) if key is None and "value" in exp else key
        if "line" in exp:
            i = exp["line"] - 1
            got = rows[i]["value"] if 0 <= i < len(rows) else None
        else:
            got = next((r["params"][exp["param"]] for r in rows if r["params"] and exp.get("param") in r["params"]), None)
        if isinstance(got, (int, float)) and target is not None and close(got, target, 1e-6):
            verified.add(it["id"])
        else:
            fail(it, f"Topline gives {got!r} for {exp}, expected {target}")

    # Near duplicates of the bank or each other (same thresholds as the bank tests)
    def full(q):
        return shingles(json.dumps(q.get("passage") or ""), q.get("stem", ""), json.dumps(q.get("choices") or ""))

    pool = [(q, full(q), shingles(json.dumps(q["passage"])) if q.get("passage") else None) for q in bank]
    for n, it in enumerate(drafts):
        mine, mine_p = full(it), shingles(json.dumps(it["passage"])) if it.get("passage") else None
        sec = it.get("section", "math")
        for q, fq, fp in pool + [(d, full(d), None) for d in drafts[:n]]:
            if q.get("section", "math") != sec:
                continue
            if overlap(mine, fq) >= 0.75:
                fail(it, f"near duplicate of {q['id']}")
            elif mine_p and fp and overlap(mine_p, fp) >= 0.6:
                fail(it, f"reuses the passage of {q['id']}")

    # Batch-level warnings: answer letters and the longest-choice tell
    mc = [d for d in drafts if d.get("format") == "mc" and d.get("answerIndex") in range(4)]
    if len(mc) >= 8:
        letters = Counter("ABCD"[d["answerIndex"]] for d in mc)
        if max(letters.values()) > 0.4 * len(mc):
            warns.setdefault("(batch)", []).append(f"right answers bunch up: {dict(sorted(letters.items()))}")
        longest = sum(1 for d in mc if len(d["choices"][d["answerIndex"]]) > max(len(c) for i, c in enumerate(d["choices"]) if i != d["answerIndex"]))
        if longest / len(mc) > 0.35:
            warns.setdefault("(batch)", []).append(f"the right answer is the longest choice in {longest} of {len(mc)} questions")

    # Report
    for it in drafts:
        iid = it.get("id", "?")
        tag = "FAIL" if iid in fails else "ok  "
        extra = " (Topline verified)" if iid in verified else ""
        print(f"{tag} {iid}{extra}")
        for m in fails.get(iid, []):
            print(f"     ✗ {m}")
        for m in warns.get(iid, []):
            print(f"     ! {m}")
    for m in warns.get("(batch)", []):
        print(f"! batch: {m}")
    print()
    print("By skill:", dict(Counter(d.get("skill") for d in drafts)))
    print("By difficulty:", dict(Counter(d.get("difficulty") for d in drafts)))
    print(f"{len(drafts) - len([d for d in drafts if d.get('id', '?') in fails])}/{len(drafts)} passed")

    if args.export:
        if fails and not args.export_passing:
            sys.exit("Not exporting: fix the failures, or pass --export-passing to export only the questions that passed.")
        out = []
        for it in drafts:
            if it.get("id", "?") in fails:
                continue
            q = {k: v for k, v in it.items() if k != "check"}
            if q.get("desmos") is not None:
                q["desmos"] = {**q["desmos"], "verified": it["id"] in verified}
            out.append(json.dumps(q, ensure_ascii=False))
        Path(args.export).write_text("\n".join(out) + ("\n" if out else ""))
        print(f"Exported {len(out)} questions to {args.export}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
