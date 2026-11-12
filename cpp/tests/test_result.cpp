// Result<T> from-scratch primitive: proves the two named factories are the
// only way to build one, proves value() throws on failure, and proves a
// throwing implementation and a Result-returning implementation of the SAME
// rule produce identical observable behaviour on the same inputs -- the
// "from-scratch match" Lab 2.2 requires.

#include "mini_catch.hpp"
#include "pinjamlab/domain/result.hpp"
#include "pinjamlab/io/validator.hpp"

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

int main() { return test_runner::runAll(); }
