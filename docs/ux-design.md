# UX Design Specification

## Vireya / AFC Restaurant Management System

**Version:** 1.0  
**Date:** 30 June 2026  
**Status:** Draft UX design for MVP review

---

## 1. UX Design Intent

The UX for Vireya should feel fast, calm, and dependable in a busy restaurant environment. The system must support high-pressure scenarios such as rush hours, offline operation, and branch-level coordination without overwhelming the user.

### Core UX goals

- Reduce bill generation time during peak hours.
- Make critical operations obvious in one glance.
- Support role-specific workflows without unnecessary clutter.
- Preserve trust through transparent status, confirmations, and audit visibility.
- Prepare the experience for future franchise growth and multi-branch operations.

---

## 2. Design Principles

1. Speed first
   - The cashier should be able to create and finalize a bill in seconds.
   - Repeated actions should use shortcuts, sticky actions, and predictable layouts.

2. Clarity over cleverness
   - The most important status and actions should always be visible.
   - Avoid hidden flows for core actions such as payment, cancellation, or kitchen updates.

3. Safe operations
   - High-risk actions such as refunds, voids, discounts, and inventory adjustments should require confirmation.
   - All sensitive changes should be traceable.

4. Role-based simplicity
   - Each role sees the minimum required controls for their workflow.
   - Managers get visibility; cashiers get speed; kitchen staff get queue focus.

5. Resilience and trust
   - Offline and sync states must be visible at all times.
   - The system should reassure users when the network is unstable.

6. Accessibility and usability
   - Large touch targets, strong contrast, readable typography, and clear error states are required.
   - The interface must work well in low-light restaurant conditions and on shared terminals.

---

## 3. Primary Personas

### 3.1 Cashier

Needs:

- Fast menu selection
- Quick item addition and bill review
- Clear payment steps
- Split bill and reprint support
- Low-friction error recovery

### 3.2 Branch Manager

Needs:

- Branch overview and live operations
- Approval for sensitive actions
- Daily sales, inventory, and exception visibility
- Staff and branch configuration access

### 3.3 Kitchen Staff

Needs:

- Immediate visibility of new KOTs
- Fast status updates
- Clear item-level progress
- Alerting for stale or delayed orders

### 3.4 Inventory Manager

Needs:

- Purchase and stock visibility
- Expiry and rotation awareness
- Waste and discrepancy handling
- Low-stock and out-of-stock alerts

### 3.5 Owner / Franchise Admin

Needs:

- Cross-branch reporting and governance
- Role and permission management
- Branch comparison and franchise-level analytics

---

## 4. Information Architecture

### Main sections

- Authentication
- Dashboard
- POS Billing
- Orders and Kitchen
- Inventory Management
- Reports and Analytics
- Administration and Settings

### Navigation structure

- Home / Dashboard
- Billing
- Kitchen
- Inventory
- Reports
- Settings

### Role-based entry points

- Cashier → Billing screen
- Kitchen Staff → Kitchen queue
- Inventory Manager → Inventory dashboard
- Manager → Dashboard + approvals
- Owner → Dashboard + reporting + governance

---

## 5. Core User Journeys

### 5.1 Cashier billing journey

1. Sign in to the POS terminal.
2. Confirm branch and shift context.
3. Select table or order type.
4. Add items from the menu.
5. Review the bill and apply discounts or split options if needed.
6. Choose payment method.
7. Complete the transaction and print or display the bill.
8. Return to a ready state for the next order.

### 5.2 Kitchen order journey

1. New order appears on the KOT board.
2. Kitchen staff sees priority and timing.
3. Staff updates item status from pending to cooking to ready.
4. If an item is rejected, a reason and notification are captured.
5. Completed items are cleared from the active queue.

### 5.3 Inventory management journey

1. Inventory manager opens the stock view.
2. Reviews low-stock and expiring batches.
3. Adds purchase entry or stock adjustments.
4. Records waste, spoilage, or discrepancies.
5. Confirms stock deductions linked to sales and BOM usage.

### 5.4 Manager oversight journey

1. Manager opens the dashboard.
2. Sees live sales, pending orders, offline alerts, and stock warnings.
3. Reviews exceptions or approvals.
4. Opens reports or branch-level detail for investigation.

---

## 6. Screen Map

### 6.1 Authentication

- Login screen
- Password reset / forgot password
- Session timeout warning

### 6.2 Dashboard

- Today at a glance
- Sales card
- Orders in progress
- Offline status
- Stock warnings
- Approval queue

### 6.3 POS Billing

- Order creation screen
- Menu browsing
- Active bill panel
- Payment selection
- Bill confirmation and receipt

### 6.3 Kitchen

- KOT queue
- Ticket detail
- Status update controls
- Exception handling view

### 6.4 Inventory

- Stock overview
- Batch and expiry view
- Purchase entry
- Waste and adjustment entry

### 6.5 Reports

- Sales report
- Inventory report
- Branch comparison
- GST and cash reconciliation

### 6.6 Administration

- User management
- Role and permissions
- Branch configuration
- Feature rollout and regional settings

---

## 7. Detailed Screen Specifications

### 7.1 Login Screen

Purpose: secure access with fast context selection.

Layout:

- Centered card with app branding
- Branch selection if applicable
- Email/username and password fields
- Remember me and forgot password link
- Clear error states and loading state

UX notes:

- The login should be compact and fast.
- If the user is already authenticated, redirect to the relevant role-based landing page.

### 7.2 Dashboard

Purpose: provide immediate operational awareness.

Layout:

- Top bar with branch switcher, search, notifications, and user profile
- Left navigation for primary modules
- Main content area with summary cards and recent activity

Key widgets:

- Today’s sales
- Orders pending
- Offline/sync state
- Expiring batches
- Pending approvals
- Top selling items

UX notes:

- The dashboard should stay lightweight and scannable.
- Critical alerts should appear before secondary metrics.

### 7.3 POS Billing Screen

Purpose: support fast order entry with minimal friction.

Layout:

- Left: category tabs and menu items
- Center: item cards and quick add actions
- Right: current bill with item list, totals, discounts, and payment actions
- Bottom: action bar for hold, cancel, split, and complete

Key controls:

- Search bar for menu items
- Category filters
- Quantity controls
- Modifier chips for extras or substitutions
- Discount entry
- Payment method buttons

UX notes:

- The active bill must remain visible at all times.
- The most used actions should be one tap away.
- The screen should support both touch and keyboard input.

### 7.4 Bill Review and Payment

Purpose: reduce confusion before payment completion.

Layout:

- Itemized summary
- Tax and total breakdown
- Payment method options
- Split payment controls
- Confirmation footer

UX notes:

- Show clear totals before accepting payment.
- If a payment fails, preserve the ordered state and guide the user to retry or switch methods.

### 7.5 Kitchen Queue Screen

Purpose: provide a simple, prioritized ticket board.

Layout:

- Left: queue of active tickets
- Right: selected ticket details and status controls
- Color-coded priority and timing indicators

Statuses:

- Pending
- Cooking
- Ready
- Served
- Rejected

UX notes:

- Priority should be obvious at a glance.
- Stale orders should be visually highlighted.
- The interface should avoid too much text and focus on quick actions.

### 7.6 Inventory Screen

Purpose: make stock health and expiry visible at a glance.

Layout:

- Summary cards for stock value, expiring batches, low stock, and waste
- Table of inventory items with quantity, batch, expiry, and status
- Quick actions for stock in, stock out, and waste entry

UX notes:

- Expiry warnings should be visually prominent.
- Inventory actions should be grouped by task type.
- Use color sparingly and consistently for status.

### 7.7 Reports Screen

Purpose: present useful reporting without overwhelming the user.

Layout:

- Filter bar for branch, date range, and report type
- Summary cards
- Charts and tabular data
- Export actions

UX notes:

- Default to a useful daily or weekly view.
- Keep primary metrics above the fold.
- Show empty states and helpful loading patterns.

### 7.8 Admin and Settings Screen

Purpose: support safe configuration and role governance.

Layout:

- Side navigation for users, roles, branches, menu settings, and integrations
- Configuration forms with clear sectioning
- Review and save actions

UX notes:

- Changes should use confirmation dialogs and clear save state.
- Permissions should be understandable with simple role labels and access summaries.

---

## 8. Interaction Patterns

### 8.1 Confirmation and safety

Use confirmation dialogs for:

- Refunds
- Voids/cancellations
- Discounts above threshold
- Inventory adjustments
- Role or branch changes

### 8.2 Feedback and status

Use:

- Toast messages for success and warning feedback
- Inline validation for form issues
- Progress indicators for sync and offline recovery
- Non-blocking banners for branch connectivity status

### 8.3 Empty and error states

Each major list or dataset should include:

- Empty state with guidance
- Retry action for failed load
- Clear explanation when data is unavailable

### 8.4 Offline experience

When offline:

- Show a persistent banner at the top of the app
- Keep the POS usable with local queueing
- Display sync progress and “last synced” details
- Prevent destructive actions when the state cannot be safely synchronized

---

## 9. Visual Design Direction

### 9.1 Style direction

The product should feel modern, warm, and practical. It should reflect a food-service environment without becoming playful or overly decorative.

### 9.2 Suggested color palette

- Primary: deep red for brand emphasis and attention
- Accent: warm amber for status highlights and action cues
- Success: green for completed and healthy states
- Warning: amber for stock and timing alerts
- Neutral: slate and gray for surfaces and text

### 9.3 Typography

- Use a clean sans-serif font for legibility.
- Keep headings bold and compact.
- Use strong contrast for data-heavy screens.

### 9.4 Spacing and layout

- Use an 8px spacing system.
- Ensure touch targets are at least 44px high and wide.
- Use a responsive layout that works on desktop terminals and tablets.

---

## 10. Accessibility Requirements

- Minimum contrast ratios should meet common accessibility standards.
- Keyboard navigation must be supported for admin and reporting screens.
- All icons should have clear labels or tooltips.
- Error messages must be descriptive and persistent enough to recover from.
- The interface should support screen readers in core flows.

---

## 11. MVP UX Scope

### In scope for MVP

- Login and role-based home screen
- POS billing flow
- Kitchen order queue and status updates
- Inventory overview and batch/expiry actions
- Sales and inventory reporting
- Basic admin and permission management
- Offline mode banner and sync status

### Phase 1 and later

- Loyalty experience
- Advanced profitability dashboards
- Reservation and table management
- Mobile-first customer experience
- QR ordering and delivery flows

---

## 12. Recommended Design Deliverables

For implementation, the following should be produced next:

- Low-fidelity wireframes for each core screen
- Interactive prototype for cashier and kitchen flows
- Component library for buttons, cards, forms, tables, and status indicators
- Accessibility checklist for the MVP
- Usability test plan for branch staff

---

## 13. Final UX Recommendation

The MVP experience should center on a fast cashier workflow, a clear kitchen queue, a dependable inventory console, and a calm management overview. The interface should prioritize speed and operational confidence over visual complexity, especially in rush-hour and offline conditions.
