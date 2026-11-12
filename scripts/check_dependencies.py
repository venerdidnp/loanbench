#!/usr/bin/env python3
"""Check inward layer dependencies and domain I/O purity without importing code."""
import argparse
import ast
import posixpath
import re
from pathlib import Path

LAYERS = ("domain", "io", "service", "app")
FORBIDDEN = {"domain": {"io", "service", "app"}, "io": {"service", "app"},
             "service": {"app"}, "app": set()}
CPP_SUFFIXES = {".h", ".hpp", ".hh", ".hxx", ".cpp", ".cc", ".cxx"}
CPP_IO = {"fstream", "iostream", "sstream", "cstdio", "stdio.h", "filesystem", "unistd.h"}
PY_IO = {"csv", "sys", "io", "os", "pathlib", "tempfile", "socket", "subprocess", "shutil"}


def cpp_clean(text, strings=False):
    # Preserve newlines so diagnostics and callsite locations remain physical lines.
    pattern = r'R"([^ ()\\\t\r\n]*)\([\s\S]*?\)\1"|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/'
    return re.sub(pattern, lambda m: re.sub(r"[^\n]", " ", m[0])
                  if strings or m[0].startswith(("//", "/*")) else m[0], text)


def python_imports(tree, module, package=False):
    parent = module.split(".") if package else module.split(".")[:-1]
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield node.lineno, alias.name
        elif isinstance(node, ast.ImportFrom):
            base = node.module or ""
            if node.level:
                base = ".".join(parent[:len(parent) - node.level + 1] + ([base] if base else []))
            for alias in node.names:
                yield node.lineno, base + ("." + alias.name if alias.name != "*" else "")


def source_files(root):
    for base, language in ((root / "cpp/include/pinjamlab", "cpp"),
                           (root / "cpp/app", "cpp"), (root / "py/pinjamlab", "py")):
        if not base.is_dir():
            raise ValueError(f"missing source directory: {base}")
        for path in sorted(base.rglob("*")):
            if path.is_file() and path.suffix in (CPP_SUFFIXES if language == "cpp" else {".py"}):
                yield language, path


def inspect(root):
    edges, violations = [], []
    for language, path in source_files(root):
        relative = path.relative_to(root).as_posix()
        parts = relative.split("/")
        source_layer = "app" if relative.startswith("cpp/app/") else parts[3 if language == "cpp" else 2]
        if source_layer not in LAYERS:
            continue
        text = path.read_text(encoding="utf-8")
        dependencies = []
        if language == "py":
            module_parts = list(path.relative_to(root / "py").with_suffix("").parts)
            package = module_parts[-1] == "__init__"
            if package:
                module_parts.pop()
            try:
                tree = ast.parse(text, filename=relative)
            except SyntaxError as error:
                violations.append(f"{relative}:{error.lineno}: invalid Python: {error.msg}")
                continue
            imports = list(python_imports(tree, ".".join(module_parts), package))
            for line, name in imports:
                bits = name.split(".")
                if len(bits) > 1 and bits[0] == "pinjamlab" and bits[1] in LAYERS:
                    dependencies.append((line, bits[1], name))
                elif source_layer == "domain" and bits[0] in PY_IO:
                    violations.append(f"{relative}:{line}: domain I/O import: {name}")
            if source_layer == "domain":
                aliases = {}
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        aliases.update((a.asname or a.name, a.name) for a in node.names)
                    elif isinstance(node, ast.ImportFrom):
                        aliases.update((a.asname or a.name, (node.module or "") + "." + a.name) for a in node.names)
                for node in ast.walk(tree):
                    if not isinstance(node, ast.Call):
                        continue
                    name = ast.unparse(node.func)
                    head, _, tail = name.partition(".")
                    name = aliases.get(head, head) + ("." + tail if tail else "")
                    if name in {"print", "open", "input", "builtins.print", "builtins.open", "builtins.input"} or name.rsplit(".", 1)[-1] in {"open", "read_text", "write_text", "read_bytes", "write_bytes"}:
                        violations.append(f"{relative}:{node.lineno}: domain I/O call: {name}")
        else:
            clean = cpp_clean(text)
            for match in re.finditer(r'^\s*#\s*include\s*[<"]([^>"\n]+)[>"]', clean, re.MULTILINE):
                name = match[1]
                line = clean.count("\n", 0, match.start(1)) + 1
                if name.startswith("pinjamlab/"):
                    target = name.split("/")
                elif (path.parent / name).is_file() or name.startswith(("../", "./", "domain/", "io/", "service/", "app/")):
                    target = posixpath.normpath(posixpath.join(posixpath.dirname(relative), name)).split("/")
                    target = target[target.index("pinjamlab"):] if "pinjamlab" in target else []
                else:
                    target = []
                if len(target) > 1 and target[1] in LAYERS:
                    dependencies.append((line, target[1], name))
                if source_layer == "domain" and (name in CPP_IO or "csv" in name.lower()):
                    violations.append(f"{relative}:{line}: domain I/O include: {name}")
            if source_layer == "domain":
                for match in re.finditer(r'\bstd\s*::\s*(?:cout|cerr|clog|cin|wcout|wcerr|wclog|wcin)\b|\b(?:printf|fprintf|fopen|freopen|puts|scanf)\s*\(|\bcsv\b', cpp_clean(text, strings=True), re.IGNORECASE):
                    violations.append(f"{relative}:{text.count(chr(10), 0, match.start()) + 1}: domain I/O: {match[0]}")
        for line, target, name in dependencies:
            edges.append((language, relative, source_layer, target, name, line))
            if target in FORBIDDEN[source_layer]:
                violations.append(f"{relative}:{line}: forbidden {source_layer} -> {target}: {name}")
    return sorted(set(edges)), sorted(set(violations))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        edges, violations = inspect(args.root.resolve())
    except (OSError, ValueError) as error:
        print(f"Dependency gate error: {error}")
        return 2
    if violations:
        print("\n".join(violations))
        print(f"FAIL: {len(violations)} dependency/purity violation(s)")
        return 1
    print(f"PASS: dependency directions and domain I/O purity ({len(edges)} local dependencies)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
