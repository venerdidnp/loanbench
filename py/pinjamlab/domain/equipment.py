"""Pure domain module: Equipment entity, carried forward from Modules 1-2."""
from __future__ import annotations

from enum import Enum, auto

from .loan_error import EquipmentUnavailable


class EquipmentState(Enum):
    AVAILABLE = auto()
    LOANED = auto()


class Equipment:
    def __init__(self, tag: str, model: str, reserved_for: str = "") -> None:
        self.tag = tag
        self.model = model
        self.reserved_for = reserved_for
        self._state = EquipmentState.AVAILABLE

    @property
    def state(self) -> EquipmentState:
        return self._state

    def is_available(self) -> bool:
        return self._state == EquipmentState.AVAILABLE

    def mark_loaned(self) -> None:
        if not self.is_available():
            raise EquipmentUnavailable(self.tag)
        self._state = EquipmentState.LOANED

    def mark_returned(self) -> None:
        self._state = EquipmentState.AVAILABLE
