# Sprint 2 Slice 2A Handoff

Status:
- Implemented and stabilized
- Narrow scope only: public intake submission by secure token link

## 1. What Slice 2A Added

Slice 2A adds a patient-facing public intake path on top of the existing internal intake record.

What now works:
- Front desk or owner can generate or retrieve a shareable intake link from:
  - the patient form
  - the appointment form
- The link opens without login.
- The public page is limited to one `hc.intake.submission` record by secure token.
- The patient can fill out the existing intake content fields and submit them.
- Public submission writes the intake content onto the existing intake record.
- Public submission sets:
  - `status = complete`
  - `submitted_on = now`
- Existing patient and appointment readiness logic continues to work because it already reads the latest intake submission status.
- Staff can still reopen and review the same intake internally through the existing `Record Intake` modal.

## 2. Changed Files

### Core intake model and actions
- `addons/hc_intake/models/intake_submission.py`
- `addons/hc_intake/models/res_partner.py`
- `addons/hc_intake/models/appointment.py`

### Public route and templates
- `addons/hc_intake/controllers/__init__.py`
- `addons/hc_intake/controllers/public_intake.py`
- `addons/hc_intake/views/hc_intake_public_templates.xml`

### Share-link wizard
- `addons/hc_intake/wizards/__init__.py`
- `addons/hc_intake/wizards/hc_intake_share_link_wizard.py`
- `addons/hc_intake/views/hc_intake_share_link_wizard_views.xml`

### Staff form entry points and addon wiring
- `addons/hc_intake/views/hc_intake_patient_views.xml`
- `addons/hc_intake/views/hc_intake_appointment_views.xml`
- `addons/hc_intake/security/ir.model.access.csv`
- `addons/hc_intake/__init__.py`
- `addons/hc_intake/__manifest__.py`

## 3. Commands

Update the intake module:

```bash
docker compose exec odoo odoo -d healthcare_dev -u hc_intake --stop-after-init
```

Restart Odoo so controller changes are active in the running web process:

```bash
docker compose restart odoo
```

## 4. Browser Verification Checklist

### Owner / Front Desk
1. Open a patient record.
2. Confirm the `Intake` group still shows:
   - `Intake Status`
   - `Record Intake`
   - `Get Intake Link`
3. Click `Get Intake Link`.
4. Confirm the `Patient Intake Link` modal opens.
5. Confirm the modal shows:
   - the intake record
   - the public intake URL
6. Open the same flow from an appointment record and confirm the same behavior there.

### Public patient flow
1. Open the generated intake link in a browser without logging in.
2. Confirm the page opens directly.
3. Confirm the page shows the practice and patient context only.
4. Submit the form with all fields empty.
5. Confirm the page stays open and shows the validation error.
6. Submit the form again with at least one intake content field filled.
7. Confirm the success page appears.
8. Reload the same URL.
9. Confirm the page now shows the closed wording that the intake was already received.

### Internal staff review
1. Return to the original patient or appointment.
2. Confirm `Intake Status` now shows `Complete`.
3. Click `Record Intake`.
4. Confirm the same intake record reopens and shows the submitted content.
5. On an appointment, confirm the existing appointment readiness behavior still reflects the completed intake.

### Provider sanity
1. Log in as a provider.
2. Confirm provider behavior is unchanged for this slice.
3. Confirm no new public-link action is exposed to the provider role.

## 5. Intentionally Out Of Scope Items Preserved

These remain intentionally excluded from Slice 2A:
- portal accounts
- email automation
- SMS or reminders
- e-signature
- document upload
- consent packet flow
- multi-form packet workflow
- intake template redesign
- encounter or chart note design
- token revocation or token rotation UI
- broad public listing, search, or record discovery
- any new external forms framework

## 6. Stabilization Notes

The stabilization pass kept the workflow unchanged and only tightened UX copy:
- staff buttons now say `Get Intake Link`
- wizard wording now makes manual sharing more explicit
- public intake instructions are clearer about filling only relevant sections
- the completion page now distinguishes:
  - newly submitted
  - already received / closed
