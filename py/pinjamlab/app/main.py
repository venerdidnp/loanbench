"""app layer entry point: argument parsing, top-level handler, exit codes.
No business rule lives in this file.
"""
from __future__ import annotations

import sys

from ..io.report_writer import ReportWriter
from ..service.loan_service import LoanService
from .runner import run_catalogue
from .seed import seed_pinjamlab


def main(argv: list[str]) -> int:
    path = argv[1] if len(argv) >= 2 else "sample-data/bad-requests.csv"

    svc = LoanService()
    seed_pinjamlab(svc)

    result = run_catalogue(svc, path)

    for line in result.rejected_lines:
        print(line, file=sys.stderr)
    print(ReportWriter.summary(result.total, result.created, result.rejected))

    return result.exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv))
