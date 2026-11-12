#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
g++ -std=c++20 -g -O0 -Wall -Wextra -Werror -fsanitize=address -fno-omit-frame-pointer -fno-pie -no-pie pinjamlab.cpp -o bin/reconstructed_asan
# Use the committed ten-error fixture: row 9 reaches allocation then quota.
set +e
ASAN_OPTIONS=detect_leaks=1:exitcode=23 ./bin/reconstructed_asan sample-data/bad-requests.csv > bin/asan.stdout 2> bin/asan.stderr
status=$?
set -e
cat bin/asan.stderr
test "$status" -eq 1
test ! -s bin/asan.stdout
! grep -Eq 'AddressSanitizer|LeakSanitizer' bin/asan.stderr
diff bin/asan.stderr "${GOLDEN:-sample-data/expected-output.txt}"
printf 'PASS: all ten diagnostics, application exit 1, no sanitizer findings\n'
