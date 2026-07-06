---
baseline_commit: c518ba7cd2a6497c5c14a82f36a29c5553edef14
---

# Story 2.2: Update Item Status and Handle Partial Fulfillment

Status: review

## Story

As a kitchen staff member,
I want to update item status and manage partial fulfillment,
so that the front-of-house and kitchen stay aligned on order progress.

## Acceptance Criteria

1. [x] A ticket can reflect item status changes such as cooking, ready, served, or rejected.
2. [x] Items can be completed independently when some remain pending.
3. [x] Tickets can be flagged as stale when they remain in the queue beyond a configured waiting threshold.

## Tasks / Subtasks

- [x] Implement status transitions for ticket items (AC: #1)
  - [x] Support updating item state and retaining audit history.
- [x] Support partial fulfillment and stale detection (AC: #2, #3)
  - [x] Allow served items to be handled independently from pending items.
  - [x] Track waiting duration and mark tickets as stale when the threshold is exceeded.

## Dev Notes

- The implementation extends the kitchen ticket model with lightweight status progression and stale-order indicators.
- This scope stays intentionally simple and can be expanded with richer kitchen-board integrations later.
- References: [Source: docs/product-requirements-document.md], [Source: docs/architecture.md]

## Dev Agent Record

### Agent Model Used

MAI-Code-1-Flash

### Debug Log References

- Extended src/vireya/kitchen.py with waiting-time tracking and stale-ticket indicators.
- Added regression tests in tests/test_kitchen_story.py for partial fulfillment and stale detection.

### Completion Notes List

- Added item status updates and per-item fulfillment handling.
- Added waiting-duration tracking and stale ticket highlighting.

### File List

- src/vireya/kitchen.py
- tests/test_kitchen_story.py

## Change Log

- 2026-07-06: Implemented item status transitions and stale-order support for kitchen tickets.

## Status

- Current status: review
- Validation: unittest suite passed (19 tests)
