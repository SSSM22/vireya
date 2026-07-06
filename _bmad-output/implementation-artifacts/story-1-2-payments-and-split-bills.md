---
baseline_commit: c518ba7cd2a6497c5c14a82f36a29c5553edef14
---

# Story 1.2: Accept Multiple Payments and Split Shared Bills

Status: review

## Story

As a cashier,
I want to accept cash, UPI, or card payments and split shared bills,
so that customers can pay flexibly without delays or confusion.

## Acceptance Criteria

1. [x] A completed bill can record a supported payment method and update the bill state accordingly.
2. [x] A shared bill can be split across multiple payment allocations with the remaining balance tracked correctly.
3. [x] A failed payment attempt leaves the bill in a recoverable state for a retry or alternate method.

## Tasks / Subtasks

- [x] Implement bill payment recording and split allocation tracking (AC: #1, #2)
  - [x] Support recording cash, UPI, or card payments against a bill.
  - [x] Track multiple payment allocations and compute the remaining balance.
- [x] Add automated tests for payment and recovery behavior (AC: #1, #2, #3)
  - [x] Cover successful payment capture, split billing, and payment failure recovery.

## Dev Notes

- The implementation extends the existing bill domain model with payment allocation state.
- Payment failures are captured as recoverable metadata without mutating the bill's item state.
- References: [Source: docs/product-requirements-document.md], [Source: docs/architecture.md]

## Dev Agent Record

### Agent Model Used

MAI-Code-1-Flash

### Debug Log References

- Extended src/vireya/billing.py with payment recording, split-payment tracking, and failure state.
- Verified behavior through unittest coverage in tests/test_payments.py.

### Completion Notes List

- Added payment recording for single and split payments.
- Added payment failure tracking so the bill remains recoverable.

### File List

- src/vireya/billing.py
- tests/test_payments.py

## Change Log

- 2026-07-05: Implemented payment capture, split-bill allocation tracking, and payment failure recovery support.

## Status

- Current status: review
- Validation: unittest suite passed (5 tests)
