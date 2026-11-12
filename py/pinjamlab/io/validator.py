"""io layer: converts a RawRow into a Result[LoanRequest]. Format failures
are rejected HERE with plain string errors -- they never reach domain.
"""
from __future__ import annotations

from dataclasses import dataclass

from ..domain.result import Result
from .csv_reader import RawRow


@dataclass(frozen=True, slots=True)
class LoanRequest:
    tag: str
    member_id: str
    days: int


class Validator:
    def validate(self, row: RawRow) -> Result[LoanRequest]:
        if not row.tag:
            return Result.failure("tag is empty")
        if not row.member_id:
            return Result.failure("memberId is empty")

        try:
            days = int(row.days_raw)
        except ValueError:
            return Result.failure(f"days is not a number: {row.days_raw}")

        if days <= 0:
            return Result.failure(f"days must be positive, got {days}")

        return Result.success(LoanRequest(row.tag, row.member_id, days))
