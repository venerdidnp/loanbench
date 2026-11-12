"""Pure domain module: Member entity, carried forward from Module 1."""
from __future__ import annotations

from enum import Enum

from .loan_error import QuotaExceeded


class Role(Enum):
    STUDENT = 2
    FACULTY = 5
    STAFF = 3


class Member:
    def __init__(self, member_id: str, name: str, role: Role) -> None:
        self.member_id = member_id
        self.name = name
        self.role = role
        self._active_loans = 0

    @property
    def max_loans(self) -> int:
        return self.role.value

    @property
    def active_loans(self) -> int:
        return self._active_loans

    def can_borrow(self) -> bool:
        return self._active_loans < self.max_loans

    def record_loan(self) -> None:
        if not self.can_borrow():
            raise QuotaExceeded(self._active_loans, self.max_loans)
        self._active_loans += 1

    def record_return(self) -> None:
        if self._active_loans > 0:
            self._active_loans -= 1

    def undo_record_loan(self) -> None:
        """Used only by the txn_guard rollback path."""
        if self._active_loans > 0:
            self._active_loans -= 1
