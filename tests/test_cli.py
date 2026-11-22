import json

from fraudwatch.cli import main


def test_cli_generate_validate_profile(tmp_path, monkeypatch, capsys):
    out = tmp_path / "gen"
    report = tmp_path / "profile.json"
    monkeypatch.setattr("sys.argv", ["fraudwatch", "generate", "--output", str(out), "--count", "40"])
    main()
    csv_path = out / "transactions.csv"
    assert csv_path.exists()

    monkeypatch.setattr("sys.argv", ["fraudwatch", "validate", "--input", str(csv_path)])
    try:
        main()
    except SystemExit as exc:
        assert exc.code == 0

    monkeypatch.setattr(
        "sys.argv", ["fraudwatch", "profile", "--input", str(csv_path), "--report", str(report)]
    )
    main()
    assert json.loads(report.read_text())["row_count"] == 40
    assert "PASS" in capsys.readouterr().out
