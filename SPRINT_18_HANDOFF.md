# Sprint 18 Handoff

Status:
- Sprint 18 is implemented as a tiny Playwright-based pilot-support smoke suite
- This handoff freezes the Sprint 18 automation slice on top of the frozen Sprint 13 product baseline

## 1. Scope

Sprint 18 adds only the smallest approved browser-smoke layer.

Implemented scope:
- Playwright test structure
- dedicated Odoo-shell smoke-data seeding script
- role-based access smoke coverage
- front-desk closed-appointment to checkout smoke
- `payment_due` smoke
- patient unpaid-summary smoke
- late-payment collection smoke
- verification that the unpaid session disappears from the patient unpaid summary after payment

Sprint 18 does not add:
- product features
- workflow changes
- finance-scope expansion
- CI/CD integration
- broad UI automation
- human-usability replacement

## 2. Files Added Or Changed

Added:
- `package.json`
- `package-lock.json`
- `playwright.config.js`
- `scripts/setup_playwright_smoke_data.py`
- `tests/playwright/helpers/odoo.js`
- `tests/playwright/smoke.spec.js`
- `tests/playwright/README.md`
- `SPRINT_18_HANDOFF.md`

Changed:
- `.gitignore`
- `docker-compose.yml`

## 3. Automation Posture

The implemented smoke suite stays intentionally narrow.

Current covered paths:
- owner access to service-fee setup surface
- provider access to appointment without `Start Checkout`
- front-desk access to a closed appointment with `Start Checkout`
- checkout creation from the appointment
- pricing default visibility in checkout
- transition from `open` to `payment_due`
- patient statement availability while unpaid
- late payment collection
- unpaid session no longer available through patient statement after payment

Current non-goals remain:
- full module coverage
- provider encounter flow automation
- report layout/pixel validation
- broad regression coverage

## 4. Seed Data

The smoke suite uses dedicated seeded data from `scripts/setup_playwright_smoke_data.py`.

Current seed shape:
- one practice: `Smoke Clinic`
- three internal users:
  - `smoke.owner`
  - `smoke.frontdesk`
  - `smoke.provider`
- one patient: `Smoke Patient`
- one practitioner
- one appointment type with a default fee
- one closed appointment reset for each clean smoke run

The setup script now commits explicitly because `odoo shell` does not persist changes automatically without a commit.

## 5. Execution Posture

The working execution posture in this environment is container-local:
- run Playwright inside the `odoo` container
- target `http://127.0.0.1:8069` from inside that container
- use Firefox via Playwright for this local setup

Reason:
- the host shell in this environment could not reliably reach the mapped Odoo UI port for browser automation
- Chromium launch in the host shell also hit runtime restrictions
- the smallest working path was to run Playwright inside the container against the local Odoo web service

This is an environment/tooling decision, not a product-scope change.

## 6. Exact Commands Used

Dependency install on host:

```bash
cd /home/alfre/healthcare-business
npm install
```

One-time container browser dependency install:

```bash
cd /home/alfre/healthcare-business
docker compose exec --user root odoo bash -lc 'cd /workspace && PLAYWRIGHT_BROWSERS_PATH=/tmp/playwright-browsers npx playwright install-deps firefox'
docker compose exec odoo bash -lc 'cd /workspace && PLAYWRIGHT_BROWSERS_PATH=/tmp/playwright-browsers npx playwright install firefox'
```

Seed command used for the final clean run:

```bash
cd /home/alfre/healthcare-business
bash -lc "docker compose exec -T odoo bash -lc 'cd /workspace && odoo shell -d healthcare_dev < scripts/setup_playwright_smoke_data.py' > addons/.playwright-smoke-data.json"
```

Final passing smoke command:

```bash
cd /home/alfre/healthcare-business
docker compose exec odoo bash -lc 'cd /workspace && PLAYWRIGHT_BROWSERS_PATH=/tmp/playwright-browsers PLAYWRIGHT_BROWSER=firefox PLAYWRIGHT_OUTPUT_DIR=/tmp/playwright-results npm run smoke:test'
```

## 7. Final Result

Final Playwright result:

```text
Running 2 tests using 1 worker
  ✓  tests/playwright/smoke.spec.js:13:3 › Sprint 18 pilot smoke › role-based access stays within the frozen clinic baseline
  ✓  tests/playwright/smoke.spec.js:36:3 › Sprint 18 pilot smoke › front desk can move one checkout from payment_due to paid and clear the unpaid summary
  2 passed
```

Sprint 18 did not reveal a product regression in the frozen Sprint 13 clinic workflow.

## 8. Boundary Notes

Sprint 18 preserves:
- the Sprint 13 implemented product baseline
- the Sprint 14 finance-direction decision
- the Sprint 15 no-implementation guardrail as a product principle
- the Sprint 16 pilot-readiness posture
- the Sprint 17 decision to keep automation tiny and pilot-support only

Sprint 18 adds only a narrow automation layer around that frozen product posture.
