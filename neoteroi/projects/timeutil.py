import re
from datetime import date
from typing import Iterable, List, Tuple

from dateutil import rrule
from dateutil.relativedelta import relativedelta

_LASTS_PATTERN = re.compile(r"(?P<amount>\d+)\s(?P<unit>\w+)")


MONTHS: List[Tuple[int, str]] = [
    (1, "January"),
    (2, "February"),
    (3, "March"),
    (4, "April"),
    (5, "May"),
    (6, "June"),
    (7, "July"),
    (8, "August"),
    (9, "September"),
    (10, "October"),
    (11, "November"),
    (12, "December"),
]


class InvalidLastsValue(ValueError):
    def __init__(self, value: str) -> None:
        super().__init__(f"Invalid lasts value: {value}.")


class UnsupportedLastsUnit(ValueError):
    def __init__(self, value: str, unit: str) -> None:
        super().__init__(f"Unsupported lasts unit: {unit} in {value}.")


def parse_lasts(value: str) -> relativedelta:
    """
    Parses a lasts value into an instance of timedelta.

    For example:
    "20 days" -> timedelta(days=20)
    """
    if not value:
        raise ValueError("Missing input value")

    match = _LASTS_PATTERN.match(value)
    if not match:
        raise InvalidLastsValue(value)
    groups = match.groupdict()

    try:
        amount = int(groups["amount"])
    except ValueError:
        raise InvalidLastsValue(value)

    unit = groups["unit"].lower()

    if unit in {"year", "years", "y"}:
        return relativedelta(days=amount * 365)

    if unit in {"month", "months", "m"}:
        return relativedelta(months=amount)

    if unit in {"week", "weeks", "w"}:
        return relativedelta(weeks=amount)

    if unit in {"day", "days", "d"}:
        return relativedelta(days=amount)

    if unit in {"hour", "hours", "h"}:
        return relativedelta(days=amount)

    raise UnsupportedLastsUnit(value, unit)


def iter_years_between_dates(min_date: date, max_date: date) -> Iterable[int]:
    if max_date < min_date:
        raise ValueError("max_date must be smaller than min_date.")

    year = min_date.year
    max_year = max_date.year

    yield year

    while year < max_year:
        year += 1
        yield year


def iter_months_between_dates(min_date: date, max_date: date) -> Iterable[date]:
    """
    Iterates month dates between two dates.

    TODO: remove?
    """
    start_date = min_date.replace(day=1)
    end_date = max_date.replace(day=1)

    for month_date in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
        yield month_date


def this_week() -> int:
    return date.today().isocalendar().week


def iter_weeks_of_year(year: int) -> Iterable[Tuple[int, date]]:
    week_number = 0
    while True:
        week_number += 1
        try:
            yield week_number, date.fromisocalendar(year, week_number, 1)
        except ValueError:
            break


def get_next_week_date(week_number, week_date) -> date:
    try:
        return date.fromisocalendar(week_date.year, week_number + 1, 1)
    except ValueError:
        return date.fromisocalendar(week_date.year + 1, 1, 1)
