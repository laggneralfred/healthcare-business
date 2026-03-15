# Sprint 6 Handoff

Status:
- Sprint 6 is implemented through the current narrow post-visit follow-up marker slice
- This handoff freezes the appointment-side follow-up posture before deciding whether the next real need is rebooking or simply preserving the lightweight marker

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

## 3. Sprint 6 Scope

Sprint 6 added one minimal appointment-side follow-up marker after visit closure.

The supported workflow is now:
- `Lead Inquiry -> Create Patient -> Create Appointment -> Intake / Consent Readiness -> Patient completes pre-visit forms -> Start Visit -> Open / Reuse Encounter in modal -> Review readiness / open intake-consent if needed -> Record encounter documentation -> Complete Visit -> Close Visit -> Mark / Clear Needs Follow-Up`

Sprint 6 intentionally stayed narrow:
- no encounter changes
- no SOAP structure
- no diagnosis or problem lists
- no billing, checkout, invoices, or payments
- no rebooking logic
- no task assignment
- no reminders
- no dashboards or queues
- no portal or security redesign

## 4. Appointment Visit Lifecycle Currently Supported

`hc_scheduling` now supports a compact appointment lifecycle with a minimal post-visit coordination marker.

Current appointment lifecycle and coordination posture:
- visit lifecycle remains on `hc.appointment`
- appointment remains the workflow hub
- encounter remains a lightweight linked documentation record
- post-visit follow-up is represented by one boolean marker instead of a broader operational system

Current appointment actions:
- `Start Visit`
- `Complete Visit`
- `Close Visit`
- `Mark Needs Follow-Up`
- `Clear Follow-Up`

## 5. `visit_status` Values And Meaning

Current `visit_status` values:
- `scheduled`
  - default state before the visit begins
- `in_progress`
  - visit has started and encounter entry is underway
- `completed`
  - visit has been completed from the appointment side
- `closed`
  - visit has been operationally closed from the appointment side after completion

Sprint 6 intentionally keeps the lifecycle small and explicit.

## 6. Start Visit Behavior

Current `Start Visit` behavior:
- available from the appointment form
- requires:
  - `intake_status = complete`
  - `consent_status = complete`
- if readiness is incomplete, raises a clear `UserError`
- if readiness is complete:
  - sets appointment `visit_status = in_progress`
  - opens or reuses the linked encounter in a modal

This preserves the appointment-as-hub workflow and keeps encounter entry lightweight.

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

This preserves the current separation of concerns:
- appointment owns lifecycle
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

This is intentionally an operational close, not a billing or rebooking trigger.

## 9. `needs_follow_up` Behavior

Sprint 6 adds:
- `needs_follow_up` on `hc.appointment`

Current meaning:
- `False`
  - no follow-up marker is currently set
- `True`
  - the appointment has been marked as needing a post-visit follow-up action later

This is intentionally just a marker.

It does not imply:
- rebooking logic
- task assignment
- reminders
- billing
- queueing

## 10. Mark / Clear Needs Follow-Up Behavior

Current follow-up actions:
- `action_mark_needs_follow_up()`
- `action_clear_follow_up()`

Behavior:
- both actions only work when `visit_status == closed`
- if `visit_status` is not `closed`, a clear `UserError` is raised
- if allowed:
  - `Mark Needs Follow-Up` sets `needs_follow_up = True`
  - `Clear Follow-Up` sets `needs_follow_up = False`
- both remain non-modal state actions on the appointment
- both stay on the appointment

This keeps the follow-up step deliberately lightweight and operational.

## 11. Explicit Note: The Follow-Up Marker Does Not Affect Encounter

The Sprint 6 follow-up marker does not modify the linked encounter.

Specifically:
- it does not change encounter `status`
- it does not change encounter `completed_on`
- it does not create or reopen encounter content
- it does not add any new encounter workflow

This is intentional.

Sprint 6 adds a front-desk coordination marker without widening the encounter subsystem.

## 12. Relationship To The Frozen Lightweight Encounter Workflow

Sprint 6 continues to preserve the frozen Sprint 3 encounter posture.

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
- appointment owns lifecycle progression
- encounter remains the documentation record
- `Open Encounter` from appointment opens in a modal
- `Start Visit` uses the same modal encounter open/reuse behavior
- `Complete Visit` updates the encounter to `complete`
- `Close Visit` leaves the encounter unchanged
- `needs_follow_up` and its actions leave the encounter unchanged

## 13. Current Role / Access Posture Preserved

### Owner
- full operational access across Sprint 1 through Sprint 6 workflow
- can manage appointment lifecycle, readiness, encounter flow, and the follow-up marker

### Front Desk
- operational access to appointment, intake, consent, and encounter workflow
- can start visits, complete visits, close visits, and mark or clear follow-up

### Provider
- remains appointment-centric
- can work within the appointment-linked encounter posture already established
- does not gain a broader security redesign
- does not take on patient-facing token-share workflow

## 14. Automated Tests Currently Present

### `hc_scheduling`
Backend `TransactionCase` tests now cover:
- `Start Visit` blocked when readiness is incomplete
- `Start Visit` sets `in_progress` and opens/reuses encounter
- `Complete Visit` requires an encounter
- `Complete Visit` sets appointment `completed` and encounter `complete`
- `Close Visit` blocked unless the appointment is already `completed`
- `Close Visit` sets appointment `closed` without changing the encounter
- follow-up actions blocked unless the appointment is `closed`
- follow-up actions mark and clear the boolean without changing encounter data

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
- `hc_scheduling`: 8 tests
- `hc_encounter`: 11 tests
- `hc_intake`: 5 tests
- `hc_consent`: 5 tests

Current combined clinic result:
- total: 19 tests
- result: `0 failed, 0 error(s)`

## 15. Makefile / Test Commands Currently Available

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
make test-scheduling
make test-encounter
make test-intake
make test-consent
make test-core
make test-clinic
make test-clinic-summary
make restart-odoo
```

Validated current tooling note:
- the project `Makefile` now includes a dedicated `test-scheduling` target for `hc_scheduling`
- `test-clinic` and `test-clinic-summary` now use the scheduling-inclusive clinic scope: `hc_scheduling,hc_encounter,hc_intake,hc_consent`
- `logs/test-clinic.log` is the raw summary log artifact written by `test-clinic-summary`
- this is a documentation and tooling-posture update only; Sprint 6 product behavior remains frozen
- no application code, model/view/workflow behavior, or user-facing scope changed

`test-clinic-summary` currently:
- runs the combined clinic backend command defined in the current `Makefile`
- saves the full raw output to `logs/test-clinic.log`
- prints the `odoo.tests.stats:` and `odoo.tests.result:` summary lines afterward

## 16. Browser Verification Checklist

### Visit lifecycle visibility
1. Open an appointment.
2. Confirm `Visit Status` is visible.
3. Confirm `Needs Follow-Up` is visible.
4. Confirm new appointments start as:
   - `Visit Status = Scheduled`
   - `Needs Follow-Up = False`

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

### Follow-up marker behavior
1. On an appointment that is not `Closed`, click `Mark Needs Follow-Up`.
2. Confirm a clear error appears.
3. On an appointment that is not `Closed`, click `Clear Follow-Up`.
4. Confirm a clear error appears.
5. On an appointment already in `Closed`, click `Mark Needs Follow-Up`.
6. Confirm `Needs Follow-Up` becomes checked.
7. Click `Clear Follow-Up`.
8. Confirm `Needs Follow-Up` becomes unchecked.
9. Reopen the encounter and confirm encounter data did not change.

### Overall workflow sanity
1. Confirm Sprint 2 intake and consent token flows still match `SPRINT_2_HANDOFF.md`.
2. Confirm Sprint 3 encounter behavior still matches `SPRINT_3_HANDOFF.md`.
3. Confirm Sprint 4 appointment start/complete behavior still matches `SPRINT_4_HANDOFF.md`.
4. Confirm Sprint 5 close-visit behavior still matches `SPRINT_5_HANDOFF.md`.
5. Confirm no billing, checkout, rebooking, tasking, reminders, or expanded charting behavior has been introduced.

## 17. Known Intentional Caveats / Out Of Scope Items

These remain intentionally excluded after Sprint 6:
- billing linkage
- checkout
- invoices
- payments
- rebooking workflow
- follow-up workflow beyond the boolean marker
- task assignment
- reminders
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

## 18. Clear Next Decision Point

Sprint 6 is now at a clean pause point.

The next phase should stay deliberate and avoid both premature encounter expansion and early billing work.

Good next decision areas:

### Option A: rebooking planning
- decide whether the clinic really needs a narrow next-step rebooking flow
- if chosen, keep it appointment-centric and operational
- do not jump straight into a broad scheduling or patient-engagement subsystem

### Option B: keep the lightweight marker without adding more workflow yet
- preserve `needs_follow_up` as a simple signal
- wait until a clearer operational need emerges before adding rebooking or coordination depth

What should not happen next by default:
- more encounter fields without a deliberate charting decision
- SOAP drift
- billing or checkout drift

Recommendation:
- keep `hc_encounter` frozen
- decide explicitly whether rebooking is a true product need now
- if not, keep the lightweight follow-up marker and stop there until operational pressure justifies a new slice
