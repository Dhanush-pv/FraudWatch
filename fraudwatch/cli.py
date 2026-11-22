import argparse
import json
from pathlib import Path

from fraudwatch.generator import generate_transactions
from fraudwatch.profiling import profile_transactions
from fraudwatch.validation import validate_extract


def main():
    parser = argparse.ArgumentParser(prog="fraudwatch")
    sub = parser.add_subparsers(dest="command", required=True)
    gen = sub.add_parser("generate")
    gen.add_argument("--output", type=Path, default=Path("data/generated"))
    gen.add_argument("--count", type=int, default=10_000)
    gen.add_argument("--seed", type=int, default=42)
    val = sub.add_parser("validate")
    val.add_argument("--input", type=Path, default=Path("data/generated/transactions.csv"))
    prof = sub.add_parser("profile")
    prof.add_argument("--input", type=Path, default=Path("data/generated/transactions.csv"))
    prof.add_argument("--report", type=Path, default=Path("reports/week-1/data-profile.json"))
    args = parser.parse_args()
    if args.command == "generate":
        path = generate_transactions(args.output, args.count, args.seed)
        print(f"Generated {args.count:,} transactions: {path}")
    elif args.command == "validate":
        errors = validate_extract(args.input)
        print("PASS" if not errors else "\n".join(errors))
        raise SystemExit(0 if not errors else 1)
    elif args.command == "profile":
        report = profile_transactions(args.input, args.report)
        print(json.dumps({k:v for k,v in report.items() if k != "columns"}, indent=2))
        print(f"Profile saved: {args.report}")

if __name__ == "__main__":
    main()
