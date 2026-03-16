# Sprint 10 Handoff

Status:
- Sprint 10 is implemented through the current narrow printable checkout summary slice
- This handoff freezes the Sprint 10 receipt posture after the frozen Sprint 9 baseline

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

## 3. Sprint 10 Scope

Sprint 10 adds the smallest possible printable checkout summary inside `hc_checkout`.

The supported workflow is now:
- `Lead Inquiry -> Create Patient -> Create Appointment -> Intake / Consent Readiness -> Patient completes pre-visit forms -> Start Visit -> Open / Reuse Encounter in modal -> Review readiness / open intake-consent if needed -> Record encounter documentation -> Complete Visit -> Close Visit -> Mark / Clear Needs Follow-Up -> Start Checkout -> Review or edit checkout lines -> Mark Cash Paid / Mark Card Paid / Mark Payment Due -> Print Checkout Summary`

Sprint 10 intentionally stayed narrow:
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
- no claims
- no packages
- no portal
- no gateway integration
- no email or SMS delivery
- no rebooking coupling

## 4. Appointment Workflow Posture Preserved

The core workflow posture remains:
- appointment remains the workflow hub
- encounter remains the lightweight documentation record
- checkout still begins only after a visit is already `closed`
- checkout remains the financial record
- pricing still improves defaults only
- Sprint 10 only adds a human-readable summary output for the existing checkout record

Current appointment actions remain:
- `Start Visit`
- `Complete Visit`
- `Close Visit`
- `Mark Needs Follow-Up`
- `Clear Follow-Up`
- `Start Checkout`

Sprint 10 adds no new appointment action.

## 5. `Close Visit` Behavior Remains Frozen

Current `Close Visit` behavior is unchanged from Sprint 9:
- available from the appointment form
- remains a non-modal state action
- only works when `visit_status == completed`
- if the appointment is not completed, raises a clear `UserError`
- if the appointment is completed:
  - sets appointment `visit_status = closed`
  - stays on the appointment

Sprint 10 does not turn `Close Visit` into a billing or receipt trigger.

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

Sprint 10 does not change:
- one checkout session per appointment
- checkout states
- checkout payment actions
- line-driven totals

## 7. Printable Checkout Summary Added

Sprint 10 adds:
- one `Checkout Summary` report/output for `hc.checkout.session`

Current access posture:
- available from the checkout session UI through the existing report/print surface
- bound directly to `hc.checkout.session`
- informational only

Current contents included:
- practice
- checkout identifier
- patient
- appointment context
- practitioner when present
- checkout lines
- `amount_total`
- payment state
- tender type when state is `paid`
- `paid_on` when state is `paid`

Current behavior:
- report works for `open`, `paid`, and `payment_due`
- report does not create a new record
- report does not mutate checkout state or payment data

## 8. Checkout Model Posture Remains Narrow

`hc.checkout.session` remains the owning financial record for one appointment.

Current preserved behavior:
- one checkout session per appointment
- one2many `checkout_line_ids`
- `amount_total` remains line-driven
- session payment fields remain the source of payment-state tracking
- existing multi-line checkout behavior remains unchanged

Sprint 10 does not add:
- a receipt model
- an invoice model
- an accounting model
- receipt numbering

## 9. Pricing Integration Remains Frozen

Sprint 10 reuses the frozen Sprint 8 and Sprint 9 pricing posture.

Current pricing behavior remains:
- `hc.service.fee` remains the pricing-default record
- appointment type `default_service_fee_id` still provides startup defaults
- checkout lines may carry optional `service_fee_id`
- copied checkout values stay stable after creation

Sprint 10 does not widen pricing into:
- billing logic
- tax logic
- package logic
- membership logic

## 10. Checkout States And Payment Actions Remain Frozen

Sprint 10 does not change checkout states.

Current states remain:
- `open`
- `paid`
- `payment_due`

Sprint 10 does not change payment actions.

Current payment actions remain:
- `Mark Cash Paid`
- `Mark Card Paid`
- `Mark Payment Due`

Current report rule:
- printing is read-only
- printing does not alter `amount_total`
- printing does not alter `tender_type`
- printing does not alter `paid_on`
- printing does not alter line content

## 11. Explicit Boundary Notes

Sprint 10 receipt behavior does not modify:
- appointment `visit_status`
- appointment `needs_follow_up`
- encounter `status`
- encounter `completed_on`
- encounter content
- checkout payment-state semantics
- checkout state names
- checkout payment action names

This is intentional.

Sprint 10 adds one summary output only.

## 12. UI Surface Currently Added

### Checkout session UI
- `Checkout Summary` report action from the checkout session UI
- one printable/report-style summary output for the current checkout session

### Appointment form
- no new appointment action
- no receipt button added to appointment

### Checkout list
- no scope expansion required beyond the existing checkout entry points

## 13. Access Posture

### Owner
- can print any checkout summary already visible through current access rules

### Front Desk
- can print checkout summaries for sessions they can access operationally

### Provider
- remains appointment-centric
- does not gain broader billing workflow through Sprint 10

## 14. Automated Tests Currently Present

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
- payment actions preserving existing state semantics
- front desk checkout access
- provider denial posture

Current direct module result from the latest run:
- `hc_checkout`: `0 failed, 0 error(s)`

### Previously frozen modules still preserved

`hc_pricing`, `hc_scheduling`, `hc_encounter`, `hc_intake`, and `hc_consent` continue to preserve their frozen baseline behaviors from Sprint 9.

## 15. Test Commands Currently Available

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

Checkout receipt verification still uses the direct Odoo test command above.

## 16. Validation Pass Completed

Implementation pass completed:
- Sprint 9 handoff reviewed as the previous authoritative implemented baseline
- Sprint 10 receipt plan reviewed as the planning authority
- implemented Sprint 10 receipt slice reviewed against both

Implementation-scope verification completed:
- `hc_checkout` adds one printable checkout summary output only
- no new financial model was introduced
- no invoice, accounting, tax, delivery-channel, or workflow scope was introduced
- no extra scope beyond the planned Sprint 10 receipt slice was identified

Current direct verification completed:
- latest direct `hc_checkout` module test run passed with `0 failed, 0 error(s)`
- code inspection found no implemented invoice, accounting, tax, discount, refund, partial-payment, package, claim, portal, gateway, email, SMS, rebooking, or visit-workflow scope beyond the planned Sprint 10 slice

## 17. Known Intentional Caveats / Out Of Scope Items

These remain intentionally excluded after Sprint 10:
- invoices
- accounting integration
- taxes
- discounts
- refunds
- partial payments
- insurance claims
- packages
- memberships
- payment gateway integration
- patient portal
- email delivery
- SMS delivery
- receipt numbering
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
- encounter remains unchanged
- `needs_follow_up` remains unchanged

## 18. New Frozen Baseline

Sprint 10 is now at a clean pause point.

The frozen baseline is:
- Sprint 9 checkout and pricing posture preserved
- one printable checkout summary added inside `hc_checkout`
- one report/output for `hc.checkout.session`
- no new financial or billing model
- existing payment actions and payment-state semantics unchanged

What should not happen next by default:
- invoice drift
- accounting drift
- tax drift
- discount, refund, or partial-payment drift
- messaging or portal delivery drift
- rebooking drift
- encounter or visit-workflow drift

Recommendation:
- preserve Sprint 10 as the new frozen baseline
- only widen receipt or financial scope if a specific operational need or later deliberate sprint requires it
