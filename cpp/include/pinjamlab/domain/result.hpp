#ifndef PINJAMLAB_DOMAIN_RESULT_HPP
#define PINJAMLAB_DOMAIN_RESULT_HPP

// From-scratch primitive (~15 lines of actual logic): no std::optional,
// no std::expected, no library type. Pure domain header.

#include <stdexcept>
#include <string>
#include <utility>

namespace pinjamlab {

template <typename T>
class [[nodiscard]] Result {  // [[nodiscard]]: ignoring the return value warns
    bool ok_;
    T value_{};
    std::string error_;

    Result(bool ok, T v, std::string e)
        : ok_(ok), value_(std::move(v)), error_(std::move(e)) {}

public:
    static Result success(T v) { return Result(true, std::move(v), ""); }
    static Result failure(std::string e) { return Result(false, T{}, std::move(e)); }

    [[nodiscard]] bool ok() const noexcept { return ok_; }
    [[nodiscard]] const std::string& error() const noexcept { return error_; }

    // Reading the value of a failed Result is a PROGRAMMING error (the caller
    // skipped ok()), not a runtime one -- so it throws rather than returning
    // a default-constructed T that looks like real data.
    [[nodiscard]] const T& value() const {
        if (!ok_) throw std::logic_error("value() on a failed Result: " + error_);
        return value_;
    }
};

}  // namespace pinjamlab

#endif  // PINJAMLAB_DOMAIN_RESULT_HPP
