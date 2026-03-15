# PLATFORM ARCHITECTURE

Status:
- Planning document only
- No implementation work is authorized from this file

## 1. System Architecture Overview

The platform should be a modular vertical SaaS built on `Odoo Community`, with a narrow core for shared clinic operations and isolated extension modules for specialty-specific workflows.

Architecture goals:
- Keep the first release usable for acupuncture clinics without hard-coding acupuncture into the entire system
- Reuse standard Odoo capabilities where they are operationally strong
- Keep clinical and specialty logic in custom modules
- Make AI assistive, optional, and always reviewable
- Preserve a migration path to `Odoo Enterprise` if support or operational needs later justify it

High-level layers:

1. Presentation layer
- Odoo web UI for staff and providers
- Patient-facing web flows for intake, booking, forms, and confirmations

2. Shared application core
- Patient lifecycle
- Scheduling
- Intake and consent
- Encounter records
- Checkout, invoicing, payments, reminders, reporting

3. Specialty extension layer
- Acupuncture module set
- Massage therapy module set
- Chiropractic module set

4. AI services layer
- Summarization, drafting, scoring, and QA services
- Strictly optional per tenant and per workflow

5. Integration layer
- Payment processor
- Email and SMS delivery
- Calendar sync
- Document storage and OCR
- Later: accounting sync, clearinghouse, fax

6. Platform operations layer
- Tenant provisioning
- Configuration management
- backups
- logging
- audit support
- upgrade orchestration

Design rule:
- Odoo should manage business objects and workflows.
- External services should handle specialized AI and infrastructure concerns.
- Custom code should extend, not replace, stable Odoo primitives.

## 2. Core Domain Models

The system should use a deliberately small shared domain model. Specialty modules may extend these models but should not fork them.

### Shared business and patient models

- `Practice`
  - tenant account representing one clinic or one legal practice
  - owns configuration, branding, timezone, specialty flags, billing plan

- `Location`
  - physical site or service area
  - supports future multi-location expansion without forcing it into Phase 1

- `User`
  - internal account for provider, front desk, owner, biller, admin

- `Provider`
  - clinical staff profile
  - license info, specialties, booking rules, schedule preferences

- `Patient`
  - person receiving services
  - demographics, communications preferences, risk flags, household links

- `Household`
  - optional grouping for family scheduling and billing relationships
  - should remain dormant until clearly needed

- `Lead`
  - pre-patient inquiry or booking prospect
  - referral source, interest, conversion status

### Intake and consent models

- `IntakeFormTemplate`
  - reusable structure for specialty-specific intake packs

- `IntakeSubmission`
  - patient-completed intake response
  - stores both structured answers and source snapshots

- `ConsentTemplate`
  - versioned legal/operational form

- `ConsentRecord`
  - signed consent instance linked to patient, practice, and version

### Scheduling and care-delivery models

- `AppointmentType`
  - service definition, duration, booking rules, price defaults

- `Appointment`
  - scheduled visit, provider, room/resource, status, reminders, source

- `Encounter`
  - canonical visit record linked to appointment or walk-in
  - should remain the central clinical event model

- `EncounterSection`
  - structured note sections such as subjective, objective, assessment, plan, treatment details
  - allows a shared note engine with specialty extensions

- `CarePlan`
  - recommended visit cadence, goals, next steps
  - generic enough for multiple specialties

### Financial and retention models

- `CheckoutSession`
  - transactional wrapper between encounter completion and final invoice/payment capture
  - holds services, retail items, package application, discounts, and payment intent

- `CheckoutLine`
  - individual service, product, package redemption, or adjustment attached to checkout

- `Invoice`
  - billable charges linked to checkout, appointments, products, packages

- `Payment`
  - captured patient payment and reconciliation status
  - early supported tender types: card, cash, package credit, gift certificate

- `GiftCertificate`
  - prepaid stored-value or service-credit instrument
  - supports issue, balance tracking, redemption, and optional expiration policy

- `Package`
  - prepaid bundle or membership definition

- `PackageBalance`
  - patient-specific remaining units, expiration, status

- `Product`
  - retail item, supplement, herb, or clinic supply

- `PaymentAllocation`
  - links payment or credit usage to invoice or checkout balance

- `InventoryMovement`
  - stock changes where inventory tracking is enabled

- `CommunicationEvent`
  - reminders, follow-up, recall messages, campaign events

- `RetentionSignal`
  - computed record for rebooking risk, lapse status, and outreach priority

### AI support models

- `AISession`
  - request metadata, user, tenant, feature type, timestamps

- `AIPromptContext`
  - normalized source bundle used for generation or scoring

- `AIOutput`
  - draft summary, note, prompt, or score
  - stores status such as draft, reviewed, accepted, rejected

- `AIReviewAction`
  - captures user review and approval action for auditability

## 3. Odoo Base Modules to Reuse

The platform should reuse Odoo where it is already strong, and avoid rewriting those capabilities.

Recommended Odoo base:

- `base`
  - users, access model, core ORM

- `contacts`
  - foundation for patients, households, referral contacts, providers

- `calendar`
  - internal scheduling primitives

- `website`
  - public intake and booking entry points

- `crm`
  - lead capture and referral tracking

- `sale` and `account`
  - simple invoice and payment-related workflows

- `point_of_sale`
  - optional only
  - use if retail-heavy clinics need faster front-desk checkout
  - should not be a Phase 1 dependency unless validated by pilots

- `product`
  - services, packages, retail items, herbs, supplements

- `stock`
  - only if inventory is actually needed in the current phase

- `mass_mailing` or equivalent lightweight messaging support
  - for campaigns and retention workflows if kept simple

- `documents` equivalent only if available and supportable in the chosen edition path
  - otherwise use a narrow custom document model integrated with attachments

Use cautiously:

- `subscription`
  - only if the operational model matches packages or memberships cleanly
  - otherwise build a lighter custom package ledger

- `website_appointment` style scheduling modules
  - only if they fit the desired booking experience without heavy patching

Avoid leaning on:

- broad HR modules
- manufacturing logic
- complex accounting features not required for the niche
- community marketplace healthcare modules as hard dependencies for core workflow

Rule:
- Reuse Odoo for operational plumbing.
- Build custom modules for clinical workflow, specialty UX, and AI orchestration.
- Keep Phase 1 financial workflows light enough that fuller accounting can remain optional.

## 4. Custom Module Boundaries

Custom code should be split into small, purpose-specific modules with clear ownership and minimal cross-coupling.

### Platform core custom modules

- `hc_practice_core`
  - practice settings
  - tenant metadata
  - provider profile extensions
  - shared terminology and feature flags

- `hc_patient_core`
  - patient record extensions beyond generic contacts
  - household links
  - patient identifiers
  - communication preferences

- `hc_intake`
  - intake templates, submissions, structured responses, patient onboarding flow

- `hc_consent`
  - versioned consent templates, signatures, consent status checks

- `hc_scheduling`
  - appointment types, booking rules, resource assignment, waitlist, rebooking cues

- `hc_encounter`
  - encounter object, note engine, shared SOAP-style sections, signatures, locking rules

- `hc_billing_light`
  - self-pay checkout, package consumption, invoices, receipts, basic balance handling
  - supported early tenders: card, cash, package credit, gift certificate

- `hc_checkout`
  - checkout session lifecycle
  - checkout lines for services and retail
  - discount and adjustment handling
  - conversion from encounter to invoiceable transaction

- `hc_gift`
  - gift certificate issuing, redemption, balance tracking

- `hc_retail_ops`
  - optional retail add-ons in checkout
  - optional POS-style workflow
  - inventory updates only when enabled

- `hc_retention`
  - reminders, recall logic, rebooking prompts, inactive-patient workflows

- `hc_reporting`
  - operational dashboard, retention metrics, provider utilization, referral tracking

- `hc_documents`
  - attachment categories, intake scans, visit files, audit-friendly document linkage

### Integration modules

- `hc_integration_payments`
  - payment processor abstraction

- `hc_integration_messaging`
  - email and SMS provider abstraction

- `hc_integration_calendar`
  - external calendar sync if needed

- `hc_integration_ai`
  - broker between Odoo and external AI services

- `hc_integration_storage`
  - document/object storage policy if attachment storage is externalized

### Guardrails for module boundaries

- No custom module should directly patch Odoo core source.
- Shared clinical abstractions belong in `hc_encounter`, not in an acupuncture module.
- Specialty modules may extend schemas and views, but should not redefine shared workflows.
- Integration modules should expose stable interfaces so vendors can change later.
- Light billing and payment recording should not require enabling full accounting complexity in every tenant.

## 5. Specialty Extension Model

Specialty logic must remain isolated so that:
- the shared core stays stable
- new specialties can be added without cloning the platform
- unsupported specialties do not complicate the base product

### Extension pattern

Each specialty should be modeled as:
- a feature flag at the practice level
- a set of add-on modules
- extra intake templates
- extra note sections and templates
- specialty-specific reports and automations

### Acupuncture extension modules

- `hc_acu_intake`
  - TCM symptom patterns, constitutional intake, treatment goals

- `hc_acu_charting`
  - point selection, meridian/body maps, treatment details

- `hc_acu_careplan`
  - treatment course planning, frequency recommendations, progress checkpoints

- `hc_acu_herbs`
  - herb/formula catalog, patient recommendations, optional inventory tie-in

### Massage therapy extension modules

- `hc_massage_intake`
  - contraindications, pressure preferences, body area priorities

- `hc_massage_charting`
  - body region work log, modalities, therapist notes

- `hc_massage_ops`
  - outcall logic, tips, room-turnover preferences, package handling

### Chiropractic extension modules

- `hc_chiro_exam`
  - exam templates, ROM, ortho/neuro findings

- `hc_chiro_careplan`
  - recurring visit plans, progress tracking, treatment milestones

- `hc_chiro_billing_plus`
  - future-only module for more complex billing support
  - should stay separate from the base product

### Extension rules

- Specialty modules may add fields to `Encounter`, `AppointmentType`, and `IntakeSubmission`.
- Specialty modules must not own tenant provisioning, patient identity, or payment infrastructure.
- A practice should activate only the specialty modules it actually uses.

## 6. AI Services Architecture

AI services must be optional, reviewable, and loosely coupled to Odoo.

### AI design principles

- AI is assistive, not authoritative
- Every output is a draft or suggestion
- The user can accept, edit, or reject the result
- AI features can be disabled per practice and per workflow
- Source inputs should be inspectable

### AI architecture components

1. In-app AI entry points
- buttons or actions inside intake review, charting, follow-up, and reporting screens

2. AI orchestration layer
- `hc_integration_ai` collects structured context from Odoo
- normalizes data into a compact request format
- enforces tenant policy and feature flags

3. External AI worker service
- isolated service for prompt assembly, model calls, post-processing, and retry logic
- should not embed Odoo business logic

4. AI result store
- generated summaries, drafts, confidence metadata, and review state stored back in Odoo

5. Review and approval layer
- user sees the generated content, source references, and actions taken

### Phase 1 AI services

- intake summarizer
- draft note assistant
- after-visit summary draft
- rebooking and retention prompts

### AI control flow

1. User triggers an AI action inside a workflow
2. Odoo collects only the required source records
3. AI broker creates a minimal context payload
4. External AI service returns a draft object
5. Odoo stores the output as unapproved
6. User reviews, edits, accepts, or rejects
7. Accepted output is committed into the operational workflow

### AI boundary decisions

Keep inside Odoo:
- permissions
- workflow state
- source record lookup
- review actions

Keep outside Odoo:
- prompt templates
- model vendor handling
- token-intensive processing
- experimentation with model providers

## 7. Data Flow Through the Workflow Spine

The workflow spine should be simple and consistent across specialties.

### Core data flow

1. Lead intake
- patient comes from website, referral, manual entry, or online booking
- data lands in `Lead` or directly in `Patient` depending on workflow

2. Patient onboarding
- patient completes intake and consent
- responses create `IntakeSubmission` and `ConsentRecord`
- important structured data is copied into patient-facing summary fields

3. Scheduling
- appointment is created from staff action or self-booking
- reminders and confirmation events attach to the appointment

4. Visit preparation
- provider sees intake, prior encounters, package balance, and alerts
- optional AI intake summarizer prepares a review draft

5. Encounter and note creation
- appointment check-in opens or links to an `Encounter`
- shared note sections load
- specialty extension sections appear only if enabled
- optional AI draft assistant creates a reviewable note draft

6. Checkout
- encounter output is handed to a `CheckoutSession`
- services and optional retail items become `CheckoutLine` entries
- package credit, gift certificate, card, or cash can be applied
- invoice is created from the finalized checkout
- payment is recorded and allocated to invoice or checkout balance
- follow-up recommendation and next-visit timing are captured

7. Invoicing and payment completion
- the financial spine continues as `checkout -> invoice -> payment`
- retail inventory is adjusted only if inventory tracking is enabled
- accounting handoff remains lightweight in Phase 1

8. Post-visit follow-up
- after-visit summary can be drafted and sent
- retention system tracks next recommended action

9. Reporting and retention
- appointment, encounter, revenue, and communication events feed dashboards
- rebooking signals generate work queues or suggested outreach

### Workflow spine rule

The platform should revolve around this chain:

`lead -> patient -> intake/consent -> appointment -> encounter -> checkout -> invoice -> payment -> follow-up -> retention`

Every specialty-specific feature should plug into this chain rather than create a parallel workflow.

### Financial workflow extension rules

- `CheckoutSession` is the boundary between care delivery and business operations.
- Early payment support is limited to card, cash, package credit, and gift certificate.
- Retail sales should ride the same checkout flow rather than create a separate business subsystem.
- POS-style checkout is optional and should only be enabled for practices that actually need it.
- Inventory updates should be feature-flagged so service-only clinics do not inherit retail complexity.
- Phase 1 should focus on light billing and payment recording, not full accounting depth.

## 8. Multi-Tenant SaaS Deployment Model

For a solo founder, the simplest maintainable SaaS model is:
- one shared application codebase
- one database per tenant
- standardized deployment and configuration templates

### Recommended tenancy model

Use database-per-tenant on a shared infrastructure stack.

Reasons:
- clearer data isolation
- easier backup and restore per clinic
- easier tenant export or migration
- lower blast radius than row-level multi-tenancy
- better fit with Odoo’s natural database separation model

### Deployment shape

- shared reverse proxy
- shared Odoo application image/build per release
- worker processes sized conservatively
- one Postgres cluster containing separate databases per tenant
- external object storage for attachments if operationally justified
- isolated AI worker service

### Tenant lifecycle

- provision new practice from a standard template
- enable only required core and specialty modules
- apply default configuration pack for the specialty
- seed intake templates, consent templates, and appointment types
- enable retail, gift certificate, and inventory features only when the practice actually needs them

### Operational constraints for solo-founder manageability

- no tenant-specific forks
- no one-off custom modules for individual clinics
- configuration-driven variation wherever possible
- a limited set of supported deployment topologies
- only a small number of external vendors in early phases

### When to avoid full SaaS complexity

If early pilots are very small, it may be simpler to start with a limited number of manually provisioned tenant databases rather than build elaborate self-service tenant automation immediately.

## 9. Security and PHI Considerations

This platform must be designed as handling sensitive health-related data from the beginning, even if formal compliance scope is phased.

### Core security principles

- least-privilege access
- per-role permissions
- tenant isolation
- auditability of sensitive actions
- encrypted transport everywhere
- minimal data exposure to AI and integrations

### Financial data considerations

- payment records and tender types should have their own access controls
- gift certificate and package-credit redemption must be auditable
- refund and adjustment actions should be logged even if advanced accounting is deferred
- retail inventory changes should be traceable when inventory is enabled

### PHI-sensitive areas

- patient demographics
- intake answers
- encounter notes
- consents
- attachments and uploaded documents
- AI prompt payloads and outputs
- message content

### Required controls for pilots

- role-based access for owner, provider, front desk, and admin
- strict tenant separation
- TLS in transit
- encrypted backups
- documented backup and restore process
- audit trail for chart creation, edits, signatures, and AI acceptance
- vendor review for every external service that may process PHI

### AI-specific controls

- AI features opt-in by tenant
- no silent background generation of clinical text without user request
- minimize prompt payloads to only necessary fields
- store review state and user acceptance
- do not let AI outputs overwrite finalized records automatically

### Operational cautions

- Do not promise more compliance coverage than is actually implemented.
- Do not assume all Odoo hosting models are suitable for PHI.
- Avoid unnecessary third-party community modules that expand the attack surface.
- Treat document handling and messaging as high-risk surfaces, not minor details.

### Compliance scope caution

Early phase design should aim for defensible privacy and security practices, but the business should not market itself as solving full clinical compliance complexity until the hosting, vendor, audit, and documentation posture are mature.

## 10. Upgrade Strategy to Keep Odoo Maintainable

Maintainability depends more on discipline than on tooling.

### Upgrade principles

- never patch Odoo core directly
- keep custom modules small and clearly named
- minimize deep view overrides
- prefer extension hooks and additive models over invasive rewrites
- isolate specialty modules from shared modules
- avoid community dependencies that are not actively maintainable

### Version strategy

- choose one Odoo major version and stay stable through Phase 1
- avoid frequent base-platform upgrades during early customer onboarding
- batch feature work between planned upgrade windows

### Customization strategy

Allowed:
- new models
- additive fields
- isolated form and list view extensions
- workflow automation around standard models
- light financial wrappers around standard invoice and payment models

Discouraged:
- replacing core scheduling internals
- rewriting accounting flows
- broad JS customization unless essential
- using many low-quality marketplace add-ons
- turning Phase 1 checkout into a full accounting subsystem

### Release strategy

- maintain one product release line for all tenants
- test upgrades on an internal staging tenant first
- then on one pilot tenant
- then roll out broadly

### Data migration strategy

- keep internal identifiers stable
- use import adapters for competitor migration, but keep them separate from the core runtime
- maintain explicit migration scripts between custom module versions

### Enterprise-switch readiness

Keep the architecture ready for a later `Odoo Enterprise` move by:
- not binding core logic to Community-only hacks
- keeping custom business modules independent of hosting assumptions
- using integration abstractions for functions that Enterprise may later cover better

## Recommended Architecture Summary

The platform should be:
- `Odoo Community` based
- database-per-tenant
- shared-core plus specialty-extension driven
- self-pay and operationally focused first
- AI-assisted but never AI-dependent

The first release should optimize for:
- acupuncture clinics
- one workflow spine
- minimal vendor surface area
- low operational surprise
- clean upgradeability

If a design decision increases support burden, tenant-specific branching, or upgrade fragility, it should be rejected unless it clearly unlocks repeatable revenue.
