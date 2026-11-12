"""io layer: turns bytes on disk into raw, untyped rows. Deliberately does
NOT interpret "days" as a number here -- that decision belongs to Validator.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class RawRow:
    line_number: int  # physical line, excluding the header's lines
    tag: str
    member_id: str
    days_raw: str


class CsvReader:
    def read(self, path: str | Path) -> list[RawRow]:
        rows: list[RawRow] = []
        with open(path, newline="", encoding="utf-8") as fh:
            reader = csv.reader(fh)
            next(reader, None)  # header, discarded
            header_lines = reader.line_num
            while True:
                i = reader.line_num - header_lines + 1
                fields = next(reader, None)
                if fields is None:
                    break
                if not fields:
                    continue
                tag = fields[0] if len(fields) > 0 else ""
                member_id = fields[1] if len(fields) > 1 else ""
                days_raw = fields[2] if len(fields) > 2 else ""
                rows.append(RawRow(i, tag, member_id, days_raw))
        return rows
