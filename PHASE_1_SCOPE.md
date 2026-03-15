# PHASE 1 SCOPE

Status:
- Planning document only
- No implementation work is authorized from this file

## 1. Phase 1 Mission

Deliver a usable first product for one acupuncture clinic that supports the full daily visit workflow from intake through payment and rebooking.

Primary mission:
- make the clinic's core visit loop run in one system without manual rescue

Workflow spine to preserve:
- `lead -> patient intake -> consent -> appointment -> encounter -> checkout -> invoice -> payment -> follow-up -> retention`

Phase 1 target:
- solo or small acupuncture clinic
- primarily cash-pay
- no insurance-heavy billing dependency
- no multi-specialty support

Phase 1 is successful if one real clinic can use the system for normal patient visits and the founder can support it without turning the business into a custom ERP or billing operation.

## 2. Required Capabilities

These capabilities must exist for the product to function as intended.

### Patient and clinic setup

- practice configuration for one clinic
- provider records
- patient records
- referral source or basic lead capture

### Intake and consent

- digital intake forms
- intake submission storage
- consent forms
- consent status tracking

### Scheduling

- appointment types
- appointment booking by staff
- basic online or intake-linked booking path
- appointment statuses
- reminders and confirmations

### Clinical workflow

- encounter record linked to appointment
- fast shared note structure
- note save and review flow
- follow-up recommendation capture

### Checkout and payment

- checkout session linked to encounter
- charge lines for visit services
- invoice creation from checkout
- payment recording
- early payment support for card, cash, and package credit
- receipt or proof of payment
- outstanding balance visibility

### Packages and retention

- create package definitions
- assign package to patient
- track package balance
- apply package credit at checkout
- capture next-visit recommendation
- support rebooking prompt or recall status

### Basic owner visibility

- visits completed
- revenue collected
- package usage
- patients due for rebooking

## 3. Recommended Capabilities

These are useful for Phase 1, but the product can still function without them.

- AI intake summary
- AI draft note assistant
- AI after-visit summary draft
- gift certificate support
- direct website booking that feels polished rather than just functional
- simple document attachments for intake scans or imported files
- basic patient communication history
- limited retail item add-on during checkout if it is trivial to include

Rule:
- recommended features are only allowed if they do not delay the required workflow spine

## 4. Explicitly Rejected Features

These features are out of scope for Phase 1.

- insurance claims submission
- clearinghouse integrations
- payer-specific billing workflows
- coding assistance for insurance billing
- chiropractic workflows
- massage therapy workflows
- multi-specialty configuration
- multi-location practice support
- mandatory POS
- advanced retail management
- advanced inventory tracking
- herb inventory depth
- memberships more complex than simple package credits
- full accounting customization
- advanced reconciliation
- telehealth
- native mobile apps
- voice AI receptionist
- autonomous clinical advice
- AI that changes records without user review
- tenant-specific one-off customizations

Hard rejection rule:
- if a feature pulls the product toward insurance-heavy EHR scope, broad ERP consulting, or multi-specialty sprawl, reject it for Phase 1

## 5. Phase 1 Module List

### Mandatory custom modules

- `hc_practice_core`
- `hc_patient_core`
- `hc_leads`
- `hc_intake`
- `hc_consent`
- `hc_scheduling`
- `hc_encounter`
- `hc_checkout`
- `hc_billing_light`
- `hc_packages`
- `hc_retention`
- `hc_reporting`
- `hc_documents`

### Optional Phase 1 modules

- `hc_integration_ai`
- `hc_ai_intake_summary`
- `hc_ai_note_draft`
- `hc_ai_followup_draft`
- `hc_gift`

### Deferred modules

- `hc_retail_ops`
- `hc_inventory_light`
- `hc_pos_bridge`
- `hc_memberships`
- `hc_accounting_bridge`
- `hc_acu_*` specialty-depth modules beyond the minimum shared workflow
- all massage modules
- all chiropractic modules
- later AI analysis modules

### Odoo base modules to reuse in Phase 1

- `base`
- `contacts`
- `calendar`
- `website`
- `crm`
- `product`
- minimal `account`

Use only if trivial and clearly justified:
- `sale`
- `mass_mailing`

Explicitly not central to Phase 1:
- `point_of_sale`
- `stock`
- deeper accounting features

## 6. Minimal Data Model

The minimal Phase 1 data model should stay small and aligned with the workflow spine.

### Core entities

- `Practice`
- `Provider`
- `Patient`
- `Lead`
- `AppointmentType`
- `Appointment`
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

### Minimal relationships

- a `Practice` has many `Providers`, `Patients`, `Appointments`, and templates
- a `Lead` may convert into a `Patient`
- a `Patient` can submit many intake forms and sign many consents
- an `Appointment` belongs to a `Patient` and a `Provider`
- an `Appointment` can create one `Encounter`
- an `Encounter` creates or links to one `CheckoutSession`
- a `CheckoutSession` produces one `Invoice`
- an `Invoice` can have one or more `Payment` records
- a `Patient` can have one or more `PackageBalance` records
- a `PackageBalance` can be consumed at checkout
- a `RetentionSignal` belongs to a `Patient`

### Minimal payment types

- card
- cash
- package credit

Optional only if easy:
- gift certificate

## 7. Minimal UI Screens

The Phase 1 UI should support the full visit loop with the fewest screens possible.

### Staff and provider screens

- login and clinic home/dashboard
- daily schedule view
- patient list and patient profile
- new patient / lead intake view
- appointment create/edit view
- intake review view
- consent status view
- encounter note view
- checkout view
- invoice and payment view
- package management view
- rebooking / recall worklist
- simple owner metrics dashboard

### Patient-facing screens

- online booking or appointment request entry
- intake form completion
- consent form signing
- appointment confirmation screen

### UI rule

- if a screen does not support the Phase 1 spine directly, it should probably not exist yet

## 8. AI Features Allowed in Phase 1

Allowed AI in Phase 1:

- intake summarizer
- draft note assistant
- after-visit summary draft
- rebooking prompt support

Conditions:

- all AI features must be optional
- all AI outputs must be reviewable and editable
- the product must remain useful without AI enabled
- AI must not silently finalize clinical or financial records

Recommended AI priority order:

1. `hc_ai_intake_summary`
2. `hc_ai_note_draft`
3. `hc_ai_followup_draft`
4. `hc_ai_retention`

## 9. AI Features Explicitly Deferred

Defer these AI features until later phases:

- missing-chart QA
- business copilot
- OCR intake extraction
- coding and billing assistance
- claim support
- voice front-desk agent
- patient-facing clinical chat
- any autonomous treatment or diagnosis support

Reason for deferral:
- they increase risk, support burden, or workflow complexity before the base system is proven

## 10. Build Order for Modules

Recommended build order for one founder using AI assistance:

1. Odoo base setup: `base`, `contacts`, `calendar`, `website`, `crm`, `product`, minimal `account`
2. `hc_practice_core`
3. `hc_patient_core`
4. `hc_leads`
5. `hc_intake`
6. `hc_consent`
7. `hc_scheduling`
8. `hc_encounter`
9. `hc_checkout`
10. `hc_billing_light`
11. `hc_packages`
12. `hc_retention`
13. `hc_reporting`
14. `hc_documents`
15. `hc_integration_ai`
16. `hc_ai_intake_summary`
17. `hc_ai_note_draft`
18. optional `hc_ai_followup_draft`
19. optional `hc_gift`

Build-order rule:
- do not build specialty depth before the shared visit loop works
- do not build optional AI before the non-AI workflow is stable
- do not build POS, inventory, or accounting bridges during the initial Phase 1 build

## 11. What a Phase 1 Demo Must Show

The demo must prove one complete clinic workflow.

### Required demo storyline

1. Create or receive a new patient lead
2. Convert the lead or create the patient
3. Send and complete intake and consent
4. Book the appointment
5. Open the appointment and review intake
6. Create and complete the encounter note
7. Optionally generate an AI note draft and review it
8. Move into checkout
9. Create the invoice
10. Record payment by card, cash, or package credit
11. Show updated package balance if a package was used
12. Capture follow-up timing
13. Rebook or flag for recall
14. Show the result on a basic owner dashboard

### Demo quality bar

- no manual patching of records behind the scenes
- no fallback to external spreadsheets or payment notes
- no dependency on insurance logic
- AI, if shown, must be clearly optional

## 12. What Signals Indicate Phase 1 Success

Product signals:

- one acupuncture clinic can use the system for real visits
- the shared workflow spine works end to end
- providers can complete notes without hating the experience
- checkout and payment recording are reliable
- package credits are usable in normal front-desk flow

Business signals:

- at least one clinic says the system reduces weekly admin pain
- a pilot clinic is willing to continue using it after initial testing
- onboarding can be repeated without one-off development work

Founder signals:

- support requests are understandable and bounded
- upgrades and fixes do not require rewriting core Odoo behavior
- the founder is not being pulled into insurance, accounting, or specialty-expansion pressure in Phase 1

## 13. Scope Traps to Avoid

- adding insurance claims because one pilot asks for it
- adding chiropractic or massage support before acupuncture is stable
- building a fancy charting system before the base encounter flow is usable
- turning package handling into a subscription accounting project
- adding POS because a clinic sells a few retail items
- adding inventory because herbs might matter later
- building too many dashboards before the core workflow works
- making AI a requirement instead of a time-saver
- over-customizing Odoo views and internals for edge cases
- accepting tenant-specific workflow branches
- building mobile apps before the web workflow is solid
- turning Phase 1 into a broad practice-management suite instead of a narrow visit-loop product

## Phase 1 Boundary Summary

Phase 1 is:
- one acupuncture clinic type
- one shared workflow spine
- light billing and payment recording
- package-credit support
- optional AI assistance
- one founder-manageable build

Phase 1 is not:
- a full EHR
- a billing platform
- a POS platform
- an inventory system
- a multi-specialty suite
- a mobile product
