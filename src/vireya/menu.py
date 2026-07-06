from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List


@dataclass
class MenuCategory:
    name: str
    items: List[str] = field(default_factory=list)


@dataclass
class MenuVersion:
    version_id: str
    scope: str
    items: List[str] = field(default_factory=list)

    def add_item(self, item_name: str) -> None:
        self.items.append(item_name)

    @property
    def is_active(self) -> bool:
        return True


@dataclass
class Promotion:
    name: str
    scope: str
    starts_on: datetime
    ends_on: datetime

    def is_active_on(self, target_date: date) -> bool:
        return self.starts_on.date() <= target_date <= self.ends_on.date()
