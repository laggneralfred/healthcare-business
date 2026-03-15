# ACCEPTANCE CRITERIA

Status:
- Planning document only
- No implementation work is authorized from this file

## 1. Acceptance Principles

Phase 1 is done when one acupuncture clinic can complete the core visit workflow in one system without manual rescue, hidden admin fixes, or dependence on deferred features.

Primary acceptance rule:
- the system must support the full Phase 1 workflow spine:
  `lead -> patient intake -> consent -> appointment -> encounter -> checkout -> invoice -> payment -> follow-up -> retention`

Acceptance principles:

- Criteria must be observable by running the workflow.
- Criteria must be testable without relying on “future” modules.
- The product must be usable without AI enabled.
- AI, if enabled, must improve the workflow without becoming required.
- Package credit behavior must work in real checkout flow, not as a theoretical model.
- Financial behavior must stay light: invoice creation, payment recording, package credit use, and simple balances only.
- No acceptance criterion may depend on insurance claims, deep accounting, heavy POS, inventory depth, or multi-specialty support.

Definition of “manual rescue”:
- editing records directly in the database
- using spreadsheets to complete core workflow steps
- finishing payment flow outside the system because core data is broken
- bypassing missing transitions with admin-only hacks

## 2. Workflow-Level Acceptance Criteria

### New patient intake workflow

Accepted when:
- a staff user can create a lead or patient record for a new patient
- a patient can receive and submit intake forms
- a patient can sign required consent forms
- staff can see whether intake and consent are complete before the appointment
- the submitted intake remains linked to the patient record and can be reviewed later

### Appointment workflow

Accepted when:
- staff can create an appointment for a patient and provider
- the appointment appears in the daily schedule
- appointment status can move through basic operational states such as scheduled and checked in
- staff or provider can open the appointment as the visit hub

### Encounter workflow

Accepted when:
- an encounter can be started from the appointment
- a provider can complete and save a structured visit note
- the encounter remains linked to patient, provider, and appointment
- the provider can capture a follow-up recommendation
- the provider can finish the note without leaving the workflow spine

### Checkout workflow

Accepted when:
- checkout can be started from a completed encounter
- the visit service line appears correctly in checkout
- package credit can be applied if available
- checkout can create an invoice without manual data repair

### Payment workflow

Accepted when:
- invoice total due is visible
- payment can be recorded as `card`, `cash`, or `package_credit`
- payment completion updates the visit’s financial state
- a receipt or clear payment confirmation can be produced
- the system shows whether the invoice is paid or still outstanding

### Package-credit workflow

Accepted when:
- a package can be assigned to a patient
- remaining package balance is visible before checkout
- package credit can be consumed during checkout
- remaining package balance updates immediately after use
- package credit cannot be applied beyond the available balance

### Rebooking and retention workflow

Accepted when:
- follow-up recommendation from the encounter can be surfaced after payment
- staff can rebook a patient from the end of the visit or mark the patient for recall
- patients due for follow-up appear in the recall or rebooking worklist
- staff can mark a recall item as booked, contacted, or deferred

### End-to-end workflow

Accepted when:
- one new patient can move from first contact through intake, consent, appointment, encounter, checkout, payment, and recall without leaving the system
- one returning patient can complete a repeat visit using package credit and be prompted to rebook

## 3. Milestone-Level Acceptance Criteria

### Milestone 0: Foundation Setup

Accepted when:
- the chosen Odoo environment runs reliably
- Phase 1 modules can be installed and loaded repeatably
- core user roles exist and can log in with the correct access boundaries

### Milestone 1: Practice, Provider, and Patient Core

Accepted when:
- one clinic can be configured
- provider records can be created and edited
- patient records can be created and edited
- a lead can be created and either retained as a lead or converted to a patient
- the patient profile screen is usable for day-to-day lookup

### Milestone 2: Intake and Consent

Accepted when:
- intake templates can be created and used
- a patient can submit an intake form
- consent templates can be issued and signed
- patient and appointment contexts show current intake and consent status

### Milestone 3: Scheduling and Appointment Hub

Accepted when:
- appointment types exist and are selectable
- appointments can be created and edited
- the daily schedule screen shows appointments correctly
- appointment detail provides access to intake, consent, and encounter workflow

### Milestone 4: Encounter and Note Workflow

Accepted when:
- encounters can be created from appointments
- providers can save draft notes and finalize notes
- follow-up recommendation can be captured in the encounter
- note completion does not require unsupported specialty complexity

### Milestone 5: Checkout, Invoice, and Payment

Accepted when:
- checkout can be launched from an encounter
- visit charges flow into an invoice
- card and cash payments can be recorded
- invoice status updates after payment
- no deep accounting configuration is required to finish a visit

### Milestone 6: Packages and Rebooking

Accepted when:
- package definitions can be created
- package credits can be applied and decremented in checkout
- recall or rebooking worklist is usable
- next-visit recommendation feeds the retention workflow

### Milestone 7: Dashboard and Operational Visibility

Accepted when:
- dashboard shows today’s appointments
- dashboard shows simple revenue visibility
- dashboard shows package usage or package-related status
- dashboard or recall worklist surfaces patients due for follow-up

### Milestone 8: Optional AI Layer

Accepted when:
- AI can be enabled without breaking the non-AI workflow
- intake summary can be generated and reviewed
- note draft can be generated and reviewed
- AI outputs remain optional, editable, and rejectable
- accepted AI content does not bypass human review

## 4. Screen-Level Acceptance Criteria

### `Home Dashboard`

Accepted when:
- today’s appointments are visible
- pending intake or consent gaps are visible
- collected revenue summary is visible at a basic level
- users can navigate directly to schedule, patient, and recall workflows

### `Daily Schedule`

Accepted when:
- appointments display by time and provider
- users can create and open appointments
- intake and consent readiness is visible from the schedule or appointment entry
- users can check a patient in

### `Patient Profile`

Accepted when:
- demographics and contact details are visible and editable
- upcoming and past appointments are visible
- intake and consent history are visible
- package balance is visible if the patient has a package
- users can create a new appointment from the patient profile

### `Lead / New Patient Intake`

Accepted when:
- new patient details can be captured
- referral source can be recorded
- staff can trigger intake and consent next steps
- staff can convert the lead into an active patient

### `Appointment Detail`

Accepted when:
- patient, provider, appointment type, and status are visible
- intake and consent status are visible
- users can move from appointment detail into intake review, encounter, or checkout as appropriate

### `Intake Review`

Accepted when:
- submitted intake answers are visible
- the user can see enough information to prepare for the visit
- if AI is enabled, an intake summary can be generated and reviewed here

### `Consent Review`

Accepted when:
- required consent records can be viewed
- missing or complete state is obvious
- staff can resend or re-request consent when needed

### `Encounter Note`

Accepted when:
- encounter context shows patient and appointment information
- the provider can enter and save structured note content
- the provider can finalize the note
- the provider can capture a follow-up recommendation
- if AI is enabled, note drafting appears as an optional action

### `Checkout`

Accepted when:
- visit service charge appears or can be added easily
- package credit can be selected and applied when available
- checkout can continue to invoice creation without unsupported manual steps
- checkout does not require POS-specific controls

### `Invoice / Payment`

Accepted when:
- invoice amount due is visible
- a payment can be recorded as card, cash, or package credit
- payment completion updates status immediately
- outstanding balance is shown if partial or no payment exists
- a receipt or clear completion indicator is available

### `Package Management`

Accepted when:
- package definitions can be created
- packages can be assigned to patients
- remaining balance can be viewed
- prior usage can be reviewed at a basic level

### `Recall / Rebooking Worklist`

Accepted when:
- patients due for follow-up appear in a visible list
- users can change recall state to booked, contacted, or deferred
- users can jump directly from the recall item to patient or scheduling flow

### Patient-facing screens

`Booking / Appointment Request` is accepted when:
- a patient can submit a request or booking with basic identifying information

`Intake Form Completion` is accepted when:
- a patient can complete and submit intake forms successfully

`Consent Signing` is accepted when:
- a patient can sign and submit consent electronically

`Appointment Confirmation` is accepted when:
- the patient sees appointment time and next steps clearly

## 5. AI Feature Acceptance Criteria

General AI acceptance:

- the system is fully usable with all AI features disabled
- AI actions are visibly optional
- AI outputs are marked as drafts or suggestions
- a user can accept, edit, or reject AI output
- AI output does not overwrite finalized clinical or financial data automatically

### AI intake summary

Accepted when:
- the user can trigger a summary from the intake review screen
- a draft summary is returned in a readable form
- the summary can be ignored without blocking the workflow

### AI draft note

Accepted when:
- the provider can trigger draft generation from the encounter note screen
- the result appears as editable draft content
- the provider can reject the draft and continue documenting manually

### AI after-visit summary

Accepted when:
- a user can generate a draft after-visit summary from encounter context
- the output is reviewable before being used

### AI rebooking prompt support

Accepted when:
- the system can surface optional suggestions for who may need follow-up
- staff can ignore those suggestions and still use the recall workflow normally

AI rejection rule:
- if AI is required to make notes understandable or the recall workflow usable, the core product is not accepted

## 6. Explicit Non-Goals

The following are not required for Phase 1 acceptance:

- insurance claims submission
- clearinghouse integration
- payer management
- coding assistance for insurance billing
- deep accounting workflows
- advanced reconciliation
- full retail/POS workflow
- inventory depth
- multi-specialty support
- chiropractic or massage-specific flows
- multi-location administration
- native mobile apps
- telehealth
- autonomous clinical AI

If any of these become necessary for basic operation, Phase 1 has drifted out of scope.

## 7. Demo Acceptance Checklist

The Phase 1 demo is accepted when all of the following can be shown end to end:

- create or convert a new patient from lead intake
- complete intake and consent
- create and confirm an appointment
- open the appointment from the daily schedule
- complete an encounter note
- capture follow-up recommendation
- move into checkout
- create an invoice
- record payment as card or cash
- show payment as complete
- assign a package to a patient
- use package credit on a repeat visit
- show updated package balance
- mark the patient for rebooking or recall
- show the patient on the recall workflow if not rebooked immediately
- show dashboard visibility into visits, revenue, package usage, and follow-up needs

Optional demo additions:

- AI intake summary
- AI note draft
- AI after-visit summary

Demo failure conditions:

- hidden admin repair is needed between steps
- external tools are needed to complete core workflow
- invoice or payment state becomes unclear
- package balance does not update reliably
- AI is required to complete the flow

## 8. Pilot Readiness Checklist

The product is pilot-ready when:

- one clinic can be configured without one-off code changes
- staff roles and provider roles can access the right screens
- the full non-AI visit workflow works end to end
- card, cash, and package-credit flows behave reliably
- patient-facing intake and consent flows work without staff intervention in normal cases
- dashboard and recall visibility are understandable to clinic staff
- major workflow states are visible and not ambiguous
- there is a repeatable way to create a new demo or pilot clinic
- deferred features are not required for routine daily use

The product is not pilot-ready if:

- it depends on insurance workflows
- it depends on full accounting configuration
- it requires POS or inventory setup to finish normal visits
- it requires specialty-depth charting beyond the shared Phase 1 encounter flow
- support would require constant developer intervention for ordinary clinic tasks
