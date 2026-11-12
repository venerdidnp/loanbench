#ifndef PINJAMLAB_APP_SEED_HPP
#define PINJAMLAB_APP_SEED_HPP

// app layer: the fixed starting roster and catalogue that bad-requests.csv
// is written against. A real deployment would load this from a database
// (Module 5); Module 3 has no persistence yet, so the app layer is the
// legitimate place to construct it -- domain and service take these objects
// as parameters and never manufacture their own test data.

#include "pinjamlab/domain/equipment.hpp"
#include "pinjamlab/domain/member.hpp"
#include "pinjamlab/service/loan_service.hpp"

namespace pinjamlab {

// Seeds exactly the state the ten committed rows in bad-requests.csv assume:
//   LP-001    available                 (rows 7, 10 touch it and expect this)
//   LP-002    ALREADY LOANED to M-103    (row 8 expects EquipmentUnavailable)
//   LP-003    available                 (row 9 touches it; its failure is quota, not this)
//   SEED-01/02 exist only to bring M-102 to quota without touching LP-00x
//   M-101     Student, 0 active / 2 max (rows 6, 8, 10)
//   M-102     Student, 2 active / 2 max (row 9 expects QuotaExceeded)
//   M-103     Student, 1 active / 2 max (holds LP-002)
inline void seedPinjamLab(LoanService& svc) {
    svc.addEquipment(Equipment("LP-001", "ThinkPad T14"));
    svc.addEquipment(Equipment("LP-002", "Latitude 5440"));
    svc.addEquipment(Equipment("LP-003", "ProBook 450"));
    svc.addEquipment(Equipment("SEED-01", "Seed placeholder A"));
    svc.addEquipment(Equipment("SEED-02", "Seed placeholder B"));

    svc.addMember(Member("M-101", "Ayu Lestari", Role::Student));
    svc.addMember(Member("M-102", "Budi Santoso", Role::Student));
    svc.addMember(Member("M-103", "Citra Dewi", Role::Student));

    // Sequenced through the real borrow() path rather than poked directly,
    // so the seed itself exercises the same invariants the CSV rows do.
    (void)svc.borrow("LP-002", "M-103", 5);   // LP-002 -> Loaned; M-103 -> 1 active
    (void)svc.borrow("SEED-01", "M-102", 5);  // M-102 -> 1 active
    (void)svc.borrow("SEED-02", "M-102", 5);  // M-102 -> 2 active == limit
}

}  // namespace pinjamlab

#endif  // PINJAMLAB_APP_SEED_HPP
