---
baseline_commit: c518ba7cd2a6497c5c14a82f36a29c5553edef14
---

# Story 1.1: Create and Review a POS Bill Quickly

Status: review

## Story

As a cashier,
I want to create and review a bill quickly from the POS screen,
so that customers can pay and leave faster during peak hours.

## Acceptance Criteria

1. [x] A cashier can add menu items to a new bill and see the bill panel update immediately.
2. [x] Quantity changes and item removal recalculate the bill totals correctly.
3. [x] The bill remains easy to review without leaving the main billing flow.

## Tasks / Subtasks

- [x] Implement core POS bill calculation and item management (AC: #1, #2)
  - [x] Create a bill model that stores items, quantities, and totals.
  - [x] Support quantity updates and item removal with recalculated totals.
- [x] Add automated tests for bill behavior (AC: #1, #2)
  - [x] Cover item addition, quantity changes, and removal flows.

## Dev Notes

- The implementation follows a lightweight domain model focused on bill totals and item management.
- The initial scope targets the core billing calculation rules needed for the first checkout workflow.
- References: [Source: docs/product-requirements-document.md], [Source: docs/architecture.md]

## Dev Agent Record

### Agent Model Used

MAI-Code-1-Flash

### Debug Log References

- Implemented a minimal POS bill model in src/vireya/billing.py.
- Verified behavior through unittest coverage in tests/test_billing.py.

### Completion Notes List

- Added a bill model that supports adding, updating, and removing bill items with subtotal, tax, and total calculations.
- Added regression tests for quantity changes and item removal.

### File List

- src/vireya/**init**.py
- src/vireya/billing.py
- tests/test_billing.py

## Change Log

- 2026-07-04: Implemented bill item and total calculation workflow for the POS billing story.

## Status

- Current status: review
- Validation: unittest suite passed (2 tests)
