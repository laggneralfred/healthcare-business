# Sprint 9 Planning Note: `hc_checkout` Multi-Line Slice

Status:
- Planning only. No implementation work is authorized from this document.
- This note starts from the frozen Sprint 8 baseline.
- Sprint 8 checkout and pricing boundaries remain unchanged.
- The slice stays intentionally narrow and checkout-only.

## 1. Planning Goal

Add the smallest possible multi-line checkout capability without widening checkout into billing, accounting, or broader financial workflows.

Target outcome:
- one checkout session can hold a small number of charge lines
- checkout total is computed from those lines
- payment actions remain exactly as they are today
- service-fee defaults continue to help with line defaults
- appointment remains the workflow hub
- encounter remains untouched

This is not an invoicing phase.

## 2. Frozen Sprint 8 Baseline Preserved

Sprint 9 planning must preserve the current Sprint 8 posture:
- appointment remains the workflow hub
- visit lifecycle remains:
  - `scheduled`
  - `in_progress`
  - `completed`
  - `closed`
- checkout still begins only after `Close Visit`
- one checkout session remains tied to one appointment
- checkout states remain:
  - `open`
  - `paid`
  - `payment_due`
- encounter remains unchanged
- `needs_follow_up` remains unchanged
- pricing remains a structured defaulting layer only

Current workflow would become:
- `Lead Inquiry -> Create Patient -> Create Appointment -> Intake / Consent -> Start Visit -> Encounter -> Complete Visit -> Close Visit -> Start Checkout -> One default checkout line appears -> Front desk may add or edit a few lines -> Mark Cash Paid / Mark Card Paid / Mark Payment Due`

## 3. In-Scope Slice

No new module is required.

Smallest supported scope:
- keep `hc_checkout` as the owning module
- add one minimal checkout-line model under `hc_checkout`
- each line supports:
  - `description`
  - `amount`
  - optional `service_fee_id`
  - `sequence`
- checkout total is computed from line amounts
- payment actions keep using the checkout session total

Operational meaning:
- checkout stops being “one description and one amount only”
- checkout still remains a very small self-pay operational record

## 4. Out Of Scope By Default

This planning note explicitly excludes:
- invoices
- accounting journals
- account moves
- taxes
- discounts
- refunds
- partial payments
- packages
- memberships
- claims
- patient portal
- payment gateway integration
- terminal integration
- multi-session checkout per appointment
- quantity-based pricing
- unit prices
- bundled pricing logic
- formulas or automatic pricing rules
- retail inventory behavior
- rebooking linkage
- encounter-based billing logic

## 5. Module Boundary

Sprint 9 should stay inside:
- `hc_checkout`

It may reuse existing Sprint 8 pricing records from:
- `hc_pricing`

Boundary rule:
- `hc_checkout` owns the session and line records
- `hc_pricing` continues to own fee defaults only
- appointment continues to initiate checkout
- encounter stays unchanged

No new billing module should be introduced for this slice.

## 6. Proposed Models And Fields

### New model: `hc.checkout.line`

Purpose:
- hold one charge entry within a checkout session

Required fields:
- `checkout_session_id`
  - required
  - many2one to `hc.checkout.session`
- `sequence`
  - integer
  - default ordering field
- `description`
  - required
  - user-facing line description
- `amount`
  - required monetary
  - line amount only
- `service_fee_id`
  - optional many2one to `hc.service.fee`
- `currency_id`
  - required monetary currency
  - related or copied from checkout session

Recommended minimal behavior:
- order by `sequence, id`
- non-negative amount validation
- optional same-practice guard for `service_fee_id`

No additional line complexity in this slice:
- no quantity
- no unit price
- no taxes
- no discount fields
- no subtotal formula beyond the line amount itself

### Minimal extension: `hc.checkout.session`

Add:
- `checkout_line_ids`
  - one2many to `hc.checkout.line`

Repurpose:
- `amount_total`
  - becomes computed from the sum of line amounts

Sprint 9 source-of-truth rule:
- checkout lines become the source of charge content
- session-level payment fields remain the source of payment-state tracking

## 7. Recommended Transition From Sprint 8 Single-Charge Checkout

To keep the implementation small and safe:
- when a checkout session is created, the system should also create exactly one default line
- that first line should carry the same default description and amount the Sprint 8 session would have used

Default source for the initial line:
- if an appointment type default service fee exists:
  - use that fee for the first line
- otherwise:
  - use the existing fallback description and amount behavior from Sprint 8

This keeps Sprint 9 behavior familiar:
- single-line checkout still works immediately
- multi-line capability is added only when needed

## 8. Total And State Behavior

### Total computation

Smallest recommended rule:
- checkout `amount_total` is computed as the sum of all checkout line `amount` values

### Payment actions

Sprint 9 must not change payment actions:
- `Mark Cash Paid`
- `Mark Card Paid`
- `Mark Payment Due`

Current preserved meaning:
- `paid` still means full payment for the computed checkout total
- `payment_due` still means no payment was collected during checkout

### Read/write posture by state

Recommended narrow rule:
- lines can be created, edited, reordered, or removed only while checkout state is `open`
- once checkout is `paid` or `payment_due`, lines become readonly

## 9. Service Fee Integration

Sprint 9 should reuse existing Sprint 8 pricing defaults without widening the pricing model.

Recommended line-level behavior:
- each line may optionally select `service_fee_id`
- selecting a fee on a line may prefill:
  - `description`
  - `amount`

Preserved manual-edit rule:
- line `description` remains manually editable
- line `amount` remains manually editable

Stability rule:
- line values are copied at the time of selection
- later changes to a service fee record do not retroactively rewrite old checkout lines

## 10. UI Touchpoints

### Checkout form

Replace the single-charge editing focus with a minimal lines section:
- one2many lines table on the checkout form
- editable only while state is `open`
- uses `list`, not deprecated `tree`

Recommended columns:
- `sequence`
- `description`
- `service_fee_id`
- `amount`

Recommended posture:
- the first line appears automatically
- front desk may add a small number of lines if needed
- session header still shows payment state and summary values

### Session summary area

Keep:
- `amount_total`
- payment fields
- payment actions

Do not add:
- invoice actions
- discount widgets
- tax widgets
- payment-allocation UI

### Appointment form

No new appointment action is needed.

Appointment remains unchanged except that its existing checkout summary would reflect the line-computed total.

## 11. Access Posture

### Owner
- full checkout-line access through existing checkout workflow

### Front Desk
- full operational access to checkout lines while checkout is `open`
- no broader billing permissions

### Provider
- no new pricing or checkout-line write workflow by default

Security intent:
- multi-line checkout remains a front-desk operational refinement, not a broader financial subsystem

## 12. Backend Test Plan

### Checkout creation and default line behavior
- starting checkout still creates only one checkout session per appointment
- starting checkout creates exactly one default checkout line
- the default line uses the Sprint 8 default fee when present
- the default line uses the Sprint 8 fallback description/amount when no fee default exists

### Line model behavior
- checkout line can store description, amount, sequence, and optional service fee
- negative line amount is rejected
- line ordering by sequence works as expected
- cross-practice service fee assignment is rejected if enforced

### Total computation
- session total equals the sum of line amounts
- adding a second line updates session total
- editing a line amount updates session total
- removing a line updates session total

### Manual edit preservation
- line selection from `service_fee_id` can prefill description and amount
- description can still be manually edited afterward
- amount can still be manually edited afterward
- later fee configuration changes do not rewrite existing line values

### State and payment preservation
- line edits are blocked when checkout is not `open`
- payment actions still work unchanged against the computed total
- `paid` still records full payment against the current total
- `payment_due` still records zero payment

### Boundary preservation
- multi-line checkout does not change appointment `visit_status`
- multi-line checkout does not change `needs_follow_up`
- multi-line checkout does not change encounter data
- multi-line checkout does not introduce invoice or accounting behavior

## 13. Acceptance Shape For This Slice

Sprint 9 should be considered successful when:
- a closed appointment starts one checkout session
- that checkout session starts with one default line
- front desk can add one or two more simple lines if needed
- checkout total updates from the line amounts
- payment actions continue to work without any new financial concepts

Nothing else should be required.

## 14. Explicit Non-Goals For Sprint 9

Do not expand Sprint 9 into:
- invoicing
- accounting entries
- taxes
- discount workflows
- refunds
- partial payments
- package redemption
- memberships
- claims
- portal flows
- gateway work
- quantity or unit-price logic
- inventory linkage
- rebooking logic
- encounter-linked charging rules

## 15. Recommended Next Decision After Sprint 9

If this slice proves useful, the next decision should still remain deliberate:
- either keep the checkout-line model small and operational
- or later decide whether real clinic pressure justifies a more formal billing layer

That later decision should not be made by default.

The burden of proof should remain on proven operational friction rather than architecture ambition.
