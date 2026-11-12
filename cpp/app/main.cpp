// app layer entry point: argument parsing, top-level handler, exit codes.
// No business rule lives in this file; it wires io + service + domain
// together and reports what happened.

#include "pinjamlab/app/runner.hpp"
#include "pinjamlab/app/seed.hpp"

#include <iostream>
#include <string>

int main(int argc, char** argv) {
    const std::string path = (argc >= 2) ? argv[1] : "sample-data/bad-requests.csv";

    pinjamlab::LoanService svc;
    pinjamlab::seedPinjamLab(svc);

    const auto result = pinjamlab::runCatalogue(svc, path);

    for (const auto& line : result.rejectedLines) {
        std::cerr << line << "\n";
    }
    std::cout << pinjamlab::ReportWriter::summary(result.total, result.created, result.rejected)
              << "\n";

    return result.exitCode();
}
