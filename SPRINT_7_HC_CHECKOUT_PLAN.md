# Sprint 7 Planning Note: `hc_checkout`

Status:
- Planning only. No implementation work is authorized from this document.
- This note starts from the frozen Sprint 6 baseline.
- `Close Visit` remains unchanged.
- The slice stays intentionally narrow and self-pay only.

## 1. Planning Goal

Add the smallest possible financial step after a visit is closed.

Target outcome:
- a closed appointment can move into one lightweight checkout record
- checkout records whether the patient paid now or still owes payment
- the appointment continues to act as the workflow hub
- the encounter remains untouched

This is not a full billing phase.

## 2. Frozen Baseline Preserved

Sprint 7 planning must preserve the current Sprint 6 posture:
- `Close Visit` remains an operational close only
- checkout is not triggered automatically by `Close Visit`
- appointment remains the hub
- encounter remains a lightweight documentation record
- `needs_follow_up` remains separate from financial handling

Current workflow becomes:
- `Lead Inquiry -> Create Patient -> Create Appointment -> Intake / Consent -> Start Visit -> Encounter -> Complete Visit -> Close Visit -> Start Checkout`

## 3. In-Scope Slice

One new module only:
- `hc_checkout`

Smallest supported flow:
- one checkout session per closed appointment
- `Start Checkout` action from appointment
- manual self-pay recording only
- tender types limited to:
  - `cash`
  - `card`
  - `payment_due`

Operational meaning:
- `cash` and `card` mean the clinic collected full payment outside or alongside the system
- `payment_due` means the clinic closed the visit but did not collect payment during checkout

## 4. Out Of Scope By Default

This planning note explicitly excludes:
- invoices
- accounting journals
- account moves
- taxes
- insurance claims
- claim status tracking
- patient portal
- payment gateway integration
- packages
- gift certificates
- retail items
- inventory effects
- discounts
- refunds
- partial payments
- payment allocations
- statements
- automated receipts
- email or SMS payment messaging
- rebooking linkage
- follow-up automation
- checkout launch from encounter
- more than one checkout session per appointment

## 5. Module Boundary

`hc_checkout` should depend only on the minimum existing workflow spine needed for this slice:
- `hc_practice_core`
- `hc_patient_core`
- `hc_scheduling`

It should not depend on:
- `hc_encounter` for ownership of financial state
- Odoo accounting modules for the first slice
- any payment processor integration

Boundary rule:
- checkout owns the financial record
- appointment may display checkout summary fields
- encounter stays unchanged

## 6. Proposed Models And Fields

### New model: `hc.checkout.session`

Purpose:
- the single financial wrapper for one closed appointment

Required fields:
- `name`
  - simple sequence or human-readable reference
- `appointment_id`
  - required
  - unique
- `patient_id`
  - required
  - copied from appointment
- `practitioner_id`
  - optional if present on appointment
  - copied for reporting convenience
- `appointment_start`
  - copied from appointment for context
- `state`
  - required selection
- `charge_label`
  - required
  - simple text label for the visit charge
- `amount_total`
  - required monetary
- `amount_paid`
  - monetary
  - expected to equal `amount_total` only when fully paid
- `tender_type`
  - selection:
    - `cash`
    - `card`
- `started_on`
  - datetime when checkout session is created
- `paid_on`
  - datetime when payment is marked collected
- `payment_note`
  - optional free text for terminal note or front-desk reference
- `notes`
  - optional internal note
- `currency_id`
  - required monetary currency

Behavior notes:
- `appointment_id` must enforce one checkout session per appointment
- `patient_id` and `practitioner_id` should be copied for record stability
- this first slice should not introduce a separate checkout line model
- the session itself carries one simple visit charge

Reason for no line model yet:
- one visit, one charge, one payment outcome is the narrowest credible self-pay slice
- line-level structure can be added later if retail, packages, or multi-line service logic becomes necessary

### Minimal appointment extension: `hc.appointment`

Appointment remains the workflow hub, but it does not own the financial record.

Add display and linkage fields only:
- `checkout_session_id`
  - readonly relation to the single checkout session
- `checkout_status`
  - readonly selection for appointment display
- `checkout_amount_total`
  - readonly monetary display
- `checkout_paid_on`
  - readonly datetime display
- `checkout_tender_type`
  - readonly display field

Field rule:
- these fields summarize checkout state for front-desk visibility
- the source of truth remains `hc.checkout.session`

## 7. State Definitions

### `hc.checkout.session.state`

Keep the state model as small as possible:

- `open`
  - checkout exists
  - payment outcome has not been finalized
  - amount and notes may still be edited

- `paid`
  - full payment was collected
  - tender type must be `cash` or `card`
  - `amount_paid` should equal `amount_total`
  - `paid_on` is set

- `payment_due`
  - payment was not collected during checkout
  - `tender_type` remains empty
  - `amount_paid` remains zero

No other states in this slice:
- no `draft`
- no `cancelled`
- no `partial`
- no `refunded`

### Appointment display state

For simplicity, appointment should display:
- `none`
  - no checkout started
- `open`
  - checkout started, not resolved
- `paid`
  - payment recorded
- `payment_due`
  - checkout completed without payment collection

## 8. Appointment Actions And Display Fields

### New appointment action: `Start Checkout`

Rules:
- visible only when `visit_status == closed`
- if no checkout session exists:
  - create one
  - open it
- if a checkout session already exists:
  - reopen the existing session

Important preserved behavior:
- `Start Checkout` does not modify `visit_status`
- `Start Checkout` does not reopen the encounter
- `Start Checkout` does not change `needs_follow_up`
- `Close Visit` remains unchanged and non-financial

### Appointment display block

Add a small readonly checkout summary area on the appointment form:
- `Checkout Status`
- `Checkout Amount`
- `Tender`
- `Paid On`

Display goal:
- front desk can tell from the appointment whether financial handling has happened
- providers do not need a broader billing workflow

## 9. Checkout Actions

Keep actions explicit and manual:

- `Mark Cash Paid`
  - allowed only from `open`
  - sets:
    - `state = paid`
    - `tender_type = cash`
    - `amount_paid = amount_total`
    - `paid_on = now`

- `Mark Card Paid`
  - allowed only from `open`
  - sets:
    - `state = paid`
    - `tender_type = card`
    - `amount_paid = amount_total`
    - `paid_on = now`

- `Mark Payment Due`
  - allowed only from `open`
  - sets:
    - `state = payment_due`
    - `amount_paid = 0`
    - `tender_type = empty`
    - `paid_on = empty`

No action in this slice should:
- split tenders
- record partial amounts
- connect to a card processor
- generate an invoice

## 10. View Outline

### Appointment form

Add:
- `Start Checkout` button in the appointment header or action area
- readonly checkout summary fields on the form
- optional smart button to open the linked checkout session once it exists

Do not add:
- invoice actions
- accounting widgets
- payment gateway controls
- checkout controls on the encounter form

### Checkout session form

Minimal layout:
- header
  - session reference
  - state badge
  - action buttons:
    - `Mark Cash Paid`
    - `Mark Card Paid`
    - `Mark Payment Due`
- context section
  - appointment
  - patient
  - practitioner
  - appointment date/time
- charge section
  - `charge_label`
  - `amount_total`
- payment section
  - `tender_type`
  - `amount_paid`
  - `paid_on`
  - `payment_note`
- internal notes
  - `notes`

### List/search posture

Keep this minimal:
- basic tree view for owner and front desk users
- simple filters:
  - `Open`
  - `Paid`
  - `Payment Due`
- no kanban
- no dashboard
- no report views

### Navigation posture

Default access should be from the appointment.

Optional minimal menu for operational staff:
- `Checkout Sessions`

If a menu is added, it should stay simple and operational, not accounting-oriented.

## 11. Access Posture

### Owner
- full read/write/create access to checkout sessions
- can use all checkout actions

### Front Desk
- full read/write/create access to checkout sessions
- can start checkout from appointment
- can mark paid or payment due

### Provider
- read-only visibility of checkout summary on appointment
- no checkout write actions by default
- no need for provider-owned checkout workflow in this slice

Security intent:
- checkout remains a front-desk operational responsibility
- provider workflow stays clinical and appointment-centric

## 12. Default Data Entry Posture

Keep charge entry simple:
- one `charge_label`
- one `amount_total`

Recommended default:
- prefill `charge_label` from appointment context if easy
- allow front desk to edit both fields

Do not require in this slice:
- service catalog setup
- product configuration
- appointment-type pricing logic

This keeps the first checkout slice usable even if service pricing is still handled informally.

## 13. Backend Test Plan

### Session creation and uniqueness
- starting checkout on a non-closed appointment raises a clear `UserError`
- starting checkout on a closed appointment creates one checkout session
- starting checkout again reopens the existing session instead of creating another
- unique appointment-to-checkout rule is enforced

### Appointment integration
- appointment `checkout_status` is `none` when no session exists
- appointment `checkout_status` becomes `open` after session creation
- appointment display fields reflect session amount, tender, and paid timestamp
- `Close Visit` behavior remains unchanged by the presence of checkout

### Payment actions
- `Mark Cash Paid` works only from `open`
- `Mark Cash Paid` sets `paid`, `cash`, full `amount_paid`, and `paid_on`
- `Mark Card Paid` works only from `open`
- `Mark Card Paid` sets `paid`, `card`, full `amount_paid`, and `paid_on`
- `Mark Payment Due` works only from `open`
- `Mark Payment Due` sets `payment_due` without a tender or payment timestamp

### Boundary preservation
- checkout actions do not modify appointment `visit_status`
- checkout actions do not modify `needs_follow_up`
- checkout actions do not modify the linked encounter
- checkout does not require encounter edits or encounter-driven launch paths

### Access posture
- owner and front desk users can create and update checkout sessions
- provider users cannot run checkout payment actions

## 14. Acceptance Shape For This Slice

This Sprint 7 slice should be considered successful when:
- a front-desk user can open a closed appointment
- click `Start Checkout`
- create or reopen one checkout session
- enter or confirm one visit charge
- mark the visit as paid by cash or card, or mark payment due
- return to the appointment and immediately see the financial summary

Nothing else should be required.

## 15. Explicit Non-Goals For Sprint 7

Do not expand Sprint 7 into:
- invoice generation
- posted accounting entries
- A/R workflows
- tax handling
- insurance or claims
- patient statements
- card-terminal integration
- online payments
- package credits
- memberships
- retail checkout
- discount workflows
- refund workflows
- partial-payment handling
- follow-up messaging
- retention workflows
- checkout analytics
- broader billing subsystem redesign

## 16. Recommended Next Decision After Sprint 7

If this slice proves operationally useful, the next decision should be narrow:
- either add a small line-item/service model for more structured pricing
- or add a minimal invoice layer in a separate later slice

That decision should be deferred until the clinic validates that the basic self-pay checkout step is actually used and stable.
