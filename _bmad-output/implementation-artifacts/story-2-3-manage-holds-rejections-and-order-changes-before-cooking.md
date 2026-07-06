---
baseline_commit: c518ba7cd2a6497c5c14a82f36a29c5553edef14
---

# Story 2.3: Manage Holds, Rejections, and Order Changes Before Cooking

Status: review

## Story

As a kitchen staff member,
I want to hold or reject items and support order changes before cooking begins,
so that the kitchen can handle exceptions cleanly and the customer experience remains accurate.

## Acceptance Criteria

1. [x] Items can be explicitly held or rejected with a recorded reason.
2. [x] Customer-requested changes before cooking can be applied to the ticket.
3. [x] The audit trail captures exception and modification events so the latest order state remains consistent.

## Tasks / Subtasks

- [x] Implement hold and reject workflows for items (AC: #1)
  - [x] Record the reason and update the ticket state.
- [x] Support order changes before cooking starts (AC: #2, #3)
  - [x] Allow item quantity and special-request updates.
  - [x] Record modification events in the audit log.

## Dev Notes

- The implementation extends the kitchen ticket model with lightweight exception handling and modification support.
- This remains intentionally simple for the current story scope and can be expanded later.
- References: [Source: docs/product-requirements-document.md], [Source: docs/architecture.md]

## Dev Agent Record

### Agent Model Used

MAI-Code-1-Flash

### Debug Log References

- Extended src/vireya/kitchen.py with reject_item and update_item methods.
- Added regression tests in tests/test_kitchen_story.py for hold, reject, and order-change tracking.

### Completion Notes List

- Added hold and reject handling with reason tracking.
- Added item modification support and audit logging.

### File List

- src/vireya/kitchen.py
- tests/test_kitchen_story.py

## Change Log

- 2026-07-06: Implemented kitchen hold/reject workflows and order-change tracking.

## Status

- Current status: review
- Validation: unittest suite passed (20 tests)
