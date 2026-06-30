# Critical Requirements Matrix

## AFC Restaurant Management System

**Version:** 1.0  
**Date:** 30 June 2026  
**Purpose:** Quick reference matrix of all critical gaps and requirements

---

## Quick Reference: Gap Summary & Priority

```
🔴 CRITICAL (Must have in MVP)
├── Payment & Settlement (14 requirements)
├── Franchise Model (14 requirements)
├── Offline Resilience (8 requirements)
├── Rush Hour Performance (10 requirements)
├── Inventory Perishability (12 requirements)
├── Security & Compliance (14 requirements)
└── QR/Delivery (Architecture only)

🟡 HIGH (MVP or very early Phase 1)
├── Order Flow Edge Cases (10 requirements)
├── Menu & Pricing (14 requirements)

🟠 MEDIUM (Phase 1)
├── Profitability Metrics (14 requirements)
├── Customer Data & Loyalty (14 requirements)
├── Staff Monitoring (12 requirements)
├── Data Migration (12 requirements)

🟢 LOW (Phase 2 or nice-to-have)
└── Table Management (10 requirements)
```

---

## Requirements Dependency Graph

```
┌─────────────────────────────────────────────────────────┐
│                   ARCHITECTURE LAYER                     │
│    Multi-Tenancy | Offline Sync | API Design | Security │
└─────────────────────────────────────────────────────────┘
                           ↑
              ┌────────────┼────────────┐
              ↓            ↓            ↓
    ┌──────────────┐ ┌──────────┐ ┌─────────────┐
    │ CORE FEATURES│ │ PAYMENT  │ │ INVENTORY   │
    ├──────────────┤ ├──────────┤ ├─────────────┤
    │ POS Billing  │ │Settlement│ │ Perishability
    │ KOT          │ │ Refunds  │ │ BOM Tracking
    │ Table Mgmt   │ │ Disputes │ │ Food Cost
    └──────────────┘ └──────────┘ └─────────────┘
              ↓            ↓            ↓
    ┌──────────────────────────────────────────┐
    │        REPORTING & ANALYTICS LAYER        │
    ├──────────────────────────────────────────┤
    │ Profitability | Labor | Customer | Menu  │
    └──────────────────────────────────────────┘
              ↓
    ┌──────────────────────────────────────────┐
    │         PHASE 2: QR + DELIVERY           │
    └──────────────────────────────────────────┘
```

---

## Gap-to-Requirement Matrix

### 1. OFFLINE RESILIENCE

| Req ID  | Requirement          | Type        | MVP | Effort | Risk   | Dependencies   |
| ------- | -------------------- | ----------- | --- | ------ | ------ | -------------- |
| OFF-001 | Offline mode for POS | Core        | ✅  | Medium | Low    | API, DB sync   |
| OFF-002 | Transaction queue    | Core        | ✅  | Medium | Low    | DB, sync       |
| OFF-003 | Conflict resolution  | Core        | ✅  | High   | Medium | Business logic |
| OFF-004 | Order status sync    | Core        | ✅  | Medium | Low    | API            |
| OFF-005 | Data integrity       | Core        | ✅  | Low    | Low    | DB constraints |
| OFF-006 | Staff notification   | UI          | ✅  | Low    | Low    | UI framework   |
| OFF-007 | Recovery time SLA    | Testing     | ✅  | Medium | Low    | Network sim    |
| OFF-008 | Menu caching         | Performance | ✅  | Low    | Low    | Cache layer    |

**MVP Scope:** All 8 requirements  
**Key Decision:** Sync conflict strategy (e.g., server wins, client wins, merge)

---

### 2. PAYMENT & SETTLEMENT

| Req ID  | Requirement         | Type        | MVP | Effort | Risk   | Dependencies      |
| ------- | ------------------- | ----------- | --- | ------ | ------ | ----------------- |
| PAY-001 | Payment gateway     | Integration | ✅  | High   | Low    | Razorpay/PayU     |
| PAY-002 | Cash reconciliation | Process     | ✅  | Medium | Medium | EOD workflow      |
| PAY-003 | Float management    | Process     | ✅  | Low    | Low    | UI                |
| PAY-004 | Split bill tracking | Core        | ✅  | High   | High   | Complex logic     |
| PAY-005 | Payment failure     | Core        | ✅  | High   | High   | Refund flow       |
| PAY-006 | Partial payments    | Core        | ⚠️  | Medium | Medium | Balance tracking  |
| PAY-007 | Refund flow         | Core        | ✅  | High   | High   | Business logic    |
| PAY-008 | Chargeback handling | Process     | ⚠️  | Low    | Low    | Reporting         |
| PAY-009 | Audit trail         | Core        | ✅  | Low    | Low    | Logging           |
| PAY-010 | EOD settlement      | Process     | ✅  | Medium | Low    | Reporting         |
| PAY-011 | Multi-currency      | Future      | ❌  | Low    | Low    | Phase 2           |
| PAY-012 | Payment reversal    | Core        | ✅  | Medium | Medium | Approval workflow |

**MVP Scope:** 10 of 12 (exclude multi-currency, chargeback simplify)  
**Estimated Effort:** 120-150 hours  
**Risk:** HIGH (complex logic, financial compliance)

---

### 3. INVENTORY PERISHABILITY

| Req ID  | Requirement             | Type          | MVP | Effort | Risk   | Dependencies    |
| ------- | ----------------------- | ------------- | --- | ------ | ------ | --------------- |
| INV-001 | Expiry date tracking    | Core          | ✅  | Medium | Low    | UI, DB          |
| INV-002 | FIFO rotation           | Core          | ✅  | Medium | Low    | Logic, reports  |
| INV-003 | Bill of Materials       | Core          | ✅  | High   | Medium | Data model      |
| INV-004 | Auto-deduction          | Core          | ✅  | High   | High   | Complex logic   |
| INV-005 | Waste tracking          | Core          | ✅  | Medium | Low    | Categorization  |
| INV-006 | Waste alerts            | Monitoring    | ⚠️  | Low    | Low    | Thresholds      |
| INV-007 | Food cost %             | Analytics     | ⚠️  | Medium | Low    | Calculations    |
| INV-008 | Supplier lead time      | Configuration | ⚠️  | Low    | Low    | Master data     |
| INV-009 | Stock-out procedure     | Process       | ✅  | Low    | Low    | Business logic  |
| INV-010 | Ingredient substitution | Core          | ⚠️  | Medium | Medium | Cost adjustment |
| INV-011 | Stock rotation report   | Reporting     | ⚠️  | Low    | Low    | Analytics       |
| INV-012 | Batch reconciliation    | Process       | ✅  | Low    | Low    | Audit           |

**MVP Scope:** 9 of 12 (defer food cost %, lead time, rotation report)  
**Estimated Effort:** 140-170 hours  
**Risk:** HIGH (impacts food safety, cost control)

---

### 4. ORDER FLOW EDGE CASES

| Req ID  | Requirement           | Type       | MVP | Effort | Risk   | Dependencies     |
| ------- | --------------------- | ---------- | --- | ------ | ------ | ---------------- |
| ORD-001 | Kitchen rejection     | Core       | ✅  | High   | High   | Refund flow      |
| ORD-002 | Order modification    | Core       | ✅  | High   | High   | Complex logic    |
| ORD-003 | Modification tracking | Audit      | ✅  | Low    | Low    | Logging          |
| ORD-004 | Partial fulfillment   | Core       | ⚠️  | High   | High   | Service flow     |
| ORD-005 | Item-level status     | Core       | ✅  | Medium | Low    | UI               |
| ORD-006 | Cancel order          | Core       | ✅  | Medium | Medium | Approval, refund |
| ORD-007 | Stale order alert     | Monitoring | ✅  | Low    | Low    | Timer logic      |
| ORD-008 | Special requests      | UI         | ✅  | Low    | Low    | Text field       |
| ORD-009 | Hold orders           | Core       | ⚠️  | Low    | Low    | Status           |
| ORD-010 | Remake tracking       | Process    | ⚠️  | Low    | Low    | Linking          |

**MVP Scope:** 8 of 10 (partial fulfillment, hold orders Phase 1)  
**Estimated Effort:** 130-160 hours  
**Risk:** HIGH (UX-critical, must work flawlessly)

---

### 5. RUSH HOUR PERFORMANCE

| Req ID   | Requirement                    | Type           | MVP | Effort | Risk   | Dependencies |
| -------- | ------------------------------ | -------------- | --- | ------ | ------ | ------------ |
| PERF-001 | Throughput SLA (100 orders/hr) | Testing        | ✅  | High   | High   | Load test    |
| PERF-002 | Latency SLA (<2sec p95)        | Testing        | ✅  | High   | High   | Profiling    |
| PERF-003 | Kitchen Display System         | UI             | ✅  | High   | Medium | Hardware     |
| PERF-004 | Queue visualization            | UI             | ⚠️  | Low    | Low    | Analytics    |
| PERF-005 | Stress testing                 | Testing        | ✅  | High   | High   | Tools, time  |
| PERF-006 | Connection pooling             | Infrastructure | ✅  | Low    | Low    | DB config    |
| PERF-007 | Caching                        | Infrastructure | ✅  | Medium | Low    | Redis        |
| PERF-008 | API rate limiting              | Infrastructure | ✅  | Low    | Low    | API gateway  |
| PERF-009 | Table turnover tracking        | Analytics      | ⚠️  | Low    | Low    | Timer        |
| PERF-010 | Reserved seating               | Future         | ❌  | Low    | Low    | Phase 2      |

**MVP Scope:** 8 of 10 (queue viz, reserved seating Phase 2)  
**Estimated Effort:** 150-200 hours (includes testing)  
**Risk:** CRITICAL (must prove system handles peak load)

---

### 6. FRANCHISE MODEL

| Req ID   | Requirement         | Type         | MVP | Effort | Risk   | Dependencies        |
| -------- | ------------------- | ------------ | --- | ------ | ------ | ------------------- |
| FRAN-001 | Multi-tenancy       | Architecture | ✅  | High   | Medium | DB design           |
| FRAN-002 | Row-level security  | Database     | ✅  | High   | High   | RLS implementation  |
| FRAN-003 | Menu override       | Core         | ✅  | Medium | Low    | UI, logic           |
| FRAN-004 | Regional variants   | Core         | ✅  | Medium | Low    | Configuration       |
| FRAN-005 | Pricing rules       | Core         | ✅  | High   | Medium | Rule engine         |
| FRAN-006 | Royalty tracking    | Analytics    | ⚠️  | Medium | Low    | Calculations        |
| FRAN-007 | Royalty invoice     | Reporting    | ⚠️  | Low    | Low    | PDF generation      |
| FRAN-008 | Payment routing     | Finance      | ⚠️  | Medium | High   | Banking integration |
| FRAN-009 | Operator billing    | Finance      | ⚠️  | Low    | Low    | Subscription mgmt   |
| FRAN-010 | Multi-currency      | Future       | ❌  | Medium | Low    | Phase 2             |
| FRAN-011 | Exchange rates      | Future       | ❌  | Low    | Low    | Phase 2             |
| FRAN-012 | Regional compliance | Compliance   | ⚠️  | Medium | High   | Legal review        |
| FRAN-013 | Franchise SLA       | Process      | ⚠️  | Low    | Low    | Documentation       |
| FRAN-014 | Feature rollout     | Operations   | ✅  | Low    | Low    | Release management  |

**MVP Scope:** 9 of 14 (defer royalty, royalty invoice, payment routing, currency, compliance)  
**Estimated Effort:** 160-200 hours  
**Risk:** CRITICAL (architecture decision, cannot retrofit)

---

### 7. SECURITY & COMPLIANCE

| Req ID  | Requirement        | Type           | MVP | Effort | Risk | Dependencies      |
| ------- | ------------------ | -------------- | --- | ------ | ---- | ----------------- |
| SEC-001 | Permission matrix  | Process        | ✅  | Low    | Low  | Documentation     |
| SEC-002 | Role definitions   | Process        | ✅  | Low    | Low  | RBAC design       |
| SEC-003 | Audit trail        | Core           | ✅  | Low    | Low  | Logging           |
| SEC-004 | Change approval    | Process        | ⚠️  | Low    | Low  | Workflow          |
| SEC-005 | Deletion logging   | Core           | ✅  | Low    | Low  | Soft deletes      |
| SEC-006 | Data encryption    | Infrastructure | ✅  | Medium | Low  | SSL/TLS, DB       |
| SEC-007 | Access logs        | Core           | ✅  | Low    | Low  | Login tracking    |
| SEC-008 | Password policy    | Infrastructure | ✅  | Low    | Low  | Auth system       |
| SEC-009 | Session timeout    | Infrastructure | ✅  | Low    | Low  | Auth system       |
| SEC-010 | 2FA (optional)     | Infrastructure | ⚠️  | Medium | Low  | TOTP              |
| SEC-011 | Data masking       | Core           | ✅  | Low    | Low  | Log filtering     |
| SEC-012 | Export controls    | UI             | ⚠️  | Low    | Low  | Buttons, logging  |
| SEC-013 | Compliance reports | Reporting      | ⚠️  | Low    | Low  | Report generation |
| SEC-014 | GDPR readiness     | Process        | ⚠️  | Low    | Low  | Data deletion API |

**MVP Scope:** 11 of 14 (defer change approval, 2FA, export controls, compliance reports, GDPR)  
**Estimated Effort:** 60-80 hours  
**Risk:** MEDIUM (security important but baseline covered)

---

### 8. PROFITABILITY METRICS (Phase 1)

| Req ID  | Requirement              | Type      | Phase1 | Effort | Risk   | Dependencies        |
| ------- | ------------------------ | --------- | ------ | ------ | ------ | ------------------- |
| FIN-001 | Gross margin per item    | Analytics | ✅     | Low    | Low    | Inventory cost      |
| FIN-002 | Gross margin by category | Analytics | ✅     | Low    | Low    | Calculations        |
| FIN-003 | Food cost %              | Analytics | ✅     | Medium | Low    | Inventory, sales    |
| FIN-004 | Waste analysis           | Analytics | ✅     | Low    | Low    | Waste tracking      |
| FIN-005 | Labor efficiency         | Analytics | ✅     | Medium | Low    | Payroll integration |
| FIN-006 | Table turnover           | Analytics | ✅     | Low    | Low    | Order timing        |
| FIN-007 | Customer repeat rate     | Analytics | ✅     | Low    | Low    | Customer data       |
| FIN-008 | Customer acquisition     | Analytics | ✅     | Low    | Low    | Customer data       |
| FIN-009 | Average order value      | Analytics | ✅     | Low    | Low    | Calculations        |
| FIN-010 | Peak vs. off-peak        | Analytics | ✅     | Low    | Low    | Time series         |
| FIN-011 | Discount impact          | Analytics | ✅     | Low    | Low    | Transactions        |
| FIN-012 | Profitability dashboard  | UI        | ✅     | Medium | Low    | Reporting           |
| FIN-013 | Variance analysis        | Analytics | ✅     | Medium | Medium | Budgets             |
| FIN-014 | Trend analysis           | Analytics | ✅     | Low    | Low    | Time series         |

**Estimated Effort:** 80-100 hours  
**Timeline:** 2-3 weeks post-MVP

---

### 9. MENU & PRICING (Phase 1 Priority)

| Req ID   | Requirement              | Type       | Phase1 | Effort | Risk   | Dependencies           |
| -------- | ------------------------ | ---------- | ------ | ------ | ------ | ---------------------- |
| MENU-001 | Dynamic pricing          | Core       | ✅     | Medium | Medium | Rule engine            |
| MENU-002 | Discount rules           | Core       | ✅     | Medium | Low    | Logic                  |
| MENU-003 | Combo rules              | Core       | ✅     | High   | Medium | Complex logic          |
| MENU-004 | Regional pricing         | Core       | ✅     | Low    | Low    | Per-franchise override |
| MENU-005 | Seasonal items           | Core       | ✅     | Low    | Low    | Date-based             |
| MENU-006 | Item availability        | Core       | ✅     | Low    | Low    | Visibility toggle      |
| MENU-007 | Ingredient price updates | Automation | ⚠️     | Low    | Low    | Recipe cost            |
| MENU-008 | Promotional items        | Tagging    | ✅     | Low    | Low    | UI flag                |
| MENU-009 | Menu history             | Audit      | ✅     | Low    | Low    | Versioning             |
| MENU-010 | Menu approval            | Workflow   | ⚠️     | Low    | Low    | Change management      |
| MENU-011 | Menu rollout             | Operations | ✅     | Low    | Low    | Scheduling             |
| MENU-012 | Category grouping        | UI         | ✅     | Low    | Low    | Hierarchy              |
| MENU-013 | Variant support          | Core       | ✅     | Medium | Low    | Pricing per variant    |
| MENU-014 | Allergen info            | Safety     | ✅     | Low    | Low    | Master data            |

**Estimated Effort:** 90-120 hours  
**Timeline:** 3-4 weeks post-MVP

---

### 10. CUSTOMER DATA & LOYALTY (Phase 1)

| Req ID   | Requirement         | Type          | Phase1 | Effort | Risk   | Dependencies       |
| -------- | ------------------- | ------------- | ------ | ------ | ------ | ------------------ |
| CUST-001 | Data capture        | UI            | ✅     | Low    | Low    | Phone/email fields |
| CUST-002 | Phone lookup        | Core          | ✅     | Low    | Low    | DB index           |
| CUST-003 | Preferences         | Configuration | ✅     | Low    | Low    | Tags               |
| CUST-004 | Visit tracking      | Analytics     | ✅     | Low    | Low    | Logging            |
| CUST-005 | Repeat ID           | UI            | ✅     | Low    | Low    | Calculation        |
| CUST-006 | At-risk alert       | Monitoring    | ✅     | Low    | Low    | Threshold          |
| CUST-007 | Loyalty points      | Core          | ✅     | Medium | Low    | Point ledger       |
| CUST-008 | Loyalty redemption  | Core          | ✅     | Medium | Medium | Point deduction    |
| CUST-009 | Referral tracking   | Analytics     | ⚠️     | Low    | Low    | Source field       |
| CUST-010 | Customer segment    | Analytics     | ✅     | Low    | Low    | Calculation        |
| CUST-011 | Personalized offers | Marketing     | ⚠️     | Low    | Low    | Segmentation       |
| CUST-012 | Birthday offers     | Marketing     | ⚠️     | Low    | Low    | DOB capture        |
| CUST-013 | Feedback            | Analytics     | ⚠️     | Low    | Low    | Survey form        |
| CUST-014 | Privacy compliance  | Compliance    | ✅     | Low    | Low    | Deletion API       |

**Estimated Effort:** 70-90 hours  
**Timeline:** 2-3 weeks post-MVP

---

### 11. STAFF MONITORING (Phase 1)

| Req ID    | Requirement           | Type           | Phase1 | Effort | Risk | Dependencies     |
| --------- | --------------------- | -------------- | ------ | ------ | ---- | ---------------- |
| LABOR-001 | Shift management      | Core           | ✅     | Low    | Low  | Scheduling       |
| LABOR-002 | Attendance tracking   | Core           | ✅     | Low    | Low  | Login/logout     |
| LABOR-003 | Overtime tracking     | Finance        | ✅     | Low    | Low  | Time calculation |
| LABOR-004 | Staff performance     | Analytics      | ✅     | Medium | Low  | Billing metrics  |
| LABOR-005 | Productivity metrics  | Analytics      | ✅     | Low    | Low  | Calculations     |
| LABOR-006 | Quality metrics       | Analytics      | ⚠️     | Medium | Low  | Error tracking   |
| LABOR-007 | Cash variance         | Audit          | ✅     | Low    | Low  | Drawer tracking  |
| LABOR-008 | Audit trail           | Security       | ✅     | Low    | Low  | Logging          |
| LABOR-009 | Payroll export        | Integration    | ✅     | Low    | Low  | CSV/API          |
| LABOR-010 | Labor cost %          | Analytics      | ✅     | Low    | Low  | Calculations     |
| LABOR-011 | Schedule optimization | AI/Forecasting | ⚠️     | High   | High | ML model         |
| LABOR-012 | Training tracking     | HR             | ⚠️     | Low    | Low  | Certificates     |

**Estimated Effort:** 60-80 hours  
**Timeline:** 2-3 weeks post-MVP

---

### 12. TABLE MANAGEMENT (Phase 2)

| Req ID    | Requirement            | Type          | Phase2 | Effort | Risk   | Dependencies         |
| --------- | ---------------------- | ------------- | ------ | ------ | ------ | -------------------- |
| TABLE-001 | Reservations           | Core          | ✅     | Medium | Low    | Booking system       |
| TABLE-002 | Overbooking prevention | Logic         | ✅     | Low    | Low    | Validation           |
| TABLE-003 | Reservation reminders  | Notification  | ✅     | Low    | Low    | SMS/Email            |
| TABLE-004 | Guest flexibility      | Logic         | ✅     | Low    | Low    | Threshold            |
| TABLE-005 | Table merging          | Core          | ✅     | High   | Medium | Complex logic        |
| TABLE-006 | Service time tracking  | Monitoring    | ✅     | Low    | Low    | Timer                |
| TABLE-007 | Turnover analytics     | Analytics     | ✅     | Low    | Low    | Calculations         |
| TABLE-008 | Waitlist               | Core          | ✅     | Medium | Low    | Queue management     |
| TABLE-009 | VIP handling           | Configuration | ⚠️     | Low    | Low    | Tagging              |
| TABLE-010 | Occupancy display      | UI            | ✅     | Low    | Low    | Status visualization |

**Estimated Effort:** 60-80 hours  
**Timeline:** Phase 2 (after Phase 1 complete)

---

### 13. DATA MIGRATION

| Req ID  | Requirement        | Type       | Effort | Risk   | Timing   |
| ------- | ------------------ | ---------- | ------ | ------ | -------- |
| MIG-001 | Data inventory     | Process    | Low    | Low    | Week 1   |
| MIG-002 | Data validation    | QA         | Medium | Medium | Week 2-3 |
| MIG-003 | Data cleansing     | Process    | High   | High   | Week 3-4 |
| MIG-004 | Migration plan     | Process    | Low    | Low    | Week 4   |
| MIG-005 | Test migration     | QA         | Medium | Medium | Week 5   |
| MIG-006 | Parallel run       | Operations | High   | High   | Week 6-7 |
| MIG-007 | Cutover plan       | Operations | Low    | Low    | Week 7   |
| MIG-008 | Reconciliation     | Audit      | High   | High   | Week 8   |
| MIG-009 | User training      | Operations | High   | Medium | Week 6-8 |
| MIG-010 | Fallback procedure | Operations | Low    | Low    | Week 5   |
| MIG-011 | Audit trail        | Compliance | Low    | Low    | Week 1   |
| MIG-012 | Archive legacy     | Operations | Low    | Low    | Week 8+  |

**Total Effort:** 100-150 hours (concurrent with final development)  
**Timeline:** 8 weeks, parallel to development  
**Risk:** HIGH (data quality issues common)

---

### 14. QR ORDERING & DELIVERY (Phase 2)

| Req ID | Requirement        | Type        | Phase2 | Effort | Risk   | Dependencies       |
| ------ | ------------------ | ----------- | ------ | ------ | ------ | ------------------ |
| QR-001 | QR code generation | Core        | ✅     | Low    | Low    | QR library         |
| QR-002 | Mobile order form  | UI          | ✅     | High   | Medium | Responsive design  |
| QR-003 | Order integration  | Core        | ✅     | High   | High   | Kitchen sync       |
| QR-004 | Delivery address   | Capture     | ✅     | Low    | Low    | Address validation |
| QR-005 | Real-time status   | Core        | ✅     | High   | Medium | WebSocket          |
| QR-006 | Online payment     | Integration | ✅     | Medium | Medium | Payment gateway    |
| QR-007 | ETA calculation    | Analytics   | ✅     | Medium | Medium | Prep time model    |
| QR-008 | Driver assignment  | Core        | ✅     | High   | High   | Route optimization |
| QR-009 | Driver app         | Mobile      | ✅     | High   | High   | Mobile development |
| QR-010 | Delivery tracking  | Integration | ✅     | High   | High   | GPS, Maps API      |
| QR-011 | Order aggregation  | Logic       | ✅     | Medium | Medium | Scheduling         |
| QR-012 | Delivery analytics | Analytics   | ✅     | Low    | Low    | Reporting          |

**Estimated Effort:** 200-300 hours  
**Timeline:** 6-8 weeks post-Phase 1  
**Risk:** CRITICAL (entirely new workflow, team may not have mobile expertise)

---

## Summary Statistics

### By Phase

| Phase             | Total Requirements | MVP Features | Effort (Hours) | Timeline             |
| ----------------- | ------------------ | ------------ | -------------- | -------------------- |
| **MVP (Phase 0)** | 95                 | 70           | 800-1000       | 10-12 weeks          |
| **Phase 1**       | 80                 | -            | 300-400        | 4-6 weeks            |
| **Phase 2**       | 22                 | -            | 200-300        | 6-8 weeks            |
| **Migration**     | 12                 | -            | 100-150        | 8 weeks (concurrent) |
| **TOTAL**         | **209**            | -            | **1400-1850**  | **6-7 months**       |

### By Risk Level

| Risk        | Count | MVP | Phase1 | Phase2 |
| ----------- | ----- | --- | ------ | ------ |
| 🔴 CRITICAL | 28    | 20  | 5      | 3      |
| 🔴 HIGH     | 42    | 25  | 12     | 5      |
| 🟡 MEDIUM   | 89    | 20  | 45     | 24     |
| 🟢 LOW      | 50    | 5   | 18     | 27     |

### By Type

| Category            | MVP    | Phase1 | Phase2 | Total   |
| ------------------- | ------ | ------ | ------ | ------- |
| Core Features       | 28     | 12     | 8      | 48      |
| Configuration       | 8      | 6      | 2      | 16      |
| UI/UX               | 15     | 10     | 8      | 33      |
| Integration         | 6      | 4      | 3      | 13      |
| Analytics           | 5      | 30     | 8      | 43      |
| Compliance/Security | 5      | 2      | 1      | 8       |
| Process/Operations  | 3      | 16     | 2      | 21      |
| Testing/QA          | 8      | 5      | 2      | 15      |
| Infrastructure      | 8      | 5      | 2      | 15      |
| Audit/Logging       | 4      | 4      | 1      | 9       |
| **TOTAL**           | **90** | **94** | **37** | **209** |

---

## Critical Path Analysis

### Must Be Resolved Before Development Starts

```
Decision Tree:

1. Scope Confirmation (Week 1)
   ├─ Approve MVP feature set
   ├─ Confirm Phase 1/2 roadmap
   └─ Sign off on exclusions

2. Architecture Decisions (Week 1-2)
   ├─ Multi-tenancy: YES (mandatory)
   ├─ Offline mode: YES (critical)
   ├─ Database: PostgreSQL + cloud
   ├─ Payment gateway: Razorpay
   └─ KDS: Digital screen

3. Risk Mitigation (Week 2)
   ├─ Data migration plan
   ├─ Parallel run strategy
   ├─ Training curriculum
   └─ Rollback procedure

4. Technical Readiness (Week 2-3)
   ├─ Dev environment setup
   ├─ CI/CD pipeline
   ├─ Testing infrastructure
   └─ API design review
```

---

## Effort Estimation Confidence

| Component               | Effort Range     | Confidence | Notes                                            |
| ----------------------- | ---------------- | ---------- | ------------------------------------------------ |
| MVP Core (POS, Billing) | 200-250 hrs      | 90%        | Well-understood, similar systems exist           |
| Payment Integration     | 100-150 hrs      | 80%        | Depends on gateway complexity                    |
| Offline Mode            | 80-120 hrs       | 70%        | Sync complexity; conflict resolution TBD         |
| Multi-Tenancy           | 120-180 hrs      | 60%        | Depends on isolation level desired               |
| Kitchen Display         | 60-100 hrs       | 85%        | Hardware + software, straightforward             |
| Inventory + BOM         | 120-160 hrs      | 75%        | Business logic complex; depends on feature depth |
| Testing + QA            | 150-200 hrs      | 70%        | Load testing critical; unknown variance          |
| Data Migration          | 100-150 hrs      | 50%        | Highly dependent on data quality                 |
| **TOTAL MVP**           | **900-1200 hrs** | **75%**    | **Recommend adding 20% buffer**                  |

---

## Red Flags for Effort Estimation

🚩 If any of these are true, **increase effort estimate by 30%:**

- Data migration unplanned or scope unknown
- Payment gateway chosen but not tested with Razorpay
- No infrastructure/DevOps support (you need it)
- Team never done offline sync before
- Multi-tenancy architecture not yet designed
- Load testing tools not yet available
- Parallel run with old system not planned

---

**Document Status:** Ready for development planning  
**Next Step:** Use this matrix to create detailed task breakdown in project management tool  
**Owner:** Technical Lead (coordinate with Business Analyst)  
**Last Updated:** 30 June 2026
