"""
Command-line interface for triggering pipeline.

Supports:
- -week → weekly_runner
- -month → monthly_runner
- -gui → launch GUI interface
"""
import argparse
from parser import run_pipeline
from runners import monthly_run, get_last_week_range
from gui import PinGui

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PIN Parser CLI")
    parser.add_argument("-week", action="store_true", help="Run weekly")
    parser.add_argument("-month", action="store_true", help="Run monthly")
    parser.add_argument("-gui", action="store_true", help="Run GUI")

    args = parser.parse_args()

    if args.month:
        run_pipeline(monthly_run())
    elif args.week:
        run_pipeline(get_last_week_range())
    elif args.gui:
        PinGui().run()
    else:
        print("No mode selected. Use -week or -month")