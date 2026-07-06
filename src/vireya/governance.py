from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import List


@dataclass
class AuditEntry:
    tenant_scope: str
    action: str
    user_id: str


class TenantAccessController:
    def __init__(self) -> None:
        self.audit_log: List[AuditEntry] = []

    def can_access(self, requested_scope: str, *, tenant_scope: str | None = None) -> bool:
        if tenant_scope is None:
            return True
        return requested_scope == tenant_scope

    def audit_action(self, tenant_scope: str, action: str, user_id: str) -> None:
        self.audit_log.append(AuditEntry(tenant_scope=tenant_scope, action=action, user_id=user_id))


@dataclass
class PricingOverride:
    scope: str
    item_name: str
    price: Decimal
    variant: str

    def applies_to_scope(self, scope: str) -> bool:
        return self.scope == scope


@dataclass
class SettlementReport:
    expected_total: Decimal
    recorded_total: Decimal

    @property
    def variance(self) -> Decimal:
        return self.expected_total - self.recorded_total

    @property
    def has_variance(self) -> bool:
        return self.variance != Decimal("0")
