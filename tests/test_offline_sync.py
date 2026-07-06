import sys
import unittest
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from vireya.billing import MenuItem, PosBill


class OfflineBillingTests(unittest.TestCase):
    def test_offline_bill_is_queued_and_synced_when_connection_returns(self):
        bill = PosBill(tax_rate=Decimal("0.10"))
        bill.add_item(MenuItem("Masala Dosa", Decimal("120")), quantity=1)

        bill.mark_offline()
        bill.record_payment("cash", Decimal("132"))

        self.assertTrue(bill.is_offline)
        self.assertEqual(bill.pending_sync_count, 1)

        bill.sync_now()

        self.assertFalse(bill.is_offline)
        self.assertEqual(bill.pending_sync_count, 0)
        self.assertEqual(bill.sync_status, "synced")

    def test_offline_status_banner_is_available(self):
        bill = PosBill(tax_rate=Decimal("0.10"))

        self.assertEqual(bill.offline_banner(), "Offline mode active")


if __name__ == "__main__":
    unittest.main()
