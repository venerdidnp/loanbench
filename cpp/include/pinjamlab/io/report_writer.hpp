#ifndef PINJAMLAB_IO_REPORT_WRITER_HPP
#define PINJAMLAB_IO_REPORT_WRITER_HPP

// io layer: the ONLY place that knows what a report line looks like. app/
// calls these formatters instead of building strings itself, so the exact
// wording (which expected-output.txt pins byte-for-byte) lives in one place.

#include <sstream>
#include <filesystem>
#include <fstream>
#include <cstdlib>
#include <stdexcept>
#include <utility>
#include <vector>
#include <unistd.h>
#include <string>

namespace pinjamlab {

// The destination is untouched until commit; the temporary lives beside it
// so the rename is atomic on the destination filesystem.
class ScopedReportFile {
    std::filesystem::path destination_, temporary_;
    std::ofstream output_;
    bool committed_ = false;
public:
    explicit ScopedReportFile(std::filesystem::path destination)
        : destination_(std::move(destination)) {
        const auto pattern = destination_.string() + ".tmp.XXXXXX";
        std::vector<char> name(pattern.begin(), pattern.end());
        name.push_back('\0');
        const int fd = ::mkstemp(name.data());
        if (fd == -1) throw std::runtime_error("cannot create report temporary: " + destination_.string());
        ::close(fd);
        try {
            temporary_ = name.data();
            output_.exceptions(std::ios::failbit | std::ios::badbit);
            output_.open(temporary_, std::ios::binary | std::ios::trunc);
        } catch (...) {
            std::error_code ignored;
            std::filesystem::remove(name.data(), ignored);
            throw;
        }
    }
    ScopedReportFile(const ScopedReportFile&) = delete;
    ScopedReportFile& operator=(const ScopedReportFile&) = delete;
    ~ScopedReportFile() noexcept {
        try { if (output_.is_open()) output_.close(); } catch (...) {}
        if (!committed_) {
            std::error_code ignored;
            std::filesystem::remove(temporary_, ignored);
        }
    }
    [[nodiscard]] std::ostream& stream() noexcept { return output_; }
    [[nodiscard]] const std::filesystem::path& temporaryPath() const noexcept { return temporary_; }
    void commit() {
        if (committed_) throw std::logic_error("report already committed");
        output_.flush();
        output_.close();
        std::filesystem::rename(temporary_, destination_);
        committed_ = true;
    }
};

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
