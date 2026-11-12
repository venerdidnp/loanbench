#ifndef PINJAMLAB_DOMAIN_LOAN_ERROR_HPP
#define PINJAMLAB_DOMAIN_LOAN_ERROR_HPP

// PURE domain header: no console output, no file streams, no text formats.
// The dependency-rule grep in run_tests.sh checks this file (and its
// siblings in domain/) for exactly those tokens.

#include <stdexcept>
#include <string>

namespace pinjamlab {

// Base for every PinjamLab loan failure. Catching `const LoanError&` catches
// the whole family; catching a concrete subclass catches one failure mode.
class LoanError : public std::runtime_error {
public:
    explicit LoanError(const std::string& msg) : std::runtime_error(msg) {}
};

class UnknownAssetTag : public LoanError {
    std::string tag_;
public:
    explicit UnknownAssetTag(std::string tag)
        : LoanError("Unknown asset tag: " + tag), tag_(std::move(tag)) {}
    [[nodiscard]] const std::string& tag() const noexcept { return tag_; }
};

class UnknownMember : public LoanError {
    std::string memberId_;
public:
    explicit UnknownMember(std::string memberId)
        : LoanError("Unknown member: " + memberId), memberId_(std::move(memberId)) {}
    [[nodiscard]] const std::string& memberId() const noexcept { return memberId_; }
};

// A business-rule violation on duration: the request was well-FORMED (the io
// layer already confirmed `days` parses and is positive) but exceeds the
// policy maximum. That distinction is why this is a domain exception and
// "days is not a number" / "days must be positive" are io-layer Result
// errors instead -- see io/validator.hpp.
class InvalidLoanDuration : public LoanError {
    int days_, maxDays_;
public:
    InvalidLoanDuration(int days, int maxDays)
        : LoanError("Loan duration exceeds maximum: " + std::to_string(days) +
                    " > " + std::to_string(maxDays)),
          days_(days), maxDays_(maxDays) {}
    [[nodiscard]] int days() const noexcept { return days_; }
    [[nodiscard]] int maxDays() const noexcept { return maxDays_; }
};

// Guard 3 of the failure cascade: an ORDINARY, expected outcome (a popular
// laptop being on loan is normal), modelled as an exception here because the
// worked case study routes it to `service`. Lab 3.1 asks you to defend, with
// a written prediction, whether it should be a Result instead.
class EquipmentUnavailable : public LoanError {
    std::string tag_;
public:
    explicit EquipmentUnavailable(std::string tag)
        : LoanError("Equipment already on loan: " + tag), tag_(std::move(tag)) {}
    [[nodiscard]] const std::string& tag() const noexcept { return tag_; }
};

class QuotaExceeded : public LoanError {
    int active_, limit_;
public:
    QuotaExceeded(int active, int limit)
        : LoanError("Loan quota exceeded: " + std::to_string(active) +
                    " active, limit " + std::to_string(limit)),
          active_(active), limit_(limit) {}
    // The handler can DO something with these -- that is why the class exists,
    // rather than just a better string.
    [[nodiscard]] int active() const noexcept { return active_; }
    [[nodiscard]] int limit() const noexcept { return limit_; }
};

}  // namespace pinjamlab

#endif  // PINJAMLAB_DOMAIN_LOAN_ERROR_HPP
