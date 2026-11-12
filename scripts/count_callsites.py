#!/usr/bin/env python3
"""Count syntactic .borrow(...) occurrences, excluding comments and definitions."""
import argparse
import ast
import re
from pathlib import Path

from check_dependencies import CPP_SUFFIXES, cpp_clean


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scopes", nargs="*", type=Path, help="files/directories; default: cpp py")
    args = parser.parse_args()
    files = set()
    for scope in args.scopes or [root / "cpp", root / "py"]:
        scope = scope.resolve()
        if not scope.exists():
            parser.error(f"scope does not exist: {scope}")
        if not scope.is_relative_to(root):
            parser.error(f"scope must be inside repository: {scope}")
        # Prune BEFORE traversal: bin can contain complete nested worktrees.
        if any(part in {"bin", ".git", ".venv", "__pycache__", ".pytest_cache"} for part in scope.relative_to(root).parts):
            parser.error(f"excluded scope: {scope}")
        if scope.is_file():
            files.add(scope)
        else:
            import os
            for directory, dirs, names in os.walk(scope, followlinks=False):
                dirs[:] = sorted(d for d in dirs if d not in {"bin", ".git", ".venv", "__pycache__", ".pytest_cache"} and not (Path(directory) / d).is_symlink())
                files.update(Path(directory) / name for name in names)
    total = 0
    print("path:line:count")
    for path in sorted(files):
        if path.suffix not in CPP_SUFFIXES | {".py"} or path.is_symlink():
            continue
        text = path.read_text(encoding="utf-8")
        counts = {}
        if path.suffix == ".py":
            for node in ast.walk(ast.parse(text, filename=str(path))):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "borrow":
                    line = node.func.end_lineno
                    counts[line] = counts.get(line, 0) + 1
        else:
            for match in re.finditer(r'\.\s*borrow\s*\(', cpp_clean(text, strings=True)):
                line = text.count("\n", 0, match.start()) + 1
                counts[line] = counts.get(line, 0) + 1
        for line, count in sorted(counts.items()):
            print(f"{path.relative_to(root).as_posix()}:{line}:{count}")
            total += count
    print(f"TOTAL: {total}")


if __name__ == "__main__":
    main()
