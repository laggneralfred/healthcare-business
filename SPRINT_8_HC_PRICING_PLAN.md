# Sprint 8 Planning Note: `hc_pricing`

Status:
- Planning only. No implementation work is authorized from this document.
- This note starts from the frozen Sprint 7 baseline.
- Sprint 7 checkout boundaries remain unchanged.
- The slice stays intentionally narrow and pricing-only.

## 1. Planning Goal

Add the smallest possible structured pricing layer that improves checkout defaults without widening checkout into invoicing or accounting.

Target outcome:
- owner can define a tiny list of practice-aware service fees
- checkout can prefill a better default charge label and amount
- front desk can still edit checkout values manually
- appointment remains the workflow hub
- encounter remains untouched

This is not a billing phase.

## 2. Frozen Sprint 7 Baseline Preserved

Sprint 8 planning must preserve the current Sprint 7 posture:
- appointment remains the workflow hub
- appointment lifecycle remains:
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
- checkout remains manual self-pay only

Current workflow would become:
- `Lead Inquiry -> Create Patient -> Create Appointment -> Intake / Consent -> Start Visit -> Encounter -> Complete Visit -> Close Visit -> Start Checkout -> Suggested Service Fee -> Manual review/edit -> Mark Cash Paid / Mark Card Paid / Mark Payment Due`

## 3. In-Scope Slice

One new module only:
- `hc_pricing`

Smallest supported scope:
- one simple practice-aware service/fee model
- optional default service/fee link from appointment type
- minimal checkout integration so checkout can prefill from a service/fee
- checkout `charge_label` and `amount_total` remain manually editable

Operational meaning:
- this slice improves pricing defaults
- this slice does not change the checkout boundary or payment behavior

## 4. Why This Should Be Separate From Appointment Types

`hc.appointment.type` already exists to support scheduling.

Sprint 8 should not silently turn appointment types into pricing records.

Recommended boundary:
- appointment type remains scheduling-oriented
- `hc_pricing` owns structured fee defaults
- appointment type may optionally point to a default fee for convenience
- checkout remains the place where the actual financial record is finalized

This avoids mixing schedule taxonomy with pricing ownership while still keeping the implementation small.

## 5. Out Of Scope By Default

This planning note explicitly excludes:
- invoices
- accounting journals
- account moves
- taxes
- insurance claims
- claim status tracking
- packages
- memberships
- retail items
- inventory effects
- discounts
- coupons
- refunds
- partial payments
- payment allocations
- patient statements
- patient portal
- payment gateway integration
- terminal integration
- subscriptions
- time-based rate calculation
- provider-specific compensation logic
- multi-line checkout
- service bundles
- automatic rebooking linkage
- encounter-driven pricing

## 6. Module Boundary

`hc_pricing` should depend only on the minimum modules needed for this slice:
- `hc_practice_core`
- `hc_scheduling`
- `hc_checkout`

It should not depend on:
- `hc_encounter`
- Odoo accounting modules
- payment integrations
- inventory modules

Boundary rule:
- `hc_pricing` owns structured fee defaults
- `hc_checkout` still owns the actual checkout record
- appointment continues to initiate checkout
- encounter stays unchanged

## 7. Proposed Models And Fields

### New model: `hc.service.fee`

Purpose:
- store a small practice-owned list of common visit/service fee defaults

Required fields:
- `name`
  - required
  - user-facing service or fee name
- `practice_id`
  - required
  - fee belongs to one practice
- `active`
  - default `True`
- `default_price`
  - required monetary
  - default suggested amount
- `short_description`
  - optional short text
- `currency_id`
  - required monetary currency

Recommended minimal behavior:
- ordering by active name or name
- practice-aware default for `practice_id`
- non-negative price validation

No additional pricing structure in this slice:
- no tax fields
- no SKU/code
- no duration pricing
- no package linkage
- no insurance metadata

### Minimal extension: `hc.appointment.type`

Add one optional field only:
- `default_service_fee_id`
  - many2one to `hc.service.fee`
  - must belong to the same practice

Purpose:
- provide a narrow default pricing suggestion for checkout startup
- keep scheduling and pricing loosely connected without merging the models

### Minimal extension: `hc.checkout.session`

Add one optional field:
- `service_fee_id`
  - many2one to `hc.service.fee`
  - editable only while checkout state is `open`

Integration rule:
- if the appointment type has a `default_service_fee_id`, checkout creation can prefill:
  - `service_fee_id`
  - `charge_label`
  - `amount_total`
- if front desk changes `service_fee_id` while checkout is `open`, checkout can refresh:
  - `charge_label`
  - `amount_total`

Important preserved behavior:
- `charge_label` remains manually editable
- `amount_total` remains manually editable
- payment actions remain unchanged

## 8. Defaulting And Edit Rules

### Startup defaulting

Smallest recommended defaulting rule:
- when `Start Checkout` creates a checkout session:
  - if appointment type has a default service fee:
    - copy fee into `service_fee_id`
    - prefill `charge_label` from fee `name`
    - prefill `amount_total` from fee `default_price`
  - otherwise:
    - keep existing Sprint 7 fallback behavior

### Manual selection in checkout

On an `open` checkout:
- front desk can choose a `service_fee_id`
- selecting a fee updates the current default values
- front desk may still manually edit `charge_label`
- front desk may still manually edit `amount_total`

### Guardrail

Sprint 8 should not introduce “hard binding” between the fee record and the checkout record.

Checkout should copy defaults, not depend on live pricing after the fact.

That means:
- changing a fee later should not retroactively rewrite old checkout sessions

## 9. Proposed UI Touchpoints

### Service fee configuration views

Add a minimal owner-facing config area for service fees:
- list view
- form view

Minimal fields shown:
- `name`
- `practice_id`
- `active`
- `default_price`
- optional `short_description`

### Appointment type form

Add one optional field:
- `Default Service Fee`

Purpose:
- let the practice tie a scheduling visit type to a likely checkout default

This should stay small and optional.

### Checkout form

Add one editable field while state is `open`:
- `service_fee_id`

Recommended placement:
- near `charge_label` and `amount_total`

Interaction goal:
- front desk can accept a suggested fee or switch to another fee quickly
- front desk can still override the copied charge text or amount

### Appointment form

No new appointment action is needed.

Keep appointment UI changes minimal:
- `Start Checkout` remains the only appointment-side checkout entry point
- no pricing controls should be added to the appointment itself in this slice

## 10. Access Posture

### Owner
- full create/read/write access to service fees
- can assign default service fees on appointment types
- retains existing checkout access

### Front Desk
- read access to service fees
- can use service fee selection from checkout
- should not manage fee configuration by default

### Provider
- no pricing configuration workflow by default
- no new pricing write access by default

Security intent:
- fee setup remains a practice-owner configuration concern
- operational checkout use remains front-desk friendly

## 11. Backend Test Plan

### `hc.service.fee` model behavior
- service fee can be created with name, practice, active flag, and default price
- negative `default_price` is rejected
- practice-aware defaulting works as expected

### Appointment type default linkage
- appointment type can store an optional default service fee
- cross-practice fee assignment is rejected

### Checkout creation defaulting
- starting checkout for a closed appointment with an appointment type default fee prefills:
  - `service_fee_id`
  - `charge_label`
  - `amount_total`
- starting checkout without a default fee preserves the Sprint 7 fallback behavior

### Checkout fee selection behavior
- selecting a service fee on an `open` checkout updates `charge_label` and `amount_total`
- `charge_label` can still be manually edited afterward
- `amount_total` can still be manually edited afterward
- changing fee selection does not create a second checkout session

### Boundary preservation
- pricing changes do not affect checkout state definitions
- pricing changes do not affect payment actions
- pricing changes do not affect appointment `visit_status`
- pricing changes do not affect `needs_follow_up`
- pricing changes do not affect encounter data

## 12. Acceptance Shape For This Slice

Sprint 8 should be considered successful when:
- owner can define a small fee catalog for one practice
- owner can optionally tie an appointment type to one default fee
- front desk starts checkout from a closed appointment
- checkout prefills a sensible charge label and amount when a default fee exists
- front desk can still change both values manually before payment handling

Nothing else should be required.

## 13. Explicit Non-Goals For Sprint 8

Do not expand Sprint 8 into:
- invoice generation
- accounting entries
- taxes
- claims
- package credit
- memberships
- discounts
- coupon rules
- refunds
- partial payments
- payment gateway work
- terminal work
- portal flows
- multi-line checkout
- retail or inventory logic
- provider compensation
- encounter-linked pricing logic
- scheduling redesign

## 14. Recommended Next Decision After Sprint 8

If this slice proves useful, the next decision should still stay narrow:
- either keep the single-fee defaulting model as-is
- or later add a very small multi-line/service selection layer in a separate sprint

That decision should not be made by default.

The burden of proof should remain on real operational friction rather than architecture ambition.
