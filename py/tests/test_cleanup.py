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


def test_forgetting_with_retains_an_open_handle_until_manually_closed(tmp_path):
    handle = open(tmp_path / "unguarded.txt", "w", encoding="utf-8")
    try:
        with pytest.raises(RuntimeError):
            handle.write("partial")
            raise RuntimeError("no with statement owns this handle")
        assert not handle.closed
    finally:
        handle.close()
    assert handle.closed


def test_contextmanager_generator_is_lazy():
    from unittest.mock import Mock

    db = Mock(spec=Database)
    guard = txn_guard(db)
    db.begin.assert_not_called()
    del guard


def test_loan_service_borrow_commits_the_ledger_on_success():
    svc = LoanService()
    svc.add_equipment(Equipment("LP-001", "ThinkPad T14"))
    svc.add_member(Member("M-101", "Ayu Lestari", Role.STUDENT))
    assert svc.borrow("LP-001", "M-101", 7).ok
    assert len(svc.ledger.committed) == 2  # "loan:" and "equipment:" records


def test_atomic_writer_replaces_only_on_success(tmp_path):
    from pathlib import Path
    from pinjamlab.io.atomic_writer import atomic_writer

    target = tmp_path / "report.txt"
    target.write_text("old", encoding="utf-8")
    with atomic_writer(target) as handle:
        temporary = Path(handle.name)
        assert temporary.parent == target.parent
        handle.write("new")
        assert target.read_text(encoding="utf-8") == "old"
    assert handle.closed
    assert target.read_text(encoding="utf-8") == "new"
    assert not temporary.exists()
    assert list(tmp_path.iterdir()) == [target]


@pytest.mark.parametrize("existing", [False, True])
def test_atomic_writer_cleans_up_on_body_failure(tmp_path, existing):
    from pinjamlab.io.atomic_writer import atomic_writer

    target = tmp_path / "report.txt"
    if existing:
        target.write_text("old", encoding="utf-8")
    with pytest.raises(RuntimeError, match="body failed"):
        with atomic_writer(target) as handle:
            handle.write("partial")
            raise RuntimeError("body failed")
    assert handle.closed
    assert target.exists() == existing
    if existing:
        assert target.read_text(encoding="utf-8") == "old"
    assert list(tmp_path.iterdir()) == ([target] if existing else [])


def test_atomic_writer_cleans_up_on_replace_failure(tmp_path, monkeypatch):
    import importlib

    module = importlib.import_module("pinjamlab.io.atomic_writer")
    target = tmp_path / "report.txt"
    target.write_text("old", encoding="utf-8")

    def fail_replace(source, destination):
        raise OSError("replace failed")

    monkeypatch.setattr(module.os, "replace", fail_replace)
    with pytest.raises(OSError, match="replace failed"):
        with module.atomic_writer(target) as handle:
            handle.write("new")
    assert handle.closed
    assert target.read_text(encoding="utf-8") == "old"
    assert list(tmp_path.iterdir()) == [target]


def test_atomic_writer_uses_unique_temporary_files(tmp_path):
    from pinjamlab.io.atomic_writer import atomic_writer

    target = tmp_path / "report.txt"
    with atomic_writer(target) as first:
        with atomic_writer(target) as second:
            assert first.name != second.name
            second.write("second")
        first.write("first")
    assert target.read_text(encoding="utf-8") == "first"
    assert list(tmp_path.iterdir()) == [target]


def test_atomic_writer_cleans_up_on_write_failure(tmp_path):
    from pinjamlab.io.atomic_writer import atomic_writer

    target = tmp_path / "report.txt"
    with pytest.raises(TypeError):
        with atomic_writer(target) as handle:
            handle.write(b"not text")
    assert handle.closed
    assert list(tmp_path.iterdir()) == []


def test_atomic_writer_cleans_up_on_base_exception(tmp_path):
    from pinjamlab.io.atomic_writer import atomic_writer

    target = tmp_path / "report.txt"
    with pytest.raises(KeyboardInterrupt):
        with atomic_writer(target) as handle:
            handle.write("partial")
            raise KeyboardInterrupt()
    assert handle.closed
    assert list(tmp_path.iterdir()) == []
