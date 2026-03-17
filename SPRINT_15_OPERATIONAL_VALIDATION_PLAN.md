# Sprint 15 Operational Validation / UX-Hardening Plan

Status:
- Planning-only sprint note
- No implementation is authorized from this document
- Grounded in the frozen Sprint 13 implemented baseline
- Preserves the frozen Sprint 14 finance-direction decision

## 1. Sprint Goal

Sprint 15 is an operational validation and UX-hardening sprint only.

Its purpose is to identify the smallest real friction points in the currently implemented workflow before adding more business scope.

Sprint 15 does not:
- add features
- change workflow
- reopen accounting integration
- widen checkout beyond the current lightweight custom boundary

## 2. Frozen Baseline In Scope

This planning note starts from the implemented Sprint 13 posture and the Sprint 14 decision:
- appointment remains the workflow hub
- visit lifecycle remains:
  - `scheduled`
  - `in_progress`
  - `completed`
  - `closed`
- encounter remains lightweight and unchanged
- checkout remains a narrow post-close operational finance layer
- one checkout session exists per appointment
- multi-line checkout is supported
- pricing remains a defaulting layer only
- printable checkout summary is implemented
- printable payment-due document is implemented
- patient-level unpaid summary is implemented
- late payment capture for `payment_due` sessions is implemented
- no invoice model
- no accounting integration
- no taxes
- no discounts, refunds, or partial payments
- no claims, portal, gateway, packages, memberships, or rebooking coupling

Sprint 14 remains the active finance-direction decision:
- continue with lightweight custom finance inside `hc_checkout` for now
- do not begin a bridge to standard Odoo accounting unless proven operational pressure meets the documented trigger conditions

## 3. Current Implemented User-Facing Workflow

The currently implemented user-facing flow is:
- front desk manages the patient and appointment lifecycle from the appointment record
- provider starts the visit and documents the encounter
- provider completes the visit
- staff closes the visit from the appointment once it is completed
- front desk may then start checkout from the closed appointment
- checkout creates or reopens one checkout session for that appointment
- checkout supports a small number of charge lines
- service fees may prefill defaults, but checkout values remain manually editable
- staff may:
  - mark the checkout paid by cash
  - mark the checkout paid by card
  - mark the checkout as `payment_due`
- staff may print:
  - a general checkout summary
  - a payment-due document when the session is `payment_due`
  - a patient-level unpaid summary across `payment_due` sessions
- later, front desk may collect a late full payment on an existing `payment_due` checkout session by cash or card

Operationally, this already supports a small self-pay clinic loop without invoicing or accounting depth.

## 4. Problems Already Solved

The current implemented workflow already solves these practical problems:
- one clear operational record exists for post-close clinic checkout
- front desk can collect payment immediately after a visit is closed
- front desk can defer payment without losing the checkout record
- staff can print a visit-level summary for paid or open sessions
- staff can print a payment-due document for unpaid sessions
- staff can print a patient-level unpaid summary
- staff can later convert an unpaid checkout to fully paid without reopening the visit or changing clinical records
- the system still avoids accounting, invoice, and tax complexity

## 5. Likely Friction Points In The Existing Workflow

These are likely operational friction points worth validating with real use. They are not assumed bugs.

### Front-desk friction candidates

- The handoff between `Close Visit` and `Start Checkout` is operationally clear, but it is still a two-step transition that may feel slightly mechanical at the desk.
- A reopened checkout session may not immediately communicate whether it is the current session or an existing one unless the user reads the form carefully.
- Multi-line checkout is now supported, but line editing on the form may still feel heavier than necessary for a very small clinic that usually charges one or two standard items.
- Staff may need clearer visual confirmation of the current checkout state when moving between `open`, `payment_due`, and `paid`.
- The available print actions may be functionally correct but may still require too much user judgment about which document to use in which situation.
- The patient-level unpaid summary exists, but it may not be obvious from the patient form when it is useful versus when the visit-level payment-due document is the better output.

### Provider friction candidates

- Providers still work mostly from the appointment and encounter flow, but they may be exposed to financial summary fields that are informative without being relevant to their daily task flow.
- Providers may experience mild confusion if checkout visibility is present but financial actions are intentionally reserved for front desk and owner roles.
- The transition from `completed` to `closed` remains operationally important, and any ambiguity there can indirectly affect checkout timing even though checkout itself is not a provider task.

## 6. Real Usability Polish Candidates

These are candidates for tiny future slices because they improve clarity or reduce clicks without widening business scope.

- Clarify checkout status visibility on the appointment form so front desk can tell at a glance whether no checkout exists, checkout is open, checkout is payment due, or checkout is paid.
- Reduce ambiguity around reopen behavior by making it explicit in the UI when `Start Checkout` is opening an existing session rather than creating a new one.
- Tighten print-action guidance in the checkout form so the correct document choice is more obvious for `paid` versus `payment_due`.

These stay inside the current narrow checkout posture.

## 7. Scope-Expanding Ideas That Should Not Be Mistaken For Polish

The following may sound like usability requests but would actually widen scope and should not be treated as simple UX hardening:
- adding due dates or aging logic
- adding partial payments or split tenders
- adding discounts, credits, refunds, or write-offs
- adding invoice numbering or pseudo-invoices
- adding ledger-style balances beyond current checkout state
- adding portal delivery, email delivery, or payment links
- adding accounting-linked patient statements
- adding rebooking or follow-up automation tied to checkout

These are outside Sprint 15 and outside the current frozen finance direction.

## 8. Recommended Tiny Future Slices

Only the following tiny slices are currently justified, and even these should be validated against real use first.

### Slice 1: clearer appointment checkout summary presentation

Reason:
- this would reduce front-desk scanning effort at the workflow hub without changing checkout rules

Expected boundary:
- presentation-only improvement on existing appointment checkout summary fields

### Slice 2: clearer existing-session reopen feedback

Reason:
- this would reduce uncertainty when staff click `Start Checkout` on appointments that already have a session

Expected boundary:
- message, label, or UI cue only
- no model or workflow expansion

### Slice 3: clearer print-action labeling

Reason:
- this would reduce wrong-document selection without creating new document types

Expected boundary:
- naming, button labeling, or small visibility polish only

No more than these 2 to 3 tiny slices should be considered from this planning note.

## 9. Finance-Direction Guardrail

Sprint 15 does not change the Sprint 14 decision.

The active recommendation remains:
- keep finance lightweight and custom inside `hc_checkout` for now

Sprint 15 should not be used to justify:
- invoice behavior
- receivables depth
- partial-payment depth
- ledger semantics
- a bridge to Odoo accounting

If future operational validation reveals pressure that matches the Sprint 14 trigger conditions, that accounting decision should be reopened explicitly rather than smuggled in as UX work.

## 10. Validation Approach For Any Future UX Slice

Before implementing even a tiny polish slice, validate:
- whether the friction occurs repeatedly in real front-desk or provider use
- whether the problem can be solved by presentation or guidance only
- whether the change preserves the appointment-as-hub posture
- whether the change avoids reopening accounting or billing depth

If the requested change fails those checks, it likely belongs to a new sprint decision rather than Sprint 15 UX hardening.

## 11. Explicit Non-Goals

Sprint 15 does not authorize:
- new product features
- new reports or document types
- new finance models
- invoices or accounting integration
- taxes
- discounts, refunds, or partial payments
- claims, portal, gateway, email, or SMS work
- encounter expansion
- lifecycle changes
- workflow coupling beyond the frozen Sprint 13 posture

## 12. Result

Sprint 15 is open as a planning-only operational validation sprint.

The intended outcome is not more business scope.

The intended outcome is a tighter understanding of whether the current implemented workflow has small, real usability friction worth addressing before any further expansion is considered.
