"""app layer: the fixed starting roster and catalogue that bad-requests.csv
is written against. Mirrors cpp/include/pinjamlab/app/seed.hpp exactly --
see that file for why each seed step exists.
"""
from __future__ import annotations

from ..domain.equipment import Equipment
from ..domain.member import Member, Role
from ..service.loan_service import LoanService


def seed_pinjamlab(svc: LoanService) -> None:
    svc.add_equipment(Equipment("LP-001", "ThinkPad T14"))
    svc.add_equipment(Equipment("LP-002", "Latitude 5440"))
    svc.add_equipment(Equipment("LP-003", "ProBook 450"))
    svc.add_equipment(Equipment("SEED-01", "Seed placeholder A"))
    svc.add_equipment(Equipment("SEED-02", "Seed placeholder B"))

    svc.add_member(Member("M-101", "Ayu Lestari", Role.STUDENT))
    svc.add_member(Member("M-102", "Budi Santoso", Role.STUDENT))
    svc.add_member(Member("M-103", "Citra Dewi", Role.STUDENT))

    svc.borrow("LP-002", "M-103", 5)   # LP-002 -> Loaned; M-103 -> 1 active
    svc.borrow("SEED-01", "M-102", 5)  # M-102 -> 1 active
    svc.borrow("SEED-02", "M-102", 5)  # M-102 -> 2 active == limit
