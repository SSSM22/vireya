from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ShiftRecord:
    shift_id: str
    branch_id: str
    state: str = "open"
    attendance_logged: bool = False
    cash_variance: bool = False

    def start_shift(self) -> None:
        self.state = "active"
        self.attendance_logged = True

    def end_shift(self) -> None:
        self.state = "ended"
        self.cash_variance = True
