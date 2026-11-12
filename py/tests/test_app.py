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
