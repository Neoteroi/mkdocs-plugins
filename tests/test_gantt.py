import markdown
import pytest

from neoteroi.mkdocs.projects import ProjectsExtension
from tests import equal_html, get_resource_file_contents

EXAMPLE_1 = get_resource_file_contents("gantt-01.html")
EXAMPLE_2 = get_resource_file_contents("gantt-02.html")


@pytest.mark.parametrize(
    "example,expected_result",
    [
        [
            """
::gantt:: id="test"

- title: Definition Phase
  activities:
  - title: Creative Brief
    start: 2022-03-03
    lasts: 1 day
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

::/gantt::
            """,
            EXAMPLE_1,
        ],
        [
            """
::gantt:: id="test"

- title: Milestones
  events:
    - title: Kick-off meeting
      time: 2022-03-03
      icon: ":octicons-rocket-16:"
    - title: Final delivery
      time: 2022-06-05
      icon: ":octicons-sun-16:"

- title: Definition Phase
  activities:
    - title: Graphic Design Research
      start: 2022-03-02
      lasts: 2 weeks
    - title: Brainstorming / Mood Boarding
      start: 2022-03-11
      lasts: 2 weeks

- title: Creation Phase
  activities:
    - title: Sketching
      start: 2022-03-21
      lasts: 2 weeks
    - title: Design Building
      start: 2022-04-02
      lasts: 4 weeks
    - title: Refining
      start: 2022-05-01
      lasts: 2 weeks

- title: Feedback Phase
  activities:
    - title: Presenting
      start: 2022-05-01
      lasts: 3 days
    - title: Revisions
      start: 2022-05-02
      end: 2022-05-31

::/gantt::
            """,
            EXAMPLE_2,
        ],
    ],
)
def test_gantt_extension(example, expected_result):
    html = markdown.markdown(example, extensions=[ProjectsExtension(priority=100)])
    assert equal_html(html, expected_result)
