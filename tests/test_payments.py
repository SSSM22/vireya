import sys
import unittest
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from vireya.billing import MenuItem, PosBill


class PosBillPaymentTests(unittest.TestCase):
    def test_accepts_cash_payment_and_updates_bill_state(self):
        bill = PosBill(tax_rate=Decimal("0.10"))
        bill.add_item(MenuItem("Masala Dosa", Decimal("120")), quantity=1)

        bill.record_payment("cash", Decimal("132"))

        self.assertEqual(bill.payment_method, "cash")
        self.assertEqual(bill.amount_paid, Decimal("132"))
        self.assertTrue(bill.is_paid)

    def test_split_bill_allocation_and_remaining_balance(self):
        bill = PosBill(tax_rate=Decimal("0.10"))
        bill.add_item(MenuItem("Masala Dosa", Decimal("120")), quantity=2)

        bill.record_payment("cash", Decimal("100"))
        bill.add_split_payment("upi", Decimal("50"))

        self.assertEqual(bill.payment_method, "mixed")
        self.assertEqual(bill.remaining_balance, Decimal("114"))
        self.assertEqual(bill.amount_paid, Decimal("150"))
        self.assertFalse(bill.is_paid)

    def test_payment_failure_keeps_bill_recoverable(self):
        bill = PosBill(tax_rate=Decimal("0.10"))
        bill.add_item(MenuItem("Masala Dosa", Decimal("120")), quantity=1)

        bill.record_payment_failure("card", "gateway timeout")

        self.assertTrue(bill.payment_failed)
        self.assertEqual(bill.last_payment_failure_reason, "gateway timeout")
        self.assertFalse(bill.is_paid)
        self.assertEqual(bill.remaining_balance, Decimal("132"))


if __name__ == "__main__":
    unittest.main()
