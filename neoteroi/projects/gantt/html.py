import logging
import sys
import xml.etree.ElementTree as etree
from dataclasses import dataclass
from datetime import date, timedelta
from uuid import uuid4

from ..domain import Activity, Plan
from ..timeutil import (
    get_first_day_of_month,
    get_last_day_of_month,
    get_next_week_date,
    iter_days_between_dates,
    iter_months_between_dates,
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

    def __post_init__(self):
        if isinstance(self.month_width, str):
            self.month_width = float(self.month_width)

    @property
    def day_width(self) -> float:
        return self.month_width / 30


"""
TODO:
1. quarters
2. animazioni
3. eventi
4. periodi in attività
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
        self._years = (
            list(iter_years_between_dates(self._min_date, self._max_date))
            if self._min_date is not None and self._max_date is not None
            else []
        )

        # se la scala sono anni:
        if options.whole_years:
            self._scale_min_date = date(self._min_date.year, 1, 1)
            self._scale_max_date = date(self._max_date.year, 12, 31)
        else:
            # se la scala sono mesi:
            self._scale_min_date = get_first_day_of_month(self._min_date)
            self._scale_max_date = get_last_day_of_month(self._max_date)

        self._months_count = len(
            list(iter_months_between_dates(self._scale_min_date, self._scale_max_date))
        )
        self._scale_diff_seconds = (
            self._scale_min_date - self._scale_max_date
        ).total_seconds()
        self._pixels_width = self.options.month_width * len(self._years) * 12

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

    def build_html(self, parent):
        root_element = etree.SubElement(
            parent, "div", {"class": "nt-plan-root", "id": self.id}
        )

        plan_element = etree.SubElement(root_element, "div", {"class": "nt-plan"})
        inner_element = etree.SubElement(
            plan_element, "div", {"class": "nt-plan-inner"}
        )

        self.build_style(root_element)
        self.build_periods_html(inner_element)
        self.build_groups_html(inner_element)

    def build_style(self, parent):
        years_count = len(self._years)
        style_element = etree.SubElement(parent, "style")

        if years_count > 1:
            rows = [f"#{self.id} .year {{ width: calc(100% / {years_count}); }}"]
        else:
            rows = [f"#{self.id} .year {{ width: 100%; }}"]

        rows.append(f"#{self.id} .quarter {{ width: calc(100% / {years_count * 2}); }}")
        rows.append(f"#{self.id} .month {{ width: {self.options.month_width}px; }}")

        # Configure activity width and left position

        style_element.text = "\n".join(rows)

    def build_periods_html(self, parent):
        periods_element = etree.SubElement(parent, "div", {"class": "nt-plan-periods"})
        min_date = self._min_date
        max_date = self._max_date

        if min_date and max_date:
            self._build_years(periods_element)
            # self._build_quarters(periods_element)
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
        years_element = etree.SubElement(periods_element, "div", {"class": "years"})
        for i, year in enumerate(self._years):
            year_element = etree.SubElement(
                years_element, "div", {"class": f"year year-{i} year-{year}"}
            )
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
        min_date = self._min_date
        max_date = self._max_date
        quarters_element = etree.SubElement(
            periods_element, "div", {"class": "quarters"}
        )
        for _ in range(min_date.year, max_date.year + 1):
            for i in [1, 2, 3, 4]:
                quarter_element = etree.SubElement(
                    quarters_element, "div", {"class": f"quarter quarter-{i}"}
                )
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
                attributes.update(
                    {"style": f"width: {element_width}px; flex: initial;"}
                )
            elif next_week_date > self._scale_max_date:
                # the last week must take into account the number of days in the
                # last month of the scale
                days_diff = (
                    self._scale_max_date
                    - date.fromisocalendar(week_date.year, week_num, 1)
                ).days
                element_width = self.options.day_width * (days_diff + 1)
                attributes.update(
                    {"style": f"width: {element_width}px; flex: initial;"}
                )
            # else:
            #     element_width = self.options.day_width * 7
            #     attributes.update(
            #         {"style": f"width: {element_width}px; flex: initial;"}
            #     )

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
        # TODO: more periods in one line?
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
                # "id": f"nt-plan-period-{id(item)}",
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
        # TODO: apply style left and width depending on the size of month!

    def _calc_period_left(self, activity: Activity) -> float:
        if activity.start is None:
            return 0

        delta = activity.start - self._scale_min_date
        pixels_width = delta.days * self.options.day_width
        return pixels_width

    def _calc_period_width(self, activity: Activity) -> float:
        if activity.end is None or activity.start is None:
            return 50

        delta = activity.end - activity.start
        pixels_width = delta.days * self.options.day_width
        return pixels_width
