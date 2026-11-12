"""Cross-language service robustness checks."""
import pytest

from pinjamlab.app.seed import seed_pinjamlab
from pinjamlab.domain.equipment import Equipment
from pinjamlab.domain.loan_error import (
    AssetTagCaseMismatch, InvalidLoanDuration, LoanError,
    ReservationConflict, UnknownAssetTag, UnknownMember,
)
from pinjamlab.service.loan_service import LoanService


def test_reservation_lives_on_equipment_and_reserve_updates_it():
    svc = LoanService()
    seed_pinjamlab(svc)
    equipment = svc.find_equipment("LP-001")
    assert equipment.reserved_for == ""
    assert svc.find_equipment("LP-004").reserved_for == "M-103"
    svc.reserve("LP-001", "M-103")
    assert equipment.reserved_for == "M-103"
    with pytest.raises(ReservationConflict) as exc:
        svc.borrow("LP-001", "M-101", 7)
    assert str(exc.value) == "Equipment reserved: LP-001 for M-103"
    with pytest.raises(UnknownAssetTag):
        svc.reserve("LP-999", "M-101")
    with pytest.raises(UnknownMember):
        svc.reserve("LP-001", "M-404")
    assert equipment.reserved_for == "M-103"
    equipment.reserved_for = ""
    result = svc.borrow("LP-001", "M-101", 7)
    assert result.ok
    assert result.value.member_id == "M-101"


@pytest.mark.parametrize("days", [0, -1, -2147483648, 91])
def test_direct_service_duration_bounds_preserve_error_and_state(days):
    svc = LoanService()
    seed_pinjamlab(svc)
    committed = list(svc.ledger.committed)
    with pytest.raises(InvalidLoanDuration) as exc:
        svc.borrow("LP-001", "M-101", days)
    assert (exc.value.days, exc.value.max_days) == (days, 90)
    assert str(exc.value) == f"Loan duration exceeds maximum: {days} > 90"
    assert svc.find_equipment("LP-001").is_available()
    assert svc.find_member("M-101").active_loans == 0
    assert svc.ledger.committed == committed
    shortest = svc.borrow("LP-001", "M-101", 1)
    assert shortest.ok
    assert shortest.value.days == 1
    svc.return_item("LP-001", "M-101")
    longest = svc.borrow("LP-001", "M-101", 90)
    assert longest.ok
    assert longest.value.days == 90


def test_case_suggestions_fold_ascii_only():
    svc = LoanService()
    seed_pinjamlab(svc)
    svc.add_equipment(Equipment("\u00c4-LP", "Unicode tag"))
    with pytest.raises(UnknownAssetTag) as exc:
        svc.borrow("\u00e4-lp", "M-101", 7)
    assert type(exc.value) is UnknownAssetTag
    assert str(exc.value) == "Unknown asset tag: \u00e4-lp"
    with pytest.raises(AssetTagCaseMismatch) as exc:
        svc.borrow("\u00c4-lp", "M-101", 7)
    assert exc.value.suggestion == "\u00c4-LP"


def test_wrong_owner_return_preserves_state_and_correct_owner_can_return():
    svc = LoanService()
    seed_pinjamlab(svc)
    committed = list(svc.ledger.committed)
    with pytest.raises(LoanError) as exc:
        svc.return_item("LP-002", "M-101")
    assert str(exc.value) == "Equipment not loaned to member: LP-002 for M-101"
    assert not svc.find_equipment("LP-002").is_available()
    assert svc.find_member("M-103").active_loans == 1
    assert svc.find_member("M-101").active_loans == 0
    assert svc.ledger.committed == committed
    svc.return_item("LP-002", "M-103")
    assert svc.find_member("M-103").active_loans == 0
    with pytest.raises(LoanError) as exc:
        svc.return_item("LP-002", "M-103")
    assert str(exc.value) == "Equipment is not on loan: LP-002"
