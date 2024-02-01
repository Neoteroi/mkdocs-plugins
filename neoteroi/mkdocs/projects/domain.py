from dataclasses import dataclass
from datetime import date, datetime
from typing import Iterable, List, Optional, Union

from dateutil.parser import parse as parse_date

from neoteroi.mkdocs.projects.timeutil import parse_lasts


@dataclass(frozen=True)
class Event:
    title: str
    description: Optional[str] = None
    time: Optional[datetime] = None
    icon: Optional[str] = None

    def __post_init__(self):
        # Note: datetimes are currently not supported, only the date component is kept
        if isinstance(self.time, datetime):
            object.__setattr__(self, "time", self.time.date())

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


def _resolve_activities(
    activities, preceding_date: Optional[date] = None
) -> Iterable["Activity"]:
    """
    Iterates through a list of objects representing activities and yields
    activities, handling automatic start date when the preceding activity specifies one.
    """
    for item in activities:
        activity = Activity.from_obj(item, preceding_date)
        preceding_date = activity.end or activity.start
        yield activity


@dataclass(frozen=True)
class Activity:
    title: str
    start: Optional[date] = None
    end: Optional[date] = None
    description: Optional[str] = None
    activities: Optional[List["Activity"]] = None
    events: Optional[List[Event]] = None
    hidden: Optional[bool] = None

    def __post_init__(self):
        # Note: datetimes are currently not supported, only the date component is kept
        if isinstance(self.start, datetime):
            object.__setattr__(self, "start", self.start.date())
        if isinstance(self.end, datetime):
            object.__setattr__(self, "end", self.end.date())

    def iter_activities(self, include_self: bool = True) -> Iterable["Activity"]:
        """
        Yields self and all descendant activities.
        """
        if include_self:
            yield self

        if self.activities:
            for activity in self.activities:
                yield from activity.iter_activities()

    def iter_events(self, include_self: bool = True) -> Iterable[Event]:
        """
        Yields all events in the activity and descendants.
        """
        for activity in self.iter_activities(include_self):
            if activity.events:
                yield from activity.events

    def iter_dates(self) -> Iterable[date]:
        if self.events:
            for event in self.events:
                if event.time:
                    yield event.time
        if self.activities:
            for activity in self.activities:
                if activity.start:
                    yield activity.start
                if activity.end:
                    yield activity.end

    def _get_event_date(self, fn) -> Optional[date]:
        if self.events:
            dates = [event.time for event in self.events if event.time is not None]
            return fn(dates) if dates else None
        return None

    def get_first_event_date(self) -> Optional[date]:
        return self._get_event_date(min)

    def get_last_event_date(self) -> Optional[date]:
        return self._get_event_date(max)

    def get_overall_start(self) -> Optional[date]:
        """
        Returns the start date of this activity, including all sub and descendants
        activities.
        """
        all_starts = [
            activity.start
            for activity in self.iter_activities()
            if activity.start is not None
        ] + [event.time for event in self.iter_events() if event.time is not None]
        return min(all_starts)

    def get_overall_end(self) -> Optional[date]:
        """
        Returns the end date of this activity, including all sub and descendants
        activities.
        """
        all_ends = [
            activity.end
            for activity in self.iter_activities()
            if activity.end is not None
        ] + [event.time for event in self.iter_events() if event.time is not None]
        return max(all_ends)

    @classmethod
    def from_obj(cls, obj, preceding_date: Optional[date] = None):
        if isinstance(obj, str):
            return cls(title=obj)
        if not isinstance(obj, dict):
            raise TypeError("Expected a str or a dict.")

        title = obj.get("title", "")
        description = obj.get("description")
        start = _parse_optional_date(obj.get("start", preceding_date))
        end = _parse_optional_date(obj.get("end"))
        skip = obj.get("skip")
        if skip:
            lasts = skip
            hidden = True
        else:
            lasts = obj.get("lasts")
            hidden = obj.get("hidden")
        child_activities = obj.get("activities") or []
        events = obj.get("events")
        if lasts:
            if start is None:
                start = date.today() if preceding_date is None else preceding_date
            end = start + parse_lasts(lasts)
        if preceding_date is None:
            preceding_date = end or start

        if child_activities and end is None:
            # avoid displaying a parent activity that would last anyway from the
            # beginning to the end of the last descendant
            hidden = True

        return cls(
            title,
            start,
            end,
            description=description,
            activities=(
                list(_resolve_activities(child_activities, end or start))
                if child_activities
                else None
            ),
            events=[Event.from_obj(item) for item in events] if events else None,
            hidden=hidden,
        )


@dataclass(frozen=True)
class Plan(Activity):
    def iter_activities(self, include_self: bool = False) -> Iterable["Activity"]:
        yield from super().iter_activities(include_self)

    @classmethod
    def from_obj(cls, obj):
        if isinstance(obj, list):
            return cls(
                title="Plan",
                activities=[Activity.from_obj(item) for item in obj],
            )

        if not isinstance(obj, dict):
            raise TypeError("Expected a list or a dict.")

        plan_start = _parse_optional_date(obj.get("start"))
        activities = obj.get("activities") or []
        events = obj.get("events")

        return cls(
            title=obj.get("title") or "Plan",
            activities=(
                [Activity.from_obj(item, plan_start) for item in activities]
                if activities
                else []
            ),
            events=[Event.from_obj(item) for item in events] if events else [],
        )
