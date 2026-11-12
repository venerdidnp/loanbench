#ifndef PINJAMLAB_DOMAIN_MEMBER_HPP
#define PINJAMLAB_DOMAIN_MEMBER_HPP

// PURE domain header: entity carried forward from Module 1, unchanged in
// shape. What is new in Module 3 is that recordLoan() now throws a TYPED
// QuotaExceeded instead of the generic std::runtime_error Module 1 used.

#include "pinjamlab/domain/loan_error.hpp"

#include <string>
#include <utility>

namespace pinjamlab {

enum class Role { Student = 2, Faculty = 5, Staff = 3 };

class Member {
    std::string id_;
    std::string name_;
    Role role_;
    int activeLoans_ = 0;

public:
    Member(std::string id, std::string name, Role role)
        : id_(std::move(id)), name_(std::move(name)), role_(role) {}

    [[nodiscard]] const std::string& id() const noexcept { return id_; }
    [[nodiscard]] const std::string& name() const noexcept { return name_; }
    [[nodiscard]] int maxLoans() const noexcept { return static_cast<int>(role_); }
    [[nodiscard]] int activeLoans() const noexcept { return activeLoans_; }
    [[nodiscard]] bool canBorrow() const noexcept { return activeLoans_ < maxLoans(); }

    void recordLoan() {
        if (!canBorrow()) throw QuotaExceeded(activeLoans_, maxLoans());
        ++activeLoans_;
    }

    void recordReturn() {
        if (activeLoans_ > 0) --activeLoans_;
    }

    // Used only by TxnGuard's rollback path (service/database.hpp) to undo a
    // recordLoan() that was staged but never committed.
    void undoRecordLoan() {
        if (activeLoans_ > 0) --activeLoans_;
    }
};

}  // namespace pinjamlab

#endif  // PINJAMLAB_DOMAIN_MEMBER_HPP
