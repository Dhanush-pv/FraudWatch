# FraudWatch+ — Streaming Fraud Detection & Fraud-Ring Intelligence

**Author:** Dhanush  


FraudWatch+ is an end-to-end fraud analytics platform designed around transaction CDC, streaming feature computation, explainable fraud alerts, model lifecycle management, drift monitoring and graph-based fraud-ring discovery.


## architecture

PostgreSQL → Debezium CDC → Redpanda → Spark Structured Streaming → S3 Bronze/Silver/Gold (Iceberg) → dbt → Athena/Redshift → analytics and investigator workflow.

Advanced capabilities planned:
- feature store for online/offline feature consistency;
- MLflow experiment tracking and model registry;
- cost-sensitive fraud thresholds and explainable alert reasons;
- drift monitoring for feature and prediction distributions;
- Neo4j graph analysis for shared devices, cards, IPs and merchant relationships.


## Repository layout
```text
contracts/   JSON Schema event contract
data/        sample extract (generated output is git-ignored)
docs/        requirements, architecture, ERD, data dictionary, ADR, runbook,
fraudwatch/  generator, schemas, validation, profiling, CLI
reports/     data profile JSON
sql/         PostgreSQL source schema
tests/       pytest suite
```

## Quick start

Requirements: Python 3.11+.

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

pip install -e ".[dev]"
python -m fraudwatch generate --output data/generated --count 10000 --seed 42
python -m fraudwatch validate --input data/generated/transactions.csv
python -m fraudwatch profile --input data/generated/transactions.csv --report reports/week-1/data-profile.json
pytest -q
```

Optional PostgreSQL 16:

```bash
docker compose up -d postgres
```

The DDL is mounted into PostgreSQL's initialization directory. For an already initialized volume, apply it manually using `psql -f sql/001_source_schema.sql`.

## Synthetic data warning
The generator deliberately creates suspicious clusters and a synthetic `is_fraud` label to support offline development. It is not a realistic estimate of fraud prevalence, and the label is not suitable for claims about model performance. Real PaySim/IEEE-CIS data adapters and label mapping need to be built and assessed separately.

## Project milestones
1. Transaction foundation, schema, generator and profiling.
2. PostgreSQL CDC with Debezium and Redpanda topics.
3. Spark Structured Streaming, idempotency, rules and Bronze/Silver.
4. Iceberg Gold, dbt marts, feature engineering and feature-store contract.
5. MLflow experiments, model evaluation, thresholds and drift monitoring.
6. Neo4j fraud-ring analysis, investigator workflow, observability and deployment hardening.

## Data-quality and modeling principles
- event time and transaction time are distinct;
- transaction keys must be idempotent;
- CDC updates must be version-aware;
- retries and dead-letter handling are required;
- replay/backfill must be supported;
- fraud evaluation must prioritize precision/recall, PR-AUC, confusion matrices and business cost, not accuracy alone.

## Author
**Dhanush**

## License
MIT — see [LICENSE](LICENSE).
