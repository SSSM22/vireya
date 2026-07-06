import sys
import unittest
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from vireya.customers import CustomerProfile
from vireya.governance import AuditEntry, PricingOverride, SettlementReport, TenantAccessController
from vireya.inventory import InventoryBatch, InventoryManager, WasteEntry
from vireya.kitchen import KitchenTicket, KitchenTicketService
from vireya.menu import MenuCategory, MenuVersion, Promotion
from vireya.migration import MigrationImport, MigrationIssue
from vireya.reporting import BranchDashboard
from vireya.shifts import ShiftRecord


class KitchenStoryTests(unittest.TestCase):
    def test_kitchen_ticket_is_created_and_prioritized(self):
        service = KitchenTicketService()
        ticket = service.create_ticket("T1", [{"name": "Dosa", "quantity": 2, "special_request": "extra chutney"}])
        service.add_ticket(ticket)
        self.assertEqual(ticket.ticket_id, "T1")
        self.assertEqual(ticket.items[0].special_request, "extra chutney")
        self.assertEqual(service.priority_queue()[0].ticket_id, "T1")

    def test_kitchen_ticket_supports_status_updates_and_rejections(self):
        ticket = KitchenTicket("T2", [{"name": "Coffee", "quantity": 1}])
        ticket.update_item_status("Coffee", "cooking")
        ticket.update_item_status("Coffee", "ready")
        ticket.hold_item("Coffee", "No milk")
        self.assertEqual(ticket.item_status("Coffee"), "held")
        self.assertEqual(ticket.audit_log[-1].reason, "No milk")


class InventoryStoryTests(unittest.TestCase):
    def test_inventory_receipt_flags_expiry_and_fifo_priority(self):
        manager = InventoryManager()
        manager.record_purchase("rice", 10, "B1", Decimal("100"), date(2026, 7, 20))
        manager.record_purchase("rice", 5, "B2", Decimal("90"), date(2026, 7, 10))
        batches = manager.batches_for("rice")
        self.assertEqual(len(batches), 2)
        self.assertTrue(batches[0].is_expiring_soon)
        self.assertTrue(batches[1].is_fifo)

    def test_bom_deduction_and_waste_variance(self):
        manager = InventoryManager()
        manager.add_stock("rice", 20)
        manager.add_stock("curry", 10)
        manager.link_recipe("Dosa", {"rice": 2, "curry": 1})
        manager.deduct_recipe("Dosa")
        self.assertEqual(manager.stock_level("rice"), 18)
        self.assertEqual(manager.stock_level("curry"), 9)
        manager.log_waste("spoilage", 2, Decimal("20"), "left out")
        self.assertEqual(manager.variance_alerts(), ["variance-exceeds-threshold"])


class GovernanceStoryTests(unittest.TestCase):
    def test_tenant_access_is_blocked_and_audited(self):
        controller = TenantAccessController()
        self.assertFalse(controller.can_access("branch-2", tenant_scope="branch-1", action="view", user_id="user-5"))
        controller.audit_action("branch-2", "delete", "user-5")
        self.assertEqual(controller.audit_log[-1].action, "delete")

    def test_sensitive_action_is_audited_with_before_and_after_state(self):
        controller = TenantAccessController()
        controller.audit_sensitive_change(
            tenant_scope="branch-1",
            action="refund",
            user_id="manager-1",
            before_state={"status": "open"},
            after_state={"status": "refunded"},
        )
        self.assertEqual(controller.audit_log[-1].action, "refund")
        self.assertEqual(controller.audit_log[-1].before_state["status"], "open")
        self.assertEqual(controller.audit_log[-1].after_state["status"], "refunded")

    def test_role_permissions_limit_visible_screens(self):
        controller = TenantAccessController()
        self.assertIn("billing", controller.visible_screens("cashier"))
        self.assertNotIn("settlement", controller.visible_screens("cashier"))
        self.assertFalse(controller.can_perform("cashier", "refund"))
        self.assertTrue(controller.can_perform("manager", "refund"))

    def test_pricing_override_and_settlement_report(self):
        override = PricingOverride("branch-1", "Paneer Pizza", Decimal("250"), "summer")
        self.assertEqual(override.applies_to_scope("branch-1"), True)
        report = SettlementReport(Decimal("1000"), Decimal("950"))
        self.assertEqual(report.variance, Decimal("50"))
        self.assertTrue(report.has_variance)


class ReportingAndCustomerStoryTests(unittest.TestCase):
    def test_dashboard_summarises_branch_operational_state(self):
        dashboard = BranchDashboard()
        dashboard.add_pending_order("P1")
        dashboard.add_offline_alert("branch offline")
        dashboard.add_stock_warning("rice")
        dashboard.add_approval("refund")
        summary = dashboard.summary()
        self.assertIn("pending-orders", summary)
        self.assertIn("offline-alerts", summary)

    def test_customer_profile_tracks_loyalty_points(self):
        profile = CustomerProfile("C1", "Asha")
        profile.add_visit()
        profile.accrue_points(100)
        profile.redeem_points(40)
        self.assertEqual(profile.loyalty_points, 60)
        self.assertEqual(profile.visit_count, 1)


class MenuAndStaffAndMigrationStoryTests(unittest.TestCase):
    def test_menu_version_and_promotion_are_scoped(self):
        version = MenuVersion("v2", "summer")
        version.add_item("Cooler")
        promotion = Promotion("summer", "branch-1", datetime(2026, 7, 1), datetime(2026, 7, 31))
        self.assertTrue(version.is_active)
        self.assertTrue(promotion.is_active_on(date(2026, 7, 15)))

    def test_shift_record_and_migration_import_are_auditable(self):
        shift = ShiftRecord("S1", "branch-1")
        shift.start_shift()
        shift.end_shift()
        self.assertEqual(shift.state, "ended")
        import_job = MigrationImport("legacy.csv")
        import_job.validate_row({"id": "1", "name": "A"})
        import_job.mark_issue("missing field")
        self.assertEqual(import_job.audit_log[-1].message, "missing field")


if __name__ == "__main__":
    unittest.main()
