# Sprint Index

This index tracks frozen sprint baselines and the expected matching Git freeze tags for this repository.

Current authoritative implemented baseline:
- [SPRINT_18_HANDOFF.md](/home/alfre/healthcare-business/SPRINT_18_HANDOFF.md)

Freeze tag naming convention:
- `sprint-<number>-freeze`

Freeze commit naming convention:
- `Sprint <number> freeze: <baseline summary>`

Note:
- this document is the process index for intended sprint-freeze tags
- actual tag existence must be verified in a git-enabled clone before marking a sprint fully closed
- `SPRINT_2_SLICE_2A_HANDOFF.md` is not a full sprint baseline and does not get its own freeze tag by default

## Frozen Baselines

| Sprint | Authoritative Baseline | Freeze Tag | Scope Summary |
| --- | --- | --- | --- |
| 1 | [SPRINT_1_HANDOFF.md](/home/alfre/healthcare-business/SPRINT_1_HANDOFF.md) | `sprint-1-freeze` | Foundation baseline |
| 2 | [SPRINT_2_HANDOFF.md](/home/alfre/healthcare-business/SPRINT_2_HANDOFF.md) | `sprint-2-freeze` | Intake and consent baseline |
| 3 | [SPRINT_3_HANDOFF.md](/home/alfre/healthcare-business/SPRINT_3_HANDOFF.md) | `sprint-3-freeze` | Encounter baseline |
| 4 | [SPRINT_4_HANDOFF.md](/home/alfre/healthcare-business/SPRINT_4_HANDOFF.md) | `sprint-4-freeze` | Frozen Sprint 4 baseline |
| 5 | [SPRINT_5_HANDOFF.md](/home/alfre/healthcare-business/SPRINT_5_HANDOFF.md) | `sprint-5-freeze` | Frozen Sprint 5 baseline |
| 6 | [SPRINT_6_HANDOFF.md](/home/alfre/healthcare-business/SPRINT_6_HANDOFF.md) | `sprint-6-freeze` | Frozen Sprint 6 baseline |
| 7 | [SPRINT_7_HANDOFF.md](/home/alfre/healthcare-business/SPRINT_7_HANDOFF.md) | `sprint-7-freeze` | Narrow post-close checkout baseline |
| 8 | [SPRINT_8_HANDOFF.md](/home/alfre/healthcare-business/SPRINT_8_HANDOFF.md) | `sprint-8-freeze` | Structured pricing-default baseline |
| 9 | [SPRINT_9_HANDOFF.md](/home/alfre/healthcare-business/SPRINT_9_HANDOFF.md) | `sprint-9-freeze` | Narrow multi-line checkout baseline |
| 10 | [SPRINT_10_HANDOFF.md](/home/alfre/healthcare-business/SPRINT_10_HANDOFF.md) | `sprint-10-freeze` | Printable checkout summary baseline |
| 11 | [SPRINT_11_HANDOFF.md](/home/alfre/healthcare-business/SPRINT_11_HANDOFF.md) | `sprint-11-freeze` | Payment-due document baseline |
| 12 | [SPRINT_12_HANDOFF.md](/home/alfre/healthcare-business/SPRINT_12_HANDOFF.md) | `sprint-12-freeze` | Patient-level unpaid summary baseline |
| 13 | [SPRINT_13_HANDOFF.md](/home/alfre/healthcare-business/SPRINT_13_HANDOFF.md) | `sprint-13-freeze` | Late-payment capture baseline |
| 18 | [SPRINT_18_HANDOFF.md](/home/alfre/healthcare-business/SPRINT_18_HANDOFF.md) | `sprint-18-freeze` | Tiny Playwright pilot-support smoke-suite baseline |

## Frozen Decision Records

These are frozen sprint records, but they are not implemented product baselines and do not define freeze tags in this index by default.

| Sprint | Frozen Record | Posture Summary |
| --- | --- | --- |
| 14 | [SPRINT_14_DECISION.md](/home/alfre/healthcare-business/SPRINT_14_DECISION.md) | Stay lightweight/custom in `hc_checkout` for now |
| 15 | [SPRINT_15_DECISION.md](/home/alfre/healthcare-business/SPRINT_15_DECISION.md) | No UX-hardening implementation authorized without stronger evidence |
| 16 | [SPRINT_16_DECISION.md](/home/alfre/healthcare-business/SPRINT_16_DECISION.md) | Pilot-readiness checklist and decision only |
| 17 | [SPRINT_17_DECISION.md](/home/alfre/healthcare-business/SPRINT_17_DECISION.md) | Playwright recommended; only a tiny smoke suite justified |

## Closure Reference

Use [SPRINT_CLOSURE_CHECKLIST.md](/home/alfre/healthcare-business/SPRINT_CLOSURE_CHECKLIST.md) when freezing any future sprint.
