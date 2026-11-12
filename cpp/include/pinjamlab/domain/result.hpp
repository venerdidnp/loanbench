#ifndef PINJAMLAB_DOMAIN_RESULT_HPP
#define PINJAMLAB_DOMAIN_RESULT_HPP

// Handmade tagged storage: failure never constructs T (Loan has no default).

#include <stdexcept>
#include <string>
#include <utility>
#include <new>
#include <type_traits>

namespace pinjamlab {

template <typename T>
class [[nodiscard]] Result {  // [[nodiscard]]: ignoring the return value warns
    bool ok_;
    union Storage {
        T value;
        Storage() noexcept {}
        ~Storage() noexcept {}
    } storage_;
    std::string error_;

    explicit Result(std::string e) : ok_(false), error_(std::move(e)) {}
    Result(T v, bool) : ok_(false) {
        new (&storage_.value) T(std::move(v));
        ok_ = true;
    }

public:
    static Result success(T v) { return Result(std::move(v), true); }
    static Result failure(std::string e) { return Result(std::move(e)); }

    Result(const Result& other) : ok_(false), error_(other.error_) {
        if (other.ok_) {
            new (&storage_.value) T(other.storage_.value);
            ok_ = true;
        }
    }
    Result(Result&& other) noexcept(std::is_nothrow_move_constructible_v<T>)
        : ok_(false), error_(std::move(other.error_)) {
        if (other.ok_) {
            new (&storage_.value) T(std::move(other.storage_.value));
            ok_ = true;
        }
    }
    Result& operator=(const Result& other) {
        if (this == &other) return *this;
        error_ = other.error_;
        if (ok_) { storage_.value.~T(); ok_ = false; }
        // Publish the tag only after construction, even when T's copy throws.
        if (other.ok_) {
            new (&storage_.value) T(other.storage_.value);
            ok_ = true;
        }
        return *this;
    }
    Result& operator=(Result&& other) noexcept(std::is_nothrow_move_constructible_v<T>) {
        if (this == &other) return *this;
        error_ = std::move(other.error_);
        if (ok_) { storage_.value.~T(); ok_ = false; }
        if (other.ok_) {
            new (&storage_.value) T(std::move(other.storage_.value));
            ok_ = true;
        }
        return *this;
    }
    ~Result() { if (ok_) storage_.value.~T(); }

    [[nodiscard]] bool ok() const noexcept { return ok_; }
    [[nodiscard]] const std::string& error() const noexcept { return error_; }

    // Reading the value of a failed Result is a PROGRAMMING error (the caller
    // skipped ok()), not a runtime one -- so it throws rather than returning
    // a default-constructed T that looks like real data.
    [[nodiscard]] const T& value() const {
        if (!ok_) throw std::logic_error("value() on a failed Result: " + error_);
        return storage_.value;
    }
};

}  // namespace pinjamlab

#endif  // PINJAMLAB_DOMAIN_RESULT_HPP
