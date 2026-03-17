# Sprint 15 Operational Validation Decision Record

Status:
- Frozen decision record only
- No implementation work is authorized from this document
- Grounded in the frozen Sprint 13 implemented baseline
- Preserves the frozen Sprint 14 finance-direction decision

## 1. Decision Scope

Sprint 15 is an operational-validation decision sprint only.

It does not:
- implement code
- add features
- change workflow
- widen checkout scope
- reopen accounting integration

## 2. Frozen Baseline And Authority

This decision starts from:
- the implemented Sprint 13 baseline
- the frozen Sprint 14 finance-direction decision
- the Sprint 15 operational-validation planning note

Current baseline posture remains:
- appointment remains the workflow hub
- encounter remains lightweight and unchanged
- checkout remains a narrow post-close operational finance layer
- one checkout session exists per appointment
- multi-line checkout is supported
- pricing remains a defaulting layer only
- printable checkout summary is implemented
- printable payment-due document is implemented
- patient-level unpaid summary is implemented
- late payment capture for `payment_due` sessions is implemented
- no invoices
- no accounting integration
- no taxes
- no discounts, refunds, or partial payments
- no claims, portal, gateway, packages, memberships, or rebooking coupling

## 3. Validation Summary

Sprint 15 reviewed the currently implemented user-facing workflow with the narrow question:
- is there already enough proven operational friction to justify an immediate tiny UX-hardening implementation slice

The review identified plausible usability friction candidates, especially around:
- checkout status visibility on the appointment
- clarity when `Start Checkout` reopens an existing session
- clarity around which checkout print action to use

However, these were identified as likely friction points, not proven operational failures.

No clear bug was identified.

No repeated real-use evidence was established in this sprint that makes one of those polish slices necessary immediately.

## 4. Frozen Decision

Current recommendation:
- no Sprint 15 implementation is authorized now

Reason:
- the candidate UX issues are credible, but they are not yet validated strongly enough to justify even a tiny slice from the frozen baseline
- the current implemented workflow is operationally coherent for the intended small-clinic self-pay use case
- adding polish without validated pressure risks drifting from operational hardening into incremental scope expansion

This is a defer-and-observe decision, not a rejection of future UX hardening.

## 5. What Remains True

Until a new sprint decision is made:
- the Sprint 13 implemented baseline remains the active product baseline
- the Sprint 14 finance-direction decision remains active
- `hc_checkout` remains the lightweight custom finance layer
- no bridge to standard Odoo accounting is authorized

## 6. Reopen Conditions For UX-Hardening Work

A future tiny UX-hardening slice may be justified only if there is concrete operational evidence such as:
- repeated front-desk hesitation or missteps around checkout state recognition
- repeated confusion about whether `Start Checkout` created or reopened a session
- repeated wrong-document selection between checkout summary and payment-due output
- observed workflow delay that can be solved by presentation-only changes without widening scope

Preferred evidence standard:
- repeated real clinic use
- observed operator friction, not speculation
- a fix that stays presentation-oriented and does not change finance semantics or workflow boundaries

## 7. Explicit Non-Authorization

Sprint 15 does not authorize:
- appointment workflow changes
- checkout model changes
- new reports or document types
- new payment logic
- invoice or accounting behavior
- pseudo-ledger behavior
- portal, gateway, email, or SMS expansion

## 8. Result

Sprint 15 is now frozen as a decision-only sprint.

Current outcome:
- no Sprint 15 implementation authorized
- continue using the frozen Sprint 13 product baseline
- preserve the Sprint 14 decision to stay lightweight and custom inside `hc_checkout` for now
