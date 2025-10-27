from typing import Tuple
from pathlib import Path
from datetime import date, timedelta
from runners.config import LAST_RUN_FILE_NAME, logger

LAST_RUN_FILE = Path(LAST_RUN_FILE_NAME)

def monthly_run() -> None:
    today = date.today()

    if should_run_monthly(today):
        start_date, end_date = get_month_range(today)
        logger.info(f"Running monthly from {start_date} to {end_date}")
        set_last_run_date(today)
        return start_date, end_date
    else:
        logger.info("Monthly run skipped not the first working day")

def get_last_run_date() -> date | None:
    if LAST_RUN_FILE.exists():
        content = LAST_RUN_FILE.read_text().strip()
        try:
            return date.fromisoformat(content)
        except ValueError:
            return None
    return None

def get_month_range(today: date) -> Tuple[str, str]:
    """"""
    first_day_last_month = today.replace(day=1).replace(month=today.month -1 if today.month > 1 else 12)
    if today.month == 1:
        first_day_last_month = first_day_last_month.replace(year=today.year - 1)
    return first_day_last_month.isoformat(), today.isoformat()

def set_last_run_date(d: date) -> None:
    LAST_RUN_FILE.write_text(d.isoformat())

def should_run_monthly(today: date) -> bool:
    last_run = get_last_run_date()
    return (
        today.day == 1 or
        (is_first_working_day(today) and (not last_run or last_run.month != today.month))
    )

def is_first_working_day(today: date) -> bool:
    first_day = today.replace(day=1)
    while first_day.weekday() >= 5:
        first_day += timedelta(days=1)
    return today == first_day


