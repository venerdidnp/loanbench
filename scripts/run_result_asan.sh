#!/usr/bin/env bash
# Entire C++ suite, limits demo, and real CLI rejection paths under sanitizers.
set -euo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p bin/result-asan
CXX="${CXX:-g++}"
export ASAN_OPTIONS=detect_leaks=1:halt_on_error=1
export UBSAN_OPTIONS=halt_on_error=1:print_stacktrace=1
flags=(-std=c++20 -Wall -Wextra -Werror -g -O1 -fno-omit-frame-pointer
       -fsanitize=address,undefined -fno-pie -no-pie -Icpp/include -Icpp/tests)
echo "Sanitizers: $ASAN_OPTIONS; $UBSAN_OPTIONS"
"$CXX" --version
for suite in test_errors test_raii test_result test_app test_robustness; do
    echo "ASan/UBSan build and run: $suite"
    "$CXX" "${flags[@]}" "cpp/tests/$suite.cpp" -o "bin/result-asan/$suite"
    "./bin/result-asan/$suite"
done
"$CXX" "${flags[@]}" tests/limits_demo.cpp -o bin/result-asan/limits_demo
./bin/result-asan/limits_demo
"$CXX" "${flags[@]}" cpp/app/main.cpp -o bin/result-asan/cli
for prefix in '' my-; do
    status=0
    ./bin/result-asan/cli "sample-data/${prefix}bad-requests.csv" \
        2>"bin/result-asan/${prefix}stderr.txt" || status=$?
    test "$status" -eq 1
    diff "sample-data/${prefix}expected-output.txt" "bin/result-asan/${prefix}stderr.txt"
    echo "ASan/UBSan CLI ${prefix}bad-requests.csv: golden exact, exit 1"
done
echo "PASS: all C++ suites, limits demo and both CLI error paths; no sanitizer diagnostics"
