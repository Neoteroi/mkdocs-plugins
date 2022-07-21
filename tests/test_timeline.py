import markdown
import pytest

from neoteroi.timeline import TimelineExtension


@pytest.mark.parametrize(
    "example,expected_result",
    [
        #         [
        #             """
        #             [timeline(...)]
        #             """,
        #             """
        #     """,
        #         ],
        [
            """
            ::timeline::
            [
                {
                    "title": "Zero",
                    "content": "Better late than never! Lorem ipsum dolor sit amet.",
                    "icon": "fa-solid fa-archway",
                    "dot_class": "blue",
                    "sub_title": "2022-Q1"
                },
                {
                    "title": "One",
                    "content": "Lorem ipsum dolor sit amet, consectetur adipiscing.",
                    "icon": "fa-solid fa-star",
                    "dot_class": "cyan",
                    "sub_title": "2022-Q2"
                }
            ]
            ::/timeline::


            This is --strike one--.

            [timeline(https://example.me/timeline.json)]

            [timeline(timeline.json)]

            """,
            """
    """,
        ],
    ],
)
def test_timeline_extension(example, expected_result):
    html = markdown.markdown(example, extensions=[TimelineExtension()])
    assert html is not None
    # assert html == expected_result.strip()


@pytest.mark.parametrize(
    "example,expected_result",
    [
        #         [
        #             """
        #             [timeline(...)]
        #             """,
        #             """
        #     """,
        #         ],
        [
            """
            ::timeline:: csv

            title,sub_title,content,icon,key
            Zero,2022-Q1,Better late than never! Lorem ipsum dolor sit amet.,fa-solid fa-archway,blue
            One,2022-Q2,"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin felis eros, facilisis sed feugiat a, efficitur ut neque. In vel nulla et nulla aliquet porta ac at est.",fa-solid fa-star,cyan
            Two,2022-Q3,Lorem ipsum dolor sit amet.,fa-solid fa-meteor,
            Three,2022-Q4,Lorem ipsum dolor sit amet.,,pink
            Four,2023-Q1,Lorem ipsum dolor sit amet.,fa-solid fa-fire,cyan

            ::/timeline::
            """,
            """
<div class="ug-timeline vertical left">
<div class="ug-timeline-before"></div>
<div class="ug-timeline-items">
<div class="ug-timeline-item blue">
<h3 class="ug-timeline-title">Zero</h3>
<span class="ug-timeline-sub-title">2022-Q1</span><p class="ug-timeline-content">Better late than never! Lorem ipsum dolor sit amet.</p>
<div class="ug-timeline-dot blue bigger"><i class="fa-solid fa-archway icon"></i></div>
</div>
<div class="ug-timeline-item cyan">
<h3 class="ug-timeline-title">One</h3>
<span class="ug-timeline-sub-title">2022-Q2</span><p class="ug-timeline-content">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin felis eros, facilisis sed feugiat a, efficitur ut neque. In vel nulla et nulla aliquet porta ac at est.</p>
<div class="ug-timeline-dot cyan bigger"><i class="fa-solid fa-star icon"></i></div>
</div>
<div class="ug-timeline-item">
<h3 class="ug-timeline-title">Two</h3>
<span class="ug-timeline-sub-title">2022-Q3</span><p class="ug-timeline-content">Lorem ipsum dolor sit amet.</p>
<div class="ug-timeline-dot  bigger"><i class="fa-solid fa-meteor icon"></i></div>
</div>
<div class="ug-timeline-item pink">
<h3 class="ug-timeline-title">Three</h3>
<span class="ug-timeline-sub-title">2022-Q4</span><p class="ug-timeline-content">Lorem ipsum dolor sit amet.</p>
<div class="ug-timeline-dot pink"></div>
</div>
<div class="ug-timeline-item cyan">
<h3 class="ug-timeline-title">Four</h3>
<span class="ug-timeline-sub-title">2023-Q1</span><p class="ug-timeline-content">Lorem ipsum dolor sit amet.</p>
<div class="ug-timeline-dot cyan bigger"><i class="fa-solid fa-fire icon"></i></div>
</div>
</div>
<div class="ug-timeline-after"></div>
</div>
""",
        ],
    ],
)
def test_timeline_extension_csv_format(example, expected_result):
    html = markdown.markdown(example, extensions=[TimelineExtension()])

    assert html is not None
    assert html.strip() == expected_result.strip()


def test_timeline_extension_mix():
    example = """

::timeline::

- title: Zero
  sub_title: 2022-Q1
  content:
    Better late than never! Lorem ipsum dolor sit amet.
  icon: fa-solid fa-archway
  key: blue
- title: One
  content:
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin felis eros,
    facilisis sed feugiat a, efficitur ut neque. In vel nulla et nulla aliquet porta
    ac at est.
  icon: fa-solid fa-star
  key: cyan
  sub_title: 2022-Q2
- title: Two
  content: Lorem ipsum dolor sit amet.
  icon: fa-solid fa-meteor
  sub_title: 2022-Q3
- title: Three
  content: Lorem ipsum dolor sit amet.
  key: pink
  sub_title: 2022-Q4
- title: Four
  content: Lorem ipsum dolor sit amet.
  icon: fa-solid fa-fire
  key: cyan
  sub_title: 2023-Q1

::/timeline::


::timeline:: dua

[
    {
        "title": "Zero",
        "sub_title": "2022-Q1",
        "content": "Better late than never! Lorem ipsum dolor sit amet.",
        "icon": "fa-solid fa-archway",
        "key": "blue"
    },
    {
        "title": "One",
        "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin felis eros, facilisis sed feugiat a, efficitur ut neque. In vel nulla et nulla aliquet porta ac at est.",
        "icon": "fa-solid fa-star",
        "key": "cyan",
        "sub_title": "2022-Q2"
    },
    {
        "title": "Two",
        "content": "Lorem ipsum dolor sit amet.",
        "icon": "fa-solid fa-meteor",
        "sub_title": "2022-Q3"
    },
    {
        "title": "Three",
        "content": "Lorem ipsum dolor sit amet.",
        "key": "pink",
        "sub_title": "2022-Q4"
    },
    {
        "title": "Four",
        "content": "Lorem ipsum dolor sit amet.",
        "icon": "fa-solid fa-fire",
        "key": "cyan",
        "sub_title": "2023-Q1"
    }
]

::/timeline::

::timeline:: csv

title,sub_title,content,icon,key
Zero,2022-Q1,Better late than never! Lorem ipsum dolor sit amet.,fa-solid fa-archway,blue
One,2022-Q2,"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin felis eros, facilisis sed feugiat a, efficitur ut neque. In vel nulla et nulla aliquet porta ac at est.",fa-solid fa-star,cyan
Two,2022-Q3,Lorem ipsum dolor sit amet.,fa-solid fa-meteor,
Three,2022-Q4,Lorem ipsum dolor sit amet.,,pink
Four,2023-Q1,Lorem ipsum dolor sit amet.,fa-solid fa-fire,cyan

::/timeline::
"""
    html = markdown.markdown(example, extensions=[TimelineExtension()])

    assert html is not None
