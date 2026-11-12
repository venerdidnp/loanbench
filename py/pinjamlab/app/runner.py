"""app layer: the top-level handler. This is the ONE place allowed to catch
`LoanError` and turn it into a message a human reads, and the ONE place that
decides the process exit code.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from ..domain.loan_error import (
    AssetTagCaseMismatch, LoanError, ReservationConflict,
)
from ..io.csv_reader import CsvReader
from ..io.report_writer import ReportWriter
from ..io.validator import Validator
from ..service.loan_service import LoanService


@dataclass
class RunResult:
    rejected_lines: list[str] = field(default_factory=list)
    total: int = 0
    created: int = 0
    rejected: int = 0

    @property
    def exit_code(self) -> int:
        return 0 if self.rejected == 0 else 1


def run_catalogue(svc: LoanService, csv_path: str) -> RunResult:
    reader = CsvReader()
    validator = Validator()
    result = RunResult()

    rows = reader.read(csv_path)
    result.total = len(rows)

    for row in rows:
        validated = validator.validate(row)
        if not validated.ok:
            result.rejected += 1
            result.rejected_lines.append(
                ReportWriter.rejected_line(row.line_number, validated.error))
            continue
        req = validated.value
        try:
            borrowed = svc.borrow(req.tag, req.member_id, req.days)
            if not borrowed.ok:
                result.rejected += 1
                result.rejected_lines.append(
                    ReportWriter.rejected_line(row.line_number, borrowed.error))
                continue
            result.created += 1
        except AssetTagCaseMismatch as e:
            result.rejected += 1
            result.rejected_lines.append(ReportWriter.rejected_line(
                row.line_number,
                f"Unknown asset tag: {e.given} (did you mean {e.suggestion}?)"))
        except ReservationConflict as e:
            result.rejected += 1
            result.rejected_lines.append(ReportWriter.rejected_line(
                row.line_number,
                f"Equipment reserved: {e.tag} for {e.reserved_for}"))
        except LoanError as e:  # the family we understand
            result.rejected += 1
            result.rejected_lines.append(
                ReportWriter.rejected_line(row.line_number, str(e)))
        # Anything that is NOT a LoanError is left to travel.

    return result
