# Sprint 3 Handoff

Status:
- Sprint 3 is implemented through the current minimal encounter slice set
- This handoff freezes the current encounter posture before any broader charting work

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

## 3. Sprint 3 Scope

Sprint 3 focused on opening the visit workflow without opening full charting.

The supported workflow is now:
- `Lead Inquiry -> Create Patient -> Create Appointment -> Intake / Consent Readiness -> Patient completes pre-visit forms -> Open Encounter -> Review readiness -> Open Intake / Open Consent if needed -> Record encounter documentation`

Sprint 3 intentionally stayed narrow:
- no SOAP structure
- no diagnosis or problem lists
- no billing, checkout, invoices, or payments
- no attachments or document upload
- no signatures
- no dashboards
- no portal architecture
- no advanced security redesign

## 4. What Was Implemented In `hc_encounter`

### Encounter foundation
- `hc.encounter` model added as the minimal start of visit documentation
- one encounter per appointment enforced at the model level
- encounter can be opened from the appointment form
- opening from an appointment reuses the existing encounter if present
- otherwise a new draft encounter is created from appointment context and opened

### Encounter documentation posture
- encounter remains intentionally small and calm
- no tabs or multi-section chart system
- no nested treatment structures
- no coding or billing linkage

### Encounter refinements added during Sprint 3
- read-only readiness visibility on the encounter form
- internal shortcuts from encounter to existing intake and consent workflows
- `completed_on` behavior tied to encounter status
- small structured text fields for lightweight documentation without full charting

## 5. Encounter Workflow Currently Supported

1. Staff schedules an appointment in `hc_scheduling`.
2. Intake and consent readiness are completed through the existing Sprint 2 workflow.
3. Staff or provider opens the appointment.
4. Staff or provider clicks `Open Encounter`.
5. Odoo opens the existing encounter tied to that appointment, or creates one if missing.
6. The encounter displays current intake and consent readiness.
7. Staff can use `Open Intake` or `Open Consent` from the encounter to review or continue those records.
8. Staff or provider records lightweight encounter documentation and marks the encounter complete when appropriate.

## 6. Encounter Fields Currently Supported

`hc.encounter` currently supports:
- `status`
- `encounter_date`
- `completed_on`
- `chief_concern`
- `visit_summary`
- `treatment_notes`
- `notes`

Linkage/context fields also present:
- `patient_id`
- `appointment_id`
- `practice_id`
- `practitioner_id`
- computed display `name`

Current status posture:
- `draft`
- `complete`

Current completion behavior:
- setting status to `complete` fills `completed_on`
- setting status back to `draft` clears `completed_on`

## 7. Readiness Visibility On Encounter

The encounter form shows a small read-only `Readiness` section with:
- `Intake Status`
- `Consent Status`

These values reflect the same practical readiness behavior already established in Sprint 2:
- appointment-linked intake/consent records are checked first
- patient-linked records without an appointment are used as fallback
- readiness stays minimal:
  - `Missing`
  - `Complete`

## 8. Encounter Shortcuts To Intake / Consent

The encounter form now includes:
- `Open Intake`
- `Open Consent`

These shortcuts intentionally reuse existing appointment-based internal logic rather than introducing separate encounter-specific creation rules.

Current behavior:
- `Open Intake` delegates to the linked appointment’s intake action
- `Open Consent` delegates to the linked appointment’s consent action
- existing internal reopen/create behavior from Sprint 2 remains intact

## 9. Current Role / Access Posture Preserved

### Owner
- full operational access across Sprint 1, Sprint 2, and Sprint 3 modules
- can open appointments, readiness workflow, and encounters

### Front Desk
- operational access to patient, appointment, intake, consent, and encounter workflow
- can open encounters from appointments
- can use encounter intake/consent shortcuts

### Provider
- remains appointment-centric
- can open and work with appointment-linked encounters
- does not gain a broader portal/security redesign
- does not become responsible for patient-facing token share actions

## 10. Automated Tests Currently Present

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

## 11. Makefile / Test Commands Currently Available

### Direct Odoo test commands

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

Run clinic tests:

```bash
docker compose exec odoo odoo -d healthcare_dev -u hc_encounter,hc_intake,hc_consent --test-enable --http-port=8070 --stop-after-init
```

Note:
- `--http-port=8070` is used because the main Odoo service already occupies `8069`

### Makefile targets from project root

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

`test-clinic-summary`:
- runs the full combined clinic backend tests
- saves the full raw output to `logs/test-clinic.log`
- prints the `odoo.tests.stats:` and `odoo.tests.result:` summary lines afterward

## 12. Browser Verification Checklist

### Encounter creation and reuse
1. Open an appointment as owner, front desk, or provider.
2. Click `Open Encounter`.
3. Confirm a new encounter opens if none exists.
4. Return to the same appointment and click `Open Encounter` again.
5. Confirm the same encounter reopens instead of creating another.

### Encounter field visibility
1. Confirm the encounter form shows:
   - `Status`
   - `Encounter Date`
   - `Completed On`
   - `Chief Concern`
   - `Visit Summary`
   - `Treatment Notes`
   - `Notes`
2. Confirm the linked record fields remain read-only.

### Readiness and shortcut flow
1. Confirm the encounter shows read-only `Intake Status`.
2. Confirm the encounter shows read-only `Consent Status`.
3. Click `Open Intake` and confirm the expected internal intake record opens.
4. Click `Open Consent` and confirm the expected internal consent record opens.

### Completion behavior
1. With encounter `Status = Draft`, confirm `Completed On` is empty.
2. Change `Status` to `Complete` and save.
3. Confirm `Completed On` is filled.
4. Change `Status` back to `Draft` and save.
5. Confirm `Completed On` is cleared.

### Overall workflow sanity
1. Confirm Sprint 2 intake and consent token flows still behave as documented in `SPRINT_2_HANDOFF.md`.
2. Confirm the encounter remains a calm single-form workflow and does not expose SOAP tabs, billing sections, or attachments.

## 13. Known Intentional Caveats / Out Of Scope Items

These remain intentionally excluded after Sprint 3:
- SOAP structure
- diagnosis or problem lists
- treatment coding or procedure lines
- prescriptions
- billing linkage
- checkout
- invoices
- payments
- attachments or document upload
- signatures
- chart tabs or multi-tab charting
- dashboards
- patient portal
- email or SMS automation
- advanced security redesign
- AI

Product decisions intentionally preserved:
- encounter remains lightweight and appointment-linked
- provider workflow remains appointment-centric
- intake and consent remain separate modules with separate staff/public workflows
- statuses stay minimal where practical
- calm small-clinic UX takes priority over broad architecture

## 14. Clear Next Decision Point

Sprint 3 is now at a natural pause point.

The next product decision should be explicit:

### Option A: keep encounter lightweight
- continue adding only a few carefully chosen structured fields
- avoid opening full charting
- preserve speed and simplicity for a small clinic workflow

### Option B: deliberately design a structured charting phase
- define whether the product should move into a true clinical note model
- decide the intended structure before implementing more fields
- if chosen, design the next phase as a separate scoped sprint rather than continuing ad hoc field growth

Recommendation:
- pause and choose deliberately before adding more encounter structure
- do not drift into accidental SOAP or billing scope without an explicit sprint decision
