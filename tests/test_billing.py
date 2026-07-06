import sys
import unittest
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from vireya.billing import MenuItem, PosBill


class PosBillTests(unittest.TestCase):
    def test_bill_updates_totals_when_items_are_added_and_quantity_changes(self):
        bill = PosBill(tax_rate=Decimal("0.10"))

        bill.add_item(MenuItem("Masala Dosa", Decimal("120")), quantity=2)
        bill.add_item(MenuItem("Coffee", Decimal("60")), quantity=1)

        self.assertEqual(bill.subtotal, Decimal("300"))
        self.assertEqual(bill.tax_amount, Decimal("30"))
        self.assertEqual(bill.total, Decimal("330"))

        bill.update_quantity("Masala Dosa", 3)

        self.assertEqual(bill.subtotal, Decimal("420"))
        self.assertEqual(bill.tax_amount, Decimal("42"))
        self.assertEqual(bill.total, Decimal("462"))

    def test_bill_recalculates_after_removing_an_item(self):
        bill = PosBill(tax_rate=Decimal("0.10"))

        bill.add_item(MenuItem("Masala Dosa", Decimal("120")), quantity=1)
        bill.add_item(MenuItem("Coffee", Decimal("60")), quantity=1)

        bill.remove_item("Coffee")

        self.assertEqual(bill.item_names(), ["Masala Dosa"])
        self.assertEqual(bill.subtotal, Decimal("120"))
        self.assertEqual(bill.tax_amount, Decimal("12"))
        self.assertEqual(bill.total, Decimal("132"))


if __name__ == "__main__":
    unittest.main()
