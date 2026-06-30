---
project: vireya
date: 2026-06-30
stepsCompleted:
  - step-01-document-discovery
  - step-02-prd-analysis
  - step-03-epic-coverage-validation
  - step-04-ux-alignment
  - step-05-epic-quality-review
selected_documents:
  prd: docs/product-requirements-document.md
  architecture: docs/architecture.md
  ux: docs/ux-design.md
  epics_and_stories: _bmad-output/planning-artifacts/epics.md
---

# Implementation Readiness Assessment Report

**Date:** 2026-06-30
**Project:** vireya

## Document Discovery Summary

The following source documents were selected for the assessment from `docs/`.

### PRD

- `docs/product-requirements-document.md`

### Architecture

- `docs/architecture.md`

### UX Design

- `docs/ux-design.md`

### Epics & Stories

- No dedicated epics or stories document was found in `docs/`.

## Notes

- `_bmad-output/planning-artifacts/` was empty, so the assessment will use the source documents under `docs/`.
- No whole vs sharded duplicates were detected for the selected documents.
- If an epics/stories artifact exists elsewhere, please point me to it before I continue.

## Findings

- `docs/product-requirements-document.md` appears to be the primary PRD.
- `docs/architecture.md` is the architecture document.
- `docs/ux-design.md` is the UX design document.
- No explicit epic/story document was located in the standard `docs/` set.

## PRD Analysis

### Functional Requirements Extracted

FR1: The system must support QR-based table ordering and bill presentation for branch and franchise partners.
FR2: The system must integrate with existing payment methods rather than building new payment gateways.
FR3: The system must provide offline resilience and sync for order capture and kitchen coordination.
FR4: The system must support franchise-ready multi-tenancy with branch-level pricing, menu overrides, and revenue partitioning.
FR5: The system must provide inventory perishability and waste control, including expiry tracking and BOM-based stock deduction.
FR6: The system must handle order flow edge cases and kitchen coordination, including item-level status updates and order modifications.
FR7: The system must provide security, audit, and compliance features, including permission controls, audit trails, and soft delete history.
FR8: The system must deliver rush-hour performance under 100+ orders/hour peak load.
FR9: The system must provide centralized reporting for branch and corporate management.
FR10: The system must support offline mode with local transaction queueing and secure sync after reconnection.
FR11: The system must cache the latest daily menu and pricing on the POS terminal at branch startup.
FR12: The system must preserve zero transaction loss and audit trails for offline transactions.
FR13: The system must support cash reconciliation and refund workflows with manager approval above thresholds.
FR14: The system must provide BOM relationships between menu items and ingredients and auto-deduct ingredients when orders are placed.
FR15: The system must support status tracking for kitchen items: pending, cooking, ready, served, rejected.
FR16: The system must provide role-based access control at UI and API layers.
FR17: The system must log permission-sensitive actions for audit and compliance.
FR18: The system must store customer contact and visit preferences and support loyalty points and redemption flows.
FR19: The system must support table management and reservations as Phase 2 scope.
FR20: The system must support data migration planning, validation, cleansing, and parallel operation during cutover.
FR21: The system must provide franchise menu override support and regional variants with pricing rules.
FR22: The system must support audit-ready reports for tax and regulatory checks.

Total FRs: 22

### Non-Functional Requirements Extracted

NFR1: The system must reduce billing time by at least 50% during peak hours.
NFR2: The system must provide audit trail for order and bill changes while leveraging existing branch payment processes.
NFR3: The system must ensure reconnection and sync complete within 5 minutes of network restoration.
NFR4: The system must guarantee zero transaction loss and preserve offline audit trails.
NFR5: The system must use role-based access control with row-level security or tenant-scoped data filters.
NFR6: The system must log all permission-sensitive actions for audit and compliance.
NFR7: The system must support system stability under 100+ orders/hour peak load.
NFR8: The system must provide performance SLAs including end-to-end billing transaction latency under 2 seconds, p95 under 3 seconds.
NFR9: The system must encrypt PII at rest and enforce TLS in transit.
NFR10: The system must auto-logout after inactivity and support optional 2FA for high-privilege users.
NFR11: The system must preserve deleted records and record deletion metadata.
NFR12: The system must allow data deletion and mask PII for non-authorized users.
NFR13: The system must support batch reconciliation and flag >5% variance between physical and system stock counts.
NFR14: The system must generate daily settlement reports and compare cash vs system receipts.
NFR15: The system must provide audit-ready reports for tax and regulatory checks.
NFR16: The system must support schedule-based menu activation and delivery/reservation workflows in Phase 2.

Total NFRs: 16

### Additional Requirements

- Constraints and assumptions include using existing payment methods without building new payment gateways for MVP.
- Integration requirements include branch-local data sync, offline order status reconciliation, and kitchen order ticket integration.
- Business constraints include supporting franchise isolation, regional menu overrides, and royalty tracking while keeping the MVP focused on branch operations.
- Technical requirements include RBAC enforcement at UI/API layers, row-level security, audit logging, soft delete history, and offline transaction queueing.

### PRD Completeness Assessment

The PRD is comprehensive in describing functional scopes and real-world scenarios. It clearly defines the MVP foundation and Phase 2 extensions, but the requirements are presented largely as feature specifications rather than a compact FR/NFR list. The document is sufficient for traceability work, though it may require normalization into a more explicit requirements register for downstream implementation.

## Epic Coverage Validation

### Coverage Matrix

### Coverage Matrix

| FR Number | PRD Requirement                                                                                                                         | Epic Coverage                                                                     | Status          |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------- |
| FR1       | The system must support QR-based table ordering and bill presentation for branch and franchise partners.                                | Epic 1 - QR table ordering and bill presentation experience                       | ✓ Covered       |
| FR2       | The system must integrate with existing payment methods rather than building new payment gateways.                                      | Epic 1 - Existing payment method integration and cashier billing flows            | ✓ Covered       |
| FR3       | The system must provide offline resilience and sync for order capture and kitchen coordination.                                         | Epic 1 - Offline resilience and sync for order capture and kitchen coordination   | ✓ Covered       |
| FR4       | The system must support franchise-ready multi-tenancy with branch-level pricing, menu overrides, and revenue partitioning.              | Epic 4 - Branch and franchise pricing override and regional variants              | ✓ Covered       |
| FR5       | The system must provide inventory perishability and waste control, including expiry tracking and BOM-based stock deduction.             | Epic 3 - Inventory perishability, expiry tracking, and BOM-based stock deduction  | ✓ Covered       |
| FR6       | The system must handle order flow edge cases and kitchen coordination, including item-level status updates and order modifications.     | Epic 2 - Order flow edge cases and kitchen coordination                           | ✓ Covered       |
| FR7       | The system must provide security, audit, and compliance features, including permission controls, audit trails, and soft delete history. | Epic 4 - Security, audit logging, and compliance controls                         | ✓ Covered       |
| FR8       | The system must deliver rush-hour performance under 100+ orders/hour peak load.                                                         | Epic 1 - Rush-hour performance for checkout and order processing                  | ✓ Covered       |
| FR9       | The system must provide centralized reporting for branch and corporate management.                                                      | Epic 5 - Branch and corporate reporting, profitability, and operations visibility | ✓ Covered       |
| FR10      | The system must support offline mode with local transaction queueing and secure sync after reconnection.                                | Epic 1 - Offline mode with local queueing and secure sync                         | ✓ Covered       |
| FR11      | The system must cache the latest daily menu and pricing on the POS terminal at branch startup.                                          | Epic 1 - POS menu caching, pricing, and branch startup availability               | ✓ Covered       |
| FR12      | The system must preserve zero transaction loss and audit trails for offline transactions.                                               | Epic 1 - Durable offline transaction handling and audit trail preservation        | ✓ Covered       |
| FR13      | The system must support cash reconciliation and refund workflows with manager approval above thresholds.                                | Epic 4 - Cash reconciliation, refunds, and manager approval workflows             | ✓ Covered       |
| FR14      | The system must provide BOM relationships between menu items and ingredients and auto-deduct ingredients when orders are placed.        | Epic 3 - BOM recipe linkage and automatic ingredient deduction                    | ✓ Covered       |
| FR15      | The system must support status tracking for kitchen items: pending, cooking, ready, served, rejected.                                   | Epic 2 - Kitchen item status tracking and workflows                               | ✓ Covered       |
| FR16      | The system must provide role-based access control at UI and API layers.                                                                 | Epic 4 - Role-based access control and RBAC enforcement                           | ✓ Covered       |
| FR17      | The system must log permission-sensitive actions for audit and compliance.                                                              | Epic 4 - Permission-sensitive audit logging and compliance governance             | ✓ Covered       |
| FR18      | The system must store customer contact and visit preferences and support loyalty points and redemption flows.                           | Epic 5 - Customer profile, visit history, and loyalty support                     | ✓ Covered       |
| FR19      | The system must support table management and reservations as Phase 2 scope.                                                             | Epic 5 - Table management and reservations (Phase 2 scope)                        | ⚠︎ Phase 2 scope |
| FR20      | The system must support data migration planning, validation, cleansing, and parallel operation during cutover.                          | Epic 5 - Data migration planning, validation, cleansing, and cutover support      | ✓ Covered       |
| FR21      | The system must provide franchise menu override support and regional variants with pricing rules.                                       | Epic 4 - Franchise menu override support and regional pricing variants            | ✓ Covered       |
| FR22      | The system must support audit-ready reports for tax and regulatory checks.                                                              | Epic 5 - Audit-ready tax and regulatory reporting                                 | ✓ Covered       |

### Coverage Statistics

- Total PRD FRs: 22
- FRs covered in current epics: 21
- PRD items requiring explicit Phase 2 or future scope coverage: 1 (FR19)
- Coverage percentage: 95%

### Additional Epic Coverage Notes

- FR1–FR22 have been aligned to the PRD-extracted functional requirements; FR23–FR25 remain artifact-level entries in the epic document.
- The epics artifact now uses PRD-consistent FR descriptions to support direct traceability across documents.
- FR19 is explicitly identified as Phase 2 scope and should be confirmed in the implementation roadmap or added to a Phase 2 epic.
- Recommendation: maintain an explicit mapping table in both the PRD and epics artifact to preserve ID consistency for future readiness checks.

## UX Alignment Assessment

### UX Document Status

Found: `docs/ux-design.md`

### Alignment Issues

- The UX design strongly supports the PRD’s emphasis on speed, offline resilience, and role-based workflows.
- Architecture also supports the UX needs with explicit branch-local caching, offline sync, multi-tenancy, and kitchen workflow components.
- The UX document clearly implies web/tablet terminal flows and offline state visibility, which the architecture accounts for through branch POS terminals, local store/cache, and sync engine.

### Warnings

- The UX design includes QR ordering and delivery flows as Phase 1/later scope, while the PRD defines QR ordering as part of MVP foundations. This is a minor alignment gap in scope staging and should be reconciled.
- The architecture document does not explicitly mention mobile customer-facing interfaces for QR ordering, though it does support browser-based or lightweight desktop apps for branch and kitchen terminals.

## Epic Quality Review

### Epic Structure Assessment

- All five epics are user-valued and avoid overtly technical milestone phrasing.
- Epic independence is sound: Epic 2 is grounded on Epic 1 outputs, Epic 3 builds on prior epics, and no epic requires a later epic to function.
- Epic 5 is broad, combining reporting, customer engagement, and migration readiness. This may dilute focus and increase implementation complexity.

### Story Quality Assessment

- Most stories are clearly user-focused and independently completable.
- The epics artifact now separates staff shift tracking (Story 5.4) from legacy import/reconciliation (Story 5.5). Confirm that this split is preserved in implementation planning and acceptance criteria.
- Several acceptance criteria are serviceable but could be made more precise, especially around measurable performance and success conditions.

### Dependency Analysis

- No explicit forward dependencies were found in the story text.
- The document lacks an explicit intra-epic dependency map, which makes hidden ordering or scope assumptions harder to spot.
- There is a semantic traceability concern where FR4 (multi-tenancy and franchise isolation) should be mapped to Epic 4 rather than the checkout-focused Epic 1.

### Findings by Severity

#### 🔴 Critical Violations

- None found. No epics were rejected for being purely technical or dependent on future epics.

#### 🟠 Major Issues

- Story 5.4 combines unrelated user capabilities and should be split into separate stories for shift tracking and legacy migration.
- The PRD and epic artifact use different FR numbering schemes, so ID-based traceability should be aligned explicitly before relying on this coverage matrix.

#### 🟡 Minor Concerns

- Acceptance criteria could be tightened for select stories to improve testability and clarity.
- Epic 5’s scope is broad and may benefit from clearer segmentation into distinct outcome-focused epics.

## Final Assessment

### Overall Readiness Status

NEEDS WORK

### Critical Issues Requiring Immediate Action

1. Reconcile the mismatch between the PRD’s formal FR numbering and the epics document’s FR coverage map, especially FR23, FR24, and FR25.
2. Confirm the artifact split between staff shift tracking (Story 5.4) and legacy migration/import (Story 5.5), and keep their acceptance criteria distinct.
3. Reevaluate the mapping of FR4 to Epic 4 and ensure multi-tenancy/franchise isolation requirements are aligned with the appropriate epic.

### Recommended Next Steps

1. Update the PRD or epic artifact so that all FRs are numbered consistently and traceable across both documents.
2. Refine Story 5.4 into distinct, independently completable stories, each with clear acceptance criteria.
3. Consider segmenting Epic 5 into narrower outcome-focused epics to reduce implementation complexity.
4. Tighten acceptance criteria across key stories to improve testability and measurable validation.
5. Clarify the QR ordering scope in UX and architecture artifacts to ensure MVP and Phase staging are aligned.

### Final Note

This assessment found several alignment and structure issues but no blocking technical epic failures. The artifacts are close to readiness, but the identified scope, traceability, and story-structure issues should be addressed before moving into implementation.

Implementation Readiness Assessment Complete.

Report generated: `_bmad-output/planning-artifacts/implementation-readiness-report-2026-06-30.md`

The assessment found 2 major issues and several minor concerns requiring attention.
