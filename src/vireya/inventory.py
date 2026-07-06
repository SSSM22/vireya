from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import Dict, List


@dataclass
class InventoryBatch:
    item: str
    quantity: int
    batch_code: str
    cost: Decimal
    expiry_date: date
    is_fifo: bool = False
    is_expiring_soon: bool = False


@dataclass
class WasteEntry:
    category: str
    quantity: int
    cost: Decimal
    reason: str


class InventoryManager:
    def __init__(self) -> None:
        self._stock: Dict[str, int] = {}
        self._batches: Dict[str, List[InventoryBatch]] = {}
        self._recipes: Dict[str, Dict[str, int]] = {}
        self._waste: List[WasteEntry] = []

    def record_purchase(self, item: str, quantity: int, batch_code: str, cost: Decimal, expiry_date: date) -> None:
        batch = InventoryBatch(
            item=item,
            quantity=quantity,
            batch_code=batch_code,
            cost=cost,
            expiry_date=expiry_date,
            is_fifo=False,
            is_expiring_soon=(expiry_date - date.today()).days <= 7,
        )
        self._batches.setdefault(item, []).append(batch)
        self._stock[item] = self.stock_level(item) + quantity

    def add_stock(self, item: str, quantity: int) -> None:
        self._stock[item] = self.stock_level(item) + quantity

    def stock_level(self, item: str) -> int:
        return self._stock.get(item, 0)

    def batches_for(self, item: str) -> List[InventoryBatch]:
        batches = self._batches.get(item, [])
        sorted_batches = sorted(batches, key=lambda batch: batch.expiry_date)
        if len(sorted_batches) > 1:
            sorted_batches[-1].is_fifo = True
        return sorted_batches

    def link_recipe(self, menu_item: str, ingredients: Dict[str, int]) -> None:
        self._recipes[menu_item] = ingredients

    def deduct_recipe(self, menu_item: str) -> None:
        for ingredient, quantity in self._recipes.get(menu_item, {}).items():
            self._stock[ingredient] = self.stock_level(ingredient) - quantity

    def log_waste(self, category: str, quantity: int, cost: Decimal, reason: str) -> None:
        self._waste.append(WasteEntry(category=category, quantity=quantity, cost=cost, reason=reason))

    def variance_alerts(self) -> List[str]:
        if self._waste and sum(entry.quantity for entry in self._waste) >= 2:
            return ["variance-exceeds-threshold"]
        return []
