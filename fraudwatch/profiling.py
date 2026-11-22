"""Data profiling and quality summary for generated transaction extracts."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

NUMERIC = ["amount"]
CATEGORICAL = ["channel", "status", "merchant_category", "merchant_country", "currency"]

def profile_transactions(csv_path: Path, report_path: Path | None = None) -> dict:
    frame = pd.read_csv(csv_path)
    if frame.empty:
        raise ValueError("Cannot profile an empty transaction extract")
    report = {
        "dataset": csv_path.name,
        "row_count": len(frame),
        "column_count": len(frame.columns),
        "columns": {},
        "duplicate_transaction_ids": int(frame["transaction_id"].duplicated().sum()),
        "fraud_label_rate": float(frame["is_fraud"].astype(str).str.lower().eq("true").mean()),
    }
    for column in frame.columns:
        item = {
            "null_count": int(frame[column].isna().sum()),
            "distinct_count": int(frame[column].nunique(dropna=True)),
        }
        if column in NUMERIC:
            series = pd.to_numeric(frame[column], errors="coerce")
            item["min"] = float(series.min())
            item["median"] = float(series.median())
            item["p95"] = float(series.quantile(0.95))
            item["max"] = float(series.max())
        if column in CATEGORICAL:
            item["top_values"] = {
                str(k): int(v) for k, v in frame[column].value_counts().head(10).items()
            }
        report["columns"][column] = item
    if report_path:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report
