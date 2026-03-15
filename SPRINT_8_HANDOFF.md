# Sprint 8 Handoff

Status:
- Sprint 8 is implemented through the current narrow structured pricing-default slice
- This handoff freezes the Sprint 8 pricing posture after the frozen Sprint 7 baseline

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

## 3. Sprint 8 Scope

Sprint 8 adds one minimal structured pricing layer that improves checkout defaults.

The supported workflow is now:
- `Lead Inquiry -> Create Patient -> Create Appointment -> Intake / Consent Readiness -> Patient completes pre-visit forms -> Start Visit -> Open / Reuse Encounter in modal -> Review readiness / open intake-consent if needed -> Record encounter documentation -> Complete Visit -> Close Visit -> Mark / Clear Needs Follow-Up -> Start Checkout -> Suggested Service Fee Default -> Manual review/edit -> Mark Cash Paid / Mark Card Paid / Mark Payment Due`

Sprint 8 intentionally stayed narrow:
- no change to appointment lifecycle
- no change to `Close Visit`
- no change to `needs_follow_up`
- no encounter changes
- no invoice generation
- no accounting integration
- no taxes
- no claims
- no packages
- no memberships
- no discounts
- no refunds
- no partial payments
- no patient portal
- no payment gateway integration
- no multi-line checkout
- no rebooking coupling

## 4. Appointment Workflow Posture Preserved

The core workflow posture remains:
- appointment remains the workflow hub
- encounter remains the lightweight documentation record
- checkout still begins only after a visit is already `closed`
- checkout remains the financial record
- pricing only improves checkout defaults
- pricing does not change the visit workflow

Current appointment actions remain:
- `Start Visit`
- `Complete Visit`
- `Close Visit`
- `Mark Needs Follow-Up`
- `Clear Follow-Up`
- `Start Checkout`

Sprint 8 adds no new appointment action.

## 5. `Close Visit` Behavior Remains Frozen

Current `Close Visit` behavior is unchanged from Sprint 7:
- available from the appointment form
- remains a non-modal state action
- only works when `visit_status == completed`
- if the appointment is not completed, raises a clear `UserError`
- if the appointment is completed:
  - sets appointment `visit_status = closed`
  - stays on the appointment

Sprint 8 does not turn `Close Visit` into a pricing or billing trigger.

## 6. `Start Checkout` Behavior Remains Frozen

Current `Start Checkout` behavior remains:
- visible to owner and front desk users
- only available when `visit_status == closed`
- if no checkout session exists:
  - creates one checkout session
  - opens the checkout form
- if a checkout session already exists:
  - reopens the same checkout session

Sprint 8 does not change:
- one checkout session per appointment
- checkout states
- checkout payment actions

## 7. `hc.service.fee` Model Currently Supported

Sprint 8 adds:
- `hc.service.fee`

Current fields:
- `name`
- `practice_id`
- `active`
- `default_price`
- `short_description`
- `currency_id`

Current model posture:
- owner-facing configuration record
- practice-aware fee default
- non-negative default price only
- no tax metadata
- no package linkage
- no insurance metadata
- no pricing complexity beyond one default amount

## 8. Appointment Type Pricing Link

Sprint 8 adds:
- `default_service_fee_id` on `hc.appointment.type`

Current behavior:
- field is optional
- field must belong to the same practice as the appointment type
- appointment type remains scheduling-oriented
- pricing ownership remains in `hc_pricing`

This creates a narrow bridge from scheduling to checkout defaults without turning visit types into billing records.

## 9. Checkout Pricing Fields And Behavior

Sprint 8 adds:
- `service_fee_id` on `hc.checkout.session`

Current behavior:
- optional
- editable only while checkout state is `open`
- must belong to the same practice as the appointment

Current startup defaulting rule:
- when `Start Checkout` creates a session:
  - if the appointment type has a `default_service_fee_id`:
    - checkout copies that fee into `service_fee_id`
    - checkout copies fee `name` into `charge_label`
    - checkout copies fee `default_price` into `amount_total`
  - otherwise:
    - checkout preserves the Sprint 7 fallback defaults

Current open-session behavior:
- front desk may choose a `service_fee_id`
- selecting a fee may refresh:
  - `charge_label`
  - `amount_total`

Current preserved manual-edit rule:
- `charge_label` remains manually editable
- `amount_total` remains manually editable
- if explicit values are written at the same time as `service_fee_id`, those explicit values win

Current stability rule:
- checkout stores copied values
- later changes to the service fee record do not retroactively rewrite existing checkout sessions

## 10. Checkout States And Payment Actions Remain Frozen

Sprint 8 does not change checkout states.

Current states remain:
- `open`
- `paid`
- `payment_due`

Sprint 8 does not change payment actions.

Current payment actions remain:
- `Mark Cash Paid`
- `Mark Card Paid`
- `Mark Payment Due`

Sprint 8 pricing behavior does not widen checkout into:
- invoice logic
- accounting logic
- discount logic
- refund logic
- partial-payment logic

## 11. Explicit Boundary Notes

Sprint 8 pricing does not modify:
- appointment `visit_status`
- appointment `needs_follow_up`
- encounter `status`
- encounter `completed_on`
- encounter content
- checkout payment-state semantics

This is intentional.

Sprint 8 adds a structured defaulting layer only.

## 12. UI Surface Currently Added

### Owner-facing pricing configuration
- minimal `Service Fees` list view
- minimal `Service Fee` form view
- owner-facing configuration menu entry

### Appointment type configuration
- optional `Default Service Fee` field on appointment type list/form

### Checkout form
- optional `service_fee_id` field on the checkout form while the session is `open`
- fee selection sits near existing checkout charge fields

No other UI expansion was added.

## 13. Access Posture

### Owner
- can create, edit, and delete service fees
- can assign default service fees on appointment types
- retains full checkout access

### Front Desk
- can read service fees
- can use service fee selection on open checkout sessions
- cannot manage service-fee configuration by default

### Provider
- remains appointment-centric
- does not gain pricing configuration workflow
- does not gain broader billing behavior

## 14. Automated Tests Currently Present

### `hc_pricing`
Backend `TransactionCase` tests now cover:
- negative service fee price rejection
- cross-practice appointment type fee assignment rejection
- checkout prefill from appointment type default service fee
- Sprint 7 checkout fallback when no default service fee exists
- open checkout fee selection refreshing charge defaults
- explicit manual checkout values winning when written alongside fee selection
- copied checkout values remaining stable after fee configuration changes later
- cross-practice checkout fee assignment rejection
- fee changes blocked when checkout is not `open`
- front desk read-only fee access posture
- front desk fee selection on open checkout

Current direct module result from the latest run:
- `hc_pricing`: `0 failed, 0 error(s)`

### Previously frozen modules still preserved

`hc_checkout` still preserves:
- one checkout session per appointment
- checkout states:
  - `open`
  - `paid`
  - `payment_due`
- payment actions:
  - `Mark Cash Paid`
  - `Mark Card Paid`
  - `Mark Payment Due`

`hc_scheduling`, `hc_encounter`, `hc_intake`, and `hc_consent` continue to preserve their frozen baseline behaviors from Sprint 7.

## 15. Test Commands Currently Available

### Direct Odoo test commands

Run pricing tests:

```bash
docker compose exec odoo odoo -d healthcare_dev -u hc_pricing --test-enable --test-tags /hc_pricing --http-port=8070 --stop-after-init
```

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

The current `Makefile` still does not include dedicated Sprint 7 or Sprint 8 targets for:
- `hc_checkout`
- `hc_pricing`

For checkout and pricing verification, use the direct Odoo test commands above.

## 16. Validation Pass Completed

Documentation pass completed:
- Sprint 7 handoff reviewed as the authoritative implemented baseline
- Sprint 8 pricing plan reviewed as the planning authority
- implemented `hc_pricing` slice reviewed against both

Implementation-scope verification completed:
- `hc_pricing` adds one new pricing module only
- pricing adds one simple service-fee model
- pricing adds one optional appointment type default fee link
- pricing adds one optional checkout fee field and defaulting layer
- no extra scope beyond the planned Sprint 8 pricing slice was identified

Current direct verification completed:
- latest direct `hc_pricing` module test run passed with `0 failed, 0 error(s)`
- code inspection found no implemented invoice, accounting, tax, claims, package, membership, discount, refund, partial-payment, portal, gateway, inventory, or multi-line checkout scope in `hc_pricing`

## 17. Known Intentional Caveats / Out Of Scope Items

These remain intentionally excluded after Sprint 8:
- invoices
- accounting integration
- taxes
- insurance claims
- packages
- memberships
- discounts
- refunds
- partial payments
- payment gateway integration
- patient portal
- multi-line checkout
- retail items
- inventory effects
- rebooking workflow
- reminders
- dashboards or queues
- encounter expansion through pricing

Product decisions intentionally preserved:
- appointment remains the workflow hub
- lifecycle remains:
  - `scheduled`
  - `in_progress`
  - `completed`
  - `closed`
- optional post-close checkout remains narrow
- checkout owns the financial record
- pricing improves defaults only
- encounter remains unchanged
- `needs_follow_up` remains unchanged

## 18. New Frozen Baseline

Sprint 8 is now at a clean pause point.

The frozen baseline is:
- Sprint 7 checkout slice preserved
- one minimal structured pricing layer added through `hc_pricing`
- one practice-aware service-fee default model
- one optional appointment type pricing default
- one optional checkout fee selection field with copied defaults
- checkout values still manually editable

What should not happen next by default:
- invoice drift
- accounting drift
- discount or refund drift
- package or membership drift
- multi-line checkout drift
- encounter or visit-workflow drift

Recommendation:
- preserve Sprint 8 as the new frozen baseline
- only widen pricing or financial scope if real clinic pressure proves the need for a later deliberate sprint
