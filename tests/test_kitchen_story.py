import sys
import unittest
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from vireya.kitchen import KitchenTicket, KitchenTicketService


class KitchenStoryTests(unittest.TestCase):
    def test_submit_order_creates_a_prioritized_kot_ticket(self):
        service = KitchenTicketService()
        order = {
            "order_id": "KOT-100",
            "priority": 3,
            "source": "qr",
            "items": [
                {
                    "name": "Dosa",
                    "quantity": 2,
                    "special_request": "extra chutney",
                    "modifiers": ["spicy"],
                }
            ],
        }

        ticket = service.submit_order(order)

        self.assertEqual(ticket.ticket_id, "KOT-100")
        self.assertEqual(ticket.priority, 3)
        self.assertEqual(ticket.source, "qr")
        self.assertEqual(ticket.items[0].special_request, "extra chutney")

        service.add_ticket(ticket)
        self.assertEqual(service.priority_queue()[0].ticket_id, "KOT-100")

    def test_partial_fulfillment_and_stale_indicator_are_supported(self):
        ticket = KitchenTicket("T2", [{"name": "Coffee", "quantity": 1}, {"name": "Dosa", "quantity": 2}])
        ticket.update_item_status("Coffee", "ready")
        ticket.update_item_status("Coffee", "served")
        ticket.update_item_status("Dosa", "cooking")

        self.assertEqual(ticket.item_status("Coffee"), "served")
        self.assertEqual(ticket.item_status("Dosa"), "cooking")

        ticket.mark_waiting_since(datetime(2026, 7, 6, 9, 0, 0))
        self.assertTrue(ticket.is_stale(waiting_threshold_minutes=15, now=datetime(2026, 7, 6, 9, 20, 0)))
        self.assertEqual(ticket.stale_indicator, "stale")

    def test_hold_reject_and_order_change_are_recorded(self):
        ticket = KitchenTicket("T3", [{"name": "Tea", "quantity": 1}])

        ticket.hold_item("Tea", "No milk")
        self.assertEqual(ticket.item_status("Tea"), "held")
        self.assertEqual(ticket.audit_log[-1].reason, "No milk")

        ticket.reject_item("Tea", "Out of stock")
        self.assertEqual(ticket.item_status("Tea"), "rejected")
        self.assertEqual(ticket.audit_log[-1].reason, "Out of stock")

        ticket.update_item("Tea", quantity=2, special_request="less sugar")
        self.assertEqual(ticket.items[0].quantity, 2)
        self.assertEqual(ticket.items[0].special_request, "less sugar")
        self.assertEqual(ticket.audit_log[-1].action, "modify")


if __name__ == "__main__":
    unittest.main()
