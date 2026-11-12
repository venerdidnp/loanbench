// Proves TxnGuard releases (rolls back) on EVERY exit path, including the
// throwing one -- Lab 2.3's explicit requirement: "a test that throws inside
// the guarded region and asserts the resource was released."

#include "mini_catch.hpp"
#include "pinjamlab/service/database.hpp"
#include "pinjamlab/service/loan_service.hpp"
#include "pinjamlab/service/txn_guard.hpp"

#include <stdexcept>

using namespace pinjamlab;

TEST_CASE("TxnGuard commits: staged records become committed") {
    Database db;
    {
        TxnGuard txn(db);
        db.stage("a");
        db.stage("b");
        txn.commit();
    }
    REQUIRE(db.committed().size() == 2);
    REQUIRE(db.pendingCount() == 0);
}

TEST_CASE("TxnGuard rolls back on normal scope exit without commit()") {
    Database db;
    {
        TxnGuard txn(db);
        db.stage("never committed");
        // txn destructs here WITHOUT commit() having been called.
    }
    REQUIRE(db.committed().empty());
    REQUIRE(db.pendingCount() == 0);  // rollback cleared the staged record
}

TEST_CASE("TxnGuard rolls back when an exception unwinds through it") {
    Database db;
    bool caught = false;
    try {
        TxnGuard txn(db);
        db.stage("about to be abandoned");
        throw std::runtime_error("simulated failure mid-transaction");
        txn.commit();  // unreachable; proves the guard, not this line, cleans up
    } catch (const std::runtime_error&) {
        caught = true;
    }
    REQUIRE(caught);
    REQUIRE(db.committed().empty());  // the throwing path released, exactly
    REQUIRE(db.pendingCount() == 0);  // like the normal exit path above
}

TEST_CASE("LoanService.borrow() commits the ledger on success") {
    // Integration: the guard is not just testable in isolation, it is wired
    // into the real orchestration.
    LoanService svc;
    svc.addEquipment(Equipment("LP-001", "ThinkPad T14"));
    svc.addMember(Member("M-101", "Ayu Lestari", Role::Student));
    (void)svc.borrow("LP-001", "M-101", 7);
    REQUIRE(svc.ledger().committed().size() == 2);  // "loan:" and "equipment:" records
}

int main() { return test_runner::runAll(); }
