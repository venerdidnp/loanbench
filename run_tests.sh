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

# ---- 1/5: the dependency-rule purity check -----------------------------------
# domain/ may not include, import, or name anything from io, service or app.
# The practical test is a grep: if domain/ contains fstream/iostream/sstream,
# std::cout/cerr/cin, or the word csv (C++); or a module-level csv/sys import,
# print(, or open( (Python) -- OUTSIDE a comment -- the rule is broken.
echo ""
echo ">>> [1/5] Dependency-rule purity check (domain/ must not touch io)"
check_purity() {
    local dir="$1" lang="$2" found=0 pattern
    if [ "$lang" = "cpp" ]; then
        pattern='#include[[:space:]]*[<"](fstream|iostream|sstream)[>"]|std::cout|std::cerr|std::cin|[Cc][Ss][Vv]'
    else
        pattern='^[[:space:]]*(import|from)[[:space:]]+(csv|sys)\b|\bprint\(|\bopen\('
    fi
    while IFS= read -r hit; do
        local file="${hit%%:*}" rest="${hit#*:}"
        local lineno="${rest%%:*}" content="${rest#*:}"
        local trimmed; trimmed="$(echo "$content" | sed -E 's/^[[:space:]]*//')"
        if [ "$lang" = "cpp" ]; then
            case "$trimmed" in '//'*) continue ;; esac
        else
            case "$trimmed" in '#'*) continue ;; esac
        fi
        echo "  PURITY VIOLATION: $file:$lineno: $content"
        found=1
    done < <(grep -rnE --exclude-dir=__pycache__ --exclude='*.pyc' "$pattern" "$dir" 2>/dev/null)
    return $found
}
purity_failed=0
check_purity cpp/include/pinjamlab/domain cpp || purity_failed=1
check_purity py/pinjamlab/domain py || purity_failed=1
if [ "$purity_failed" -ne 0 ]; then
    echo "FATAL: domain/ is no longer pure. See violations above."
    exit 3
fi
echo "  clean: domain/ contains no io, no console, no CSV, in either language."

# ---- 2/5: build the C++ suites -----------------------------------------------
echo ""
echo ">>> [2/5] Building C++20 tests (-Wall -Wextra -Werror)"
for t in test_errors test_raii test_result test_app; do
    "$CXX" -std=c++20 -Wall -Wextra -Werror \
           -Icpp/include -Icpp/tests "cpp/tests/$t.cpp" -o "bin/$t"
done
"$CXX" -std=c++20 -Wall -Wextra -Werror -Icpp/include cpp/app/main.cpp -o bin/pinjamlab_cli

# ---- 3/5: run the C++ suites --------------------------------------------------
echo ""
echo ">>> [3/5] Running C++20 test suites"
for t in test_errors test_raii test_result test_app; do
    "./bin/$t"
done

# ---- 4/5: the cross-language golden-file check -------------------------------
echo ""
echo ">>> [4/5] Cross-language golden file: C++ CLI vs sample-data/expected-output.txt"
./bin/pinjamlab_cli sample-data/bad-requests.csv 2>bin/cpp_stderr.txt 1>/dev/null || true
# Line endings are normalised on BOTH sides (tr -d '\r'): the Windows CLI prints
# CRLF, Linux/macOS prints LF, and the golden file is stored as LF (.gitattributes).
# The message text must still match exactly; only the line terminator is ignored.
GOLDEN="${GOLDEN:-sample-data/expected-output.txt}"
diff <(tr -d '\r' < bin/cpp_stderr.txt) <(tr -d '\r' < "$GOLDEN")
echo "  match: C++ CLI output is byte-for-byte identical to $GOLDEN (modulo CR)"

# ---- 5/5: run the Python suite, including the SAME golden-file check --------
echo ""
echo ">>> [5/5] Running Python test suite (version reported above)"
PYTHONPATH=py "$PY" -m pytest py/tests -q

echo ""
echo "================================================================================"
echo " [SUCCESS] Purity check, C++ suites, golden file, and Python suite all passed."
echo "================================================================================"
