#ifndef PINJAMLAB_SERVICE_TXN_GUARD_HPP
#define PINJAMLAB_SERVICE_TXN_GUARD_HPP

// From-scratch primitive: an RAII transaction guard. The constructor
// acquires (begin()); the destructor releases (rollback()) UNLESS commit()
// was called first. That pairing is RAII, and it is what makes borrow()
// exception-safe with zero try/catch of its own -- Figure "Stack Unwinding"
// is doing the actual work; this class only wires it to a resource.

#include "pinjamlab/service/database.hpp"

#include <iostream>

namespace pinjamlab {

class TxnGuard {
    Database& db_;
    bool committed_ = false;

public:
    explicit TxnGuard(Database& db) : db_(db) { db_.begin(); }  // acquire

    // Rule of Five: a guard must not be copied -- two guards, one transaction.
    TxnGuard(const TxnGuard&) = delete;
    TxnGuard& operator=(const TxnGuard&) = delete;
    TxnGuard(TxnGuard&&) = delete;
    TxnGuard& operator=(TxnGuard&&) = delete;

    void commit() {
        db_.commit();
        committed_ = true;
    }

    ~TxnGuard() noexcept {  // noexcept: destructors must NOT throw
        if (committed_) return;
        try {
            db_.rollback();  // released on EVERY path that did not commit
        } catch (...) {
            // Swallowing is correct HERE and almost nowhere else: throwing
            // from a destructor during unwinding calls std::terminate().
            std::cerr << "rollback failed during unwind\n";
        }
    }
};

}  // namespace pinjamlab

#endif  // PINJAMLAB_SERVICE_TXN_GUARD_HPP
