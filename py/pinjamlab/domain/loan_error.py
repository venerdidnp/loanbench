"""Pure domain module: no console output, no file streams, no text formats.

The dependency-rule check in run_tests.sh greps this package for exactly
those things (module-level file or console access) and fails the build if
it finds one outside a comment.
"""


class LoanError(Exception):
    """Base for every PinjamLab loan failure."""


class UnknownAssetTag(LoanError):
    def __init__(self, tag: str) -> None:
        super().__init__(f"Unknown asset tag: {tag}")
        self.tag = tag


class UnknownMember(LoanError):
    def __init__(self, member_id: str) -> None:
        super().__init__(f"Unknown member: {member_id}")
        self.member_id = member_id


class InvalidLoanDuration(LoanError):
    """A business-rule violation on duration (exceeds the policy maximum).

    Distinct from the io-layer's "days is not a number" / "days must be
    positive" checks, which are format failures returned as a Result before
    a request ever reaches the domain layer.
    """

    def __init__(self, days: int, max_days: int) -> None:
        super().__init__(f"Loan duration exceeds maximum: {days} > {max_days}")
        self.days = days
        self.max_days = max_days


class EquipmentUnavailable(LoanError):
    """Guard 3 of the failure cascade: an ORDINARY, expected outcome."""

    def __init__(self, tag: str) -> None:
        super().__init__(f"Equipment already on loan: {tag}")
        self.tag = tag


class QuotaExceeded(LoanError):
    def __init__(self, active: int, limit: int) -> None:
        super().__init__(f"Loan quota exceeded: {active} active, limit {limit}")
        self.active = active
        self.limit = limit
