# BUILD SEQUENCE

Status:
- Planning document only
- No implementation work is authorized from this file

## 1. Build Strategy for Phase 1

Phase 1 should be built as a sequence of small, testable workflow slices, not as a big parallel ERP customization effort.

Primary rule:
- preserve the workflow spine at every stage:
  `lead -> patient intake -> consent -> appointment -> encounter -> checkout -> invoice -> payment -> follow-up -> retention`

Build strategy:

- Start with the minimum Odoo base needed to support identity, scheduling, CRM, products, and light invoicing.
- Build the clinic workflow in dependency order from patient intake through payment and rebooking.
- Keep the first usable version non-AI and non-specialty-deep.
- Add AI only after the human workflow works reliably without AI.
- Treat each milestone as a stable slice that can be demoed.
- Reject work that introduces insurance, deep accounting, heavy POS, inventory depth, or multi-specialty branching.

Solo-founder rule:
- prefer milestones that reduce ambiguity and expose real workflow issues quickly
- do not carry multiple unstable subsystems at once

## 2. Milestones in Dependency Order

### Milestone 0: Foundation Setup

Goal:
- prepare the Odoo base, security posture, and module skeletons without building clinic logic yet

### Milestone 1: Practice, Provider, and Patient Core

Goal:
- make the system capable of representing one clinic, its staff, patients, and leads

### Milestone 2: Intake and Consent

Goal:
- support the pre-visit onboarding workflow for new and returning patients

### Milestone 3: Scheduling and Appointment Hub

Goal:
- support appointment creation, daily schedule management, and appointment-centered visit prep

### Milestone 4: Encounter and Note Workflow

Goal:
- support provider documentation and follow-up recommendation capture

### Milestone 5: Checkout, Invoice, and Payment

Goal:
- support the financial closeout of a visit using card, cash, and package credit

### Milestone 6: Packages and Rebooking

Goal:
- support prepaid visit bundles and basic patient retention workflows

### Milestone 7: Dashboard and Operational Visibility

Goal:
- give the clinic basic day-to-day visibility into visits, revenue, packages, and rebooking gaps

### Milestone 8: Optional AI Layer

Goal:
- add optional, reviewable AI assistance on top of the working workflow

## 3. What Each Milestone Must Deliver

### Milestone 0: Foundation Setup

Must deliver:
- chosen Odoo version for Phase 1
- working local/staging environment
- base security groups and roles
- custom module scaffolding
- initial navigation structure

### Milestone 1: Practice, Provider, and Patient Core

Must deliver:
- one clinic configuration record
- provider records
- patient records
- lead or new-patient creation flow
- patient profile screen

### Milestone 2: Intake and Consent

Must deliver:
- intake form templates
- intake submission storage
- consent templates
- consent signature recording
- intake and consent status visible from patient and appointment contexts

### Milestone 3: Scheduling and Appointment Hub

Must deliver:
- appointment types
- appointment creation and editing
- daily schedule screen
- appointment detail screen
- booking or appointment-request entry point
- appointment status flow including check-in readiness

### Milestone 4: Encounter and Note Workflow

Must deliver:
- encounter creation from appointment
- encounter note screen
- shared note structure
- note save/finalize path
- follow-up recommendation capture

### Milestone 5: Checkout, Invoice, and Payment

Must deliver:
- checkout session from encounter
- checkout lines for visit charges
- invoice creation from checkout
- payment recording for card and cash
- proof of payment or receipt
- updated visit financial status

### Milestone 6: Packages and Rebooking

Must deliver:
- package definition
- package assignment to patient
- package balance tracking
- package credit application at checkout
- recall or rebooking worklist
- next-visit recommendation surfaced for staff

### Milestone 7: Dashboard and Operational Visibility

Must deliver:
- home dashboard
- daily counts of visits
- revenue summary
- package usage summary
- rebooking or recall summary

### Milestone 8: Optional AI Layer

Must deliver:
- AI integration broker
- intake summary action in intake review
- draft note action in encounter note
- optional after-visit summary draft
- optional rebooking prompt support
- review and approval tracking for AI outputs

## 4. What Must Be Stable Before Moving to the Next Milestone

### Before Milestone 1

- Odoo environment boots reliably
- module loading is repeatable
- role and permission basics are understood

### Before Milestone 2

- patient and provider records can be created and edited reliably
- one clinic can be configured without hacks

### Before Milestone 3

- intake and consent records can be created, stored, and viewed
- staff can determine whether a patient is ready for a visit

### Before Milestone 4

- appointments can be created, scheduled, and opened from the daily schedule
- appointment detail acts as a stable hub for the visit

### Before Milestone 5

- providers can complete an encounter note without workflow confusion
- encounter status is clearly tied to the appointment

### Before Milestone 6

- checkout produces a correct invoice
- card and cash payments can be recorded reliably
- there is no need to fix invoices manually in the database

### Before Milestone 7

- package credits can be applied cleanly in checkout
- rebooking and recall states are visible and usable

### Before Milestone 8

- the full clinic workflow works without AI
- users can complete intake, scheduling, encounter, checkout, payment, and rebooking manually
- AI is clearly additive, not compensating for broken core UX

## 5. Which Odoo Base Modules Are Touched in Each Milestone

### Milestone 0

- `base`
- `contacts`
- `calendar`
- `website`
- `crm`
- `product`
- minimal `account`

### Milestone 1

- `base`
- `contacts`
- `crm`

### Milestone 2

- `base`
- `contacts`
- `website`

### Milestone 3

- `calendar`
- `website`
- `contacts`

### Milestone 4

- `base`
- `contacts`

### Milestone 5

- `product`
- minimal `account`
- optional limited `sale` usage only if it simplifies the flow

### Milestone 6

- `product`
- minimal `account`

### Milestone 7

- `base`
- minimal `account`

### Milestone 8

- `base`
- `website` only if AI touches patient-facing summaries later

Odoo-touch rule:
- if a milestone would require deep modification of `account`, `point_of_sale`, or `stock`, stop and reconsider the scope

## 6. Which Custom Modules Are Introduced in Each Milestone

### Milestone 0

- module scaffolding for all planned Phase 1 custom modules

### Milestone 1

- `hc_practice_core`
- `hc_patient_core`
- `hc_leads`

### Milestone 2

- `hc_intake`
- `hc_consent`
- `hc_documents` if needed for storing intake or consent attachments

### Milestone 3

- `hc_scheduling`

### Milestone 4

- `hc_encounter`

### Milestone 5

- `hc_checkout`
- `hc_billing_light`

### Milestone 6

- `hc_packages`
- `hc_retention`

### Milestone 7

- `hc_reporting`

### Milestone 8

- `hc_integration_ai`
- `hc_ai_intake_summary`
- `hc_ai_note_draft`
- optional `hc_ai_followup_draft`
- optional `hc_ai_retention`

Custom-module rule:
- do not introduce specialty-depth acupuncture modules in Phase 1 unless the shared workflow is already stable and they are proven necessary

## 7. Scope Traps During Implementation

- letting one pilot clinic push the build toward insurance billing
- over-modeling accounting so invoices and payments become the main project
- treating package credits like a full membership or subscription engine
- pulling in `point_of_sale` because retail might matter later
- adding inventory models before a real need exists
- making the appointment model too generic for future specialties
- building too much charting structure before providers can complete a note quickly
- using AI to cover workflow gaps instead of fixing the workflow
- customizing Odoo internals deeply when a lighter custom model would be cleaner
- designing for multi-specialty support during Phase 1
- building extra dashboards before the visit loop is working
- splitting one task across too many screens or modules

Implementation trap rule:
- if a task does not directly improve the Phase 1 clinic workflow, delay it

## 8. Suggested Internal Demo Checkpoints

### Checkpoint A: Basic Clinic Setup

Show:
- clinic setup
- provider creation
- patient creation
- lead capture

Purpose:
- verify the system can represent one clinic and its people

### Checkpoint B: Intake and Consent Flow

Show:
- new patient intake request
- intake completion
- consent signing
- staff visibility of completion state

Purpose:
- verify pre-visit onboarding works cleanly

### Checkpoint C: Scheduling Flow

Show:
- appointment creation
- schedule view
- appointment detail as visit hub

Purpose:
- verify the clinic can prepare the day

### Checkpoint D: Encounter Flow

Show:
- check-in
- encounter creation
- note completion
- follow-up recommendation

Purpose:
- verify provider workflow is usable

### Checkpoint E: Financial Closeout

Show:
- checkout from encounter
- invoice creation
- card payment
- cash payment
- receipt or payment confirmation

Purpose:
- verify the clinic can finish a visit and get paid

### Checkpoint F: Package and Rebooking Flow

Show:
- assign package
- consume package credit at checkout
- see remaining balance
- mark patient for rebooking or recall

Purpose:
- verify the repeat-care business loop works

### Checkpoint G: Full Non-AI Workflow

Show:
- end-to-end patient flow from lead to payment and recall without AI

Purpose:
- confirm Phase 1 is independently useful

### Checkpoint H: Optional AI Overlay

Show:
- AI intake summary
- AI draft note
- AI after-visit summary draft or rebooking prompt
- explicit user review and acceptance

Purpose:
- confirm AI improves the workflow without becoming required

## Recommended Sequence Summary

Build in this order:

1. foundation
2. clinic and patient core
3. intake and consent
4. scheduling
5. encounter
6. checkout and payment
7. packages and retention
8. dashboard
9. optional AI

That sequence is the most realistic low-stress path because it produces a usable clinic workflow before it introduces optional intelligence or future-facing complexity.
