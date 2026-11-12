"""io layer: the ONLY place that knows what a report line looks like."""
from __future__ import annotations


class ReportWriter:
    @staticmethod
    def rejected_line(row_number: int, message: str) -> str:
        return f"row {row_number}: {message}"

    @staticmethod
    def summary(total: int, created: int, rejected: int) -> str:
        return f"Processed {total} rows.\n{created} loans created, {rejected} rejected."
