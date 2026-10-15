"""Merge a batch file into the bank.

usage: python3 web/scripts/merge_batch.py <batch-name>
  reads  web/content/batches/<batch-name>.ts   (export const batch: Item[] = [ ... ];)
         web/scripts/checks_<batch_name_with_underscores>.py   (CHECKS = {...})
  appends the entries to web/content/items.ts under a batch comment, appends the
  check module's functions to verify_items.py and registers them in CHECKS, then
  deletes the two batch files. Run verify_items.py and lint_items.py afterwards.
"""
import re, sys
from pathlib import Path

name = sys.argv[1]
root = Path(__file__).resolve().parents[2]
batch_ts = root / "web/content/batches" / f"{name}.ts"
checks_py = root / "web/scripts" / f"checks_{name.replace('-', '_')}.py"
items_ts = root / "web/content/items.ts"
verify_py = root / "web/scripts/verify_items.py"

src = batch_ts.read_text()
m = re.search(r"export const batch: Item\[\] = \[\n(.*)\n\];\s*$", src, re.S)
assert m, "batch file must end with `export const batch: Item[] = [ ... ];`"
entries = m.group(1).rstrip()
items = items_ts.read_text()
idx = items.find("\n];")
assert idx > 0
tail = items[idx + len("\n];"):]  # listItems / getItem stay after the array
items = items[:idx].rstrip() + f"\n\n  // ---------------------------------------------------------------------------\n  // Batch {name} (claude-agent, 2026-10-15). Keys verified with SymPy.\n  // ---------------------------------------------------------------------------\n{entries}\n];" + tail
items_ts.write_text(items)

chk = checks_py.read_text()
# drop the docstring and the sys.path / verify_items import lines; keep sympy
# imports, symbol definitions and helpers, which the functions depend on
if chk.startswith('"""'):
    chk = chk[chk.find('"""', 3) + 3:]
body = "\n".join(
    l for l in chk.splitlines()
    if not l.startswith(("from __future__", "import sys", "from pathlib", "sys.path.insert", "from verify_items import"))
    and "noqa: E402" not in l
)
cm = re.search(r"\nCHECKS\s*(?::[^=]*)?=\s*\{(.*?)\n\}", body, re.S)
assert cm, "checks module must define CHECKS = {...}"
registry = cm.group(1)
body = body[:cm.start()].rstrip() + "\n"
v = verify_py.read_text()
ci = v.find("\nCHECKS = {")
assert ci > 0
v = v[:ci].rstrip() + f"\n\n\n# ----- Batch {name} -----\n" + body.lstrip("\n") + "\n" + v[ci:]
# register entries before the closing brace of CHECKS
ce = v.find("\n}", v.find("\nCHECKS = {"))
v = v[:ce] + f"\n    # batch {name}" + registry.rstrip().rstrip(",") + "," + v[ce:]
verify_py.write_text(v)
batch_ts.unlink(); checks_py.unlink()
print(f"merged {name}: {entries.count('    id: ')} items")
