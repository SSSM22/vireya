# Implementation Readiness Checklist

## AFC Restaurant Management System

**Version:** 1.0  
**Date:** 30 June 2026  
**Purpose:** Decision framework for MVP scope, phasing, and risk mitigation

---

## Critical Decision Points

### 1. MVP Scope Confirmation

**QUESTION:** Which 14 gaps MUST be in MVP vs. Phase 1 vs. Phase 2?

**Current Recommendation:**

| Gap                     | MVP               | Phase 1 | Phase 2 | Rationale                                                               |
| ----------------------- | ----------------- | ------- | ------- | ----------------------------------------------------------------------- |
| Offline Resilience      | ✅                |         |         | Revenue loss if system unavailable during peak hours                    |
| Payment & Settlement    | ✅                |         |         | Non-negotiable: trust, audit, regulatory compliance                     |
| Inventory Perishability | ✅                |         |         | Food safety + cost control; must be Day 1                               |
| Order Flow              | ✅                |         |         | Kitchen rejection + modification essential; QA nightmare if post-MVP    |
| Rush Hour Performance   | ✅                |         |         | SLA must be defined + tested in MVP; fixing later = rework              |
| Security & Compliance   | ✅                |         |         | Regulatory + audit trail; non-negotiable                                |
| Franchise Model         | ✅                |         |         | Multi-tenancy must be in architecture Day 1; retrofitting is impossible |
| Menu & Pricing          | ✅                |         |         | Dynamic pricing + regional override needed for franchise model          |
| Profitability Metrics   |                   | ✅      |         | Important but not blocking; added after launch                          |
| Customer Data           |                   | ✅      |         | Loyalty/retention; Phase 1 feature                                      |
| Staff Monitoring        |                   | ✅      |         | Labor analytics; Phase 1 feature                                        |
| Table Management        |                   | ✅      |         | Reservations Phase 2; basic seating Phase 1                             |
| Data Migration          | Concurrent        |         |         | Parallel to dev; testing during Phase 1                                 |
| QR/Delivery             | Architecture only |         | ✅      | Design for it NOW; implement Phase 2                                    |

**Decision Needed:** Do you agree with this phasing?

---

### 2. Multi-Tenancy vs. Single-Tenant

**QUESTION:** Build as SaaS multi-tenant from Day 1, or single-tenant with migration later?

**Implication:**

| Approach                     | MVP Cost    | Phase 2 Cost | Risk | Recommendation                         |
| ---------------------------- | ----------- | ------------ | ---- | -------------------------------------- |
| **Multi-tenant from Day 1**  | +30% effort | Minimal      | Low  | ✅ RECOMMENDED for franchise model     |
| **Single-tenant (AFC only)** | Standard    | +200% rework | High | ❌ Not viable if 25 franchises planned |

**Decision Needed:** Commit to multi-tenancy architecture from MVP?

---

### 3. Offline Fallback Strategy

**QUESTION:** What happens when cloud is unreachable?

**Option A: Offline Mode (Recommended)**

- POS continues billing on local DB
- Transactions queued, sync when online
- Effort: +15% MVP cost
- Risk: Low (proven pattern in retail)

**Option B: Manual Fallback**

- System locks when offline
- Cashiers use paper bills + manual entry next day
- Effort: +5% (just documentation)
- Risk: High (revenue loss during outage, data entry errors)

**Option C: Hybrid**

- Offline for POS; cloud-only for inventory (separate system)
- Effort: +25% MVP cost
- Risk: Medium (data sync complexity)

**Decision Needed:** Which offline strategy?

---

### 4. Payment Gateway Selection

**QUESTION:** Which payment provider? (Impacts data security, compliance, fees)

**Candidate Providers:**

| Provider     | Supported Modes             | GST Support | Compliance    | Fee           | Notes                             |
| ------------ | --------------------------- | ----------- | ------------- | ------------- | --------------------------------- |
| **Razorpay** | UPI, Card, Wallet, PayLater | ✅          | PCI-DSS, ISO  | 1.5-2%        | Recommended; strong India support |
| **PayU**     | UPI, Card, Wallet           | ✅          | PCI-DSS       | 1.7-2.2%      | Alternative                       |
| **Cashfree** | UPI, Card, Wallet           | ✅          | PCI-DSS       | 1.5-2.5%      | Alternative                       |
| **Stripe**   | Card, Wallet (limited UPI)  | ⚠️ Partial  | PCI-DSS, GDPR | 2.2% + ₹2/txn | International; limited India UPI  |

**Decision Needed:** Which provider?

---

### 5. Database Architecture

**QUESTION:** Monolithic or microservices? Cloud or on-premise?

**Option A: Monolithic + Cloud (Recommended)**

- Single PostgreSQL database
- Cloud hosting: AWS RDS / GCP Cloud SQL
- Multi-tenancy: schema-based isolation (separate schema per franchisee)
- Effort: Standard
- Risk: Low (proven pattern)
- Scaling: Vertical first, then read replicas

**Option B: Microservices**

- Separate services: POS, Inventory, Reporting, Kitchen
- Database per service
- Message queue: RabbitMQ/Kafka for async
- Effort: +50%
- Risk: High (complexity, debugging harder)
- Recommendation: ❌ Overkill for MVP; consider Phase 2 if scaling issues

**Decision Needed:** Monolithic or microservices?

---

### 6. Inventory: Batch Expiry Tracking

**QUESTION:** Simple (FIFO only) or advanced (batch-level expiry)?

**Option A: Simple**

- First-in-first-out rotation
- Effort: Low
- Risk: Medium (potential spoilage if not rotated properly)

**Option B: Batch Expiry (Recommended)**

- Each purchase: batch ID + expiry date
- System alerts when approaching expiry
- Effort: +10%
- Risk: Low (proactive waste prevention)
- Business value: Prevents food safety issues; reduces waste

**Decision Needed:** Simple or batch expiry?

---

### 7. Role-Based Access Control (RBAC)

**QUESTION:** How many roles in MVP?

**Option A: Minimal (5 Roles)**

- Owner (all access)
- Branch Manager (branch-only access)
- Cashier (billing only)
- Kitchen (KOT only)
- Inventory Manager (inventory only)
- Effort: Standard
- Risk: Low

**Option B: Detailed (10+ Roles)**

- Add: Assistant Manager, Senior Cashier, Junior Kitchen, Delivery, Accountant
- Effort: +20%
- Risk: Over-engineering; customize in Phase 1

**Decision Needed:** Minimal (5) or detailed (10+)?

---

### 8. Kitchen Display System (KDS)

**QUESTION:** Printed tickets vs. digital screen?

**Option A: Printed KOT Tickets (Traditional)**

- Print on thermal printer at POS
- Kitchen hangs tickets
- Effort: Low
- Cost: ₹5,000 printer
- Risk: Medium (paper lost, hard to prioritize)

**Option B: Digital KDS Screen (Recommended)**

- Large touchscreen at kitchen
- Color-coded by priority (dine-in = red, takeaway = yellow)
- Orders auto-remove when marked ready
- Effort: Standard
- Cost: ₹25,000-50,000 for tablet/screen
- Risk: Low (modern, efficient)
- Business value: Faster service, reduce stale orders

**Decision Needed:** Printed or digital KDS?

---

### 9. Launch Timeline

**QUESTION:** What's the realistic timeline?

**Estimated Phases:**

| Phase                                | Duration   | Deliverables                                 | Gate                 |
| ------------------------------------ | ---------- | -------------------------------------------- | -------------------- |
| **PRD + Design**                     | 2 weeks    | Requirements, UX mockups, DB schema          | Sign-off on scope    |
| **MVP Development**                  | 8-10 weeks | Core features (POS, Inventory, KOT, Billing) | Code review, testing |
| **QA + Testing**                     | 3 weeks    | Functional, performance, security testing    | Pass SLA tests       |
| **Training + Migration**             | 2 weeks    | Staff training, data migration, parallel run | No data loss         |
| **Pilot Launch**                     | 1 week     | Deploy to 1 branch; monitor, fix bugs        | Monitor metrics      |
| **Full Rollout**                     | 1 week     | Deploy to all 6 branches                     | Success criteria met |
| **Phase 1 (Profitability, Loyalty)** | 4-6 weeks  | Advanced reporting, customer features        | New capabilities     |
| **Phase 2 (QR + Delivery)**          | 6-8 weeks  | QR ordering, delivery tracking, driver app   | Expansion ready      |

**Total Timeline to Franchise-Ready:** 6-7 months

**Decision Needed:** Is this timeline acceptable?

---

### 10. Budget & Resource Estimation

**QUESTION:** What's the budget for MVP?

**Rough Estimate (assuming 4-person dev team, India-based):**

| Item                        | Cost         | Notes                            |
| --------------------------- | ------------ | -------------------------------- |
| **Development (MVP)**       | ₹25-35 L     | 8-10 weeks, 4 developers         |
| **QA + Testing**            | ₹5-7 L       | 3 weeks                          |
| **Infrastructure (Year 1)** | ₹3-5 L       | AWS RDS, EC2, hosting, backups   |
| **Payment Gateway Setup**   | ₹1-2 L       | Integration, testing, compliance |
| **KDS Hardware**            | ₹2-4 L       | Kitchen screens, POS terminals   |
| **Training + Cutover**      | ₹2-3 L       | Staff training, data migration   |
| **Contingency (15%)**       | ₹5-7 L       | Buffer for scope creep, issues   |
| **TOTAL MVP COST**          | **₹43-63 L** | (~$50-75k USD)                   |
| **Phase 1**                 | ₹10-15 L     | 4-6 weeks                        |
| **Phase 2**                 | ₹15-20 L     | 6-8 weeks                        |

**Decision Needed:** Budget available?

---

## Validation Checklist

Before proceeding to PRD, confirm:

### Requirements Clarity

- [ ] Business objectives: precise and measurable
- [ ] User roles: defined with explicit permissions
- [ ] SLAs: documented (billing time <2sec, uptime >99.9%)
- [ ] Success metrics: defined (billing time reduced 50%, waste <5%, etc.)

### Scope Confirmation

- [ ] MVP features: listed and agreed
- [ ] Out-of-scope: explicitly marked (e.g., loyalty, QR, delivery)
- [ ] Phase 1/2 features: planned and sequenced
- [ ] Architectural constraints: identified (multi-tenancy, offline, scalability)

### Risk Mitigation

- [ ] Offline strategy: decided
- [ ] Data migration plan: sketched
- [ ] Parallel run period: planned
- [ ] Rollback procedure: documented
- [ ] Training plan: drafted

### Technical Foundation

- [ ] Database architecture: selected (monolithic vs. microservices)
- [ ] Payment gateway: chosen
- [ ] Multi-tenancy approach: defined
- [ ] Security/compliance: mapped to requirements
- [ ] KDS strategy: decided

### Stakeholder Alignment

- [ ] Owner: reviewed gaps, approved phasing
- [ ] IT/Operations: confirmed infrastructure availability
- [ ] Finance: approved budget
- [ ] HR: aware of training timeline

---

## Red Flags (Stop & Re-Discuss If):

🚩 **"We need all 14 gaps in MVP"** → Unrealistic; phasing is necessary. Prioritize critical gaps.

🚩 **"We'll go single-tenant, migrate to multi-tenant later"** → Architectural nightmare. Go multi-tenant Day 1.

🚩 **"We'll figure out offline strategy in Phase 1"** → Not optional for QSR POS. Define now.

🚩 **"We don't need franchise-readiness in MVP"** → You do. Multi-tenancy architecture is foundational.

🚩 **"Budget is ₹15-20 L for MVP"** → Likely underestimated. Real: ₹43-63 L based on scope.

🚩 **"Timeline: 3 months to launch"** → Unrealistic. Real: 6-7 months with quality. 3-4 months if cutting corners (risky).

🚩 **"No stress testing for rush hour"** → Mandatory. Must prove system handles 100 orders/hour without degradation.

---

## Recommended Next Actions

### Immediate (This Week)

1. ✅ Review this checklist + gaps analysis with stakeholders
2. ✅ Confirm MVP scope (which 14 gaps are must-have?)
3. ✅ Approve phasing (Phase 0, 1, 2 schedule)
4. ✅ Decide on multi-tenancy commitment
5. ✅ Select payment gateway

### Short-term (Next 2 Weeks)

1. Create formal PRD translating gaps + requirements
2. Conduct technical architecture review with dev team
3. Finalize database schema design
4. Plan data migration (current Excel → system)
5. Schedule stakeholder sign-off

### Preparation (Weeks 3-4)

1. Develop UI/UX mockups based on requirements
2. Set up development environment (Git, CI/CD, test infra)
3. Create training materials and staff onboarding plan
4. Plan testing strategy (unit, integration, performance, UAT)
5. Draft cutover + rollback runbook

---

**Document Status:** Ready for stakeholder review  
**Next Review Date:** After stakeholder sign-off on scope  
**Owner:** Business Analyst (Mary)  
**Last Updated:** 30 June 2026
