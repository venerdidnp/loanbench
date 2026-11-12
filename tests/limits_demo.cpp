#include "mini_catch.hpp"
#include "pinjamlab/domain/result.hpp"
#include <functional>

using pinjamlab::Result;

static Result<int> deepChain(int depth, bool fail, int& visited) {
    ++visited;
    if (depth == 0)
        return fail ? Result<int>::failure("leaf unavailable") : Result<int>::success(7);
    const auto child = deepChain(depth - 1, fail, visited);
    if (!child.ok()) return Result<int>::failure(child.error());
    return Result<int>::success(child.value() + 1);
}

TEST_CASE("Limits demo: deep chain explicitly propagates failure through every frame") {
    int visited = 0;
    const auto failed = deepChain(32, true, visited);
    REQUIRE(visited == 33);
    REQUIRE(!failed.ok());
    REQUIRE(failed.error() == "leaf unavailable");
    visited = 0;
    const auto success = deepChain(32, false, visited);
    REQUIRE(success.ok());
    REQUIRE(success.value() == 39);
    REQUIRE(visited == 33);
}

TEST_CASE("Limits demo: fixed void callback cannot return Result and needs an adapter") {
    std::function<void()> callback = [] {
        const auto result = Result<int>::failure("callback unavailable");
        if (!result.ok()) throw std::runtime_error(result.error());
    };
    REQUIRE_THROWS_AS(callback(), std::runtime_error);
}

int main() { return test_runner::runAll(); }
