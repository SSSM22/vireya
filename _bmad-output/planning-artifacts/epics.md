---
stepsCompleted:
  - validate-prerequisites
  - design-epics
  - create-stories
inputDocuments:
  - docs/product-requirements-document.md
  - docs/architecture.md
  - docs/ux-design.md
---

# vireya - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for vireya, decomposing the requirements from the PRD, UX Design, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

FR1: Support QR-based table ordering and bill presentation for in-branch customers.

FR2: Allow cashiers to create and finalize POS bills quickly with itemized totals.

FR3: Support multiple payment methods including cash, UPI, and card, with payment failure handling.

FR4: Support split bills and partial payments for shared checks.

FR5: Continue billing and order capture in offline mode with local transaction queueing.

FR6: Synchronize offline orders, KOT updates, and payment metadata after connectivity returns.

FR7: Send digital kitchen orders to kitchen staff with real-time status updates.

FR8: Support item-level kitchen statuses including pending, cooking, ready, served, and rejected.

FR9: Allow kitchen staff to reject or hold items and notify the cashier or customer.

FR10: Allow order modifications before food prep begins, with cost updates.

FR11: Record purchase receipts, batch expiry dates, and stock movements.

FR12: Support BOM-based recipe mapping and automatic ingredient deduction on orders.

FR13: Track waste by category and reconcile stock variances against physical counts.

FR14: Show stock-out and low-stock states and hide or substitute unavailable items.

FR15: Enforce branch-level and franchise-level tenant isolation for data and configuration.

FR16: Permit branch-specific menu pricing and availability overrides within franchise scope.

FR17: Support role-based permissions and audit logs for sensitive actions such as refunds, discounts, and deletions.

FR18: Generate daily settlement and reconciliation reports for cash and payment totals.

FR19: Provide branch and corporate reporting for sales, inventory, profitability, and operations.

FR20: Capture and display customer profiles, visit history, and loyalty points at checkout.

FR21: Support loyalty point accrual and redemption during billing.

FR22: Manage shifts, attendance, and cash variance alerts for branch staff.

FR23: Support menu versioning, promotional items, categories, and seasonal availability.

FR24: Enable data migration import, validation, and reconciliation from legacy Excel or notebook sources.

FR25: Support QR ordering integration with the existing KOT and POS pipeline.

### NonFunctional Requirements

NFR1: Maintain offline operation and sync recovery within 5 minutes after reconnection.

NFR2: Support 100+ concurrent orders per hour and billing response times under 2 seconds, with p95 under 3 seconds.

NFR3: Enforce tenant isolation, RBAC, audit logging, and soft-delete retention for auditability and compliance.

NFR4: Protect payment and customer data with TLS, encryption at rest, and secure local branch storage.

NFR5: Guarantee durable handling of local transactions and preserve audit trails during offline sync.

NFR6: Ensure accessibility and usability for shared terminals in low-light restaurant conditions.

NFR7: Provide observability for sync health, inventory variance, and operational exceptions.

NFR8: Support branch-local caching and deterministic conflict resolution for offline and reconnect flows.

NFR9: Keep role-specific interfaces simple and data access limited to authorized users.

NFR10: Maintain compliance-ready reporting for financial and operational data.

### Additional Requirements

- Use a modular monolith with clear domain boundaries for POS, Orders, Inventory, Kitchen, Payments, and Reporting.
- Use PostgreSQL with schema-based multi-tenancy and row-level security for franchise and branch isolation.
- Use a local SQLite branch store plus an event queue and sync state machine for offline branch operation.
- Use Redis for menu, session, and permission caching, plus rate limiting for API stability.
- Integrate with existing branch payment methods via adapter-based payment services rather than building new payment gateways.
- Preserve immutable audit records for payments, inventory events, order events, and sensitive configuration changes.
- Define a versioned branch sync API contract with deterministic conflict handling and rollback support.
- Provide migration runbooks, reconciliation steps, and cutover controls for legacy data transition.
- No starter template was explicitly specified in the architecture; the implementation should start from a greenfield modular monolith foundation.

### UX Design Requirements

UX-DR1: Provide a fast, one-glance billing experience with menu search, quick-add controls, and a persistent bill panel on the POS screen.

UX-DR2: Expose offline and sync status clearly in the POS and dashboard UI, including recovery progress and connection warnings.

UX-DR3: Provide a prioritized kitchen queue with color-coded statuses, stale-order highlighting, and fast item updates.

UX-DR4: Make high-risk actions such as refunds, voids, discounts, and inventory adjustments require confirmation and show audit context.

UX-DR5: Provide role-based entry points so cashiers land in Billing, kitchen staff in the KOT queue, inventory managers in stock views, and managers or owners in dashboard and approvals.

UX-DR6: Surface item-level state transitions and exceptions clearly to reduce order confusion and speed resolution.

UX-DR7: Implement accessible, touch-friendly controls with strong contrast, large targets, and clear error or loading states.

UX-DR8: Make inventory health, expiring batches, and stock warnings visually prominent in the inventory screen.

UX-DR9: Provide a lightweight dashboard with sales, pending orders, offline status, stock warnings, and approvals.

UX-DR10: Support split payments, payment failure recovery, and bill review flows without losing order state.

UX-DR11: Offer branch switching, notifications, and user profile context in the top bar for multi-branch operations.

UX-DR12: Provide clear empty states and loading patterns on reports, inventory, and admin screens.

### FR Coverage Map

> Note: FR1–FR22 correspond to the PRD-extracted functional requirements. FR23–FR25 are additional artifact-level requirements that are useful for epic/story planning but are not explicit PRD IDs.

FR1: Epic 1 - QR table ordering and bill presentation experience
FR2: Epic 1 - Existing payment method integration and cashier billing flows
FR3: Epic 1 - Offline resilience and sync for order capture and kitchen coordination
FR4: Epic 4 - Franchise-ready multi-tenancy with branch pricing and menu overrides
FR5: Epic 3 - Inventory perishability, expiry tracking, and BOM-based stock deduction
FR6: Epic 2 - Order flow edge cases, kitchen coordination, and item-status lifecycle
FR7: Epic 4 - Security, audit trails, and compliance controls
FR8: Epic 1 - Rush-hour performance for checkout and order processing
FR9: Epic 5 - Centralized branch and corporate reporting
FR10: Epic 1 - Offline mode with local queueing and secure sync after reconnection
FR11: Epic 1 - POS menu caching, pricing, and branch startup availability
FR12: Epic 1 - Durable offline transaction handling and audit trail preservation
FR13: Epic 4 - Cash reconciliation, refunds, and manager approval workflows
FR14: Epic 3 - BOM recipe linkage and automatic ingredient deduction
FR15: Epic 2 - Kitchen item status tracking: pending, cooking, ready, served, rejected
FR16: Epic 4 - Role-based access control at UI and API layers
FR17: Epic 4 - Permission-sensitive audit logging and compliance governance
FR18: Epic 5 - Customer profile, visit history, and loyalty support
FR19: Epic 5 - Table management and reservations (Phase 2 scope)
FR20: Epic 5 - Data migration planning, validation, cleansing, and cutover support
FR21: Epic 4 - Franchise menu override support and regional pricing variants
FR22: Epic 5 - Audit-ready tax and regulatory reporting
FR23: Epic 5 - Menu versioning, promotions, categories, and seasonal availability
FR24: Epic 5 - Legacy data import, validation, reconciliation, and migration controls
FR25: Epic 2 - QR ordering integration into the existing KOT and POS flow

## Epic List

### Epic 1: Fast, Resilient Checkout

This epic enables cashiers and managers to take orders, present bills, accept payments, and keep selling even when branch connectivity is unstable. It delivers the core front-counter experience and the resilience needed for rush-hour operations.
**FRs covered:** FR1, FR2, FR3, FR4, FR5, FR6

### Epic 2: Kitchen Coordination and Order Lifecycle

This epic gives the kitchen and front-of-house a reliable order flow from QR ordering through dish preparation, status changes, held or rejected items, and modifications before cooking begins.
**FRs covered:** FR7, FR8, FR9, FR10, FR25

### Epic 3: Inventory, Waste, and Stock Control

This epic gives inventory managers the tooling to record stock, track expiry and rotation, link recipes to ingredients, and manage waste and stock-outs safely.
**FRs covered:** FR11, FR12, FR13, FR14

### Epic 4: Franchise-Safe Operations and Governance

This epic establishes the tenant-aware foundation for multi-branch and multi-franchise operations, including role-based access, auditability, pricing overrides, and settlement controls.
**FRs covered:** FR15, FR16, FR17, FR18

### Epic 5: Reporting, Customer Engagement, and Migration Readiness

This epic expands the platform into a more complete branch operating system, covering reporting, loyalty, shift oversight, menu management, and legacy data migration readiness.
**FRs covered:** FR19, FR20, FR21, FR22, FR23, FR24

<!-- Repeat for each epic in epics_list (N = 1, 2, 3...) -->

## Epic 1: Fast, Resilient Checkout

This epic enables cashiers and managers to create and finalize bills quickly, accept payments flexibly, and keep selling during connectivity interruptions.

### Story 1.1: Create and Review a POS Bill Quickly

As a cashier,
I want to create and review a bill quickly from the POS screen,
So that customers can pay and leave faster during peak hours.

**Acceptance Criteria:**

**Given** a cashier is signed in to a branch POS terminal
**When** they search for and add menu items to a new bill
**Then** the bill panel updates immediately with item quantity, price, tax, and running total
**And** the cashier can review the bill without leaving the main billing screen.

**Given** a bill contains multiple items
**When** the cashier edits quantities or removes items
**Then** the totals and item list recalculate instantly and reflect the latest state.

**Given** the POS screen is used in a busy restaurant environment
**When** the cashier uses the interface
**Then** menu search, quick-add actions, and the active bill remain clearly visible and accessible.

### Story 1.2: Accept Multiple Payments and Split Shared Bills

As a cashier,
I want to accept cash, UPI, or card payments and split shared bills,
So that customers can pay flexibly without delays or confusion.

**Acceptance Criteria:**

**Given** a completed bill is ready for payment
**When** the cashier selects a supported payment method
**Then** the system records the payment method and updates the bill state accordingly.

**Given** a bill is shared by multiple guests
**When** the cashier splits the total into multiple payment allocations
**Then** the system stores each allocation and updates the remaining balance correctly.

**Given** a payment attempt fails after the user chooses a method
**When** the failure is returned by the payment service
**Then** the bill remains in a recoverable state and the cashier can retry or switch methods without losing the order.

### Story 1.3: Continue Billing Offline and Recover Sync State

As a cashier,
I want the POS to keep accepting orders and payments while offline,
So that branch operations continue during connectivity interruptions.

**Acceptance Criteria:**

**Given** the branch terminal loses network connectivity
**When** the cashier creates or updates a bill
**Then** the POS continues operating and stores the transaction locally for later synchronization.

**Given** a transaction is queued locally while offline
**When** connectivity is restored
**Then** the system batches and syncs the transaction and shows recovery progress to staff.

**Given** the branch terminal is operating offline
**When** the cashier views the interface
**Then** a clear offline banner and sync status indicator are visible at all times.

## Epic 2: Kitchen Coordination and Order Lifecycle

This epic provides a dependable kitchen flow from QR ordering through ticket creation, status changes, holds, rejections, and order modifications before cooking begins.

### Story 2.1: Deliver Digital Kitchen Tickets for New Orders

As a kitchen staff member,
I want new orders to appear as digital KOT tickets immediately,
So that food preparation can begin without delay.

**Acceptance Criteria:**

**Given** a bill is finalized and sent to the kitchen
**When** the order is created
**Then** a KOT ticket is generated with all items, quantities, modifiers, and special requests.

**Given** multiple tickets are active in the kitchen queue
**When** the kitchen staff views the board
**Then** tickets are prioritized and displayed in a way that makes urgency obvious.

**Given** a QR-based table order is submitted
**When** the order reaches the kitchen
**Then** it is routed through the existing KOT and POS pipeline without manual re-entry.

### Story 2.2: Update Item Status and Handle Partial Fulfillment

As a kitchen staff member,
I want to update item status and manage partial fulfillment,
So that the front-of-house and kitchen stay aligned on order progress.

**Acceptance Criteria:**

**Given** a ticket is active in the kitchen queue
**When** the staff changes an item status to cooking, ready, served, or rejected
**Then** the updated status is visible to the relevant branch users.

**Given** some items on a ticket are ready while others remain pending
**When** the kitchen staff marks the ready items as served
**Then** the system allows those items to be completed separately from pending items.

**Given** a ticket remains in the queue beyond a configurable waiting threshold
**When** the kitchen staff views the board
**Then** stale-order indicators highlight the ticket for follow-up.

### Story 2.3: Manage Holds, Rejections, and Order Changes Before Cooking

As a kitchen staff member,
I want to hold or reject items and support order changes before cooking begins,
So that the kitchen can handle exceptions cleanly and the customer experience remains accurate.

**Acceptance Criteria:**

**Given** an item cannot be prepared as requested
**When** the kitchen staff marks it as held or rejected
**Then** the system records the reason and notifies the relevant branch user.

**Given** a customer requests a change before cooking starts
**When** the staff or cashier updates the order
**Then** the system recalculates totals and updates the kitchen ticket accordingly.

**Given** an item is modified or rejected
**When** the change is saved
**Then** the audit trail captures the change and the latest order state remains consistent.

## Epic 3: Inventory, Waste, and Stock Control

This epic gives inventory managers the tools to receive stock, track expiry and rotation, link recipes to ingredients, and control waste and stock-outs safely.

### Story 3.1: Record Purchase Receipts and Expiry Data

As an inventory manager,
I want to record purchase receipts with expiry and batch information,
So that stock can be rotated safely and expired items are avoided.

**Acceptance Criteria:**

**Given** stock is received in the branch
**When** the inventory manager enters a purchase receipt
**Then** the system stores the item, quantity, batch, cost, and expiry date.

**Given** an inventory batch is nearing expiry
**When** the inventory view is opened
**Then** the batch is flagged with an expiry warning and prioritized for review.

**Given** multiple batches of the same item exist
**When** the inventory manager reviews stock
**Then** the system highlights older batches so FIFO rotation can be followed.

### Story 3.2: Link Recipes to Inventory and Deduct Stock Automatically

As an inventory manager,
I want bills of materials to drive stock deduction and availability rules,
So that ingredient consumption is accurate and menu availability reflects actual stock.

**Acceptance Criteria:**

**Given** a menu item has an associated recipe or BOM
**When** the order is placed
**Then** the system deducts the defined ingredient quantities from available stock.

**Given** a menu item depends on ingredients that are unavailable
**When** the order is attempted
**Then** the system prevents the order or suggests a substitution according to the configured rule.

**Given** ingredient stock changes after an order is placed
**When** the stock view is refreshed
**Then** the system shows the updated available quantity and stock status.

### Story 3.3: Track Waste, Variance, and Reconciliation

As an inventory manager,
I want to record waste categories and reconcile variances,
So that spoilage, theft, and discrepancies are visible and auditable.

**Acceptance Criteria:**

**Given** waste or stock discrepancy occurs
**When** the inventory manager logs an entry
**Then** the system stores the category, quantity, reason, and cost impact.

**Given** physical stock counts differ from system records
**When** reconciliation is run
**Then** the system identifies a variance and flags it for review when it exceeds the configured threshold.

**Given** the inventory view is used for decision-making
**When** waste and variance data are present
**Then** the system exposes them in an understandable summary for operations review.

## Epic 4: Franchise-Safe Operations and Governance

This epic establishes the tenant-aware foundation for multi-branch and multi-franchise operations, including secure access, pricing control, and settlement governance.

### Story 4.1: Enforce Tenant-Aware Access and Audit Logging

As an owner or branch manager,
I want role-based access and audit logs to be enforced across branches and franchises,
So that sensitive actions are secure and traceable.

**Acceptance Criteria:**

**Given** a user accesses the system
**When** they attempt to view or modify data outside their tenant or branch scope
**Then** the system blocks the action and records the attempt.

**Given** a sensitive action such as a refund, discount, or deletion occurs
**When** the change is saved
**Then** the system records before-and-after state and the acting user in the audit trail.

**Given** a user has limited permissions
**When** they open the application
**Then** they only see the screens and actions permitted by their role.

### Story 4.2: Support Branch and Franchise Pricing Overrides

As a branch manager or franchise admin,
I want to apply menu pricing overrides and regional variants,
So that local operations can adapt without impacting unrelated branches.

**Acceptance Criteria:**

**Given** a branch or franchise requires a local price or availability rule
**When** the override is configured
**Then** the system applies the override only to the authorized scope.

**Given** a regional or seasonal menu variant is created
**When** the variant is published
**Then** it is available only to the intended branch or franchise group.

**Given** a pricing or availability change is made
**When** the change is saved
**Then** the system records the change history for review and rollback.

### Story 4.3: Reconcile Cash and Settlement Activity

As a branch manager,
I want daily settlement and cash reconciliation to be visible and auditable,
So that branch cash handling and payment activity can be verified quickly.

**Acceptance Criteria:**

**Given** cash and payment activity is recorded for a day
**When** the reconciliation report is generated
**Then** it compares expected totals with recorded totals and highlights variances.

**Given** a high-risk financial action is triggered
**When** the user proceeds
**Then** a confirmation step and audit context are shown before the action is completed.

**Given** a manager reviews settlement history
**When** they inspect an entry
**Then** the system shows the relevant payment, refund, and adjustment details for investigation.

## Epic 5: Reporting, Customer Engagement, and Migration Readiness

This epic expands the platform into a complete branch operating system by covering reporting, loyalty, menu governance, staff oversight, and legacy migration readiness.

### Story 5.1: Provide Branch Reporting and Operational Dashboards

As an owner or branch manager,
I want dashboards and reports for sales, inventory, and operations,
So that I can monitor branch performance and respond to issues quickly.

**Acceptance Criteria:**

**Given** the reporting module is opened
**When** a user selects a branch and date range
**Then** the system displays relevant sales, order, inventory, and exception summaries.

**Given** a branch or corporate user needs operational visibility
**When** they review the dashboard
**Then** they can see pending orders, offline status, stock warnings, and approvals without navigating to multiple screens.

**Given** report data is empty or incomplete
**When** the report is loaded
**Then** the system shows a clear empty state and guidance for next steps.

### Story 5.2: Capture Customer Profiles and Loyalty Activity

As a cashier or owner,
I want customer profiles and loyalty points to be captured during checkout,
So that repeat customers can be recognized and rewarded.

**Acceptance Criteria:**

**Given** a customer checks out
**When** their profile is available or created
**Then** the system stores their contact details, visit history, and preferences.

**Given** a customer makes qualifying purchases
**When** the order is completed
**Then** loyalty points are accrued and displayed in the customer profile or checkout flow.

**Given** a customer redeems loyalty points during billing
**When** the transaction is finalized
**Then** the points are deducted and the final bill reflects the adjusted total.

### Story 5.3: Manage Menu Versions, Promotions, and Categories

As an owner or branch manager,
I want to manage menu versions, promotions, seasonal items, and categories,
So that the menu can be updated safely across branches and channels.

**Acceptance Criteria:**

**Given** a menu update is prepared
**When** it is saved
**Then** the system creates or updates a versioned menu record with change history.

**Given** a promotional or seasonal item is configured
**When** it is published
**Then** it appears only in the intended scope and time window.

**Given** a menu category or item is updated
**When** the change is saved
**Then** the system keeps the item visible and navigable in the correct category.

### Story 5.4: Track Staff Shifts and Attendance

As a branch manager,
I want shift tracking and attendance logging to be supported,
So that staff productivity and cash variance can be monitored accurately.

**Acceptance Criteria:**

**Given** a staff shift starts or ends
**When** the branch manager or system records the event
**Then** the system logs attendance, shift start/end times, and shift state for reporting.

**Given** a staff shift is in progress
**When** the branch manager reviews the shift data
**Then** the system displays active shift status, attendance details, and any cash variance alerts.

**Given** a shift ends with cash variance
**When** the manager reviews the reconciliation
**Then** the system flags the variance and links it to the shift report for investigation.

### Story 5.5: Import Legacy Branch Data with Auditability

As an implementation lead,
I want legacy branch data import to be supported with validation and audit trail,
So that migration can be completed safely and corrected when issues arise.

**Acceptance Criteria:**

**Given** legacy branch data is prepared for import
**When** the import is run
**Then** the system validates records, flags issues, and preserves a migration audit trail.

**Given** a data migration issue is detected
**When** the import is reviewed
**Then** the system reports the issue and allows the team to correct or re-run the affected records.

**Given** the migration process completes
**When** the data is accepted
**Then** the system records the import outcome, issue summary, and audit metadata for verification.
