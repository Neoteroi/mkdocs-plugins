from datetime import date, datetime

import pytest
import yaml
from dateutil.parser import parse as parse_date

from neoteroi.mkdocs.projects.domain import Activity, Plan

EXAMPLE_1 = """
- title: Definition Phase
  activities:
  - title: Creative Brief
    start: 2022-03-01
    end: 2022-03-02
  - title: Graphic Design Research
    start: 2022-03-02
    end: 2022-03-10
    lasts: 2 weeks
  - title: Brainstorming / Mood Boarding
    start: 2022-03-11
    end: 2022-03-20

- title: Creation Phase
  activities:
  - title: Sketching
    start: 2022-03-21
    end: 2022-04-01
  - title: Design Building
    start: 2022-04-02
    end: 2022-04-20
  - title: Refining
    start: 2022-04-21
    end: 2022-04-30

- title: Feedback Phase
  activities:
  - title: Presenting
    start: 2022-04-22
    end: 2022-05-01
  - title: Revisions
    start: 2022-05-02
    end: 2022-05-10

- title: Delivery Phase
  activities:
  - title: Final delivery
    start: 2022-05-11
    end: 2022-05-12
"""


@pytest.mark.parametrize(
    "value,expected_result",
    [
        ("Creative brief", Activity("Creative brief")),
        ({"title": "Creative brief"}, Activity("Creative brief")),
        (
            {"title": "Creative brief", "start": "2022-07-30", "lasts": "1 day"},
            Activity(
                "Creative brief", start=datetime(2022, 7, 30), end=datetime(2022, 7, 31)
            ),
        ),
        (
            {"title": "Creative brief", "start": "2022-07-30", "lasts": "1 month"},
            Activity(
                "Creative brief", start=datetime(2022, 7, 30), end=datetime(2022, 8, 30)
            ),
        ),
    ],
)
def test_activity_from_obj(value, expected_result):
    activity = Activity.from_obj(value)
    assert activity == expected_result


def test_plan_from_object():
    obj = yaml.safe_load(EXAMPLE_1)
    plan = Plan.from_obj(obj)

    assert plan.activities is not None
    assert len(plan.activities) == 4
    assert plan.get_overall_start() == parse_date("2022-03-01").date()
    assert plan.get_overall_end() == parse_date("2022-05-12").date()

    all_activities = list(plan.iter_activities())

    assert all_activities == [
        Activity(
            title="Definition Phase",
            start=None,
            end=None,
            description=None,
            activities=[
                Activity(
                    title="Creative Brief",
                    start=date(2022, 3, 1),
                    end=date(2022, 3, 2),
                    description=None,
                    activities=None,
                    events=None,
                    hidden=None,
                ),
                Activity(
                    title="Graphic Design Research",
                    start=date(2022, 3, 2),
                    end=date(2022, 3, 16),
                    description=None,
                    activities=None,
                    events=None,
                    hidden=None,
                ),
                Activity(
                    title="Brainstorming / Mood Boarding",
                    start=date(2022, 3, 11),
                    end=date(2022, 3, 20),
                    description=None,
                    activities=None,
                    events=None,
                    hidden=None,
                ),
            ],
            events=None,
            hidden=True,
        ),
        Activity(
            title="Creative Brief",
            start=date(2022, 3, 1),
            end=date(2022, 3, 2),
            description=None,
            activities=None,
            events=None,
            hidden=None,
        ),
        Activity(
            title="Graphic Design Research",
            start=date(2022, 3, 2),
            end=date(2022, 3, 16),
            description=None,
            activities=None,
            events=None,
            hidden=None,
        ),
        Activity(
            title="Brainstorming / Mood Boarding",
            start=date(2022, 3, 11),
            end=date(2022, 3, 20),
            description=None,
            activities=None,
            events=None,
            hidden=None,
        ),
        Activity(
            title="Creation Phase",
            start=None,
            end=None,
            description=None,
            activities=[
                Activity(
                    title="Sketching",
                    start=date(2022, 3, 21),
                    end=date(2022, 4, 1),
                    description=None,
                    activities=None,
                    events=None,
                    hidden=None,
                ),
                Activity(
                    title="Design Building",
                    start=date(2022, 4, 2),
                    end=date(2022, 4, 20),
                    description=None,
                    activities=None,
                    events=None,
                    hidden=None,
                ),
                Activity(
                    title="Refining",
                    start=date(2022, 4, 21),
                    end=date(2022, 4, 30),
                    description=None,
                    activities=None,
                    events=None,
                    hidden=None,
                ),
            ],
            events=None,
            hidden=True,
        ),
        Activity(
            title="Sketching",
            start=date(2022, 3, 21),
            end=date(2022, 4, 1),
            description=None,
            activities=None,
            events=None,
            hidden=None,
        ),
        Activity(
            title="Design Building",
            start=date(2022, 4, 2),
            end=date(2022, 4, 20),
            description=None,
            activities=None,
            events=None,
            hidden=None,
        ),
        Activity(
            title="Refining",
            start=date(2022, 4, 21),
            end=date(2022, 4, 30),
            description=None,
            activities=None,
            events=None,
            hidden=None,
        ),
        Activity(
            title="Feedback Phase",
            start=None,
            end=None,
            description=None,
            activities=[
                Activity(
                    title="Presenting",
                    start=date(2022, 4, 22),
                    end=date(2022, 5, 1),
                    description=None,
                    activities=None,
                    events=None,
                    hidden=None,
                ),
                Activity(
                    title="Revisions",
                    start=date(2022, 5, 2),
                    end=date(2022, 5, 10),
                    description=None,
                    activities=None,
                    events=None,
                    hidden=None,
                ),
            ],
            events=None,
            hidden=True,
        ),
        Activity(
            title="Presenting",
            start=date(2022, 4, 22),
            end=date(2022, 5, 1),
            description=None,
            activities=None,
            events=None,
            hidden=None,
        ),
        Activity(
            title="Revisions",
            start=date(2022, 5, 2),
            end=date(2022, 5, 10),
            description=None,
            activities=None,
            events=None,
            hidden=None,
        ),
        Activity(
            title="Delivery Phase",
            start=None,
            end=None,
            description=None,
            activities=[
                Activity(
                    title="Final delivery",
                    start=date(2022, 5, 11),
                    end=date(2022, 5, 12),
                    description=None,
                    activities=None,
                    events=None,
                    hidden=None,
                )
            ],
            events=None,
            hidden=True,
        ),
        Activity(
            title="Final delivery",
            start=date(2022, 5, 11),
            end=date(2022, 5, 12),
            description=None,
            activities=None,
            events=None,
            hidden=None,
        ),
    ]


def test_activities_auto_start_1():
    configuration = """
- title: Beginning
  start: 2022-01-01
  activities:
  - title: Activity 1
    lasts: 1 day
  - title: Activity 2
    lasts: 1 week
  - title: Activity 3
    lasts: 2 days
    """
    obj = yaml.safe_load(configuration)
    plan = Plan.from_obj(obj)

    assert plan.activities is not None
    assert len(plan.activities) == 1
    assert plan.get_overall_start() == date(2022, 1, 1)
    assert plan.get_overall_end() == date(2022, 1, 11)


def test_activities_auto_start_2():
    configuration = """
- title: Beginning
  start: 2022-01-01
  activities:
  - title: Activity 1
    lasts: 1 day
    activities:
    - title: Activity 1.1
      lasts: 3 days
  - title: Activity 2
    lasts: 1 week
  - title: Activity 3
    lasts: 2 days
    """
    obj = yaml.safe_load(configuration)
    plan = Plan.from_obj(obj)

    assert plan.activities is not None
    assert len(plan.activities) == 1
    assert plan.get_overall_start() == date(2022, 1, 1)
    assert plan.get_overall_end() == date(2022, 1, 11)
