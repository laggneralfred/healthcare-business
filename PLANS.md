# PLANS

This file is the source of truth for product planning for the alternative and complementary healthcare practice-management platform.

Status: Planning only. No implementation work is authorized from this document.

## Product Direction

Build a modular practice-management platform for small alternative and complementary healthcare practices, starting with acupuncture and expanding through shared core modules plus specialty-specific extensions.

Working platform assumption:
- Base the system on self-hosted `Odoo Community` first.
- Keep the architecture compatible with a later move to `Odoo Enterprise` if support burden or operational needs justify it.

Primary business goal:
- Create a realistic, low-stress software business that produces extra income without forcing early expansion into the most complex parts of healthcare software.

## Strategic Positioning

Initial wedge:
- Serve solo and small acupuncture clinics first.
- Prioritize cash-pay and light-insurance practices.
- Focus on operational calm: intake, booking, notes, checkout, packages, reminders, and rebooking.

Core thesis:
- Existing niche tools are either specialty-aware but clunky, or easy to use but too generic.
- The best opening is a calmer, modular system with practical AI that reduces daily admin work.

Non-goals for initial phases:
- Full insurance claims platform
- Hospital/enterprise workflows
- Broad support for all complementary care specialties at launch
- Native mobile apps
- Autonomous clinical AI

## Milestones

### Phase 0: Research and Validation

Objective:
- Validate the wedge, pricing, and switching triggers before building.

Deliverables:
- 20 to 30 structured practitioner interviews
- Workflow map for acupuncture, massage, and chiropractic
- Competitor comparison with pricing and complaint patterns
- Clickable prototype of key user flows
- Draft pricing hypotheses
- Initial compliance and hosting risk memo

Exit criteria:
- At least 5 interviewees confirm strong pain in the same workflow cluster
- At least 3 say they would seriously evaluate switching for a better solution
- Clear decision on first niche and first workflow scope

### Phase 1: Smallest Useful Product

Objective:
- Deliver a usable product for one niche with one operational backbone.

Target buyer:
- Solo or 2 to 5 provider acupuncture clinics with cash-pay or light-insurance workflows

Planned scope:
- Lead intake
- Patient intake
- Consent forms and signatures
- Appointment scheduling
- Encounter notes
- Checkout and payments
- Packages and memberships
- Reminders and rebooking
- Basic business dashboard
- AI intake summary
- AI note draft assistant

Deferred:
- Insurance claims
- Clearinghouse integrations
- Advanced inventory
- Multi-location groups
- Deep accounting customization

Exit criteria:
- First live pilot site
- Repeatable onboarding process
- Stable use of daily workflows without manual rescue

### Phase 2: Acupuncture-Specific MVP

Objective:
- Add enough specialty depth to justify choosing the product over generic alternatives.

Planned scope:
- TCM-oriented intake extensions
- Point charting
- Treatment plan tracking
- Herb or formula recommendations workflow
- Better patient follow-up automation
- Migration/import tools

Exit criteria:
- Clear evidence that acupuncture-specific features drive adoption
- Reduced charting friction compared with general-purpose systems

### Phase 3: Second Specialty Expansion

Objective:
- Prove the modular architecture works across another specialty.

Preferred next specialty:
- Massage therapy

Candidate scope:
- Body-region charting
- Modalities and pressure preferences
- Outcall support
- Tips and package handling
- Membership retention workflows

Exit criteria:
- Shared core remains stable
- Second specialty can be added mostly through extension modules

### Phase 4: Broader Platform and Advanced AI

Objective:
- Expand to additional specialties and add higher-leverage AI.

Potential scope:
- Chiropractic-lite operational workflows
- Better analytics and benchmarking
- Missing-chart QA
- Business copilot
- OCR document ingestion
- Later, carefully reviewed billing support features

Gate condition:
- Only pursue if support load and reliability are under control

## Assumptions

Product assumptions:
- Solo and small clinics remain underserved by current software.
- Many practices prefer simpler workflows over bloated enterprise feature sets.
- AI is valuable if it saves time inside existing workflows, not as a separate gimmick.
- Modular design is commercially and technically better than building three products at once.

Market assumptions:
- Acupuncture is a good first niche because founder expertise reduces discovery risk.
- Massage therapy is attractive later but more price-sensitive.
- Chiropractic has stronger budgets but substantially higher complexity and support burden.

Platform assumptions:
- `Odoo Community` is sufficient for early validation and early product development.
- The team can self-host and manage a narrow, secure deployment in early phases.
- Custom modules can remain maintainable if the base scope stays disciplined.

Business assumptions:
- Customers will pay for time savings, better charting flow, and better retention.
- A calm niche SaaS with moderate revenue can be preferable to a larger, high-stress business.

## Risks

### Strategic Risks

- Trying to serve too many specialties too early will destroy focus.
- Starting with insurance-heavy workflows will create a stress trap.
- Competing on feature count against mature incumbents is not realistic.

### Product Risks

- Charting UX may be harder than expected to make fast and pleasant.
- Migration from incumbent systems may become a major sales blocker.
- Scheduling edge cases can consume disproportionate product time.

### AI Risks

- AI note drafting may hallucinate or omit required details.
- Trust will collapse if AI outputs are not visibly grounded in source data.
- Privacy and PHI handling raise vendor, hosting, and audit concerns.

### Platform Risks

- `Odoo Community` may save license cost while increasing maintenance burden.
- Community add-ons may become fragile upgrade dependencies.
- Over-customizing Odoo could make upgrades painful and slow.

### Business Risks

- Price sensitivity may be higher than expected in massage and solo practices.
- Support demands may exceed what a solo founder can handle.
- Compliance diligence may slow sales if not addressed early and clearly.

## Open Questions

Market:
- Which exact workflow causes the strongest switching intent in acupuncture clinics?
- Will acupuncture buyers value AI enough to influence purchase decisions?
- Are there specific subsegments worth targeting first, such as fertility, pain, or general wellness practices?

Product:
- How much specialty charting is needed before the product feels credible?
- Is household/family scheduling needed in Phase 1 or later?
- Should packages and memberships be core from day one?

Platform:
- Which Odoo Community modules are stable enough to adopt directly?
- Which capabilities would push an edition switch to `Odoo Enterprise`?
- What hosting and deployment model best fits low-stress operations?

Compliance:
- What is the intended HIPAA posture in Phase 1?
- Which vendors can support a defensible PHI handling model?
- What audit logging and access controls are minimally necessary before pilots?

Commercial:
- What pricing model fits best: per provider, per location, or tiered plan?
- How much onboarding can be standardized?
- What level of migration support can be offered without turning services-heavy?

## Decision Rules

Use these rules to avoid stress traps:

- Do not add a feature unless it removes repeated weekly pain for the target buyer.
- Do not enter claims and insurance complexity until the self-pay workflow is solid.
- Do not support a second specialty until the first niche has a stable onboarding path.
- Do not add AI that cannot be reviewed and corrected by the user.
- Do not treat low license cost as success if maintenance burden climbs.

## Immediate Next Planning Outputs

- Interview script for practitioner discovery
- Clickable prototype scope and screens
- Odoo Community vs Enterprise decision memo
- Initial data model outline for core modules and specialty extensions
