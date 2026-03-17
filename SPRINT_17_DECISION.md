# Sprint 17 Smoke Automation Decision Record

Status:
- Frozen decision record only
- No implementation work is authorized from this document
- Grounded in the frozen Sprint 13 implemented baseline
- Preserves the frozen Sprint 14 finance-direction decision
- Preserves the frozen Sprint 15 no-implementation guardrail
- Preserves the frozen Sprint 16 pilot-readiness posture

## 1. Decision Scope

Sprint 17 is an automation decision sprint only.

It does not:
- implement automation
- change product behavior
- add features
- change workflow
- expand finance scope

## 2. Frozen Decision

Current recommendation:
- if browser automation is later approved, Playwright is the recommended default tool

Current scope recommendation:
- only a tiny pilot-support smoke suite is justified

Reason:
- the current frozen workflow is narrow enough that a very small browser smoke layer could add pilot confidence
- broader automation would create maintenance overhead before there is evidence that it is needed
- human pilot observation remains necessary for usability judgment and should not be displaced by automation

## 3. What This Authorizes

Sprint 17 authorizes no implementation now.

It records only that a future narrow implementation could be justified if explicitly approved later and kept to:
- pilot-critical workflow verification
- role-based smoke paths only
- a very small set of state and report checks

## 4. Recommended Default If Approved Later

If a future sprint explicitly approves implementation:
- use Playwright as the default browser automation tool

Why Playwright:
- smallest practical modern choice for this project
- readable role-based flows
- good support for stable waits and UI assertions
- more maintainable than heavier alternatives for a tiny smoke layer

## 5. Recommended First Automation Slice

If implementation is approved later, the smallest justified slice is:
- provider visit path smoke
- front-desk close-and-checkout smoke
- `payment_due` plus late-payment smoke
- patient unpaid-summary verification

This should remain a pilot-support suite only.

## 6. Explicit Deferrals

The following are explicitly deferred:
- broader automation coverage
- full regression automation
- broad UI coverage across all modules
- CI/CD integration
- replacing backend tests with browser automation
- replacing human usability evaluation with automation

## 7. Guardrails For Any Future Approval

If automation is approved later:
- keep the suite intentionally tiny
- limit it to the frozen Sprint 13 workflow
- avoid cosmetic assertions
- avoid expanding into subjective usability testing
- avoid turning the suite into a broad end-to-end platform

## 8. Result

Sprint 17 is now frozen as an automation decision-only sprint.

Current outcome:
- Playwright is the recommended default if automation is later approved
- only a tiny pilot-support smoke suite is justified
- broader automation, CI/CD integration, and full usability replacement are explicitly deferred
