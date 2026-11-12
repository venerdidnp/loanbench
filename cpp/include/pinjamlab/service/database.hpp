#ifndef PINJAMLAB_SERVICE_DATABASE_HPP
#define PINJAMLAB_SERVICE_DATABASE_HPP

// A minimal in-memory stand-in for persistence. Real durability (SQLite)
// arrives in Module 5; here "the database" is just enough state -- a staged
// list and a committed list -- to demonstrate begin/commit/rollback
// honestly, and to give TxnGuard something real to guard.

#include <string>
#include <vector>

namespace pinjamlab {

class Database {
    std::vector<std::string> committed_;
    std::vector<std::string> pending_;

public:
    void begin() { pending_.clear(); }
    void stage(std::string record) { pending_.push_back(std::move(record)); }

    void commit() {
        for (auto& r : pending_) committed_.push_back(std::move(r));
        pending_.clear();
    }

    void rollback() { pending_.clear(); }

    [[nodiscard]] const std::vector<std::string>& committed() const noexcept { return committed_; }
    [[nodiscard]] std::size_t pendingCount() const noexcept { return pending_.size(); }
};

}  // namespace pinjamlab

#endif  // PINJAMLAB_SERVICE_DATABASE_HPP
