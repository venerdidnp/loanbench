"""Result[T]: proves value on a failed Result raises, and that a Result-
based rule and a throwing equivalent agree on every input -- the
"from-scratch match" Lab 2.2 requires.
"""
import pytest

from pinjamlab.domain.result import Result
from pinjamlab.app.seed import seed_pinjamlab
from pinjamlab.domain.loan_error import EquipmentUnavailable, LoanError
from pinjamlab.service.loan_service import LoanService
from pinjamlab.io.csv_reader import RawRow
from pinjamlab.io.validator import Validator


def borrow_or_raise(svc, tag, member, days):
    """Test-only adapter, deliberately not a production throwing twin."""
    result = svc.borrow(tag, member, days)
    if not result.ok:
        raise EquipmentUnavailable(tag)
    return result.value


@pytest.mark.parametrize("tag,member,days", [
    ("LP-001", "M-101", 7), ("LP-002", "M-101", 7),
    ("LP-999", "M-101", 7), ("lp-001", "M-101", 7),
    ("LP-001", "M-404", 7), ("LP-001", "M-101", 0),
    ("LP-001", "M-101", 91), ("LP-004", "M-101", 7),
    ("LP-003", "M-102", 7), ("LP-002", "M-404", 7),
    ("LP-002", "M-101", 0), ("LP-002", "M-102", 7),
])
def test_borrow_result_throwing_twin_same_inputs_outcome_and_state(tag, member, days):
    actual, twin = LoanService(), LoanService()
    seed_pinjamlab(actual)
    seed_pinjamlab(twin)
    before = list(actual.ledger.committed)
    success = False
    try:
        result = actual.borrow(tag, member, days)
        success = result.ok
        if result.ok:
            loan = result.value
            outcome = (None, loan.loan_id, loan.tag, loan.member_id, loan.days)
        else:
            outcome = (EquipmentUnavailable, result.error)
            with pytest.raises(RuntimeError):
                _ = result.value
    except LoanError as error:
        outcome = (type(error), str(error))
    try:
        loan = borrow_or_raise(twin, tag, member, days)
        twin_outcome = (None, loan.loan_id, loan.tag, loan.member_id, loan.days)
    except LoanError as error:
        twin_outcome = (type(error), str(error))
    assert outcome == twin_outcome
    for item in ("LP-001", "LP-002", "LP-003", "LP-004", "SEED-01", "SEED-02"):
        a, b = actual.find_equipment(item), twin.find_equipment(item)
        assert (a.is_available(), a.reserved_for) == (b.is_available(), b.reserved_for)
    for person in ("M-101", "M-102", "M-103"):
        assert actual.find_member(person).active_loans == twin.find_member(person).active_loans
    assert actual.ledger.committed == twin.ledger.committed
    assert len(actual.ledger.committed) == (8 if success else 6)
    assert actual.ledger.pending_count == twin.ledger.pending_count == 0
    if not success:
        assert actual.ledger.committed == before
        assert [actual.find_member(m).active_loans for m in ("M-101", "M-102", "M-103")] == [0, 2, 1]
        assert [actual.find_equipment(t).is_available() for t in ("LP-001", "LP-002", "LP-003", "LP-004")] == [True, False, True, True]
    item, owner = (tag, member) if success else ("LP-002", "M-103")
    actual.return_item(item, owner)
    twin.return_item(item, owner)
    assert actual.find_equipment(item).is_available()
    assert twin.find_equipment(item).is_available()


def test_success_carries_a_value_and_ok_is_true():
    r = Result.success(42)
    assert r.ok is True
    assert r.value == 42
    assert r.error == ""


def test_failure_carries_a_message_and_ok_is_false():
    r = Result.failure("days must be positive, got -3")
    assert r.ok is False
    assert r.error == "days must be positive, got -3"


def test_value_on_a_failed_result_raises_rather_than_returning_garbage():
    r = Result.failure("tag is empty")
    with pytest.raises(RuntimeError):
        _ = r.value


def parse_days_or_raise(raw: str) -> int:
    """A deliberately duplicated throwing version of Validator's own rule,
    so the two can be compared on the same inputs."""
    digits = raw[1:] if raw.startswith(("+", "-")) else raw
    if not digits or any(char < "0" or char > "9" for char in digits):
        raise ValueError(f"days is not a number: {raw}")
    value = 0
    for digit in digits:
        value = value * 10 + ord(digit) - ord("0")
        if value > (2147483648 if raw.startswith("-") else 2147483647):
            raise ValueError(f"days is out of range: {raw}")
    days = -value if raw.startswith("-") else value
    if days <= 0:
        raise ValueError(f"days must be positive, got {days}")
    return days


def test_from_scratch_match_agree_on_well_formed_input():
    v = Validator()
    row = RawRow(1, "LP-001", "M-101", "7")
    r = v.validate(row)
    assert r.ok
    assert r.value.days == 7
    assert parse_days_or_raise("7") == 7


@pytest.mark.parametrize("raw", ["abc", "-3", "0"])
def test_from_scratch_match_agree_on_every_malformed_input(raw):
    v = Validator()
    row = RawRow(1, "LP-001", "M-101", raw)
    r = v.validate(row)
    assert not r.ok  # Result: caller decides, cannot ignore .ok

    with pytest.raises(ValueError):
        parse_days_or_raise(raw)


@pytest.mark.parametrize("raw", [
    "7", "+7", "0007", "+0007", "2147483647", "-2147483648",
    "2147483648", "-2147483649", "+2147483648", "0", "-0", "-3",
    "", "+", "-", " 7", "7 ", "7\n", "1_0", "1.0", "++7", "+-7",
    "\u0667", "\uff17", "\u22127", "9" * 5000, "0" * 5000 + "7",
])
def test_strict_days_parsing_parity(raw):
    result = Validator().validate(RawRow(1, "LP-001", "M-101", raw))
    try:
        expected = parse_days_or_raise(raw)
    except ValueError as error:
        assert not result.ok
        assert result.error == str(error)
    else:
        assert result.ok
        assert result.value.days == expected


@pytest.mark.parametrize("tag,member,message", [
    ("", "M-101", "tag is empty"),
    (" \t", "M-101", "tag is blank"),
    ("LP-001", "", "memberId is empty"),
    ("LP-001", " \t", "memberId is blank"),
])
def test_empty_and_blank_fields_are_validator_results(tag, member, message):
    result = Validator().validate(RawRow(1, tag, member, "7"))
    assert not result.ok
    assert result.error == message


@pytest.mark.parametrize("raw", ["2147483648", "-2147483649", "+9999999999"])
def test_out_of_range_message_preserves_raw_days(raw):
    result = Validator().validate(RawRow(1, "LP-001", "M-101", raw))
    assert result.error == f"days is out of range: {raw}"
