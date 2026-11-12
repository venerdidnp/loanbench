# Lab 2 Result Refactor

> DRAF: generated implementation/evidence report. The technical snippets below are actual changes against 5b26936, but the rationale must be reviewed and rewritten as personal analysis before submission. This draft label is not a claim that tests or implementation are incomplete.

## Decision And Contract

An already-loaned catalogue item is expected in normal operation, and the batch runner can reject that row and continue. `LoanService::borrow` / `LoanService.borrow` now returns `Result<Loan>` / `Result[Loan]`. Only EquipmentUnavailable becomes a failed Result, with the exact old message. Unknown tag/member, case mismatch, invalid duration, reservation conflict, and quota still throw/raise in their original order. Errors other than LoanError still propagate through the runner. There is no production throwing twin.

## Actual Diff Snippets

C++ service, `cpp/include/pinjamlab/service/loan_service.hpp`:

```diff
-    [[nodiscard]] Loan borrow(const std::string& tag, const std::string& memberId, int days) {
+    // Only unavailability returns failure; all other guards still throw.
+    [[nodiscard]] Result<Loan> borrow(const std::string& tag, const std::string& memberId, int days) {
-        if (!eq.isAvailable()) throw EquipmentUnavailable(tag);
+        if (!eq.isAvailable()) return Result<Loan>::failure(EquipmentUnavailable(tag).what());
-        return Loan("L-" + tag + "-" + memberId, tag, memberId, days);
+        return Result<Loan>::success(Loan("L-" + tag + "-" + memberId, tag, memberId, days));
```

C++ caller, `cpp/include/pinjamlab/app/runner.hpp`:

```diff
-            (void)svc.borrow(req.tag, req.memberId, req.days);
+            const auto borrowed = svc.borrow(req.tag, req.memberId, req.days);
+            if (!borrowed.ok()) {
+                ++result.rejected;
+                result.rejectedLines.push_back(
+                    ReportWriter::rejectedLine(row.lineNumber, borrowed.error()));
+                continue;
+            }
```

Python service, `py/pinjamlab/service/loan_service.py`:

```diff
-    def borrow(self, tag: str, member_id: str, days: int) -> Loan:
+    def borrow(self, tag: str, member_id: str, days: int) -> Result[Loan]:
+        # Only unavailability returns failure; other guards still raise.
-            raise EquipmentUnavailable(tag)
+            return Result.failure(str(EquipmentUnavailable(tag)))
-        return Loan(f"L-{tag}-{member_id}", tag, member_id, days)
+        return Result.success(Loan(f"L-{tag}-{member_id}", tag, member_id, days))
```

Python caller, `py/pinjamlab/app/runner.py`:

```diff
-            svc.borrow(req.tag, req.member_id, req.days)
+            borrowed = svc.borrow(req.tag, req.member_id, req.days)
+            if not borrowed.ok:
+                result.rejected += 1
+                result.rejected_lines.append(
+                    ReportWriter.rejected_line(row.line_number, borrowed.error))
+                continue
```

Simpler in one sentence: the runner can handle the expected unavailable outcome locally by checking a value, without interpreting an exception as normal control flow. This does not make the whole function shorter, nor does it eliminate its remaining typed exception handlers.

## Handmade Storage

C++ Result owns a manual union payload, bool discriminator, and error string. Failure does not construct T, so the unchanged non-default-constructible Loan works. Placement construction sets the discriminator only after success; destruction occurs only when a payload is alive. Copy/move construction and assignment are explicit, including self-assignment and transitions between failure and success. A throwing assignment provides the basic guarantee (valid, destructible failure), not preservation of the old success. The error string is ordinary message data, not a library payload container. No optional, expected, variant, or pointer storage is used.

Python's existing handmade frozen Result dataclass already holds a Loan reference without default-constructing Loan, so it did not need a storage rewrite. Both types guard failed value access. C++ nodiscard warns but can be explicitly suppressed; Python provides no such warning and callers can ignore a Result.

## Equivalence And Limits

`cpp/tests/test_result.cpp` and `py/tests/test_result.py` contain test-only wrappers that call the real borrow and convert only a failed Result into EquipmentUnavailable. Twelve identical input cases cover success, unavailable, every remaining service guard, and guard precedence on an unavailable item. Tests compare loan fields, exception type/message or failure message, availability, reservation, member counts, ledger contents and pending count. Rejections additionally preserve the known seeded state. Returning the owned item in both services observes the private ownership mapping. This is adapter equivalence against the current rules, not an independent archived implementation of the old algorithm.

`tests/limits_demo.cpp` and `tests/limits_demo.py` are executable assertions: a 33-frame chain propagates a failure explicitly at every frame and succeeds with the expected value on the alternate path. The C++ fixed void callback must translate failure into an exception; Python demonstrates a silently ignored failure and then its checked counterpart. The normal runner executes both demos.

## Fixtures And Evidence

The new CSV contains a header (required because both readers skip it) followed by five data rows: blank tag, blank member ID, int32 overflow, ASCII case mismatch, and reservation conflict. None duplicate the fixed fixture's failure cases. `my-expected-output.txt` was generated from the compiled C++ CLI, not handwritten; Python matches it exactly. Both suites assert all five messages and rejection counters; run_tests also checks exact CLI status 1. The original ten data rows and golden remain untouched.

Reproduce with `bash run_tests.sh` and `bash scripts/run_result_asan.sh`. The latter uses ASan leak detection and UBSan on every C++ suite, limits demo and both real CLI rejection fixtures, with non-PIE sanitizer binaries. Recorded results: 35 C++ suite cases plus 2 C++ demo cases, 111 Python suite cases plus 2 named Python demo assertions, both golden checks, and dependency gate pass. Sanitizers report no diagnostics. This validates exercised paths, not every possible allocation-failure guarantee of the existing service.

See `docs/evidence/result_full_run.txt`, `result_asan.txt`, `result_golden_generation.txt`, `result_changed_callsites.txt`, `result_callsites.txt`, `result_production_callsites.txt`, `result_diff_stat.txt` and `result_diff.patch`. The latter two are raw git snapshots against 5b26936, so Git omits untracked additions and includes the two pre-existing modified baseline evidence logs. `result_new_files.patch` separately captures task-created untracked files, excluding evidence itself and the unrelated untracked Modul 3.txt. No commits were made. PREDICTION.md and the dependency test were not edited.
