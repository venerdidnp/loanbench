#!/usr/bin/env bash
# ==============================================================================
# PinjamLab Module 3: one command -- build, C++ tests, Python tests, AND the
# dependency-rule purity check (Lab 3.2: "Add the purity check to run_tests.sh
# so a violation fails the build.").
#
# Like Module 2's script and unlike Module 1's, this one FAILS (non-zero exit)
# when a toolchain is missing or a check fails -- it never prints a success
# banner over a step that did not actually run.
# ==============================================================================
set -euo pipefail

cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p bin

CXX="${CXX:-g++}"
# Prefer the WSL project venv; never select a Windows interpreter implicitly.
if [ -z "${PY:-}" ]; then
    if [ -x ".venv/bin/python" ]; then PY=".venv/bin/python"
    else PY="python3"; fi
fi
command -v "$CXX" >/dev/null || { echo "FATAL: no C++ compiler ($CXX) on PATH."; exit 2; }
command -v "$PY"  >/dev/null || { echo "FATAL: no Python interpreter ($PY) on PATH."; exit 2; }

echo "================================================================================"
echo " [PinjamLab M3] $("$CXX" --version | head -1)"
echo " [PinjamLab M3] $("$PY" --version 2>&1)"
echo "================================================================================"

# ---- 1/5: parsed layer directions and domain I/O purity ----------------------
echo ""
echo ">>> [1/5] Dependency gate (C++ includes and Python AST)"
"$PY" scripts/check_dependencies.py .

# ---- 2/5: build the C++ suites -----------------------------------------------
echo ""
echo ">>> [2/5] Building C++20 tests (-Wall -Wextra -Werror)"
for t in test_errors test_raii test_result test_app test_robustness; do
    "$CXX" -std=c++20 -Wall -Wextra -Werror \
           -Icpp/include -Icpp/tests "cpp/tests/$t.cpp" -o "bin/$t"
done
"$CXX" -std=c++20 -Wall -Wextra -Werror -Icpp/include cpp/app/main.cpp -o bin/pinjamlab_cli

# ---- 3/5: run the C++ suites --------------------------------------------------
echo ""
echo ">>> [3/5] Running C++20 test suites"
for t in test_errors test_raii test_result test_app test_robustness; do
    "./bin/$t"
done

# ---- 4/5: the cross-language golden-file check -------------------------------
echo ""
echo ">>> [4/5] Cross-language golden files and exact CLI exit codes"
expect_rejected() {
    local status=0
    "$@" || status=$?
    if [ "$status" -ne 1 ]; then
        echo "FATAL: CLI must exit 1 for bad requests, got $status: $*" >&2
        exit 1
    fi
}
# Line endings are normalised on BOTH sides (tr -d '\r'): the Windows CLI prints
# CRLF, Linux/macOS prints LF, and the golden file is stored as LF (.gitattributes).
# The message text must still match exactly; only the line terminator is ignored.
GOLDEN="${GOLDEN:-sample-data/expected-output.txt}"
expect_rejected ./bin/pinjamlab_cli sample-data/bad-requests.csv 2>bin/cpp_stderr.txt >/dev/null
expect_rejected env PYTHONPATH=py "$PY" -m pinjamlab.app.main sample-data/bad-requests.csv 2>bin/py_stderr.txt >/dev/null
for output in bin/cpp_stderr.txt bin/py_stderr.txt; do
    diff <(tr -d '\r' < "$output") <(tr -d '\r' < sample-data/expected-output.txt)
    if [ "$GOLDEN" != "sample-data/expected-output.txt" ]; then
        [ -f "$GOLDEN" ] || { echo "FATAL: golden file not found: $GOLDEN" >&2; exit 1; }
        diff <(tr -d '\r' < "$output") <(tr -d '\r' < "$GOLDEN")
    fi
    echo "  match: $output matches golden file(s), CLI exit 1"
done

# ---- 5/5: run the Python suite, including gate mutation tests ------------------
echo ""
echo ">>> [5/5] Running Python test suite (version reported above)"
PYTHONPATH=py "$PY" -m pytest py/tests -q

echo ""
echo "================================================================================"
echo " [SUCCESS] Purity check, C++ suites, golden file, and Python suite all passed."
echo "================================================================================"
