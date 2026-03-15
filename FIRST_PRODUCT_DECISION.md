# FIRST PRODUCT DECISION

Status:
- Planning document only
- No implementation work is authorized from this file

## Decision

Build the first product for:
- solo and small acupuncture clinics
- primarily cash-pay, with at most light insurance use
- owner-operated practices that need one calmer system for intake, scheduling, charting, checkout, packages, and rebooking

Do not build the first product for:
- chiropractic clinics
- general multi-specialty clinics
- insurance-heavy practices
- retail-heavy clinics that need POS first

This is the right first product because it aligns with the founder's expertise, keeps operational and compliance burden lower, and still fits the long-term modular Odoo platform strategy.

## 1. Recommended First Buyer Profile

Target buyer:
- solo acupuncturist or small acupuncture clinic with 1 to 3 providers

Operational profile:
- mostly cash-pay, or mixed cash-pay with only light superbill-style insurance support
- books repeat visits over a treatment course
- sells packages or prepaid visits
- wants better intake, notes, checkout, and rebooking
- currently uses either a clunky acupuncture-specific system or a patchwork of scheduler, forms, and payments tools

Best initial sub-profile:
- owner-operator clinic
- no billing department
- no complex multi-location setup
- no urgent demand for claim submission

Why this buyer:
- has real workflow pain
- can make purchase decisions directly
- has manageable complexity
- is more likely to appreciate calm operational software than a large feature matrix

## 2. Recommended First Specialty

Start with:
- acupuncture

Do not start with:
- massage therapy as the first launch
- chiropractic as the first launch

Reason:
- acupuncture gives the best balance of founder-market fit, moderate willingness to pay, manageable complexity, and strong reuse potential for the shared platform core

Why not massage first:
- larger market, but more price-sensitive
- many therapists tolerate lightweight schedulers if they are cheap enough
- weaker urgency to switch unless you clearly outperform on daily workflow

Why not chiropractic first:
- higher budgets, but much higher complexity
- documentation, care plans, insurance, PI, and support burden create a stress trap for a solo founder

## 3. Recommended First Workflow to Solve

Solve this first:
- the repeatable patient visit loop from booking through checkout and rebooking

The exact workflow spine:
- `lead -> patient intake -> consent -> appointment -> encounter note -> checkout -> invoice -> payment -> follow-up -> retention`

Most important part of that chain:
- `appointment -> encounter -> checkout -> payment -> rebooking`

Why this workflow first:
- it is used every day
- it touches the strongest pain points
- it creates obvious value even without solving insurance
- it forms the shared backbone for later specialties

This is not just a scheduling product and not just a charting product.
It is a visit workflow product for small acupuncture clinics.

## 4. Why This Is the Best Low-Stress Entry Point

- It matches the founder's real-world domain knowledge, which lowers discovery risk.
- It avoids the most dangerous complexity layer: insurance claims and heavier revenue-cycle operations.
- It has a clear and narrow buyer profile.
- It fits well with `Odoo Community` as a business workflow foundation.
- It supports practical AI in a controlled way: intake summary, note drafting, and rebooking prompts.
- It creates reusable shared modules for massage later.
- It does not require a large support organization to be useful.

Low-stress interpretation:
- fewer edge cases than chiropractic
- better pricing potential than massage
- easier to explain than a broad “alternative healthcare platform”
- easier to pilot with a small number of clinics

## 5. What the First Product Must Include

The first product must be able to support one complete clinic workflow without manual rescue.

Required capabilities:
- patient and provider records
- lead capture or direct new-patient entry
- digital intake forms
- consent forms and signatures
- appointment scheduling
- encounter note workflow with a fast shared note structure
- checkout session linked to the encounter
- invoice creation from checkout
- payment recording for card, cash, and package credit
- package balance tracking and package credit use at checkout
- follow-up recommendation capture
- rebooking and retention prompts
- basic owner dashboard for visits, revenue, and rebooking

Recommended AI in the first product:
- intake summarizer
- draft note assistant

Optional but acceptable in the first product if it does not slow launch:
- after-visit summary draft
- gift certificate support

Product standard:
- a clinic should be able to book a patient, document a visit, take payment, and prompt rebooking in one system

## 6. What Is Explicitly Out of Scope

These are explicitly out of scope for the first product:

- insurance claims submission
- clearinghouse integrations
- payer-specific billing workflows
- chiropractic-specific exams and care plans
- massage-specific bodywork workflows
- full herb inventory management
- deep retail operations
- mandatory POS
- advanced inventory management
- full accounting customization
- advanced reconciliation workflows
- enterprise multi-location support
- native mobile apps
- telehealth
- automated clinical decision-making
- AI coding or billing assistant
- extensive tenant-specific customization

Hard rule:
- if a feature pulls the product toward an insurance-heavy EHR or a generic ERP customization business, it is out of scope

## 7. A 90-Day Success Definition

At day 90, success means:

- one internal demo environment reliably supports the full target workflow
- one or two real acupuncture pilot clinics can complete the workflow without falling back to their old tools for the core visit loop
- at least one pilot can run:
  - intake
  - booking
  - encounter note
  - checkout
  - payment
  - package credit
  - rebooking
  inside the product
- the founder can onboard a new pilot using a repeatable setup process rather than hand-built custom work
- the product remains usable without AI
- AI outputs, if enabled, are reviewable and helpful rather than mandatory

Not required by day 90:
- broad sales traction
- multiple specialties
- insurance workflows
- full accounting depth
- polished POS retail flows

## 8. Simple Demo Storyline Showing One Full Clinic Workflow

Demo clinic:
- a solo acupuncture practice treating pain and stress

Demo patient story:

1. A new patient books an initial visit from the website.
2. The patient receives intake and consent forms before the appointment.
3. The patient completes the forms online.
4. The provider opens the upcoming appointment and sees:
   - patient summary
   - intake answers
   - consent status
   - optional AI intake summary
5. The appointment is checked in and converted into an encounter.
6. The provider completes the visit note using the shared encounter workflow.
7. Optional AI drafts part of the note, but the provider reviews and edits it.
8. At checkout, the clinic adds the visit charge.
9. The patient pays using either card, cash, or package credit.
10. The system creates the invoice and records the payment.
11. The provider or front desk selects a recommended follow-up interval.
12. The patient is prompted to rebook before leaving.
13. The owner dashboard later shows:
   - completed visits
   - collected revenue
   - package usage
   - patients due for rebooking

That demo is enough to show the product promise clearly.

## 9. Top Risks If We Choose the Wrong First Scope

- Starting with chiropractic would pull the product into documentation, billing, and support complexity too early.
- Starting with massage first could produce a lower-priced, harder-to-differentiate business.
- Starting with insurance workflows would create a compliance and support trap.
- Starting with too many specialties would blur the product and slow feedback.
- Starting with POS or inventory-heavy retail would distract from the main clinic workflow.
- Starting with deep specialty charting before the shared workflow is solid would create fragile architecture.
- Starting with AI-first positioning instead of workflow-first positioning would reduce trust and increase product risk.
- Starting with full accounting expectations would turn Phase 1 into an ERP project.

The main failure mode is simple:
- building too much system for too many edge cases before proving one weekly painkiller workflow

## 10. Final Recommendation

If the goal is modest extra income with low stress, the first product should be:
- a narrow acupuncture practice workflow system
- built on an `Odoo Community` foundation
- focused on the visit loop from intake through payment and rebooking
- designed for solo and small cash-pay clinics
- explicitly not designed around insurance claims

This is the calm path.

It uses what you already know.
It avoids the parts of healthcare software most likely to become a second career in support, billing, and compliance.
It still creates real long-term leverage because the same core modules can later support massage and, more cautiously, chiropractic.

The first product should not try to win by being the biggest system.
It should win by being the least burdensome useful system for a very specific kind of clinic.

That is the right product for a retired programmer and retired acupuncturist who wants a practical business, steady extra income, and a manageable operating life.
