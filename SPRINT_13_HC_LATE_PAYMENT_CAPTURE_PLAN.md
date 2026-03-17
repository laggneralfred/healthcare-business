# Sprint 13 Planning Note: Late Payment Capture Slice

Status:
- Planning only. No implementation work is authorized from this document.
- This note starts from the frozen Sprint 12 baseline.
- Sprint 12 checkout, pricing, summary, payment-due, and patient-statement boundaries remain unchanged.
- The slice stays intentionally narrow and checkout-only.

## 1. Planning Goal

Add the smallest possible late-payment capture path for existing `payment_due` checkout sessions without widening checkout into invoicing, accounting, or broader billing workflows.

Target outcome:
- front desk can reopen the narrow operational loop on an existing unpaid checkout
- a `payment_due` checkout can later be marked fully paid by cash or card
- the output documents already added in earlier sprints continue to reflect the updated session state
- appointment remains the workflow hub
- encounter remains untouched

This is not a collections or invoicing phase.

## 2. Frozen Sprint 12 Baseline Preserved

Sprint 13 planning must preserve the current Sprint 12 posture:
- appointment remains the workflow hub
- visit lifecycle remains:
  - `scheduled`
  - `in_progress`
  - `completed`
  - `closed`
- checkout still begins only after `Close Visit`
- one checkout session remains tied to one appointment
- checkout remains line-driven
- checkout states remain:
  - `open`
  - `paid`
  - `payment_due`
- pricing remains a structured defaulting layer only
- printable checkout summary remains implemented
- printable payment-due document remains implemented
- patient-level unpaid summary remains implemented
- encounter remains unchanged
- `needs_follow_up` remains unchanged

Current workflow would become:
- `Lead Inquiry -> Create Patient -> Create Appointment -> Intake / Consent -> Start Visit -> Encounter -> Complete Visit -> Close Visit -> Start Checkout -> Mark Payment Due when needed -> Later collect payment -> Mark existing checkout paid`

Sprint 13 must not disturb the existing:
- `Checkout Summary` behavior
- `Payment Due` document behavior
- patient statement behavior

## 3. In-Scope Slice

No new financial module is required.

Smallest supported scope:
- keep `hc_checkout` as the owning module
- extend `hc.checkout.session` only
- allow `payment_due` checkout sessions to be marked paid later
- add narrow late-collection actions:
  - `Collect Cash Payment`
  - `Collect Card Payment`

Operational meaning:
- a session already marked `payment_due` can transition to `paid`
- this remains full-payment-only
- no new record is created for the later payment event

## 4. Out Of Scope By Default

This planning note explicitly excludes:
- invoices
- accounting journals
- account moves
- taxes
- discounts
- refunds
- partial payments
- split tenders
- payment schedules
- installment logic
- claims
- patient portal delivery
- payment gateway integration
- email delivery
- SMS delivery
- packages
- memberships
- rebooking linkage
- encounter-based billing logic

## 5. Module Boundary

Sprint 13 should stay inside:
- `hc_checkout`

It may continue to read existing data from:
- `hc_checkout`
- `hc_pricing`

Boundary rule:
- `hc_checkout` owns the late-payment state transition
- `hc_pricing` continues to own service-fee defaults only
- no new payment or receipt model should be introduced for this slice
- no invoice or accounting dependency should be introduced

## 6. Models Touched

### `hc.checkout.session`

Primary touched model:
- `hc.checkout.session`

Reason:
- late payment capture is a state transition on an existing checkout session

Expected data already present and sufficient:
- `state`
- `tender_type`
- `paid_on`
- `amount_paid`
- `amount_total`

Recommended model posture:
- no new required business fields
- no payment transaction model
- no balance field
- no partial-payment data

### `hc.appointment`

No model change required.

Appointment remains the workflow hub, but Sprint 13 does not need new appointment data or new appointment actions.

## 7. Proposed Actions And Behavior

Recommended new actions on `hc.checkout.session`:
- `Collect Cash Payment`
- `Collect Card Payment`

Recommended eligibility rule:
- available only when `state == payment_due`

Recommended behavior for `Collect Cash Payment`:
- set `state = paid`
- set `tender_type = cash`
- set `paid_on`
- set `amount_paid = amount_total`

Recommended behavior for `Collect Card Payment`:
- set `state = paid`
- set `tender_type = card`
- set `paid_on`
- set `amount_paid = amount_total`

Recommended guardrail:
- these actions should not reopen checkout to `open`
- they should directly convert `payment_due` to `paid`

## 8. UI Touchpoints

### Checkout form

Recommended smallest UI addition:
- two buttons visible only when `state == payment_due`

Suggested button labels:
- `Collect Cash Payment`
- `Collect Card Payment`

Recommended placement:
- checkout form header near the existing status and payment actions

### Appointment form

No new appointment action is required.

The existing appointment checkout summary should simply reflect the updated session state after late collection.

### Patient statement and payment-due document

No new UI entry point is required.

Expected downstream effect only:
- once late payment is collected, the session should no longer appear in unpaid-only outputs

## 9. Access Posture

### Owner
- can collect late payment on accessible `payment_due` checkout sessions

### Front Desk
- can collect late payment on accessible `payment_due` checkout sessions

### Provider
- no new billing workflow should be introduced by default
- provider access should stay aligned with existing checkout access, not widened for this slice

## 10. State Behavior

Sprint 13 must not change the available checkout states:
- `open`
- `paid`
- `payment_due`

Sprint 13 must not add:
- `partially_paid`
- `refunded`
- `cancelled`

Recommended transition rule:
- `payment_due -> paid` is allowed through the new late-collection actions

Preserved rules:
- `open -> paid` still works through the existing payment actions
- `open -> payment_due` still works through the existing `Mark Payment Due` action
- amount totals remain line-driven

## 11. Reporting Behavior

Existing outputs should remain, but their content should naturally reflect the new session state.

Expected result:
- `Checkout Summary` for the session shows the later `paid` state, tender, and paid date
- `Payment Due` document remains a payment-due-only document and should no longer be the relevant output after late collection
- patient statement should exclude sessions no longer in `payment_due`

Sprint 13 should not introduce:
- new receipt numbering
- new statement model
- new payment history report

## 12. Backend Test Plan

Recommended automated coverage:
- `Collect Cash Payment` works only for `payment_due`
- `Collect Card Payment` works only for `payment_due`
- both actions set:
  - `state = paid`
  - `amount_paid = amount_total`
  - `paid_on`
  - the expected `tender_type`
- late collection does not alter appointment lifecycle fields
- late collection does not alter `needs_follow_up`
- payment-due document action is no longer appropriate once the session is paid
- patient statement no longer includes the session after late payment is collected
- front desk can perform late collection
- provider does not gain broader checkout access through late collection

## 13. Explicit Non-Goals

Sprint 13 late-payment planning does not include:
- invoice generation
- posted accounting entries
- partial payments
- split tenders
- refund flows
- write-offs
- discounts
- claims handling
- emailed reminders
- SMS reminders
- portal payments
- gateway capture
- package or membership summaries
- checkout-state expansion
- encounter expansion

## 14. Recommended Acceptance Criteria

The smallest credible Sprint 13 slice should satisfy:
- front desk can mark an existing `payment_due` checkout as paid later
- the action records full payment only
- tender type, paid date, and amount paid are updated correctly
- unpaid-only outputs stop including the session after late collection
- existing checkout summary behavior remains intact
- no invoice or accounting behavior is introduced
- appointment, encounter, and visit lifecycle behavior remain unchanged

## 15. Recommendation

Keep Sprint 13 strictly to:
- two late-collection actions on `hc.checkout.session`
- no new financial records
- no new delivery-channel work
- no partial-payment logic

If later clinic pressure appears, it should be evaluated as a separate sprint rather than folded into this slice.
