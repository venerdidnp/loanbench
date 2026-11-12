"""The acceptance criterion for Lab 2: running the fixed bad-requests.csv
through the real io+service+domain pipeline must produce the ten messages in
sample-data/expected-output.txt, in order, byte for byte, with a non-zero
exit code -- and it must be the SAME ten messages the C++ side produces.
"""
from pathlib import Path

from pinjamlab.app.runner import run_catalogue
from pinjamlab.app.seed import seed_pinjamlab
from pinjamlab.service.loan_service import LoanService

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "sample-data" / "bad-requests.csv"
EXPECTED = ROOT / "sample-data" / "expected-output.txt"


def test_bad_requests_csv_reproduces_expected_output_byte_for_byte():
    svc = LoanService()
    seed_pinjamlab(svc)
    result = run_catalogue(svc, str(CSV))

    expected_lines = EXPECTED.read_text(encoding="utf-8").splitlines()
    assert result.rejected_lines == expected_lines
    assert result.total == 10
    assert result.created == 0
    assert result.rejected == 10
    assert result.exit_code == 1


def test_runner_specific_catches_use_fields_before_family(tmp_path):
    from pinjamlab.domain.loan_error import AssetTagCaseMismatch, ReservationConflict

    errors = [AssetTagCaseMismatch("lp-001", "LP-001"),
              ReservationConflict("LP-004", "M-103")]
    for error in errors:
        error.args = ("generic handler must not use this",)

    class FailingService:
        def borrow(self, *args):
            raise errors.pop(0)

    source = tmp_path / "requests.csv"
    source.write_bytes(b"tag,memberId,days\r\nlp-001,M-101,7\r\n\r\nLP-004,M-101,7\r\n")
    result = run_catalogue(FailingService(), str(source))
    assert result.rejected_lines == [
        "row 1: Unknown asset tag: lp-001 (did you mean LP-001?)",
        "row 3: Equipment reserved: LP-004 for M-103",
    ]
    assert (result.total, result.created, result.rejected, result.exit_code) == (2, 0, 2, 1)


def test_csv_counts_physical_lines_including_multiline_fields(tmp_path):
    from pinjamlab.io.csv_reader import CsvReader

    source = tmp_path / "requests.csv"
    source.write_bytes(b'tag,memberId,days\r\n\r\n"LP-\r\n001",M-101,7\r\n\r\nLP-003,M-101,7\r\n')
    rows = CsvReader().read(source)
    assert [row.line_number for row in rows] == [2, 5]
    assert rows[0].tag == "LP-\r\n001"
