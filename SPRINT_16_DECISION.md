# Sprint 16 Pilot-Readiness Decision Record

Status:
- Frozen decision and checklist record only
- No implementation work is authorized from this document
- Grounded in the frozen Sprint 13 implemented baseline
- Preserves the frozen Sprint 14 finance-direction decision
- Preserves the frozen Sprint 15 posture that no implementation is authorized without stronger evidence

## 1. Decision Scope

Sprint 16 is a pilot-readiness decision sprint only.

It does not:
- implement code
- add features
- change workflow
- reopen accounting integration
- override the current no-implementation posture

## 2. Frozen Decision

Current recommendation:
- proceed with pilot preparation using the frozen Sprint 13 product baseline

Current implementation decision:
- no Sprint 16 implementation is authorized

Reason:
- the current product is operationally coherent enough for a first realistic small-clinic pilot within the validated self-pay boundary
- the next useful step is real-world setup and observation, not more speculative feature work

## 3. Pilot Scope Guardrails

The pilot should stay inside the current frozen posture:
- appointment remains the workflow hub
- encounter remains lightweight
- checkout remains narrow and post-close
- `hc_checkout` remains the active lightweight custom finance layer
- no accounting bridge is authorized
- no invoices, taxes, refunds, discounts, or partial payments are in scope

## 4. Demo/Test Clinic Minimum Required Records

Prepare the demo or test clinic database with the smallest realistic setup.

### Organization and users

- 1 practice record
- 1 owner user
- 1 front-desk user
- 1 provider user

Optional but still reasonable:
- 1 second provider user for role validation

### Core operational records

- 3 to 5 patient records
- 2 to 4 appointment types
- 3 to 6 service fee records in `hc_pricing`
- default service fee links on the appointment types that usually have standard fees

### Visit scenarios to preload or rehearse

- 1 appointment that ends paid by cash
- 1 appointment that ends paid by card
- 1 appointment that ends as `payment_due`
- 1 earlier `payment_due` checkout session that can later be collected

This is enough to validate the current workflow without inventing extra business scope.

## 5. Role Setup

### Owner

Use for:
- practice setup review
- access review
- fee review
- pilot oversight

### Front desk

Use for:
- patient creation and updates
- appointment scheduling
- readiness review
- post-visit closure handoff
- starting checkout
- editing checkout while it is `open`
- marking:
  - cash paid
  - card paid
  - payment due
- printing checkout summary or payment-due output
- collecting late payment on `payment_due`
- reviewing patient unpaid summary

### Provider

Use for:
- starting visits
- reviewing readiness
- documenting the encounter
- completing the visit

Provider use during the pilot should remain clinical, not finance-driven.

## 6. Practical Pilot-Prep Checklist

Use this checklist before the first pilot session.

### Database setup

- create the practice record with correct clinic-facing name
- create owner, front-desk, and provider users
- confirm each user can log in
- confirm the right operational groups are assigned
- create appointment types actually used by the clinic
- create a minimal fee list in `hc_pricing`
- assign default fee records to appointment types where appropriate
- create a small set of realistic patient records

### Workflow readiness

- confirm staff understand the appointment lifecycle:
  - `scheduled`
  - `in_progress`
  - `completed`
  - `closed`
- confirm staff understand that checkout starts only after `Close Visit`
- confirm staff understand that one checkout session exists per appointment
- confirm staff understand that pricing defaults may be edited
- confirm staff understand the difference between:
  - checkout summary
  - payment-due document
  - patient unpaid summary

### Pilot-case readiness

- prepare one same-day cash case
- prepare one same-day card case
- prepare one unpaid case
- prepare one later-collection case

## 7. First-Day Walkthrough

Run the first day slowly with a very small number of visits.

1. Front desk creates or confirms the patient.
2. Front desk creates the appointment with the correct appointment type.
3. Staff confirms intake and consent readiness.
4. Provider starts the visit from the appointment.
5. Provider documents the encounter.
6. Provider completes the visit.
7. Front desk or authorized staff closes the visit.
8. Front desk starts checkout from the closed appointment.
9. Front desk reviews the default fee or adjusts checkout lines manually.
10. Front desk finishes one of these outcomes:
    - `Mark Cash Paid`
    - `Mark Card Paid`
    - `Mark Payment Due`
11. If the session is unpaid, front desk prints the payment-due document.
12. For a prior unpaid case, front desk later uses:
    - `Collect Cash Payment`
    - or `Collect Card Payment`
13. Staff verifies that the patient unpaid summary reflects only currently unpaid sessions.

## 8. Friction To Observe And Record

Record only repeated, concrete friction. Avoid speculative wishlist items.

### Front-desk observations

- Is it obvious when an appointment is ready for checkout?
- Is the `completed -> closed` handoff understood?
- Is `Start Checkout` easy to find and use?
- Is it clear whether checkout was created or reopened?
- Are checkout lines easy enough to review and edit?
- Is the current checkout state obvious?
- Is it clear when to print checkout summary versus payment-due output?
- Is the patient unpaid summary easy to find and interpret?
- Is late payment collection on `payment_due` straightforward?

### Provider observations

- Is the appointment still a sufficient workflow hub?
- Is encounter documentation easy enough to complete?
- Is the provider clear on when the visit is handed back to front desk?
- Are finance elements visible but non-disruptive to provider work?

### Cross-role observations

- Where do users hesitate repeatedly?
- Where do users ask for help repeatedly?
- Where do users choose the wrong action repeatedly?
- Does any repeated friction look solvable by presentation-only polish rather than new business features?

## 9. What Does Not Count As Pilot Evidence By Itself

The following should not automatically trigger implementation from Sprint 16:
- generic preference for more automation
- requests for invoices
- requests for accounting reports
- requests for partial payments
- requests for refunds or discounts
- requests for portal or gateway features
- speculative ideas that were not observed during pilot use

Those require a separate decision if they become real needs.

## 10. Result

Sprint 16 is now frozen as a pilot-readiness decision and checklist sprint.

Current outcome:
- use the frozen Sprint 13 product baseline for pilot prep
- no Sprint 16 implementation is authorized
- gather concrete pilot evidence before considering any further change
