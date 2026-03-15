# Sprint 9 Handoff

Status:
- Sprint 9 is implemented through the current narrow multi-line checkout slice
- This handoff freezes the Sprint 9 checkout posture after the frozen Sprint 8 baseline

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

## 3. Sprint 9 Scope

Sprint 9 adds the smallest possible multi-line checkout layer inside `hc_checkout`.

The supported workflow is now:
- `Lead Inquiry -> Create Patient -> Create Appointment -> Intake / Consent Readiness -> Patient completes pre-visit forms -> Start Visit -> Open / Reuse Encounter in modal -> Review readiness / open intake-consent if needed -> Record encounter documentation -> Complete Visit -> Close Visit -> Mark / Clear Needs Follow-Up -> Start Checkout -> One default checkout line appears -> Front desk may add or edit a few lines -> Mark Cash Paid / Mark Card Paid / Mark Payment Due`

Sprint 9 intentionally stayed narrow:
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
- no rebooking coupling

## 4. Appointment Workflow Posture Preserved

The core workflow posture remains:
- appointment remains the workflow hub
- encounter remains the lightweight documentation record
- checkout still begins only after a visit is already `closed`
- checkout remains the financial record
- pricing still improves defaults only
- Sprint 9 only widens checkout from one charge to a small set of lines

Current appointment actions remain:
- `Start Visit`
- `Complete Visit`
- `Close Visit`
- `Mark Needs Follow-Up`
- `Clear Follow-Up`
- `Start Checkout`

Sprint 9 adds no new appointment action.

## 5. `Close Visit` Behavior Remains Frozen

Current `Close Visit` behavior is unchanged from Sprint 8:
- available from the appointment form
- remains a non-modal state action
- only works when `visit_status == completed`
- if the appointment is not completed, raises a clear `UserError`
- if the appointment is completed:
  - sets appointment `visit_status = closed`
  - stays on the appointment

Sprint 9 does not turn `Close Visit` into a pricing or billing trigger.

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

Sprint 9 does not change:
- one checkout session per appointment
- checkout states
- checkout payment actions

## 7. `hc.checkout.line` Model Currently Supported

Sprint 9 adds:
- `hc.checkout.line`

Current fields:
- `checkout_session_id`
- `sequence`
- `description`
- `amount`
- `currency_id`
- optional `service_fee_id` when `hc_pricing` is installed

Current model posture:
- one charge record under one checkout session
- ordered by `sequence, id`
- non-negative amount only
- line editing allowed only while checkout is `open`
- no quantity
- no unit price
- no tax metadata
- no discount fields
- no refund behavior

## 8. Checkout Session Posture After Sprint 9

`hc.checkout.session` remains the owning financial record for one appointment.

Current behavior:
- one checkout session per appointment
- one2many `checkout_line_ids`
- line content is now the source of charge content
- payment fields on the session remain the source of payment-state tracking

Current line-based total rule:
- `amount_total` is synchronized from the sum of checkout-line amounts

Current header-summary rule:
- the session `charge_label` remains present for compatibility
- the session `charge_label` follows the first checkout line description
- payment actions still operate on the session total

## 9. Historical Compatibility And Backfill Behavior

Sprint 9 preserves existing Sprint 7 and Sprint 8 checkout history.

Current compatibility rule:
- new checkout sessions still start with one default line
- that default line is created from the session's current `charge_label` and `amount_total`

Current backfill rule:
- if an existing checkout session has no lines, Sprint 9 creates exactly one default line from the historical session values
- this preserves historical checkout data without requiring invoice or migration complexity

Operational result:
- no historical single-charge checkout data is discarded
- old sessions remain representable in the new line-based model

## 10. Pricing Integration Preserved But Not Expanded

Sprint 9 reuses the frozen Sprint 8 pricing-default posture.

Current pricing behavior:
- `hc.service.fee` remains the pricing-default record
- appointment type `default_service_fee_id` still provides startup defaults
- if practical pricing integration is present, checkout lines may carry optional `service_fee_id`
- selecting a fee on an open line may prefill:
  - `description`
  - `amount`

Current preserved manual-edit rule:
- line `description` remains manually editable
- line `amount` remains manually editable

Current stability rule:
- copied checkout values stay stable after creation
- later changes to service-fee configuration do not retroactively rewrite historical checkout values

Sprint 9 does not turn pricing into:
- billing logic
- tax logic
- package logic
- membership logic

## 11. Checkout States And Payment Actions Remain Frozen

Sprint 9 does not change checkout states.

Current states remain:
- `open`
- `paid`
- `payment_due`

Sprint 9 does not change payment actions.

Current payment actions remain:
- `Mark Cash Paid`
- `Mark Card Paid`
- `Mark Payment Due`

Current state/write rule:
- checkout lines can be created, edited, reordered, or removed only while checkout state is `open`
- once checkout is `paid` or `payment_due`, lines become readonly

## 12. Explicit Boundary Notes

Sprint 9 multi-line checkout does not modify:
- appointment `visit_status`
- appointment `needs_follow_up`
- encounter `status`
- encounter `completed_on`
- encounter content
- checkout payment-state semantics
- checkout state names
- checkout payment action names

This is intentional.

Sprint 9 adds a narrow line-item layer only.

## 13. UI Surface Currently Added

### Checkout form
- minimal `Checkout Lines` one2many section on the checkout form
- Odoo 19 `list` view, not deprecated `tree`
- inline editing only while checkout state is `open`

Current visible columns:
- `sequence`
- `description`
- `amount`
- optional `service_fee_id` when pricing is installed

### Session summary area
- `amount_total`
- payment fields
- payment actions

### Appointment form
- no new appointment actions
- existing readonly checkout summary still reflects the session total

No invoice, accounting, or payment-allocation UI was added.

## 14. Access Posture

### Owner
- retains full checkout access
- retains full pricing configuration access

### Front Desk
- can create and edit checkout lines while checkout is `open`
- can use optional service-fee selection on open checkout lines
- cannot widen checkout into accounting behavior

### Provider
- remains appointment-centric
- does not gain broader billing workflow

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
- payment actions preserving existing state semantics
- front desk checkout access
- provider denial posture

### `hc_pricing`
Backend `TransactionCase` tests now cover:
- negative service fee price rejection
- cross-practice appointment type fee assignment rejection
- checkout prefill from appointment type default service fee
- Sprint 7 and Sprint 8 fallback behavior when no default service fee exists
- line-level fee selection refreshing line and session defaults
- explicit manual line values winning when written alongside fee selection
- copied checkout values remaining stable after fee configuration changes later
- cross-practice checkout-line fee assignment rejection
- fee changes blocked when checkout is not `open`
- front desk read-only fee access posture
- front desk fee selection on open checkout lines

Current combined result from the latest run:
- `hc_checkout`: `0 failed, 0 error(s)`
- `hc_pricing`: `0 failed, 0 error(s)`

### Previously frozen modules still preserved

`hc_scheduling`, `hc_encounter`, `hc_intake`, and `hc_consent` continue to preserve their frozen baseline behaviors from Sprint 8.

## 16. Test Commands Currently Available

### Combined Odoo test command

Run the current Sprint 9 checkout and pricing verification:

```bash
docker compose exec odoo odoo -d healthcare_dev -u hc_checkout,hc_pricing --test-enable --test-tags /hc_checkout,/hc_pricing --http-port=8070 --stop-after-init
```

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

The validated test-tooling posture remains:
- `Makefile` includes `test-scheduling`
- `test-clinic` and `test-clinic-summary` use the scheduling-inclusive clinic scope
- `logs/test-clinic.log` is the summary log artifact

Checkout and pricing verification still uses the direct Odoo test commands above.

## 17. Validation Pass Completed

Documentation pass completed:
- Sprint 8 handoff reviewed as the previous authoritative implemented baseline
- Sprint 9 checkout-lines plan reviewed as the planning authority
- implemented Sprint 9 checkout slice reviewed against both

Implementation-scope verification completed:
- `hc_checkout` adds one new checkout-line model only
- checkout totals now follow line amounts
- historical single-charge sessions are preserved through default-line representation and backfill
- pricing remains a defaulting layer only
- no extra scope beyond the planned Sprint 9 multi-line checkout slice was identified

Current direct verification completed:
- latest combined `hc_checkout` plus `hc_pricing` test run passed with `0 failed, 0 error(s)`
- code inspection found no implemented invoice, accounting, tax, discount, refund, partial-payment, package, membership, claims, portal, gateway, inventory, rebooking, or visit-workflow scope beyond the planned Sprint 9 slice

## 18. Known Intentional Caveats / Out Of Scope Items

These remain intentionally excluded after Sprint 9:
- invoices
- accounting integration
- taxes
- insurance claims
- discounts
- refunds
- partial payments
- packages
- memberships
- payment gateway integration
- patient portal
- rebooking workflow
- retail items
- inventory effects
- dashboards or queues
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
- service fees may prefill checkout defaults
- encounter remains unchanged
- `needs_follow_up` remains unchanged

## 19. New Frozen Baseline

Sprint 9 is now at a clean pause point.

The frozen baseline is:
- Sprint 8 checkout and pricing posture preserved
- one minimal multi-line checkout layer added inside `hc_checkout`
- one minimal `hc.checkout.line` model
- line-based checkout totals
- historical single-charge checkout sessions safely represented through default-line backfill
- existing payment actions and payment-state semantics unchanged

What should not happen next by default:
- invoice drift
- accounting drift
- tax drift
- discount, refund, or partial-payment drift
- package or membership drift
- rebooking drift
- encounter or visit-workflow drift

Recommendation:
- preserve Sprint 9 as the new frozen baseline
- only widen checkout scope if a specific operational problem or a later deliberate sprint requires it
