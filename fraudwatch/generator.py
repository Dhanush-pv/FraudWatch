"""Reproducible synthetic card-transaction generator; labels are for offline evaluation."""
from __future__ import annotations

import csv
import random
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path

from fraudwatch.schemas import TransactionEvent

MERCHANT_CATEGORIES = ["GROCERY", "ELECTRONICS", "TRAVEL", "FUEL", "FASHION", "GAMING"]
COUNTRIES = ["DE", "FR", "NL", "ES", "GB", "US", "TR", "PL"]
CHANNELS = ["POS", "ECOMMERCE", "ATM", "MOBILE"]
STATUSES = ["AUTHORIZED", "DECLINED", "REVERSED"]

def generate_transactions(output_dir: Path, count: int = 10_000, seed: int = 42) -> Path:
    if count < 1:
        raise ValueError("count must be at least 1")
    rng = random.Random(seed)
    start = datetime(2025, 1, 1, tzinfo=UTC)
    rows = []
    fraud_customers = {f"CUST-{i:05d}" for i in range(1, max(3, count // 80))}
    for i in range(1, count + 1):
        customer_num = rng.randint(1, max(50, count // 10))
        customer = f"CUST-{customer_num:05d}"
        suspicious = customer in fraud_customers and rng.random() < 0.32
        amount = (rng.uniform(450, 2500) if suspicious else rng.lognormvariate(3.2, 0.85))
        timestamp = start + timedelta(seconds=rng.randint(0, 365 * 24 * 3600))
        channel = rng.choice(CHANNELS)
        country = rng.choice(COUNTRIES)
        category = rng.choice(MERCHANT_CATEGORIES)
        status = rng.choices(STATUSES, weights=[88, 9, 3])[0]
        is_fraud = suspicious and rng.random() < 0.72
        row = {
            "event_id": f"EVT-{i:012d}",
            "transaction_id": f"TXN-{i:012d}",
            "event_version": 1,
            "event_type": "TRANSACTION_CREATED",
            "event_timestamp": timestamp.isoformat(),
            "transaction_timestamp": timestamp.isoformat(),
            "customer_id": customer,
            "card_id": f"CARD-{customer_num:06d}-{rng.randint(1,3)}",
            "merchant_id": f"MER-{rng.randint(1, max(30, count // 100)):06d}",
            "merchant_category": category,
            "merchant_country": country,
            "device_id": f"DEV-{rng.randint(1, max(40, count // 60)):06d}",
            "ip_address": f"10.{rng.randint(0,255)}.{rng.randint(0,255)}.{rng.randint(1,254)}",
            "channel": channel,
            "amount": f"{Decimal(str(amount)).quantize(Decimal('0.01'))}",
            "currency": "EUR",
            "status": status,
            "is_fraud": str(bool(is_fraud)).lower(),
            "source_system": "CARD_AUTHORIZATION",
        }
        validated = TransactionEvent.model_validate(row)
        rows.append(validated.model_dump(mode="json"))
    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / "transactions.csv"
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return target
