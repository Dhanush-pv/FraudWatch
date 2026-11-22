import csv

import pytest

from fraudwatch.generator import generate_transactions
from fraudwatch.schemas import TransactionEvent


def test_generator_is_reproducible(tmp_path):
    a = generate_transactions(tmp_path / "a", count=20, seed=7)
    b = generate_transactions(tmp_path / "b", count=20, seed=7)
    assert a.read_text() == b.read_text()

def test_generator_outputs_schema_valid_rows(tmp_path):
    path = generate_transactions(tmp_path, count=25, seed=10)
    with path.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 25
    for row in rows:
        row["event_version"] = int(row["event_version"])
        row["amount"] = row["amount"]
        row["is_fraud"] = row["is_fraud"].lower() == "true"
        TransactionEvent.model_validate(row)

def test_generator_rejects_zero_count(tmp_path):
    with pytest.raises(ValueError):
        generate_transactions(tmp_path, count=0)
