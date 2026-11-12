"""Orchestration only: LoanService coordinates domain objects and raises the
domain's own typed exceptions. No CSV parsing, no console output here.
"""
from __future__ import annotations

from ..domain.equipment import Equipment
from ..domain.loan import Loan
from ..domain.loan_error import (
    AssetTagCaseMismatch,
    LoanError,
    ReservationConflict,
    EquipmentUnavailable,
    InvalidLoanDuration,
    QuotaExceeded,
    UnknownAssetTag,
    UnknownMember,
)
from ..domain.member import Member
from .database import Database
from .txn_guard import txn_guard

MAX_LOAN_DAYS = 90
_ASCII_UPPER = str.maketrans(
    "abcdefghijklmnopqrstuvwxyz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
)


class LoanService:
    def __init__(self) -> None:
        self._catalog: dict[str, Equipment] = {}
        self._roster: dict[str, Member] = {}
        self._owners: dict[str, str] = {}
        self._db = Database()

    def add_equipment(self, equipment: Equipment) -> None:
        if equipment.tag in self._catalog:
            raise ValueError(f"Duplicate equipment: {equipment.tag}")
        self._catalog[equipment.tag] = equipment

    def reserve(self, tag: str, member_id: str) -> None:
        if tag not in self._catalog:
            raise UnknownAssetTag(tag)
        if member_id not in self._roster:
            raise UnknownMember(member_id)
        self._catalog[tag].reserved_for = member_id

    def add_member(self, member: Member) -> None:
        self._roster[member.member_id] = member

    def find_equipment(self, tag: str) -> Equipment | None:
        return self._catalog.get(tag)

    def find_member(self, member_id: str) -> Member | None:
        return self._roster.get(member_id)

    @property
    def ledger(self) -> Database:
        return self._db

    def borrow(self, tag: str, member_id: str, days: int) -> Loan:
        equipment = self._catalog.get(tag)
        if equipment is None:
            for known_tag in self._catalog:
                if known_tag.translate(_ASCII_UPPER) == tag.translate(_ASCII_UPPER):
                    raise AssetTagCaseMismatch(tag, known_tag)
            raise UnknownAssetTag(tag)

        member = self._roster.get(member_id)
        if member is None:
            raise UnknownMember(member_id)

        if days <= 0 or days > MAX_LOAN_DAYS:
            raise InvalidLoanDuration(days, MAX_LOAN_DAYS)

        # Checked before any mutation, same order as the C++ side:
        # availability, reservation, then quota.
        if not equipment.is_available():
            raise EquipmentUnavailable(tag)
        reserved_for = equipment.reserved_for
        if reserved_for and reserved_for != member_id:
            raise ReservationConflict(tag, reserved_for)
        if not member.can_borrow():
            raise QuotaExceeded(member.active_loans, member.max_loans)

        with txn_guard(self._db) as db:
            member.record_loan()
            db.stage(f"loan:{member_id}:{tag}")
            try:
                equipment.mark_loaned()
            except Exception:
                member.undo_record_loan()
                raise
            db.stage(f"equipment:{tag}:loaned")

        self._owners[tag] = member_id
        return Loan(f"L-{tag}-{member_id}", tag, member_id, days)

    def return_item(self, tag: str, member_id: str) -> None:
        equipment = self._catalog.get(tag)
        member = self._roster.get(member_id)
        if equipment is None:
            raise UnknownAssetTag(tag)
        if member is None:
            raise UnknownMember(member_id)
        if tag not in self._owners:
            raise LoanError(f"Equipment is not on loan: {tag}")
        if self._owners[tag] != member_id:
            raise LoanError(f"Equipment not loaned to member: {tag} for {member_id}")
        equipment.mark_returned()
        member.record_return()
        del self._owners[tag]
