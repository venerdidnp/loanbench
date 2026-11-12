#ifndef PINJAMLAB_IO_VALIDATOR_HPP
#define PINJAMLAB_IO_VALIDATOR_HPP
#include "pinjamlab/domain/result.hpp"
#include "pinjamlab/io/csv_reader.hpp"
#include <cstdint>
#include <string>
namespace pinjamlab {
struct LoanRequest { std::string tag; std::string memberId; int days; };
class Validator {
public:
    [[nodiscard]] Result<LoanRequest> validate(const RawRow& row) const {
        if (row.tag.empty()) return Result<LoanRequest>::failure("tag is empty");
        if (row.memberId.empty()) return Result<LoanRequest>::failure("memberId is empty");
        if (row.tag.find_first_not_of(" \t\r\n\v\f") == std::string::npos)
            return Result<LoanRequest>::failure("tag is blank");
        if (row.memberId.find_first_not_of(" \t\r\n\v\f") == std::string::npos)
            return Result<LoanRequest>::failure("memberId is blank");
        const auto& raw = row.daysRaw;
        std::size_t start = 0;
        const bool negative = !raw.empty() && raw[0] == '-';
        if (!raw.empty() && (raw[0] == '+' || raw[0] == '-')) start = 1;
        if (start == raw.size() || raw.find_first_not_of("0123456789", start) != std::string::npos)
            return Result<LoanRequest>::failure("days is not a number: " + raw);
        // Check before multiplying so arbitrarily long input cannot overflow.
        const std::uint32_t limit = negative ? 2147483648u : 2147483647u;
        std::uint32_t magnitude = 0;
        for (std::size_t i = start; i < raw.size(); ++i) {
            const auto digit = static_cast<std::uint32_t>(raw[i] - '0');
            if (magnitude > (limit - digit) / 10)
                return Result<LoanRequest>::failure("days is out of range: " + raw);
            magnitude = magnitude * 10 + digit;
        }
        const int days = static_cast<int>(negative ? -static_cast<std::int64_t>(magnitude)
                                                   : static_cast<std::int64_t>(magnitude));
        if (days <= 0)
            return Result<LoanRequest>::failure("days must be positive, got " + std::to_string(days));
        return Result<LoanRequest>::success(LoanRequest{row.tag, row.memberId, days});
    }
};
}  // namespace pinjamlab
#endif
