"""Exercise the real gate against isolated source copies, never live sources."""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
GATE = ROOT / "scripts/check_dependencies.py"
DIRECTIONS = [("domain", "io"), ("domain", "service"), ("domain", "app"),
              ("io", "service"), ("io", "app"), ("service", "app")]


@pytest.fixture
def source_copy():
    (ROOT / "bin").mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="dependency-gate-", dir=ROOT / "bin") as directory:
        root = Path(directory)
        for source in ("cpp/include/pinjamlab", "cpp/app", "py/pinjamlab"):
            shutil.copytree(ROOT / source, root / source, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        yield root


def run_gate(root):
    return subprocess.run([sys.executable, str(GATE), str(root)], capture_output=True, text=True)


def test_real_sources_pass():
    result = run_gate(ROOT)
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize("source,target", DIRECTIONS)
@pytest.mark.parametrize("language", ["cpp", "py"])
def test_each_forbidden_direction(source_copy, source, target, language):
    if language == "cpp":
        path = source_copy / "cpp/include/pinjamlab" / source / "gate_probe.hpp"
        text = f'#include "pinjamlab/{target}/gate_probe.hpp"\n'
    else:
        path = source_copy / "py/pinjamlab" / source / "gate_probe.py"
        text = f"from ..{target} import gate_probe\n"
    path.write_text(text, encoding="utf-8")
    result = run_gate(source_copy)
    assert result.returncode == 1, result.stdout + result.stderr
    assert f"forbidden {source} -> {target}" in result.stdout
    print(f"REJECTED {language} {source} -> {target}: {result.stdout.strip()}")


@pytest.mark.parametrize("language,text", [
    ("py", "def hidden():\n    import csv as c\n"),
    ("py", "from builtins import open as op\nop('file')\n"),
    ("py", "print('forbidden')\n"),
    ("cpp", "#include <fstream>\n"),
    ("cpp", "void probe() { std::cout << 1; }\n"),
])
def test_domain_io_rejected(source_copy, language, text):
    base = "py/pinjamlab/domain" if language == "py" else "cpp/include/pinjamlab/domain"
    path = source_copy / base / ("gate_probe.py" if language == "py" else "gate_probe.hpp")
    path.write_text(text, encoding="utf-8")
    result = run_gate(source_copy)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "domain I/O" in result.stdout


def test_comments_and_strings_are_not_dependencies(source_copy):
    (source_copy / "py/pinjamlab/domain/gate_probe.py").write_text(
        '# import csv\ntext = "print(open())"\n', encoding="utf-8")
    (source_copy / "cpp/include/pinjamlab/domain/gate_probe.hpp").write_text(
        '/* #include "pinjamlab/app/runner.hpp" */\n// std::cout\nconst char* text = "csv std::cout";\n', encoding="utf-8")
    result = run_gate(source_copy)
    assert result.returncode == 0, result.stdout + result.stderr
