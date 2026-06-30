# Real-World Scenarios & Critical Gaps Analysis

## AFC Restaurant Management System

**Version:** 1.0  
**Date:** 30 June 2026  
**Purpose:** Comprehensive analysis of operational blind spots and real-world edge cases

---

## Overview

This document identifies 14 critical gaps between the current business requirements and production-ready requirements. Each gap includes real-world failure scenarios, system requirements, and acceptance criteria.

---

## 1. OFFLINE/CONNECTIVITY RESILIENCE

### Risk Level: 🔴 **HIGH**

### Problem Statement

Current assumption: "Internet connectivity is available at each branch"

**Reality:** Peak dinner hour coincides with peak network congestion. WiFi failures, ISP downtime, and cloud API latency occur during maximum revenue hours.

### Real-World Scenario

**Scenario:** Friday 7:30 PM - Peak Dinner Rush

- 40 customers in restaurant
- 8 orders being processed
- ISP goes down (15-minute outage)
- POS system locked because it can't reach cloud
- Cashiers can't bill customers
- Customers get angry, leave without paying
- Revenue loss: ₹8000-10000
- Staff frustrated, no fallback procedure

### Missing Requirements

| Requirement ID | Requirement          | Acceptance Criteria                                          |
| -------------- | -------------------- | ------------------------------------------------------------ |
| OFF-001        | Offline mode for POS | System continues billing when cloud unavailable              |
| OFF-002        | Transaction queue    | Transactions queued locally, sync when online                |
| OFF-003        | Conflict resolution  | Strategy defined for conflicting inventory updates           |
| OFF-004        | Order status sync    | Kitchen orders cached locally, sync when connection restored |
| OFF-005        | Data integrity       | No transaction loss during reconnection                      |
| OFF-006        | Staff notification   | UI shows "Offline Mode" with warning                         |
| OFF-007        | Recovery time        | Reconnection and sync completes within 5 minutes             |
| OFF-008        | Menu caching         | Latest menu cached at branch startup daily                   |

### System Design Impact

- **Database:** Local SQLite backup on POS machine
- **API:** Sync protocol for delta updates
- **UI:** Offline mode toggle with visual indicator
- **Testing:** Must simulate 30-minute cloud outage

---

## 2. PAYMENT & SETTLEMENT CHAOS

### Risk Level: 🔴 **CRITICAL**

### Problem Statement

Current requirement mentions "Multiple payment modes" but defines zero settlement, reconciliation, or dispute handling workflow.

### Real-World Scenario

**Scenario A: Split Bill Disaster**

- Table 3: ₹2500 total bill for 4 customers
- Customer A pays ₹800 cash → Cashier marks settled
- Customer B pays ₹900 UPI → System processes
- Customer C says: "I'll pay tomorrow"
- Customer D says: "I already paid last week" (false claim)
- Next day, Customer C doesn't come back
- Owner asks: "Who owes us ₹800?" → No audit trail

**Scenario B: Card Payment Failed**

- Customer orders ₹5000 meal
- Kitchen prepares and serves
- Card payment fails (insufficient funds)
- Customer leaves without paying
- Who owns the loss? Kitchen? Cashier? System?

**Scenario C: Cash Discrepancy**

- End of day: System shows ₹45000 in cash transactions
- Cashier counts: Only ₹44200 in drawer
- Missing: ₹800
- Theft? Error? System bug?
- No audit trail to investigate

### Missing Requirements

| Requirement ID | Requirement                 | Acceptance Criteria                                                   |
| -------------- | --------------------------- | --------------------------------------------------------------------- |
| PAY-001        | Payment gateway integration | Specify UPI, credit card, debit card, wallet support                  |
| PAY-002        | Cash reconciliation         | Daily shift-end reconciliation with discrepancy flagging              |
| PAY-003        | Float management            | Opening/closing cash tracking per cashier per shift                   |
| PAY-004        | Split bill logic            | Each customer on split bill tracked separately with settlement status |
| PAY-005        | Payment failure handling    | Order state when payment fails; refund/cancellation flow              |
| PAY-006        | Partial payments            | Support payment in installments with balance tracking                 |
| PAY-007        | Refund flow                 | Refund to same payment method; audit trail logged                     |
| PAY-008        | Chargeback handling         | Process and flag disputes; financial reconciliation                   |
| PAY-009        | Audit trail                 | Every transaction: timestamp, cashier ID, amount, mode, status        |
| PAY-010        | EOD settlement report       | Daily cash vs. system variance report                                 |
| PAY-011        | Multi-currency (future)     | Support for different currencies if expanding to multiple countries   |
| PAY-012        | Payment reversal            | Manager approval required for refunds >₹2000                          |

### System Design Impact

- **Database:** Payment ledger with immutable transaction records
- **API:** Payment gateway SDK integration (Razorpay/PayU recommended)
- **UI:** Payment mode selection, receipt generation, reconciliation dashboard
- **Compliance:** GST invoice generation per transaction
- **Reporting:** Daily settlement report by payment mode

---

## 3. INVENTORY: PERISHABILITY & RECIPE GAPS

### Risk Level: 🔴 **HIGH**

### Problem Statement

Current requirement: "Stock In, Stock Out, Daily Consumption" — but zero mention of expiry dates, recipes, food cost, or waste tracking.

### Real-World Scenario

**Scenario A: Expired Inventory Crisis**

- 5kg chicken purchased Monday
- Expiry: Wednesday (3-day shelf life)
- Monday-Tuesday: 3kg sold
- Wednesday 10am: 2kg chicken still in stock but expired
- Kitchen doesn't know expiry
- Chef uses expired chicken in 40 orders
- Food poisoning incident; regulatory fine; reputation damage

**Scenario B: Wastage Without Data**

- Daily inventory count: 10kg chicken used
- System shows: 10kg deducted from stock
- Reality: 3kg used in cooking, 4kg spoiled (refrigerator failure), 2kg normal trim, 1kg unaccounted (theft?)
- Owner doesn't know waste %; can't reduce costs
- Food cost % creeping up; profit margin shrinking

**Scenario C: Bill of Materials Missing**

- Fried Chicken Combo = ? kg chicken + ? ml oil + ? grams salt
- Inventory has no recipe
- When order created, system doesn't auto-deduct ingredients
- Manual stock updates = errors, inconsistency
- Can't calculate food cost per menu item

**Scenario D: Ingredient Substitution**

- Menu item: "Cheese Burger" (requires imported cheese)
- Imported cheese out of stock
- Chef substitutes with domestic cheese
- Customer charged same price
- Food cost suddenly different; profit margin changes
- System doesn't track substitution

### Missing Requirements

| Requirement ID | Requirement             | Acceptance Criteria                                               |
| -------------- | ----------------------- | ----------------------------------------------------------------- |
| INV-001        | Expiry date tracking    | Track batch expiry; alert before expiration                       |
| INV-002        | FIFO rotation           | System suggests oldest stock first; reports out-of-rotation items |
| INV-003        | Bill of Materials (BOM) | Each menu item linked to ingredient requirements                  |
| INV-004        | Auto-deduction          | When order placed, ingredients auto-deducted from inventory       |
| INV-005        | Waste tracking          | Separate tracking: spoilage, theft, normal trim, discrepancy      |
| INV-006        | Waste alerts            | Alert when waste % exceeds threshold (e.g., >5%)                  |
| INV-007        | Food cost %             | Calculated daily: total inventory cost ÷ total revenue            |
| INV-008        | Supplier lead time      | Track reorder time and auto-trigger orders                        |
| INV-009        | Stock-out procedure     | Define: hide from menu vs. backorder vs. substitute               |
| INV-010        | Ingredient substitution | Log substitution; adjust cost; track pattern                      |
| INV-011        | Stock rotation report   | Weekly: items not sold in 10+ days flagged as at-risk             |
| INV-012        | Batch reconciliation    | Physical count vs. system count; investigate >5% variance         |

### System Design Impact

- **Database:** Inventory ledger with batch tracking, expiry dates, BOM tables
- **API:** Daily waste calculation; cost rollup
- **UI:** Expiry dashboard, waste alert, stock rotation priority list
- **Reporting:** Food cost %, waste %, supplier lead time analysis
- **Integration:** Supplier auto-orders when stock <reorder point

---

## 4. ORDER FLOW EDGE CASES

### Risk Level: 🟡 **MEDIUM**

### Problem Statement

Current workflow: "Kitchen receives KOT immediately after billing" — but zero handling for order modifications, rejections, cancellations, or partial fulfillment.

### Real-World Scenario

**Scenario A: Kitchen Rejects Mid-Order**

- Table 5 orders "Fried Chicken Combo" at 7:05pm
- Bill generated: ₹450
- Customer pays
- Kitchen starts prep at 7:06pm
- 7:08pm: Chicken unexpectedly runs out
- Kitchen rejects order verbally; no system record
- Cashier doesn't know order rejected
- Customer waits 20 minutes expecting food
- Customer angry; asks for refund
- System shows order "completed" (paid)
- Refund process undefined

**Scenario B: Customer Modifies After Billing**

- Order placed: "Burger with extra cheese"
- Bill generated: ₹280
- Customer pays
- Customer changes mind: "Actually, no cheese, extra mayo"
- Kitchen receives KOT: "Burger with extra cheese"
- Burger prepared and served
- Customer refuses: "I said no cheese!"
- Dispute: Customer demands refund or remade burger
- System doesn't support modifications after billing

**Scenario C: Partial Fulfillment**

- Table 2 orders: Chicken (15min), Burger (5min), Fries (3min)
- All billed together: ₹850
- 7:10pm: Burger and Fries ready; Chicken still cooking
- Can cashier serve Burger + Fries now, Chicken later?
- System doesn't track partial delivery
- Customer eats cold fries waiting for chicken

**Scenario D: Stale Order**

- Order placed: 7:00pm
- Bill generated
- Kitchen displays KOT but doesn't start (busy with 30 other orders)
- 7:45pm: Order still not started
- Customer angry, cancels
- System shows: order paid, order cancelled (loss)
- No procedure to prevent stale orders

### Missing Requirements

| Requirement ID | Requirement            | Acceptance Criteria                                                    |
| -------------- | ---------------------- | ---------------------------------------------------------------------- |
| ORD-001        | Kitchen rejection flow | Kitchen can reject order; cashier notified; refund process triggered   |
| ORD-002        | Order modification     | Allow modification before kitchen starts; cost adjustment if needed    |
| ORD-003        | Modification tracking  | Log: original order, modified order, reason, who authorized            |
| ORD-004        | Partial fulfillment    | Track items ready vs. pending; split service option                    |
| ORD-005        | Item-level status      | Each item in order has: pending, cooking, ready, served, rejected      |
| ORD-006        | Cancel order workflow  | Manager approval for cancellations >₹500; refund process               |
| ORD-007        | Stale order alert      | Alert kitchen if order pending >20 minutes (configurable)              |
| ORD-008        | Special requests       | Text field on KOT for customer requests (allergies, "less salt", etc.) |
| ORD-009        | Hold orders            | Kitchen can hold order if ingredient temporarily unavailable           |
| ORD-010        | Remake orders          | Track remake requests; link to original order; no additional charge    |

### System Design Impact

- **Database:** Order status ledger; modification audit trail; cancellation reason tracking
- **API:** Order rejection endpoint; status change events
- **UI:** Real-time order status to kitchen; item-level progress indicator
- **Kitchen Display:** Visual alerts for stale/pending orders; rejection interface
- **Reporting:** Remake rate, rejection rate, avg time-to-serve by item

---

## 5. RUSH HOUR PERFORMANCE & SCALABILITY

### Risk Level: 🔴 **HIGH**

### Problem Statement

Current pain point: "Slow billing during peak hours" — but no SLA defined, no load testing, no queue management strategy.

### Real-World Scenario

**Scenario: Friday Night Dinner Rush**

- 6:30pm: 35 customers arrive
- 2 cashiers, 1 POS terminal
- Orders coming in: 3 orders/minute
- Billing: 2-3 minutes per order (navigating menu, selecting items, processing payment)
- Queue forms: 30+ customers waiting
- POS cloud API latency: 3 seconds/request
- Customer frustration builds
- Some customers leave without ordering (lost revenue: ₹15000+)
- Staff overtime costs increase
- Next hour: System stabilizes but opportunity lost

### Missing Requirements

| Requirement ID | Requirement                  | Acceptance Criteria                                            |
| -------------- | ---------------------------- | -------------------------------------------------------------- |
| PERF-001       | Throughput SLA               | System handles 100+ concurrent orders/hour without degradation |
| PERF-002       | Latency SLA                  | Billing transaction <2 seconds end-to-end, p95 <3 seconds      |
| PERF-003       | Kitchen Display System (KDS) | Visual display of 50+ tickets; color-coded priority            |
| PERF-004       | Queue visualization          | Display: "Est. wait time: 15 min" for new customers            |
| PERF-005       | Load testing                 | Stress test: 100 orders/hour sustained for 4 hours             |
| PERF-006       | Connection pooling           | Reuse DB connections; avoid pool exhaustion                    |
| PERF-007       | Caching strategy             | Cache menu, pricing, tables; minimal DB hits per transaction   |
| PERF-008       | API rate limiting            | Graceful degradation if payment gateway throttled              |
| PERF-009       | Table turnover tracking      | Alert: table >2 hours. Suggest customer move or order more.    |
| PERF-010       | Reserved seating (future)    | Block table for VIP; prevent overbooking                       |

### System Design Impact

- **Architecture:** Horizontal scaling for POS API; load balancer across multiple instances
- **Database:** Read replicas for reporting; write optimized for transactions
- **Cache:** Redis for menu, pricing, session data
- **Kitchen Display:** Large touchscreen or monitor with visual ticket management
- **Testing:** Load test with 100 concurrent users, 200 orders/hour

---

## 6. FRANCHISE MODEL & MULTI-TENANCY

### Risk Level: 🔴 **CRITICAL**

### Problem Statement

Vision: "Expand to 25+ franchises" — but zero definition of data isolation, pricing control, menu override, or royalty tracking.

### Real-World Scenario

**Scenario A: Data Leakage**

- Franchisee A: "Why can I see Franchisee B's sales numbers?"
- System has no tenant isolation
- All franchisees see all sales data
- Business sensitivity: Revenue data should be confidential
- Legal risk: Data breach, breach of franchisee agreements

**Scenario B: Menu Override Failure**

- Central office pushes "Fried Chicken Combo" at ₹350
- Franchisee in expensive metro city: "That's too cheap. Cost is ₹240. Margin only ₹110."
- Franchisee in small town: "₹350 is too expensive. No one will buy."
- System has no per-franchise pricing
- Franchisee manually edits DB; audit trail lost
- Central office can't track who changed what

**Scenario C: Royalty Miscalculation**

- Franchisee A revenue: ₹500,000
- Royalty due: 5% = ₹25,000
- System doesn't calculate or track royalties
- Manual invoice at end of month
- Franchisee disputes: "My revenue was ₹480,000."
- No digital agreement on calculation

**Scenario D: Multi-Currency**

- Future: Expand to Nepal, Sri Lanka
- Currency: NPR, LKR
- System designed for ₹ only
- Exchange rates fluctuate daily
- No currency conversion logic

### Missing Requirements

| Requirement ID | Requirement              | Acceptance Criteria                                              |
| -------------- | ------------------------ | ---------------------------------------------------------------- |
| FRAN-001       | Multi-tenancy            | Complete data isolation per franchisee; no data leakage          |
| FRAN-002       | Row-level security (RLS) | DB enforces: franchisee sees only their data                     |
| FRAN-003       | Menu override            | Franchisee can override central menu item price/availability     |
| FRAN-004       | Regional variants        | Franchisee can add local menu items (not on central menu)        |
| FRAN-005       | Pricing rules            | Support: base price + regional premium + seasonal discount       |
| FRAN-006       | Royalty tracking         | Auto-calculate royalty % on daily revenue                        |
| FRAN-007       | Royalty invoice          | Auto-generate monthly royalty invoice per franchisee             |
| FRAN-008       | Payment routing          | Revenue split: franchisee account vs. central account            |
| FRAN-009       | Operator billing         | Track which franchisee paid subscription fee, when               |
| FRAN-010       | Multi-currency           | Support ₹, $, €, NPR, LKR; auto-convert for reporting            |
| FRAN-011       | Exchange rates           | Daily rate updates; historical tracking                          |
| FRAN-012       | Compliance by region     | Support different tax rules: GST (India), VAT (others)           |
| FRAN-013       | Franchise SLA            | Define uptime, support hours, incident response time             |
| FRAN-014       | Feature rollout          | Gradual rollout of new features to franchisees; rollback support |

### System Design Impact

- **Architecture:** SaaS multi-tenant with isolated databases per franchisee (or schema-isolated)
- **Database:** Tenant ID on every table; RLS policies enforced at DB layer
- **API:** Tenant context passed through entire stack; middleware validates permission
- **Pricing:** Configuration table for each franchisee overrides
- **Reporting:** Aggregated reports for corporate; isolated reports for franchisee
- **Compliance:** Tax rules configurable per franchisee; auto-generated tax reports

---

## 7. SECURITY & COMPLIANCE BLIND SPOTS

### Risk Level: 🟡 **MEDIUM**

### Problem Statement

Requirements mention "GST Invoice" and "Role-Based Access" but lack permission matrix, audit trails, and compliance enforcement.

### Real-World Scenario

**Scenario A: Unauthorized Discount**

- Cashier A applies ₹5000 discount to friend's bill
- Bill was ₹10,000; friend pays only ₹5,000
- Owner discovers: manual audit of bills
- System has no audit trail; can't prove who discounted
- Suspicion falls on cashier A, but no evidence
- HR dispute; potential wrongful termination lawsuit

**Scenario B: Manager Permission Abuse**

- Manager has access to "Delete Order" (for legitimate refunds)
- Manager deletes 10 orders totaling ₹50,000 revenue
- System records deleted, but no "why" explanation
- Owner asks: "Why so many deletes?" → "System error" (false)
- Audit finds theft: manager refunded self + accomplices
- Manager already fled; minimal recovery

**Scenario C: Privacy Violation**

- Customer phone numbers: 2000+ stored in system
- Employee exports customer list to personal laptop
- Laptop stolen
- Customers' phone numbers used for spam marketing by competitor
- Compliance liability: potential legal action

### Missing Requirements

| Requirement ID | Requirement           | Acceptance Criteria                                                                  |
| -------------- | --------------------- | ------------------------------------------------------------------------------------ |
| SEC-001        | Permission matrix     | Define: who can do what (Owner → all; Manager → branch only; Cashier → billing only) |
| SEC-002        | Role definitions      | Define 5+ roles; document each role's permissions                                    |
| SEC-003        | Audit trail           | Every action logged: user, timestamp, action, before/after state                     |
| SEC-004        | Change approval       | Actions >₹5000 require manager approval before execution                             |
| SEC-005        | Deletion logging      | Soft deletes; history preserved; original user recorded                              |
| SEC-006        | Data encryption       | Customer PII encrypted at rest; SSL/TLS in transit                                   |
| SEC-007        | Access logs           | Track: who logged in, when, from where, duration                                     |
| SEC-008        | Password policy       | Min 8 chars, complexity, expiry 90 days, no reuse                                    |
| SEC-009        | Session timeout       | Auto-logout after 30 minutes inactivity                                              |
| SEC-010        | Two-factor auth (2FA) | Optional for high-privilege users (owner, managers)                                  |
| SEC-011        | Data masking          | Mask customer PII in logs; full number only for authorized users                     |
| SEC-012        | Export controls       | Restrict data export; require manager approval; log export                           |
| SEC-013        | Compliance reports    | Generate audit reports for tax/regulatory audits                                     |
| SEC-014        | GDPR readiness        | Support data deletion requests, data portability                                     |

### System Design Impact

- **Database:** Immutable audit log table; soft delete pattern
- **API:** Permission middleware; action validation before execution
- **UI:** Feature visibility based on role; confirmation dialogs for high-risk actions
- **Compliance:** Audit report generation; compliance checklist
- **Monitoring:** Alert on unusual activity: 50+ deletions/day, export >1000 rows

---

## 8. PROFITABILITY METRICS & FINANCIAL ANALYSIS

### Risk Level: 🟡 **MEDIUM**

### Problem Statement

Current reports: "Daily Sales, Monthly Sales, Branch-wise Sales" — but zero measurement of profitability, margins, or efficiency.

### Real-World Scenario

**Scenario: False Profitability**

- Report shows: Branch 1 revenue ₹500k/month, Branch 2 revenue ₹480k/month
- Owner conclusion: "Branch 1 is best; replicate its model"
- Hidden reality:
  - Branch 1: Food cost ₹180k (36%), Waste ₹40k (8%), Labor ₹150k (30%) → Profit ₹130k (26%)
  - Branch 2: Food cost ₹144k (30%), Waste ₹12k (2.5%), Labor ₹130k (27%) → Profit ₹194k (40%)
- Branch 2 is actually 49% more profitable (₹194k vs ₹130k)
- Owner makes wrong strategic decision based on incomplete data

### Missing Requirements

| Requirement ID | Requirement                | Acceptance Criteria                                           |
| -------------- | -------------------------- | ------------------------------------------------------------- |
| FIN-001        | Gross margin per item      | Calculate: (selling price - food cost) / selling price        |
| FIN-002        | Gross margin by category   | Chicken category: margin X%; Pizza: margin Y%                 |
| FIN-003        | Food cost % tracking       | Daily: total ingredient cost ÷ total revenue                  |
| FIN-004        | Waste analysis             | Separate: spoilage %, theft %, normal trim %, unaccounted %   |
| FIN-005        | Labor efficiency           | Payroll per branch ÷ revenue = labor cost % (target <30%)     |
| FIN-006        | Table turnover rate        | Orders per table per day; compare branches                    |
| FIN-007        | Customer repeat rate       | % of customers who return within 30 days                      |
| FIN-008        | Customer acquisition       | Track: new customers per day; trend                           |
| FIN-009        | Average order value (AOV)  | Total revenue ÷ total orders; trend by day/week/month         |
| FIN-010        | Peak vs. off-peak analysis | Revenue during peak hours (6-9pm) vs. off-peak                |
| FIN-011        | Discount impact            | Total discounts given ÷ revenue = discount %; trend           |
| FIN-012        | Profitability dashboard    | Branch-wise profit margin comparison; identify inefficiencies |
| FIN-013        | Variance analysis          | Actual cost vs. budgeted cost; alert if >10% variance         |
| FIN-014        | Trend analysis             | Compare metrics month-over-month; alert on decline            |

### System Design Impact

- **Database:** Sales ledger, inventory cost tracking, labor records linked
- **Calculations:** Real-time profit margin calculation; daily rollup
- **Reporting:** Profitability dashboard; variance alerts; trend charts
- **Integration:** Payroll system (to get labor costs)
- **Analytics:** Predictive: if trends continue, profit forecast for next month

---

## 9. MENU & PRICING FLEXIBILITY

### Risk Level: 🟡 **MEDIUM**

### Problem Statement

Current requirement: "Standardized menu across all branches" — but zero flexibility for dynamic pricing, regional variants, or seasonal updates.

### Real-World Scenario

**Scenario A: Dynamic Pricing Failure**

- Owner wants: Happy Hour 6-8pm, all burgers 30% off
- System has no time-based pricing rules
- Cashier manually changes burger price at 6pm, changes back at 8pm
- Errors: forgot to change Tuesday, Thursday price change applied Monday
- System records show inconsistent pricing; margins unpredictable

**Scenario B: Regional Variation**

- Central menu: "Fried Chicken Combo" ₹400
- North branch wants it at ₹450 (premium market, high rent)
- South branch wants it at ₹350 (price-sensitive market)
- Central system has no override
- South branch manually edits inventory; audit trail lost
- Owner can't see why North and South have different prices

**Scenario C: Seasonal Item Management**

- Summer: "Cold Lassi" promoted, featured on menu
- Winter: "Hot Coffee" featured
- System has no version control
- Manual process: update menu, print new bill books, train staff
- Error: "Cold Lassi" still appears on winter menu; customer confused

### Missing Requirements

| Requirement ID | Requirement              | Acceptance Criteria                                          |
| -------------- | ------------------------ | ------------------------------------------------------------ |
| MENU-001       | Dynamic pricing          | Support time-based pricing (6-8pm: 30% off)                  |
| MENU-002       | Discount rules           | Define: day-based, time-based, quantity-based discounts      |
| MENU-003       | Combo rules              | E.g., "Buy Chicken + Fries, get drink free"                  |
| MENU-004       | Regional pricing         | Override central price per franchisee/branch                 |
| MENU-005       | Seasonal items           | Add/remove items by date; version control                    |
| MENU-006       | Item availability        | Mark unavailable at time-of-ordering; remove from menu       |
| MENU-007       | Ingredient price updates | When chicken price changes, auto-update "Chicken Combo" cost |
| MENU-008       | Promotional item         | Flag items on promotion; track impact on sales               |
| MENU-009       | Menu history             | Track: who changed what, when, why (change log)              |
| MENU-010       | Menu approval            | Owner approves menu changes before going live                |
| MENU-011       | Menu rollout             | Gradual rollout to branches; schedule future changes         |
| MENU-012       | Category grouping        | Organize menu: Appetizers, Mains, Beverages, Desserts        |
| MENU-013       | Variant support          | "Burger: Small/Medium/Large" with different prices           |
| MENU-014       | Allergen info            | Track allergens: nuts, dairy, gluten, etc.                   |

### System Design Impact

- **Database:** Menu version history; pricing rules engine; allergen tracking
- **API:** Dynamic price calculation based on rules; time/date checking
- **UI:** Menu builder with rule engine; approval workflow
- **Kitchen Display:** Display promotions; flag allergens on KOT
- **Reporting:** Promo effectiveness; sales by variant; allergen queries

---

## 10. CUSTOMER DATA & LOYALTY

### Risk Level: 🟡 **MEDIUM**

### Problem Statement

Current requirement: "Customer Management" — but zero definition of data capture, repeat tracking, preferences, or loyalty mechanics.

### Real-World Scenario

**Scenario A: Lost Customer Insight**

- Customer A visits 5 times over 2 months; total spend ₹5000
- Customer hasn't returned in 30 days
- Owner doesn't know: Customer is unhappy? Moved away? Busy? Forgot?
- No system to flag at-risk customers; no retention strategy

**Scenario B: Preference Ignored**

- Repeat customer: "I'm vegetarian; always order vegetables"
- Cashier doesn't know; kitchen receives order without note
- Non-veg item accidentally prepared
- Customer angry; wastes food; reputation damage

**Scenario C: Loyalty Abandoned**

- Owner says: "We'll build a loyalty program later"
- Competitors offer: "Stamp card: 10 purchases, 1 free"
- AFC doesn't offer loyalty; customers drift to competitors
- Lost revenue: 20% of potential repeat business

### Missing Requirements

| Requirement ID | Requirement                    | Acceptance Criteria                                           |
| -------------- | ------------------------------ | ------------------------------------------------------------- |
| CUST-001       | Customer data capture          | Collect: name, phone, email (optional) at billing             |
| CUST-002       | Phone-based lookup             | Cashier enters phone; system shows customer history           |
| CUST-003       | Customer preferences           | Track: vegetarian/non-veg, allergies, favorite items          |
| CUST-004       | Visit tracking                 | Log: date, time, amount, items ordered                        |
| CUST-005       | Repeat customer identification | "This is your 3rd visit" message to cashier                   |
| CUST-006       | At-risk alert                  | Flag if customer hasn't visited in 30+ days                   |
| CUST-007       | Loyalty points                 | Award 1 point per ₹10 spent; track points                     |
| CUST-008       | Loyalty redemption             | 100 points = ₹500 discount; redeemable                        |
| CUST-009       | Referral tracking              | New customer: "Referred by [existing customer]"               |
| CUST-010       | Customer segment               | Classify: high-value (>₹10k), regular (₹2-10k), casual (<₹2k) |
| CUST-011       | Personalized offers            | Offer: "You always order burgers; 20% off today"              |
| CUST-012       | Birthday offers                | Award discount on customer's birthday (if birthday captured)  |
| CUST-013       | Customer feedback              | Post-order survey: rate experience; flag complaints           |
| CUST-014       | Privacy compliance             | GDPR: support deletion request, data export                   |

### System Design Impact

- **Database:** Customer master; visit history; preference tags; loyalty ledger
- **API:** Customer lookup, preference retrieval, loyalty calculation
- **UI:** Customer dashboard; preference display at billing; loyalty balance
- **Analytics:** Customer lifetime value (CLV); churn prediction; segment analysis
- **Marketing:** Email/SMS to at-risk customers; personalized offers

---

## 11. TABLE MANAGEMENT & RESERVATIONS

### Risk Level: 🟢 **LOW** (but real)

### Problem Statement

Current requirement: "Table Management" — but zero handling for reservations, guest count changes, or table merging.

### Real-World Scenario

**Scenario A: Table Overallocation**

- 3 customers call: "Book table for 4, tomorrow 7pm"
- Only 2 tables available
- Staff double-books: assigns both customers to same table
- Next day: Both parties arrive; conflict
- System has no reservation tracking; no overbooking prevention

**Scenario B: Guest Count Change**

- Reservation: Party of 4
- Party arrives: 6 people (friends joined)
- No table for 6; forced to split
- Customer angry; bad experience

**Scenario C: Service Time Creep**

- Table 3 seated: 7pm
- Still there: 9:45pm
- Kitchen has fresh order; no table available
- Customer waits 30+ minutes
- No system alert to manager

### Missing Requirements

| Requirement ID | Requirement              | Acceptance Criteria                                       |
| -------------- | ------------------------ | --------------------------------------------------------- |
| TABLE-001      | Reservation system       | Book table by date/time; capture guest count, name, phone |
| TABLE-002      | Overbooking prevention   | System prevents double-booking same table same time       |
| TABLE-003      | Reservation reminder     | SMS/call 24 hours before; no-show tracking                |
| TABLE-004      | Guest count flexibility  | Allow +/- 1 guest without penalizing                      |
| TABLE-005      | Table merging            | Merge adjacent tables for larger parties; single bill     |
| TABLE-006      | Service time tracking    | Alert if table >2 hours without new order                 |
| TABLE-007      | Table turnover rate      | Track: avg time per table; compare to targets             |
| TABLE-008      | Waitlist management      | If no table available, add to waitlist; notify when ready |
| TABLE-009      | VIP flagging             | Mark VIP customers; priority seating; special treatment   |
| TABLE-010      | Table occupation display | UI shows: which tables occupied, how long, status         |

### System Design Impact

- **Database:** Reservation ledger; table status tracking
- **API:** Reservation booking, table assignment, waitlist
- **UI:** Reservation dashboard; table occupancy heatmap
- **Alerts:** Service time warnings; no-show alerts; waitlist notifications
- **Analytics:** Table turnover rate; occupancy %; revenue per table

---

## 12. DELIVERY & QR ORDERING (PHASE 2 DEPENDENCIES)

### Risk Level: 🔴 **CRITICAL** (marked as "Future" but blocks architecture)

### Problem Statement

Current scope excludes "Delivery" and "QR Ordering" — but architecture decisions made now will need rework later.

### Real-World Scenario

**Scenario: Phase 2 Rework Hell**

- Phase 1 complete: POS, billing, inventory built
- Phase 2 planned: QR ordering
- Problem: Architecture assumes orders originate from Cashier
- QR ordering: Orders originate from customer's phone
- Kitchen expects: Customer name, table number
- QR orders: No table (online), no customer name (just phone)
- System redesign needed; significant rework; delays, budget overrun

### Missing Requirements

| Requirement ID | Requirement            | Acceptance Criteria                                               |
| -------------- | ---------------------- | ----------------------------------------------------------------- |
| QR-001         | QR code generation     | Each table has unique QR code linking to order form               |
| QR-002         | Mobile order interface | Customer-facing: select items, customize, checkout                |
| QR-003         | Order integration      | QR orders flow into same KDS as POS orders                        |
| QR-004         | Delivery address       | Capture delivery address for takeaway/delivery                    |
| QR-005         | Real-time status       | Customer sees: order received, preparing, ready, out for delivery |
| QR-006         | Payment gateway        | Online payment: UPI, card, wallet                                 |
| QR-007         | Estimated time         | System calculates: prep time, delivery time; displays to customer |
| QR-008         | Driver assignment      | Admin assigns order to delivery driver                            |
| QR-009         | Driver app             | Separate app: see pending orders, navigate, mark delivered        |
| QR-010         | Delivery tracking      | Customer tracks driver location (Google Maps integration)         |
| QR-011         | Order aggregation      | Group multiple QR orders by prep time; optimize kitchen flow      |
| QR-012         | Delivery analytics     | Track: delivery time variance, driver efficiency                  |

### System Design Impact

- **Architecture:** Orders table must support source (POS, QR, app)
- **API:** Order creation from mobile; real-time status updates (WebSocket)
- **UI:** Customer-facing order portal; driver app; tracking dashboard
- **Integration:** Google Maps for delivery tracking; payment gateway for online orders
- **Testing:** Load test: 1000 concurrent QR orders during lunch rush

---

## 13. DATA MIGRATION & LEGACY CONTINUITY

### Risk Level: 🟡 **MEDIUM**

### Problem Statement

Current state: Excel sheets, notebooks — but zero strategy for migration, data integrity, or parallel-run risk.

### Real-World Scenario

**Scenario: Migration Disaster**

- Current data: 2 years of sales in Excel (manual entries, errors)
- Import into system: 10,000 transactions loaded
- After 2 weeks: Owner asks "Why does February revenue differ from last year's total?"
- Investigation: Excel had ₹50,000 in Feb; system shows ₹49,200
- Data loss? System error? Invalid migration? Unknown.
- Audit trail lost; financial records questioned

### Missing Requirements

| Requirement ID | Requirement         | Acceptance Criteria                                         |
| -------------- | ------------------- | ----------------------------------------------------------- |
| MIG-001        | Data inventory      | List all data sources (Excel files, notebooks, systems)     |
| MIG-002        | Data validation     | Verify source data integrity; identify anomalies, gaps      |
| MIG-003        | Data cleansing      | Standardize formats, remove duplicates, fix errors          |
| MIG-004        | Migration plan      | Define: what to migrate, timeline, validation steps         |
| MIG-005        | Test migration      | Run migration on copy; validate results before production   |
| MIG-006        | Parallel run period | Run old + new system for 2 weeks; compare results           |
| MIG-007        | Cutover plan        | Define: date, time, rollback procedure if issues arise      |
| MIG-008        | Data reconciliation | Post-migration: compare totals; investigate discrepancies   |
| MIG-009        | User training       | Train staff on new system before cutover; practice runs     |
| MIG-010        | Fallback procedure  | If system fails, revert to manual; procedure documented     |
| MIG-011        | Audit trail         | Keep migration logs; track what was imported, by whom, when |
| MIG-012        | Archive legacy data | Preserve old Excel/notebooks for 3+ years for audit         |

### System Design Impact

- **Data:** Import scripts with validation; audit logs; manual reconciliation checklist
- **Testing:** Test migration with 2+ years of data; stress test; performance verification
- **Operations:** Parallel run checklist; training schedule; cutover runbook
- **Compliance:** Data retention policy; archival process

---

## 14. STAFF MONITORING & LABOR ANALYTICS

### Risk Level: 🟡 **MEDIUM**

### Problem Statement

Current pain point: "Hard to monitor staff activities" — but system doesn't track shifts, performance, or labor efficiency.

### Real-World Scenario

**Scenario: Labor Cost Creep**

- Month 1: 2 cashiers, staff cost ₹50,000
- Month 2: 2.5 cashiers, staff cost ₹62,500
- Month 3: 3 cashiers, staff cost ₹75,000
- Owner asks: "Why are labor costs rising?"
- System doesn't track: shift lengths, overtime, productivity
- Manager says: "Traffic increased; needed more staff"
- But billing traffic only up 8%; labor cost up 50%
- System has no efficiency metrics; can't diagnose problem

### Missing Requirements

| Requirement ID | Requirement           | Acceptance Criteria                                                |
| -------------- | --------------------- | ------------------------------------------------------------------ |
| LABOR-001      | Shift management      | Log: who works, when, how long, role (cashier, kitchen, manager)   |
| LABOR-002      | Attendance tracking   | Attendance/absence logs; late arrivals flagged                     |
| LABOR-003      | Overtime tracking     | Overtime hours logged; overtime pay calculated                     |
| LABOR-004      | Staff performance     | Avg billing time per cashier; orders per kitchen staff per hour    |
| LABOR-005      | Productivity metrics  | Revenue per staff member; transactions per hour                    |
| LABOR-006      | Quality metrics       | Order mistakes per kitchen staff; customer complaints              |
| LABOR-007      | Cash variance         | If drawer short, investigate associated cashier; pattern detection |
| LABOR-008      | Audit trail           | Every action logged with staff ID (who, what, when)                |
| LABOR-009      | Payroll export        | Export shifts/hours to payroll system for salary calculation       |
| LABOR-010      | Labor cost %          | Payroll ÷ revenue; target <30%; alert if exceeded                  |
| LABOR-011      | Schedule optimization | Suggest optimal staffing for predicted traffic                     |
| LABOR-012      | Training tracking     | Log training completed; certifications (food safety, etc.)         |

### System Design Impact

- **Database:** Staff master, shift logs, performance metrics, audit trail
- **API:** Login/logout timestamp, action logging with staff ID
- **UI:** Staff dashboard showing: today's shifts, performance metrics
- **Integration:** Payroll system export; HR system (if exists)
- **Analytics:** Labor efficiency trends; cost per transaction; productivity benchmarks

---

## Summary: Priority Matrix

### By Risk Level & Impact

| Rank | Gap                     | Risk        | Impact          | Phase               |
| ---- | ----------------------- | ----------- | --------------- | ------------------- |
| 1    | Payment & Settlement    | 🔴 CRITICAL | Revenue + Trust | MVP                 |
| 2    | Franchise Model         | 🔴 CRITICAL | Business Model  | MVP                 |
| 3    | Offline Resilience      | 🔴 HIGH     | Revenue Loss    | MVP                 |
| 4    | Rush Hour Performance   | 🔴 HIGH     | UX + Revenue    | MVP                 |
| 5    | Inventory Perishability | 🔴 HIGH     | Cost Control    | MVP                 |
| 6    | Order Flow Edge Cases   | 🟡 MEDIUM   | UX + Refund     | MVP                 |
| 7    | Profitability Metrics   | 🟡 MEDIUM   | Strategy        | Phase 1             |
| 8    | Menu & Pricing          | 🟡 MEDIUM   | Flexibility     | Phase 1             |
| 9    | Security & Compliance   | 🟡 MEDIUM   | Legal + Trust   | MVP                 |
| 10   | Customer Data           | 🟡 MEDIUM   | Retention       | Phase 1             |
| 11   | Staff Monitoring        | 🟡 MEDIUM   | Efficiency      | Phase 1             |
| 12   | Data Migration          | 🟡 MEDIUM   | Accuracy        | Cutover             |
| 13   | Table Management        | 🟢 LOW      | UX              | Phase 2             |
| 14   | QR/Delivery             | 🔴 CRITICAL | Future Scope    | Design Now, Phase 2 |

---

## Next Steps

1. **Review & Validate** – Confirm which gaps are critical for MVP vs. Phase 1 vs. Phase 2
2. **Prioritize** – Decide implementation order based on business priority
3. **Define Acceptance Criteria** – For each requirement, define pass/fail conditions
4. **Create PRD** – Translate gaps + requirements into formal Product Requirements Document
5. **Architecture Design** – Ensure multi-tenancy, offline resilience, and scalability are baked in from day 1
6. **Risk Mitigation** – Plan for migration, training, cutover, and rollback scenarios

---

**Document Version:** 1.0  
**Created:** 30 June 2026  
**Status:** Ready for stakeholder review and prioritization
