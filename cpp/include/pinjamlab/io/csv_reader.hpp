#ifndef PINJAMLAB_IO_CSV_READER_HPP
#define PINJAMLAB_IO_CSV_READER_HPP

// io layer: turns bytes on disk into raw, untyped rows. Deliberately does
// NOT interpret "days" as a number here -- that decision belongs to
// Validator, which is the one component allowed to reject malformed input.

#include <fstream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace pinjamlab {

struct RawRow {
    int lineNumber;  // Physical data lines, including blanks (header excluded).
    std::string tag;
    std::string memberId;
    std::string daysRaw;
};

class CsvReader {
public:
    // Format: "tag,member_id,days" with one header line.
    [[nodiscard]] std::vector<RawRow> read(const std::string& path) const {
        std::ifstream in(path);
        if (!in) throw std::runtime_error("cannot open input: " + path);

        std::vector<RawRow> rows;
        std::string line;
        std::getline(in, line);  // header, discarded

        int n = 0;
        while (std::getline(in, line)) {
            ++n;
            if (!line.empty() && line.back() == '\r') line.pop_back();
            if (line.empty()) continue;
            std::istringstream ls(line);
            RawRow r;
            r.lineNumber = n;
            std::getline(ls, r.tag, ',');
            std::getline(ls, r.memberId, ',');
            std::getline(ls, r.daysRaw, ',');
            rows.push_back(std::move(r));
        }
        return rows;
    }
};

}  // namespace pinjamlab

#endif  // PINJAMLAB_IO_CSV_READER_HPP
