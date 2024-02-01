import logging
import sys
import xml.etree.ElementTree as etree
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from enum import Enum
from typing import List, Union
from uuid import uuid4

from neoteroi.mkdocs.markdown.images import build_icon_html

from ..domain import Activity, Event, Plan
from ..timeutil import (
    date_delta,
    get_first_day_of_month,
    get_last_day_of_month,
    get_next_week_date,
    iter_days_between_dates,
    iter_months_between_dates,
    iter_months_between_dates_of_year,
    iter_quarters_between_dates,
    iter_weeks_between_dates,
    iter_years_between_dates,
)

logger = logging.getLogger("MARKDOWN")


class VerticalLinesPace(Enum):
    MONTHLY = "MONTHLY"
    WEEKLY = "WEEKLY"


@dataclass
class GanttViewOptions:
    id: str = ""
    month_width: float = 150
    month_format: str = "%B %Y"
    whole_years: bool = False
    no_groups: bool = False
    no_years: bool = False
    no_weeks: bool = False
    no_quarters: bool = False
    no_days: bool = False
    pastello: bool = False
    vlines_pace: VerticalLinesPace = VerticalLinesPace.MONTHLY

    def __post_init__(self):
        if isinstance(self.month_width, str):
            self.month_width = float(self.month_width)
        if isinstance(self.vlines_pace, str):
            self.vlines_pace = VerticalLinesPace(self.vlines_pace.upper())
        elif self.month_width >= 500:
            self.vlines_pace = VerticalLinesPace.WEEKLY

    @property
    def day_width(self) -> float:
        return self.month_width / 30


@dataclass
class VerticalLine:
    left: float


@dataclass
class BuildContext:
    vertical_lines: List[VerticalLine] = field(default_factory=list)
    styles: List[str] = field(default_factory=list)


class GanttHTMLBuilder:
    def __init__(self, plan: Plan, options: GanttViewOptions) -> None:
        self._id = uuid4()
        self._plan = plan
        self._options = options

        self._min_date = plan.get_overall_start() or date.today()
        self._max_date = plan.get_overall_end() or date.today().replace(
            year=self._min_date.year + 1
        )

        if options.whole_years:
            self._scale_min_date = date(self._min_date.year, 1, 1)
            self._scale_max_date = date(self._max_date.year, 12, 31)
        else:
            self._scale_min_date = get_first_day_of_month(self._min_date)
            self._scale_max_date = get_last_day_of_month(self._max_date)

        self._months_count = len(
            list(iter_months_between_dates(self._scale_min_date, self._scale_max_date))
        )

    @property
    def plan(self) -> Plan:
        return self._plan

    @property
    def options(self) -> GanttViewOptions:
        return self._options

    @property
    def client_width(self) -> int:
        return int(self.options.month_width * self._months_count)

    @property
    def id(self) -> str:
        if self.options.id:
            return self.options.id

        return f"nt-plan-{str(self._id)}"

    def _get_root_class(self) -> str:
        classes = ["nt-plan-root"]
        if self.options.no_groups:
            classes.append("no-groups")
        if self.options.pastello:
            classes.append("nt-pastello")

        return " ".join(classes)

    def build_html(self, parent):
        context = BuildContext()
        root_element = etree.SubElement(
            parent, "div", {"class": self._get_root_class(), "id": self.id}
        )

        plan_element = etree.SubElement(root_element, "div", {"class": "nt-plan"})
        inner_element = etree.SubElement(
            plan_element, "div", {"class": "nt-plan-inner"}
        )

        self._build_periods_html(inner_element, context)
        self._build_groups_html(inner_element, context)
        self._build_style(root_element, context)

    def _build_style(self, parent, context: BuildContext):
        if not context.styles:
            return
        style_element = etree.SubElement(parent, "style")
        style_element.text = "\n".join(context.styles)

    def _build_periods_html(self, parent, context: BuildContext):
        periods_element = etree.SubElement(parent, "div", {"class": "nt-plan-periods"})
        min_date = self._min_date
        max_date = self._max_date

        if min_date and max_date:
            self._build_years(periods_element)

            if not self.options.no_quarters:
                self._build_quarters(periods_element)
            self._build_months(periods_element, context)
            self._build_weeks(periods_element, context)

            if self.options.day_width > 20 and not self.options.no_days:
                self._build_days(periods_element)

    def _build_years(self, periods_element):
        if self.options.no_years:
            return

        min_date = self._scale_min_date
        max_date = self._scale_max_date

        years_element = etree.SubElement(periods_element, "div", {"class": "years"})
        for i, year in enumerate(iter_years_between_dates(min_date, max_date)):
            # it can happen that a year has just a few months visible on the scale!!
            # therefore it is necessary to know also the month, to generate a proper
            # scale
            attributes = {"class": f"year year-{i} year-{year}"}
            if min_date.year != max_date.year:
                year_width = sum(
                    self._get_month_width(month_date)
                    for month_date in iter_months_between_dates_of_year(
                        min_date, max_date, year
                    )
                    if self._scale_max_date >= month_date >= self._scale_min_date
                )
                attributes["style"] = f"width: {year_width}px;"
            year_element = etree.SubElement(years_element, "div", attributes)
            year_element.text = str(year)

    def _build_quarters(self, periods_element):
        min_date = self._scale_min_date
        max_date = self._scale_max_date
        quarters_element = etree.SubElement(
            periods_element, "div", {"class": "quarters"}
        )
        for quarter in iter_quarters_between_dates(min_date, max_date):
            i = quarter.number
            attributes = {
                "class": f"quarter quarter-{i}",
                "title": f"{quarter.year} Q{quarter.number}",
            }

            quarter_width = sum(
                self._get_month_width(month_date)
                for month_date in quarter.iter_dates()
                if self._scale_max_date >= month_date >= self._scale_min_date
            )
            attributes["style"] = f"width: {quarter_width}px;"

            quarter_element = etree.SubElement(quarters_element, "div", attributes)
            quarter_element.text = f"Q{i}"

    def _build_months(self, periods_element, context: BuildContext):
        min_date = self._scale_min_date
        max_date = self._scale_max_date

        total_width: float = 0
        months_element = etree.SubElement(periods_element, "div", {"class": "months"})

        for month_date in iter_months_between_dates(min_date, max_date):
            name = month_date.strftime("%B").lower()
            month_width = self._get_month_width(month_date)
            month_element = etree.SubElement(
                months_element,
                "div",
                {
                    "class": f"month month-{name}",
                    "style": f"width: {month_width}px;",
                },
            )
            month_element.text = month_date.strftime(self.options.month_format)

            # add vertical line
            if self.options.vlines_pace == VerticalLinesPace.MONTHLY:
                total_width += month_width
                context.vertical_lines.append(VerticalLine(round(total_width, 2)))

    def _get_month_width(self, month_date) -> float:
        last_day_of_month = get_last_day_of_month(month_date).day

        if last_day_of_month == 30:
            return self.options.month_width

        return round(self.options.day_width * last_day_of_month, 2)

    def _build_weeks(self, periods_element, context: BuildContext):
        if self.options.no_weeks:
            return

        if sys.version_info < (3, 8):  # pragma: no cover
            logger.warning(
                "[Gantt] To render weeks, Python 3.8 is the minimum supported version."
            )
            return

        min_date = self._scale_min_date
        max_date = self._scale_max_date

        total_width: float = 0
        weeks_element = etree.SubElement(periods_element, "div", {"class": "weeks"})

        for week_num, week_date in iter_weeks_between_dates(min_date, max_date):
            next_week_date = get_next_week_date(week_num, week_date)
            attributes = {
                "class": f"week week-{week_num}",
                "title": (
                    f"W{week_num}: {week_date.strftime('%Y-%m-%d')} "
                    "&rarr; "
                    f"{(next_week_date - timedelta(days=1)).strftime('%Y-%m-%d')}"
                ),
            }
            element_width: float = 0

            if week_date < self._scale_min_date:
                # the first week must take into account the number of days in the
                # first month of the scale
                element_width = round(
                    self.options.day_width * (next_week_date.day - 1), 2
                )
                attributes.update({"style": f"width: {element_width}px; flex: none;"})
            elif next_week_date > self._scale_max_date:
                # the last week must take into account the number of days in the
                # last month of the scale
                days_diff = (
                    self._scale_max_date
                    - date.fromisocalendar(week_date.year, week_num, 1)
                ).days
                element_width = round(self.options.day_width * (days_diff + 1), 2)
                attributes.update({"style": f"width: {element_width}px; flex: none;"})
            else:
                element_width = self.options.day_width * 7

            week_element = etree.SubElement(weeks_element, "span", attributes)
            week_text_element = etree.SubElement(
                week_element, "span", {"class": "week-text"}
            )
            week_text_element.text = f"W{week_num}"

            # add vertical line
            if self.options.vlines_pace == VerticalLinesPace.WEEKLY:
                total_width += element_width
                context.vertical_lines.append(VerticalLine(round(total_width, 2)))

    def _build_days(self, periods_element):
        min_date = self._scale_min_date
        max_date = self._scale_max_date

        days_element = etree.SubElement(periods_element, "div", {"class": "days"})

        for i, day_date in enumerate(iter_days_between_dates(min_date, max_date)):
            day_element = etree.SubElement(
                days_element,
                "span",
                {
                    "class": f"day day-{i}",
                    "title": day_date.strftime("%Y-%m-%d"),
                },
            )
            day_text_element = etree.SubElement(
                day_element, "span", {"class": "day-text"}
            )
            day_text_element.text = str(day_date.day)

    def _build_groups_html(self, parent, context: BuildContext):
        plan = self.plan
        if plan.activities is None:
            return

        for i, item in enumerate(plan.activities):
            group_element = etree.SubElement(
                parent, "div", {"class": f"nt-plan-group nt-group-{i}"}
            )
            summary_element = etree.SubElement(
                group_element, "div", {"class": "nt-plan-group-summary"}
            )
            p_element = etree.SubElement(summary_element, "p")
            p_element.text = item.title or f"Group {i}"

            activities_element = etree.SubElement(
                group_element, "div", {"class": "nt-plan-group-activities"}
            )

            for line in context.vertical_lines:
                etree.SubElement(
                    activities_element,
                    "i",
                    {"class": "nt-vline", "style": f"left: {line.left}px;"},
                )

            if item.events:
                # TODO: put in common function
                item_element = etree.SubElement(
                    activities_element, "div", {"class": "nt-plan-activity events"}
                )
                actions_element = etree.SubElement(
                    item_element, "div", {"class": "actions"}
                )
                for event in item.events:
                    self.build_event(actions_element, event)

            # for activity in item.iter_activities(False):
            for activity in item.activities or []:
                self._build_item_html(activities_element, activity)

    def _build_item_html(self, parent, item: Activity):
        item_element = etree.SubElement(parent, "div", {"class": "nt-plan-activity"})
        actions_element = etree.SubElement(item_element, "div", {"class": "actions"})

        for activity in item.iter_activities():
            # don't render parent activities: they would be overlapped by their children
            # anyway
            #  activity.activities or  ?? quando?
            if activity.hidden is True:
                continue
            self._build_period_html(actions_element, activity)

        if item.events:
            for event in item.events:
                self.build_event(actions_element, event)

    def _build_period_html(self, parent, item: Activity):
        title_date = (
            (
                f" {item.start.strftime('%Y-%m-%d')} "
                "&rarr; "
                f"{(item.end + timedelta(days=-1)).strftime('%Y-%m-%d')}"
            )
            if item.start and item.end
            else ""
        )
        period_element = etree.SubElement(
            parent,
            "div",
            {
                "class": "period",
                "title": f"{item.title}{title_date}",
                "style": (
                    f"left: {self._calc_period_left(item)}px; "
                    f"width: {self._calc_period_width(item)}px;"
                ),
            },
        )
        span_el = etree.SubElement(period_element, "span")
        span_el.text = item.title

    def _format_time(self, value: Union[None, date, datetime]):
        if value is None:
            return ""
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d, %H:%M:%S")
        return value.strftime("%Y-%m-%d")

    def build_event(self, parent, event: Event):
        dot_element = etree.SubElement(
            parent,
            "div",
            {
                "class": "nt-timeline-dot bigger",
                "title": f"{event.title} {self._format_time(event.time)}",
                "style": (
                    f"left: {self._calc_time_left(event.time) - 4}px;"
                    if event.time
                    else ""
                ),
            },
        )

        if event.icon:
            build_icon_html(dot_element, event.icon)

        if event.description:
            try:
                des = etree.fromstring(event.description)
            except etree.ParseError:
                des = etree.fromstring(f"<span>{event.description}</span>")

            des.set("class", f"description {des.get('class') or ''}")
            dot_element.append(des)

    def _calc_time_left(self, time: Union[date, datetime]) -> float:
        delta = (
            time
            - datetime(
                self._scale_min_date.year,
                self._scale_min_date.month,
                self._scale_min_date.day,
                0,
                0,
                0,
            )
            if isinstance(time, datetime)
            else time - self._scale_min_date
        )
        return round(delta.days * self.options.day_width, 2)

    def _calc_period_left(self, activity: Activity) -> float:
        start = activity.start or activity.get_overall_start()
        if start is None:
            return 0

        delta = date_delta(start, self._scale_min_date)
        pixels_width = delta.days * self.options.day_width
        return round(pixels_width, 2)

    def _calc_period_width(self, activity: Activity) -> float:
        start = activity.start or activity.get_overall_start()
        end = activity.end or activity.get_overall_end()
        if end is None or start is None:
            return 50

        delta = date_delta(end, start)
        pixels_width = delta.days * self.options.day_width
        return round(pixels_width, 2)
