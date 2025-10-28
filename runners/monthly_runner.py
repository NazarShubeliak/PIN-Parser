"""
Monthly pipeline trigger.

Runs on first working day of the month.
Processes all documents from 1st of previous month to today.
Tracks last run to avoid duplicates.
"""
from typing import Tuple
from pathlib import Path
from datetime import date, timedelta
from runners.config import LAST_RUN_FILE_NAME, logger

LAST_RUN_FILE = Path(LAST_RUN_FILE_NAME)

def monthly_run() -> None:
    """
    Entry point for monthly pipeline trigger.

    If today is the first working day of the month (or the 1st), and the pipeline hasn't run yet this month,
    it calculates the date range (from 1st of previous month to today), logs it, and returns the range.

    Returns:
        Optional[Tuple[str, str]]: Start and end dates in ISO format if pipeline should run, else None.
    """
    today = date.today()

    if should_run_monthly(today):
        start_date, end_date = get_month_range(today)
        logger.info(f"Running monthly from {start_date} to {end_date}")
        set_last_run_date(today)
        return start_date, end_date
    else:
        logger.info("Monthly run skipped not the first working day")

def get_last_run_date() -> date | None:
    """
    Reads the last run date from the tracking file.

    Returns:
        Optional[date]: The date of the last successful monthly run, or None if not found or invalid.
    """
    if LAST_RUN_FILE.exists():
        content = LAST_RUN_FILE.read_text().strip()
        try:
            return date.fromisoformat(content)
        except ValueError:
            return None
    return None

def get_month_range(today: date) -> Tuple[str, str]:
    """
    Calculates the date range for the monthly pipeline.

    Args:
        today (date): The current date.

    Returns:
        Tuple[str, str]: Start date (1st of previous month) and end date (today), both in ISO format.
    """
    first_day_last_month = today.replace(day=1).replace(month=today.month -1 if today.month > 1 else 12)
    if today.month == 1:
        first_day_last_month = first_day_last_month.replace(year=today.year - 1)
    return first_day_last_month.isoformat(), today.isoformat()

def set_last_run_date(d: date) -> None:
    """
    Saves the given date as the last successful monthly run.

    Args:
        d (date): The date to store.
    """
    LAST_RUN_FILE.write_text(d.isoformat())

def should_run_monthly(today: date) -> bool:
    """
    Determines whether the monthly pipeline should run today.

    Conditions:
    - Today is the 1st of the month
    - OR today is the first working day and the pipeline hasn't run this month

    Args:
        today (date): The current date.

    Returns:
        bool: True if the pipeline should run, False otherwise.
    """
    last_run = get_last_run_date()
    return (
        today.day == 1 or
        (is_first_working_day(today) and (not last_run or last_run.month != today.month))
    )

def is_first_working_day(today: date) -> bool:
    """
    Checks if today is the first working (non-weekend) day of the month.

    Args:
        today (date): The current date.

    Returns:
        bool: True if today is the first working day, False otherwise.
    """
    first_day = today.replace(day=1)
    while first_day.weekday() >= 5:
        first_day += timedelta(days=1)
    return today == first_day


