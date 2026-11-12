#ifndef PINJAMLAB_DOMAIN_LOAN_ERROR_HPP
#define PINJAMLAB_DOMAIN_LOAN_ERROR_HPP
#include <stdexcept>
#include <string>
#include <utility>
namespace pinjamlab {
class LoanError : public std::runtime_error {
public:
    explicit LoanError(const std::string& msg) : std::runtime_error(msg) {}
};
class UnknownAssetTag : public LoanError {
    std::string tag_;
protected:
    UnknownAssetTag(std::string tag, const std::string& message)
        : LoanError(message), tag_(std::move(tag)) {}
public:
    explicit UnknownAssetTag(std::string tag)
        : LoanError("Unknown asset tag: " + tag), tag_(std::move(tag)) {}
    [[nodiscard]] const std::string& tag() const noexcept { return tag_; }
};
class AssetTagCaseMismatch : public UnknownAssetTag {
    std::string suggestion_;
public:
    AssetTagCaseMismatch(std::string given, std::string suggestion)
        : UnknownAssetTag(given, "Unknown asset tag: " + given +
                          " (did you mean " + suggestion + "?)"),
          suggestion_(std::move(suggestion)) {}
    [[nodiscard]] const std::string& given() const noexcept { return tag(); }
    [[nodiscard]] const std::string& suggestion() const noexcept { return suggestion_; }
};
class ReservationConflict : public LoanError {
    std::string tag_, reservedFor_;
public:
    ReservationConflict(std::string tag, std::string reservedFor)
        : LoanError("Equipment reserved: " + tag + " for " + reservedFor),
          tag_(std::move(tag)), reservedFor_(std::move(reservedFor)) {}
    [[nodiscard]] const std::string& tag() const noexcept { return tag_; }
    [[nodiscard]] const std::string& reservedFor() const noexcept { return reservedFor_; }
};
class UnknownMember : public LoanError {
    std::string memberId_;
public:
    explicit UnknownMember(std::string memberId)
        : LoanError("Unknown member: " + memberId), memberId_(std::move(memberId)) {}
    [[nodiscard]] const std::string& memberId() const noexcept { return memberId_; }
};
class InvalidLoanDuration : public LoanError {
    int days_, maxDays_;
public:
    InvalidLoanDuration(int days, int maxDays)
        : LoanError("Loan duration exceeds maximum: " + std::to_string(days) + " > " + std::to_string(maxDays)),
          days_(days), maxDays_(maxDays) {}
    [[nodiscard]] int days() const noexcept { return days_; }
    [[nodiscard]] int maxDays() const noexcept { return maxDays_; }
};
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
        : LoanError("Loan quota exceeded: " + std::to_string(active) + " active, limit " + std::to_string(limit)),
          active_(active), limit_(limit) {}
    [[nodiscard]] int active() const noexcept { return active_; }
    [[nodiscard]] int limit() const noexcept { return limit_; }
};
}  // namespace pinjamlab
#endif
