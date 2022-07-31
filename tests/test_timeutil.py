import pytest
from dateutil.parser import parse as parse_date
from dateutil.relativedelta import relativedelta

from neoteroi.projects.timeutil import iter_years_between_dates, parse_lasts


@pytest.mark.parametrize(
    "value,expected_result",
    [
        ("1 year", relativedelta(days=365)),
        ("2 years", relativedelta(days=365 * 2)),
        ("3 y", relativedelta(days=365 * 3)),
        ("1 month", relativedelta(months=1)),
        ("2 months", relativedelta(months=2)),
        ("10 months", relativedelta(months=10)),
        ("1 week", relativedelta(weeks=1)),
        ("2 weeks", relativedelta(weeks=2)),
        ("20 weeks", relativedelta(weeks=20)),
        ("1 day", relativedelta(days=1)),
        ("30 days", relativedelta(days=30)),
        ("60 days", relativedelta(days=60)),
    ],
)
def test_parse_lasts(value, expected_result):
    result = parse_lasts(value)
    assert result == expected_result


@pytest.mark.parametrize(
    "date_1,date_2,expected_result",
    [
        [parse_date("2022-05-30"), parse_date("2022-06-30"), [2022]],
        [parse_date("2022-05-30"), parse_date("2023-05-30"), [2022, 2023]],
        [parse_date("2022-05-30"), parse_date("2024-05-30"), [2022, 2023, 2024]],
    ],
)
def test_get_years_between_dates(date_1, date_2, expected_result):
    years = list(iter_years_between_dates(date_1, date_2))
    assert years == expected_result
