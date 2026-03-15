# SCREEN FLOW

Status:
- Planning document only
- No implementation work is authorized from this file

## 1. UI Design Principles for Phase 1

The Phase 1 UI should help one acupuncture clinic run daily visits with minimal clicks, minimal training, and minimal visual clutter.

Primary rule:
- every screen must support the Phase 1 workflow spine:
  `lead -> patient intake -> consent -> appointment -> encounter -> checkout -> invoice -> payment -> follow-up -> retention`

UI principles:

- Prefer fewer screens with clearer transitions.
- Keep the default workflow linear and easy to follow.
- Make the next action obvious on every screen.
- Separate staff tasks from provider tasks where useful, but avoid duplicating screens unnecessarily.
- Show only the information needed for the current task.
- Treat billing and accounting as light operational steps, not as the center of the UI.
- Keep optional AI actions visible but never mandatory.
- Avoid exposing unused retail, POS, inventory, or multi-specialty controls.

Phase 1 visual philosophy:
- calm
- task-oriented
- low cognitive load
- tablet-friendly web UI, but not a separate mobile app

## 2. Primary User Roles and Their Screen Needs

### Front desk or owner-operator

Needs:
- create or locate patients
- review intake and consent status
- book and manage appointments
- check patients in
- handle checkout
- record card, cash, or package-credit payment
- prompt rebooking
- review basic daily business status

Primary screens:
- dashboard
- schedule
- patient profile
- appointment detail
- checkout
- package management
- recall worklist

### Provider

Needs:
- view daily appointments
- review intake and consent before the visit
- complete encounter notes
- set follow-up recommendation
- optionally use AI for intake review and note drafting

Primary screens:
- schedule
- appointment detail
- intake review
- encounter note

### Owner

In a solo clinic this may be the same person as front desk or provider.

Needs:
- quick visibility into visits, revenue, package usage, and rebooking gaps

Primary screens:
- dashboard
- recall worklist
- patient profile

### Patient

Needs:
- request or book an appointment
- complete intake forms
- sign consent
- receive confirmation

Primary screens:
- booking/request screen
- intake form screen
- consent screen
- confirmation screen

## 3. Required Screens

These are the minimum screens required for the Phase 1 product.

### Internal screens

- `Home Dashboard`
- `Daily Schedule`
- `Patient Profile`
- `Lead / New Patient Intake`
- `Appointment Detail`
- `Intake Review`
- `Consent Review`
- `Encounter Note`
- `Checkout`
- `Invoice / Payment`
- `Package Management`
- `Recall / Rebooking Worklist`

### Patient-facing screens

- `Booking / Appointment Request`
- `Intake Form Completion`
- `Consent Signing`
- `Appointment Confirmation`

Rule:
- if a screen does not directly help complete or monitor the visit loop, it should be deferred

## 4. Screen-by-Screen Purpose and Key Actions

### `Home Dashboard`

Purpose:
- give the clinic a calm starting point for the day

Key actions:
- see today's appointments
- see pending intake or consent gaps
- see patients waiting for checkout or rebooking
- see simple metrics: completed visits, collected revenue, package usage, recall count
- jump to schedule, patient, or recall screens

Primary user:
- front desk, owner

### `Daily Schedule`

Purpose:
- manage the working day

Key actions:
- view appointments by time and provider
- check patient intake/consent status
- create, edit, confirm, cancel, or check in appointments
- open the appointment detail
- create a new appointment from an existing patient record

Primary user:
- front desk, provider

### `Patient Profile`

Purpose:
- provide a single place to view the patient’s relationship with the clinic

Key actions:
- view demographics and contact details
- see intake history and consent status
- see upcoming and past appointments
- see package balance
- see retention or recall status
- create appointment
- open encounter history

Primary user:
- front desk, provider, owner

### `Lead / New Patient Intake`

Purpose:
- create a new patient or convert a lead into an active patient record

Key actions:
- capture referral source
- create lead or patient
- trigger intake and consent workflow
- schedule initial appointment

Primary user:
- front desk, owner-operator

### `Appointment Detail`

Purpose:
- act as the hub for one scheduled visit

Key actions:
- view patient, provider, appointment type, and status
- confirm intake completion and consent status
- check in patient
- open intake review
- open encounter note
- move to checkout after the visit

Primary user:
- front desk, provider

### `Intake Review`

Purpose:
- let the provider or staff quickly understand the patient before the visit

Key actions:
- read submitted intake answers
- see concise summary of visit reason and history
- mark intake as reviewed
- optionally trigger AI intake summary
- jump to encounter note

Primary user:
- provider, front desk if checking completeness

### `Consent Review`

Purpose:
- confirm that the patient has signed the required forms

Key actions:
- view required consent records
- see signed or missing status
- resend or re-request consent if needed

Primary user:
- front desk, provider

### `Encounter Note`

Purpose:
- document the visit in a fast, structured way

Key actions:
- view appointment context and recent history
- enter subjective, objective, assessment, and plan content
- save draft note
- finalize visit note
- set follow-up recommendation
- optionally trigger AI draft note assistance
- continue to checkout

Primary user:
- provider

### `Checkout`

Purpose:
- convert the completed visit into billable and payable items

Key actions:
- review visit service line
- optionally add a simple additional charge if needed
- apply package credit
- create invoice
- move to payment recording

Primary user:
- front desk, owner-operator

Scope limit:
- this is not a full POS screen
- retail add-ons should only appear if trivial and enabled

### `Invoice / Payment`

Purpose:
- complete the financial closeout for the visit

Key actions:
- view invoice amount due
- record payment
- choose tender type: card, cash, or package credit
- issue receipt or mark payment complete
- show updated patient balance
- continue to rebooking or recall

Primary user:
- front desk, owner-operator

### `Package Management`

Purpose:
- manage prepaid visit bundles without turning them into a full accounting subsystem

Key actions:
- create package definition
- assign package to patient
- see remaining sessions or credit
- view package usage history

Primary user:
- front desk, owner, provider if needed

### `Recall / Rebooking Worklist`

Purpose:
- help the clinic keep patients returning on time

Key actions:
- see patients due for follow-up
- see lapsed patients
- mark contacted, booked, or deferred
- open patient profile or create appointment
- optionally view AI rebooking prompt suggestions

Primary user:
- front desk, owner

### `Booking / Appointment Request`

Purpose:
- let a patient begin the workflow online

Key actions:
- request or book an appointment
- provide basic identifying information
- receive intake and consent next steps

Primary user:
- patient

### `Intake Form Completion`

Purpose:
- collect the patient’s structured intake information

Key actions:
- complete and submit intake questions
- save and continue if needed

Primary user:
- patient

### `Consent Signing`

Purpose:
- collect signed consent before the visit

Key actions:
- read consent
- sign electronically
- submit signed form

Primary user:
- patient

### `Appointment Confirmation`

Purpose:
- confirm next steps and appointment status

Key actions:
- show appointment time
- show intake and consent completion state
- provide simple instructions

Primary user:
- patient

## 5. Workflow Transitions Between Screens

The screen flow should follow the clinic’s actual work, not an abstract system design.

### New patient flow

`Booking / Appointment Request`
-> `Lead / New Patient Intake`
-> `Intake Form Completion`
-> `Consent Signing`
-> `Appointment Detail`
-> `Daily Schedule`

### Staff scheduling flow

`Home Dashboard`
-> `Daily Schedule`
-> `Appointment Detail`
-> `Patient Profile`

### Provider pre-visit flow

`Daily Schedule`
-> `Appointment Detail`
-> `Intake Review`
-> `Consent Review`
-> `Encounter Note`

### Checkout flow

`Encounter Note`
-> `Checkout`
-> `Invoice / Payment`
-> `Patient Profile` or `Recall / Rebooking Worklist`

### Retention flow

`Home Dashboard`
-> `Recall / Rebooking Worklist`
-> `Patient Profile`
-> `Appointment Detail` or `Daily Schedule`

Transition rule:
- the next screen should be the next task in the clinic workflow, not just a list of related records

## 6. Where AI Appears in the UI

AI should appear as a small assistive action inside existing screens.

### `Intake Review`

Optional AI action:
- `Generate Intake Summary`

Expected behavior:
- produces a concise draft summary from the submitted intake
- user can review it before relying on it

### `Encounter Note`

Optional AI action:
- `Draft Note`

Expected behavior:
- produces draft note text or section suggestions
- provider reviews, edits, or rejects it

### `Invoice / Payment` or `Recall / Rebooking Worklist`

Optional AI action:
- `Suggest Rebooking Prompt`

Expected behavior:
- suggests who may need follow-up and optionally drafts a prompt or next action

### `Encounter Note` or post-visit context

Optional AI action:
- `Draft After-Visit Summary`

Expected behavior:
- creates patient-facing draft instructions after the note is complete

AI UI rule:
- AI must never appear as the only path forward
- AI outputs must be clearly marked as drafts
- AI acceptance must be an explicit user action

## 7. Screens Explicitly Deferred

These screens should not exist in Phase 1.

- insurance claims screen
- clearinghouse submission screen
- payer management screen
- full accounting dashboard
- reconciliation workspace
- advanced POS counter interface
- inventory management screen
- retail catalog management for large product sets
- multi-location administration
- specialty-switching configuration screen
- chiropractic exam screen
- massage charting screen
- mobile app-specific screens
- voice AI call console
- patient clinical chat screen

Deferred-screen rule:
- if a screen exists mainly to support a deferred business model, it should not be designed yet

## 8. Risks of Overcomplicating the Screen Flow

- Too many handoff screens will make the clinic feel slower rather than calmer.
- Splitting one task across too many forms will create training burden.
- Mixing provider and front-desk needs too aggressively will clutter every screen.
- Adding financial detail screens too early will drag the product toward accounting software.
- Adding retail and POS flows early will distract from the core visit loop.
- Building specialty-specific screen branches in Phase 1 will weaken the shared architecture.
- Putting AI in too many places will make the workflow feel uncertain and fragile.
- Designing for every future role now will create a bloated interface before one clinic is working successfully.

Final screen-flow guardrail:
- if a screen does not make it easier to intake, schedule, document, check out, get paid, or rebook, it is probably not a Phase 1 screen
