# Product Requirements Document (PRD)

## AFC Restaurant Management System

**Version:** 1.0

**Date:** 30 June 2026

**Status:** Draft PRD for stakeholder review

**Derived from:** 14 critical gap analysis + 209 requirements

---

## 1. Executive Summary

### 1.1 Purpose

This PRD defines the product requirements for the AFC Restaurant Management System, a cloud-enabled restaurant operations platform designed to support AFC-owned branches and franchise partners. The goal is to replace manual billing, inventory, and reporting workflows with a resilient, scalable, audit-ready system that supports rapid growth.

### 1.2 Scope

The initial delivery scope covers the critical MVP foundation for branch operations, including:

- POS billing and payment settlement
- Offline resilience and sync
- Franchise-ready multi-tenancy
- Inventory perishability and waste control
- Order flow edge cases and kitchen coordination
- Security, audit, and compliance
- Rush hour performance and reporting

Phase 1 expands analytics, dynamic menu management, customer loyalty, and staff monitoring. Phase 2 adds table/reservation workflows, QR ordering, and delivery enablement.

### 1.3 Success Criteria

The solution will be considered successful when it achieves:

- Billing time reduced by at least 50% during peak hours
- Real-time branch visibility across sales, inventory, and operations
- Offline POS operation with local transaction queueing and safe sync
- Audit trail for all payments, refunds, discounts, and order changes
- Franchise isolation with branch-level pricing, menu overrides, and revenue partitioning
- Inventory cost control with expiry tracking, BOM-based stock deduction, and waste categorization
- System stability under 100+ orders/hour peak load
- Centralized reporting for branch and corporate management

### 1.4 Key Risks

- **Architecture risk:** Multi-tenancy and offline sync must be designed early; retrofitting later will be expensive.
- **Financial risk:** Payment settlement, split bills, refunds, and audit trail are high-risk areas with direct revenue impact.
- **Operational risk:** Incomplete order flow handling or kitchen coordination will create customer service failures.
- **Data risk:** Poor inventory and waste tracking can lead to food safety issues and inaccurate profitability.
- **Performance risk:** If the platform cannot sustain rush hour load, the system may increase customer churn and revenue loss.

---

## 2. User Roles & Permissions

### 2.1 Role Definitions

| Role                  | Primary Responsibilities                                             | Key Permissions                                                            | Scope                                     |
| --------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------------- | ----------------------------------------- |
| **Owner**             | Oversees business performance and franchise operations               | Full system access, financial reports, franchise configuration, compliance | Global across all branches and franchises |
| **Branch Manager**    | Manages branch operations, staff, inventory, and reports             | Branch reports, staff assignments, approvals, inventory adjustments        | One branch                                |
| **Cashier**           | Executes billing, processes payments, manages customer checkouts     | POS billing, payment capture, split bills, reprints, cash reconciliation   | Branch-level sales only                   |
| **Kitchen Staff**     | Receives kitchen orders, updates item statuses, flags order issues   | View KOTs, mark items cooking/ready/served, reject or hold items           | Branch kitchen workflow                   |
| **Inventory Manager** | Controls purchasing, stock updates, waste entries, vendor management | Purchase entry, stock in/out, BOM management, expiry tracking              | Branch inventory only                     |

### 2.2 Permission Overview

Permission categories are defined for each role as follows:

- **Billing & payments:** Cashier, Branch Manager, Owner
- **Order management:** Cashier, Kitchen Staff, Branch Manager, Owner
- **Inventory management:** Inventory Manager, Branch Manager, Owner
- **Reports & analytics:** Branch Manager, Owner
- **Configuration:** Owner, Branch Manager (branch-specific); Owner only for franchise and system-level settings
- **Audit & security:** Owner, Branch Manager
- **Approvals:** Branch Manager, Owner

### 2.3 Enforcement Principles

- Apply Role-Based Access Control (RBAC) at UI and API layers.
- Use row-level security or tenant-scoped data filters to prevent data leakage.
- Log all permission-sensitive actions for audit and compliance.
- Soft delete data and preserve history to support incident investigation.

---

## 3. Feature Specs per Gap

Each feature specification below is anchored to a critical real-world scenario identified in the gap analysis.

### 3.1 Gap 1: Offline/Connectivity Resilience

#### Real-World Scenario

Friday 7:30 PM during dinner rush, network outage causes POS systems to stop processing bills. Customers wait, revenue is lost, and staff cannot continue selling.

#### Feature Spec

- **Offline Mode:** POS must continue to accept orders and payments when cloud connectivity is unavailable.
- **Local Transaction Queue:** Store transactions locally in a secure queue and synchronize when connectivity returns.
- **Menu Caching:** Cache the latest daily menu and pricing on the POS terminal at branch startup.
- **Order Status Sync:** Keep local KOT states for pending kitchen orders and reconcile status when reconnected.
- **Conflict Resolution:** Define merge rules for inventory, order, and payment updates after offline periods.
- **Staff Notification:** Display a clear offline mode banner and sync progress indicator.
- **Recovery SLA:** Ensure reconnection and sync complete within 5 minutes of network restoration.
- **Data Integrity:** Guarantee zero transaction loss and preserve audit trails for offline transactions.

### 3.2 Gap 2: Payment & Settlement Chaos

#### Real-World Scenario

A split bill with cash and UPI payments, a failed card transaction, and a cash drawer discrepancy leave ownership without a clear audit trail.

#### Feature Spec

- **Payment Gateway Integration:** Support UPI, credit/debit cards, and wallet payments through a validated gateway.
- **Cash Reconciliation:** Track opening/closing cash float per cashier and reconcile shift totals.
- **Split Bill Logic:** Allow multiple payment modes per order with individual settlement status.
- **Partial Payment Support:** Capture installments and maintain outstanding balance per order.
- **Refund & Reversal Workflow:** Require manager approval for refunds above threshold and log reversals.
- **Payment Failure Handling:** Preserve order state when payment fails and define retry/refund/cancellation flows.
- **Audit Trail:** Record every payment event with user, timestamp, amount, method, and status.
- **EOD Settlement Report:** Generate daily reports comparing cash counted vs system totals.

### 3.3 Gap 3: Inventory Perishability & Recipe Gaps

#### Real-World Scenario

Expired chicken is unknowingly used in 40 orders, and lack of BOM-based deduction means food cost is invisible.

#### Feature Spec

- **Expiry Tracking:** Record batch expiry dates and alert before expiration.
- **FIFO Rotation:** Prioritize older inventory for use and report out-of-rotation items.
- **Bill of Materials (BOM):** Link menu items to ingredient recipes.
- **Auto-Deduction:** Deduct ingredients automatically when orders are placed.
- **Waste Tracking:** Log spoilage, theft, trim, and discrepancy separately.
- **Stock-Out Procedure:** Handle unavailable ingredients by hiding menu items or suggesting substitutes.
- **Ingredient Substitution:** Track substitutions and adjust cost calculations.
- **Batch Reconciliation:** Compare physical counts against system records and flag >5% variance.

### 3.4 Gap 4: Order Flow Edge Cases

#### Real-World Scenario

A kitchen rejects an order mid-preparation, but the cashier and customer are not notified. The system still shows the order as completed.

#### Feature Spec

- **Kitchen Rejection Flow:** Kitchen staff can reject or hold an order item and notify cashier immediately.
- **Order Modification:** Allow order changes before kitchen begins cooking, with cost updates.
- **Item-Level Status:** Track item states: pending, cooking, ready, served, rejected.
- **Partial Fulfillment:** Support serving ready items separately from pending items.
- **Cancellation Workflow:** Manager approval required for cancellation above threshold, with refund initiation.
- **Stale Order Alerts:** Alert kitchen when orders exceed configurable waiting thresholds.
- **Special Requests Field:** Capture customer instructions and allergies on the KOT.
- **Remake Tracking:** Link remakes to the original order and preserve audit history.

### 3.5 Gap 5: Rush Hour Performance & Scalability

#### Real-World Scenario

Friday night rush generates 3 orders per minute. Billing lags, queues form, and customers leave before ordering.

#### Feature Spec

- **Throughput SLA:** System supports 100+ concurrent orders/hour with consistent response times.
- **Latency SLA:** End-to-end billing transaction latency should be under 2 seconds, p95 under 3 seconds.
- **Kitchen Display System (KDS):** Provide a visible, prioritized ticket board for kitchen staff.
- **Caching Strategy:** Cache menu, pricing, and session data to reduce backend load.
- **Connection Pooling:** Optimize database and gateway connections for high-concurrency operation.
- **Rate Limiting:** Handle external payment or API throttling gracefully.
- **Queue Visualization:** Display estimated wait times for incoming customers.
- **Stress Testing:** Validate the platform under sustained peak load.

### 3.6 Gap 6: Franchise Model & Multi-Tenancy

#### Real-World Scenario

A franchisee sees another branch's revenue and cannot use local pricing or royalty reporting.

#### Feature Spec

- **Multi-Tenancy:** Enforce data isolation per franchisee and branch.
- **Row-Level Security:** Ensure each user only accesses permitted tenant data.
- **Menu Override:** Allow franchisees to override central menu prices and availability.
- **Regional Variants:** Permit branch-specific menu additions and promotions.
- **Pricing Rules Engine:** Support base pricing plus regional and seasonal adjustments.
- **Royalty Tracking:** Calculate franchise royalty percentages on revenue.
- **Franchise Invoice Generation:** Generate monthly royalty invoices per franchisee.
- **Revenue Routing:** Support separate revenue tracking for franchise and corporate.
- **Compliance Config:** Allow tax rule configuration by region.
- **Feature Rollout:** Support staged release of features to franchise subsets.

### 3.7 Gap 7: Security & Compliance Blind Spots

#### Real-World Scenario

A cashier applies a large unauthorized discount while the system lacks a retrievable audit trail.

#### Feature Spec

- **Permission Matrix:** Define granular permissions per role and action.
- **Audit Trail:** Log every action, including before/after state for sensitive changes.
- **Soft Delete:** Preserve deleted records and record deletion metadata.
- **Access Logging:** Track logins, session duration, and source information.
- **Password Policy:** Enforce complexity, expiry, and reuse restrictions.
- **Session Timeout:** Auto-logout after inactivity.
- **Optional 2FA:** Provide two-factor authentication for high-privilege users.
- **Data Encryption:** Encrypt PII at rest and enforce TLS in transit.
- **Export Controls:** Restrict and log exports of sensitive data.
- **Compliance Reporting:** Generate audit-ready reports for tax and regulatory checks.

### 3.8 Gap 8: Profitability Metrics & Financial Analysis

#### Real-World Scenario

Branch A has higher revenue than Branch B, but Branch B is actually more profitable after costs and waste are considered.

#### Feature Spec

- **Margin Calculation:** Compute gross margin per item and category.
- **Food Cost %:** Track daily food cost as a percentage of revenue.
- **Waste Analysis:** Distinguish spoilage, theft, trim, and unaccounted loss.
- **Labor Efficiency:** Track payroll cost relative to revenue.
- **Turnover & AOV:** Monitor table turnover and average order value.
- **Customer Repeat Metrics:** Track repeat customer rate over 30 days.
- **Discount Impact:** Report discount percentage and trend.
- **Peak vs Off-Peak Analysis:** Compare revenue and order volume by time window.
- **Profitability Dashboard:** Surface branch comparisons and inefficiency flags.
- **Variance Reporting:** Flag deviations from budget thresholds.

### 3.9 Gap 9: Menu & Pricing Management

#### Real-World Scenario

A central menu price is not appropriate for a particular city, but the franchisee cannot adjust local pricing safely.

#### Feature Spec

- **Dynamic Pricing:** Support per-item pricing rules and overrides.
- **Menu Versioning:** Track menu changes and approval history.
- **Item Availability:** Mark menu items unavailable automatically when ingredients are out of stock.
- **Promotional Items:** Support promotional labels and time-bound offers.
- **Menu Categories:** Group items by category and enable easy navigation.
- **Combo/Bundles:** Support combo pricing and bundled discounts.
- **Allergen and Safety Info:** Display allergen data on items.
- **Seasonal Item Management:** Enable date-based menu item activation.
- **Price Override Audit:** Log manual price changes with justification.
- **Menu Rollout Control:** Roll out updates to select franchises or branches first.

### 3.10 Gap 10: Customer Data & Loyalty

#### Real-World Scenario

The restaurant has no customer purchase history and cannot identify returning customers or reward loyalty.

#### Feature Spec

- **Customer Capture:** Record customer contact and visit preferences at checkout.
- **Phone Lookup:** Look up returning customers by phone or email.
- **Visit Tracking:** Associate orders with customer profiles.
- **Loyalty Points:** Award points for repeat visits and spend thresholds.
- **Redemption Flow:** Allow points redemption at checkout.
- **Customer Segmentation:** Tag customers for future offers.
- **Birthday Offers:** Track birthdays and permit targeted promotions.
- **Feedback Collection:** Capture customer feedback from checkout.
- **Privacy Controls:** Allow data deletion and mask PII for non-authorized users.
- **Acquisition Metrics:** Measure new vs returning customer trends.

### 3.11 Gap 11: Staff Monitoring

#### Real-World Scenario

Staff attendance and cash variance are tracked manually, with limited visibility into productivity.

#### Feature Spec

- **Shift Management:** Manage cashier and kitchen staff shifts.
- **Attendance Logging:** Track login/logout times per user.
- **Overtime Tracking:** Calculate overtime for payroll reconciliation.
- **Cash Variance Alerts:** Flag drawer count discrepancies at shift end.
- **Performance Metrics:** Capture sales, order speed, and service quality indicators.
- **Payroll Export:** Export labor cost data for payroll systems.
- **Staff Productivity Dashboard:** Provide branch-level staff efficiency reporting.
- **Training Status:** Track training completion and certifications.
- **Incident Logging:** Record operational incidents linked to staff roles.
- **Role-Based Visibility:** Limit staff monitoring data to managers and owners.

### 3.12 Gap 12: Table Management (Phase 2)

#### Real-World Scenario

During peak dining hours, tables are double-booked and the waitlist is unmanaged.

#### Feature Spec

- **Reservations:** Capture and manage table bookings.
- **Waitlist Management:** Track waiting guests and estimated availability.
- **Table Merge / Split:** Support flexible table grouping for larger parties.
- **Occupancy Display:** Show live table status on floorplan.
- **Guest Flexibility Rules:** Automatically suggest table options for group size.
- **Service Time Tracking:** Measure table occupancy duration.
- **Reservation Reminders:** Notify guests of upcoming bookings.
- **VIP Handling:** Tag VIP guests and reserve priority seating.
- **Overbooking Prevention:** Validate availability before booking confirmation.
- **Table Turnover Analytics:** Report table usage and efficiency.

### 3.13 Gap 13: Data Migration

#### Real-World Scenario

Existing branch data exists in Excel and notebooks, requiring validation, cleansing, and parallel operation during cutover.

#### Feature Spec

- **Data Inventory:** Catalog legacy data sources before migration.
- **Validation Rules:** Define rules for customer, inventory, product, and sales data.
- **Cleansing Workflow:** Identify duplicates, invalid entries, and missing fields.
- **Migration Plan:** Sequence branch data migration with test and rollback steps.
- **Parallel Run:** Support running legacy process alongside the new system during transition.
- **Cutover Procedure:** Define go/no-go criteria and fallback conditions.
- **Reconciliation:** Verify migrated data against legacy totals.
- **Archive Legacy Data:** Preserve a backup snapshot of legacy source data.
- **Migration Audit:** Log all migration operations and corrections.
- **Training & Support:** Provide end-user training for data-entry and reconciliation.

### 3.14 Gap 14: QR Ordering & Delivery (Phase 2)

#### Real-World Scenario

Customers request QR-based ordering and delivery, but the current system only supports in-branch POS workflows.

#### Feature Spec

- **QR Menu Access:** Generate QR codes for table and takeout ordering.
- **Mobile Order Form:** Provide a mobile-friendly order capture interface.
- **Order Integration:** Route QR and delivery orders into the existing KOT and POS pipeline.
- **Delivery Address Capture:** Collect address and contact details for delivery orders.
- **Real-Time Status:** Display order status updates to customers.
- **Online Payment:** Accept payments from the mobile order channel.
- **ETA Calculator:** Estimate preparation time and delivery readiness.
- **Delivery Assignment:** Assign drivers or pickup personnel.
- **Delivery Tracking:** Track delivery status and route progress.
- **Delivery Analytics:** Report delivery order volume and fulfilment times.

---

## 4. User Stories

### 4.1 MVP Stories (30 stories)

1. As a **Cashier**, I want to create a POS bill quickly so that customers can pay and leave faster.
2. As a **Cashier**, I want to accept multiple payment methods so that customers can pay by cash, UPI, or card.
3. As a **Cashier**, I want to split a bill into separate payments so that multiple customers can pay independently.
4. As a **Cashier**, I want the POS to work when the network is down so that I can continue serving customers during outages.
5. As a **Cashier**, I want offline transactions queued locally so that orders sync automatically after reconnection.
6. As a **Kitchen Staff**, I want to receive digital KOTs immediately after billing so that I can start preparing food without delay.
7. As a **Kitchen Staff**, I want to update item status to cooking/ready/served so that the front desk knows order progress.
8. As a **Branch Manager**, I want a clear audit trail for payments and refunds so that I can investigate discrepancies.
9. As an **Owner**, I want branch-level sales reports so that I can compare performance across branches.
10. As an **Inventory Manager**, I want to record purchase receipts with expiry dates so that I can avoid using expired stock.
11. As an **Inventory Manager**, I want BOM relationships between menu items and ingredients so that stock decrements automatically.
12. As a **Branch Manager**, I want expired stock alerts so that I can remove unsafe inventory before it is used.
13. As a **Cashier**, I want order modifications before kitchen prep so that customer changes can be accommodated without waste.
14. As a **Kitchen Staff**, I want to reject or hold an item in the KOT so that unavailable items are handled cleanly.
15. As a **Branch Manager**, I want stale-order alerts so that orders waiting too long are escalated.
16. As an **Owner**, I want multi-tenant data isolation so that each franchise sees only its own data.
17. As a **Branch Manager**, I want franchise menu override support so that local pricing can adapt to market conditions.
18. As an **Owner**, I want row-level security so that users cannot access other franchise data.
19. As a **Branch Manager**, I want cash reconciliation at shift end so that cash drawer totals are verified.
20. As a **Branch Manager**, I want daily settlement reports so that I can compare cash vs system receipts.
21. As an **Owner**, I want audit logs for discounts and deletions so that every high-risk change is documented.
22. As a **Cashier**, I want staff-level login/logout tracking so that attendance is recorded by shift.
23. As an **Inventory Manager**, I want stock-out handling to hide unavailable menu items so that customers cannot order impossible items.
24. As an **Owner**, I want a kitchen display board so that the kitchen can manage high-volume ticket flow.
25. As a **Branch Manager**, I want performance metrics during rush hour so that I can understand bottlenecks.
26. As a **Cashier**, I want payment failure handling so that failed transactions do not incorrectly mark orders as complete.
27. As a **Branch Manager**, I want partial fulfillment tracking so that items can be delivered separately when ready.
28. As an **Inventory Manager**, I want waste categories for spoilage, theft, and trim so that my reports reflect true loss.
29. As an **Owner**, I want secure role permissions so that only authorized users can perform sensitive actions.
30. As a **Branch Manager**, I want offline sync recovery status so that I can confirm branch data is up to date.

### 4.2 Phase 1 Stories (20 stories)

31. As an **Owner**, I want profitability dashboards so that I can compare branch margins and food costs.
32. As an **Inventory Manager**, I want food cost percentage reports so that I can monitor ingredient spend.
33. As a **Branch Manager**, I want labor efficiency metrics so that I can manage staff costs.
34. As an **Cashier**, I want customer profiles captured at checkout so that I can recognize returning customers.
35. As a **Branch Manager**, I want loyalty point accrual so that repeat customers receive rewards.
36. As a **Cashier**, I want loyalty redemption at billing so that loyal customers can redeem points.
37. As an **Owner**, I want menu version history so that I can audit pricing and menu changes.
38. As an **Inventory Manager**, I want supplier lead time tracking so that I can reorder before stockouts.
39. As a **Branch Manager**, I want regional menu variants so that I can add local items without impacting other branches.
40. As an **Owner**, I want royalty tracking so that franchise revenue sharing can be calculated automatically.
41. As a **Branch Manager**, I want onboarding reports for new branches so that growth is monitored.
42. As a **Cashier**, I want manager approval requests for large refunds so that high-risk actions are controlled.
43. As an **Owner**, I want compliance status reporting so that I can prepare for audits.
44. As a **Branch Manager**, I want data export controls so that sensitive data is only shared with approval.
45. As a **Branch Manager**, I want menu item availability rules triggered by inventory levels so that stockouts are handled automatically.
46. As a **Kitchen Staff**, I want item-level remake tracking so that remade orders are associated correctly.
47. As an **Owner**, I want access logs for user sessions so that suspicious activity can be reviewed.
48. As a **Branch Manager**, I want customer acquisition and repeat rate insights so that marketing focus can be prioritized.
49. As an **Inventory Manager**, I want batch reconciliation reports so that physical vs system stock discrepancies are highlighted.
50. As a **Branch Manager**, I want a cash variance alert when drawer totals diverge from system totals so that issues are investigated.

### 4.3 Phase 2 Stories (10 stories)

51. As a **Customer**, I want to scan a QR code to view the menu so that I can order from my table.
52. As a **Customer**, I want to submit a mobile order so that I can pay without visiting the cashier.
53. As an **Owner**, I want delivery orders integrated into the POS so that all revenue is consolidated.
54. As a **Branch Manager**, I want delivery address capture so that orders can be fulfilled correctly.
55. As a **Customer**, I want to see order status updates from my mobile device so that I know when my food is ready.
56. As a **Branch Manager**, I want delivery analytics so that I can evaluate delivery efficiency.
57. As an **Owner**, I want driver assignment support so that delivery orders can be managed operationally.
58. As a **Branch Manager**, I want reservation management so that table bookings are handled in the system.
59. As a **Branch Manager**, I want a waitlist display so that guests waiting for tables can be managed.
60. As a **Branch Manager**, I want live occupancy status so that table availability is visible in real time.

---

## 5. MVP Roadmap with Epic-Level Breakdown

### 5.1 MVP Objectives

Deliver a production-ready restaurant management system that:

- Enables branch operations with resilient POS billing and kitchen coordination
- Supports franchise isolation and local branch configuration
- Provides inventory and payment controls to protect revenue and food safety
- Delivers core reporting and auditing tools for owners and managers
- Meets stability requirements for peak hour performance

### 5.2 MVP Epics

#### Epic 1: Core POS Billing & Kitchen Workflow

- POS billing UI and payment capture
- Split bill and partial payment handling
- Kitchen Order Ticket generation and item status updates
- Order modification and cancellation workflow
- Payment failure and refund handling

#### Epic 2: Offline Resilience & Sync

- Local menu caching and offline mode indicator
- Offline transaction queue
- Reconnect sync and conflict resolution
- Offline order status reconciliation
- Offline audit preservation

#### Epic 3: Franchise & Branch Security

- Multi-tenant data partitioning
- Role-based access control and permission matrix
- Branch-level menu overrides and pricing rules
- Row-level security enforcement
- Audit logs for sensitive actions

#### Epic 4: Inventory Perishability & Waste Control

- Ingredient batch tracking and expiry alerts
- BOM-based stock deduction
- Stock in/out purchase workflow
- Waste category logging and reconciliation
- Stock-out and substitution procedures

#### Epic 5: Payment Settlement & Reconciliation

- Payment gateway integration for UPI/card/cash
- Cash drawer and float management
- EOD settlement and variance report
- Refund approval and chargeback handling
- Payment audit trail and transaction logging

#### Epic 6: Rush Hour Performance & Reporting

- Kitchen Display System and order queuing
- Throughput and latency SLAs
- Menu/pricing caching
- Stress testing and load validation
- Branch performance dashboard

### 5.3 MVP Timeline

| Phase    | Duration | Focus                                                    |
| -------- | -------- | -------------------------------------------------------- |
| Sprint 0 | 1 week   | Architecture, data model, tenant/security design         |
| Sprint 1 | 2 weeks  | Core POS billing, payment integration, role model        |
| Sprint 2 | 2 weeks  | Kitchen workflow, order lifecycle, audit trail           |
| Sprint 3 | 2 weeks  | Offline resilience, local sync, menu caching             |
| Sprint 4 | 2 weeks  | Inventory batch tracking, BOM, waste capture             |
| Sprint 5 | 2 weeks  | Franchise menu overrides, branch reports, reconciliation |
| Sprint 6 | 2 weeks  | Performance validation, QA, stabilization, UAT           |

Total MVP duration: 10-11 weeks.

### 5.4 Phase 1 Epics

- Profitability & analytics dashboard
- Loyalty and customer retention
- Menu versioning and dynamic pricing
- Supplier lead time and procurement planning
- Data migration and branch onboarding tools
- Compliance reporting and export controls

### 5.5 Phase 2 Epics

- Table reservations and waitlist management
- QR ordering and mobile ordering integration
- Delivery order workflow and driver tracking
- Multi-currency and regional tax support
- Advanced staff productivity and scheduling

---

## 6. Risk Flags for Architect & Developer

### 6.1 Architecture Risk Flags

- **Multi-tenancy lock-in:** If tenant isolation is delayed, the system will need a costly retrofit.
- **Offline sync complexity:** Designing conflict resolution after initial development is high risk.
- **Payment integrity:** Payment gateway and settlement logic are critical; errors will directly impact cash flow.
- **Data model rigidity:** Inventory, order, and payment models must support audit history and branch-specific overrides from the start.
- **Scalability assumptions:** Underestimating peak load will threaten customer experience and branch productivity.
- **Security enforcement:** RBAC and row-level security must be enforced at the data layer, not only UI.

### 6.2 Developer Risk Flags

- **Order lifecycle edge cases:** Missing item-level status transitions will lead to incorrect order state and refunds.
- **Offline transition gaps:** Partial sync or duplicate transaction handling can corrupt inventory and payments.
- **Payment reconciliation:** Failure to track every payment event will create unreconciled cash and disputes.
- **Inventory auto-deduction:** Incorrect BOM logic can cause stock mismatches and hidden food cost errors.
- **Audit trail gaps:** If soft deletes and logs are not preserved, investigations cannot be completed.
- **Performance shortcuts:** Implementing bottleneck-prone APIs without load validation will cause build failures under rush hour.

### 6.3 Mitigation Principles

- Build the data model first and validate it with sample branch data.
- Prototype offline sync and conflict resolution before full implementation.
- Use API contracts and schema validation for payment and order events.
- Create automated tests for every item-level order state and payment scenario.
- Instrument load testing early and repeat after major changes.
- Enforce audit logging in shared middleware and database triggers where possible.

---

## 7. Appendix

### 7.1 Requirement Coverage

This PRD is derived from the existing gap analysis and requirement matrix, capturing 209 discrete requirements across 14 critical operational areas.

### 7.2 Document References

- `docs/real-world-scenarios-and-gaps.md`
- `docs/critical-requirements-matrix.md`
- `docs/discovery.md`
- `docs/implementation-readiness-checklist.md`

---

**Prepared by:** Product Management

**Next Step:** Review and approve MVP scope, then translate epics into backlog stories and tasks.
