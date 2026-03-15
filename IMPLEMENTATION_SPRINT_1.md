# IMPLEMENTATION SPRINT 1

Status:
- Planning document only
- Intended to guide the first real implementation slice
- No code is included in this document

## 1. Sprint 1 Objective

Build the smallest working foundation for one acupuncture clinic to exist in the system, manage its people, and schedule appointments.

Sprint 1 goal:
- prove the application can represent one clinic, its providers, its patients, and its appointment calendar

This sprint must align with the full workflow spine, but it only implements the earliest necessary slice:
- `lead -> patient -> appointment`

This sprint does not try to complete the full visit workflow.

## 2. Exact In-Scope Features

Sprint 1 includes only the following:

### Clinic and user foundation

- one clinic configuration record
- basic role structure for owner, front desk, and provider
- provider records linked to system users

### Patient and lead foundation

- patient record creation and editing
- patient list and patient profile
- basic lead or new-patient record creation
- lead-to-patient conversion path at a simple operational level
- referral source capture on leads or new-patient entry

### Basic scheduling foundation

- appointment type definition
- appointment creation and editing
- daily schedule view
- appointment detail view
- basic appointment statuses such as scheduled, confirmed, cancelled, and checked in
- ability to create an appointment from a patient record

### Minimal navigation

- login
- access to patient, schedule, and appointment workflows

## 3. Exact Out-of-Scope Features

Sprint 1 explicitly excludes:

- intake forms
- consent forms and signatures
- patient-facing intake workflows
- encounter creation
- encounter notes
- checkout
- invoice creation
- payment recording
- package definitions or package balance
- recall or rebooking worklist
- dashboard metrics
- AI of any kind
- gift certificates
- retail products
- POS
- inventory
- insurance workflows
- accounting workflows beyond bare Odoo setup
- multi-specialty support
- multi-location support
- mobile apps

Hard sprint rule:
- if a feature is not required to create patients, providers, leads, and appointments, it is out of scope for Sprint 1

## 4. Models Touched in Sprint 1

### Required models

- `Practice`
- `Provider`
- `Patient`
- `Lead`
- `AppointmentType`
- `Appointment`

### Odoo-linked models touched

- `res.users`
- `res.partner`
- `crm.lead`
- calendar-related appointment primitives if reused

### Models explicitly not touched yet

- `IntakeFormTemplate`
- `IntakeSubmission`
- `ConsentTemplate`
- `ConsentRecord`
- `Encounter`
- `EncounterSection`
- `CheckoutSession`
- `CheckoutLine`
- `Invoice`
- `Payment`
- `Package`
- `PackageBalance`
- `RetentionSignal`
- all AI review models

## 5. Odoo Base Modules Reused

Sprint 1 should reuse only the Odoo base needed for this slice:

- `base`
- `contacts`
- `crm`
- `calendar`

Use only if clearly needed for navigation or simple configuration:

- `website`

Explicitly do not depend on in Sprint 1:

- `product`
- `account`
- `sale`
- `point_of_sale`
- `stock`

## 6. Custom Modules Created

Sprint 1 should introduce only the smallest set of custom modules needed for the slice.

### Required custom modules

- `hc_practice_core`
  - clinic configuration
  - role and feature-flag foundation

- `hc_patient_core`
  - patient extensions on top of Odoo contacts
  - provider profile extensions on top of Odoo users/contacts

- `hc_leads`
  - new-patient lead capture
  - referral source handling
  - lead conversion support

- `hc_scheduling`
  - appointment type
  - appointment object or appointment extensions
  - schedule and appointment detail workflow

### Explicitly not created yet

- `hc_intake`
- `hc_consent`
- `hc_encounter`
- `hc_checkout`
- `hc_billing_light`
- `hc_packages`
- `hc_retention`
- `hc_reporting`
- `hc_documents`
- all AI modules

## 7. Minimal Screens to Implement

Sprint 1 should implement only the screens necessary for clinic identity and appointment setup.

### Required internal screens

- `Clinic Setup` or minimal practice settings screen
- `Patient List`
- `Patient Profile`
- `Lead / New Patient Intake`
- `Daily Schedule`
- `Appointment Detail`
- `Appointment Create/Edit`

### Minimal user-access foundation

- login
- role-based visibility for owner, front desk, and provider

### Explicitly deferred screens

- intake review
- consent review
- encounter note
- checkout
- invoice/payment
- package management
- recall/rebooking
- dashboard
- all patient-facing screens

Screen rule:
- if a screen exists only to support later workflow stages, do not build it in Sprint 1

## 8. Acceptance Criteria for Sprint 1

Sprint 1 is accepted when all of the following are true:

### Clinic and user setup

- one clinic can be configured in the system
- at least one provider user can be created and assigned to that clinic
- owner, front desk, and provider roles can log in and access the appropriate screens

### Patient and lead workflow

- a patient can be created and edited
- a lead can be created with basic referral information
- a lead can be converted into a patient without losing core identifying information
- patient profile can be opened from both patient list and lead conversion path

### Scheduling workflow

- an appointment type can be created
- an appointment can be created for a patient and provider
- the appointment appears in the daily schedule
- the appointment can be opened in appointment detail
- appointment status can be updated through the allowed basic states
- a new appointment can be created from the patient profile

### Stability requirements

- no manual database fixes are needed to complete the above flows
- no AI is required anywhere
- no accounting setup is required to create appointments
- no later-phase models are required to make Sprint 1 usable

## 9. Internal Demo for Sprint 1

The Sprint 1 demo should show one complete “early workflow” slice:

1. Log in as clinic owner or front desk.
2. Configure one clinic record.
3. Create one provider.
4. Create one new patient lead with referral source.
5. Convert the lead to a patient.
6. Open the patient profile.
7. Create one appointment type.
8. Create an appointment for that patient and provider.
9. View the appointment on the daily schedule.
10. Open the appointment detail and update its status.
11. Return to the patient profile and create a second appointment from there.

Demo success condition:
- the system demonstrates a believable foundation for the later intake-to-payment workflow without pretending later milestones already exist

## 10. Risks and Likely Sticking Points

- Overbuilding the practice model for future multi-location or multi-specialty use
- Over-customizing Odoo calendar behavior instead of using a simpler appointment model
- Making provider and patient models too abstract for the real clinic workflow
- Letting lead management become a full CRM project
- Building schedule views that assume intake, consent, encounter, or billing state too early
- Pulling in `account`, `sale`, or `product` before they are needed
- Designing too many screens when one patient profile and one appointment detail screen are enough
- Adding fields “for later” that create clutter now

Main sticking point:
- deciding whether to extend Odoo calendar/event objects lightly or to own a cleaner custom appointment model early

Sprint 1 bias:
- choose the option that is easier to keep stable and understandable, not the option that looks more future-complete

## 11. Suggested Implementation Order Inside the Sprint

1. Settle the Phase 1 Odoo base for Sprint 1:
   - `base`
   - `contacts`
   - `crm`
   - `calendar`

2. Create `hc_practice_core`:
   - clinic record
   - role foundations
   - basic configuration

3. Create `hc_patient_core`:
   - provider extensions
   - patient extensions
   - patient list and patient profile

4. Create `hc_leads`:
   - lead capture
   - referral source
   - lead conversion to patient

5. Create `hc_scheduling`:
   - appointment type
   - appointment creation/edit
   - schedule view
   - appointment detail

6. Run the Sprint 1 demo flow repeatedly until it works without rescue.

Implementation-order rule:
- do not start intake or consent as “just a little extra”
- do not start encounters because appointment detail feels incomplete
- stop at a clean, working patient-and-schedule slice

## Sprint 1 Summary

Sprint 1 should produce:
- one clinic
- one provider setup path
- one patient and lead foundation
- one usable schedule
- one appointment flow

Sprint 1 should not produce:
- a full visit workflow
- financial workflows
- AI features
- patient-facing forms
- specialty depth

That is the smallest meaningful implementation slice that still moves the product forward.
