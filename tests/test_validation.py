import pandas as pd

from fraudwatch.generator import generate_transactions
from fraudwatch.validation import validate_extract


def test_generated_extract_passes(tmp_path):
    path = generate_transactions(tmp_path, count=30)
    assert validate_extract(path) == []

def test_duplicate_transaction_id_is_rejected(tmp_path):
    path = generate_transactions(tmp_path, count=5)
    frame = pd.read_csv(path)
    frame.loc[1, "transaction_id"] = frame.loc[0, "transaction_id"]
    frame.to_csv(path, index=False)
    assert "transaction_id contains duplicates" in validate_extract(path)

def test_missing_columns_are_reported(tmp_path):
    path = tmp_path / "bad.csv"
    path.write_text("transaction_id,amount\nTXN-00000001,10.00\n")
    assert validate_extract(path)[0].startswith("Missing columns:")
