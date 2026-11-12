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
    days = int(raw)  # raises ValueError on anything non-numeric
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
