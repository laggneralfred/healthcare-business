# Sprint 11 Planning Note: `hc_checkout` Payment-Due Document Slice

Status:
- Planning only. No implementation work is authorized from this document.
- This note starts from the frozen Sprint 10 baseline.
- Sprint 10 checkout, pricing, and receipt boundaries remain unchanged.
- The slice stays intentionally narrow and checkout-only.

## 1. Planning Goal

Add the smallest possible printable payment-due document for one checkout session in the unpaid case without widening checkout into invoicing, accounting, collections, or broader billing workflows.

Target outcome:
- staff can produce one simple human-readable payment-due document for a checkout session in `payment_due`
- the output reuses the existing checkout record and checkout lines
- the current paid receipt / summary behavior remains unchanged
- appointment remains the workflow hub
- encounter remains untouched

This is not an invoicing phase.

## 2. Frozen Sprint 10 Baseline Preserved

Sprint 11 planning must preserve the current Sprint 10 posture:
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
- encounter remains unchanged
- `needs_follow_up` remains unchanged

Current workflow would become:
- `Lead Inquiry -> Create Patient -> Create Appointment -> Intake / Consent -> Start Visit -> Encounter -> Complete Visit -> Close Visit -> Start Checkout -> Review or edit lines -> Mark Payment Due -> Print Payment-Due Document`

Sprint 11 must not disturb the existing:
- `Print Checkout Summary` behavior for general checkout output
- paid receipt / summary behavior

## 3. In-Scope Slice

No new financial module is required.

Smallest supported scope:
- keep `hc_checkout` as the owning module
- add one printable/report-style payment-due output for `hc.checkout.session`
- restrict the document semantically to the `payment_due` case
- optionally add one visible print action from the checkout form when state is `payment_due`

Operational meaning:
- staff can hand or print a plain unpaid summary for the patient
- the document reflects the checkout session exactly as stored
- this slice does not add any collection workflow or payment processing behavior

## 4. Out Of Scope By Default

This planning note explicitly excludes:
- invoices
- accounting journals
- account moves
- taxes
- discounts
- refunds
- partial payments
- payment schedules
- statements of account
- aging logic
- dunning logic
- claims
- patient portal delivery
- payment gateway integration
- email delivery
- SMS delivery
- package or membership logic
- receipt numbering
- rebooking linkage
- encounter-based billing logic

## 5. Module Boundary

Sprint 11 should stay inside:
- `hc_checkout`

It may read existing Sprint 8, Sprint 9, and Sprint 10 checkout and pricing data from:
- `hc_checkout`
- `hc_pricing`

Boundary rule:
- `hc_checkout` owns the payment-due document output
- `hc_pricing` continues to own service-fee defaults only
- no new payment-due model should be introduced for this slice
- no invoice or accounting dependency should be introduced

## 6. Models Touched

### `hc.checkout.session`

Primary touched model:
- `hc.checkout.session`

Reason:
- the payment-due document is for one existing checkout session
- the report content should be sourced directly from the existing checkout record

Expected data already present and sufficient:
- `patient_id`
- `appointment_id`
- `appointment_start`
- `checkout_line_ids`
- `amount_total`
- `state`
- `payment_note`
- `tender_type`
- `paid_on`

Recommended model posture:
- no new required business fields
- no new payment fields
- no due-date field unless later clinic pressure proves it necessary
- `payment_note` may be reused as an optional due note if already populated

### `hc.checkout.line`

Read-only document content source:
- `sequence`
- `description`
- `amount`

Optional `service_fee_id` remains internal and does not need to display by default.

### `hc.appointment`

No model change required.

The appointment remains the workflow hub, but Sprint 11 does not need to add new appointment data or state.

## 7. Proposed Output Content

The payment-due document should remain plain and human-readable.

Recommended contents:
- practice
- checkout identifier or session name
- patient name
- appointment date/time context
- practitioner name if already present on the session
- checkout lines in sequence order
- line amounts
- total amount
- payment state
- optional due note using existing `payment_note` if present

Recommended display rule:
- the document should make it visually clear that payment is still due

Recommended omissions for this slice:
- invoice numbers
- due dates
- tax breakdowns
- claim references
- account balances beyond the current session total
- signatures
- portal links
- payment links

## 8. Report / Output Design

Smallest recommended implementation:
- one Odoo report action for `hc.checkout.session`
- one simple printable template specifically for the payment-due case

Recommended posture:
- report is intended for `payment_due`
- report is informational only
- report does not mutate checkout data

Suggested title options:
- `Payment Due`
- `Payment Due Summary`

Recommended state behavior:
- if `state == payment_due`, render the document normally
- if a later implementation needs a guard, prefer blocking or hiding the action outside `payment_due` rather than changing session state semantics

## 9. UI Touchpoints

### Checkout form

Recommended smallest UI addition:
- one `Print Payment Due` action on the checkout form

Recommended placement:
- form header or action menu

Recommended visibility:
- visible only when `state == payment_due`

Behavior:
- opens printable payment-due output for the current checkout session
- does not replace the existing `Checkout Summary` report

### Checkout list

Optional only if truly useful:
- keep list unchanged
- rely on form-level print action only

This is the preferred narrow approach.

### Appointment form

No new appointment action is required.

The current checkout entry point is enough.

## 10. Access Posture

### Owner
- can print any payment-due document already visible through current checkout access rules

### Front Desk
- can print payment-due documents for sessions they can access operationally

### Provider
- no new billing workflow should be introduced by default
- provider print access should stay aligned with existing checkout access, not widened for this slice

## 11. State Behavior

Sprint 11 must not change checkout states:
- `open`
- `paid`
- `payment_due`

Sprint 11 must not change payment actions:
- `Mark Cash Paid`
- `Mark Card Paid`
- `Mark Payment Due`

Document behavior rule:
- printing is read-only
- printing does not create a new record
- printing does not alter `state`, `paid_on`, `tender_type`, `amount_total`, or line content
- existing paid receipt / summary behavior remains unchanged

## 12. Backend / Report Test Plan

Recommended automated coverage:
- payment-due report action is available for a `payment_due` checkout session
- payment-due report renders for a `payment_due` checkout
- rendered document includes patient, appointment context, lines, total, and payment state
- rendered document includes `payment_note` when present
- rendered document does not show paid-only fields such as tender type and `paid_on`
- rendering does not mutate checkout state or payment fields
- front desk user can access the payment-due report for allowed sessions
- provider does not gain broader checkout access through the report
- existing receipt / summary behavior remains unaffected

If the implementation uses a QWeb report:
- include a report-render test at the model/report level
- do not rely only on manual browser printing

## 13. Explicit Non-Goals

Sprint 11 payment-due planning does not include:
- invoice generation
- posted accounting entries
- due-date tracking
- payment reminders
- emailed due notices
- SMS due notices
- claim forms
- partial-payment documents
- refund documents
- package or membership summaries
- checkout-state expansion
- encounter expansion

## 14. Recommended Acceptance Criteria

The smallest credible Sprint 11 slice should satisfy:
- staff can print one readable payment-due document for a checkout session in `payment_due`
- the document shows practice, patient, appointment context, checkout lines, total, and payment state
- an optional due note appears when `payment_note` is already populated
- existing paid receipt / summary behavior remains unchanged
- printing works without changing checkout data
- no invoice or accounting behavior is introduced
- appointment, encounter, and visit lifecycle behavior remain unchanged

## 15. Recommendation

Keep Sprint 11 strictly to:
- one payment-due report action
- one printable template for `payment_due`
- no new financial records
- no delivery-channel work
- no collections workflow

If later clinic pressure appears, it should be evaluated as a separate sprint rather than folded into this slice.
