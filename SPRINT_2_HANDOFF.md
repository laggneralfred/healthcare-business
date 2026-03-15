# Sprint 2 Handoff

Status:
- Sprint 2 is complete and stable
- This handoff consolidates the current intake and consent state into one reference file

## 1. Project / Environment Summary

- Odoo Community 19
- Docker-based local development
- Database: `healthcare_dev`
- Project root: `~/healthcare-business`
- Custom addons root: `~/healthcare-business/addons`
- Mounted addons path in container: `/mnt/extra-addons`

## 2. Modules In Play

### Sprint 1 foundation
- `hc_practice_core`
- `hc_patient_core`
- `hc_leads`
- `hc_scheduling`

### Sprint 2 modules
- `hc_intake`
- `hc_consent`

## 3. Sprint 2 Scope

Sprint 2 focused on pre-visit readiness only.

The supported workflow is now:
- `Lead Inquiry -> Create Patient -> Patient record -> Create Appointment -> Intake / Consent Readiness -> Patient completes pre-visit forms -> Appointment ready for visit`

Sprint 2 intentionally stayed narrow:
- no portal
- no email or SMS automation
- no e-signature or legal-signature system
- no encounter charting depth
- no billing, checkout, invoices, or payments
- no packages
- no AI
- no advanced template builder
- no advanced permissions redesign

## 4. What Was Implemented In `hc_intake`

### Internal intake foundation
- `hc.intake.submission` and `hc.intake.template`
- `Intake Status` shown on patient and appointment
- `Record Intake` action from patient and appointment
- modal workflow for quick staff use
- latest intake record reopens instead of always opening a new blank record
- template defaulting and active-template validation
- meaningful validation so complete intake cannot be empty
- patient and appointment readiness remain minimal:
  - `Missing`
  - `Complete`

### Public intake-by-token
- staff can generate or retrieve a public intake link from patient or appointment context
- public page opens without login
- secure token is tied to one existing intake record
- patient can complete the existing intake content fields and submit them
- successful submit writes intake content, sets `status = complete`, and fills `submitted_on`
- re-opening the token after completion shows the closed/already-received state

## 5. What Was Implemented In `hc_consent`

### Internal consent foundation
- `hc.consent.record` and `hc.consent.template`
- `Consent Status` shown on patient and appointment
- `Record Consent` action from patient and appointment
- modal workflow for quick staff use
- latest consent record reopens instead of always opening a new blank record
- template defaulting and active-template validation
- meaningful validation so complete consent cannot be empty
- patient and appointment readiness remain minimal:
  - `Missing`
  - `Complete`

### Public consent-by-token
- staff can generate or retrieve a public consent link from patient or appointment context
- public page opens without login
- secure token is tied to one existing consent record
- patient can complete the existing consent content fields and submit them
- successful submit writes consent content, sets `status = complete`, and fills `signed_on`
- re-opening the token after completion shows the closed/already-received state

## 6. Public Token Flows Now Supported

### Intake token flow
1. Staff opens patient or appointment.
2. Staff clicks `Get Intake Link`.
3. Odoo reuses the latest linked intake record or creates a minimal missing one.
4. Odoo shows a small modal with the public intake URL.
5. Staff shares the link manually outside Odoo.
6. Patient opens the link without login and submits the intake.
7. The linked intake record becomes `Complete` and fills `submitted_on`.

### Consent token flow
1. Staff opens patient or appointment.
2. Staff clicks `Get Consent Link`.
3. Odoo reuses the latest linked consent record or creates a minimal missing one.
4. Odoo shows a small modal with the public consent URL.
5. Staff shares the link manually outside Odoo.
6. Patient opens the link without login and submits the consent.
7. The linked consent record becomes `Complete` and fills `signed_on`.

## 7. Role / Access Posture Preserved

### Owner
- full access to Sprint 1 and Sprint 2 workflow
- can manage intake and consent templates
- can record and share intake/consent links

### Front Desk
- operational access to patient, appointment, intake, and consent workflow
- can record intake and consent
- can generate and manually share public intake and consent links
- does not get broad new architecture or portal duties

### Provider
- remains appointment-centric
- can review intake and consent records in the existing posture
- does not gain patient-facing token-link actions
- does not gain a broader permissions redesign in Sprint 2

## 8. Exact Commands To Update Modules

Update the current Sprint 1 and Sprint 2 modules:

```bash
docker compose exec odoo odoo -d healthcare_dev -u hc_practice_core,hc_patient_core,hc_leads,hc_scheduling,hc_intake,hc_consent --stop-after-init
```

If Python/controller changes are not visible in the running server, restart Odoo:

```bash
docker compose restart odoo
```

## 9. Browser Verification Checklist

### Core Sprint 1 flow still intact
1. Create or open a lead inquiry.
2. Create a patient from the lead.
3. Create an appointment from the patient.
4. Confirm the appointment still opens and saves normally.

### Intake readiness
1. Open a patient and confirm `Intake Status` is visible.
2. Open an appointment and confirm `Intake Status` is visible.
3. Use `Record Intake` and confirm the modal opens and latest-record reopen still works.
4. Use `Get Intake Link` and confirm the intake link modal opens.
5. Open the public intake link without login.
6. Submit with empty content and confirm validation appears.
7. Submit with content and confirm success.
8. Reopen the patient or appointment and confirm intake readiness shows `Complete`.

### Consent readiness
1. Open a patient and confirm `Consent Status` is visible.
2. Open an appointment and confirm `Consent Status` is visible.
3. Use `Record Consent` and confirm the modal opens and latest-record reopen still works.
4. Use `Get Consent Link` and confirm the consent link modal opens.
5. Open the public consent link without login.
6. Submit with empty content and confirm validation appears.
7. Submit with content and confirm success.
8. Reopen the patient or appointment and confirm consent readiness shows `Complete`.

### Provider sanity
1. Log in as provider.
2. Confirm appointment access still works.
3. Confirm no patient-facing token-share action is exposed to the provider role.

## 10. Known Intentional Caveats / Out Of Scope Items

These are still intentionally excluded after Sprint 2:
- patient portal
- email automation
- SMS automation or reminders
- e-signature flow
- legal-signature subsystem
- identity verification
- document upload
- intake + consent packet workflow
- advanced template builder
- advanced record-rule redesign
- encounter charting depth
- SOAP structure
- diagnosis/problem lists
- checkout
- invoices
- payments
- packages
- AI

Product decisions intentionally preserved:
- intake and consent remain staff-managed, with optional patient-facing token completion
- statuses remain minimal:
  - `Missing`
  - `Complete`
- templates stay under the hood rather than becoming a daily staff UI focus
- quick actions remain modal
- provider posture remains appointment-centric

## 11. Clear Next Recommended Slice

Sprint 3 should open with the smallest possible encounter foundation from the appointment screen.

Recommended next slice:
- create `hc_encounter`
- add one encounter per appointment
- add an `Open Encounter` action on the appointment
- keep the encounter form extremely small:
  - one main notes field
  - one status field
  - only the minimum linkage/context fields

What Sprint 3 should still avoid at first:
- SOAP structure
- diagnosis or treatment detail
- billing linkage
- attachments
- signatures
- multi-tab charting

That keeps the workflow moving from pre-visit readiness into the start of visit documentation without opening full charting scope too early.
