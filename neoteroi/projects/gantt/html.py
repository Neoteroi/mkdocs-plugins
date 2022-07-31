import logging
import sys
import xml.etree.ElementTree as etree
from dataclasses import dataclass
from datetime import date
from enum import Enum

from ..domain import Activity, Plan
from ..timeutil import (
    MONTHS,
    get_next_week_date,
    iter_weeks_of_year,
    iter_years_between_dates,
)

logger = logging.getLogger("MARKDOWN")


@dataclass
class GanttViewOptions:
    month_width: int = 150
    render_weeks: bool = True


class GanttScale(Enum):
    YEARS = "years"
    MONTHS = "months"
    WEEKS = "weeks"
    DAYS = "days"
    HOURS = "hours"


# ???
def get_best_scale(min_date: date, max_date: date) -> GanttScale:
    diff = max_date - min_date

    if diff.days >= 365:
        return GanttScale.YEARS

    if diff.days == 0:
        return GanttScale.HOURS

    if diff.days > 60:
        return GanttScale.WEEKS

    return GanttScale.YEARS


class GanttHTMLBuilder:
    def __init__(self, plan: Plan, options: GanttViewOptions) -> None:
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
        # self._scale_min_date = date(self._min_date.year, 1, 1)
        # self._scale_max_date = date(self._max_date.year, 12, 31)

        # se la scala sono mesi:
        self._scale_min_date = date(self._min_date.year, self._min_date.month, 1)
        self._scale_max_date = date(self._max_date.year, self._max_date.month, 31)

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
    def id(self) -> str:
        return f"nt-plan-{str(id(self.plan))}"

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
            self._build_quarters(periods_element)
            self._build_months(periods_element)
            self._build_weeks(periods_element)

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
        min_date = self._min_date
        max_date = self._max_date

        months_element = etree.SubElement(periods_element, "div", {"class": "months"})
        for year in range(min_date.year, max_date.year + 1):
            for i, name in MONTHS:
                month_element = etree.SubElement(
                    months_element, "div", {"class": f"month month-{i} month-{name}"}
                )
                month_element.text = f"{name} {year}"

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

        min_date = self._min_date
        max_date = self._max_date

        weeks_element = etree.SubElement(periods_element, "div", {"class": "weeks"})

        for year in range(min_date.year, max_date.year + 1):
            for i, week_date in iter_weeks_of_year(year):
                next_week_date = get_next_week_date(i, week_date)
                week_element = etree.SubElement(
                    weeks_element,
                    "span",
                    {
                        "class": f"week week-{i}",
                        "title": (
                            f"W{i}: {week_date.strftime('%Y-%m-%d')} "
                            "&rarr; "
                            f"{next_week_date.strftime('%Y-%m-%d')}"
                        ),
                    },
                )
                week_text_element = etree.SubElement(
                    week_element, "span", {"class": "week-text"}
                )
                week_text_element.text = f"W{i}"

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
        period_element = etree.SubElement(
            actions_element,
            "div",
            {
                "id": f"nt-plan-period-{id(item)}",
                "class": "period",
                "title": item.title,
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
        start_time = activity.start
        if start_time is None:
            return 0

        diff_seconds = (self._scale_min_date - start_time).total_seconds()
        return (
            self._pixels_width * float(diff_seconds) / float(self._scale_diff_seconds)
        )

    def _calc_period_width(self, activity: Activity) -> float:
        end_time = activity.end
        if end_time is None:
            return 0

        left_perc = self._calc_period_left(activity)
        diff_seconds = (self._scale_min_date - end_time).total_seconds()
        return (
            self._pixels_width * float(diff_seconds) / float(self._scale_diff_seconds)
        ) - left_perc
