---
baseline_commit: c518ba7cd2a6497c5c14a82f36a29c5553edef14
---

# Story 1.3: Continue Billing Offline and Recover Sync State

Status: review

## Story

As a cashier,
I want the POS to keep accepting orders and payments while offline,
so that branch operations continue during connectivity interruptions.

## Acceptance Criteria

1. [x] A bill can be marked offline and continue to queue local transaction state for later synchronization.
2. [x] When connectivity is restored, the bill can be synced and its pending queue cleared.
3. [x] The POS exposes a clear offline banner so staff always know the sync state.

## Tasks / Subtasks

- [x] Implement offline state and local sync queue handling (AC: #1, #2)
  - [x] Support entering offline mode and counting pending sync work.
  - [x] Support syncing queued work back to ready state.
- [x] Add automated tests for offline and recovery behavior (AC: #1, #2, #3)
  - [x] Cover offline queuing, sync recovery, and banner display.

## Dev Notes

- The implementation extends the bill domain model with offline-mode state and a lightweight sync queue.
- Sync states are intentionally simple for the current story scope and can be expanded later.
- References: [Source: docs/product-requirements-document.md], [Source: docs/architecture.md]

## Dev Agent Record

### Agent Model Used

MAI-Code-1-Flash

### Debug Log References

- Extended src/vireya/billing.py with offline mode, pending sync counting, and sync transition logic.
- Verified behavior through unittest coverage in tests/test_offline_sync.py.

### Completion Notes List

- Added offline-mode tracking and pending sync queue behavior.
- Added offline banner support and sync recovery logic.

### File List

- src/vireya/billing.py
- tests/test_offline_sync.py

## Change Log

- 2026-07-05: Implemented offline billing state, pending sync queueing, and sync recovery support.

## Status

- Current status: review
- Validation: unittest suite passed (7 tests)
