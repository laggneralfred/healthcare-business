# Sprint 12 Handoff

Status:
- Sprint 12 is implemented through the current narrow patient-statement slice
- This handoff freezes the Sprint 12 patient-account-summary posture after the frozen Sprint 11 baseline

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

## 3. Sprint 12 Scope

Sprint 12 adds the smallest possible patient-level unpaid statement inside `hc_checkout`.

The supported workflow is now:
- `Lead Inquiry -> Create Patient -> Create Appointment -> Intake / Consent Readiness -> Patient completes pre-visit forms -> Start Visit -> Open / Reuse Encounter in modal -> Review readiness / open intake-consent if needed -> Record encounter documentation -> Complete Visit -> Close Visit -> Mark / Clear Needs Follow-Up -> Start Checkout -> Mark Payment Due where needed -> Open Patient -> Print Patient Statement`

Sprint 12 intentionally stayed narrow:
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
- no rebooking coupling

## 4. Appointment Workflow Posture Preserved

The core workflow posture remains:
- appointment remains the workflow hub
- encounter remains the lightweight documentation record
- checkout still begins only after a visit is already `closed`
- checkout remains the financial record
- pricing still improves defaults only
- Sprint 12 only adds a patient-level unpaid summary for existing checkout records

Current appointment actions remain:
- `Start Visit`
- `Complete Visit`
- `Close Visit`
- `Mark Needs Follow-Up`
- `Clear Follow-Up`
- `Start Checkout`

Sprint 12 adds no new appointment action.

## 5. `Close Visit` Behavior Remains Frozen

Current `Close Visit` behavior is unchanged from Sprint 11:
- available from the appointment form
- remains a non-modal state action
- only works when `visit_status == completed`
- if the appointment is not completed, raises a clear `UserError`
- if the appointment is completed:
  - sets appointment `visit_status = closed`
  - stays on the appointment

Sprint 12 does not turn `Close Visit` into a billing or statement trigger.

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

Sprint 12 does not change:
- one checkout session per appointment
- checkout states
- checkout payment actions
- line-driven totals

## 7. Existing Checkout Summary And Payment-Due Behavior Preserved

Sprint 10 `Checkout Summary` remains implemented and unchanged.

Sprint 11 `Payment Due` document remains implemented and unchanged.

Current preserved behavior:
- `Checkout Summary` still works for `open`, `paid`, and `payment_due`
- `Payment Due` still applies only to `payment_due`
- paid summary behavior still shows tender type and `paid_on` when relevant
- payment-due document still uses existing `payment_note` when present

Sprint 12 does not replace or widen those outputs.

## 8. Patient Statement Added

Sprint 12 adds:
- one `Patient Statement` report/output anchored to `res.partner`

Current access posture:
- available from the patient UI
- intended for owner and front desk users
- informational only

Current contents included:
- practice
- patient
- unpaid checkout sessions in `payment_due`
- appointment context for each included checkout
- per-session totals
- patient-level total due
- existing `payment_note` when present
- lightweight line summaries from existing checkout lines

Current behavior:
- report includes only checkout sessions in `payment_due`
- report excludes `open` and `paid` checkout sessions
- report does not create a new record
- report does not mutate checkout state or payment data
- action is blocked when the patient has no unpaid checkout sessions

## 9. Checkout Model Posture Remains Narrow

`hc.checkout.session` remains the owning financial record for one appointment.

Current preserved behavior:
- one checkout session per appointment
- one2many `checkout_line_ids`
- `amount_total` remains line-driven
- session payment fields remain the source of payment-state tracking
- existing multi-line checkout behavior remains unchanged

Sprint 12 does not add:
- a patient statement model
- an invoice model
- an accounting model
- due dates
- receivable balances

## 10. Pricing Integration Remains Frozen

Sprint 12 reuses the frozen Sprint 8 through Sprint 11 pricing posture.

Current pricing behavior remains:
- `hc.service.fee` remains the pricing-default record
- appointment type `default_service_fee_id` still provides startup defaults
- checkout lines may carry optional `service_fee_id`
- copied checkout values stay stable after creation

Sprint 12 does not widen pricing into:
- billing logic
- tax logic
- package logic
- membership logic

## 11. Checkout States And Payment Actions Remain Frozen

Sprint 12 does not change checkout states.

Current states remain:
- `open`
- `paid`
- `payment_due`

Sprint 12 does not change payment actions.

Current payment actions remain:
- `Mark Cash Paid`
- `Mark Card Paid`
- `Mark Payment Due`

Current patient-statement rule:
- printing is read-only
- printing does not alter `state`
- printing does not alter `amount_total`
- printing does not alter `tender_type`
- printing does not alter `paid_on`
- printing does not alter line content

## 12. Explicit Boundary Notes

Sprint 12 patient-statement behavior does not modify:
- appointment `visit_status`
- appointment `needs_follow_up`
- encounter `status`
- encounter `completed_on`
- encounter content
- checkout payment-state semantics
- checkout state names
- checkout payment action names

This is intentional.

Sprint 12 adds one patient-level unpaid summary output only.

## 13. UI Surface Currently Added

### Patient UI
- `Print Patient Statement` action from the patient form
- one printable/report-style patient-level unpaid summary for the current patient

### Existing checkout UI
- `Checkout Summary` remains present and unchanged
- `Payment Due` remains present and unchanged

### Appointment form
- no new appointment action
- no statement button added to appointment

## 14. Access Posture

### Owner
- can print any patient statement already visible through current access rules

### Front Desk
- can print patient statements for patients and checkout sessions they can access operationally

### Provider
- remains appointment-centric
- does not gain broader billing workflow through Sprint 12

## 15. Automated Tests Currently Present

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
- payment-due print action blocked unless checkout state is `payment_due`
- patient statement rendering for unpaid sessions only
- patient statement action blocked when no unpaid checkout sessions exist
- front desk access to the payment-due document
- front desk access to the patient statement
- payment actions preserving existing state semantics
- front desk checkout access
- provider denial posture

Current direct module result from the latest run:
- `hc_checkout`: `0 failed, 0 error(s)`

### Previously frozen modules still preserved

`hc_pricing`, `hc_scheduling`, `hc_encounter`, `hc_intake`, and `hc_consent` continue to preserve their frozen baseline behaviors from Sprint 11.

## 16. Test Commands Currently Available

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

Checkout patient-statement verification still uses the direct Odoo test command above.

## 17. Validation Pass Completed

Implementation pass completed:
- Sprint 11 handoff reviewed as the previous authoritative implemented baseline
- Sprint 12 patient-statement plan reviewed as the planning authority
- implemented Sprint 12 patient-statement slice reviewed against both

Implementation-scope verification completed:
- `hc_checkout` adds one patient-level unpaid summary output only
- existing checkout summary behavior remains unchanged
- existing payment-due behavior remains unchanged
- no new financial model was introduced
- no invoice, accounting, tax, delivery-channel, or workflow scope was introduced
- no extra scope beyond the planned Sprint 12 patient-statement slice was identified

Current direct verification completed:
- latest direct `hc_checkout` module test run passed with `0 failed, 0 error(s)`
- code inspection found no implemented invoice, accounting, tax, discount, refund, partial-payment, claim, portal, gateway, email, SMS, package, or visit-workflow scope beyond the planned Sprint 12 slice

## 18. Known Intentional Caveats / Out Of Scope Items

These remain intentionally excluded after Sprint 12:
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
- encounter remains unchanged
- `needs_follow_up` remains unchanged

## 19. New Frozen Baseline

Sprint 12 is now at a clean pause point.

The frozen baseline is:
- Sprint 11 checkout, pricing, and document posture preserved
- one patient-level unpaid summary added inside `hc_checkout`
- one report/output for patient-level `payment_due` checkout summaries
- no new financial or billing model
- existing payment actions and payment-state semantics unchanged

What should not happen next by default:
- invoice drift
- accounting drift
- tax drift
- statement-family drift beyond this narrow patient summary
- messaging or portal delivery drift
- rebooking drift
- encounter or visit-workflow drift

Recommendation:
- preserve Sprint 12 as the next candidate frozen baseline
- only widen patient-statement or financial scope if a specific operational need or later deliberate sprint requires it
