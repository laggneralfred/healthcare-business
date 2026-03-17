# Sprint 14 Decision Record

Status:
- Frozen decision record only
- No implementation work is authorized from this document
- This decision starts from the frozen Sprint 13 baseline

## 1. Decision Scope

Sprint 14 is an architecture decision sprint only.

It does not:
- implement code
- add features
- change workflow
- widen the current financial scope

## 2. Frozen Sprint 13 Baseline

This decision is grounded in the implemented Sprint 13 baseline:
- appointment remains the workflow hub
- checkout remains a narrow post-close operational finance layer
- one checkout session exists per appointment
- checkout is line-driven
- pricing remains a defaulting layer only
- printable checkout summary is implemented
- printable payment-due document is implemented
- patient-level unpaid summary is implemented
- late payment capture for `payment_due` sessions is implemented
- encounter remains unchanged
- `needs_follow_up` remains unchanged
- no invoices
- no accounting integration
- no taxes
- no discounts
- no refunds
- no partial payments
- no claims
- no portal or gateway
- no package or membership finance

## 3. Frozen Decision

Current recommendation:
- continue with lightweight custom finance inside `hc_checkout` for now

Current explicit deferral:
- do not begin a bridge to standard Odoo accounting yet

Reason:
- the currently implemented checkout layer already solves the validated small-clinic self-pay operational loop
- the currently unsolved problems are real, but they are not yet proven to require accounting-layer depth inside the product
- adopting Odoo accounting now would introduce complexity before the current operational boundary has been exhausted

## 4. What This Decision Means

Until this decision is reopened:
- `hc_checkout` remains the active operational finance layer
- future finance slices should stay narrow and operational
- future work should avoid inventing custom ledger behavior
- future work should not silently drift into invoice, receivable, or accounting semantics

This is a deferral decision, not a permanent rejection of accounting integration.

## 5. Reopening Trigger Conditions

The accounting-bridge decision should be reopened only when there is proven operational pressure, not speculative preference.

Any one of the following is enough to justify reopening the decision:
- the clinic needs real invoices rather than printable operational summaries
- the clinic needs formal receivables tracking beyond `payment_due`
- the clinic needs partial payments, split tenders, credits, refunds, or write-offs
- the clinic needs taxes or tax-compliant financial documents
- the clinic needs accounting-period reporting or reconciliation inside Odoo
- the clinic needs a defensible ledger rather than checkout-state reporting
- the next requested finance slice would require custom reimplementation of core accounting concepts

Recommended evidence standard before reopening:
- repeated real clinic use
- observed operational friction
- a concrete finance requirement that cannot be met cleanly by the current lightweight checkout boundary

## 6. Explicit Deferred Topics

These are explicitly deferred until the decision is reopened:
- invoice creation
- account moves
- accounting journals
- reconciliation
- receivables ledger behavior
- taxes
- refunds
- partial payments
- write-offs
- credits
- accounting-linked statements

## 7. Guardrails Before Reopening

Before the accounting-bridge decision is reopened:
- do not add pseudo-invoice concepts without real invoice models
- do not add custom ledger semantics inside `hc_checkout`
- do not add partial-payment or refund logic
- do not widen checkout into a bespoke accounting subsystem

## 8. Result

Sprint 14 is now frozen as a decision-only sprint.

The active architectural direction remains:
- preserve `hc_checkout` as the lightweight custom finance layer for now
- defer any bridge to standard Odoo accounting until proven operational pressure justifies reopening the decision
