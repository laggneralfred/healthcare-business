# Sprint 12 Planning Note: Patient Statement / Account Summary Slice

Status:
- Planning only. No implementation work is authorized from this document.
- This note starts from the frozen Sprint 11 baseline.
- Sprint 11 checkout, pricing, receipt, and payment-due boundaries remain unchanged.
- The slice stays intentionally narrow and reporting-only.

## 1. Planning Goal

Add the smallest possible patient-level unpaid summary without widening checkout into invoicing, accounting, collections, or broader billing workflows.

Target outcome:
- front desk can produce one simple human-readable patient statement based on existing unpaid checkout sessions
- the output reuses existing `hc.checkout.session` records in `payment_due`
- no new financial record is introduced
- appointment remains the workflow hub
- encounter remains untouched

This is not an invoicing phase.

## 2. Frozen Sprint 11 Baseline Preserved

Sprint 12 planning must preserve the current Sprint 11 posture:
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
- encounter remains unchanged
- `needs_follow_up` remains unchanged

Current workflow would become:
- `Lead Inquiry -> Create Patient -> Create Appointment -> Intake / Consent -> Start Visit -> Encounter -> Complete Visit -> Close Visit -> Start Checkout -> Mark Payment Due where needed -> Open Patient Statement -> Print Patient Account Summary`

Sprint 12 must not disturb the existing:
- `Checkout Summary` behavior
- `Payment Due` document behavior
- checkout payment actions

## 3. In-Scope Slice

No new financial module is required.

Smallest supported scope:
- keep `hc_checkout` as the owning module
- add one patient-level report/output based on existing `hc.checkout.session` records in `payment_due`
- allow front desk to generate that output for one patient
- compute a patient-level total due from existing unpaid checkout sessions

Operational meaning:
- staff can hand or print a plain patient account summary of currently unpaid checkout sessions
- the output reflects existing checkout records exactly as stored
- this slice does not add collection workflow or payment processing behavior

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
- aging buckets
- dunning logic
- claim processing
- patient portal delivery
- payment gateway integration
- email delivery
- SMS delivery
- packages
- memberships
- rebooking linkage
- encounter-based billing logic
- balance-forward logic beyond unpaid checkout totals

## 5. Module Boundary

Sprint 12 should stay inside:
- `hc_checkout`

It may read existing data from:
- `hc_checkout`
- `hc_pricing`
- `hc_patient_core`

Boundary rule:
- `hc_checkout` owns the patient statement output
- `hc_pricing` continues to own service-fee defaults only
- no new patient statement model should be introduced for this slice
- no invoice or accounting dependency should be introduced

## 6. Models Touched

### `res.partner`

Primary patient context model:
- `res.partner`

Reason:
- the statement is patient-level
- the report should be anchored to one patient and derive unpaid sessions from existing checkout records

Recommended model posture:
- no new required fields
- no account-balance field
- no receivable logic

### `hc.checkout.session`

Primary record source:
- filter to sessions where:
  - `patient_id` matches the selected patient
  - `state == payment_due`

Expected data already present and sufficient:
- `patient_id`
- `appointment_id`
- `appointment_start`
- `checkout_line_ids`
- `amount_total`
- `payment_note`
- `state`

Recommended model posture:
- no new business fields
- no new due-date field unless later clinic pressure proves it necessary

### `hc.checkout.line`

Optional supporting detail source:
- `description`
- `amount`

Recommended narrow rule:
- line summaries are optional in Sprint 12
- if included, keep them lightweight and derived from existing lines only

### `hc.appointment`

No model change required.

Appointment remains the workflow hub, but Sprint 12 does not need to add new appointment data or state.

## 7. Proposed Output Content

The patient statement should remain plain and human-readable.

Recommended contents:
- practice
- patient
- list of unpaid checkout sessions
- appointment context for each unpaid session
- per-session amount due
- total due across unpaid sessions
- optional per-session note using existing `payment_note` if present

Optional only if already practical:
- lightweight line summaries under each unpaid checkout session

Recommended omissions for this slice:
- invoice numbers
- due dates
- tax breakdowns
- claim references
- account history beyond current unpaid checkout sessions
- payment links
- signatures

## 8. Report / Output Design

Smallest recommended implementation:
- one Odoo report action anchored to the patient context or a simple patient-level wizardless action
- one printable template summarizing all current `payment_due` checkout sessions for that patient

Recommended posture:
- report is informational only
- report does not mutate checkout data
- report is limited to unpaid checkout sessions only

Suggested title options:
- `Patient Statement`
- `Account Summary`
- `Unpaid Checkout Summary`

Recommended total rule:
- statement total equals the sum of `amount_total` for all included `payment_due` checkout sessions

## 9. UI Touchpoints

### Patient form

Recommended smallest UI addition:
- one `Print Patient Statement` action on the patient form

Recommended behavior:
- prints a statement for the current patient
- includes only current `payment_due` checkout sessions

### Checkout area

Optional only if truly useful:
- no new checkout action required
- keep patient statement generation patient-centered

This is the preferred narrow approach.

### Appointment form

No new appointment action is required.

## 10. Access Posture

### Owner
- can print any patient statement already visible through current access rules

### Front Desk
- can print patient statements for patients and checkout sessions they can access operationally

### Provider
- no new billing workflow should be introduced by default
- provider access should stay aligned with existing checkout access, not widened for this slice

## 11. State Behavior

Sprint 12 must not change checkout states:
- `open`
- `paid`
- `payment_due`

Sprint 12 must not change payment actions:
- `Mark Cash Paid`
- `Mark Card Paid`
- `Mark Payment Due`

Statement behavior rule:
- printing is read-only
- printing does not create a new record
- printing does not alter `state`, `paid_on`, `tender_type`, `amount_total`, or line content
- existing `Checkout Summary` and `Payment Due` document behavior remain unchanged

## 12. Backend / Report Test Plan

Recommended automated coverage:
- patient statement report action is available for an eligible patient context
- report includes only `payment_due` checkout sessions for the selected patient
- report excludes `paid` and `open` checkout sessions
- report includes appointment context and per-session totals
- report includes the patient-level total due
- report includes `payment_note` when present
- optional line summaries render correctly if included
- rendering does not mutate checkout state or payment fields
- front desk user can access the patient statement for allowed patients
- provider does not gain broader checkout access through the statement

If the implementation uses a QWeb report:
- include a report-render test at the model/report level
- do not rely only on manual browser printing

## 13. Explicit Non-Goals

Sprint 12 patient statement planning does not include:
- invoice generation
- posted accounting entries
- due-date tracking
- payment reminders
- emailed statements
- SMS statements
- portal statements
- claims summaries
- partial-payment statements
- refund statements
- package or membership summaries
- checkout-state expansion
- encounter expansion

## 14. Recommended Acceptance Criteria

The smallest credible Sprint 12 slice should satisfy:
- front desk can print one readable patient-level unpaid summary
- the statement shows practice, patient, unpaid checkout sessions, appointment context, and total due
- only `payment_due` checkout sessions are included
- optional line summaries are included only if they remain simple and derived from existing data
- printing works without changing checkout data
- no invoice or accounting behavior is introduced
- appointment, encounter, and visit lifecycle behavior remain unchanged

## 15. Recommendation

Keep Sprint 12 strictly to:
- one patient-level statement report
- one printable template
- no new financial records
- no delivery-channel work
- no collections workflow

If later clinic pressure appears, it should be evaluated as a separate sprint rather than folded into this slice.
