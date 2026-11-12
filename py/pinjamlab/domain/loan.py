"""Pure domain module: the record produced by a successful borrow()."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Loan:
    loan_id: str
    tag: str
    member_id: str
    days: int
