"""
Weekly pipeline trigger.

Runs every Monday, checks previous week's documents.
If documents exist → runs pipeline.
Else → exits silently.
"""
from datetime import date, timedelta
from typing import Tuple

def get_last_week_range() -> Tuple[str, str]:
    """Returns ISO-formatted start and end dates for the previous week"""
    today = date.today()
    last_monday = today - timedelta(days=today.weekday() + 7)
    last_sunday = last_monday + timedelta(days=6)

    return last_monday.isoformat(), last_sunday.isoformat()
