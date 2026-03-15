# Sprint 5 Handoff

Status:
- Sprint 5 is implemented through the current narrow front-desk operational flow slice
- This handoff freezes the appointment visit lifecycle before any post-visit, rebooking, or billing expansion

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

## 3. Sprint 5 Scope

Sprint 5 added one more appointment-side operational state beyond `completed`.

The supported workflow is now:
- `Lead Inquiry -> Create Patient -> Create Appointment -> Intake / Consent Readiness -> Patient completes pre-visit forms -> Start Visit -> Open / Reuse Encounter in modal -> Review readiness / Open Intake or Consent if needed -> Record encounter documentation -> Complete Visit -> Close Visit`

Sprint 5 intentionally stayed narrow:
- no new encounter fields
- no SOAP structure
- no diagnosis or problem lists
- no billing, checkout, invoices, or payments
- no follow-up or rebooking logic
- no dashboards or queues
- no portal or security redesign

## 4. Appointment Visit Lifecycle Currently Supported

`hc_scheduling` now supports a minimal appointment visit lifecycle that remains centered on the appointment record.

Current appointment lifecycle steps:
- `scheduled`
- `in_progress`
- `completed`
- `closed`

Current appointment actions:
- `Start Visit`
- `Complete Visit`
- `Close Visit`

Design posture preserved:
- appointment remains the workflow hub
- encounter remains a lightweight linked documentation record
- front-desk workflow advances from the appointment rather than from a broader charting or billing subsystem

## 5. `visit_status` Values And Meaning

Current `visit_status` values:
- `scheduled`
  - default state before visit work begins
- `in_progress`
  - visit has started and encounter entry is underway
- `completed`
  - visit has been completed from the appointment side
- `closed`
  - visit has been operationally closed from the appointment side after completion

Sprint 5 intentionally keeps the visit status posture minimal and appointment-centered.

## 6. Start Visit Behavior

Current `Start Visit` behavior:
- available from the appointment form
- requires both:
  - `intake_status = complete`
  - `consent_status = complete`
- if readiness is incomplete, raises a clear `UserError`
- if readiness is complete:
  - sets appointment `visit_status = in_progress`
  - opens or reuses the linked encounter in a modal

This keeps visit start lightweight and tied to readiness without opening larger workflow architecture.

## 7. Complete Visit Behavior

Current `Complete Visit` behavior:
- available from the appointment form
- remains a non-modal state action
- requires an encounter already linked to the appointment
- if no encounter exists, raises a clear `UserError`
- if an encounter exists:
  - sets appointment `visit_status = completed`
  - sets linked encounter `status = complete`
  - relies on the encounter’s existing logic to fill `completed_on`

This preserves a clean separation:
- appointment owns visit-state progression
- encounter owns its own completion timestamp behavior

## 8. Close Visit Behavior

Current `Close Visit` behavior:
- available from the appointment form
- remains a non-modal state action
- only works when `visit_status == completed`
- if the appointment is not completed, raises a clear `UserError`
- if the appointment is completed:
  - sets appointment `visit_status = closed`
  - stays on the appointment

Sprint 5 intentionally keeps this as a small operational state change only.

## 9. Explicit Note: Close Visit Does Not Change Encounter

`Close Visit` does not modify the linked encounter.

Specifically:
- it does not change encounter `status`
- it does not change encounter `completed_on`
- it does not create or reopen encounter content
- it does not add any new encounter workflow

This is intentional.

The appointment gets one additional operational state without widening the encounter subsystem.

## 10. Relationship To The Frozen Lightweight Encounter Workflow

Sprint 5 continues to build around the frozen Sprint 3 encounter rather than expanding it.

`hc_encounter` remains lightweight and currently supports:
- `status`
- `encounter_date`
- `completed_on`
- `chief_concern`
- `visit_summary`
- `treatment_notes`
- `notes`
- read-only readiness section:
  - `Intake Status`
  - `Consent Status`
- internal shortcuts:
  - `Open Intake`
  - `Open Consent`

Current relationship between appointment and encounter:
- appointment owns visit-state progression
- encounter remains the documentation record
- `Open Encounter` from the appointment opens in a modal
- `Start Visit` uses the same modal encounter open/reuse behavior
- `Complete Visit` updates the encounter to `complete`
- `Close Visit` leaves the encounter unchanged

## 11. Current Role / Access Posture Preserved

### Owner
- full operational access across Sprint 1 through Sprint 5 workflow
- can manage appointment lifecycle, readiness, and encounter workflow

### Front Desk
- operational access to appointment, intake, consent, and encounter workflow
- can start visits, complete visits, and close visits from the appointment

### Provider
- remains appointment-centric
- can work within the appointment-linked encounter posture already established
- does not gain a broader security redesign
- does not take on patient-facing token-share workflow

## 12. Automated Tests Currently Present

### `hc_scheduling`
Backend `TransactionCase` tests now cover:
- `Start Visit` blocked when readiness is incomplete
- `Start Visit` sets `in_progress` and opens/reuses encounter
- `Complete Visit` requires an encounter
- `Complete Visit` sets appointment `completed` and encounter `complete`
- `Close Visit` blocked unless the appointment is already `completed`
- `Close Visit` sets appointment `closed` without changing the encounter

### `hc_encounter`
Backend `TransactionCase` tests cover:
- encounter creation from appointment
- one-encounter-per-appointment reopen behavior
- notes and status persistence
- `visit_summary` persistence
- `chief_concern` persistence
- `treatment_notes` persistence
- `completed_on` following status
- encounter shortcut delegation to intake/consent appointment logic

### `hc_intake`
Backend `TransactionCase` tests cover:
- public intake submission marking complete
- empty public intake rejection
- stable access token generation

### `hc_consent`
Backend `TransactionCase` tests cover:
- public consent submission marking complete
- empty public consent rejection
- stable access token generation

Current direct module-level counts from recent runs:
- `hc_scheduling`: 6 tests
- `hc_encounter`: 11 tests
- `hc_intake`: 5 tests
- `hc_consent`: 5 tests

Current combined clinic result:
- total: 17 tests
- result: `0 failed, 0 error(s)`

## 13. Makefile / Test Commands Currently Available

### Direct Odoo test commands

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

Run combined clinic tests:

```bash
docker compose exec odoo odoo -d healthcare_dev -u hc_scheduling,hc_encounter,hc_intake,hc_consent --test-enable --test-tags /hc_scheduling,/hc_encounter,/hc_intake,/hc_consent --http-port=8070 --stop-after-init
```

Note:
- `--http-port=8070` is used because the main Odoo service already occupies `8069`

### Makefile targets currently present

From `~/healthcare-business`:

```bash
make test-encounter
make test-intake
make test-consent
make test-core
make test-clinic
make test-clinic-summary
make restart-odoo
```

Important current note:
- the project `Makefile` still does not include a dedicated `hc_scheduling` target
- the current `Makefile` `test-clinic` targets still reflect the earlier non-scheduling combined scope
- scheduling tests and the full current combined clinic run are available through the direct Odoo commands above

`test-clinic-summary` currently:
- runs the combined clinic backend command defined in the current `Makefile`
- saves the full raw output to `logs/test-clinic.log`
- prints the `odoo.tests.stats:` and `odoo.tests.result:` summary lines afterward

## 14. Browser Verification Checklist

### Visit lifecycle visibility
1. Open an appointment.
2. Confirm `Visit Status` is visible.
3. Confirm new appointments start as `Scheduled`.

### Start Visit behavior
1. Open an appointment with incomplete intake or consent.
2. Click `Start Visit`.
3. Confirm a clear error appears.
4. Confirm `Visit Status` remains `Scheduled`.
5. Complete intake and consent.
6. Click `Start Visit`.
7. Confirm `Visit Status` becomes `In Progress`.
8. Confirm the encounter opens in a modal.
9. Save or discard and confirm you return to the appointment underneath.

### Complete Visit behavior
1. On an appointment without an encounter, click `Complete Visit`.
2. Confirm a clear error appears.
3. On an appointment with an encounter, click `Complete Visit`.
4. Confirm `Visit Status` becomes `Completed`.
5. Open the encounter and confirm:
   - encounter `Status` is `Complete`
   - `Completed On` is filled

### Close Visit behavior
1. On an appointment that is not `Completed`, click `Close Visit`.
2. Confirm a clear error appears.
3. On an appointment already in `Completed`, click `Close Visit`.
4. Confirm `Visit Status` becomes `Closed`.
5. Reopen the encounter and confirm:
   - encounter `Status` is unchanged
   - `Completed On` remains intact

### Overall workflow sanity
1. Confirm Sprint 2 intake and consent token flows still match `SPRINT_2_HANDOFF.md`.
2. Confirm Sprint 3 encounter behavior still matches `SPRINT_3_HANDOFF.md`.
3. Confirm Sprint 4 appointment start/complete behavior still matches `SPRINT_4_HANDOFF.md`.
4. Confirm no billing, checkout, rebooking, or expanded charting behavior has been introduced.

## 15. Known Intentional Caveats / Out Of Scope Items

These remain intentionally excluded after Sprint 5:
- billing linkage
- checkout
- invoices
- payments
- follow-up workflow
- rebooking workflow
- dashboards or operational queues
- SOAP structure
- diagnosis or problem lists
- prescriptions
- attachments or document upload
- signatures
- patient portal
- email or SMS automation
- advanced security redesign
- AI

Product decisions intentionally preserved:
- appointment remains the workflow hub
- encounter remains lightweight and calm
- related record entry generally uses modal return-to-previous behavior
- state-only actions stay on the appointment
- intake and consent remain staff-managed with optional token-based patient completion
- provider workflow remains appointment-centric
- statuses stay small and explicit

## 16. Clear Next Decision Point

Sprint 5 is now at a clean pause point.

The next phase should stay deliberate and avoid both premature encounter expansion and early billing work.

Good next decision areas:

### Option A: post-visit follow-up flow
- define whether the clinic needs a narrow next-step marker after visit closure
- keep it appointment-centric
- do not open full rebooking yet unless explicitly chosen

### Option B: front-desk coordination flow
- improve how front desk tracks the next operational step after a closed visit
- keep it lightweight and workflow-oriented

### Option C: stay frozen until a clearer operational need emerges
- preserve the current stable workflow
- avoid speculative workflow growth

What should not happen next by default:
- more encounter fields without a deliberate charting decision
- SOAP drift
- billing or checkout drift

Recommendation:
- keep `hc_encounter` frozen
- choose the next workflow area deliberately from post-visit or front-desk operations
- do not open billing until there is a clear product decision and a separate scoped sprint
