# Prediction Outcome

> DRAF: evidence-backed implementation notes, not a claim of independently authored student reflection. Rewrite the personal interpretation in your own words before submission. PREDICTION.md remains frozen.

Comparison base: commit `5b26936`. The prediction was 20 changed call-site expressions out of 48, including all 8 production sites. The measured result is **23 changed enclosing call-site source lines out of the original 48**, including **all 8 production sites**. Thus the usage-change prediction was low by 3, while the production prediction was exact.

## Counting Method

Run `python3 scripts/audit_result_calls.py`. It reads baseline sources with `git show 5b26936:<path>`, identifies Python attribute-call AST nodes and cleaned C++ `.borrow(` occurrences, and compares exact enclosing source lines with the working tree using SequenceMatcher. Each original expression contributes once. The complete per-call inventory is `docs/evidence/result_changed_callsites.txt`.

This is a usage-change metric, not an argument-change metric: strictly counting only the text of the `svc.borrow(...)` invocation gives **0 changed invocations**. Calls now sit inside assignments, explicit checks, or value extraction instead. This distinction matters because the prediction used the ambiguous phrase "expressions need text changes." No count is inflated by newly added tests.

| Scope | Original calls | Changed enclosing usage |
| --- | ---: | ---: |
| C++ production | 4 | 4 |
| Python production | 4 | 4 |
| C++ tests | 21 | 7 |
| Python tests | 19 | 8 |
| Total | 48 | 23 |

The unchanged 25 call-site lines test errors which still throw. Two of those unchanged calls are loops whose unavailable case was removed from the input table; the surrounding test behavior changed without changing its call expression. Those are deliberately not counted as changed call-site lines.

All six seed calls changed text and explicitly check success; none are merely asserted away or left ignored. Both runner calls also check the Result before counting a created loan. Seed unavailability raises a programming/setup error; runner unavailability produces the existing rejection message and continues.

## Current Inventory

`bash scripts/count_callsites.sh` now reports 52 expressions in cpp/py: 48 originals plus four new calls in test-only wrappers and equivalence tests. `docs/evidence/result_callsites.txt` captures that inventory; `result_production_callsites.txt` separately records the 8 production calls. Root limits demos contain no service borrow calls and do not affect the comparison.

## Observed Outcome

Unavailability is an ordinary branch at the runner; it no longer needs to travel by exception. However the runner already caught the entire LoanError family before this refactor, so there was no dedicated EquipmentUnavailable catch to remove. The runner actually grows an explicit branch. The benefit is visible expected-outcome handling, not fewer lines or the disappearance of exception handling. Unknown tag/member, case mismatch, duration, reservation and quota remain typed exceptions.

The old fixed ten-row CSV and golden are unchanged. The new CSV has one header and exactly five data rows; both CLI implementations match the C++-generated new golden and exit 1. Full test names and results are in `result_full_run.txt`; all C++ suites and error paths pass sanitizers in `result_asan.txt`. These runs used Python 3.14.4 in the existing venv, not Python 3.12; no 3.12 run is claimed.
