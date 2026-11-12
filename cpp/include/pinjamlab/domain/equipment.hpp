#ifndef PINJAMLAB_DOMAIN_EQUIPMENT_HPP
#define PINJAMLAB_DOMAIN_EQUIPMENT_HPP

// PURE domain header: entity carried forward from Modules 1-2. Module 3 does
// not need the polymorphic Equipment hierarchy (that lesson is done); this is
// the concrete shape LoanService actually holds in its catalogue.

#include "pinjamlab/domain/loan_error.hpp"

#include <string>
#include <utility>

namespace pinjamlab {

enum class EquipmentState { Available, Loaned };

class Equipment {
    std::string tag_;
    std::string model_;
    EquipmentState state_ = EquipmentState::Available;
    std::string reservedFor_;  // Empty means no reservation.

public:
    Equipment(std::string tag, std::string model, std::string reservedFor = "")
        : tag_(std::move(tag)), model_(std::move(model)),
          reservedFor_(std::move(reservedFor)) {}
    [[nodiscard]] const std::string& reservedFor() const noexcept { return reservedFor_; }

    [[nodiscard]] const std::string& tag() const noexcept { return tag_; }
    [[nodiscard]] const std::string& model() const noexcept { return model_; }
    [[nodiscard]] EquipmentState state() const noexcept { return state_; }
    [[nodiscard]] bool isAvailable() const noexcept { return state_ == EquipmentState::Available; }

    void markLoaned() {
        if (!isAvailable()) throw EquipmentUnavailable(tag_);
        state_ = EquipmentState::Loaned;
    }

    void markReturned() { state_ = EquipmentState::Available; }
};

}  // namespace pinjamlab

#endif  // PINJAMLAB_DOMAIN_EQUIPMENT_HPP
