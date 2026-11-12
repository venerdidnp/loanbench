"""Result[T]: a small frozen dataclass. Pure domain module."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class Result(Generic[T]):
    ok: bool
    _value: T | None = None
    error: str = ""

    @staticmethod
    def success(value: T) -> "Result[T]":
        return Result(True, value, "")

    @staticmethod
    def failure(error: str) -> "Result[T]":
        return Result(False, None, error)

    @property
    def value(self) -> T:
        if not self.ok:
            raise RuntimeError(f"value on a failed Result: {self.error}")
        return self._value  # type: ignore[return-value]
