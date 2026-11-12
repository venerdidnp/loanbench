"""io layer: converts a RawRow into a Result[LoanRequest]. Format failures
are rejected HERE with plain string errors -- they never reach domain.
"""
from __future__ import annotations

from dataclasses import dataclass
import re

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
        if not row.tag.strip():
            return Result.failure("tag is blank")
        if not row.member_id:
            return Result.failure("memberId is empty")
        if not row.member_id.strip():
            return Result.failure("memberId is blank")

        if re.fullmatch(r"[+-]?[0-9]+", row.days_raw) is None:
            return Result.failure(f"days is not a number: {row.days_raw}")

        # Compare significant digits before conversion to avoid Python's digit limit.
        digits = row.days_raw.lstrip("+-").lstrip("0") or "0"
        bound = "2147483648" if row.days_raw.startswith("-") else "2147483647"
        if len(digits) > len(bound) or (len(digits) == len(bound) and digits > bound):
            return Result.failure(f"days is out of range: {row.days_raw}")
        days = int(("-" if row.days_raw.startswith("-") else "") + digits)
        if days <= 0:
            return Result.failure(f"days must be positive, got {days}")

        return Result.success(LoanRequest(row.tag, row.member_id, days))
