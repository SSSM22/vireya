---
baseline_commit: c518ba7cd2a6497c5c14a82f36a29c5553edef14
---

# Story 2.1: Deliver Digital Kitchen Tickets for New Orders

Status: review

## Story

As a kitchen staff member,
I want new orders to appear as digital KOT tickets immediately,
so that food preparation can begin without delay.

## Acceptance Criteria

1. [x] A finalized order can be submitted to the kitchen as a KOT ticket with item details, quantities, modifiers, and special requests.
2. [x] Active tickets are prioritized so higher-urgency orders rise to the top of the kitchen queue.
3. [x] QR or other digital order submissions can flow through the shared KOT pipeline without manual re-entry.

## Tasks / Subtasks

- [x] Implement KOT ticket creation for new orders (AC: #1, #3)
  - [x] Accept order payloads and map them into kitchen ticket items.
  - [x] Preserve order source, priority, and item-level details.
- [x] Add automated coverage for ticket creation and prioritization (AC: #2)
  - [x] Verify ticket submission creates a prioritized queue entry.

## Dev Notes

- The implementation adds a lightweight order-to-ticket pathway in the kitchen domain model.
- Ticket payloads are intentionally simple for the current scope and can be expanded later for richer kitchen workflows.
- References: [Source: docs/product-requirements-document.md], [Source: docs/architecture.md]

## Dev Agent Record

### Agent Model Used

MAI-Code-1-Flash

### Debug Log References

- Extended src/vireya/kitchen.py with a submit_order flow that builds a ticket from order payloads.
- Added regression coverage in tests/test_kitchen_story.py for ticket creation, source tracking, and queue prioritization.

### Completion Notes List

- Added a kitchen ticket submission flow for new orders.
- Added queue prioritization and source-aware ticket creation.

### File List

- src/vireya/kitchen.py
- tests/test_kitchen_story.py

## Change Log

- 2026-07-06: Implemented KOT ticket submission from new order payloads and added priority-based queue support.

## Status

- Current status: review
- Validation: unittest suite passed (18 tests)
