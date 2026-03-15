# SPRINT 1 EXECUTION PLAN

Status:
- Planning document only
- Intended to guide actual Codex execution for Sprint 1
- Assumes `Odoo Community`

## 1. Execution Strategy

Sprint 1 should be executed as a narrow, sequential build of the earliest useful clinic-management slice.

Primary execution rule:
- build only enough to support:
  `clinic setup -> provider/patient/lead records -> appointment creation -> schedule view -> appointment detail`

Implementation assumptions:

- Odoo Community is the platform base
- `hc_scheduling` owns a custom `Appointment` model
- generic calendar events should not be deeply reused as the core appointment object
- Codex should work module by module and verify each layer before moving on

Execution principles:

- Keep the number of new models small.
- Prefer additive extensions to `res.partner`, `res.users`, and `crm.lead`.
- Build menu and security incrementally so partial slices can already be exercised.
- Validate screens and record flows immediately after each task cluster.
- Do not start any intake, consent, encounter, billing, package, dashboard, or AI work in Sprint 1.

## 2. Module-by-Module Build Tasks

### `hc_practice_core`

Purpose:
- establish clinic identity and base access structure

Build tasks:
- create module manifest with dependencies on `base` and `contacts`
- add `models/clinic_practice.py` for the `Practice` model
- define minimal fields:
  - name
  - timezone
  - active
  - default appointment duration if needed
- extend `res.users` or related profile link to associate internal users with one practice
- add security groups:
  - `hc_group_owner`
  - `hc_group_front_desk`
  - `hc_group_provider`
- create basic access control CSV entries for practice records
- create practice form and list views
- create minimal practice menu entry under a configuration/admin area

Validation after module task:
- one practice record can be created
- owner user can see practice settings
- front desk and provider access is appropriately limited

### `hc_patient_core`

Purpose:
- represent patients and providers cleanly without overbuilding

Build tasks:
- create module manifest with dependencies on `base`, `contacts`, and `hc_practice_core`
- extend `res.partner` for patient fields:
  - `is_hc_patient`
  - practice link
  - phone/email basics
  - active/inactive
  - optional notes field for Sprint 1 only if truly needed
- extend `res.users` and/or `res.partner` for provider fields:
  - `is_hc_provider`
  - practice link
  - display name
  - schedule display color or short code if useful
- create patient list and patient form views
- create provider form extensions in user or contact view
- create patient action and menu
- add record rules or access controls so clinic staff can access patient records appropriately

Validation after module task:
- patient can be created and edited
- provider can be marked and linked to a practice
- patient list opens cleanly
- patient form can be opened and saved without unrelated fields cluttering the experience

### `hc_leads`

Purpose:
- support simple new-patient lead capture and conversion

Build tasks:
- create module manifest with dependencies on `crm`, `hc_practice_core`, and `hc_patient_core`
- extend `crm.lead` with:
  - practice link
  - referral source field
  - `is_new_patient_lead` boolean or similar lightweight marker
- create simplified lead form adjustments for healthcare use
- create lead action/menu entry focused on new-patient leads
- add a server action, wizard, or button flow to convert a lead into a patient record
- ensure core identifying information is copied during conversion

Validation after module task:
- a lead can be created with referral source
- a lead can be converted to a patient
- patient record retains core contact data
- converted lead does not require manual cleanup

### `hc_scheduling`

Purpose:
- own the appointment model and appointment-centered workflow

Build tasks:
- create module manifest with dependencies on `hc_practice_core`, `hc_patient_core`, and optionally `calendar` only for helper UI concepts if needed
- create `models/appointment_type.py`
- define `AppointmentType` fields:
  - name
  - practice link
  - duration_minutes
  - active
- create `models/appointment.py`
- define custom `Appointment` model fields:
  - name or generated display label
  - practice link
  - patient link
  - provider link
  - appointment type link
  - start datetime
  - end datetime
  - status selection: `scheduled`, `confirmed`, `cancelled`, `checked_in`
  - notes field for scheduling notes only if needed
- add simple computed display logic for schedule readability
- create appointment list, form, and basic calendar views
- create appointment search/filter definitions
- create ability to launch new appointment from patient profile
- create appointment detail screen as the appointment form view or a specific action path
- add menus for appointment types and appointments

Validation after module task:
- appointment type can be created
- appointment can be created for patient and provider
- appointment appears in list and calendar/schedule view
- appointment status can be updated
- appointment can be opened from the patient profile and from the schedule

## 3. Recommended File Structure

Recommended repo layout for Sprint 1:

```text
addons/
  hc_practice_core/
    __init__.py
    __manifest__.py
    models/
      __init__.py
      clinic_practice.py
      res_users.py
    security/
      ir.model.access.csv
      hc_practice_security.xml
    views/
      hc_practice_views.xml
      hc_practice_menus.xml

  hc_patient_core/
    __init__.py
    __manifest__.py
    models/
      __init__.py
      res_partner.py
      res_users.py
    security/
      ir.model.access.csv
    views/
      hc_patient_views.xml
      hc_provider_views.xml
      hc_patient_menus.xml

  hc_leads/
    __init__.py
    __manifest__.py
    models/
      __init__.py
      crm_lead.py
    security/
      ir.model.access.csv
    views/
      hc_lead_views.xml
      hc_lead_menus.xml
    wizard/
      __init__.py
      lead_to_patient.py
    views/
      hc_lead_views.xml
      hc_lead_menus.xml
      lead_to_patient_views.xml

  hc_scheduling/
    __init__.py
    __manifest__.py
    models/
      __init__.py
      appointment_type.py
      appointment.py
    security/
      ir.model.access.csv
    views/
      hc_appointment_type_views.xml
      hc_appointment_views.xml
      hc_scheduling_menus.xml
```

Notes:

- Keep XML files separated by domain so later changes stay localized.
- Keep model extensions small and explicit.
- Do not add `data/` fixtures unless they are needed for role or sequence setup.
- If a sequence is needed for appointments, add a small `data/sequence.xml` inside `hc_scheduling`.

## 4. Suggested Order of Implementation

### Step 1: Sprint 1 base setup

Tasks:
- confirm Odoo Community version
- create `addons/` structure
- create empty module scaffolds for:
  - `hc_practice_core`
  - `hc_patient_core`
  - `hc_leads`
  - `hc_scheduling`

Validation:
- Odoo starts with addon path configured
- empty modules install without errors if scaffolded incrementally

### Step 2: Practice model and security groups

Tasks:
- implement `Practice`
- add groups and basic role XML
- add access CSV for practice model
- add minimal practice menu and settings view

Validation:
- owner can create practice
- front desk/provider cannot see admin-only setup if restricted

### Step 3: Patient and provider extensions

Tasks:
- extend `res.partner` for patient fields
- extend `res.users` or linked partner for provider fields
- implement patient list and profile views
- expose provider link to practice

Validation:
- create patient
- create provider
- open and edit both successfully

### Step 4: Lead workflow

Tasks:
- extend `crm.lead`
- add referral source and practice link
- create healthcare-focused lead view
- add conversion action to patient

Validation:
- create lead
- convert lead
- resulting patient opens correctly

### Step 5: Appointment types

Tasks:
- create `AppointmentType` model
- create list and form views
- link appointment types to practice

Validation:
- appointment type can be created and listed

### Step 6: Appointment model

Tasks:
- implement custom `Appointment` model
- define patient/provider/type/status/date fields
- add list, form, search, and calendar-style view
- create action buttons or smart buttons from patient profile

Validation:
- create appointment from menu
- create appointment from patient profile
- view appointment in schedule

### Step 7: Menus and workflow refinement

Tasks:
- finalize top-level navigation
- ensure menus are role-appropriate
- clean form titles, defaults, and action labels

Validation:
- front desk can navigate from patient to appointment in a small number of clicks
- provider can view schedule and appointment detail

### Step 8: Sprint 1 demo pass

Tasks:
- execute the full demo path repeatedly
- fix only defects inside Sprint 1 scope

Validation:
- no manual rescue
- no deferred modules needed

## 5. Security and Access-Control Tasks

Minimum security work for Sprint 1:

- create three main groups:
  - owner
  - front desk
  - provider
- assign model access rights for:
  - `Practice`
  - patient-related extensions
  - lead records
  - appointment types
  - appointments
- restrict practice configuration to owner or admin users
- allow front desk to create and edit patients, leads, and appointments
- allow providers to view patients relevant to their clinic and view/edit appointments as needed for schedule awareness

Suggested security files:

- `security/hc_practice_security.xml`
- `security/ir.model.access.csv` per module

Security guardrails:

- do not overengineer record rules for future multi-tenant SaaS in Sprint 1
- keep rules simple enough to understand and debug
- avoid permissions that require later modules to function

## 6. Menu and Navigation Tasks

Sprint 1 menu design should stay minimal.

Suggested top-level menu structure:

- `Healthcare`
  - `Patients`
  - `Leads`
  - `Schedule`
  - `Appointments`
  - `Configuration`

Suggested submenu layout:

- `Patients`
  - patient list

- `Leads`
  - new-patient leads

- `Schedule`
  - calendar/schedule view

- `Appointments`
  - appointment list
  - appointment types

- `Configuration`
  - practice settings

Navigation tasks:

- add patient smart button for appointments
- add lead action button for conversion to patient
- add appointment creation action from patient profile
- keep menus free of later-phase placeholders

Menu guardrail:
- do not create empty menus for intake, billing, packages, AI, or specialty modules

## 7. Validation Checks After Each Step

### After Step 1

- modules install or at least load manifests correctly
- no addon path or import errors

### After Step 2

- create one practice
- log in as owner and confirm practice access
- confirm non-owner roles do not get unintended configuration access

### After Step 3

- create one provider linked to the practice
- create one patient linked to the practice
- edit both records and save successfully

### After Step 4

- create one lead with referral source
- convert lead to patient
- verify patient record has expected identity fields

### After Step 5

- create one appointment type
- verify it is scoped to the correct practice

### After Step 6

- create one appointment from the appointment menu
- create one appointment from the patient profile
- verify appointment appears in the schedule view
- change appointment status and save

### After Step 7

- log in as each role and click through the entire Sprint 1 navigation path
- verify there are no dead-end menus or screens requiring deferred modules

### After Step 8

- run the full Sprint 1 demo twice with fresh records
- verify no manual cleanup is required between runs

Validation rule:
- when a step fails, fix the current step before starting the next one

## 8. Final Sprint 1 Demo Runbook

Run the final Sprint 1 demo in this exact order:

1. Log in as owner.
2. Open `Configuration` and create one practice.
3. Create one provider user and assign provider role plus practice link.
4. Log in as front desk or continue as owner acting as front desk.
5. Create one lead with name, phone/email, and referral source.
6. Convert the lead into a patient.
7. Open the resulting patient profile.
8. Create one appointment type such as `Initial Visit`.
9. Create one appointment for the patient and provider.
10. Open `Schedule` and show the appointment.
11. Open `Appointment Detail` and update status from `scheduled` to `confirmed` or `checked_in`.
12. Return to the patient profile and create another appointment from there.

Demo passes when:

- every step completes in the application
- there is no need for developer-only fixes
- the schedule and patient workflow feel coherent
- the product clearly looks ready for the next slice: intake and consent

## 9. Common Implementation Mistakes to Avoid

- Reusing generic calendar events too deeply and then fighting Odoo behavior
- Adding fields now for intake, consent, encounter, payment, or packages
- Pulling in `account`, `sale`, `product`, `point_of_sale`, or `stock` before needed
- Making leads too CRM-heavy for the narrow new-patient use case
- Creating duplicate patient/provider concepts instead of extending Odoo identity models cleanly
- Adding menus for future modules “just to prepare”
- Building a dashboard before the schedule slice works
- Writing overly complex record rules that are hard to debug in a solo-founder environment
- Mixing Sprint 2 work into Sprint 1 because appointment detail feels incomplete
- Optimizing for future multi-specialty architecture instead of a clean first slice

Final guardrail:
- if a task does not help represent the clinic, create people records, convert a lead, or schedule an appointment, it is not a Sprint 1 task
