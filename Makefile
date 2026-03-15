.PHONY: test-scheduling test-encounter test-intake test-consent test-core test-clinic test-clinic-summary restart-odoo sprint-freeze

test-scheduling:
	docker compose exec odoo odoo -d healthcare_dev -u hc_scheduling --test-enable --test-tags /hc_scheduling --http-port=8070 --stop-after-init

test-encounter:
	docker compose exec odoo odoo -d healthcare_dev -u hc_encounter --test-enable --http-port=8070 --stop-after-init

test-intake:
	docker compose exec odoo odoo -d healthcare_dev -u hc_intake --test-enable --http-port=8070 --stop-after-init

test-consent:
	docker compose exec odoo odoo -d healthcare_dev -u hc_consent --test-enable --http-port=8070 --stop-after-init

test-core:
	docker compose exec odoo odoo -d healthcare_dev -u hc_encounter,hc_intake --test-enable --http-port=8070 --stop-after-init

test-clinic:
	docker compose exec odoo odoo -d healthcare_dev -u hc_scheduling,hc_encounter,hc_intake,hc_consent --test-enable --test-tags /hc_scheduling,/hc_encounter,/hc_intake,/hc_consent --http-port=8070 --stop-after-init

test-clinic-summary:
	mkdir -p logs
	bash -o pipefail -c 'docker compose exec odoo odoo -d healthcare_dev -u hc_scheduling,hc_encounter,hc_intake,hc_consent --test-enable --test-tags /hc_scheduling,/hc_encounter,/hc_intake,/hc_consent --http-port=8070 --stop-after-init 2>&1 | tee logs/test-clinic.log'
	@echo
	@echo "Test Summary"
	@grep -E "odoo.tests.result:|odoo.tests.stats:" logs/test-clinic.log || true

restart-odoo:
	docker compose restart odoo

sprint-freeze:
	@[ -n "$(SPRINT)" ] || (echo "Usage: make sprint-freeze SPRINT=<number> MESSAGE='Sprint <number> freeze: <summary>' [REMOTE=origin]"; exit 1)
	@[ -n "$(MESSAGE)" ] || (echo "Usage: make sprint-freeze SPRINT=<number> MESSAGE='Sprint <number> freeze: <summary>' [REMOTE=origin]"; exit 1)
	bash scripts/sprint-freeze-tag.sh "$(SPRINT)" "$(MESSAGE)" "$(if $(REMOTE),$(REMOTE),origin)"
