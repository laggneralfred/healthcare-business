# AI FEATURES

## Purpose

Rank AI features by real-world usefulness, implementation feasibility, and operational risk for a small complementary healthcare practice platform.

Planning rule:
- AI must reduce work inside a real workflow.
- AI must remain reviewable.
- AI must not create hidden clinical or compliance risk.

## Ranking Summary

| Rank | Feature | Usefulness | Feasibility | Risk | Recommended phase |
|---|---|---|---|---|---|
| 1 | Intake summarizer | High | High | Low to moderate | Phase 1 |
| 2 | Draft note assistant | High | Moderate | Moderate | Phase 1 |
| 3 | After-visit summary drafts | High | High | Low to moderate | Phase 1 |
| 4 | Rebooking and retention prompts | High | High | Low | Phase 1 |
| 5 | Message drafting for recalls and follow-up | Medium to high | High | Low | Phase 2 |
| 6 | Missing-chart QA | Medium to high | Moderate | Moderate | Phase 2 |
| 7 | Business copilot | Medium | Moderate | Moderate | Phase 2 |
| 8 | OCR document extraction | Medium | Moderate | Moderate | Phase 2 |
| 9 | Coding and billing assistant | Medium | Low to moderate | High | Phase 3 |
| 10 | Voice front-desk agent | Medium | Low to moderate | High | Phase 3 |

## Feature Details

### 1. Intake Summarizer

User problem solved:
- Practitioners waste time reviewing long intake forms before a visit.

Inputs:
- Intake forms
- prior visit summaries
- structured health history

Output:
- Concise visit prep summary with reason for visit, red flags, relevant history, and unresolved issues

Why it ranks highly:
- Clear time savings
- Low workflow disruption
- Easy for users to verify against source data

Main risks:
- Omission of important history
- Hallucinated summary details if not properly grounded

### 2. Draft Note Assistant

User problem solved:
- Treatment notes are repetitive and time-consuming.

Inputs:
- Intake summary
- prior notes
- specialty template selections
- optional visit transcript or dictated points

Output:
- Draft SOAP or encounter note for clinician review and signature

Why it ranks highly:
- Directly attacks one of the most painful daily tasks
- Strong differentiator if accuracy and speed are good

Main risks:
- False details in signed notes
- Overreliance by busy clinicians

Rule:
- Never auto-finalize. Provider review is mandatory.

### 3. After-Visit Summary Drafts

User problem solved:
- Home-care advice and follow-up instructions are inconsistently delivered.

Inputs:
- Finalized note
- provider selections
- reusable instruction library

Output:
- Patient-friendly summary and next-step instructions

Why it ranks highly:
- Useful to both clinic and patient
- Easier to constrain than open-ended clinical generation

Main risks:
- Overstating treatment claims
- Producing advice not approved by the provider

### 4. Rebooking and Retention Prompts

User problem solved:
- Owners do not know who should be contacted for rebooking or who is slipping away.

Inputs:
- appointment history
- no-show history
- package balance
- treatment cadence
- patient status

Output:
- Ranked outreach list and suggested next action

Why it ranks highly:
- Strong business value
- Low regulatory risk
- Easy to explain commercially

Main risks:
- Annoying patients with poor outreach timing
- Misleading scores if the heuristics are weak

### 5. Message Drafting for Recalls and Follow-Up

User problem solved:
- Front-desk communication is repetitive and inconsistent.

Inputs:
- patient status
- appointment history
- clinic templates

Output:
- Draft email or SMS for review or automated send under clear rules

Why it ranks well:
- Easy implementation path
- Tangible admin savings

Main risks:
- Tone mistakes
- Consent and opt-out compliance failures

### 6. Missing-Chart QA

User problem solved:
- Incomplete notes create quality, billing, or audit problems.

Inputs:
- draft note
- specialty documentation rules
- required fields

Output:
- Missing items, contradictions, and checklist warnings

Why it matters:
- Improves reliability and trust in the chart

Main risks:
- Users may treat warnings as legal advice
- Rules are specialty-dependent and can become brittle

### 7. Business Copilot

User problem solved:
- Owners struggle to interpret reports and take action.

Inputs:
- appointments
- revenue
- retention
- referral sources
- package utilization

Output:
- Plain-language insights and answers to business questions

Why it is attractive:
- Good owner-facing differentiation
- Makes reporting more actionable

Main risks:
- Low trust if answers are not tied to visible source metrics
- Query accuracy and permissions control

### 8. OCR Document Extraction

User problem solved:
- Manual entry from uploaded forms, scans, or external documents is slow.

Inputs:
- PDFs
- images
- scanned intake documents

Output:
- Structured fields, suggested imports, or review tasks

Why it matters:
- Helpful for onboarding and document-heavy clinics

Main risks:
- Extraction errors
- Handling sensitive uploaded documents

### 9. Coding and Billing Assistant

User problem solved:
- Coding and claim prep take expertise and time.

Inputs:
- note content
- selected services
- diagnosis choices
- payer rules

Output:
- Suggested codes or claim checklist

Why it is lower priority:
- Valuable mainly in insurance-heavy workflows
- Harder to get right
- Higher liability and support burden

Main risks:
- Incorrect coding
- User overtrust
- Rapid rule changes

### 10. Voice Front-Desk Agent

User problem solved:
- Clinics miss calls and spend time answering repetitive questions.

Inputs:
- business rules
- scheduling availability
- FAQ content

Output:
- Call handling, intake capture, or callback routing

Why it is later:
- High failure visibility
- Complex real-time interactions
- Support burden is substantial

Main risks:
- Bad call experiences
- Booking errors
- Reputation damage from obvious failure

## Priority Guidance

Phase 1 AI should do three things well:

- summarize intake
- draft notes
- improve rebooking and follow-up

These are high-value, workflow-native, and relatively controllable.

## AI Design Principles

- Every output must be reviewable by the user.
- Every generated summary should link back to source inputs where possible.
- AI should assist decisions, not silently make them.
- Clinical or billing outputs must remain explicitly advisory.
- If a feature cannot be explained simply, it should not be in Phase 1.

## Features to Avoid Early

- autonomous clinical recommendations
- automated diagnosis support
- fully automatic claim submission
- open-ended patient chatbot with clinical advice
- broad “chat with all patient data” before auditability is mature
