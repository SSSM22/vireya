from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, List


@dataclass(frozen=True)
class PaymentAllocation:
    method: str
    amount: Decimal


@dataclass(frozen=True)
class MenuItem:
    name: str
    price: Decimal


class PosBill:
    def __init__(self, tax_rate: Decimal = Decimal("0.00")) -> None:
        self.tax_rate = tax_rate
        self._items: Dict[str, Dict[str, object]] = {}
        self._payments: List[PaymentAllocation] = []
        self._payment_failure_reason: str | None = None
        self._is_offline = False
        self._pending_sync_count = 0
        self._sync_status = "ready"

    def add_item(self, item: MenuItem, quantity: int = 1) -> None:
        if quantity <= 0:
            raise ValueError("quantity must be positive")

        existing = self._items.get(item.name)
        if existing is None:
            self._items[item.name] = {"item": item, "quantity": quantity}
        else:
            existing["quantity"] = int(existing["quantity"]) + quantity

    def update_quantity(self, name: str, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("quantity must be positive")

        if name not in self._items:
            raise KeyError(name)

        self._items[name]["quantity"] = quantity

    def remove_item(self, name: str) -> None:
        if name not in self._items:
            raise KeyError(name)

        del self._items[name]

    @property
    def subtotal(self) -> Decimal:
        return sum((entry["item"].price * int(entry["quantity"]) for entry in self._items.values()), Decimal("0"))

    @property
    def tax_amount(self) -> Decimal:
        return (self.subtotal * self.tax_rate).quantize(Decimal("0.01"))

    @property
    def total(self) -> Decimal:
        return (self.subtotal + self.tax_amount).quantize(Decimal("0.01"))

    def item_names(self) -> List[str]:
        return list(self._items.keys())

    def record_payment(self, method: str, amount: Decimal) -> None:
        if amount <= 0:
            raise ValueError("amount must be positive")
        self._payments.append(PaymentAllocation(method=method, amount=amount))
        if self._is_offline:
            self._pending_sync_count += 1
            self._sync_status = "queued"

    def add_split_payment(self, method: str, amount: Decimal) -> None:
        self.record_payment(method, amount)

    def record_payment_failure(self, method: str, reason: str) -> None:
        self._payment_failure_reason = reason

    def mark_offline(self) -> None:
        self._is_offline = True
        self._sync_status = "offline"

    def sync_now(self) -> None:
        if self._pending_sync_count > 0:
            self._pending_sync_count = 0
        self._is_offline = False
        self._sync_status = "synced"

    def offline_banner(self) -> str:
        return "Offline mode active"

    @property
    def payment_failed(self) -> bool:
        return self._payment_failure_reason is not None

    @property
    def last_payment_failure_reason(self) -> str | None:
        return self._payment_failure_reason

    @property
    def payment_method(self) -> str:
        if not self._payments:
            return "unpaid"
        if len(self._payments) == 1:
            return self._payments[0].method
        return "mixed"

    @property
    def amount_paid(self) -> Decimal:
        return sum((payment.amount for payment in self._payments), Decimal("0"))

    @property
    def remaining_balance(self) -> Decimal:
        return (self.total - self.amount_paid).quantize(Decimal("0.01"))

    @property
    def is_paid(self) -> bool:
        return self.amount_paid >= self.total

    @property
    def is_offline(self) -> bool:
        return self._is_offline

    @property
    def pending_sync_count(self) -> int:
        return self._pending_sync_count

    @property
    def sync_status(self) -> str:
        return self._sync_status
