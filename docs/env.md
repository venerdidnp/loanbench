# Environment (as measured, not assumed)

| Item | Value |
|---|---|
| OS | Windows 11 Home 10.0.26200 |
| Shell used for `run_tests.sh` | Git Bash (MSYS2, `bash` 3.x+) |
| C++ compiler | g++ 15.2.0 (MinGW-Builds, posix-seh) -- `-std=c++20 -Wall -Wextra -Werror` |
| Python (tests) | 3.12.7 inside `.venv` (created from `.../Python312/python.exe`) |
| pytest | 9.2.0 (in `.venv`) |
| Python on PATH (NOT used for tests) | 3.11.9 -- the first baseline run, `evidence/00_baseline_run.txt`, used it |
| Clang / MSVC | not installed |
| WSL | present on the machine but deliberately **not used** |
| ASan | MinGW has no `libasan`; see T6 in the task prompt. Method to be reported honestly in Phase 2.4 |

## Creating the venv

Git Bash:

    "/c/Users/<user>/AppData/Local/Programs/Python/Python312/python.exe" -m venv .venv
    .venv/Scripts/python -m pip install -r py/requirements.txt

cmd.exe:

    "C:\Users\<user>\AppData\Local\Programs\Python\Python312\python.exe" -m venv .venv
    .venv\Scripts\python -m pip install -r py\requirements.txt

PowerShell:

    & "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" -m venv .venv
    .venv\Scripts\python -m pip install -r py\requirements.txt

`run_tests.sh` uses `.venv/Scripts/python` (Windows) or `.venv/bin/python` (Linux/macOS) when present,
otherwise `python` from PATH. Override with `PY=...`. `.venv/` is git-ignored.

## Line endings (T1)

`sample-data/expected-output.txt` is stored with LF (`.gitattributes`: `sample-data/*.txt text eol=lf`).
Step 4 of `run_tests.sh` strips `\r` from both sides before `diff`, so the Windows CLI (CRLF) and a
Linux CLI (LF) both pass. Proof: `evidence/01_t1_line_ending_proof.txt`.

## Not yet tested

Linux/macOS have **not** been tested. This is the job of the lab partner in Lab 3.4
(`docs/peer_reproduction_checklist.md`, to be created in Phase 3).
