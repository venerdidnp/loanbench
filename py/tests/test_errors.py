"""One test per failure mode, plus the catch-order/precision guarantees."""
import pytest

from pinjamlab.domain.loan_error import (
    EquipmentUnavailable,
    InvalidLoanDuration,
    LoanError,
    QuotaExceeded,
    UnknownAssetTag,
    UnknownMember,
)
from pinjamlab.service.loan_service import LoanService
from pinjamlab.app.seed import seed_pinjamlab


def seeded() -> LoanService:
    svc = LoanService()
    seed_pinjamlab(svc)
    return svc


def test_unknown_asset_tag_carries_the_tag():
    svc = seeded()
    with pytest.raises(UnknownAssetTag) as exc:
        svc.borrow("LP-999", "M-101", 7)
    assert exc.value.tag == "LP-999"
    assert str(exc.value) == "Unknown asset tag: LP-999"


def test_unknown_member_carries_the_id():
    svc = seeded()
    with pytest.raises(UnknownMember) as exc:
        svc.borrow("LP-001", "M-404", 7)
    assert exc.value.member_id == "M-404"


def test_invalid_loan_duration_is_the_business_rule_maximum():
    svc = seeded()
    with pytest.raises(InvalidLoanDuration) as exc:
        svc.borrow("LP-001", "M-101", 400)
    assert exc.value.days == 400
    assert exc.value.max_days == 90
    assert str(exc.value) == "Loan duration exceeds maximum: 400 > 90"


def test_equipment_unavailable_carries_the_tag():
    svc = seeded()  # LP-002 was loaned to M-103 during seeding
    with pytest.raises(EquipmentUnavailable) as exc:
        svc.borrow("LP-002", "M-101", 7)
    assert exc.value.tag == "LP-002"


def test_quota_exceeded_carries_active_and_limit():
    svc = seeded()  # M-102 was seeded to exactly 2/2
    with pytest.raises(QuotaExceeded) as exc:
        svc.borrow("LP-003", "M-102", 7)
    assert exc.value.active == 2
    assert exc.value.limit == 2


def test_every_concrete_error_is_catchable_as_the_loan_error_family():
    svc = seeded()
    cases = [
        ("LP-999", "M-101", 7), ("LP-001", "M-404", 7), ("LP-001", "M-101", 400),
        ("LP-002", "M-101", 7), ("LP-003", "M-102", 7),
    ]
    caught_as_family = 0
    for tag, member, days in cases:
        try:
            svc.borrow(tag, member, days)
        except LoanError:
            caught_as_family += 1
    assert caught_as_family == 5


def test_a_bare_except_would_also_catch_keyboard_interrupt_dont_write_one():
    # Not a runtime-testable property of LoanError itself, but documents the
    # rule this module insists on: `except LoanError` or `except Exception`,
    # never a bare `except:`.
    assert issubclass(KeyboardInterrupt, BaseException)
    assert not issubclass(KeyboardInterrupt, Exception)
    assert issubclass(LoanError, Exception)


def test_a_successful_borrow_raises_nothing_and_updates_both_entities():
    svc = seeded()
    loan = svc.borrow("LP-001", "M-101", 7)
    assert loan.tag == "LP-001"
    assert loan.member_id == "M-101"
    assert svc.find_equipment("LP-001").is_available() is False
    assert svc.find_member("M-101").active_loans == 1


def test_case_mismatch_fields_message_and_family():
    from pinjamlab.domain.loan_error import AssetTagCaseMismatch

    with pytest.raises(AssetTagCaseMismatch) as exc:
        seeded().borrow("lp-001", "M-101", 7)
    error = exc.value
    assert isinstance(error, UnknownAssetTag)
    assert isinstance(error, LoanError)
    assert (error.given, error.suggestion, error.tag) == ("lp-001", "LP-001", "lp-001")
    assert str(error) == "Unknown asset tag: lp-001 (did you mean LP-001?)"


def test_reservation_fields_message_family_and_allowed_member():
    from pinjamlab.domain.loan_error import ReservationConflict

    svc = seeded()
    with pytest.raises(ReservationConflict) as exc:
        svc.borrow("LP-004", "M-101", 7)
    assert isinstance(exc.value, LoanError)
    assert (exc.value.tag, exc.value.reserved_for) == ("LP-004", "M-103")
    assert str(exc.value) == "Equipment reserved: LP-004 for M-103"
    assert svc.find_equipment("LP-004").is_available()
    assert svc.borrow("LP-004", "M-103", 7).member_id == "M-103"


def test_duplicate_equipment_preserves_original():
    from pinjamlab.domain.equipment import Equipment

    svc = seeded()
    original = svc.find_equipment("LP-001")
    with pytest.raises(ValueError, match="Duplicate equipment: LP-001"):
        svc.add_equipment(Equipment("LP-001", "replacement"))
    assert svc.find_equipment("LP-001") is original


@pytest.mark.parametrize("tag,member,error,message", [
    ("LP-999", "M-101", UnknownAssetTag, "Unknown asset tag: LP-999"),
    ("LP-002", "M-404", UnknownMember, "Unknown member: M-404"),
    ("LP-001", "M-101", LoanError, "Equipment is not on loan: LP-001"),
    ("LP-002", "M-101", LoanError, "Equipment not loaned to member: LP-002 for M-101"),
])
def test_invalid_returns_raise_without_mutation(tag, member, error, message):
    svc = seeded()
    committed = list(svc.ledger.committed)
    with pytest.raises(error) as exc:
        svc.return_item(tag, member)
    assert str(exc.value) == message
    assert not svc.find_equipment("LP-002").is_available()
    assert svc.find_equipment("LP-001").is_available()
    assert svc.find_member("M-103").active_loans == 1
    assert svc.find_member("M-101").active_loans == 0
    assert svc.ledger.committed == committed


def test_return_updates_owner_once_and_allows_reborrow():
    svc = seeded()
    svc.return_item("LP-002", "M-103")
    assert svc.find_equipment("LP-002").is_available()
    assert svc.find_member("M-103").active_loans == 0
    with pytest.raises(LoanError, match="not on loan"):
        svc.return_item("LP-002", "M-103")
    svc.borrow("LP-002", "M-101", 7)
    with pytest.raises(LoanError, match="not loaned to member"):
        svc.return_item("LP-002", "M-103")
    svc.return_item("LP-002", "M-101")
    assert svc.find_member("M-101").active_loans == 0
