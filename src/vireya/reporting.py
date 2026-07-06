from __future__ import annotations

from typing import List


class BranchDashboard:
    def __init__(self) -> None:
        self.pending_orders: List[str] = []
        self.offline_alerts: List[str] = []
        self.stock_warnings: List[str] = []
        self.approvals: List[str] = []

    def add_pending_order(self, order_id: str) -> None:
        self.pending_orders.append(order_id)

    def add_offline_alert(self, message: str) -> None:
        self.offline_alerts.append(message)

    def add_stock_warning(self, item: str) -> None:
        self.stock_warnings.append(item)

    def add_approval(self, approval: str) -> None:
        self.approvals.append(approval)

    def summary(self) -> dict:
        return {
            "pending-orders": len(self.pending_orders),
            "offline-alerts": len(self.offline_alerts),
            "stock-warnings": len(self.stock_warnings),
            "approvals": len(self.approvals),
        }
