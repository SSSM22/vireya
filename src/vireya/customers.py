from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CustomerProfile:
    customer_id: str
    name: str
    loyalty_points: int = 0
    visit_count: int = 0

    def add_visit(self) -> None:
        self.visit_count += 1

    def accrue_points(self, points: int) -> None:
        self.loyalty_points += points

    def redeem_points(self, points: int) -> None:
        self.loyalty_points -= points
