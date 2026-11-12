# Reconstructed Baseline

direkonstruksi oleh mahasiswa karena m3-start tidak diterima

See RECONSTRUCTION.md for scope, intentional defects and harness exceptions.

# PinjamLab Module 3 — Error Handling & Modular Programming

Part of **Laboratorium Pemrograman II** (`25MP7716G014`), S1 Informatika,
Universitas Muhammadiyah Surabaya. Extends the same repository as Modules 1–2.

## Unit verification table

| Unit / test file | Language | Concept verified | Outcome |
|---|---|---|---|
| `cpp/tests/test_errors.cpp` | C++20 | Every `LoanError` subclass, catch-order/precision, a successful borrow | **8 passed** |
| `cpp/tests/test_raii.cpp` | C++20 | `TxnGuard` commits, rolls back on normal exit, rolls back on the throwing path; wired into `LoanService` | **4 passed** |
| `cpp/tests/test_result.cpp` | C++20 | `Result<T>` factories, `value()` throws on failure, the from-scratch match against a throwing twin | **5 passed** |
| `cpp/tests/test_app.cpp` | C++20 | The full pipeline reproduces `expected-output.txt` byte for byte | **1 passed** |
| `py/tests/test_errors.py` | Python 3.12 | Same 5 failure modes, same catch-family guarantee | **8 passed** |
| `py/tests/test_cleanup.py` | Python 3.12 | `txn_guard` context manager releases on every exit path, incl. raising | **4 passed** |
| `py/tests/test_result.py` | Python 3.12 | `Result` + the from-scratch match | **7 passed** |
| `py/tests/test_app.py` | Python 3.12 | The full pipeline matches the SAME `expected-output.txt` as C++ | **1 passed** |

**18 C++ test cases + 20 Python tests.**

## One command

```bash
./run_tests.sh
```

Five steps, and **the script fails (non-zero exit) if any of them does**:

1. **The dependency-rule purity check** — greps `domain/` in both languages
   for io/console tokens outside a comment. `domain/` may not include,
   import, or name anything from `io`, `service` or `app`.
2. Build the C++ suites at `-Wall -Wextra -Werror`.
3. Run the C++ suites.
4. **Cross-language golden file** — run the compiled C++ CLI against
   `sample-data/bad-requests.csv` and diff its stderr against
   `sample-data/expected-output.txt`.
5. Run the Python suite (which independently re-checks the same golden file).

Unlike Module 1's script, this one (like Module 2's) treats a missing
toolchain, a failed diff, or a purity violation as a hard failure — never a
`[SUCCESS]` banner over a step that did not run.

## The ten rows, ten failures, one rule each

`sample-data/bad-requests.csv` is fixed and committed. Every row triggers
exactly one failure, and the two implementations must produce the identical
message, in order, on stderr, exit code 1:

| Row | CSV content | Rejected by | Message |
|---|---|---|---|
| 1 | `,M-101,7` | Validator (io) | `tag is empty` |
| 2 | `LP-001,,7` | Validator (io) | `memberId is empty` |
| 3 | `LP-001,M-101,abc` | Validator (io) | `days is not a number: abc` |
| 4 | `LP-001,M-101,-3` | Validator (io) | `days must be positive, got -3` |
| 5 | `LP-001,M-101,0` | Validator (io) | `days must be positive, got 0` |
| 6 | `LP-999,M-101,7` | domain | `Unknown asset tag: LP-999` |
| 7 | `LP-001,M-404,7` | domain | `Unknown member: M-404` |
| 8 | `LP-002,M-101,7` | domain | `Equipment already on loan: LP-002` |
| 9 | `LP-003,M-102,7` | domain | `Loan quota exceeded: 2 active, limit 2` |
| 10 | `LP-001,M-101,400` | domain | `Loan duration exceeds maximum: 400 > 90` |

Rows 1–5 never reach `domain` — the io-layer `Validator` returns a
`Result<LoanRequest>` and rejects them at the boundary. Rows 6–10 are
business-rule failures raised as typed `LoanError` subclasses and caught once,
centrally, in `app/runner.hpp`'s row loop.

**The seed state these rows depend on** (`app/seed.hpp` / `app/seed.py`),
because the failures for rows 8 and 9 require specific starting conditions:

| Entity | State before row 1 runs | Why |
|---|---|---|
| `LP-001` | Available | rows 7, 10 need it available so their OWN rule is what fails |
| `LP-002` | **Loaned** (to `M-103`) | row 8 expects `EquipmentUnavailable` |
| `LP-003` | Available | row 9's failure is quota, not availability |
| `M-101` | 0 / 2 active | rows 6, 8, 10 need quota to NOT be the failure |
| `M-102` | **2 / 2 active** (at quota) | row 9 expects `QuotaExceeded` |
| `M-103` | 1 / 2 active | holds `LP-002` |

The seed is built by calling the real `borrow()` path (against two
seed-only tags, `SEED-01`/`SEED-02`, that never appear in the CSV), so the
seed itself already exercises the same invariants the ten rows do.

## The dependency rule, enforced

`domain/` contains `LoanError`, `Result<T>`, `Member`, `Equipment`, `Loan` —
pure rules, in both languages. It does not include `<fstream>`, `<iostream>`,
or `<sstream>` in C++, and does not `import csv`/`sys` or call `print(`/`open(`
in Python. `run_tests.sh` step 1 greps for exactly those tokens (outside
comments) and fails the build on a hit — verified against both a clean run
and a deliberately injected violation during authoring.

## Verified

- **Environment:** Windows 11 · g++ (GCC) 15.2.0 · Python 3.12.13 · pytest 8.3.4
- **Date:** 2026-09-15
- **Result:** `./run_tests.sh` exits 0; all five steps pass; no warnings under
  `-Wall -Wextra -Werror`.

## Directory structure

```
Module3/
├── run_tests.sh                    # purity check, C++, golden file, Python -- all 5 fail loudly
├── cpp/
│   ├── include/pinjamlab/
│   │   ├── domain/                 # PURE: LoanError, Result<T>, Member, Equipment, Loan
│   │   ├── service/                # LoanService (orchestration), Database + TxnGuard (RAII)
│   │   ├── io/                     # CsvReader, Validator, ReportWriter
│   │   └── app/                    # seed.hpp, runner.hpp (pure of console I/O, returns lines)
│   ├── app/main.cpp                # the ONLY place with iostream + exit codes
│   └── tests/
├── py/pinjamlab/                   # domain/ service/ io/ app/ -- the same four
├── py/tests/
└── sample-data/
    ├── bad-requests.csv            # fixed, committed, 10 rows, one failure each
    └── expected-output.txt         # generated FROM the real C++ binary, not hand-typed
```

`my-bad-requests.csv` and the two original `LoanError` subclasses named in the
module (e.g. `ReservationConflict`, `FineCapReached`) are **deliberately
absent**: they are Lab 1.3's bring-your-own-input and Lab 2.1's original-work
deliverables respectively, not instructor-provided starter content.

## AddressSanitizer

This toolchain (WinLibs/MinGW g++ 15.2.0) does not ship `libasan`, so Lab
2.4's Defect B evidence (`-fsanitize=address`) cannot be captured here. Per
the fallback already established in Week 2's deck: accept a destructor-trace
print (a live-object counter that changes between the raw-pointer and
smart-pointer versions) as equivalent evidence when a student's own toolchain
also lacks ASan.
