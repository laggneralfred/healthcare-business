# MODULE MAP

Status:
- Planning document only
- No implementation work is authorized from this file

## Purpose

This document translates the planning set into a realistic module plan for a solo-founder build on `Odoo Community`.

Primary rule:
- Preserve the workflow spine:
  `appointment -> encounter -> checkout -> invoice -> payment -> follow-up -> retention`

Planning constraints:
- Keep Phase 1 narrow
- Avoid over-customizing Odoo
- Keep specialty logic isolated
- Make AI optional and reviewable
- Treat card, cash, and package credit as the early payment priorities
- Treat POS as optional
- Treat full accounting as optional and not central to Phase 1

## 1. Shared Core Modules Required for Phase 1

These modules are the minimum credible product for the initial acupuncture-focused launch.

| Module | Purpose | Phase | Mandatory |
|---|---|---|---|
| `hc_practice_core` | Practice settings, tenant config, provider setup, feature flags | 1 | Yes |
| `hc_patient_core` | Patient profile, communication preferences, identifiers, household-ready structure | 1 | Yes |
| `hc_leads` | Lead capture and referral-source tracking | 1 | Yes |
| `hc_intake` | Intake templates, form submissions, patient onboarding | 1 | Yes |
| `hc_consent` | Versioned consent templates, signatures, renewal status | 1 | Yes |
| `hc_scheduling` | Appointment types, booking rules, confirmations, reminders | 1 | Yes |
| `hc_encounter` | Encounter record, note engine, shared SOAP-style structure | 1 | Yes |
| `hc_checkout` | Checkout session, checkout lines, encounter-to-financial handoff | 1 | Yes |
| `hc_billing_light` | Light invoices, receipts, balance handling, payment recording | 1 | Yes |
| `hc_packages` | Package definitions, package balances, package-credit application | 1 | Yes |
| `hc_retention` | Rebooking cues, inactive-patient workflows, recall logic | 1 | Yes |
| `hc_reporting` | Basic dashboard: visits, revenue, rebooking, referral sources | 1 | Yes |
| `hc_documents` | Attachments, intake scans, consent files, encounter-linked documents | 1 | Yes |

Phase 1 interpretation:
- These modules together cover intake, scheduling, notes, checkout, payment capture, and patient retention.
- If a module does not materially support that chain, it should not be in the Phase 1 build.

## 2. Optional Shared Business Modules

These modules are useful, but not required to validate the initial wedge.

| Module | Purpose | When to enable | Mandatory |
|---|---|---|---|
| `hc_gift` | Gift certificate issue, balance tracking, redemption | Enable if clinics actively sell gift certificates | Optional |
| `hc_retail_ops` | Add retail items to checkout, simple retail handling | Enable when clinics sell herbs, supplements, or retail items | Optional |
| `hc_inventory_light` | Inventory tracking for products and stock movements | Only when actual stock control is required | Optional |
| `hc_calendar_sync` | External calendar synchronization | Enable only if validated by pilot demand | Optional |
| `hc_messaging_plus` | Expanded campaign messaging beyond basic reminders | Later Phase 2 need | Optional |
| `hc_households` | Family or grouped patient scheduling and billing relationships | Later if clearly needed by pilots | Optional |
| `hc_memberships` | Recurring membership logic beyond simple packages | Later if package handling proves insufficient | Optional |
| `hc_accounting_bridge` | Export or sync into fuller accounting workflows | Only when practices need more formal accounting integration | Optional |
| `hc_pos_bridge` | POS-style front desk flow using Odoo POS or a light wrapper | Only for retail-heavy practices | Optional |

Rule:
- Optional business modules should be feature-flagged per practice.
- Service-only clinics should not carry retail, POS, inventory, or accounting complexity by default.

## 3. Specialty Extension Modules

Specialty modules should extend the core workflow, not replace it.

### Acupuncture

| Module | Purpose | Phase | Mandatory for acupuncture |
|---|---|---|---|
| `hc_acu_intake` | TCM-oriented intake extensions | 2 | Yes |
| `hc_acu_charting` | Point charting, treatment details, meridian/body map support | 2 | Yes |
| `hc_acu_careplan` | Treatment-course planning and progress tracking | 2 | Yes |
| `hc_acu_herbs` | Herb/formula workflows, optional retail/inventory tie-in | 2 | Optional |

### Massage Therapy

| Module | Purpose | Phase | Mandatory for massage launch |
|---|---|---|---|
| `hc_massage_intake` | Contraindications, pressure preferences, body priorities | 3 | Yes |
| `hc_massage_charting` | Body-region notes and modalities tracking | 3 | Yes |
| `hc_massage_ops` | Outcall, tips, room-turnover, massage-specific package handling | 3 | Optional at first |

### Chiropractic

| Module | Purpose | Phase | Mandatory for chiropractic launch |
|---|---|---|---|
| `hc_chiro_exam` | Exam templates, ROM, ortho/neuro findings | 4 | Yes |
| `hc_chiro_careplan` | Care plans and repeat-visit management | 4 | Yes |
| `hc_chiro_billing_plus` | Heavier billing support and later insurance-adjacent workflows | 4+ | Optional and deferred |

Specialty rule:
- A practice should only load the extension modules required for its specialty.
- Shared workflows must still run through the same intake, appointment, encounter, checkout, payment, and retention pipeline.

## 4. AI Modules

AI modules should be thin adapters around concrete workflow steps.

| Module | Purpose | Phase | Mandatory |
|---|---|---|---|
| `hc_integration_ai` | AI broker, feature flags, provider abstraction, audit hooks | 1 | Yes if any AI is enabled |
| `hc_ai_intake_summary` | Summarize intake and prior visit context | 1 | Optional |
| `hc_ai_note_draft` | Draft reviewable encounter notes | 1 | Optional |
| `hc_ai_followup_draft` | Draft after-visit summaries and follow-up messaging | 1 | Optional |
| `hc_ai_retention` | Rebooking prompts and outreach prioritization | 1 | Optional |
| `hc_ai_message_draft` | Recall and follow-up message drafting | 2 | Optional |
| `hc_ai_chart_qa` | Missing-chart checks and contradictions | 2 | Optional |
| `hc_ai_business_copilot` | Natural-language operational insights | 2 | Optional |
| `hc_ai_ocr_intake` | OCR extraction from uploads and scans | 2 | Optional |
| `hc_ai_billing_assist` | Coding or claim support for later insurance-heavy workflows | 3+ | Optional and deferred |

AI rule:
- AI must never be a hard dependency for the core platform.
- Any AI-generated output must be reviewable, editable, and rejectable before it affects the record.

## 5. Odoo Base Modules to Reuse

Reuse Odoo for operational plumbing and stable business primitives.

| Odoo module | Planned use | Phase 1 stance |
|---|---|---|
| `base` | ORM, users, security groups, configuration foundation | Reuse |
| `contacts` | Foundation for patients, providers, referral contacts | Reuse |
| `calendar` | Internal scheduling primitives | Reuse |
| `website` | Public entry points for intake and booking | Reuse |
| `crm` | Lead intake and referral tracking | Reuse |
| `sale` | Sales-order-style plumbing only if it cleanly supports checkout/invoice flow | Use cautiously |
| `account` | Light invoicing and payment recording | Use minimally |
| `product` | Service definitions, retail items, herbs, supplements | Reuse |
| `stock` | Inventory only when enabled | Optional |
| `point_of_sale` | POS-style retail checkout when justified | Optional |
| `mass_mailing` or equivalent | Reminder and retention messaging support if simple enough | Optional |

Avoid as core dependencies:
- complex accounting features
- heavy subscription logic unless clearly needed
- marketplace healthcare modules that become upgrade liabilities
- deep rewrites of Odoo scheduling or accounting internals

## 6. Dependency Order

This is the recommended build order for a solo founder.

### Foundation order

1. `base`, `contacts`, `calendar`, `website`, `crm`, `product`
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

### AI layer order

1. `hc_integration_ai`
2. `hc_ai_intake_summary`
3. `hc_ai_note_draft`
4. `hc_ai_followup_draft`
5. `hc_ai_retention`

### Specialty layer order

1. `hc_acu_intake`
2. `hc_acu_charting`
3. `hc_acu_careplan`
4. `hc_acu_herbs`
5. later massage modules
6. later chiropractic modules

Dependency rule:
- Do not start specialty modules before the shared encounter and checkout spine is stable.
- Do not add AI modules before the source workflows are usable without AI.

## 7. Mandatory vs Optional Modules

### Mandatory for Phase 1

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

### Optional in Phase 1

- `hc_gift`
- `hc_retail_ops`
- `hc_inventory_light`
- `hc_pos_bridge`
- `hc_calendar_sync`
- `hc_memberships`
- `hc_accounting_bridge`
- AI feature modules

### Mandatory only when a specialty launches

- `hc_acu_intake`
- `hc_acu_charting`
- `hc_acu_careplan`
- later massage and chiropractic modules when those verticals are intentionally added

## 8. Modules to Defer to Later Phases

These modules are likely to become scope traps if brought into Phase 1.

| Module or area | Why deferred | Target phase |
|---|---|---|
| `hc_acu_herbs` with full inventory depth | Useful, but not required for first usable product | 2 |
| `hc_retail_ops` with richer retail workflows | Adds front-desk and inventory complexity | 2 |
| `hc_pos_bridge` | Important for some clinics, but not universal | 2 |
| `hc_inventory_light` | Not needed for service-only clinics | 2 |
| `hc_memberships` | More complex than package credits | 2 |
| `hc_massage_*` modules | Second specialty only after core is stable | 3 |
| `hc_chiro_*` modules | High-support specialty and higher billing complexity | 4 |
| `hc_ai_chart_qa` | Useful, but depends on stable note structure | 2 |
| `hc_ai_business_copilot` | Better after reporting is trustworthy | 2 |
| `hc_ai_ocr_intake` | Helpful but not essential | 2 |
| `hc_ai_billing_assist` | High risk and tied to heavier billing | 3+ |
| fuller accounting workflows | Not central to the initial value proposition | 2+ only if demanded |
| insurance and clearinghouse logic | Stress trap for a solo founder | 3+ or later |

## 9. Financial Workflow Notes

### Payment methods

Phase 1 early priorities:
- card
- cash
- package credit

Supported but optional early:
- gift certificate

Guidance:
- Card and cash should be first-class payment types from the start.
- Package credit is essential because treatment plans and prepaid visits are common in the target market.
- Gift certificates matter for some clinics, but can remain optional if they slow Phase 1.

### Package handling

Package behavior should be handled in a dedicated module rather than buried inside accounting logic.

Required package capabilities:
- define package or prepaid service bundle
- assign to patient
- track remaining balance
- consume package credit at checkout
- show package status during scheduling and visit prep

Do not make package handling depend on:
- complex subscription accounting
- full recurring billing logic
- POS-specific flows

### POS

POS is important, but not universal.

Recommended stance:
- keep POS optional
- only enable it for practices that actually sell enough retail products to justify it
- keep the default checkout flow inside `hc_checkout`
- use `point_of_sale` only when a pilot practice clearly needs faster counter-style retail checkout

### Inventory

Inventory should be disabled by default in service-first clinics.

Enable inventory only when:
- the clinic sells enough herbs, supplements, or retail items to need stock tracking
- there is a real operational need for stock deduction and low-stock visibility

Do not let inventory requirements distort the Phase 1 product for service-only clinics.

### Optional accounting

Accounting principle:
- start with light billing and payment recording
- make fuller accounting optional
- avoid tying the platform too tightly to complex accounting dependencies in Phase 1

Phase 1 financial scope should include:
- invoice creation from checkout
- recording payment type and amount
- receipt generation
- simple outstanding balances
- payment allocation

Phase 1 should not require:
- deep chart-of-accounts customization
- advanced reconciliation workflows
- complex tax or multi-entity accounting
- insurance claim accounting

## 10. Guardrails to Avoid Over-Customizing Odoo

- Do not patch Odoo core source.
- Do not rewrite Odoo accounting internals for Phase 1.
- Do not turn `point_of_sale` into a hard dependency for all tenants.
- Do not use community healthcare modules as foundational runtime dependencies.
- Keep custom modules additive: new models, additive fields, isolated views, clear service boundaries.
- Keep specialty logic in specialty modules, not in shared models unless the fields are truly cross-specialty.
- Keep package logic and checkout logic separate from deep accounting logic.
- Keep AI orchestration outside Odoo business logic where possible.
- Prefer configuration flags over tenant-specific code forks.
- Reject features that create one-off clinic customization obligations.
- Delay any module that forces heavy JavaScript rewrites unless it is core to adoption.
- If a module makes upgrades harder but does not clearly increase recurring revenue, defer it.

## Recommended Phase 1 Build Slice

For the first usable product, the realistic module slice is:

- Odoo base: `base`, `contacts`, `calendar`, `website`, `crm`, `product`, minimal `account`
- Custom core: `hc_practice_core`, `hc_patient_core`, `hc_leads`, `hc_intake`, `hc_consent`, `hc_scheduling`, `hc_encounter`, `hc_checkout`, `hc_billing_light`, `hc_packages`, `hc_retention`, `hc_reporting`, `hc_documents`
- Optional AI for first pilots: `hc_integration_ai`, `hc_ai_intake_summary`, `hc_ai_note_draft`

That is enough to validate the product promise without stepping into POS-heavy retail, inventory-heavy operations, or accounting-heavy complexity too early.
