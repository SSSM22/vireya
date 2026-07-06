from __future__ import annotations

import argparse
import sys
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from vireya.billing import MenuItem, PosBill
from vireya.kitchen import KitchenTicketService
from vireya.reporting import BranchDashboard


def build_demo_bill() -> PosBill:
    bill = PosBill(tax_rate=Decimal("0.10"))
    bill.add_item(MenuItem("Masala Dosa", Decimal("120")), quantity=2)
    bill.add_item(MenuItem("Coffee", Decimal("60")), quantity=1)
    return bill


def run_demo() -> dict:
    bill = build_demo_bill()
    dashboard = BranchDashboard()
    dashboard.add_pending_order("KOT-100")
    dashboard.add_offline_alert("branch offline")
    dashboard.add_stock_warning("rice")
    dashboard.add_approval("refund")

    service = KitchenTicketService()
    service.submit_order(
        {
            "order_id": "KOT-100",
            "priority": 3,
            "source": "qr",
            "items": [{"name": "Masala Dosa", "quantity": 2, "special_request": "extra chutney"}],
        }
    )

    return {
        "bill_total": str(bill.total),
        "bill_subtotal": str(bill.subtotal),
        "bill_tax": str(bill.tax_amount),
        "dashboard": dashboard.summary(),
        "tickets": [ticket.ticket_id for ticket in service.priority_queue()],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Vireya MVP demo")
    parser.add_argument("--demo", action="store_true", help="Run the built-in domain demo")
    args = parser.parse_args()

    if args.demo:
        print(run_demo())
        return

    parser.print_help()


if __name__ == "__main__":
    main()
