#ifndef PINJAMLAB_IO_REPORT_WRITER_HPP
#define PINJAMLAB_IO_REPORT_WRITER_HPP

// io layer: the ONLY place that knows what a report line looks like. app/
// calls these formatters instead of building strings itself, so the exact
// wording (which expected-output.txt pins byte-for-byte) lives in one place.

#include <sstream>
#include <string>

namespace pinjamlab {

class ReportWriter {
public:
    [[nodiscard]] static std::string rejectedLine(int rowNumber, const std::string& message) {
        std::ostringstream os;
        os << "row " << rowNumber << ": " << message;
        return os.str();
    }

    [[nodiscard]] static std::string summary(int total, int created, int rejected) {
        std::ostringstream os;
        os << "Processed " << total << " rows.\n"
           << created << " loans created, " << rejected << " rejected.";
        return os.str();
    }
};

}  // namespace pinjamlab

#endif  // PINJAMLAB_IO_REPORT_WRITER_HPP
