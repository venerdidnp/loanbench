#ifndef PINJAMLAB_SERVICE_LOAN_SERVICE_HPP
#define PINJAMLAB_SERVICE_LOAN_SERVICE_HPP

// Orchestration only: LoanService coordinates domain objects and raises the
// domain's own typed exceptions. It contains no CSV parsing, no console
// output, and no formatting -- those belong to io/ and app/.

#include "pinjamlab/domain/equipment.hpp"
#include "pinjamlab/domain/loan.hpp"
#include "pinjamlab/domain/loan_error.hpp"
#include "pinjamlab/domain/member.hpp"
#include "pinjamlab/service/database.hpp"
#include "pinjamlab/service/txn_guard.hpp"

#include <string>
#include <unordered_map>

namespace pinjamlab {

class LoanService {
public:
    static constexpr int kMaxLoanDays = 90;

    void addEquipment(Equipment eq) {
        catalog_.emplace(eq.tag(), std::move(eq));
    }
    void addMember(Member m) {
        roster_.emplace(m.id(), std::move(m));
    }

    [[nodiscard]] Equipment* findEquipment(const std::string& tag) {
        auto it = catalog_.find(tag);
        return it == catalog_.end() ? nullptr : &it->second;
    }
    [[nodiscard]] Member* findMember(const std::string& id) {
        auto it = roster_.find(id);
        return it == roster_.end() ? nullptr : &it->second;
    }

    // The failure cascade, guard by guard. Every check below happens BEFORE
    // any mutation, so no rollback is ever needed for the current guard set
    // -- the TxnGuard exists for the mutation step itself, to keep the
    // pattern honest for the day a guard is added AFTER a mutation begins
    // (Module 5's database transactions are exactly that day).
    [[nodiscard]] Loan borrow(const std::string& tag, const std::string& memberId, int days) {
        auto eqIt = catalog_.find(tag);
        if (eqIt == catalog_.end()) throw UnknownAssetTag(tag);

        auto memIt = roster_.find(memberId);
        if (memIt == roster_.end()) throw UnknownMember(memberId);

        if (days > kMaxLoanDays) throw InvalidLoanDuration(days, kMaxLoanDays);

        Equipment& eq = eqIt->second;
        Member& mem = memIt->second;

        if (!eq.isAvailable()) throw EquipmentUnavailable(tag);
        if (!mem.canBorrow()) throw QuotaExceeded(mem.activeLoans(), mem.maxLoans());

        TxnGuard txn(db_);
        mem.recordLoan();
        db_.stage("loan:" + memberId + ":" + tag);
        try {
            eq.markLoaned();
        } catch (...) {
            mem.undoRecordLoan();  // manual compensation: txn.commit() was
            throw;                 // never called, so the guard still rolls
        }                          // back the LEDGER on the way out.
        db_.stage("equipment:" + tag + ":loaned");
        txn.commit();

        return Loan("L-" + tag + "-" + memberId, tag, memberId, days);
    }

    void returnItem(const std::string& loanTag, const std::string& memberId) {
        auto eqIt = catalog_.find(loanTag);
        auto memIt = roster_.find(memberId);
        if (eqIt != catalog_.end()) eqIt->second.markReturned();
        if (memIt != roster_.end()) memIt->second.recordReturn();
    }

    [[nodiscard]] const Database& ledger() const noexcept { return db_; }

private:
    std::unordered_map<std::string, Equipment> catalog_;
    std::unordered_map<std::string, Member> roster_;
    Database db_;
};

}  // namespace pinjamlab

#endif  // PINJAMLAB_SERVICE_LOAN_SERVICE_HPP
