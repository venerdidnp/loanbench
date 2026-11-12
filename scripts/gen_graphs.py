#!/usr/bin/env python3
"""Generate measured before/after Mermaid graphs; arrows mean depends on."""
import argparse
import ast
import json
import re
from pathlib import Path

from check_dependencies import cpp_clean, inspect, python_imports


def write_graph(path, title, edges, nodes=()):
    labels = sorted(set(nodes) | {node for edge in edges for node in edge})
    ids = {label: f"n{index}" for index, label in enumerate(labels)}
    lines = [f"%% {title}", "%% Arrow: source --> dependency", "flowchart LR"]
    lines += [f"    {ids[label]}[{json.dumps(label)}]" for label in labels]
    lines += [f"    {ids[source]} --> {ids[target]}" for source, target in sorted(set(edges))]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{path}: {len(labels)} nodes, {len(set(edges))} edges")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--baseline", type=Path, help="directory containing reconstructed pinjamlab.cpp and pinjamlab.py")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    baseline = (args.baseline or root / "bin/reconstructed").resolve()
    output = (args.output or root / "docs/graphs").resolve()
    if not output.is_relative_to(root):
        parser.error("output must be inside repository")
    sources = [baseline / "pinjamlab.cpp", baseline / "pinjamlab.py"]
    if not all(path.is_file() for path in sources):
        parser.error(f"standalone reconstructed baseline missing in {baseline}; pass --baseline")
    edges, violations = inspect(root)
    output.mkdir(parents=True, exist_ok=True)
    for language, path in zip(("cpp", "py"), sources):
        text = path.read_text(encoding="utf-8")
        if language == "cpp":
            imports = re.findall(r'^\s*#\s*include\s*[<"]([^>"\n]+)[>"]', cpp_clean(text), re.MULTILINE)
        else:
            imports = [name for _, name in python_imports(ast.parse(text), "pinjamlab")]
        write_graph(output / f"before-{language}.mmd",
                    f"Measured standalone reconstructed baseline: {path.relative_to(root) if path.is_relative_to(root) else path.name}",
                    [(path.name, name) for name in imports], [path.name])
        local_edges = []
        layer_edges = []
        for lang, source, source_layer, target_layer, target, _ in edges:
            if lang != language:
                continue
            if language == "py":
                bits = target.split(".")
                # ImportFrom includes symbols; resolve to the longest existing module.
                while bits and not ((root / "py" / Path(*bits)).with_suffix(".py").is_file()
                                    or (root / "py" / Path(*bits) / "__init__.py").is_file()):
                    bits.pop()
                candidate = root / "py" / Path(*bits)
                resolved = candidate.with_suffix(".py") if candidate.with_suffix(".py").is_file() else candidate / "__init__.py"
                target = resolved.relative_to(root).as_posix()
            else:
                target = (root / "cpp/include" / target if target.startswith("pinjamlab/") else root / source / ".." / target).resolve().relative_to(root).as_posix()
            local_edges.append((source, target))
            if source_layer != target_layer:
                layer_edges.append((source_layer, target_layer))
        write_graph(output / f"after-{language}.mmd", "Actual local include/import dependencies", local_edges)
        write_graph(output / f"after-{language}-layers.mmd", "Actual cross-layer include/import dependencies", layer_edges)
    print(f"Dependency gate findings during generation: {len(violations)}")
    return bool(violations)


if __name__ == "__main__":
    raise SystemExit(main())
