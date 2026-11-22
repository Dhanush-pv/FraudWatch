import json
from pathlib import Path

from fraudwatch.schemas import TransactionEvent

CONTRACT = Path(__file__).resolve().parents[1] / "contracts" / "transaction-event.schema.json"


def test_json_schema_matches_pydantic_fields():
    schema = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert set(schema["properties"]) == set(TransactionEvent.model_fields)
    assert set(schema["required"]) == set(TransactionEvent.model_fields)
    assert schema["additionalProperties"] is False
