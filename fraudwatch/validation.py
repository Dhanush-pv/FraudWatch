"""Dataset-level checks beyond per-event Pydantic validation."""
from pathlib import Path

import pandas as pd

REQUIRED = {
    "event_id", "transaction_id", "event_version", "event_timestamp",
    "transaction_timestamp", "customer_id", "card_id", "merchant_id",
    "merchant_category", "merchant_country", "device_id", "ip_address",
    "channel", "amount", "currency", "status", "is_fraud", "source_system",
}

def validate_extract(path: Path) -> list[str]:
    errors = []
    frame = pd.read_csv(path)
    missing = sorted(REQUIRED - set(frame.columns))
    if missing:
        errors.append(f"Missing columns: {', '.join(missing)}")
        return errors
    if frame.empty:
        errors.append("Extract contains no rows")
    if frame["transaction_id"].isna().any():
        errors.append("transaction_id contains nulls")
    if frame["transaction_id"].duplicated().any():
        errors.append("transaction_id contains duplicates")
    amount = pd.to_numeric(frame["amount"], errors="coerce")
    if amount.isna().any() or (amount <= 0).any():
        errors.append("amount must contain positive numeric values")
    if not frame["currency"].astype(str).str.fullmatch(r"[A-Z]{3}").all():
        errors.append("currency must be a three-letter uppercase code")
    return errors
