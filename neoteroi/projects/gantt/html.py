import logging
import sys
from typing import Union
import xml.etree.ElementTree as etree
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from uuid import uuid4

from neoteroi.markdown.images import build_icon_html

from ..domain import Activity, Event, Plan
from ..timeutil import (
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


@dataclass
class GanttViewOptions:
    month_width: float = 150
    render_weeks: bool = True
    render_days: bool = True
    whole_years: bool = False
    no_groups: bool = False
    no_quarters: bool = False

    def __post_init__(self):
        if isinstance(self.month_width, str):
            self.month_width = float(self.month_width)

    @property
    def day_width(self) -> float:
        return self.month_width / 30


"""
TODO:
1. quarters ✅
1.1. larghezza anni esatta ✅
2. animazioni ?
3. eventi
4. periodi in attività
5. esempio con Milestones e eventi
"""


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
        return f"nt-plan-{str(self._id)}"

    def _get_root_class(self) -> str:
        classes = ["nt-plan-root"]
        if self.options.no_groups:
            classes.append("no-groups")

        return " ".join(classes)

    def build_html(self, parent):
        root_element = etree.SubElement(
            parent, "div", {"class": self._get_root_class(), "id": self.id}
        )

        plan_element = etree.SubElement(root_element, "div", {"class": "nt-plan"})
        inner_element = etree.SubElement(
            plan_element, "div", {"class": "nt-plan-inner"}
        )

        self.build_style(root_element)
        self.build_periods_html(inner_element)
        self.build_groups_html(inner_element)

    def build_style(self, parent):
        pass
        # years_count = len(self._years)
        # style_element = etree.SubElement(parent, "style")

        # if years_count > 1:
        #     rows = [f"#{self.id} .year {{ width: calc(100% / {years_count}); }}"]
        # else:
        #     rows = [f"#{self.id} .year {{ width: 100%; }}"]

        # rows.append(f"#{self.id} .month {{ width: {self.options.month_width}px; }}")

        # Configure activity width and left position

        # style_element.text = "\n".join(rows)

    def build_periods_html(self, parent):
        periods_element = etree.SubElement(parent, "div", {"class": "nt-plan-periods"})
        min_date = self._min_date
        max_date = self._max_date

        if min_date and max_date:
            self._build_years(periods_element)

            if not self.options.no_quarters:
                self._build_quarters(periods_element)
            self._build_months(periods_element)
            self._build_weeks(periods_element)

            if self.options.day_width > 30:
                self._build_days(periods_element)

    def _build_years(self, periods_element):
        """
        <div class="years">
            <div class="year year-1">2022</div>
            <div class="year year-2">2023</div>
        </div>
        """
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
        """
        <div class="quarters">
            <span class="quarter quarter-1">Q1</span>
            <span class="quarter quarter-2">Q2</span>
            <span class="quarter quarter-3">Q3</span>
            <span class="quarter quarter-4">Q4</span>
            <span class="quarter quarter-1">Q1</span>
            <span class="quarter quarter-2">Q2</span>
            <span class="quarter quarter-3">Q3</span>
            <span class="quarter quarter-4">Q4</span>
        </div>
        """
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

    def _build_months(self, periods_element):
        """
        <div class="months">
            <span class="month month-1 january">January 2022</span>
            <span class="month month-2 february">February 2022</span>
            <span class="month month-3 march">March 2022</span>
            ...
        """
        min_date = self._scale_min_date
        max_date = self._scale_max_date

        months_element = etree.SubElement(periods_element, "div", {"class": "months"})

        for month_date in iter_months_between_dates(min_date, max_date):
            name = month_date.strftime("%B").lower()
            month_element = etree.SubElement(
                months_element,
                "div",
                {
                    "class": f"month month-{name}",
                    "style": f"width: {self._get_month_width(month_date)}px;",
                },
            )
            month_element.text = month_date.strftime("%B %Y")

    def _get_month_width(self, month_date) -> float:
        last_day_of_month = get_last_day_of_month(month_date).day

        if last_day_of_month == 30:
            return self.options.month_width

        return self.options.day_width * last_day_of_month

    def _build_weeks(self, periods_element):
        """
        <div class="weeks">
            <span class="week week-1" title="W1: 2022-01-03 &rarr; 2022-01-09">
                <span class="week-text">W1</span>
            </span>
            <span class="week week-2" title="W2: 2022-01-10 &rarr; 2022-01-16">
                <span class="week-text">W2</span>
            </span>
            ...
        """
        if not self.options.render_weeks:
            return

        if sys.version_info < (3, 8):  # pragma: no cover
            logger.warning(
                "[Gantt] to render weeks, Python 3.8 is the minimum supported required."
            )
            return

        min_date = self._scale_min_date
        max_date = self._scale_max_date

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
            if week_date < self._scale_min_date:
                # the first week must take into account the number of days in the
                # first month of the scale
                element_width = self.options.day_width * (next_week_date.day - 1)
                attributes.update({"style": f"width: {element_width}px; flex: none;"})
            elif next_week_date > self._scale_max_date:
                # the last week must take into account the number of days in the
                # last month of the scale
                days_diff = (
                    self._scale_max_date
                    - date.fromisocalendar(week_date.year, week_num, 1)
                ).days
                element_width = self.options.day_width * (days_diff + 1)
                attributes.update({"style": f"width: {element_width}px; flex: none;"})

            week_element = etree.SubElement(weeks_element, "span", attributes)
            week_text_element = etree.SubElement(
                week_element, "span", {"class": "week-text"}
            )
            week_text_element.text = f"W{week_num}"

    def _build_days(self, periods_element):
        if not self.options.render_days:
            return

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

    def build_groups_html(self, parent):
        plan = self.plan
        if plan.activities is None:
            return

        for i, item in enumerate(plan.activities):
            group_element = etree.SubElement(
                parent, "div", {"class": f"nt-plan-group group-{i}"}
            )
            summary_element = etree.SubElement(
                group_element, "div", {"class": "nt-plan-group-summary"}
            )
            p_element = etree.SubElement(summary_element, "p")
            p_element.text = item.title or f"Group {i}"

            activities_element = etree.SubElement(
                group_element, "div", {"class": "nt-plan-group-activities"}
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

            for activity in item.iter_activities(False):
                self.build_item_html(activities_element, activity)

    def build_item_html(self, parent, item: Activity):
        """
        <div class="nt-plan-group group-0">
            <div class="nt-plan-group-summary">
                <p>Lorem ipsum dolor shit amet.</p>
            </div>
            <div class="nt-plan-group-activities">
                <div class="nt-plan-activity">
                    <div>Act. 1</div>
                    <div class="ug-timeline-dot blue bigger" title="Some event"><i
                            class="fa-solid fa-archway icon"></i></div>
                    <div class="actions">
                        <div class="period period-0" title="Some activity">
                            <div class="nt-tooltip">
                                <span>Some activity</span>
                                <ul>
                                    <li>Start date: ...</li>
                                    <li>End date: ...</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="nt-plan-activity">
                    <div>Act. 1</div>
                    <div class="actions">
                        <div class="period period-1">
                        </div>
                    </div>
                </div>
                <div class="nt-plan-activity">
                    <div>Act. 2</div>
                    <div class="actions">
                        <div class="period period-2"></div>
                    </div>
                </div>
                <div class="nt-plan-activity">
                    <div>Act. 3</div>
                    <div class="actions">
                        <div class="period period-3"></div>
                    </div>
                </div>
            </div>
        </div>
        """
        item_element = etree.SubElement(parent, "div", {"class": "nt-plan-activity"})
        actions_element = etree.SubElement(item_element, "div", {"class": "actions"})

        """
        <div class="period period-0" title="Some activity">
            <div class="nt-tooltip">
                <span>Some activity</span>
                <ul>
                    <li>Start date: ...</li>
                    <li>End date: ...</li>
                </ul>
            </div>
        </div>
        """
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
            actions_element,
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

        if item.events:
            for event in item.events:
                self.build_event(actions_element, event)
        # TODO: apply style left and width depending on the size of month!? (supporto
        # per animazioni!)

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
                "style": f"left: {self._calc_time_left(event.time)-4}px;"
                if event.time
                else "",
            },
        )

        if event.icon:
            build_icon_html(dot_element, event.icon)

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
        return delta.days * self.options.day_width

    def _calc_period_left(self, activity: Activity) -> float:
        start = activity.start or activity.get_overall_start()
        if start is None:
            return 0

        delta = start - self._scale_min_date
        pixels_width = delta.days * self.options.day_width
        return pixels_width

    def _calc_period_width(self, activity: Activity) -> float:
        start = activity.start or activity.get_overall_start()
        end = activity.end or activity.get_overall_end()
        if end is None or start is None:
            return 50

        delta = end - start
        pixels_width = delta.days * self.options.day_width
        return pixels_width
