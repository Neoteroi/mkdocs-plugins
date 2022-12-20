import textwrap
import xml.etree.ElementTree as etree

import markdown
import pytest

from neoteroi.mkdocs.timeline import BaseTimelineProcessor, TimelineExtension
from tests import get_resource_file_path

EXAMPLE_1 = """
<div class="nt-timeline vertical left">
<div class="nt-timeline-before"></div>
<div class="nt-timeline-items">
<div class="nt-timeline-item blue">
<p class="nt-timeline-title">Zero</p>
<span class="nt-timeline-sub-title">2022-Q1</span><p class="nt-timeline-content">Better late than never! Lorem ipsum dolor sit amet.</p>
<div class="nt-timeline-dot blue bigger"><i class="fa-solid fa-archway icon"></i></div>
</div>
<div class="nt-timeline-item cyan">
<p class="nt-timeline-title">One</p>
<span class="nt-timeline-sub-title">2022-Q2</span><p class="nt-timeline-content">Lorem ipsum dolor sit amet, consectetur adipiscing.</p>
<div class="nt-timeline-dot cyan bigger"><i class="fa-solid fa-star icon"></i></div>
</div>
</div>
<div class="nt-timeline-after"></div>
</div>
"""

EXAMPLE_2 = """
<div class="nt-timeline vertical left">
<div class="nt-timeline-before"></div>
<div class="nt-timeline-items">
<div class="nt-timeline-item blue">
<p class="nt-timeline-title">Zero</p>
<span class="nt-timeline-sub-title">2022-Q1</span><p class="nt-timeline-content">Better late than never! Lorem ipsum dolor sit amet.</p>
<div class="nt-timeline-dot blue bigger"><i class="fa-solid fa-archway icon"></i></div>
</div>
<div class="nt-timeline-item cyan">
<p class="nt-timeline-title">One</p>
<span class="nt-timeline-sub-title">2022-Q2</span><p class="nt-timeline-content">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin felis eros, facilisis sed feugiat a, efficitur ut neque. In vel nulla et nulla aliquet porta ac at est.</p>
<div class="nt-timeline-dot cyan bigger"><i class="fa-solid fa-star icon"></i></div>
</div>
<div class="nt-timeline-item">
<p class="nt-timeline-title">Two</p>
<span class="nt-timeline-sub-title">2022-Q3</span><p class="nt-timeline-content">Lorem ipsum dolor sit amet.</p>
<div class="nt-timeline-dot  bigger"><i class="fa-solid fa-meteor icon"></i></div>
</div>
<div class="nt-timeline-item pink">
<p class="nt-timeline-title">Three</p>
<span class="nt-timeline-sub-title">2022-Q4</span><p class="nt-timeline-content">Lorem ipsum dolor sit amet.</p>
<div class="nt-timeline-dot pink"></div>
</div>
<div class="nt-timeline-item cyan">
<p class="nt-timeline-title">Four</p>
<span class="nt-timeline-sub-title">2023-Q1</span><p class="nt-timeline-content">Lorem ipsum dolor sit amet.</p>
<div class="nt-timeline-dot cyan bigger"><i class="fa-solid fa-fire icon"></i></div>
</div>
</div>
<div class="nt-timeline-after"></div>
</div>
"""

EXAMPLE_3 = """
<div class="nt-timeline vertical left">
<div class="nt-timeline-before"></div>
<div class="nt-timeline-items">
<div class="nt-timeline-item blue">
<p class="nt-timeline-title">Zero</p>
<span class="nt-timeline-sub-title">2022-Q1</span><p class="nt-timeline-content">Better late than never! Lorem ipsum dolor sit amet.</p>
<div class="nt-timeline-dot blue bigger"><img alt="step icon" class="icon" src="/img/foo-1.png" /></div>
</div>
<div class="nt-timeline-item cyan">
<p class="nt-timeline-title">One</p>
<span class="nt-timeline-sub-title">2022-Q2</span><p class="nt-timeline-content">Lorem ipsum dolor sit amet, consectetur adipiscing.</p>
<div class="nt-timeline-dot cyan bigger"><img alt="step icon" class="icon" src="/img/foo-2.png" /></div>
</div>
</div>
<div class="nt-timeline-after"></div>
</div>
"""

EXAMPLE_4 = """
<div class="nt-timeline vertical left">
<div class="nt-timeline-before"></div>
<div class="nt-timeline-items">
<div class="nt-timeline-item blue">
<p class="nt-timeline-title">Zero</p>
<span class="nt-timeline-sub-title">2022-Q1</span><p class="nt-timeline-content">Better late than never! Lorem ipsum dolor sit amet.</p>
<div class="nt-timeline-dot blue bigger"><span class="icon">:fontawesome-regular-face-laugh-wink:</span></div>
</div>
<div class="nt-timeline-item cyan">
<p class="nt-timeline-title">One</p>
<span class="nt-timeline-sub-title">2022-Q2</span><p class="nt-timeline-content">Lorem ipsum dolor sit amet, consectetur adipiscing.</p>
<div class="nt-timeline-dot cyan bigger"><span class="icon">:octicons-bug-16:</span></div>
</div>
</div>
<div class="nt-timeline-after"></div>
</div>
"""

EXAMPLE_5 = """
<div class="nt-timeline vertical left">
<div class="nt-timeline-before"></div>
<div class="nt-timeline-items">
<div class="nt-timeline-item">
<p class="nt-timeline-title">Zero</p>
<div class="nt-timeline-dot "></div>
</div>
<div class="nt-timeline-item">
<p class="nt-timeline-title">One</p>
<div class="nt-timeline-dot "></div>
</div>
</div>
<div class="nt-timeline-after"></div>
</div>
"""


def test_base_timeline_processor_raises_for_not_list_input():
    processor = BaseTimelineProcessor()

    with pytest.raises(TypeError):
        processor.build_html(etree.Element("div"), "", {})


@pytest.mark.parametrize(
    "example,expected_result",
    [
        [
            """
            ::timeline::

            [
                {
                    "title": "Zero",
                    "content": "Better late than never! Lorem ipsum dolor sit amet.",
                    "icon": "fa-solid fa-archway",
                    "key": "blue",
                    "sub_title": "2022-Q1"
                },
                {
                    "title": "One",
                    "content": "Lorem ipsum dolor sit amet, consectetur adipiscing.",
                    "icon": "fa-solid fa-star",
                    "key": "cyan",
                    "sub_title": "2022-Q2"
                }
            ]

            ::/timeline::
            """,
            EXAMPLE_1,
        ],
        [
            """
            ::timeline:: json


            [
                {
                    "title": "Zero",
                    "content": "Better late than never! Lorem ipsum dolor sit amet.",
                    "icon": "fa-solid fa-archway",
                    "key": "blue",
                    "sub_title": "2022-Q1"
                },
                {
                    "title": "One",
                    "content": "Lorem ipsum dolor sit amet, consectetur adipiscing.",
                    "icon": "fa-solid fa-star",
                    "key": "cyan",
                    "sub_title": "2022-Q2"
                }
            ]


            ::/timeline::
            """,
            EXAMPLE_1,
        ],
        [
            """
            ::timeline::
            [
                {
                    "title": "Zero",
                    "content": "Better late than never! Lorem ipsum dolor sit amet.",
                    "icon": "fa-solid fa-archway",
                    "key": "blue",
                    "sub_title": "2022-Q1"
                },
                {
                    "title": "One",
                    "content": "Lorem ipsum dolor sit amet, consectetur adipiscing.",
                    "icon": "fa-solid fa-star",
                    "key": "cyan",
                    "sub_title": "2022-Q2"
                }
            ]
            ::/timeline::
            """,
            EXAMPLE_1,
        ],
        [
            """
            ::timeline::

            [
                {
                    "title": "Zero",
                    "content": "Better late than never! Lorem ipsum dolor sit amet.",
                    "icon": "/img/foo-1.png",
                    "key": "blue",
                    "sub_title": "2022-Q1"
                },
                {
                    "title": "One",
                    "content": "Lorem ipsum dolor sit amet, consectetur adipiscing.",
                    "icon": "/img/foo-2.png",
                    "key": "cyan",
                    "sub_title": "2022-Q2"
                }
            ]

            ::/timeline::
            """,
            EXAMPLE_3,
        ],
        [
            """
            ::timeline::

            [
                {
                    "title": "Zero",
                    "content": "Better late than never! Lorem ipsum dolor sit amet.",
                    "icon": ":fontawesome-regular-face-laugh-wink:",
                    "key": "blue",
                    "sub_title": "2022-Q1"
                },
                {
                    "title": "One",
                    "content": "Lorem ipsum dolor sit amet, consectetur adipiscing.",
                    "icon": ":octicons-bug-16:",
                    "key": "cyan",
                    "sub_title": "2022-Q2"
                }
            ]

            ::/timeline::
            """,
            EXAMPLE_4,
        ],
        [
            """
            ::timeline::

            [
                {
                    "title": "Zero"
                },
                {
                    "title": "One"
                }
            ]

            ::/timeline::
            """,
            EXAMPLE_5,
        ],
    ],
)
def test_timeline_extension(example, expected_result):
    html = markdown.markdown(example, extensions=[TimelineExtension(priority=100)])
    assert html.strip() == expected_result.strip()


@pytest.mark.parametrize(
    "example,expected_result",
    [
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
            EXAMPLE_2,
        ],
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
            EXAMPLE_2,
        ],
    ],
)
def test_timeline_extension_csv_format(example, expected_result):
    html = markdown.markdown(example, extensions=[TimelineExtension(priority=100)])
    assert html.strip() == expected_result.strip()


@pytest.mark.parametrize(
    "example,expected_result",
    [
        [
            textwrap.dedent(
                f"""
                [timeline({get_resource_file_path('./timeline-1.json')})]
                """
            ),
            EXAMPLE_1,
        ],
        [
            textwrap.dedent(
                f"""
                [timeline({get_resource_file_path('./timeline-1.yaml')})]
                """
            ),
            EXAMPLE_1,
        ],
        [
            textwrap.dedent(
                f"""
                [timeline yaml({get_resource_file_path('./timeline-1.yaml')})]
                """
            ),
            EXAMPLE_1,
        ],
    ],
)
def test_timeline_from_source(example, expected_result):
    html = markdown.markdown(example, extensions=[TimelineExtension(priority=100)])
    assert html.strip() == expected_result.strip()
