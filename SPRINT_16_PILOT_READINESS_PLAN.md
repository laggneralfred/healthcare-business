# Sprint 16 Pilot-Readiness / Real-World Validation Plan

Status:
- Planning-only sprint note
- No implementation is authorized from this document
- Grounded in the frozen Sprint 13 implemented baseline
- Preserves the frozen Sprint 14 finance-direction decision
- Preserves the frozen Sprint 15 posture that no implementation is justified without stronger evidence

## 1. Sprint Goal

Sprint 16 is a pilot-readiness and real-world validation sprint only.

Its purpose is to prepare the current product for a first realistic small-clinic pilot without adding business-scope features by default.

Sprint 16 does not:
- implement code
- add features
- change workflow
- reopen accounting integration
- override the Sprint 15 decision that no implementation is currently justified without stronger evidence

## 2. Current Implemented Workflow Through Sprint 13

The currently implemented workflow remains:
- `Lead Inquiry -> Create Patient -> Create Appointment -> Intake / Consent Readiness -> Patient completes pre-visit forms -> Start Visit -> Open / Reuse Encounter in modal -> Review readiness / open intake-consent if needed -> Record encounter documentation -> Complete Visit -> Close Visit -> Mark / Clear Needs Follow-Up -> Start Checkout -> Mark Cash Paid / Mark Card Paid / Mark Payment Due -> If payment is due, optionally print Payment Due -> Later collect cash or card payment on the same checkout session`

Current product posture remains:
- appointment is the workflow hub
- encounter remains lightweight and unchanged
- checkout starts only after the appointment is `closed`
- one checkout session exists per appointment
- checkout supports a small number of lines
- pricing is a defaulting layer only
- checkout summary, payment-due document, and patient unpaid summary are implemented
- late payment capture exists only for existing `payment_due` sessions
- no invoices or accounting integration exist

## 3. Target Pilot Clinic Profile

The target pilot should be a clinic that matches the system's currently validated boundary as closely as possible.

Recommended pilot profile:
- one small self-pay acupuncture clinic
- one owner or clinic manager
- one front-desk user, even if part-time
- one to three providers
- low to moderate daily visit volume
- no insurance billing requirement
- no claim submission requirement
- no tax complexity inside checkout
- no need for partial payments, split tenders, refunds, or package accounting during the pilot
- willingness to use printable operational summaries rather than formal invoices

This is the right pilot shape because it matches the frozen Sprint 13 product scope and the Sprint 14 decision to stay lightweight/custom for now.

## 4. Required Setup Before Pilot Use

The pilot should not begin until the following setup is completed.

### Core organization setup

- create the practice record
- confirm the clinic name and core practice details used in printed outputs
- create owner, front-desk, and provider users
- assign users to the correct operational groups

### Scheduling and visit setup

- create the appointment types the clinic actually uses
- confirm that providers can work from the appointment workflow as implemented
- confirm visit-status transitions are understood:
  - `scheduled`
  - `in_progress`
  - `completed`
  - `closed`

### Intake, consent, and encounter readiness

- confirm the clinic understands the pre-visit intake and consent flow
- confirm providers understand encounter documentation from the appointment
- confirm staff understand that checkout begins only after `Close Visit`

### Pricing and checkout readiness

- create a minimal fee list in `hc_pricing`
- assign `default_service_fee_id` on appointment types where a default charge is useful
- confirm staff understand that pricing defaults are only starting points
- confirm staff understand that checkout lines, `charge_label`, and amounts remain manually editable

### Document and print readiness

- verify the clinic can produce:
  - checkout summary
  - payment-due document
  - patient unpaid summary
- confirm where printed or exported documents will be stored operationally outside the system if needed

### Pilot data readiness

- prepare a short set of realistic test patients
- prepare a short set of realistic appointment scenarios:
  - paid at checkout
  - marked `payment_due`
  - later paid after an earlier `payment_due`

## 5. Staff Roles And Who Performs Which Actions

### Owner / clinic manager

Expected responsibilities:
- initial setup oversight
- fee list review
- user access review
- pilot observation review
- escalation point if pilot blockers appear

### Front desk

Expected responsibilities:
- create or update patient records
- create appointments
- monitor readiness before the visit
- close the operational loop after the provider finishes the visit
- start checkout after the appointment is `closed`
- edit checkout lines as needed while checkout is `open`
- mark checkout:
  - cash paid
  - card paid
  - payment due
- print the correct checkout document when needed
- later collect late payment on existing `payment_due` sessions
- use the patient unpaid summary when reviewing outstanding payment-due sessions

### Provider

Expected responsibilities:
- start the visit
- review readiness information
- document the encounter
- complete the visit
- coordinate with front desk so the appointment can be closed and moved into checkout

Provider responsibility should remain clinical and workflow-oriented, not finance-oriented.

## 6. First-Day Operational Walkthrough

The first pilot day should be run deliberately with a very small number of visits.

Recommended walkthrough:

1. Front desk creates or confirms the patient record.
2. Front desk creates the appointment with the correct appointment type.
3. Staff confirms intake and consent readiness before the visit.
4. Provider starts the visit from the appointment.
5. Provider documents the encounter and completes the visit.
6. Front desk or authorized staff closes the visit from the appointment.
7. Front desk starts checkout from the closed appointment.
8. Front desk verifies the default charge line or adjusts the checkout lines manually.
9. Front desk chooses one real end-state:
   - `Mark Cash Paid`
   - `Mark Card Paid`
   - `Mark Payment Due`
10. If needed, front desk prints:
   - checkout summary for general visit-level confirmation
   - payment-due document for an unpaid visit
11. For at least one `payment_due` case, front desk later reopens the same session and uses:
   - `Collect Cash Payment`
   - or `Collect Card Payment`
12. Staff verifies that the patient unpaid summary reflects only currently unpaid sessions.

The first pilot day should emphasize observation, not speed.

## 7. Pilot Observation Checklist

The point of the pilot is to gather real evidence before authorizing more implementation.

### Front-desk observation checklist

- Is it immediately clear when an appointment is ready for checkout?
- Is the transition from `completed` to `closed` understood by staff?
- Is `Start Checkout` easy to find at the right moment?
- Is it clear whether clicking `Start Checkout` created a new session or reopened an existing one?
- Are checkout lines easy enough to review and edit for a small clinic workflow?
- Is the current checkout state obvious at a glance?
- Is it clear when to use checkout summary versus payment-due document?
- Is the patient unpaid summary easy to find and interpret when reviewing outstanding balances?
- Does late-payment capture on `payment_due` sessions feel operationally straightforward?

### Provider observation checklist

- Is the appointment still a sufficient workflow hub for the provider?
- Is encounter documentation easy enough to reach and complete from the appointment?
- Is the provider clear on the handoff point between clinical completion and front-desk checkout?
- Are any finance-related UI elements distracting the provider from the clinical flow?

### Cross-role observation checklist

- Are there repeated moments where staff hesitate, ask for help, or choose the wrong action?
- Are there repeated moments where staff rely on memory instead of the UI to know the next step?
- Is there any observed friction that can be solved by a tiny presentation-only improvement?

## 8. Likely Blockers That Would Justify A Tiny Future Implementation Sprint

The following would justify reopening implementation only if they are actually observed in pilot use.

- repeated front-desk confusion about whether checkout exists, is open, is paid, or is payment due
- repeated confusion when `Start Checkout` reopens an existing session
- repeated wrong selection between checkout summary and payment-due document
- repeated provider confusion caused by finance visibility inside otherwise clinical workflow
- repeated operational delay caused by UI clarity issues rather than missing business capability

If observed, these should still be handled as tiny UX-hardening slices only, not as new business-scope features.

## 9. What Does Not Count As A Pilot-Readiness Blocker

The following are important ideas, but they should not be treated as pilot blockers unless the pilot produces strong evidence and a new sprint decision:
- invoices
- accounting integration
- taxes
- partial payments or split tenders
- discounts, refunds, credits, or write-offs
- claim workflows
- portal or payment gateway delivery
- package or membership finance
- rebooking automation

Those remain outside the current product posture.

## 10. Pilot Success Standard

The pilot should be considered operationally successful if:
- staff can complete the full visit-to-checkout loop on real visits
- staff can handle both same-day payment and `payment_due`
- staff can later collect payment on an earlier `payment_due` session
- printed outputs are sufficient for the clinic's immediate operational needs
- observed friction is limited to small clarity issues rather than missing finance depth

If the pilot fails for reasons outside that boundary, the next step should be a new decision sprint, not silent scope creep.

## 11. Explicit Non-Goals

Sprint 16 does not authorize:
- code implementation
- product changes
- workflow changes
- new finance models
- invoices or accounting integration
- taxes
- discounts, refunds, or partial payments
- claims, portal, gateway, email, or SMS features
- rebooking or package logic
- reopening the Sprint 14 finance-direction decision without trigger evidence
- overriding the Sprint 15 posture that stronger evidence is required before implementation

## 12. Result

Sprint 16 is open as a planning-only pilot-readiness sprint.

The intended outcome is a realistic pilot checklist and observation frame for the frozen Sprint 13 product, not new product scope.
