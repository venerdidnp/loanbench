#include "mini_catch.hpp"
#include "pinjamlab/app/runner.hpp"
#include "pinjamlab/app/seed.hpp"
#include <filesystem>
#include <fstream>
#include <iterator>
#include <type_traits>

using namespace pinjamlab;
namespace fs = std::filesystem;

// A scoped directory also isolates parallel test processes.
struct TestDirectory {
    fs::path path;
    TestDirectory() {
        std::string pattern = (fs::temp_directory_path() / "loanbench-tests-XXXXXX").string();
        if (!::mkdtemp(pattern.data())) throw std::runtime_error("cannot create test directory");
        path = pattern;
    }
    ~TestDirectory() noexcept { std::error_code ec; fs::remove_all(path, ec); }
};
static std::string contents(const fs::path& path) {
    std::ifstream input(path, std::ios::binary);
    return {std::istreambuf_iterator<char>(input), std::istreambuf_iterator<char>()};
}

TEST_CASE("Case mismatch fields, exact message, and both catch families") {
    LoanService svc;
    seedPinjamLab(svc);
    try {
        (void)svc.borrow("lp-001", "M-101", 7);
        REQUIRE(false);
    } catch (const AssetTagCaseMismatch& e) {
        REQUIRE(e.given() == "lp-001");
        REQUIRE(e.tag() == e.given());
        REQUIRE(e.suggestion() == "LP-001");
        REQUIRE(std::string(e.what()) == "Unknown asset tag: lp-001 (did you mean LP-001?)");
    } catch (const UnknownAssetTag&) {
        REQUIRE(false);
    }
    REQUIRE_THROWS_AS((void)svc.borrow("lp-001", "M-101", 7), UnknownAssetTag);
    REQUIRE_THROWS_AS((void)svc.borrow("lp-001", "M-101", 7), LoanError);
    REQUIRE(svc.findEquipment("LP-001")->isAvailable());
}

TEST_CASE("Reservation fields, family, allowed holder, and empty sentinel") {
    LoanService svc;
    seedPinjamLab(svc);
    REQUIRE(svc.findEquipment("LP-001")->reservedFor().empty());
    REQUIRE(svc.findEquipment("LP-004")->reservedFor() == "M-103");
    try {
        (void)svc.borrow("LP-004", "M-101", 7);
        REQUIRE(false);
    } catch (const ReservationConflict& e) {
        REQUIRE(e.tag() == "LP-004");
        REQUIRE(e.reservedFor() == "M-103");
        REQUIRE(std::string(e.what()) == "Equipment reserved: LP-004 for M-103");
    }
    REQUIRE_THROWS_AS((void)svc.borrow("LP-004", "M-101", 7), LoanError);
    REQUIRE(svc.findMember("M-101")->activeLoans() == 0);
    const auto result = svc.borrow("LP-004", "M-103", 7);
    REQUIRE(result.ok());
    REQUIRE(result.value().memberId() == "M-103");
}

TEST_CASE("Validator distinguishes blank fields while preserving empty errors") {
    Validator validator;
    REQUIRE(validator.validate({1, " \t\r\n\v\f", "M-101", "7"}).error() == "tag is blank");
    REQUIRE(validator.validate({1, "LP-001", " \t\r\n\v\f", "7"}).error() == "memberId is blank");
    REQUIRE(validator.validate({1, "", "M-101", "7"}).error() == "tag is empty");
    REQUIRE(validator.validate({1, "LP-001", "", "7"}).error() == "memberId is empty");
}

TEST_CASE("Days accepts only signed ASCII digits and checks int32 bounds") {
    Validator validator;
    const std::string malformed[] = {"", "+", "-", " 7", "7 ", "7\t", "1_0", "7abc", "++7", "\xd9\xa7", "999999999999999999999x"};
    for (const auto& raw : malformed)
        REQUIRE(validator.validate({1, "LP-001", "M-101", raw}).error() == "days is not a number: " + raw);
    const std::string overflow[] = {"2147483648", "+2147483648", "-2147483649", std::string(1000, '9')};
    for (const auto& raw : overflow)
        REQUIRE(validator.validate({1, "LP-001", "M-101", raw}).error() == "days is out of range: " + raw);
    REQUIRE(validator.validate({1, "LP-001", "M-101", "2147483647"}).value().days == 2147483647);
    REQUIRE(validator.validate({1, "LP-001", "M-101", "-2147483648"}).error() == "days must be positive, got -2147483648");
    REQUIRE(validator.validate({1, "LP-001", "M-101", "+007"}).value().days == 7);
    REQUIRE(validator.validate({1, "LP-001", "M-101", "-0"}).error() == "days must be positive, got 0");
}

TEST_CASE("CRLF reader counts blank physical data lines and app dispatches handlers") {
    TestDirectory dir;
    const auto csv = dir.path / "input.csv";
    { std::ofstream out(csv, std::ios::binary);
      out << "tag,member_id,days\r\n\r\nlp-001,M-101,7\r\n\nLP-004,M-101,7\r\nLP-001,M-101,+7\r\n"; }
    const auto rows = CsvReader().read(csv.string());
    REQUIRE(rows.size() == 3);
    REQUIRE(rows[0].lineNumber == 2);
    REQUIRE(rows[1].lineNumber == 4);
    REQUIRE(rows[2].lineNumber == 5);
    REQUIRE(rows[2].daysRaw == "+7");
    LoanService svc;
    seedPinjamLab(svc);
    const auto result = runCatalogue(svc, csv.string());
    REQUIRE(result.total == 3);
    REQUIRE(result.created == 1);
    REQUIRE(result.rejected == 2);
    REQUIRE(result.rejectedLines[0] == "row 2: Unknown asset tag: lp-001 (did you mean LP-001?)");
    REQUIRE(result.rejectedLines[1] == "row 4: Equipment reserved: LP-004 for M-103");
}

TEST_CASE("Duplicate equipment throws logic_error and preserves original") {
    LoanService svc;
    svc.addEquipment(Equipment("LP-001", "Original"));
    REQUIRE_THROWS_AS(svc.addEquipment(Equipment("LP-001", "Replacement")), std::logic_error);
    REQUIRE(svc.findEquipment("LP-001")->model() == "Original");
}

TEST_CASE("Returns reject invalid requests before mutation and succeed once") {
    LoanService svc;
    seedPinjamLab(svc);
    REQUIRE_THROWS_AS(svc.returnItem("LP-999", "M-103"), UnknownAssetTag);
    REQUIRE_THROWS_AS(svc.returnItem("LP-002", "M-404"), UnknownMember);
    REQUIRE_THROWS_AS(svc.returnItem("LP-001", "M-103"), LoanError);
    REQUIRE(!svc.findEquipment("LP-002")->isAvailable());
    REQUIRE(svc.findMember("M-103")->activeLoans() == 1);
    svc.returnItem("LP-002", "M-103");
    REQUIRE(svc.findEquipment("LP-002")->isAvailable());
    REQUIRE(svc.findMember("M-103")->activeLoans() == 0);
    REQUIRE_THROWS_AS(svc.returnItem("LP-002", "M-103"), LoanError);
}

TEST_CASE("Report commit atomically replaces destination and removes unique same-dir temporary") {
    static_assert(std::is_nothrow_destructible_v<ScopedReportFile>);
    static_assert(!std::is_copy_constructible_v<ScopedReportFile>);
    TestDirectory dir;
    const auto destination = dir.path / "report.txt";
    { std::ofstream out(destination); out << "old"; }
    fs::path temp;
    {
        ScopedReportFile report(destination);
        ScopedReportFile other(destination);
        temp = report.temporaryPath();
        REQUIRE(temp.parent_path() == destination.parent_path());
        REQUIRE(temp != other.temporaryPath());
        REQUIRE(fs::exists(temp));
        report.stream() << "new\n";
        REQUIRE(contents(destination) == "old");
        report.commit();
        REQUIRE(contents(destination) == "new\n");
        REQUIRE(!fs::exists(temp));
        REQUIRE_THROWS_AS(report.commit(), std::logic_error);
    }
    REQUIRE(std::distance(fs::directory_iterator(dir.path), fs::directory_iterator()) == 1);
}

TEST_CASE("Report normal and throwing exits remove temporary and preserve destination") {
    TestDirectory dir;
    const auto destination = dir.path / "report.txt";
    { std::ofstream out(destination); out << "old"; }
    fs::path temp;
    {
        ScopedReportFile report(destination);
        temp = report.temporaryPath();
        report.stream() << "discard";
    }
    REQUIRE(!fs::exists(temp));
    try {
        ScopedReportFile report(destination);
        temp = report.temporaryPath();
        report.stream() << "discard";
        throw std::runtime_error("test unwind");
    } catch (const std::runtime_error&) {}
    REQUIRE(!fs::exists(temp));
    REQUIRE(contents(destination) == "old");
    REQUIRE(std::distance(fs::directory_iterator(dir.path), fs::directory_iterator()) == 1);
}

TEST_CASE("Report failed rename cleans up, and invalid parent fails construction") {
    TestDirectory dir;
    const auto destination = dir.path / "directory";
    fs::create_directory(destination);
    fs::path temp;
    {
        ScopedReportFile report(destination);
        temp = report.temporaryPath();
        report.stream() << "data";
        REQUIRE_THROWS_AS(report.commit(), fs::filesystem_error);
    }
    REQUIRE(!fs::exists(temp));
    REQUIRE(fs::is_directory(destination));
    REQUIRE_THROWS_AS(ScopedReportFile(dir.path / "missing" / "report"), std::runtime_error);
}
TEST_CASE("Report write failure unwinds without publishing partial output") {
    TestDirectory dir;
    const auto destination = dir.path / "report.txt";
    { std::ofstream out(destination); out << "old"; }
    fs::path temp;
    bool caught = false;
    try {
        ScopedReportFile report(destination);
        temp = report.temporaryPath();
        report.stream() << "partial";
        report.stream().setstate(std::ios::badbit);
        report.commit();
    } catch (const std::ios_base::failure&) {
        caught = true;
    }
    REQUIRE(caught);
    REQUIRE(!fs::exists(temp));
    REQUIRE(contents(destination) == "old");
}
int main() { return test_runner::runAll(); }

TEST_CASE("Case suggestions fold ASCII only") {
    LoanService svc;
    seedPinjamLab(svc);
    svc.addEquipment(Equipment("\xc3\x84-LP", "Unicode tag"));
    try {
        (void)svc.borrow("\xc3\xa4-lp", "M-101", 7);
        REQUIRE(false);
    } catch (const UnknownAssetTag& e) {
        REQUIRE(std::string(e.what()) == "Unknown asset tag: \xc3\xa4-lp");
    }
    REQUIRE_THROWS_AS((void)svc.borrow("\xc3\x84-lp", "M-101", 7), AssetTagCaseMismatch);
}
TEST_CASE("Parity wrong-owner return preserves state") {
    LoanService svc;
    seedPinjamLab(svc);
    const auto committed = svc.ledger().committed();
    try {
        svc.returnItem("LP-002", "M-101");
        REQUIRE(false);
    } catch (const LoanError& e) {
        REQUIRE(std::string(e.what()) == "Equipment not loaned to member: LP-002 for M-101");
    }
    REQUIRE(!svc.findEquipment("LP-002")->isAvailable());
    REQUIRE(svc.findMember("M-103")->activeLoans() == 1);
    REQUIRE(svc.findMember("M-101")->activeLoans() == 0);
    REQUIRE(svc.ledger().committed() == committed);
    svc.returnItem("LP-002", "M-103");
    try {
        svc.returnItem("LP-002", "M-103");
        REQUIRE(false);
    } catch (const LoanError& e) {
        REQUIRE(std::string(e.what()) == "Equipment is not on loan: LP-002");
    }
    REQUIRE(svc.borrow("LP-002", "M-101", 7).ok());
    REQUIRE_THROWS_AS(svc.returnItem("LP-002", "M-103"), LoanError);
    svc.returnItem("LP-002", "M-101");
    REQUIRE(svc.findMember("M-101")->activeLoans() == 0);
}
TEST_CASE("Direct service rejects nonpositive durations") {
    LoanService svc;
    seedPinjamLab(svc);
    const auto committed = svc.ledger().committed();
    for (const int days : {0, -1, -2147483647 - 1, 91}) {
        try {
            (void)svc.borrow("LP-001", "M-101", days);
            REQUIRE(false);
        } catch (const InvalidLoanDuration& e) {
            REQUIRE(e.days() == days);
            REQUIRE(e.maxDays() == 90);
            REQUIRE(std::string(e.what()) == "Loan duration exceeds maximum: " + std::to_string(days) + " > 90");
        }
        REQUIRE(svc.findEquipment("LP-001")->isAvailable());
        REQUIRE(svc.findMember("M-101")->activeLoans() == 0);
        REQUIRE(svc.ledger().committed() == committed);
    }
    const auto shortest = svc.borrow("LP-001", "M-101", 1);
    REQUIRE(shortest.ok());
    REQUIRE(shortest.value().days() == 1);
    svc.returnItem("LP-001", "M-101");
    const auto longest = svc.borrow("LP-001", "M-101", 90);
    REQUIRE(longest.ok());
    REQUIRE(longest.value().days() == 90);
}
