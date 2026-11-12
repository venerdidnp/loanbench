#ifndef PINJAMLAB_IO_VALIDATOR_HPP
#define PINJAMLAB_IO_VALIDATOR_HPP

// io layer: converts a RawRow into a Result<LoanRequest>. Format failures
// (empty fields, unparseable or non-positive numbers) are rejected HERE,
// with plain string errors -- they never reach domain, and domain never
// sees a request that could not possibly be valid. This is the boundary
// Figure "The Failure Cascade" calls guard 2.

#include "pinjamlab/domain/result.hpp"
#include "pinjamlab/io/csv_reader.hpp"

#include <string>

namespace pinjamlab {

struct LoanRequest {
    std::string tag;
    std::string memberId;
    int days;
};

class Validator {
public:
    [[nodiscard]] Result<LoanRequest> validate(const RawRow& row) const {
        if (row.tag.empty()) return Result<LoanRequest>::failure("tag is empty");
        if (row.memberId.empty()) return Result<LoanRequest>::failure("memberId is empty");

        int days = 0;
        if (!parseInt(row.daysRaw, days)) {
            return Result<LoanRequest>::failure("days is not a number: " + row.daysRaw);
        }
        if (days <= 0) {
            return Result<LoanRequest>::failure(
                "days must be positive, got " + std::to_string(days));
        }
        return Result<LoanRequest>::success(LoanRequest{row.tag, row.memberId, days});
    }

private:
    // A hand-rolled parse rather than std::stoi: stoi accepts a LEADING
    // numeric prefix ("7abc" -> 7) and silently ignores the rest, which
    // would misclassify row 3 ("abc") only by accident of no leading digit.
    // Reject anything that is not ENTIRELY digits (with an optional sign).
    [[nodiscard]] static bool parseInt(const std::string& s, int& out) {
        if (s.empty()) return false;
        std::size_t i = 0;
        bool neg = false;
        if (s[0] == '+' || s[0] == '-') { neg = (s[0] == '-'); i = 1; }
        if (i == s.size()) return false;
        long long value = 0;
        for (; i < s.size(); ++i) {
            if (s[i] < '0' || s[i] > '9') return false;
            value = value * 10 + (s[i] - '0');
        }
        out = static_cast<int>(neg ? -value : value);
        return true;
    }
};

}  // namespace pinjamlab

#endif  // PINJAMLAB_IO_VALIDATOR_HPP
