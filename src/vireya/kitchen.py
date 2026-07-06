from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List


@dataclass
class KitchenItem:
    name: str
    quantity: int
    special_request: str | None = None
    modifiers: List[str] = field(default_factory=list)
    status: str = "pending"


@dataclass
class KitchenAuditEvent:
    action: str
    reason: str | None = None


@dataclass
class KitchenTicket:
    ticket_id: str
    items: List[KitchenItem]
    priority: int = 0
    source: str = "pos"
    audit_log: List[KitchenAuditEvent] = field(default_factory=list)
    waiting_since: datetime | None = None
    stale_indicator: str = "fresh"

    def __init__(self, ticket_id: str, item_specs: List[dict], priority: int = 0, source: str = "pos") -> None:
        self.ticket_id = ticket_id
        self.items = [KitchenItem(**spec) for spec in item_specs]
        self.priority = priority
        self.source = source
        self.audit_log = []
        self.waiting_since = None
        self.stale_indicator = "fresh"

    def update_item_status(self, item_name: str, status: str) -> None:
        for item in self.items:
            if item.name == item_name:
                item.status = status
                self.audit_log.append(KitchenAuditEvent(action="status", reason=status))
                return
        raise KeyError(item_name)

    def hold_item(self, item_name: str, reason: str) -> None:
        for item in self.items:
            if item.name == item_name:
                item.status = "held"
                self.audit_log.append(KitchenAuditEvent(action="hold", reason=reason))
                return
        raise KeyError(item_name)

    def reject_item(self, item_name: str, reason: str) -> None:
        for item in self.items:
            if item.name == item_name:
                item.status = "rejected"
                self.audit_log.append(KitchenAuditEvent(action="reject", reason=reason))
                return
        raise KeyError(item_name)

    def update_item(self, item_name: str, quantity: int | None = None, special_request: str | None = None) -> None:
        for item in self.items:
            if item.name == item_name:
                if quantity is not None:
                    item.quantity = quantity
                if special_request is not None:
                    item.special_request = special_request
                self.audit_log.append(KitchenAuditEvent(action="modify", reason="updated"))
                return
        raise KeyError(item_name)

    def item_status(self, item_name: str) -> str:
        for item in self.items:
            if item.name == item_name:
                return item.status
        raise KeyError(item_name)

    def mark_waiting_since(self, timestamp: datetime) -> None:
        self.waiting_since = timestamp
        self.stale_indicator = "fresh"

    def is_stale(self, waiting_threshold_minutes: int = 15, now: datetime | None = None) -> bool:
        if self.waiting_since is None:
            return False
        current_time = now or datetime.now()
        stale = (current_time - self.waiting_since).total_seconds() >= waiting_threshold_minutes * 60
        if stale:
            self.stale_indicator = "stale"
        return stale

    def mark_stale(self) -> None:
        self.stale_indicator = "stale"


class KitchenTicketService:
    def __init__(self) -> None:
        self._tickets: List[KitchenTicket] = []

    def create_ticket(self, ticket_id: str, item_specs: List[dict], priority: int = 0, source: str = "pos") -> KitchenTicket:
        return KitchenTicket(ticket_id, item_specs, priority=priority, source=source)

    def submit_order(self, order: Dict[str, Any]) -> KitchenTicket:
        item_specs: List[dict] = []
        for item in order.get("items", []):
            spec: Dict[str, Any] = {
                "name": item["name"],
                "quantity": item.get("quantity", 1),
                "special_request": item.get("special_request"),
            }
            if "modifiers" in item:
                spec["modifiers"] = list(item.get("modifiers", []))
            item_specs.append(spec)

        ticket = self.create_ticket(
            order.get("order_id", f"KOT-{len(self._tickets) + 1}"),
            item_specs,
            priority=order.get("priority", 0),
            source=order.get("source", "pos"),
        )
        self.add_ticket(ticket)
        return ticket

    def add_ticket(self, ticket: KitchenTicket) -> None:
        self._tickets.append(ticket)

    def priority_queue(self) -> List[KitchenTicket]:
        return sorted(self._tickets, key=lambda ticket: ticket.priority, reverse=True)
