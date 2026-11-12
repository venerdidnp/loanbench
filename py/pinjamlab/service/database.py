"""A minimal in-memory stand-in for persistence -- the Python twin of
service/database.hpp. Real durability (SQLite) arrives in Module 5.
"""
from __future__ import annotations


class Database:
    def __init__(self) -> None:
        self._committed: list[str] = []
        self._pending: list[str] = []

    def begin(self) -> None:
        self._pending.clear()

    def stage(self, record: str) -> None:
        self._pending.append(record)

    def commit(self) -> None:
        self._committed.extend(self._pending)
        self._pending.clear()

    def rollback(self) -> None:
        self._pending.clear()

    @property
    def committed(self) -> list[str]:
        return list(self._committed)

    @property
    def pending_count(self) -> int:
        return len(self._pending)
