from dataclasses import dataclass
from datetime import date, datetime
from typing import Iterable, List, Optional, Union

from dateutil.parser import parse as parse_date

from neoteroi.projects.timeutil import parse_lasts


@dataclass(frozen=True)
class Event:
    title: str
    description: Optional[str] = None
    time: Optional[datetime] = None
    icon: Optional[str] = None

    @classmethod
    def from_obj(cls, obj):
        return cls(
            obj.get("title") or "",
            obj.get("description") or "",
            _parse_optional_datetime(obj.get("time")),
            icon=obj.get("icon"),
        )


def _parse_optional_datetime(value: Union[None, datetime, str]) -> Optional[datetime]:
    if isinstance(value, date):
        # YAML parses dates automatically
        return value

    if value:
        return parse_date(value)
    return None


def _parse_optional_date(value: Union[None, date, str]) -> Optional[date]:
    if isinstance(value, date):
        # YAML parses dates automatically
        return value

    if value:
        return parse_date(value)
    return None


@dataclass(frozen=True)
class Activity:
    title: str
    start: Optional[date] = None
    end: Optional[date] = None
    description: Optional[str] = None
    activities: Optional[List["Activity"]] = None
    events: Optional[List[Event]] = None

    def iter_activities(self, include_self: bool = True) -> Iterable["Activity"]:
        """
        Yields self and all descendant activities.
        """
        if include_self:
            yield self

        if self.activities:
            for activity in self.activities:
                yield from activity.iter_activities()

    def get_overall_start(self) -> Optional[date]:
        """
        Returns the start date of this activity, including all sub and descendants
        activities.
        """
        # TODO: is this practical? Maybe it is better to have ActivityGroup?
        if self.activities:
            return min(
                [
                    start
                    for start in (
                        activity.get_overall_start() for activity in self.activities
                    )
                    if start is not None
                ]
            )
        return self.start

    def get_overall_end(self) -> Optional[date]:
        """
        Returns the end date of this activity, including all sub and descendants
        activities.
        """
        if self.activities:
            return max(
                [
                    end
                    for end in (
                        activity.get_overall_end() for activity in self.activities
                    )
                    if end is not None
                ]
            )
        return self.end

    @classmethod
    def from_obj(cls, obj):
        if isinstance(obj, str):
            return cls(title=obj)
        if not isinstance(obj, dict):
            raise TypeError("Expected a str or a dict.")

        title = obj.get("title", "")
        description = obj.get("description")
        start = _parse_optional_date(obj.get("start"))
        end = _parse_optional_date(obj.get("end"))
        lasts = obj.get("lasts")
        child_activities = obj.get("activities")
        events = obj.get("events")
        if lasts:
            if start is None:
                start = date.today()
            end = start + parse_lasts(lasts)

        return cls(
            title,
            start,
            end,
            description=description,
            activities=[Activity.from_obj(item) for item in child_activities]
            if child_activities
            else None,
            events=[Event.from_obj(item) for item in events] if events else None,
        )


@dataclass(frozen=True)
class Plan(Activity):
    events: Optional[List[Event]] = None

    def iter_activities(self) -> Iterable["Activity"]:
        """
        Yields all descendant activities.
        """

        if self.activities:
            for activity in self.activities:
                yield from activity.iter_activities()

    @classmethod
    def from_obj(cls, obj):
        if isinstance(obj, list):
            return cls(
                title="Plan", activities=[Activity.from_obj(item) for item in obj]
            )

        if not isinstance(obj, dict):
            raise TypeError("Expected a list or a dict.")

        activities = obj.get("activities")
        events = obj.get("events")

        return cls(
            title=obj.get("title") or "Plan",
            activities=[Activity.from_obj(item) for item in activities]
            if activities
            else [],
            events=[Event.from_obj(item) for item in events] if events else [],
        )
