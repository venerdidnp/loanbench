#!/usr/bin/env python3
"""Audit changed baseline call-site source lines, not just total-count deltas."""
import ast
import difflib
import re
import subprocess
from pathlib import Path

from check_dependencies import cpp_clean

ROOT = Path(__file__).resolve().parents[1]
BASE = "5b26936"
total = changed = production = 0
for name in subprocess.check_output(["git", "ls-tree", "-r", "--name-only", BASE], text=True).splitlines():
    if not name.startswith(("cpp/", "py/")) or Path(name).suffix not in {".cpp", ".hpp", ".py"}:
        continue
    before = subprocess.check_output(["git", "show", f"{BASE}:{name}"], text=True)
    after = (ROOT / name).read_text()
    if name.endswith(".py"):
        calls = [node.func.end_lineno for node in ast.walk(ast.parse(before))
                 if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                 and node.func.attr == "borrow"]
    else:
        calls = [before.count("\n", 0, match.start()) + 1
                 for match in re.finditer(r"\.\s*borrow\s*\(", cpp_clean(before, strings=True))]
    same = set()
    for block in difflib.SequenceMatcher(None, before.splitlines(), after.splitlines(), autojunk=False).get_matching_blocks():
        same.update(range(block.a + 1, block.a + block.size + 1))
    for line in sorted(calls):
        total += 1
        modified = line not in same
        changed += modified
        is_production = "/tests/" not in name
        production += modified and is_production
        print(f"{'CHANGED' if modified else 'same':7} {name}:{line}: {before.splitlines()[line - 1].strip()}")
print(f"Baseline expressions: {total}; changed enclosing source lines: {changed}; production changed: {production}")
print("Method: baseline AST/C++ cleaned calls; exact-line diff matching. New calls excluded.")
print("The borrow invocation arguments themselves are unchanged; enclosing usage is what changed.")
