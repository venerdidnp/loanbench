// One test per failure mode in the LoanError hierarchy, plus the catch-order
// and catch-precision guarantees the module's Figure "Hierarchy" promises.

#include "mini_catch.hpp"
#include "pinjamlab/app/seed.hpp"
#include "pinjamlab/service/loan_service.hpp"

using namespace pinjamlab;

static LoanService seeded() {
    LoanService svc;
    seedPinjamLab(svc);
    return svc;
}

TEST_CASE("UnknownAssetTag: unknown tag, carries the tag") {
    LoanService svc = seeded();
    try {
        (void)svc.borrow("LP-999", "M-101", 7);
        REQUIRE(false);  // must not reach here
    } catch (const UnknownAssetTag& e) {
        REQUIRE(e.tag() == "LP-999");
        REQUIRE(std::string(e.what()) == "Unknown asset tag: LP-999");
    }
}

TEST_CASE("UnknownMember: unknown member, carries the id") {
    LoanService svc = seeded();
    try {
        (void)svc.borrow("LP-001", "M-404", 7);
        REQUIRE(false);
    } catch (const UnknownMember& e) {
        REQUIRE(e.memberId() == "M-404");
    }
}

TEST_CASE("InvalidLoanDuration: business-rule maximum, not the format check") {
    LoanService svc = seeded();
    try {
        (void)svc.borrow("LP-001", "M-101", 400);
        REQUIRE(false);
    } catch (const InvalidLoanDuration& e) {
        REQUIRE(e.days() == 400);
        REQUIRE(e.maxDays() == 90);
        REQUIRE(std::string(e.what()) == "Loan duration exceeds maximum: 400 > 90");
    }
}

TEST_CASE("EquipmentUnavailable: already on loan returns the same message") {
    LoanService svc = seeded();  // LP-002 was loaned to M-103 during seeding
    const auto result = svc.borrow("LP-002", "M-101", 7);
    REQUIRE(!result.ok());
    REQUIRE(result.error() == EquipmentUnavailable("LP-002").what());
}

TEST_CASE("QuotaExceeded: over quota, carries active and limit") {
    LoanService svc = seeded();  // M-102 was seeded to exactly 2/2
    try {
        (void)svc.borrow("LP-003", "M-102", 7);
        REQUIRE(false);
    } catch (const QuotaExceeded& e) {
        REQUIRE(e.active() == 2);
        REQUIRE(e.limit() == 2);
    }
}

TEST_CASE("Remaining thrown service errors are catchable as LoanError") {
    LoanService svc = seeded();
    int caughtAsFamily = 0;
    const struct { const char* tag; const char* member; int days; } cases[] = {
        {"LP-999", "M-101", 7}, {"LP-001", "M-404", 7}, {"LP-001", "M-101", 400},
        {"LP-003", "M-102", 7},
    };
    for (const auto& c : cases) {
        try {
            (void)svc.borrow(c.tag, c.member, c.days);
        } catch (const LoanError&) {
            ++caughtAsFamily;
        }
    }
    REQUIRE(caughtAsFamily == 4);
}

TEST_CASE("Catch order: most-specific handler runs when listed first") {
    // Mirrors the module's warning that catch (LoanError&) above
    // catch (QuotaExceeded&) makes the second one unreachable -- this test
    // proves the CORRECT order (specific first) actually dispatches specific.
    LoanService svc = seeded();
    bool sawQuotaExceeded = false;
    bool sawGenericLoanError = false;
    try {
        (void)svc.borrow("LP-003", "M-102", 7);
    } catch (const QuotaExceeded&) {
        sawQuotaExceeded = true;
    } catch (const LoanError&) {
        sawGenericLoanError = true;
    }
    REQUIRE(sawQuotaExceeded);
    REQUIRE(!sawGenericLoanError);
}

TEST_CASE("A successful borrow raises nothing and updates both entities") {
    LoanService svc = seeded();
    const auto result = svc.borrow("LP-001", "M-101", 7);
    REQUIRE(result.ok());
    const Loan& loan = result.value();
    REQUIRE(loan.tag() == "LP-001");
    REQUIRE(loan.memberId() == "M-101");
    REQUIRE(svc.findEquipment("LP-001")->isAvailable() == false);
    REQUIRE(svc.findMember("M-101")->activeLoans() == 1);
}

int main() { return test_runner::runAll(); }
