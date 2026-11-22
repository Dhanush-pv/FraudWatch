.PHONY: install generate validate profile test lint db-up db-down
install:
	pip install -e ".[dev]"
generate:
	python -m fraudwatch generate --output data/generated --count 10000 --seed 42
validate:
	python -m fraudwatch validate --input data/generated/transactions.csv
profile:
	python -m fraudwatch profile --input data/generated/transactions.csv --report reports/week-1/data-profile.json
test:
	pytest -q
lint:
	ruff check fraudwatch tests
db-up:
	docker compose up -d postgres
db-down:
	docker compose down
