# Sprint 14 Planning Note: Finance Direction Decision

Status:
- Planning only. No implementation work is authorized from this document.
- This note starts from the frozen Sprint 13 baseline.
- It is an architecture decision sprint, not a feature sprint.

## 1. Decision Goal

Decide whether future financial depth should:

1. continue inside the lightweight custom `hc_checkout` layer
2. keep `hc_checkout` as the operational front-desk layer while planning a narrow bridge to standard Odoo accounting for future invoice and payment depth

This document does not authorize implementation of either path.

## 2. Frozen Sprint 13 Baseline

Current implemented finance posture from the frozen Sprint 13 baseline:
- appointment remains the workflow hub
- checkout begins only after `Close Visit`
- one checkout session exists per appointment
- checkout is line-driven
- pricing remains a defaulting layer only
- checkout supports:
  - `open`
  - `paid`
  - `payment_due`
- checkout supports:
  - immediate cash/card payment from `open`
  - `payment_due`
  - later cash/card collection from `payment_due`
- printable outputs currently implemented:
  - checkout summary
  - payment-due document
  - patient-level unpaid summary
- encounter remains unchanged
- no invoices
- no accounting integration
- no taxes
- no discounts
- no refunds
- no partial payments
- no claims
- no portal or gateway
- no package or membership finance

This is the baseline for the decision.

## 3. Operational Problems Already Solved

The current lightweight custom path already solves several real clinic problems for a small self-pay practice:

- front desk can start checkout only after the visit is operationally closed
- one appointment maps cleanly to one checkout session
- checkout can hold multiple simple charge lines
- front desk can mark visits paid immediately by cash or card
- front desk can mark a visit as unpaid and collect later
- patient-facing or staff-facing printable outputs exist for:
  - general checkout summary
  - payment-due document
  - patient-level unpaid summary
- patient statement and payment-due outputs are driven from the same source of truth
- the clinical workflow remains insulated from finance handling
- implementation complexity has stayed low and locally understandable

For a small acupuncture clinic running simple self-pay, this is already a meaningful operational base.

## 4. Meaningful Financial Problems Still Unsolved

The current baseline intentionally does not solve several classes of financial problems:

- invoice creation and numbering
- accounting journal entries
- receivables ledger behavior
- tax handling
- refunds and reversals
- partial payments and split tenders
- credits, write-offs, and adjustments
- payment allocation across multiple obligations
- aging and formal account statements
- audit-ready financial reporting
- reconciliation against bank/card settlement
- accounting-period controls
- broader product, package, membership, or claim-linked finance

These are not minor omissions. They mark the boundary between operational checkout support and real financial depth.

## 5. Path 1: Continue Lightweight Custom Finance In `hc_checkout`

### What it means

Keep expanding the custom checkout layer for the next finance steps without introducing a bridge to Odoo accounting yet.

Likely future work under this path would remain operational:
- more document variants
- slightly richer unpaid handling
- small workflow conveniences
- narrow front-desk financial actions

### Pros

- fastest path for small-clinic operational needs
- lowest conceptual overhead for the current product
- preserves the current clean appointment-to-checkout workflow
- avoids premature accounting configuration burden
- keeps implementation localized in a codebase already validated around `hc_checkout`
- reduces risk of Odoo accounting complexity overwhelming the clinic use case too early

### Cons

- every new finance need must be custom-designed and custom-maintained
- custom logic starts to approximate accounting concepts without real accounting structure
- reporting consistency gets harder as more edge cases appear
- future migration into accounting becomes more expensive the further custom finance grows
- auditability and reconciliation pressure will eventually outgrow the lightweight model

## 6. Path 2: Preserve `hc_checkout` Operationally But Plan A Narrow Bridge To Odoo Accounting

### What it means

Keep `hc_checkout` as the front-desk operational wrapper, but stop treating it as the final destination for all future finance depth. Instead, plan a future bridge where finalized checkout data can feed standard Odoo accounting models when the product genuinely needs invoice and payment depth.

Under this path:
- `hc_checkout` would still own clinic checkout flow
- Odoo accounting would eventually own deeper financial records
- the bridge would be narrow and deliberate, not a wholesale rewrite

### Pros

- aligns future invoice and payment depth with standard Odoo primitives
- reduces risk of building a fragile custom accounting subsystem
- improves long-term path for receivables, reconciliation, and reporting
- provides a clearer boundary between operational workflow and financial ledger concerns
- makes future financial controls more defensible

### Cons

- introduces much more configuration and implementation complexity
- raises the technical and operational bar for a small clinic that may not need it yet
- risks dragging accounting concepts into a product that is currently intentionally simple
- could slow product momentum if adopted before genuine need exists
- requires careful tenancy, account, journal, and lifecycle design to avoid user confusion

## 7. Risks Of Continuing Custom Too Far

The main danger of Path 1 is not that it fails immediately. The danger is gradual drift.

Key risks:
- custom checkout becomes an accidental accounting subsystem
- state logic becomes hard to reason about once credits, adjustments, or mixed obligations appear
- document outputs begin to imply invoice-like status without invoice-grade rules
- financial reporting becomes bespoke and brittle
- later migration to standard accounting requires backfilling concepts never modeled cleanly
- support burden rises as finance edge cases multiply

The threshold problem is important:
- adding one more narrow operational feature is cheap
- adding ten more finance features without a ledger is usually not cheap

## 8. Risks Of Adopting Odoo Accounting Too Early

The main danger of Path 2 is premature complexity.

Key risks:
- the product stops feeling lightweight for a small self-pay clinic
- front desk workflows become harder to train and harder to use
- implementation effort moves from validated clinic operations into accounting setup and exception handling
- early accounting integration can force design decisions before the real clinic needs are proven
- the team can burn time on accounting correctness before the business actually needs accounting depth in-product

This is especially relevant because the current baseline is intentionally narrow and operational, not finance-heavy.

## 9. Recommended Decision Threshold

A bridge to Odoo accounting becomes justified when at least one of these thresholds is real, repeated, and operationally validated:

- the clinic needs real invoices rather than printable operational summaries
- the clinic needs formal receivables tracking beyond `payment_due`
- the clinic needs partial payments, credits, refunds, or write-offs
- the clinic needs tax calculation or tax-compliant financial documents
- the clinic needs reconciliation or accounting-period reporting inside Odoo
- the clinic needs a defensible ledger rather than checkout-state reporting
- multiple finance features would otherwise require custom reimplementation of core accounting concepts

Recommended practical rule:
- remain on the lightweight custom path while needs are still fundamentally front-desk operational
- start planning the bridge once the next requested finance slice would require ledger semantics rather than simple checkout-state semantics

## 10. Recommended Decision

From the frozen Sprint 13 baseline, the recommended decision is:

- continue with the lightweight custom `hc_checkout` path for now
- do not start implementation of accounting integration yet
- explicitly treat Odoo accounting as the next architectural tier, not as the current sprint direction

Reasoning:
- the current product solves the validated self-pay operational loop for a small clinic
- the meaningful unsolved problems are real, but they are still mostly outside the currently validated narrow scope
- adopting accounting now would be a premature complexity jump unless a later sprint is explicitly driven by invoice, receivable, tax, reconciliation, or adjustment requirements

This is a decision to defer the bridge, not to reject it permanently.

## 11. Decision Guardrails For Future Sprints

If future finance work is approved before an accounting bridge:
- it should remain explicitly operational
- it should avoid inventing custom ledger concepts
- it should not introduce pseudo-invoice semantics without real invoice models
- it should stop short of partial-payment, refund, tax, and reconciliation logic

If a future sprint crosses those lines:
- that sprint should be treated as the point where accounting-bridge planning becomes mandatory

## 12. Explicit Non-Goals

This decision note does not authorize:
- invoices
- account moves
- accounting integration
- taxes
- refunds
- partial payments
- package or membership finance
- claims finance
- portal payments
- gateway work
- workflow changes
- any code implementation

## 13. Recommendation Summary

Current recommendation:
- preserve `hc_checkout` as the lightweight operational finance layer for now
- do not continue custom finance indefinitely without a boundary
- use invoice/ledger-style requirements as the trigger for a deliberate accounting bridge sprint

This keeps the product grounded in the frozen Sprint 13 baseline instead of drifting into accidental accounting.
