#ifndef PINJAMLAB_DOMAIN_LOAN_HPP
#define PINJAMLAB_DOMAIN_LOAN_HPP

// PURE domain header: the record produced by a successful borrow().

#include <string>
#include <utility>

namespace pinjamlab {

class Loan {
    std::string id_;
    std::string tag_;
    std::string memberId_;
    int days_;

public:
    Loan(std::string id, std::string tag, std::string memberId, int days)
        : id_(std::move(id)), tag_(std::move(tag)),
          memberId_(std::move(memberId)), days_(days) {}

    [[nodiscard]] const std::string& id() const noexcept { return id_; }
    [[nodiscard]] const std::string& tag() const noexcept { return tag_; }
    [[nodiscard]] const std::string& memberId() const noexcept { return memberId_; }
    [[nodiscard]] int days() const noexcept { return days_; }
};

}  // namespace pinjamlab

#endif  // PINJAMLAB_DOMAIN_LOAN_HPP
