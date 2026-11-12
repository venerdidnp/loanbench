"""Proves txn_guard releases (rolls back) on EVERY exit path, including the
raising one -- Lab 2.3's requirement: "a test that throws inside the guarded
region and asserts the resource was released."
"""
import pytest

from pinjamlab.domain.equipment import Equipment
from pinjamlab.domain.member import Member, Role
from pinjamlab.service.database import Database
from pinjamlab.service.loan_service import LoanService
from pinjamlab.service.txn_guard import txn_guard


def test_txn_guard_commits_staged_records_become_committed():
    db = Database()
    with txn_guard(db) as txn:
        txn.stage("a")
        txn.stage("b")
    assert len(db.committed) == 2
    assert db.pending_count == 0


def test_txn_guard_rolls_back_when_an_exception_propagates_through_it():
    db = Database()
    with pytest.raises(RuntimeError):
        with txn_guard(db) as txn:
            txn.stage("about to be abandoned")
            raise RuntimeError("simulated failure mid-transaction")
    assert db.committed == []       # the raising path released, exactly
    assert db.pending_count == 0    # like the normal exit path above


def test_forgetting_with_silently_loses_the_guarantee():
    # The lesson Figure "Deterministic Cleanup" names explicitly: the
    # guarantee in Python is attached to the STATEMENT, not the object, so a
    # caller who writes this instead of `with txn_guard(db) as txn:` gets a
    # generator object and nothing runs at all.
    db = Database()
    guard = txn_guard(db)  # constructs the generator; begin() has NOT run yet
    assert db.pending_count == 0
    del guard  # dropping it runs no cleanup -- there was nothing to clean up


def test_loan_service_borrow_commits_the_ledger_on_success():
    svc = LoanService()
    svc.add_equipment(Equipment("LP-001", "ThinkPad T14"))
    svc.add_member(Member("M-101", "Ayu Lestari", Role.STUDENT))
    svc.borrow("LP-001", "M-101", 7)
    assert len(svc.ledger.committed) == 2  # "loan:" and "equipment:" records
