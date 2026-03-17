# Sprint 13 Handoff

Status:
- Sprint 13 is implemented through the current narrow late-payment capture slice
- This handoff freezes the Sprint 13 late-payment posture after the frozen Sprint 12 baseline

## 1. Project / Environment Summary

- Odoo Community 19
- Docker-based local development
- Database: `healthcare_dev`
- Project root: `~/healthcare-business`
- Custom addons root: `~/healthcare-business/addons`
- Mounted addons path in container: `/mnt/extra-addons`

## 2. Modules Currently In Play

### Sprint 1 foundation
- `hc_practice_core`
- `hc_patient_core`
- `hc_leads`
- `hc_scheduling`

### Sprint 2 modules
- `hc_intake`
- `hc_consent`

### Sprint 3 module
- `hc_encounter`

### Sprint 7 module
- `hc_checkout`

### Sprint 8 module
- `hc_pricing`

## 3. Sprint 13 Scope

Sprint 13 adds the smallest possible late-payment capture path inside `hc_checkout`.

The supported workflow is now:
- `Lead Inquiry -> Create Patient -> Create Appointment -> Intake / Consent Readiness -> Patient completes pre-visit forms -> Start Visit -> Open / Reuse Encounter in modal -> Review readiness / open intake-consent if needed -> Record encounter documentation -> Complete Visit -> Close Visit -> Mark / Clear Needs Follow-Up -> Start Checkout -> Mark Payment Due when needed -> Later collect cash or card payment on the same checkout session`

Sprint 13 intentionally stayed narrow:
- no change to appointment lifecycle
- no change to `Close Visit`
- no change to `needs_follow_up`
- no encounter changes
- no new financial model
- no invoice generation
- no accounting integration
- no taxes
- no discounts
- no refunds
- no partial payments
- no claim handling
- no portal
- no gateway integration
- no email or SMS delivery
- no packages
- no memberships
- no rebooking coupling

## 4. Appointment Workflow Posture Preserved

The core workflow posture remains:
- appointment remains the workflow hub
- encounter remains the lightweight documentation record
- checkout still begins only after a visit is already `closed`
- checkout remains the financial record
- pricing still improves defaults only
- Sprint 13 only adds a late full-payment transition for existing `payment_due` checkout sessions

Current appointment actions remain:
- `Start Visit`
- `Complete Visit`
- `Close Visit`
- `Mark Needs Follow-Up`
- `Clear Follow-Up`
- `Start Checkout`

Sprint 13 adds no new appointment action.

## 5. `Close Visit` Behavior Remains Frozen

Current `Close Visit` behavior is unchanged from Sprint 12:
- available from the appointment form
- remains a non-modal state action
- only works when `visit_status == completed`
- if the appointment is not completed, raises a clear `UserError`
- if the appointment is completed:
  - sets appointment `visit_status = closed`
  - stays on the appointment

Sprint 13 does not turn `Close Visit` into a billing or payment trigger.

## 6. `Start Checkout` Behavior Remains Frozen

Current `Start Checkout` behavior remains:
- visible to owner and front desk users
- only available when `visit_status == closed`
- if no checkout session exists:
  - creates one checkout session
  - creates one default checkout line
  - opens the checkout form
- if a checkout session already exists:
  - reopens the same checkout session

Sprint 13 does not change:
- one checkout session per appointment
- checkout states
- checkout payment actions from the `open` state
- line-driven totals

## 7. Existing Reporting Behavior Preserved

Sprint 10 `Checkout Summary` remains implemented and unchanged.

Sprint 11 `Payment Due` document remains implemented and unchanged.

Sprint 12 patient statement remains implemented and unchanged.

Current preserved behavior:
- `Checkout Summary` still works for `open`, `paid`, and `payment_due`
- `Payment Due` still applies only to `payment_due`
- patient statement still includes only `payment_due` sessions

Sprint 13 does not replace or widen those outputs.

## 8. Late-Payment Capture Added

Sprint 13 adds:
- `Collect Cash Payment`
- `Collect Card Payment`

Current access posture:
- available on `hc.checkout.session`
- visible only when checkout state is `payment_due`
- intended for owner and front desk users

Current behavior:
- allowed only when `state == payment_due`
- `Collect Cash Payment` sets:
  - `state = paid`
  - `tender_type = cash`
  - `paid_on`
  - `amount_paid = amount_total`
- `Collect Card Payment` sets:
  - `state = paid`
  - `tender_type = card`
  - `paid_on`
  - `amount_paid = amount_total`

Current guardrail:
- these actions do not reopen checkout to `open`
- these actions do not create a new payment record

## 9. Checkout Content And Pricing Posture Preserved

Sprint 13 keeps checkout content stable during late-payment capture.

Current preserved behavior:
- checkout lines are unchanged
- `amount_total` is unchanged
- `charge_label` is unchanged
- service-fee linkage/default data is unchanged
- payment actions only update payment-state fields

This is intentional.

## 10. Checkout Model Posture Remains Narrow

`hc.checkout.session` remains the owning financial record for one appointment.

Current preserved behavior:
- one checkout session per appointment
- one2many `checkout_line_ids`
- `amount_total` remains line-driven
- session payment fields remain the source of payment-state tracking
- existing multi-line checkout behavior remains unchanged

Sprint 13 does not add:
- a payment transaction model
- an invoice model
- an accounting model
- due dates
- receivable balances
- partial-payment data

## 11. Pricing Integration Remains Frozen

Sprint 13 reuses the frozen Sprint 8 through Sprint 12 pricing posture.

Current pricing behavior remains:
- `hc.service.fee` remains the pricing-default record
- appointment type `default_service_fee_id` still provides startup defaults
- checkout lines may carry optional `service_fee_id`
- copied checkout values stay stable after creation

Sprint 13 does not widen pricing into:
- billing logic
- tax logic
- package logic
- membership logic

## 12. Checkout States And Payment Actions Remain Frozen

Sprint 13 does not change checkout states.

Current states remain:
- `open`
- `paid`
- `payment_due`

Sprint 13 keeps the existing payment actions from `open`:
- `Mark Cash Paid`
- `Mark Card Paid`
- `Mark Payment Due`

Sprint 13 adds late-collection actions from `payment_due`:
- `Collect Cash Payment`
- `Collect Card Payment`

Current late-payment rule:
- late collection is read/write only on payment-state fields
- late collection does not alter `amount_total`
- late collection does not alter line content
- late collection does not alter charge labels

## 13. Explicit Boundary Notes

Sprint 13 late-payment behavior does not modify:
- appointment `visit_status`
- appointment `needs_follow_up`
- encounter `status`
- encounter `completed_on`
- encounter content
- checkout state names
- checkout payment-state semantics outside the allowed `payment_due -> paid` transition

This is intentional.

Sprint 13 adds one narrow late-payment transition only.

## 14. UI Surface Currently Added

### Checkout session UI
- `Collect Cash Payment` action from the checkout session UI
- `Collect Card Payment` action from the checkout session UI
- both visible only when checkout state is `payment_due`

### Existing UI preserved
- `Checkout Summary` remains present and unchanged
- `Payment Due` remains present and unchanged
- patient statement remains present and unchanged

### Appointment form
- no new appointment action
- no late-payment button added to appointment

## 15. Access Posture

### Owner
- can collect late payment on accessible `payment_due` checkout sessions

### Front Desk
- can collect late payment on accessible `payment_due` checkout sessions

### Provider
- remains appointment-centric
- does not gain broader billing workflow through Sprint 13

## 16. Automated Tests Currently Present

### `hc_checkout`
Backend `TransactionCase` tests now cover:
- `Start Checkout` blocked unless the appointment is `closed`
- create-or-reopen checkout behavior
- one checkout session per appointment
- default line creation when checkout starts
- line-based total updates
- line resequencing and deletion updating the total and header summary
- line edits blocked once checkout is not `open`
- negative line amount rejection
- historical backfill creating a default line for legacy single-charge sessions
- receipt report rendering for checkout session context
- receipt report rendering for a paid checkout with tender visibility
- payment-due report rendering for a payment-due checkout with note visibility
- patient statement rendering for unpaid sessions only
- late cash collection blocked unless session is `payment_due`
- late card collection blocked once session is no longer `payment_due`
- late card collection preserving checkout lines, totals, labels, and service-fee linkage
- late collection removing the session from the patient statement by state change only
- front desk access to late collection
- front desk access to existing payment-due and patient-statement outputs
- payment actions preserving existing state semantics
- provider denial posture

Current direct module result from the latest run:
- `hc_checkout`: `0 failed, 0 error(s)`

### Previously frozen modules still preserved

`hc_pricing`, `hc_scheduling`, `hc_encounter`, `hc_intake`, and `hc_consent` continue to preserve their frozen baseline behaviors from Sprint 12.

## 17. Test Commands Currently Available

### Direct Odoo test commands

Run checkout tests:

```bash
docker compose exec odoo odoo -d healthcare_dev -u hc_checkout --test-enable --test-tags /hc_checkout --http-port=8070 --stop-after-init
```

Run pricing tests:

```bash
docker compose exec odoo odoo -d healthcare_dev -u hc_pricing --test-enable --test-tags /hc_pricing --http-port=8070 --stop-after-init
```

Run scheduling tests:

```bash
docker compose exec odoo odoo -d healthcare_dev -u hc_scheduling --test-enable --test-tags /hc_scheduling --http-port=8070 --stop-after-init
```

Run encounter tests:

```bash
docker compose exec odoo odoo -d healthcare_dev -u hc_encounter --test-enable --http-port=8070 --stop-after-init
```

Run intake tests:

```bash
docker compose exec odoo odoo -d healthcare_dev -u hc_intake --test-enable --http-port=8070 --stop-after-init
```

Run consent tests:

```bash
docker compose exec odoo odoo -d healthcare_dev -u hc_consent --test-enable --http-port=8070 --stop-after-init
```

Note:
- `--http-port=8070` is used because the main Odoo service already occupies `8069`

### Makefile posture currently present

The validated test-tooling posture remains:
- `Makefile` includes `test-scheduling`
- `test-clinic` and `test-clinic-summary` use the scheduling-inclusive clinic scope
- `logs/test-clinic.log` is the summary log artifact

Checkout late-payment verification still uses the direct Odoo test command above.

## 18. Validation Pass Completed

Implementation pass completed:
- Sprint 12 handoff reviewed as the previous authoritative implemented baseline
- Sprint 13 late-payment plan reviewed as the planning authority
- implemented Sprint 13 late-payment slice reviewed against both

Implementation-scope verification completed:
- `hc_checkout` extends `hc.checkout.session` only
- late-payment actions are limited to the `payment_due` state
- existing summary, payment-due, and patient-statement behavior remains intact
- no new financial model was introduced
- no invoice, accounting, tax, delivery-channel, or workflow scope was introduced
- no extra scope beyond the planned Sprint 13 late-payment slice was identified

Current direct verification completed:
- latest direct `hc_checkout` module test run passed with `0 failed, 0 error(s)`
- code inspection found no implemented invoice, accounting, tax, discount, refund, partial-payment, claim, portal, gateway, email, SMS, package, membership, or visit-workflow scope beyond the planned Sprint 13 slice

## 19. Known Intentional Caveats / Out Of Scope Items

These remain intentionally excluded after Sprint 13:
- invoices
- accounting integration
- taxes
- discounts
- refunds
- partial payments
- claims
- insurance statement workflows
- packages
- memberships
- payment gateway integration
- patient portal
- email delivery
- SMS delivery
- due dates
- rebooking workflow
- encounter expansion through checkout

Product decisions intentionally preserved:
- appointment remains the workflow hub
- lifecycle remains:
  - `scheduled`
  - `in_progress`
  - `completed`
  - `closed`
- optional post-close checkout remains narrow
- one checkout session remains tied to one appointment
- checkout states remain:
  - `open`
  - `paid`
  - `payment_due`
- amount totals remain line-driven
- service fees may prefill checkout defaults
- printable checkout summary remains implemented
- printable payment-due document remains implemented
- patient-level unpaid summary remains implemented
- encounter remains unchanged
- `needs_follow_up` remains unchanged

## 20. New Frozen Baseline

Sprint 13 is now at a clean pause point.

The frozen baseline is:
- Sprint 12 checkout, pricing, and document posture preserved
- one narrow late-payment capture path added on existing `payment_due` checkout sessions
- no new financial or billing model
- existing payment actions and reporting surfaces preserved

What should not happen next by default:
- invoice drift
- accounting drift
- tax drift
- statement-family drift beyond the current narrow outputs
- messaging or portal delivery drift
- rebooking drift
- encounter or visit-workflow drift

Recommendation:
- preserve Sprint 13 as the next candidate frozen baseline
- only widen late-payment or financial scope if a specific operational need or later deliberate sprint requires it
