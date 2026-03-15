# Sprint 7 Handoff

Status:
- Sprint 7 is implemented through the current narrow self-pay checkout slice
- This handoff freezes the appointment-to-checkout posture after the frozen Sprint 6 baseline

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

## 3. Sprint 7 Scope

Sprint 7 adds one minimal post-close checkout step.

The supported workflow is now:
- `Lead Inquiry -> Create Patient -> Create Appointment -> Intake / Consent Readiness -> Patient completes pre-visit forms -> Start Visit -> Open / Reuse Encounter in modal -> Review readiness / open intake-consent if needed -> Record encounter documentation -> Complete Visit -> Close Visit -> Mark / Clear Needs Follow-Up -> Start Checkout -> Mark Cash Paid / Mark Card Paid / Mark Payment Due`

Sprint 7 intentionally stayed narrow:
- no encounter changes
- no changes to `Close Visit`
- no changes to `needs_follow_up`
- no invoice generation
- no accounting integration
- no taxes
- no claims
- no patient portal
- no payment gateway integration
- no refunds
- no partial payments
- no package logic
- no rebooking logic
- no reminders
- no dashboards or queues

## 4. Appointment Workflow Posture Preserved

The core workflow posture remains:
- appointment remains the workflow hub
- encounter remains the lightweight documentation record
- checkout becomes the financial record only after the visit is already `closed`
- checkout does not reopen or modify the encounter
- checkout does not replace the appointment lifecycle

Current appointment actions:
- `Start Visit`
- `Complete Visit`
- `Close Visit`
- `Mark Needs Follow-Up`
- `Clear Follow-Up`
- `Start Checkout`

## 5. `Close Visit` Behavior Remains Frozen

Current `Close Visit` behavior is unchanged from Sprint 6:
- available from the appointment form
- remains a non-modal state action
- only works when `visit_status == completed`
- if the appointment is not completed, raises a clear `UserError`
- if the appointment is completed:
  - sets appointment `visit_status = closed`
  - stays on the appointment

Sprint 7 does not turn `Close Visit` into a financial trigger.

Checkout remains a separate next step.

## 6. `Start Checkout` Behavior

Sprint 7 adds:
- `action_start_checkout()` on `hc.appointment`

Behavior:
- visible to owner and front desk users
- only available when `visit_status == closed`
- if the appointment is not `closed`, raises a clear `UserError`
- if no checkout session exists:
  - creates one checkout session
  - copies appointment context into it
  - opens the checkout form
- if a checkout session already exists:
  - reopens the same checkout session

This preserves:
- one checkout session per appointment
- appointment-as-hub workflow
- explicit operational control after visit closure

## 7. Appointment Checkout Summary Fields

Sprint 7 adds readonly checkout summary fields on `hc.appointment`:
- `checkout_status`
- `checkout_amount_total`
- `checkout_tender_type`
- `checkout_paid_on`

Current summary meanings:
- `none`
  - no checkout session exists yet
- `open`
  - checkout has started and payment outcome is unresolved
- `paid`
  - checkout has been marked paid by `cash` or `card`
- `payment_due`
  - checkout exists but payment was not collected during checkout

These fields are display-only on the appointment.

The source of truth remains the checkout session.

## 8. `hc.checkout.session` Model Currently Supported

Sprint 7 adds:
- `hc.checkout.session`

Current fields:
- `name`
- `appointment_id`
- `patient_id`
- `practitioner_id`
- `appointment_start`
- `state`
- `charge_label`
- `amount_total`
- `amount_paid`
- `tender_type`
- `started_on`
- `paid_on`
- `payment_note`
- `notes`
- `currency_id`

Current model posture:
- one checkout session per appointment
- checkout session can only be created for a `closed` appointment
- checkout copies patient, practitioner, and appointment timing context from the appointment
- checkout stores one simple visit charge
- checkout does not introduce line items
- checkout does not create invoices or accounting records

## 9. Checkout States

Current checkout states are intentionally limited to:
- `open`
  - checkout exists and payment outcome is still unresolved
- `paid`
  - full self-pay amount has been marked collected
- `payment_due`
  - payment was not collected during checkout

There are intentionally no states for:
- draft
- cancelled
- partial
- refunded

## 10. Checkout Payment Actions

Current payment actions:
- `Mark Cash Paid`
- `Mark Card Paid`
- `Mark Payment Due`

Behavior:
- all three actions only work when checkout state is `open`
- if checkout is not `open`, a clear `UserError` is raised

`Mark Cash Paid`:
- sets `state = paid`
- sets `tender_type = cash`
- sets `amount_paid = amount_total`
- sets `paid_on`

`Mark Card Paid`:
- sets `state = paid`
- sets `tender_type = card`
- sets `amount_paid = amount_total`
- sets `paid_on`

`Mark Payment Due`:
- sets `state = payment_due`
- clears `tender_type`
- sets `amount_paid = 0`
- clears `paid_on`

## 11. Explicit Boundary Notes

Sprint 7 checkout does not modify:
- appointment `visit_status`
- appointment `needs_follow_up`
- encounter `status`
- encounter `completed_on`
- encounter content

This is intentional.

Checkout adds the smallest financial wrapper after visit closure without widening the clinical workflow.

## 12. Access Posture

### Owner
- full operational access across Sprint 1 through Sprint 7 workflow
- can create, open, and update checkout sessions
- can use all checkout payment actions

### Front Desk
- operational access to appointment, intake, consent, encounter, and checkout workflow
- can start checkout from the appointment
- can use checkout payment actions

### Provider
- remains appointment-centric
- can see readonly checkout summary fields on the appointment
- does not get checkout write actions
- does not gain a broader billing workflow

## 13. Automated Tests Currently Present

### `hc_checkout`
Backend `TransactionCase` tests now cover:
- `Start Checkout` blocked unless the appointment is `closed`
- `Start Checkout` creates one checkout session
- `Start Checkout` reopens the existing checkout session
- checkout creation blocked unless the appointment is `closed`
- `Mark Cash Paid` sets paid state and updates appointment summary
- `Mark Card Paid` sets paid state and updates appointment summary
- `Mark Payment Due` sets due state without payment metadata
- payment actions blocked once checkout is no longer `open`
- front desk user can start checkout
- provider cannot update checkout sessions

Current direct module result from the recent run:
- `hc_checkout`: `0 failed, 0 error(s)`

### Previously frozen modules still preserved

`hc_scheduling` still covers:
- appointment lifecycle
- follow-up marker behavior

`hc_encounter` still covers:
- encounter creation and reopen behavior
- encounter field persistence
- encounter completion timestamp logic

`hc_intake` and `hc_consent` still preserve their existing readiness and token flows.

## 14. Test Commands Currently Available

### Direct Odoo test commands

Run checkout tests:

```bash
docker compose exec odoo odoo -d healthcare_dev -u hc_checkout --test-enable --test-tags /hc_checkout --http-port=8070 --stop-after-init
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

The current `Makefile` does not yet include a dedicated checkout test target.

For Sprint 7 checkout verification, use the direct Odoo test command above.

## 15. Validation Pass Completed

Documentation pass completed:
- Sprint 6 baseline reviewed
- Sprint 7 planning note reviewed
- implemented `hc_checkout` slice reviewed against both

Live application validation completed:
- verified the merged appointment form exposes checkout summary fields
- verified the merged appointment form exposes `Start Checkout` for a front desk user
- verified `Start Checkout` is not exposed to a provider user
- verified a closed appointment can create a checkout session through `action_start_checkout()`
- verified the created checkout session defaults to `open`
- verified marking checkout `cash` payment updates appointment summary to `paid`

Manual browser-click validation status:
- not completed in this terminal-only environment
- no local browser or browser automation runtime is available here
- no browser-only UI bug was identified during live view and action validation

## 16. Browser Verification Checklist For A Future Manual Pass

### Appointment form visibility
1. Open a closed appointment as an owner or front desk user.
2. Confirm `Start Checkout` is visible.
3. Confirm the readonly checkout summary block is visible.
4. Confirm the summary initially shows:
   - `Checkout Status = None`
   - empty tender
   - empty paid date

### Start Checkout behavior
1. On an appointment that is not `Closed`, confirm `Start Checkout` is not available to owner or front desk.
2. On a `Closed` appointment, click `Start Checkout`.
3. Confirm a checkout form opens.
4. Confirm the checkout shows:
   - linked appointment
   - patient
   - practitioner
   - appointment start
   - default `State = Open`
5. Close the checkout form or navigate back to the appointment.
6. Click `Start Checkout` again.
7. Confirm the same checkout session reopens instead of creating a second one.

### Checkout payment actions
1. On an `Open` checkout, set a test amount.
2. Click `Mark Cash Paid`.
3. Confirm:
   - `State = Paid`
   - `Tender = Cash`
   - `Amount Paid = Amount Total`
   - `Paid On` is filled
4. Repeat on another closed appointment using `Mark Card Paid`.
5. Repeat on another closed appointment using `Mark Payment Due`.
6. Confirm `payment_due` leaves tender and paid date empty.

### Appointment summary reflection
1. Return to the appointment after each checkout action.
2. Confirm the summary block reflects:
   - `Open` after checkout creation
   - `Paid` after cash or card payment
   - `Payment Due` after due-state action
3. Confirm `Visit Status` remains `Closed`.
4. Confirm `Needs Follow-Up` remains unchanged.

### Encounter boundary
1. Reopen the linked encounter after checkout activity.
2. Confirm encounter content did not change.
3. Confirm encounter `Status` and `Completed On` remain unchanged.

## 17. Known Intentional Caveats / Out Of Scope Items

These remain intentionally excluded after Sprint 7:
- invoices
- accounting integration
- taxes
- insurance claims
- patient statements
- payment gateway integration
- refunds
- partial payments
- package credits
- retail items
- inventory effects
- rebooking workflow
- reminders
- dashboards or queues
- SOAP structure
- diagnosis or problem lists
- patient portal
- advanced security redesign
- AI

Product decisions intentionally preserved:
- appointment remains the workflow hub
- encounter remains lightweight and calm
- checkout begins only after a closed appointment
- checkout owns the financial record
- encounter remains untouched by checkout
- state-only actions still stay close to the appointment workflow
- provider workflow remains appointment-centric

## 18. New Frozen Baseline

Sprint 7 is now at a clean pause point.

The frozen baseline is:
- Sprint 6 appointment lifecycle and follow-up marker behavior preserved
- one minimal self-pay checkout session per closed appointment
- one explicit appointment-side checkout entry point
- one minimal financial outcome layer: `cash`, `card`, or `payment_due`

What should not happen next by default:
- invoice drift
- accounting drift
- payment-gateway drift
- package or retail drift
- encounter expansion through checkout

Recommendation:
- preserve this checkout slice as the new frozen baseline
- only widen financial scope if real clinic pressure proves that invoices, packages, or accounting depth are actually needed
