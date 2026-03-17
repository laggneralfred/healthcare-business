# Playwright Smoke Suite

This is a tiny pilot-support smoke suite for the frozen Sprint 13 clinic workflow.

Recommended run posture for this repo:
- run the smoke suite inside the local `odoo` container
- keep it local-only
- use it as pilot-support verification, not broad UI coverage

One-time container browser setup:
```bash
cd /home/alfre/healthcare-business
docker compose exec --user root odoo bash -lc 'cd /workspace && PLAYWRIGHT_BROWSERS_PATH=/tmp/playwright-browsers npx playwright install-deps firefox'
docker compose exec odoo bash -lc 'cd /workspace && PLAYWRIGHT_BROWSERS_PATH=/tmp/playwright-browsers npx playwright install firefox'
```

Seed the dedicated smoke data:

```bash
cd /home/alfre/healthcare-business
bash -lc "docker compose exec -T odoo bash -lc 'cd /workspace && odoo shell -d healthcare_dev < scripts/setup_playwright_smoke_data.py' > addons/.playwright-smoke-data.json"
```

Run the smoke suite:

```bash
cd /home/alfre/healthcare-business
docker compose exec odoo bash -lc 'cd /workspace && PLAYWRIGHT_BROWSERS_PATH=/tmp/playwright-browsers PLAYWRIGHT_BROWSER=firefox PLAYWRIGHT_OUTPUT_DIR=/tmp/playwright-results npm run smoke:test'
```

The smoke data setup writes a generated file to `addons/.playwright-smoke-data.json`.

The suite is intentionally small:
- role-based access smoke
- front-desk checkout to `payment_due`
- patient unpaid summary
- late payment collection
- unpaid summary no longer available after payment
