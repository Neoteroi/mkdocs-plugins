import xml.etree.ElementTree as etree

import markdown
import pytest

from neoteroi.mkdocs.cards import BaseCardsProcessor, CardsExtension
from neoteroi.mkdocs.cards.domain import CardItem
from neoteroi.mkdocs.markdown.images import Image
from tests import equal_html

EXAMPLE_1 = """
<div class="nt-cards nt-grid cols-3">
<div class="nt-card"><a href="/some-path/a"><div><div class="nt-card-image tags"><img alt="Title A" src="/img/icons/lorem-ipsum-1.png" /></div><div class="nt-card-content"><p class="nt-card-title">Title A</p><p class="nt-card-text">Lorem ipsum dolor sit amet 1.</p></div></div></a></div>
<div class="nt-card"><a href="/some-path/b"><div><div class="nt-card-image tags"><img alt="Title B" src="/img/icons/lorem-ipsum-2.png" /></div><div class="nt-card-content"><p class="nt-card-title">Title B</p><p class="nt-card-text">Lorem ipsum dolor sit amet 2.</p></div></div></a></div>
<div class="nt-card"><a href="/some-path/c"><div><div class="nt-card-image tags"><img alt="Title C" src="/img/icons/lorem-ipsum-3.png" /></div><div class="nt-card-content"><p class="nt-card-title">Title C</p><p class="nt-card-text">Lorem ipsum dolor sit amet 3.</p></div></div></a></div>
<div class="nt-card"><a href="/some-path/d"><div><div class="nt-card-image tags"><img alt="Title D" src="/img/icons/lorem-ipsum-4.png" /></div><div class="nt-card-content"><p class="nt-card-title">Title D</p><p class="nt-card-text">Lorem ipsum dolor sit amet 4.</p></div></div></a></div>
</div>
"""

EXAMPLE_1_b = """
<div class="nt-cards nt-grid cols-3">
<div class="nt-card"><a href="/some-path/a" rel="noopener" target="_blank"><div><div class="nt-card-image tags"><img alt="Title A" src="/img/icons/lorem-ipsum-1.png" /></div><div class="nt-card-content"><p class="nt-card-title">Title A</p><p class="nt-card-text">Lorem ipsum dolor sit amet 1.</p></div></div></a></div>
<div class="nt-card"><a href="/some-path/b" rel="noopener" target="_blank"><div><div class="nt-card-image tags"><img alt="Title B" src="/img/icons/lorem-ipsum-2.png" /></div><div class="nt-card-content"><p class="nt-card-title">Title B</p><p class="nt-card-text">Lorem ipsum dolor sit amet 2.</p></div></div></a></div>
<div class="nt-card"><a href="/some-path/c" rel="noopener" target="_blank"><div><div class="nt-card-image tags"><img alt="Title C" src="/img/icons/lorem-ipsum-3.png" /></div><div class="nt-card-content"><p class="nt-card-title">Title C</p><p class="nt-card-text">Lorem ipsum dolor sit amet 3.</p></div></div></a></div>
<div class="nt-card"><a href="/some-path/d" rel="noopener" target="_blank"><div><div class="nt-card-image tags"><img alt="Title D" src="/img/icons/lorem-ipsum-4.png" /></div><div class="nt-card-content"><p class="nt-card-title">Title D</p><p class="nt-card-text">Lorem ipsum dolor sit amet 4.</p></div></div></a></div>
</div>
"""

EXAMPLE_2 = """
<div class="nt-cards nt-grid cols-3">
<div class="nt-card"><a href="/some-path/a"><div><div class="nt-card-image tags"><img alt="Title A" src="/img/icons/lorem-ipsum-1.png" /></div><div class="nt-card-content"><p class="nt-card-title">Title A</p><p class="nt-card-text">Lorem ipsum dolor sit amet 1.</p></div></div></a></div>
<div class="nt-card"><a href="/some-path/b"><div><div class="nt-card-image tags"><img alt="Title B" src="/img/icons/lorem-ipsum-2.png" /></div><div class="nt-card-content"><p class="nt-card-title">Title B</p><p class="nt-card-text">Lorem ipsum dolor sit amet 2.</p></div></div></a></div>
<div class="nt-card"><a href="/some-path/c"><div><div class="nt-card-image tags"><img alt="Title C" src="/img/icons/lorem-ipsum-3.png" /></div><div class="nt-card-content"><p class="nt-card-title">Title C</p><p class="nt-card-text">Lorem ipsum dolor sit amet 3.</p></div></div></a></div>
<div class="nt-card"><a href="/some-path/d"><div><div class="nt-card-image tags"><img alt="Title D" src="/img/icons/lorem-ipsum-4.png" /></div><div class="nt-card-content"><p class="nt-card-title">Title D</p><p class="nt-card-text">Lorem ipsum dolor sit amet 4.</p></div></div></a></div>
</div>
"""

EXAMPLE_3 = """
<div class="nt-cards nt-grid cols-4">
<div class="nt-card aaa"><a href="/some-path/a"><div><div class="nt-card-image tags"><img alt="Title A" src="/img/icons/lorem-ipsum-1.png" /></div><div class="nt-card-content"><p class="nt-card-title">Title A</p><p class="nt-card-text">Lorem ipsum dolor sit amet 1.</p></div></div></a></div>
<div class="nt-card bbb"><a href="/some-path/b"><div><div class="nt-card-image tags"><img alt="Title B" src="/img/icons/lorem-ipsum-2.png" /></div><div class="nt-card-content"><p class="nt-card-title">Title B</p><p class="nt-card-text">Lorem ipsum dolor sit amet 2.</p></div></div></a></div>
<div class="nt-card ccc"><a href="/some-path/c"><div><div class="nt-card-image tags"><img alt="Title C" src="/img/icons/lorem-ipsum-3.png" /></div><div class="nt-card-content"><p class="nt-card-title">Title C</p><p class="nt-card-text">Lorem ipsum dolor sit amet 3.</p></div></div></a></div>
<div class="nt-card ddd"><a href="/some-path/d"><div><div class="nt-card-image tags"><img alt="Title D" src="/img/icons/lorem-ipsum-4.png" /></div><div class="nt-card-content"><p class="nt-card-title">Title D</p><p class="nt-card-text">Lorem ipsum dolor sit amet 4.</p></div></div></a></div>
</div>
"""

EXAMPLE_4 = """
<div class="nt-cards nt-grid cols-4">
<div class="nt-card aaa">
<div class="nt-card-wrap">
<div>
<div class="nt-card-image tags"><img alt="Title A" src="/img/icons/lorem-ipsum-1.png" /></div>
<div class="nt-card-content">
<p class="nt-card-title">Title A</p>
<p class="nt-card-text">Lorem ipsum dolor sit amet 1.</p>
</div>
</div>
</div>
</div>
<div class="nt-card bbb">
<div class="nt-card-wrap">
<div>
<div class="nt-card-image tags"><img alt="Title B" src="/img/icons/lorem-ipsum-2.png" /></div>
<div class="nt-card-content">
<p class="nt-card-title">Title B</p>
<p class="nt-card-text">Lorem ipsum dolor sit amet 2.</p>
</div>
</div>
</div>
</div>
</div>
"""

EXAMPLE_5 = """
<div class="nt-cards nt-grid cols-3">
<div class="nt-card"><div class="nt-card-wrap"><div><div class="nt-card-content"><p class="nt-card-title">Title A</p><p class="nt-card-text">Hello World.</p></div></div></div></div>
<div class="nt-card"><div class="nt-card-wrap"><div><div class="nt-card-content"><p class="nt-card-title">Title B</p><p class="nt-card-text">Hello Spank.</p></div></div></div></div>
</div>
"""

EXAMPLE_6 = """
<div class="nt-cards nt-grid cols-3">
<div class="nt-card"><a href="/some-path/a"><div><div class="nt-card-icon"><img alt="step icon" class="icon" src="/img/icons/icon.svg" /></div><div class="nt-card-content"><p class="nt-card-title">Title A</p><p class="nt-card-text">Lorem ipsum dolor sit amet 1.</p></div></div></a></div>
<div class="nt-card"><a href="/some-path/b"><div><div class="nt-card-icon"><i class="fa-solid fa-star icon"></i></div><div class="nt-card-content"><p class="nt-card-title">Title B</p><p class="nt-card-text">Lorem ipsum dolor sit amet 2.</p></div></div></a></div>
<div class="nt-card"><a href="/some-path/c"><div><div class="nt-card-icon"><span class="icon">:octicons-bug-16:</span></div><div class="nt-card-content"><p class="nt-card-title">Title C</p><p class="nt-card-text">Lorem ipsum dolor sit amet 3.</p></div></div></a></div>
</div>
"""


def test_base_cards_processor_raises_for_not_list_input():
    processor = BaseCardsProcessor()

    with pytest.raises(TypeError):
        processor.build_html(etree.Element("div"), "", {})


@pytest.mark.parametrize(
    "example,expected_result",
    [
        [
            """
            ::cards:: flex=25 image-tags

            - title: Title A
              url: /some-path/a
              content: Lorem ipsum dolor sit amet 1.
              image: /img/icons/lorem-ipsum-1.png

            - title: Title B
              url: /some-path/b
              content: Lorem ipsum dolor sit amet 2.
              image: /img/icons/lorem-ipsum-2.png

            - title: Title C
              url: /some-path/c
              content: Lorem ipsum dolor sit amet 3.
              image: /img/icons/lorem-ipsum-3.png

            - title: Title D
              url: /some-path/d
              content: Lorem ipsum dolor sit amet 4.
              image: /img/icons/lorem-ipsum-4.png

            ::/cards::
            """,
            EXAMPLE_1,
        ],
        [
            """
            ::cards:: flex=25 image-tags blank_target

            - title: Title A
              url: /some-path/a
              content: Lorem ipsum dolor sit amet 1.
              image: /img/icons/lorem-ipsum-1.png

            - title: Title B
              url: /some-path/b
              content: Lorem ipsum dolor sit amet 2.
              image: /img/icons/lorem-ipsum-2.png

            - title: Title C
              url: /some-path/c
              content: Lorem ipsum dolor sit amet 3.
              image: /img/icons/lorem-ipsum-3.png

            - title: Title D
              url: /some-path/d
              content: Lorem ipsum dolor sit amet 4.
              image: /img/icons/lorem-ipsum-4.png

            ::/cards::
            """,
            EXAMPLE_1_b,
        ],
    ],
)
def test_cards_extension_image_tags(example, expected_result):
    html = markdown.markdown(example, extensions=[CardsExtension(priority=100)])
    assert html.strip() == expected_result.strip()


@pytest.mark.parametrize(
    "example,expected_result",
    [
        [
            """
            ::cards:: flex=25 image-tags

            - title: Title A
              url: /some-path/a
              content: Lorem ipsum dolor sit amet 1.
              image: /img/icons/lorem-ipsum-1.png

            - title: Title B
              url: /some-path/b
              content: Lorem ipsum dolor sit amet 2.
              image: /img/icons/lorem-ipsum-2.png

            - title: Title C
              url: /some-path/c
              content: Lorem ipsum dolor sit amet 3.
              image: /img/icons/lorem-ipsum-3.png

            - title: Title D
              url: /some-path/d
              content: Lorem ipsum dolor sit amet 4.
              image: /img/icons/lorem-ipsum-4.png

            ::/cards::
            """,
            EXAMPLE_1_b,
        ],
    ],
)
def test_cards_extension_target_blank_config(example, expected_result):
    html = markdown.markdown(
        example, extensions=[CardsExtension(priority=100, blank_target=True)]
    )
    assert html.strip() == expected_result.strip()


@pytest.mark.parametrize(
    "example,expected_result",
    [
        [
            """
            ::cards::

            - title: Title A
              url: /some-path/a
              content: Lorem ipsum dolor sit amet 1.
              image: /img/icons/lorem-ipsum-1.png

            - title: Title B
              url: /some-path/b
              content: Lorem ipsum dolor sit amet 2.
              image: /img/icons/lorem-ipsum-2.png

            - title: Title C
              url: /some-path/c
              content: Lorem ipsum dolor sit amet 3.
              image: /img/icons/lorem-ipsum-3.png

            - title: Title D
              url: /some-path/d
              content: Lorem ipsum dolor sit amet 4.
              image: /img/icons/lorem-ipsum-4.png

            ::/cards::
            """,
            EXAMPLE_2,
        ],
        [
            """
            ::cards::

            [
                {
                    "title": "Title A",
                    "url": "/some-path/a",
                    "content": "Lorem ipsum dolor sit amet 1.",
                    "image": "/img/icons/lorem-ipsum-1.png"
                },
                {
                    "title": "Title B",
                    "url": "/some-path/b",
                    "content": "Lorem ipsum dolor sit amet 2.",
                    "image": "/img/icons/lorem-ipsum-2.png"
                },
                {
                    "title": "Title C",
                    "url": "/some-path/c",
                    "content": "Lorem ipsum dolor sit amet 3.",
                    "image": "/img/icons/lorem-ipsum-3.png"
                },
                {
                    "title": "Title D",
                    "url": "/some-path/d",
                    "content": "Lorem ipsum dolor sit amet 4.",
                    "image": "/img/icons/lorem-ipsum-4.png"
                }
            ]

            ::/cards::
            """,
            EXAMPLE_2,
        ],
        [
            """
            ::cards:: cols=4

            - title: Title A
              url: /some-path/a
              content: Lorem ipsum dolor sit amet 1.
              image: /img/icons/lorem-ipsum-1.png
              key: aaa

            - title: Title B
              url: /some-path/b
              content: Lorem ipsum dolor sit amet 2.
              image: /img/icons/lorem-ipsum-2.png
              key: bbb

            - title: Title C
              url: /some-path/c
              content: Lorem ipsum dolor sit amet 3.
              image: /img/icons/lorem-ipsum-3.png
              key: ccc

            - title: Title D
              url: /some-path/d
              content: Lorem ipsum dolor sit amet 4.
              image: /img/icons/lorem-ipsum-4.png
              key: ddd

            ::/cards::
            """,
            EXAMPLE_3,
        ],
        [
            """
            ::cards:: cols=4

            - title: Title A
              content: Lorem ipsum dolor sit amet 1.
              image: /img/icons/lorem-ipsum-1.png
              key: aaa

            - title: Title B
              content: Lorem ipsum dolor sit amet 2.
              image: /img/icons/lorem-ipsum-2.png
              key: bbb

            ::/cards::
            """,
            EXAMPLE_4,
        ],
        [
            """
            ::cards::

            - title: Title A
              content: Hello World.

            - title: Title B
              content: Hello Spank.

            ::/cards::
            """,
            EXAMPLE_5,
        ],
    ],
)
def test_cards_extension(example, expected_result):
    html = markdown.markdown(example, extensions=[CardsExtension(priority=100)])
    assert equal_html(html, expected_result)


@pytest.mark.parametrize(
    "example,expected_result",
    [
        [
            """
            ::cards::

            - title: Title A
              url: /some-path/a
              content: Lorem ipsum dolor sit amet 1.
              icon: /img/icons/icon.svg

            - title: Title B
              url: /some-path/b
              content: Lorem ipsum dolor sit amet 2.
              icon: "fa-solid fa-star"

            - title: Title C
              url: /some-path/c
              content: Lorem ipsum dolor sit amet 3.
              icon: ":octicons-bug-16:"

            ::/cards::
            """,
            EXAMPLE_6,
        ],
    ],
)
def test_cards_extension_icons(example, expected_result):
    html = markdown.markdown(example, extensions=[CardsExtension(priority=100)])
    assert html.strip() == expected_result.strip()


def test_card_item_image_alt_default():
    """
    When a CardItem is instantiated and its image does not have an alt value, the image
    alt value is set to match the title.
    """

    card = CardItem("A nice Example", image=Image("example.jpg"))

    assert card.image is not None
    assert card.image.alt == card.title

    card = CardItem("A nice Example", image=Image("example.jpg", alt="Different alt"))
    assert card.image is not None
    assert card.image.alt == "Different alt"
