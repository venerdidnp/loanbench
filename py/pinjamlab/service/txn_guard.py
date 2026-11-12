"""The @contextmanager equivalent of service/txn_guard.hpp's RAII guard.

Everything before `yield` is acquisition; everything after is release. The
`raise` in the except clause is essential -- without it this would silently
swallow every exception from the body, which is the defect Lab 2 asks you
to find in the wild.
"""
from __future__ import annotations

import sys
from collections.abc import Iterator
from contextlib import contextmanager

from .database import Database


@contextmanager
def txn_guard(db: Database) -> Iterator[Database]:
    db.begin()  # acquire
    try:
        yield db  # the body of the `with` runs here
    except Exception:
        try:
            db.rollback()  # released on the exception path
        except Exception:
            # Swallowing here is correct, and almost nowhere else: an
            # exception escaping __exit__ during unwinding would replace
            # the original exception instead of adding to it.
            print("rollback failed during unwind", file=sys.stderr)
        raise  # ...and the error keeps travelling
    else:
        db.commit()  # released on the success path
