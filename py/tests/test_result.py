"""Result[T]: proves value on a failed Result raises, and that a Result-
based rule and a throwing equivalent agree on every input -- the
"from-scratch match" Lab 2.2 requires.
"""
import pytest

from pinjamlab.domain.result import Result
from pinjamlab.io.csv_reader import RawRow
from pinjamlab.io.validator import Validator


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
