"""Runnable assertions illustrating Result's explicit propagation cost."""
from pinjamlab.domain.result import Result


def deep_chain(depth, fail, visited):
    visited.append(depth)
    if depth == 0:
        return Result.failure("leaf unavailable") if fail else Result.success(7)
    child = deep_chain(depth - 1, fail, visited)
    if not child.ok:
        return Result.failure(child.error)
    return Result.success(child.value + 1)


def main():
    visited = []
    failed = deep_chain(32, True, visited)
    assert len(visited) == 33
    assert not failed.ok and failed.error == "leaf unavailable"
    visited.clear()
    success = deep_chain(32, False, visited)
    assert success.ok and success.value == 39 and len(visited) == 33
    print("PASSED: limits_demo deep chain explicit propagation")

    calls = []

    def operation():
        calls.append("attempted")
        return Result.failure("ignored unavailable")

    operation()  # Python has no nodiscard warning: a failure can be ignored.
    assert calls == ["attempted"]
    checked = operation()
    assert not checked.ok and checked.error == "ignored unavailable"
    print("PASSED: limits_demo Python can silently ignore a failed Result")


if __name__ == "__main__":
    main()
