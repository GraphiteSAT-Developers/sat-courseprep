"""Compiles the Reading and Writing question sources into the bank the site serves.

    python3 backend/compile_rw.py          # check every question and write rw_items.jsonl
    python3 backend/compile_rw.py --check  # check only; exit 1 if rw_items.jsonl is out of date

Sources: app/content/bank/rw_src/*.txt (the format is described in rw_src/README.md).
Output:  app/content/bank/rw_items.jsonl, one question per line, in a stable order.

Question ids are the skill code plus a number counted within the skill (rw-wic-007), in file
order. Add new questions at the end of a skill's last file so existing ids (and the students'
done lists, which are stored by id) keep pointing at the same questions.
"""
import json
import re
import sys
from pathlib import Path

BANK = Path(__file__).resolve().parent / "app" / "content" / "bank"
SRC = BANK / "rw_src"
OUT = BANK / "rw_items.jsonl"
SKILLS = json.loads((BANK / "rw_skills.json").read_text())
CODES = {s["code"]: s for s in SKILLS["skills"]}
LEVELS = ("easy", "medium", "hard")
TAGS = ("I", "P", "P1", "P2", "N", "T", "G", "Q", "A", "*A", "X")
INLINE_OK = re.compile(r"\[(/?)(u|i)\]")


class SourceError(ValueError):
    pass


def _check_inline(text, where):
    depth = {"u": 0, "i": 0}
    for m in INLINE_OK.finditer(text):
        depth[m.group(2)] += -1 if m.group(1) else 1
        if depth[m.group(2)] not in (0, 1):
            raise SourceError(f"{where}: unbalanced [{m.group(2)}]")
    if any(depth.values()):
        raise SourceError(f"{where}: unclosed [u] or [i]")
    if re.search(r"\[(?!/?(u|i)\])", text):
        raise SourceError(f"{where}: unknown [tag]")


def _rows(lines, where):
    rows = []
    for line in lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(cells)
    if len(rows) < 2:
        raise SourceError(f"{where}: a table needs a header row and at least one data row")
    width = len(rows[0])
    if any(len(r) != width for r in rows):
        raise SourceError(f"{where}: every table row needs {width} cells")
    return rows


def parse_block(text, where):
    """One question's lines as a dict of raw fields."""
    lines = text.split("\n")
    head = lines[0].split()
    if len(head) != 2 or head[0] not in CODES or head[1] not in LEVELS:
        raise SourceError(f"{where}: the first line must be '## <skill code> <easy|medium|hard>'")
    code, difficulty = head
    entries = []  # [tag, [lines]]
    for raw in lines[1:]:
        line = raw.rstrip()
        m = re.match(r"^(\*?A|I|P1|P2|P|N|T|G|Q|X):\s?(.*)$", line)
        if m:
            entries.append([m.group(1), [m.group(2)]])
        elif line.startswith("|"):
            if not entries or entries[-1][0] not in ("T", "G"):
                raise SourceError(f"{where}: a table row must follow a T: or G: line")
            entries[-1][1].append(line)
        elif not line.strip():
            if entries:
                entries[-1][1].append("")
        else:
            if not entries:
                raise SourceError(f"{where}: text before the first tag")
            entries[-1][1].append(line.strip())

    blocks, choices, answer, prompt, explanation = [], [], None, None, None
    for tag, body in entries:
        if tag in ("T", "G"):
            title, rows = body[0], [b for b in body[1:] if b.strip()]
            table = _rows(rows, where)
            if tag == "T":
                blocks.append({"kind": "table", "caption": title.strip(), "header": table[0], "rows": table[1:]})
            else:
                name, _, label = title.partition("|")
                header, data = table[0], table[1:]
                for r in data:
                    for v in r[1:]:
                        if not re.fullmatch(r"-?[\d,]*\.?\d+", v):
                            raise SourceError(f"{where}: graph values must be numbers, not {v!r}")
                blocks.append({"kind": "graph", "title": name.strip(), "label": label.strip(), "header": header, "rows": data})
            continue
        # Paragraphs: blank lines inside a tag split paragraphs; other lines join with spaces.
        paras, cur = [], []
        for b in body:
            if b == "":
                if cur:
                    paras.append(" ".join(cur))
                    cur = []
            else:
                cur.append(b)
        if cur:
            paras.append(" ".join(cur))
        joined = " ".join(paras)
        _check_inline(joined, where)
        if tag in ("A", "*A"):
            if len(paras) != 1:
                raise SourceError(f"{where}: a choice must be one line")
            if tag == "*A":
                if answer is not None:
                    raise SourceError(f"{where}: more than one starred choice")
                answer = len(choices)
            choices.append(paras[0])
        elif tag == "Q":
            prompt = joined
        elif tag == "X":
            explanation = joined
        elif tag == "I":
            blocks.append({"kind": "intro", "text": joined})
        elif tag == "N":
            if blocks and blocks[-1]["kind"] == "notes":
                blocks[-1]["items"].append(joined)
            else:
                blocks.append({"kind": "notes", "items": [joined]})
        else:
            blocks.append({"kind": {"P": "p", "P1": "text1", "P2": "text2"}[tag], "paras": paras})

    if len(choices) != 4:
        raise SourceError(f"{where}: needs exactly 4 choices, found {len(choices)}")
    if answer is None:
        raise SourceError(f"{where}: mark the right choice with *A:")
    if len(set(choices)) != 4:
        raise SourceError(f"{where}: two choices are the same")
    if not prompt or not explanation:
        raise SourceError(f"{where}: needs a Q: line and an X: line")
    if not any(b["kind"] in ("p", "text1", "notes", "table", "graph") for b in blocks):
        raise SourceError(f"{where}: needs a passage")
    if (code == "ctc") != any(b["kind"] == "text1" for b in blocks):
        raise SourceError(f"{where}: cross-text questions (and only those) use P1: and P2:")
    if code in ("wic", "inf", "tr", "bnd", "fss") and "______" not in json.dumps(blocks) + prompt and "most nearly mean" not in prompt:
        raise SourceError(f"{where}: this skill needs a ______ blank")
    return {"code": code, "difficulty": difficulty, "blocks": blocks, "prompt": prompt,
            "choices": choices, "answerIndex": answer, "explanation": explanation}


def compile_all():
    counters, items, seen_passages = {}, [], {}
    for path in sorted(SRC.glob("*.txt")):
        text = path.read_text()
        parts = re.split(r"(?m)^## ", text)
        line_no = 1 + parts[0].count("\n")
        for part in parts[1:]:
            where = f"{path.name}:{line_no}"
            line_no += part.count("\n")
            q = parse_block(part.strip("\n"), where)
            key = json.dumps(q["blocks"], sort_keys=True) + q["prompt"]
            if key in seen_passages:
                raise SourceError(f"{where}: same question as {seen_passages[key]}")
            seen_passages[key] = where
            skill = CODES[q["code"]]
            counters[q["code"]] = counters.get(q["code"], 0) + 1
            items.append({
                "id": f"rw-{q['code']}-{counters[q['code']]:03d}",
                "section": "rw", "domain": skill["domain"], "skill": skill["name"], "difficulty": q["difficulty"],
                "format": "mc", "blocks": q["blocks"], "prompt": q["prompt"], "choices": q["choices"],
                "answerIndex": q["answerIndex"], "explanation": q["explanation"],
                "provenance": {"author": "graphite", "source": path.name}, "status": "draft",
            })
    return items


def render(items):
    return "".join(json.dumps(i, ensure_ascii=False, separators=(",", ":")) + "\n" for i in items)


def summary(items):
    from collections import Counter
    by_skill = Counter(i["skill"] for i in items)
    by_level = Counter(i["difficulty"] for i in items)
    letters = Counter("ABCD"[i["answerIndex"]] for i in items)
    out = [f"{len(items)} questions"]
    out += [f"  {n:4d}  {s}" for s, n in by_skill.items()]
    out.append("  difficulty: " + ", ".join(f"{k} {by_level[k]}" for k in LEVELS))
    out.append("  answers: " + ", ".join(f"{k} {letters[k]}" for k in "ABCD"))
    return "\n".join(out)


def main(argv):
    try:
        items = compile_all()
    except SourceError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    text = render(items)
    if "--check" in argv:
        if not OUT.exists() or OUT.read_text() != text:
            print("rw_items.jsonl is out of date: run python3 backend/compile_rw.py", file=sys.stderr)
            return 1
        return 0
    OUT.write_text(text)
    print(summary(items))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
