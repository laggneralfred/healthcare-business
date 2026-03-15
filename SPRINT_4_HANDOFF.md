# Sprint 4 Handoff

Status:
- Sprint 4 is implemented through the current minimal appointment visit-flow slice set
- This handoff freezes the appointment-centric visit workflow before opening any broader post-visit or charting scope

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

## 3. Sprint 4 Scope

Sprint 4 focused on a small appointment visit-flow layer without expanding encounter structure.

The supported workflow is now:
- `Lead Inquiry -> Create Patient -> Create Appointment -> Intake / Consent Readiness -> Patient completes pre-visit forms -> Open Encounter -> Review readiness -> Open Intake / Open Consent if needed -> Record encounter documentation -> Start Visit -> Complete Visit`

Sprint 4 intentionally stayed narrow:
- no checkout, billing, invoices, or payments
- no SOAP structure
- no diagnosis or problem lists
- no encounter field expansion beyond the frozen Sprint 3 posture
- no dashboards or queues
- no portal or security redesign

## 4. Appointment Visit Flow Currently Supported

`hc_scheduling` now carries the smallest visit-state workflow on `hc.appointment`.

Current appointment behavior:
- appointment has a `visit_status`
- appointment has `Start Visit`
- appointment has `Complete Visit`
- appointment remains the workflow hub
- encounter entry from the appointment uses modal return-to-previous behavior
- state-only completion remains on the appointment itself

## 5. `visit_status` Values And Meaning

Current `visit_status` values:
- `scheduled`
  - default state before the visit begins
- `in_progress`
  - visit has started and encounter entry is underway
- `completed`
  - visit has been completed from the appointment side

Sprint 4 intentionally keeps this status posture minimal.

## 6. Start Visit Behavior

Current `Start Visit` behavior:
- available from the appointment form
- checks appointment readiness before the visit can begin
- requires both:
  - `intake_status = complete`
  - `consent_status = complete`
- if readiness is incomplete, raises a clear `UserError`
- if readiness is complete:
  - sets `visit_status = in_progress`
  - opens or reuses the linked encounter

Design intent preserved:
- visit start is a small workflow transition, not a new charting system

## 7. Complete Visit Behavior

Current `Complete Visit` behavior:
- available from the appointment form
- remains a non-modal state action
- requires an encounter already linked to the appointment
- if no encounter exists, raises a clear `UserError`
- if an encounter exists:
  - sets appointment `visit_status = completed`
  - sets linked encounter `status = complete`
  - relies on the encounter’s existing `write()` logic to fill `completed_on`

This keeps completion logic simple and avoids duplicating encounter completion mechanics.

## 8. Modal Encounter Behavior From Appointment

Current appointment-to-encounter UX:
- `Open Encounter` from the appointment opens the encounter form in a modal
- `Start Visit` opens or reuses the encounter in the same modal style
- save or discard returns to the appointment underneath
- `Complete Visit` does not open a modal and remains a state change on the appointment

This preserves the clinic UX rule established elsewhere:
- related record entry uses modal return-to-previous behavior
- state-only actions stay on the current record

## 9. Relationship To Existing Encounter Workflow

Sprint 4 intentionally builds around the frozen Sprint 3 encounter rather than expanding it.

`hc_encounter` remains lightweight and currently supports:
- `status`
- `encounter_date`
- `completed_on`
- `chief_concern`
- `visit_summary`
- `treatment_notes`
- `notes`
- readiness section:
  - `Intake Status`
  - `Consent Status`
- encounter shortcuts:
  - `Open Intake`
  - `Open Consent`

Current relationship between appointment and encounter:
- appointment owns visit-state progression
- encounter remains the lightweight documentation record
- appointment start/open actions reuse the same encounter create-or-reopen logic
- appointment completion uses existing encounter status completion behavior

## 10. Current Role / Access Posture Preserved

### Owner
- full operational access across Sprint 1 through Sprint 4
- can manage appointment, readiness, encounter, and visit-state workflow

### Front Desk
- operational access to appointment, intake, consent, and encounter workflow
- can start visits, open encounters, and complete visits

### Provider
- remains appointment-centric
- can access appointment-linked encounters through the existing posture
- does not gain a broader security redesign
- does not take on patient-facing token-share workflow

## 11. Automated Tests Currently Present

### `hc_scheduling`
Backend `TransactionCase` tests now cover:
- `Start Visit` blocked when readiness is incomplete
- `Start Visit` sets `in_progress` and opens/reuses encounter
- `Complete Visit` requires an encounter
- `Complete Visit` sets appointment `completed` and encounter `complete`

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

Current full clinic summary from recent runs:
- `hc_scheduling`: 6 tests
- `hc_encounter`: 11 tests
- `hc_intake`: 5 tests
- `hc_consent`: 5 tests
- total: 17 tests
- result: `0 failed, 0 error(s)`

## 12. Makefile / Test Commands Currently Available

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
- the project `Makefile` does not currently include a dedicated `hc_scheduling` target
- scheduling tests are available through the direct Odoo command above

`test-clinic-summary`:
- runs the combined clinic backend test command currently defined in the Makefile
- saves the full raw output to `logs/test-clinic.log`
- prints the `odoo.tests.stats:` and `odoo.tests.result:` summary lines afterward

## 13. Browser Verification Checklist

### Visit status flow
1. Open an appointment.
2. Confirm `Visit Status` is visible.
3. Confirm new appointments start as `Scheduled`.

### Start Visit readiness gating
1. Open an appointment with incomplete intake or consent.
2. Click `Start Visit`.
3. Confirm a clear error appears.
4. Confirm `Visit Status` remains `Scheduled`.

### Start Visit modal behavior
1. Complete intake and consent for the appointment.
2. Return to the appointment and click `Start Visit`.
3. Confirm `Visit Status` becomes `In Progress`.
4. Confirm the encounter opens in a modal dialog.
5. Save or discard and confirm you return to the appointment underneath.

### Open Encounter modal behavior
1. From the same appointment, click `Open Encounter`.
2. Confirm the same encounter opens in a modal dialog.
3. Save or discard and confirm you return to the appointment underneath.

### Complete Visit behavior
1. On an appointment without an encounter, click `Complete Visit`.
2. Confirm a clear error appears.
3. On an appointment with an encounter, click `Complete Visit`.
4. Confirm `Visit Status` becomes `Completed`.
5. Open the encounter and confirm:
   - encounter `Status` is `Complete`
   - `Completed On` is filled

### Overall workflow sanity
1. Confirm Sprint 2 intake and consent token flows still behave as documented in `SPRINT_2_HANDOFF.md`.
2. Confirm Sprint 3 encounter behavior still matches `SPRINT_3_HANDOFF.md`.
3. Confirm no billing, checkout, or expanded charting sections were introduced.

## 14. Known Intentional Caveats / Out Of Scope Items

These remain intentionally excluded after Sprint 4:
- checkout
- billing linkage
- invoices
- payments
- SOAP structure
- diagnosis or problem lists
- prescriptions
- attachments or document upload
- signatures
- dashboards or operational queues
- patient portal
- email or SMS automation
- advanced security redesign
- AI

Product decisions intentionally preserved:
- appointment stays the workflow hub
- encounter stays lightweight and calm
- modal return-to-previous behavior is used for related record entry
- state-only actions remain on the appointment
- intake and consent remain staff-managed with optional token-based patient completion
- provider workflow remains appointment-centric

## 15. Clear Next Decision Point

Sprint 4 is now at a clean stopping point.

The next phase should avoid expanding encounter prematurely.

Recommended decision frame:

### Option A: keep encounter frozen and move to a post-visit workflow area
- decide whether the next narrow slice should be something like:
  - visit wrap-up
  - post-visit follow-up marker
  - rebooking or next-step operational flow

### Option B: keep encounter frozen and improve front-desk operational flow
- focus on the appointment lifecycle from the scheduling/operations side
- avoid turning the encounter into an accidental charting subsystem

What should not happen next by default:
- more encounter fields without an explicit charting decision
- SOAP drift
- billing/checkout drift

Recommendation:
- keep `hc_encounter` frozen for now
- choose the next workflow area deliberately from the appointment or front-desk side rather than continuing ad hoc encounter expansion
