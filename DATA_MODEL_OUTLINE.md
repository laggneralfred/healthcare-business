# DATA MODEL OUTLINE

Status:
- Planning document only
- No implementation work is authorized from this file

## 1. Phase 1 Data Model Principles

The Phase 1 data model must support one acupuncture clinic running the core visit workflow without dragging in insurance, full accounting, or multi-specialty complexity.

Primary rule:
- preserve the workflow spine:
  `lead -> patient intake -> consent -> appointment -> encounter -> checkout -> invoice -> payment -> follow-up -> retention`

Phase 1 data modeling principles:

- Include only entities required to make the Phase 1 workflow usable.
- Prefer extending stable Odoo base models where they already fit.
- Use custom models for clinical workflow, intake, checkout, packages, and retention.
- Keep financial data light: invoice, payment, package credit, and simple balances only.
- Treat AI as optional and record only enough review state to keep outputs auditable.
- Do not model insurance claims, clearinghouse logic, inventory-heavy retail, or multi-specialty structures beyond a minimal future-ready hook.
- Avoid schema choices that force deep Odoo accounting customization.

Design bias:
- one clinic type
- one shared workflow spine
- one founder-manageable scope

## 2. Required Entities

These are the minimum entities needed for Phase 1.

| Entity | Purpose | Odoo reuse or custom | Required |
|---|---|---|---|
| `Practice` | Clinic-level settings, branding, timezone, feature flags | Custom | Yes |
| `Provider` | Clinical staff profile and scheduling context | Extends Odoo user/contact models | Yes |
| `Patient` | Person receiving care, with communication and status fields | Extends Odoo contact model | Yes |
| `Lead` | New inquiry or prospective patient before conversion | Extends Odoo CRM lead | Yes |
| `AppointmentType` | Service definitions, duration, price defaults | Custom, may reference Odoo product | Yes |
| `Appointment` | Scheduled visit linking patient, provider, and service type | Extends Odoo calendar/event patterns or custom scheduling model | Yes |
| `IntakeFormTemplate` | Defines intake questions for Phase 1 workflows | Custom | Yes |
| `IntakeSubmission` | Stores patient intake responses and source snapshot | Custom | Yes |
| `ConsentTemplate` | Versioned form definition for clinic policies and treatment consent | Custom | Yes |
| `ConsentRecord` | Signed consent instance linked to patient and template version | Custom | Yes |
| `Encounter` | Core visit record created from an appointment | Custom | Yes |
| `EncounterSection` | Structured note sections within the encounter | Custom | Yes |
| `CheckoutSession` | Bridge from encounter completion to financial closeout | Custom | Yes |
| `CheckoutLine` | Service charge, adjustment, or package-credit application line | Custom | Yes |
| `Invoice` | Light financial record for billed charges | Reuses minimal Odoo accounting models | Yes |
| `Payment` | Payment record for card, cash, and package credit usage | Extends minimal Odoo payment/account concepts | Yes |
| `Package` | Prepaid visit bundle definition | Custom | Yes |
| `PackageBalance` | Patient-owned remaining units or credit from a package | Custom | Yes |
| `RetentionSignal` | Rebooking status, lapse marker, or next-action reminder | Custom | Yes |

### Optional AI review records in Phase 1

These are allowed in Phase 1 if AI features are enabled.

| Entity | Purpose | Odoo reuse or custom | Required only if AI is enabled |
|---|---|---|---|
| `AISession` | Tracks an AI request event, timing, user, and feature type | Custom | Optional |
| `AIOutput` | Stores generated draft text or recommendation with state | Custom | Optional |
| `AIReviewAction` | Captures user acceptance, edit, rejection, or finalization | Custom | Optional |

### Required payment types

The required payment model must support:

- card
- cash
- package credit

Optional only if easy:
- gift certificate

## 3. Optional Later Entities

These entities should not be part of the strict Phase 1 minimum unless they prove necessary during pilots.

| Entity | Why deferred |
|---|---|
| `GiftCertificate` | Useful, but not essential to the first clinic workflow |
| `Product` | Only needed if retail products are actually sold in Phase 1 |
| `InventoryMovement` | Not needed unless stock tracking is enabled |
| `PaymentAllocation` | Can remain implicit at first if invoice-payment relationships stay simple |
| `CarePlan` | Useful later, but not required for the first shared workflow |
| `CommunicationEvent` | Helpful for message history, but can be deferred if reminder logs are simple |
| `Household` | Not required for single-clinic Phase 1 |
| `Location` | Not required if the first clinic uses one site only |
| `AIPromptContext` | Nice for richer auditing, but can be deferred if `AISession` and `AIOutput` are enough |
| `GiftCertificateRedemption` | Defer unless gift support is enabled |
| `RetailSale` | Do not introduce a separate retail subsystem in Phase 1 |
| `Membership` | More complex than simple package credits |
| `InsuranceClaim` | Explicitly out of scope |
| `Payer` | Explicitly out of scope |
| `ClaimSubmission` | Explicitly out of scope |

Optional-later rule:
- if an entity is not required to complete the Phase 1 spine for one acupuncture clinic, it should stay out of the initial schema

## 4. Key Relationships

The data model should reflect the core visit loop clearly.

### Practice and people

- one `Practice` has many `Providers`
- one `Practice` has many `Patients`
- one `Practice` owns many templates such as `IntakeFormTemplate` and `ConsentTemplate`
- one `Lead` belongs to one `Practice`
- one `Lead` may convert to one `Patient`

### Intake and consent

- one `Patient` can have many `IntakeSubmission` records
- one `IntakeSubmission` belongs to one `Patient`
- one `IntakeSubmission` is created from one `IntakeFormTemplate`
- one `Patient` can have many `ConsentRecord` entries
- one `ConsentRecord` belongs to one `ConsentTemplate`

### Appointment and encounter

- one `Appointment` belongs to one `Patient`
- one `Appointment` belongs to one `Provider`
- one `Appointment` references one `AppointmentType`
- one `Appointment` may create one `Encounter`
- one `Encounter` belongs to one `Patient`
- one `Encounter` belongs to one `Provider`
- one `Encounter` may contain many `EncounterSection` records

### Checkout and payment

- one `Encounter` creates or links to one `CheckoutSession`
- one `CheckoutSession` contains many `CheckoutLine` records
- one `CheckoutSession` creates one `Invoice`
- one `Invoice` can have one or more `Payment` records
- one `Payment` belongs to one `Patient`
- one `Payment` should identify its tender type: `card`, `cash`, or `package_credit`

### Packages and retention

- one `Package` can be sold to many patients
- one `Patient` can hold many `PackageBalance` records
- one `PackageBalance` references one `Package`
- one `CheckoutLine` may consume one `PackageBalance`
- one `Patient` can have one or more `RetentionSignal` records over time

### Optional AI review flow

- one `AISession` belongs to one user action in one workflow context
- one `AISession` can produce one or more `AIOutput` records
- one `AIOutput` may link to one `Encounter`, `IntakeSubmission`, or `RetentionSignal` context
- one `AIReviewAction` belongs to one `AIOutput`

## 5. Odoo Base Model Reuse

Phase 1 should reuse Odoo where it reduces work and does not distort the product.

### Strong reuse candidates

- `res.partner`
  - base for `Patient`
  - base for external contacts and possibly simplified provider contact records

- `res.users`
  - base for internal staff accounts
  - supports provider login and permissions

- `crm.lead`
  - base for `Lead`
  - useful for referral-source capture and new-patient conversion

- `product.template` or `product.product`
  - base for visit services and later retail items
  - can support `AppointmentType` pricing references

- minimal `account.move`
  - base for Phase 1 invoice records

- minimal payment/account objects
  - base for card and cash recording, if used lightly

### Reuse with caution

- calendar/event-based scheduling primitives
  - useful if they fit without heavy customization
  - avoid deep coupling if a custom appointment model is cleaner

- `sale.order`
  - use only if it helps checkout-to-invoice flow without adding complexity

### Odoo reuse rule

- Reuse Odoo for identity, CRM, simple products, and light accounting primitives.
- Do not force the data model to mirror every Odoo accounting concept if the clinic workflow does not need it.

## 6. Custom Model Candidates

These models are good candidates for custom implementation because they reflect the vertical workflow rather than generic ERP behavior.

### Definitely custom

- `Practice`
- `AppointmentType`
- `IntakeFormTemplate`
- `IntakeSubmission`
- `ConsentTemplate`
- `ConsentRecord`
- `Encounter`
- `EncounterSection`
- `CheckoutSession`
- `CheckoutLine`
- `Package`
- `PackageBalance`
- `RetentionSignal`

### Custom if AI is enabled

- `AISession`
- `AIOutput`
- `AIReviewAction`

### Likely extension models rather than entirely standalone

- `Provider`
  - extend Odoo user/contact records with clinical and scheduling fields

- `Patient`
  - extend Odoo contact records with patient-specific fields and flags

- `Lead`
  - extend Odoo CRM lead with referral and conversion fields

- `Payment`
  - may wrap or extend Odoo payment records so Phase 1 can cleanly track tender type and encounter-related usage

### Custom-model rule

- If a model represents the clinic workflow directly, it should usually be custom.
- If a model represents generic identity or lightweight financial plumbing, extend Odoo first.

## 7. Data Model Risks and Simplifications

### Intentional simplifications

- One clinic at a time, even if the schema leaves room for a `Practice` record.
- One main specialty only; no broad specialty matrix in Phase 1.
- No insurance claims, payer entities, or claim life cycle.
- No deep accounting layers beyond invoice and payment recording.
- No separate retail domain unless retail actually matters in pilot use.
- No complex household or family scheduling relationships.
- AI review state remains simple and optional.

### Key risks

- Over-extending Odoo accounting models too early could pull the schema into full accounting complexity.
- Over-modeling future specialties now would bloat the schema before the first product is validated.
- Adding too much structure to encounter notes too early could slow the charting UX.
- Trying to fully normalize packages, gift credits, and retail on day one could complicate checkout unnecessarily.
- Storing AI context too aggressively could create privacy and maintenance burden.

### Recommended simplifications to preserve

- Keep payment types to a short controlled list.
- Keep package handling separate from full subscription logic.
- Keep appointment and encounter as the central operational objects.
- Keep the invoice-payment model simple enough for cash-pay clinics.
- Add optional entities only when a real pilot workflow requires them.

### Final schema guardrail

If an entity does not directly support:
- intake
- consent
- appointment
- encounter
- checkout
- invoice
- payment
- rebooking

then it should not be part of the Phase 1 minimum data model.
