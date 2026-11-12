// The acceptance criterion for Lab 2: running the fixed bad-requests.csv
// through the real io+service+domain pipeline must produce the ten messages
// in sample-data/expected-output.txt, in order, byte for byte, with a
// non-zero exit code. This is the golden-file test Lab 3.4 asks a partner to
// reproduce from a clean clone.

#include "mini_catch.hpp"
#include "pinjamlab/app/runner.hpp"
#include "pinjamlab/app/seed.hpp"

#include <fstream>
#include <sstream>
#include <string>
#include <vector>

using namespace pinjamlab;

static std::vector<std::string> readLines(const std::string& path) {
    std::ifstream in(path);
    std::vector<std::string> lines;
    std::string line;
    while (std::getline(in, line)) {
        if (!line.empty() && line.back() == '\r') line.pop_back();
        lines.push_back(line);
    }
    return lines;
}

TEST_CASE("bad-requests.csv reproduces expected-output.txt byte for byte") {
    LoanService svc;
    seedPinjamLab(svc);
    const auto result = runCatalogue(svc, "sample-data/bad-requests.csv");

    const auto expected = readLines("sample-data/expected-output.txt");
    REQUIRE(result.rejectedLines.size() == expected.size());
    for (std::size_t i = 0; i < expected.size(); ++i) {
        REQUIRE(result.rejectedLines[i] == expected[i]);
    }
    REQUIRE(result.total == 10);
    REQUIRE(result.created == 0);
    REQUIRE(result.rejected == 10);
    REQUIRE(result.exitCode() == 1);
}

int main() { return test_runner::runAll(); }
