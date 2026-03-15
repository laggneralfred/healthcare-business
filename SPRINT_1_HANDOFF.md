# Sprint 1 Handoff

Status:
- Documentation summary only
- Reflects the current Sprint 1 foundation in the repo

## 1. Sprint 1 Module Summary

### `hc_practice_core`
- Defines the Healthcare root menu and basic configuration area.
- Adds `hc.practice` as the clinic/practice model.
- Extends `res.users` with a practice link.
- Defines the three Sprint 1 roles:
  - `hc_group_owner`
  - `hc_group_front_desk`
  - `hc_group_provider`

### `hc_patient_core`
- Extends `res.partner` for patient use with:
  - `is_hc_patient`
  - `practice_id`
- Extends `res.users` with:
  - `is_hc_provider`
- Provides the cleaned Patient list and Patient profile UI.
- Adds the patient-to-appointment handoff action from the patient form.

### `hc_leads`
- Extends `crm.lead` for clinic lead inquiry use with:
  - `is_hc_lead`
  - `practice_id`
- Provides the cleaned Lead Inquiries list and form.
- Supports manual `Create Patient` handoff from a Lead Inquiry.

### `hc_scheduling`
- Owns the custom scheduling models for Sprint 1:
  - `hc.practitioner`
  - `hc.appointment.type`
  - `hc.appointment`
- Provides:
  - Appointments list
  - Appointment form
  - Calendar display layer on `hc.appointment`
  - Configuration for Practitioners and Visit Types

## 2. Implemented Workflow Summary

Current working Sprint 1 workflow:
- `Lead Inquiry -> Create Patient -> Patient record -> Create Appointment -> Appointment list/calendar/form`

What currently works:
- Create one clinic/practice record.
- Mark provider users and link them to a practice.
- Create and manage patient records in a healthcare-focused UI.
- Create and manage lead inquiries in a clinic-focused UI.
- Create a patient manually from a lead inquiry.
- Open the created patient immediately after lead handoff.
- Create practitioners and visit types for scheduling.
- Create appointments from:
  - the Appointments menu
  - the Patient profile
- View appointments in:
  - list view
  - calendar view
  - appointment detail form

What Sprint 1 intentionally does not do:
- intake
- consent
- encounters
- billing
- payments
- packages
- reminders
- dashboards
- AI

## 3. Role / Permission Summary

### Owner
- Full access to practice setup.
- Full access to patient, lead, practitioner, visit type, and appointment workflow.
- Can see Healthcare configuration items.

### Front Desk
- Operational access to:
  - Patients
  - Lead Inquiries
  - Appointments
- Can create and edit:
  - leads
  - patients
  - practitioners
  - appointments
- Can access Configuration only where needed for Sprint 1 operational setup.

### Provider
- Focused appointment/schedule access only.
- Can access:
  - Healthcare root
  - Appointments
- Does not currently get menu access to:
  - Patients
  - Lead Inquiries
- This is intentional because Sprint 1 does not yet add module-local read-only safety on the core `res.partner` patient UI.

## 4. Exact Install / Update Commands

Update all current Sprint 1 modules:

```bash
docker compose exec odoo odoo -d healthcare_dev -u hc_practice_core,hc_patient_core,hc_leads,hc_scheduling --stop-after-init
```

If Python method changes were made and the running web container appears stale, restart Odoo after updating:

```bash
docker compose restart odoo
```

## 5. Exact Browser Acceptance Checklist

### Core setup
1. Log in as `owner`.
2. Open `Healthcare -> Configuration -> Clinic / Practices`.
3. Confirm a practice can be created and saved.
4. Open Users and confirm provider users can be linked to a practice and marked as healthcare providers.

### Lead inquiry flow
1. Open `Healthcare -> Lead Inquiries`.
2. Create a new lead inquiry with:
   - Name
   - Phone or Email
   - Practice
   - Notes
3. Save and reopen it.
4. Confirm `Create Patient` is visible.
5. Click `Create Patient`.
6. Confirm a patient record opens.
7. Confirm copied fields:
   - Name
   - Phone
   - Email
   - Practice
   - Notes
8. Confirm `Healthcare Patient` is checked.
9. Confirm the original lead inquiry still exists.

### Patient flow
1. Open `Healthcare -> Patients`.
2. Confirm the patient appears in the list.
3. Open the patient profile.
4. Confirm the UI is clinic-specific and calm.
5. Confirm `Create Appointment` is visible.

### Scheduling flow
1. Open `Healthcare -> Configuration -> Practitioners`.
2. Confirm a practitioner can be created.
3. Open `Healthcare -> Configuration -> Visit Types`.
4. Confirm a visit type can be created.
5. Return to the patient profile and click `Create Appointment`.
6. Confirm the appointment form opens with:
   - Patient prefilled
   - Practice prefilled when present on the patient
7. Complete the remaining appointment fields and save.
8. Open `Healthcare -> Appointments`.
9. Confirm the appointment appears in the list.
10. Open calendar view.
11. Confirm the appointment appears in the calendar and opens the same appointment form.

### Role sanity
1. Log in as `front desk`.
2. Confirm access to:
   - Patients
   - Lead Inquiries
   - Appointments
   - Practitioners via Configuration
3. Log in as `provider`.
4. Confirm access to:
   - Appointments
5. Confirm `provider` does not see:
   - Patients
   - Lead Inquiries

## 6. Known Limitations / Acceptable Gaps

These are expected and acceptable for the current Sprint 1 finish:

- No intake workflow.
- No consent workflow.
- No encounter or chart note workflow.
- No appointment status workflow beyond simple scheduling.
- No checkout, invoice, or payment workflow.
- No package or rebooking workflow.
- No dashboards.
- No AI.
- No multi-location or multi-specialty support.

Operational limitations:
- `Create Patient` from Lead Inquiry is intentionally manual and simple.
- Duplicate patient protection is not implemented.
- Provider setup still lives on `res.users`, which is functional but admin-facing.
- Patient and lead screens sit on top of core Odoo models, so safety currently relies partly on menu restriction rather than deep record-rule hardening.
- If method-based changes are not picked up after update, the Odoo container may need a restart.

## 7. Recommended Next Priorities For Sprint 2 Planning

Priority order:

1. Define the next workflow milestone explicitly.
   - Choose whether Sprint 2 starts with:
     - intake/consent
     - encounter/note workflow
     - checkout/payment
   - Do not mix all three at once.

2. Tighten the appointment hub concept before adding more stages.
   - Decide what the appointment detail should become in Sprint 2.
   - Keep it the main workflow anchor.

3. Decide whether provider access should stay schedule-only or expand.
   - This matters before building encounter/note work.

4. Add the next workflow slice as one narrow module group.
   - Best candidate:
     - `hc_intake` + `hc_consent`
   - Alternative:
     - `hc_encounter` only if the workflow anchor is fully decided first

5. Keep the same Sprint discipline.
   - One usable slice at a time.
   - No dashboards, billing depth, or AI until the human workflow is stable.

## 8. Practical Summary

Sprint 1 is now a believable small-clinic foundation.

It supports:
- clinic setup
- provider/practitioner setup
- lead inquiry capture
- patient creation and management
- patient handoff from lead inquiry
- appointment creation and schedule viewing

It does not yet support the actual visit lifecycle beyond scheduling.

That is acceptable.

The right next step is not “more polish everywhere.”
The right next step is choosing the next narrow workflow slice and implementing it without breaking the current foundation.
