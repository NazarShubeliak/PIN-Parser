"""
Command-line interface for triggering pipeline.

Supports:
- -week → weekly_runner
- -month → monthly_runner

Can be extended with --from, --to, --dry-run, etc.
"""
import argparse
from parser import run_pipeline
from runners import monthly_run, get_last_week_range

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PIN Parser CLI")
    parser.add_argument("-week", action="store_true", help="Run weekly")
    parser.add_argument("-month", action="store_true", help="Run monthly")

    args = parser.parse_args()

    if args.month:
        run_pipeline(monthly_run())
    elif args.week:
        run_pipeline(get_last_week_range())
    else:
        print("No mode selected. Use -week or -month")