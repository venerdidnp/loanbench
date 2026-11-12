#ifndef PINJAMLAB_APP_RUNNER_HPP
#define PINJAMLAB_APP_RUNNER_HPP

// app layer: the top-level handler. This is the ONE place in the codebase
// allowed to catch `const LoanError&` and turn it into a message a human
// reads, and the ONE place that decides the process exit code. It contains
// no business rules of its own.

#include "pinjamlab/domain/loan_error.hpp"
#include "pinjamlab/io/csv_reader.hpp"
#include "pinjamlab/io/report_writer.hpp"
#include "pinjamlab/io/validator.hpp"
#include "pinjamlab/service/loan_service.hpp"

#include <string>
#include <vector>

namespace pinjamlab {

struct RunResult {
    std::vector<std::string> rejectedLines;  // exactly what expected-output.txt holds
    int total = 0;
    int created = 0;
    int rejected = 0;
    [[nodiscard]] int exitCode() const noexcept { return rejected == 0 ? 0 : 1; }
};

// Pure of console I/O on purpose: returns the lines instead of printing them,
// so both the CLI (main.cpp) and the tests (test_app.cpp) can drive the same
// code path -- one prints to stderr, the other diffs against a golden file.
[[nodiscard]] inline RunResult runCatalogue(LoanService& svc, const std::string& csvPath) {
    CsvReader reader;
    Validator validator;
    RunResult result;

    const auto rows = reader.read(csvPath);
    result.total = static_cast<int>(rows.size());

    for (const auto& row : rows) {
        const auto validated = validator.validate(row);
        if (!validated.ok()) {
            ++result.rejected;
            result.rejectedLines.push_back(
                ReportWriter::rejectedLine(row.lineNumber, validated.error()));
            continue;
        }
        const auto& req = validated.value();
        try {
            const auto borrowed = svc.borrow(req.tag, req.memberId, req.days);
            if (!borrowed.ok()) {
                ++result.rejected;
                result.rejectedLines.push_back(
                    ReportWriter::rejectedLine(row.lineNumber, borrowed.error()));
                continue;
            }
            ++result.created;
        } catch (const AssetTagCaseMismatch& e) {
            ++result.rejected;
            result.rejectedLines.push_back(ReportWriter::rejectedLine(
                row.lineNumber, "Unknown asset tag: " + e.given() +
                " (did you mean " + e.suggestion() + "?)"));
        } catch (const LoanError& e) {  // the family we understand
            ++result.rejected;
            result.rejectedLines.push_back(
                ReportWriter::rejectedLine(row.lineNumber, e.what()));
        }
        // Anything that is NOT a LoanError is left to travel: we do not know
        // what it is, so we are not entitled to decide it is unimportant.
    }
    return result;
}

}  // namespace pinjamlab

#endif  // PINJAMLAB_APP_RUNNER_HPP
