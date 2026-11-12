"""Reconstructed teaching baseline, not the missing original m3-start."""
import csv
from dataclasses import dataclass
import re
import sys

@dataclass
class Loan:
    tag: st
    member: st
    days: int

@dataclass
class Member:
    active: int

    def recordLoan(self):
        if self.active >= 2:
            raise RuntimeError(f"Loan quota exceeded: {self.active} active, limit 2")
        self.active += 1

def parse(path):
    with open(path, newline="", encoding="utf-8") as source:
        reader = csv.reader(source)
        next(reader, None)
        for row, fields in enumerate(reader, 1):
            if fields:
                yield row, (fields + ["", "", ""])[:3]

def rules(fields, equipment, members):
    tag, member, raw_days = fields
    if not tag:
        raise RuntimeError("tag is empty")
    if not member:
        raise RuntimeError("memberId is empty")
    if not re.fullmatch(r"[+-]?[0-9]+", raw_days):
        raise RuntimeError(f"days is not a number: {raw_days}")
    days = int(raw_days)
    if not -(2**31) <= days < 2**31:
        raise RuntimeError(f"days is not a number: {raw_days}")
    if days <= 0:
        raise RuntimeError(f"days must be positive, got {days}")
    if tag not in equipment:
        raise RuntimeError(f"Unknown asset tag: {tag}")
    if member not in members:
        raise RuntimeError(f"Unknown member: {member}")
    if days > 90:
        raise RuntimeError(f"Loan duration exceeds maximum: {days} > 90")
    if not equipment[tag]:
        raise RuntimeError(f"Equipment already on loan: {tag}")
    loan = Loan(tag, member, days)
    members[member].recordLoan()
    equipment[tag] = False
    return loan

def print_loan(row, loan):
    print(f"row {row}: loan created: {loan.tag}")

def main(argv):
    if len(argv) != 2:
        print("usage: pinjamlab INPUT.csv", file=sys.stderr)
        return 2
    equipment = {"LP-001": True, "LP-002": False, "LP-003": True}
    members = {"M-101": Member(0), "M-102": Member(2), "M-103": Member(1)}
    failed = False
    try:
        for row, fields in parse(argv[1]):
            try:
                print_loan(row, rules(fields, equipment, members))
            except Exception as error:
                print(f"row {row}: {error}", file=sys.stderr)
                failed = True
    except Exception as error:
        message = f"cannot open input: {argv[1]}" if isinstance(error, OSError) else str(error)
        print(message, file=sys.stderr)
        failed = True
    return 1 if failed else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
