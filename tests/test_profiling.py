from fraudwatch.generator import generate_transactions
from fraudwatch.profiling import profile_transactions


def test_profile_contains_core_metrics(tmp_path):
    source = generate_transactions(tmp_path / "source", count=50, seed=4)
    report_path = tmp_path / "profile.json"
    report = profile_transactions(source, report_path)
    assert report["row_count"] == 50
    assert report["duplicate_transaction_ids"] == 0
    assert "amount" in report["columns"]
    assert report_path.exists()
