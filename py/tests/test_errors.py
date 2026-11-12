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
