# Architecture Overview

## Vireya Restaurant Management System Architecture

**Version:** 1.0
**Date:** 30 June 2026
**Status:** Draft architecture for stakeholder and delivery review

---

## 1. Purpose

This architecture document defines the long-term technical foundation for the Vireya Restaurant Management System.
It is designed to be stable, extensible, and resilient for franchise operations, offline branch workflows, and rush-hour performance.

This architecture is explicitly aligned with the PRD and gap analysis, with the following mandatory anchors:

- Multi-tenancy for franchise and branch isolation
- Offline POS resilience and safe sync
- Audit-ready payment and order workflows
- Inventory and perishability control
- Kitchen coordination and order edge-case handling
- Scalable, cloud-hosted backend with branch-local caching

---

## 2. Architectural Principles

### 2.1 Stability over novelty

- Favor proven, boring technology.
- Use a modular monolith for MVP, with clear boundaries between domains.
- Defer microservices until scaling requirements are real.

### 2.2 Data isolation and auditability

- Enforce tenant isolation at the database and API layers.
- Preserve audit trails for all financial, order, inventory, and configuration changes.
- Use immutable ledgers for payments, inventory events, and order events where practical.

### 2.3 Offline-first branch operations

- Branch POS terminals must continue taking orders when cloud connectivity is unavailable.
- Store local state in a secure branch cache.
- Queue changes and replay them reliably once connectivity returns.

### 2.4 Domain modularity

- Separate domain responsibilities cleanly: POS, Orders, Inventory, Kitchen, Payments, Reporting.
- Share only well-defined contracts between domains.
- Use common infrastructure services for identity, audit, and integration.

### 2.5 Operational visibility

- Monitor sync health, branch connectivity, order throughput, inventory variance, and security events.
- Build dashboards for branch and corporate stakeholders.

---

## 3. System Context and Components

### 3.1 Key system components

1. Branch POS / Terminal
2. Branch Local Store + Sync Engine
3. Central Cloud Backend
4. API Gateway and Backend Services
5. Kitchen Display System (KDS)
6. Integration Services
7. Reporting and Analytics
8. Identity, Security, and Audit

### 3.2 Component summary

#### Branch POS / Terminal

- Browser-based or lightweight desktop app used by cashiers and managers.
- Provides menu display, order entry, bill presentation, payment capture, and offline mode indicator.
- Caches the latest menu, pricing, inventory availability, and configuration.
- Writes order and payment events to the local store when offline.

#### Branch Local Store + Sync Engine

- Local branch cache: SQLite or equivalent embedded database.
- Stores a subset of branch data required for offline operation:
  - active menu, pricing, branch config
  - inventory balance and batch expiry metadata
  - pending orders and KOT states
  - local transaction queue and sync metadata
- Sync Engine responsibilities:
  - compress and batch local events
  - reconcile branch state with cloud state
  - apply deterministic conflict resolution rules
  - emit sync status for staff and managers

#### Central Cloud Backend

- Cloud-hosted services supporting all branches and franchise-level operations.
- Manages authoritative data for orders, inventory, menus, reporting, users, and audit logs.
- Exposes secure REST/GraphQL APIs for branch terminals, mobile apps, and admin portals.

#### API Gateway and Backend Services

- API Gateway handles routing, authentication, rate limiting, caching, and telemetry.
- Backend service layers implement business domains:
  - Orders and Billing
  - Inventory and Procurement
  - Kitchen Coordination
  - Payments and Reconciliation
  - Tenancy and Permissions
  - Reporting and Analytics

#### Kitchen Display System (KDS)

- Digital screen or tablet in the kitchen.
- Receives prioritized order tickets from the order service.
- Tracks item-level status: pending, cooking, ready, served, rejected.
- Supports partial fulfillment and order holds.

#### Integration Services

- Payment provider adapter (Razorpay / PayU / Cashfree).
- Optional third-party inventory or accounting connectors.
- Notification and messaging adapters for branch alerts.

#### Reporting and Analytics

- Batch and near-real-time reporting service.
- Supports profitability metrics, waste tracking, cash reconciliation, and franchise rollups.
- Feeds dashboards and EOD reports.

#### Identity, Security, and Audit

- Central identity service for authentication and RBAC.
- Tenant-aware authorization enforced in API middleware.
- Audit service captures every state change and sensitive action.

---

## 4. Multi-Tenancy Architecture

### 4.1 Primary approach: Schema-based multi-tenancy

- Use a single cloud PostgreSQL instance.
- Create a separate schema per franchisee/tenant.
- Tenant schema includes branch-specific entities and data partitioning.
- Keep shared reference data in a common schema.
- Use PostgreSQL Row-Level Security (RLS) and tenant context enforcement.

### 4.2 Why schema-based tenancy

- Strong isolation while preserving operational simplicity.
- Easier to implement than separate databases for MVP.
- Supports tenant-specific overrides (pricing, menu availability, reports).
- Easier data management for branch onboarding and backup.

### 4.3 Tenant context flow

- Every request includes tenant identity from authentication token or branch binding.
- API middleware resolves tenant context and binds it to DB session.
- Queries use schema-qualified tables or RLS policies based on tenant id.
- Tenant-aware authorization ensures users access only permitted branches.

### 4.4 Branch-level isolation

- Branches belong to a franchise tenant.
- Branch permission model restricts data by branch, role, and scope.
- Users can have cross-branch visibility only when explicitly allowed.

---

## 5. Offline Sync Architecture

### 5.1 Branch offline mode behavior

- Branch terminal stays online if possible, but can continue operating when disconnected.
- Local store supports:
  - order creation and modification
  - item status changes for kitchen orders
  - payment capture metadata for cash/UPI settlement
  - inventory reservation and deduction events

### 5.2 Sync design

- Use an event queue for branch-local changes.
- Batch upload when connectivity returns.
- Prefer append-only event flow for branch changes.
- Maintain a sync state machine per branch.

### 5.3 Conflict resolution rules

- Configuration data: cloud wins on reconnect.
- Order and inventory events: branch wins for locally committed orders, but cloud validates and may reject invalid states.
- If the same inventory item is updated in parallel, resolve by:
  - applying timestamped ledger events in deterministic order
  - preserving both events in audit logs
  - alerting operations for reconciliation if a business rule conflict arises
- If menu changes arrive while offline, continue using cached pricing until next sync.

### 5.4 Offline integrity guarantees

- Ensure every locally accepted transaction is durable before acknowledgement.
- Preserve ordered event sequence when syncing.
- Do not lose pending orders during branch restarts.
- Provide staff with clear offline status and sync recovery progress.

---

## 6. Data Architecture

### 6.1 Core data domains

- Tenants and Branches
- Users and Roles
- Menu Catalog
- Orders and KOTs
- Payments and Settlements
- Inventory, Batches, and BOMs
- Waste and Reconciliation
- Audit Logs
- Reports and Metrics

### 6.2 Recommended data model shape

#### Tenant / Branch

- Tenant: franchise group identity
- Branch: store location, region, pricing overrides

#### Menu Catalog

- MenuItem: base item definition
- MenuPrice: tenant/branch override
- MenuAvailability: branch- or time-based visibility
- Recipe/BOM: ingredient quantities per menu item

#### Order / Kitchen

- Order: source, channel, table, waiter, status
- OrderItem: item-level status, quantity, modifiers, substitutions
- KOTTicket: kitchen tracking data and priority
- OrderEvent: immutable event ledger for changes

#### Inventory

- InventoryBatch: item, quantity, expiry, batch cost, location
- InventoryTransaction: inbound, consumption, waste, adjustment
- StockReservation: ingredients reserved for pending orders
- WasteEntry: type, reason, quantity, cost

#### Payments

- PaymentTransaction: amount, method, status, reference
- SettlementBatch: cash count, UPI reconciliation, variance
- RefundEvent: approved reversal, reason, reviewer

#### Audit

- AuditEntry: actor, action, entity, before/after snapshot, timestamp
- AccessLog: login, session, source IP, device

### 6.3 Data storage choices

- Primary cloud storage: PostgreSQL
- Local branch store: SQLite
- Caching layer: Redis for menu/session caching and rate limiting
- Analytics store: same PostgreSQL with reporting schema or separate analytics schema

---

## 7. Service and Integration Patterns

### 7.1 Recommended service architecture

- Modular monolith for MVP with domain modules:
  - Tenancy / Identity
  - POS / Orders
  - Inventory / Procurement
  - Kitchen / KDS
  - Payments / Settlement
  - Reports / Analytics
  - Audit / Logging
- Shared middleware for tenant context, RBAC, validation, and audit.

### 7.2 Integration patterns

- Payment integration via adapter pattern.
- External services are called through explicit integration modules.
- Keep payment gateway dependency isolated behind a service interface.
- Use event-based notifications for branch alerts and KDS updates.

### 7.3 API surface

- Use REST APIs with JSON payloads for backend-to-branch traffic.
- If the team prefers, use GraphQL for admin portals and reporting clients.
- Expose sync APIs for branch local store.
- Keep branch sync API thin and deterministic.

### 7.4 Branch sync API responsibilities

- Authenticate branch token and tenant context
- Ingest branch event batches
- Return conflict / validation responses
- Provide latest configuration and menu deltas
- Provide inventory availability changes
- Provide order status updates and KOT acknowledgements

---

## 8. Security and Compliance

### 8.1 Identity and access control

- Central authentication service with JWT tokens.
- RBAC enforced in API middleware.
- Permission model must include tenant-level, branch-level, and action-level control.
- Soft delete and retain deleted records for audit.

### 8.2 Data protection

- TLS for all network communication.
- Encrypt sensitive data at rest in cloud storage.
- Mask or redact PII in logs and exports.
- Secure local branch store with file-level protections.

### 8.3 Audit and logging

- Audit all financial, order, inventory, and configuration changes.
- Log login/access events with source details.
- Log sync failures and branch reconciliation anomalies.
- Retain audit logs for the required compliance period.

### 8.4 Compliance priorities

- PCI scope for payment-related operations.
- GST and local tax compliance for invoices and reports.
- Franchise-specific reporting for royalty and revenue partitioning.
- Data retention and export controls as required by local law.

---

## 9. Nonfunctional Requirements

### 9.1 Performance

- Support 100+ branch orders per hour per branch in MVP.
- End-to-end billing response time < 2s, p95 < 3s.
- KDS updates must appear within 1-2 seconds.

### 9.2 Availability

- Target branch-level online availability of 99.9% for cloud services.
- Branch terminals must continue operating during cloud outage.
- Cloud deployment should include redundancy across availability zones.

### 9.3 Scalability

- Scale vertically first, then horizontally for API services.
- Use read replicas for reporting and analytics workloads.
- Use Redis cache to reduce repeated menu and permission lookups.

### 9.4 Operability

- Provide branch sync health dashboards.
- Provide alerting for failed sync, inventory variance, and payment exceptions.
- Document runbooks for cutover, rollback, and branch recovery.

---

## 10. Long-Term Stability Guidance

### 10.1 Keep business logic explicit

- Avoid hidden behavior in UI-only flows.
- Put pricing, menu override, and inventory deduction rules in backend services.

### 10.2 Preserve version compatibility

- Version branch sync contracts.
- Allow old branch clients to continue operating during gradual rollout.

### 10.3 Decouple data reads from writes

- Use separate read models for billing and reporting where needed.
- Keep writes strongly consistent for order, payment, and inventory transactions.

### 10.4 Avoid premature microservices

- Adopt a modular monolith first.
- Split into services only when a component has independent scaling or deployment needs.

### 10.5 Build for observability

- Instrument service latency, sync duration, conflict rates, and audit volume.
- Log business events, not just technical errors.

---

## 11. Recommended Technology Stack

### 11.1 Core platform

- Backend: Node.js / .NET / Java / Python (choose team expertise; prefer stable, well-supported stack)
- Database: PostgreSQL
- Local branch DB: SQLite
- Cache: Redis
- API gateway: NGINX / AWS API Gateway / Azure API Management

### 11.2 Branch runtime

- Web-based POS client or Electron wrapper
- KDS client: browser-based digital display
- Local sync service bundled with terminal app

### 11.3 Integrations

- Payment gateway: Razorpay / PayU / Cashfree
- Optional messaging: SMTP/SMS provider

---

## 12. Phasing and Roadmap Alignment

### MVP focus

- Multi-tenancy groundwork
- Core POS billing and kitchen workflow
- Offline branch sync and local queue
- Inventory batch expiry and BOM deduction
- Payment audit and cash reconciliation
- Security, RBAC, and audit logging
- Rush-hour performance validation

### Phase 1 focus

- Profitability metrics and dashboards
- Advanced menu pricing rules
- Loyalty and customer data tracking
- Staff monitoring and labor analytics

### Phase 2 focus

- QR ordering and delivery integration
- Multi-brand franchise support
- Advanced feature rollout control

---

## 13. Next Steps

- Validate architecture with stakeholders and dev team.
- Create a detailed data model and schema diagram.
- Define API contracts for branch sync and order workflows.
- Prototype offline sync and conflict resolution.
- Build a proof-of-concept branch POS + local store sync path.
- Review budget and timeline against the architecture assumptions.
