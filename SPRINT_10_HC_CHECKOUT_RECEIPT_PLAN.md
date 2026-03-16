# Sprint 10 Planning Note: `hc_checkout` Receipt / Printable Summary Slice

Status:
- Planning only. No implementation work is authorized from this document.
- This note starts from the frozen Sprint 9 baseline.
- Sprint 9 checkout and pricing boundaries remain unchanged.
- The slice stays intentionally narrow and checkout-only.

## 1. Planning Goal

Add the smallest possible printable checkout summary for one checkout session without widening checkout into invoicing, accounting, messaging, or broader patient-financial workflows.

Target outcome:
- staff can produce one simple human-readable summary for a checkout session
- the output reflects the existing checkout record rather than creating a new financial model
- appointment remains the workflow hub
- checkout remains a narrow self-pay operational record
- encounter remains untouched

This is not an invoicing phase.

## 2. Frozen Sprint 9 Baseline Preserved

Sprint 10 planning must preserve the current Sprint 9 posture:
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
- encounter remains unchanged
- `needs_follow_up` remains unchanged

Current workflow would become:
- `Lead Inquiry -> Create Patient -> Create Appointment -> Intake / Consent -> Start Visit -> Encounter -> Complete Visit -> Close Visit -> Start Checkout -> Review or edit lines -> Mark Cash Paid / Mark Card Paid / Mark Payment Due -> Print Checkout Summary`

## 3. In-Scope Slice

No new financial module is required.

Smallest supported scope:
- keep `hc_checkout` as the owning module
- add one printable/report-style output for `hc.checkout.session`
- optionally add one visible print action from the checkout form
- optionally expose the print action from the existing checkout entry point only

Operational meaning:
- staff can hand a patient or keep a paper copy of a plain checkout summary
- the summary reflects the checkout session as currently stored
- this slice does not change checkout payment behavior

## 4. Out Of Scope By Default

This planning note explicitly excludes:
- invoices
- accounting journals
- account moves
- taxes
- discounts
- refunds
- partial payments
- customer statements
- account balances
- claims
- patient portal delivery
- payment gateway integration
- email delivery
- SMS delivery
- receipt numbering
- fiscal printer integration
- barcode or QR payment flows
- package or membership logic
- rebooking linkage
- encounter-based billing logic

## 5. Module Boundary

Sprint 10 should stay inside:
- `hc_checkout`

It may read existing Sprint 8 and Sprint 9 checkout and pricing data from:
- `hc_checkout`
- `hc_pricing`

Boundary rule:
- `hc_checkout` owns the printable summary output
- `hc_pricing` continues to own service-fee defaults only
- no new receipt model should be introduced for this slice
- no invoice or accounting dependency should be introduced

## 6. Models Touched

### `hc.checkout.session`

Primary touched model:
- `hc.checkout.session`

Reason:
- the printable output is for one checkout session
- the report content should be sourced directly from the existing checkout record

Expected data already present and sufficient:
- `patient_id`
- `appointment_id`
- `appointment_start`
- `checkout_line_ids`
- `amount_total`
- `state`
- `tender_type`
- `paid_on`

Recommended model posture:
- no new required business fields
- no new payment fields
- no new numbering field unless later clinic pressure proves it necessary

### `hc.checkout.line`

Read-only report content source:
- `sequence`
- `description`
- `amount`
- optional `service_fee_id` stays internal and does not need to be displayed by default

### `hc.appointment`

No model change required.

The appointment remains the workflow hub, but Sprint 10 does not need to add new appointment data or state.

## 7. Proposed Output Content

The printable summary should remain plain and human-readable.

Recommended contents:
- clinic/practice name if already available through existing relationships
- checkout identifier or session name
- patient name
- appointment date/time context
- practitioner name if already present on the session
- checkout lines in sequence order
- line amounts
- total amount
- payment state
- tender type when state is `paid`
- paid date/time when state is `paid`

Recommended omissions for this slice:
- tax breakdowns
- balance-forward sections
- invoice numbers
- claim references
- payment processor metadata
- signatures
- portal links

## 8. Report / Output Design

Smallest recommended implementation:
- one Odoo report action for `hc.checkout.session`
- one simple printable template

Recommended posture:
- report works for `open`, `paid`, and `payment_due`
- report is informational only
- report does not mutate checkout data

Suggested title:
- `Checkout Summary`

Suggested status display:
- `Open`
- `Paid`
- `Payment Due`

Suggested payment display rules:
- if `state == paid`, show:
  - tender type
  - paid date/time
- if `state == payment_due`, show that payment was not collected
- if `state == open`, show that checkout is still open

## 9. UI Touchpoints

### Checkout form

Recommended smallest UI addition:
- one `Print Summary` action on the checkout form

Recommended placement:
- form header or action menu

Behavior:
- available without changing checkout state
- opens printable report output for the current checkout session

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
- can print any checkout summary already visible through current access rules

### Front Desk
- can print checkout summaries for sessions they can access operationally

### Provider
- no new billing workflow should be introduced by default
- provider print access should stay aligned with existing checkout access, not widened for this slice

## 11. State Behavior

Sprint 10 must not change checkout states:
- `open`
- `paid`
- `payment_due`

Sprint 10 must not change payment actions:
- `Mark Cash Paid`
- `Mark Card Paid`
- `Mark Payment Due`

Report behavior rule:
- printing is read-only
- printing does not create a new record
- printing does not alter `paid_on`, `tender_type`, `amount_total`, or line content

## 12. Backend / Report Test Plan

Recommended automated coverage:
- report action is available for a checkout session
- report renders for an `open` checkout
- report renders for a `paid` checkout and includes tender type and paid date
- report renders for a `payment_due` checkout
- multi-line checkout content appears in sequence order
- rendered summary includes total amount
- rendering does not mutate checkout state or payment fields
- front desk user can access the report for allowed sessions
- provider does not gain broader checkout access through the report

If the implementation uses a QWeb report:
- include a report-render test at the model/report level
- do not rely only on manual browser printing

## 13. Explicit Non-Goals

Sprint 10 receipt planning does not include:
- invoice generation
- posted accounting entries
- tax receipts
- discount receipts
- refund receipts
- partial-payment receipts
- emailed receipts
- SMS receipts
- downloadable portal receipts
- printed claim forms
- package or membership summaries
- checkout-state expansion
- encounter expansion

## 14. Recommended Acceptance Criteria

The smallest credible Sprint 10 slice should satisfy:
- staff can print one readable summary for a checkout session
- the summary shows patient, appointment context, checkout lines, total, and payment status
- tender type and paid date appear only when applicable
- printing works without changing checkout data
- no invoice or accounting behavior is introduced
- appointment, encounter, and visit lifecycle behavior remain unchanged

## 15. Recommendation

Keep Sprint 10 strictly to:
- one report action
- one printable template
- no new financial records
- no delivery channel work

If later clinic pressure appears, it should be evaluated as a separate sprint rather than folded into this slice.
