"""Publish a text file only after its guarded write succeeds."""
from collections.abc import Iterator
from contextlib import contextmanager
import os
from pathlib import Path
import tempfile
from typing import TextIO


@contextmanager
def atomic_writer(path: str | Path) -> Iterator[TextIO]:
    destination = Path(path)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="",
            dir=destination.parent, prefix=f".{destination.name}.",
            suffix=".tmp", delete=False,
        ) as handle:
            temporary = Path(handle.name)
            yield handle
        os.replace(temporary, destination)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
