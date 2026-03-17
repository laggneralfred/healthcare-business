# Sprint 17 Pilot Smoke Automation Plan

Status:
- Planning-only sprint note
- No implementation is authorized from this document
- Grounded in the frozen Sprint 13 implemented baseline
- Preserves the frozen Sprint 14 finance-direction decision
- Preserves the frozen Sprint 15 no-implementation guardrail
- Preserves the frozen Sprint 16 pilot-readiness posture

## 1. Sprint Goal

Sprint 17 is an automation-planning sprint only.

Its purpose is to define the smallest practical browser-based smoke automation layer for the current frozen clinic workflow so pilot preparation has a repeatable UI-level safety check.

Sprint 17 does not:
- implement automation
- change product behavior
- add features
- change workflow
- replace human pilot walkthroughs or human usability judgment

## 2. Purpose

The smoke automation is meant to validate:
- that the core frozen workflow can still be traversed in the browser
- that the right actions are available to the right roles
- that key state transitions still succeed
- that key report actions still open or render
- that the current pilot-critical flow has not regressed at the UI level

The smoke automation is not meant to validate:
- subjective usability quality
- whether wording feels intuitive
- whether layout feels cluttered or elegant
- whether users would naturally discover the right next step
- broader business correctness beyond the current frozen workflow

Clear distinction:
- automated workflow verification checks whether the implemented system still works as expected
- human usability judgment checks whether real clinic staff understand and comfortably use the workflow

## 3. Candidate Tool Choice

Recommended default:
- Playwright

Reason:
- it is the narrowest practical modern browser automation choice for this project
- it is easier to keep readable than lower-level Selenium-style setups
- it has good support for role-based browser flows, robust waiting, and report-opening checks
- it is more maintainable for a small intentionally limited smoke suite than custom browser scripting

Brief comparison:

### Playwright

Pros:
- strong selector and wait model
- readable end-to-end role flows
- good local developer ergonomics
- practical for a tiny smoke suite

Cons:
- adds browser automation dependencies
- still requires careful selector discipline

### Selenium

Pros:
- widely known
- flexible

Cons:
- heavier and less pleasant for a small modern smoke suite
- more setup overhead for little benefit here

### Odoo tour-based approach

Pros:
- Odoo-native concept
- can fit simple client-side walkthroughs

Cons:
- less attractive for role-switched multi-user pilot flows
- less comfortable for report-window and broader smoke orchestration
- easier to drift into frontend-coupled implementation details

Current recommendation:
- if Sprint 17 implementation is approved later, use Playwright as the default tool

## 4. Frozen Workflow Paths Worth Automating

The smoke suite should automate only the smallest role-based paths that matter for the frozen Sprint 13 baseline.

### Owner/admin setup smoke path

Purpose:
- verify that a privileged user can access the key setup surfaces needed for pilot preparation

Minimum path:
- log in as owner/admin
- open practice-related records already required by the pilot
- open appointment types
- open service fees
- verify setup forms and lists load

### Front-desk operational path

Purpose:
- verify the operational workflow hub from patient and appointment through checkout

Minimum path:
- log in as front desk
- open or create patient
- open or create appointment
- verify readiness-linked workflow surfaces are reachable
- close the visit after provider completion preconditions are satisfied
- start checkout

### Provider clinical path

Purpose:
- verify the provider can perform the clinical part of the frozen workflow without finance expansion

Minimum path:
- log in as provider
- open assigned appointment
- start visit
- open or reuse encounter
- complete visit

### Checkout `payment_due` path

Purpose:
- verify the unpaid operational path remains usable

Minimum path:
- open checkout from closed appointment
- verify line editing while open
- mark session `payment_due`
- open payment-due document

### Late-payment path

Purpose:
- verify the frozen Sprint 13 late-payment transition

Minimum path:
- reopen existing `payment_due` session
- collect cash or card payment
- verify session becomes `paid`

### Patient unpaid-summary path

Purpose:
- verify the patient-level unpaid summary still reflects only unpaid sessions

Minimum path:
- open patient unpaid summary while a session is `payment_due`
- collect late payment
- verify that session no longer appears in the unpaid summary

## 5. Suggested Smoke Scenarios

The suite should stay intentionally small.

Recommended initial scenarios:

1. Owner setup access smoke
- open service fee list/form
- open appointment type list/form
- verify default-fee linkage surface is present

2. Provider visit workflow smoke
- open appointment
- start visit
- open or reuse encounter
- complete visit

3. Front-desk close-and-checkout smoke
- open completed appointment
- close visit
- start checkout
- verify pricing defaults appear when expected
- add or edit checkout line
- mark paid
- open checkout summary

4. Front-desk unpaid path smoke
- open checkout
- mark `payment_due`
- open payment-due document
- open patient unpaid summary

5. Late-payment smoke
- reopen same `payment_due` checkout
- collect cash or card payment
- verify state changed to `paid`
- verify patient unpaid summary no longer includes the session

These scenarios are enough to exercise the frozen pilot-critical path without trying to automate every screen.

## 6. What The Automation Should Verify

The smoke automation should verify:
- login works for the intended roles
- pages and forms load for the expected role
- key actions and buttons are available when expected
- restricted actions are not available to the wrong role when that check is practical
- readiness-gated and state-gated transitions succeed
- visit status changes occur as expected
- checkout opens only from the proper state path
- pricing defaults appear when expected
- checkout lines can be added or edited while checkout is open
- paid and `payment_due` state transitions succeed
- checkout summary action opens or renders
- payment-due document action opens or renders
- patient unpaid summary opens or renders
- a previously unpaid session disappears from the patient unpaid summary after late payment

## 7. What The Automation Should Explicitly Not Try To Judge

The smoke automation should not try to judge:
- whether wording is intuitive
- whether labels are the best possible labels
- whether layout feels cluttered
- whether a user would naturally know the next step
- whether the UI feels elegant
- whether the overall workflow is pleasant or efficient
- whether a human would prefer a different mental model

Those are human pilot and observation questions, not automation questions.

## 8. Test Data Strategy

Use the smallest stable test data shape possible.

Recommended approach:
- dedicated demo or test clinic database for smoke runs
- a very small fixed dataset matching Sprint 16 pilot prep
- one practice
- one owner/admin user
- one front-desk user
- one provider user
- a few patients only
- a few appointment types only
- a few service fees only

Stable scenario data should include:
- one appointment ready for provider flow
- one appointment ready for close-and-checkout flow
- one session that can become `payment_due`
- one session that can be collected later if needed by the scenario

To avoid brittle data coupling:
- prefer explicit setup records created for smoke use
- avoid depending on leftover manual data
- avoid relying on dynamic search results when a direct known record can be used
- keep labels and scenario names predictable and unique

## 9. Execution Posture

Initial execution posture should be conservative.

Recommended approach:
- local-only at first
- run manually before pilot walkthroughs or before a demo session
- use it as a complement to the existing backend test pass, not a replacement
- keep it outside CI/CD initially

Recommended cadence:
- run after meaningful environment refreshes
- run before a pilot rehearsal
- run before a real clinic walkthrough if recent changes were made

Relationship to current backend tests:
- backend tests continue to validate model and server behavior
- smoke automation adds browser-level confidence that the frozen workflow is still operable through the UI

CI/CD posture:
- no CI/CD expansion is recommended initially
- revisit only if local smoke automation proves stable and genuinely useful

## 10. Risks And Maintenance Concerns

Main risks:
- brittle selectors tied too closely to layout details
- test failures caused by role/setup drift rather than true regressions
- report-opening behavior being harder to validate consistently than ordinary form actions
- browser automation overhead that becomes disproportionate for a very small project
- silent suite growth from smoke checks into pseudo end-to-end coverage

How to keep it intentionally small:
- automate only pilot-critical flows
- avoid cosmetic assertions
- prefer stable role and record setup
- keep assertions state-oriented and action-oriented
- cap the first implementation to a handful of scenarios
- treat anything more ambitious as a separate future decision

## 11. Recommendation

Current recommendation:
- a tiny Sprint 17 implementation could be justified later, but only as a narrow pilot-support automation slice

Reason:
- the frozen product is stable enough that a small browser smoke layer could add useful pilot confidence
- this would complement backend tests and pilot walkthroughs without changing product scope

Recommended tool:
- Playwright

Recommended smallest first implementation slice if approved later:
- one minimal smoke suite covering:
  - provider visit path
  - front-desk close-and-checkout path
  - `payment_due` plus late-payment path
  - patient unpaid-summary verification

Implementation guardrail if later approved:
- keep the suite intentionally tiny
- use it only for pilot-critical workflow verification
- do not turn it into broad UI coverage or a replacement for human usability testing

## 12. Explicit Non-Goals

Sprint 17 does not authorize:
- automation implementation now
- any application code changes
- any product behavior changes
- any workflow changes
- any accounting or finance architecture expansion
- any expansion beyond the frozen Sprint 13 workflow

## 13. Result

Sprint 17 is open as a planning-only automation sprint.

The intended outcome is a narrow browser-smoke strategy for pilot support.

No implementation is authorized from this document by itself.
