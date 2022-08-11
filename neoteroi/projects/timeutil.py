import calendar
import re
from dataclasses import dataclass
from datetime import date, datetime
from typing import Dict, Iterable, List, Tuple

from dateutil import rrule
from dateutil.relativedelta import relativedelta

_LASTS_PATTERN = re.compile(r"(?P<amount>\d+)\s?(?P<unit>\w+)")


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

QUARTERS_BY_MONTH_NUMBER: Dict[int, int] = {
    1: 1,
    2: 1,
    3: 1,
    4: 2,
    5: 2,
    6: 2,
    7: 3,
    8: 3,
    9: 3,
    10: 4,
    11: 4,
    12: 4,
}


_MIN_MONTHS_BY_QUARTER_NUMBER: Dict[int, int] = {
    1: 1,
    2: 4,
    3: 7,
    4: 10,
}


_MAX_MONTHS_BY_QUARTER_NUMBER: Dict[int, int] = {
    1: 3,
    2: 6,
    3: 9,
    4: 12,
}


@dataclass(frozen=True)
class Quarter:
    year: int
    number: int

    @property
    def min_month(self) -> int:
        return _MIN_MONTHS_BY_QUARTER_NUMBER[self.number]

    @property
    def max_month(self) -> int:
        return _MAX_MONTHS_BY_QUARTER_NUMBER[self.number]

    @property
    def min_month_date(self) -> date:
        return date(self.year, self.min_month, 1)

    @property
    def max_month_date(self) -> date:
        return date(self.year, self.max_month, 1)

    def iter_dates(self) -> Iterable[date]:
        for value in iter_months_between_dates(
            self.min_month_date, self.max_month_date
        ):
            yield value.date()


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
        return relativedelta(hours=amount)

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


def iter_months_between_dates_of_year(
    min_date: date, max_date: date, year: int
) -> Iterable[date]:
    if min_date.year > year:
        raise ValueError("Year out of boundary")
    start_date = min_date.replace(day=1)
    end_date = get_last_day_of_month(max_date)

    for month_date in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
        if month_date.year == year:
            yield month_date.date()
        if month_date.year > year:
            break


def iter_months_between_dates(min_date: date, max_date: date) -> Iterable[datetime]:
    """
    Iterates month dates between two dates.
    """
    start_date = min_date.replace(day=1)
    end_date = max_date.replace(day=1)

    for month_date in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
        yield month_date


def iter_days_between_dates(min_date: date, max_date: date) -> Iterable[date]:
    """
    Iterates dates between two dates.
    """
    start_date = min_date.replace(day=1)
    end_date = get_last_day_of_month(max_date)

    for day_date in rrule.rrule(rrule.DAILY, dtstart=start_date, until=end_date):
        yield day_date


def iter_quarters_between_dates(min_date: date, max_date: date) -> Iterable[Quarter]:
    """
    Iterates quarters numbers between two dates.
    """
    current_value: int = -1
    for month_date in iter_months_between_dates(min_date, max_date):
        value = QUARTERS_BY_MONTH_NUMBER[month_date.month]

        if value != current_value:
            current_value = value
            yield Quarter(month_date.year, value)


def iter_weeks_between_dates(
    min_date: date, max_date: date
) -> Iterable[Tuple[int, date]]:
    current_week_year, current_week_number, _ = min_date.isocalendar()
    current_week_date = date.fromisocalendar(current_week_year, current_week_number, 1)
    end_date = get_last_day_of_month(max_date)
    week_date: datetime

    for week_date in rrule.rrule(
        rrule.WEEKLY, dtstart=current_week_date, until=end_date
    ):
        yield week_date.isocalendar()[1], week_date.date()


def get_next_week_date(week_number, week_date) -> date:
    try:
        return date.fromisocalendar(week_date.year, week_number + 1, 1)
    except ValueError:
        return date.fromisocalendar(week_date.year + 1, 1, 1)


def get_first_day_of_month(value: date) -> date:
    """
    Returns the date of the first day of a month from a given date.
    """
    return date(value.year, value.month, 1)


def get_last_day_of_month(value: date) -> date:
    """
    Returns the date of the last day of a month from a given date.
    """
    return date(
        value.year, value.month, calendar.monthrange(value.year, value.month)[1]
    )


def date_delta(value1: date, value2: date):
    """
    Returns the delta between the date components of two dates, supporting
    datetimes.
    Note: a simple substraction causes TypeError if any of the two dates
    is a datetime.
    """
    if isinstance(value1, datetime):
        value1 = value1.date()
    if isinstance(value2, datetime):
        value2 = value2.date()
    return value1 - value2
