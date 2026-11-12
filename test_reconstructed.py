"""Subprocess contracts shared by both standalone reconstructions."""
from pathlib import Path
import subprocess
import sys
import pytest

ROOT = Path(__file__).resolve().parent

@pytest.fixture(scope="session")
def cpp():
    target = ROOT / "bin" / "reconstructed_cli"
    subprocess.run(["g++", "-std=c++20", "-Wall", "-Wextra", "-Werror", str(ROOT / "pinjamlab.cpp"), "-o", str(target)], check=True)
    return [str(target)]

@pytest.fixture(params=["cpp", "python"])
def command(request, cpp):
    return cpp if request.param == "cpp" else [sys.executable, str(ROOT / "pinjamlab.py")]

@pytest.mark.parametrize("fields,message", [
    ("LP-999,M-101,7", "Unknown asset tag: LP-999"),
    ("LP-003,M-102,7", "Loan quota exceeded: 2 active, limit 2"),
    ("LP-001,M-101,abc", "days is not a number: abc"),
])
def test_rejected_row_exact_message_and_nonzero(command, tmp_path, fields, message):
    source = tmp_path / "request.csv"
    source.write_text("tag,memberId,days\n" + fields + "\n")
    result = subprocess.run(command + [str(source)], capture_output=True, text=True)
    assert (result.stderr, result.returncode, result.stdout) == (f"row 1: {message}\n", 1, "")

def test_missing_input_exact_message_and_nonzero(command, tmp_path):
    path = str(tmp_path / "missing.csv")
    result = subprocess.run(command + [path], capture_output=True, text=True)
    assert (result.stderr, result.returncode, result.stdout) == (f"cannot open input: {path}\n", 1, "")

def test_valid_request(command, tmp_path):
    source = tmp_path / "valid.csv"
    source.write_text("tag,memberId,days\nLP-001,M-101,7\n")
    result = subprocess.run(command + [str(source)], capture_output=True, text=True)
    assert (result.stdout, result.stderr, result.returncode) == ("row 1: loan created: LP-001\n", "", 0)

def test_ten_errors_match_main_golden(command):
    result = subprocess.run(command + [str(ROOT / "sample-data/bad-requests.csv")], capture_output=True, text=True)
    expected = Path("/home/venerdi/loanbench/sample-data/expected-output.txt").read_text()
    assert (result.stderr, result.returncode, result.stdout) == (expected, 1, "")
