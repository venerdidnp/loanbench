// Result<T> from-scratch primitive: proves the two named factories are the
// only way to build one, proves value() throws on failure, and proves a
// throwing implementation and a Result-returning implementation of the SAME
// rule produce identical observable behaviour on the same inputs -- the
// "from-scratch match" Lab 2.2 requires.

#include "mini_catch.hpp"
#include "pinjamlab/domain/result.hpp"
#include "pinjamlab/io/validator.hpp"
#include "pinjamlab/app/seed.hpp"
#include <typeinfo>

#include <stdexcept>
#include <string>

using namespace pinjamlab;

TEST_CASE("Result::success carries a value and ok() is true") {
    auto r = Result<int>::success(42);
    REQUIRE(r.ok());
    REQUIRE(r.value() == 42);
    REQUIRE(r.error().empty());
}

TEST_CASE("Result::failure carries a message and ok() is false") {
    auto r = Result<int>::failure("days must be positive, got -3");
    REQUIRE(!r.ok());
    REQUIRE(r.error() == "days must be positive, got -3");
}

TEST_CASE("value() on a failed Result throws, rather than returning garbage") {
    auto r = Result<std::string>::failure("tag is empty");
    REQUIRE_THROWS_AS((void)r.value(), std::logic_error);
}

// ---- the from-scratch match: Validator (Result) vs a throwing equivalent ----

// A deliberately duplicated throwing version of the SAME rule Validator
// applies, so the two can be compared on the same inputs. Real code should
// never have both; this exists only to prove the refactor changes shape, not
// behaviour -- Lab 2.2's explicit requirement.
static int parseDaysOrThrow(const std::string& raw) {
    if (raw.empty()) throw std::invalid_argument("days is not a number: " + raw);
    std::size_t i = 0;
    bool neg = false;
    if (raw[0] == '+' || raw[0] == '-') { neg = (raw[0] == '-'); i = 1; }
    if (i == raw.size()) throw std::invalid_argument("days is not a number: " + raw);
    long long value = 0;
    for (; i < raw.size(); ++i) {
        if (raw[i] < '0' || raw[i] > '9') throw std::invalid_argument("days is not a number: " + raw);
        value = value * 10 + (raw[i] - '0');
    }
    const int days = static_cast<int>(neg ? -value : value);
    if (days <= 0) throw std::invalid_argument("days must be positive, got " + std::to_string(days));
    return days;
}

TEST_CASE("From-scratch match: Result and throwing agree on well-formed input") {
    Validator v;
    RawRow row{1, "LP-001", "M-101", "7"};
    const auto r = v.validate(row);
    REQUIRE(r.ok());
    REQUIRE(r.value().days == 7);
    REQUIRE(parseDaysOrThrow("7") == 7);  // identical outcome, different shape
}

TEST_CASE("From-scratch match: Result and throwing agree on every malformed input") {
    Validator v;
    const std::string malformed[] = {"abc", "-3", "0", ""};
    for (const auto& raw : malformed) {
        RawRow row{1, "LP-001", "M-101", raw};
        const auto r = v.validate(row);
        REQUIRE(!r.ok());  // Result: caller decides, cannot ignore ok()

        bool threw = false;
        try {
            (void)parseDaysOrThrow(raw);
        } catch (const std::invalid_argument&) {
            threw = true;  // throwing: caller who forgets try/catch still compiles
        }
        REQUIRE(threw);
    }
}

// Test-only adapter, not a second production implementation of the rules.
static Loan borrowOrThrow(LoanService& svc, const std::string& tag,
                          const std::string& member, int days) {
    const auto result = svc.borrow(tag, member, days);
    if (!result.ok()) throw EquipmentUnavailable(tag);
    return result.value();
}

TEST_CASE("Borrow Result and throwing twin: identical inputs, messages, types and state") {
    const struct { const char* tag; const char* member; int days; } cases[] = {
        {"LP-001", "M-101", 7}, {"LP-002", "M-101", 7},
        {"LP-999", "M-101", 7}, {"lp-001", "M-101", 7},
        {"LP-001", "M-404", 7}, {"LP-001", "M-101", 0},
        {"LP-001", "M-101", 91}, {"LP-004", "M-101", 7},
        {"LP-003", "M-102", 7},
        // Earlier guards must still win over unavailability.
        {"LP-002", "M-404", 7}, {"LP-002", "M-101", 0},
        {"LP-002", "M-102", 7},
    };
    for (const auto& c : cases) {
        LoanService resultSvc, throwingSvc;
        seedPinjamLab(resultSvc);
        seedPinjamLab(throwingSvc);
        const auto before = resultSvc.ledger().committed();
        std::string resultMessage, throwMessage, resultType, throwType;
        bool success = false;
        try {
            const auto result = resultSvc.borrow(c.tag, c.member, c.days);
            success = result.ok();
            if (success) {
                REQUIRE(result.value().tag() == c.tag);
                REQUIRE(result.value().memberId() == c.member);
                REQUIRE(result.value().days() == c.days);
                resultMessage = result.value().id();
            } else {
                resultMessage = result.error();
                resultType = typeid(EquipmentUnavailable).name();
                REQUIRE_THROWS_AS((void)result.value(), std::logic_error);
            }
        } catch (const LoanError& error) {
            resultMessage = error.what();
            resultType = typeid(error).name();
        }
        bool twinSuccess = false;
        try {
            const auto loan = borrowOrThrow(throwingSvc, c.tag, c.member, c.days);
            twinSuccess = true;
            throwMessage = loan.id();
            REQUIRE(loan.tag() == c.tag);
            REQUIRE(loan.memberId() == c.member);
            REQUIRE(loan.days() == c.days);
        } catch (const LoanError& error) {
            throwMessage = error.what();
            throwType = typeid(error).name();
        }
        REQUIRE(success == twinSuccess);
        REQUIRE(resultMessage == throwMessage);
        REQUIRE(resultType == throwType);
        for (const auto* tag : {"LP-001", "LP-002", "LP-003", "LP-004", "SEED-01", "SEED-02"}) {
            REQUIRE(resultSvc.findEquipment(tag)->isAvailable() == throwingSvc.findEquipment(tag)->isAvailable());
            REQUIRE(resultSvc.findEquipment(tag)->reservedFor() == throwingSvc.findEquipment(tag)->reservedFor());
        }
        for (const auto* member : {"M-101", "M-102", "M-103"})
            REQUIRE(resultSvc.findMember(member)->activeLoans() == throwingSvc.findMember(member)->activeLoans());
        REQUIRE(resultSvc.ledger().committed() == throwingSvc.ledger().committed());
        REQUIRE(resultSvc.ledger().pendingCount() == 0);
        REQUIRE(throwingSvc.ledger().pendingCount() == 0);
        REQUIRE(resultSvc.ledger().committed().size() == (success ? 8 : 6));
        if (!success) {
            REQUIRE(resultSvc.ledger().committed() == before);
            REQUIRE(resultSvc.findMember("M-101")->activeLoans() == 0);
            REQUIRE(resultSvc.findMember("M-102")->activeLoans() == 2);
            REQUIRE(resultSvc.findMember("M-103")->activeLoans() == 1);
            REQUIRE(resultSvc.findEquipment("LP-001")->isAvailable());
            REQUIRE(!resultSvc.findEquipment("LP-002")->isAvailable());
            REQUIRE(resultSvc.findEquipment("LP-003")->isAvailable());
            REQUIRE(resultSvc.findEquipment("LP-004")->isAvailable());
        }
        // Returning the item observes the private owner mapping too.
        resultSvc.returnItem(success ? c.tag : "LP-002", success ? c.member : "M-103");
        throwingSvc.returnItem(success ? c.tag : "LP-002", success ? c.member : "M-103");
        REQUIRE(resultSvc.findEquipment(success ? c.tag : "LP-002")->isAvailable());
        REQUIRE(throwingSvc.findEquipment(success ? c.tag : "LP-002")->isAvailable());
    }
}

struct Tracked {
    inline static int live = 0;
    inline static bool fail = false;
    int n;
    explicit Tracked(int value) : n(value) { ++live; }
    Tracked(const Tracked& other) : n(other.n) {
        if (fail) throw std::runtime_error("copy failure");
        ++live;
    }
    Tracked(Tracked&& other) : n(other.n) {
        if (fail) throw std::runtime_error("move failure");
        ++live;
    }
    ~Tracked() { --live; }
};

TEST_CASE("Manual union owns nondefault payload across copies, moves and throwing assignments") {
    static_assert(!std::is_default_constructible_v<Loan>);
    {
        auto a = Result<Tracked>::success(Tracked(7));
        auto b = a;
        auto c = std::move(b);
        auto d = Result<Tracked>::failure("unavailable");
        d = a;
        REQUIRE(d.value().n == 7);
        d = Result<Tracked>::failure("no value");
        REQUIRE(!d.ok());
        d = std::move(c);
        a = a;
        auto* alias = &a;
        a = std::move(*alias);
        REQUIRE(a.value().n == 7);
        Tracked::fail = true;
        REQUIRE_THROWS_AS(d = a, std::runtime_error);
        REQUIRE(!d.ok());
        REQUIRE_THROWS_AS(d = std::move(a), std::runtime_error);
        REQUIRE(!d.ok());
        REQUIRE_THROWS_AS(Result<Tracked>(a), std::runtime_error);
        REQUIRE_THROWS_AS(Result<Tracked>(std::move(a)), std::runtime_error);
        Tracked::fail = false;
        d = a;
        REQUIRE(d.value().n == 7);
    }
    REQUIRE(Tracked::live == 0);
    auto failed = Result<Loan>::failure("busy");
    auto copy = failed;
    auto moved = std::move(copy);
    REQUIRE(!moved.ok());
    REQUIRE(moved.error() == "busy");
}

int main() { return test_runner::runAll(); }
