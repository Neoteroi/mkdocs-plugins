import pytest

from neoteroi.mkdocs.markdown.images import Image


def test_image_from_str():
    url_path = "/one/two/three.png"
    image = Image.from_obj(url_path)
    assert image.url == url_path
    assert image.alt is None


def test_image_from_obj():
    url_path = "/one/two/three.png"
    image = Image.from_obj({"url": url_path, "alt": "Some picture"})
    assert image.url == url_path
    assert image.alt == "Some picture"


def test_image_raises_for_invalid_obj():
    with pytest.raises(TypeError):
        Image.from_obj(set())


@pytest.mark.parametrize(
    "image,expected_props",
    [
        (Image.from_obj("/one/two/three.png"), {"src": "/one/two/three.png"}),
        (
            Image(url="/one/two/three.png", height=100),
            {"src": "/one/two/three.png", "height": "100"},
        ),
        (
            Image(url="/one/two/three.png", alt="Something"),
            {"src": "/one/two/three.png", "alt": "Something"},
        ),
        (
            Image(url="/one/two/three.png", width=100),
            {"src": "/one/two/three.png", "width": "100"},
        ),
        (
            Image(url="/one/two/three.png", height=50, width=100),
            {"src": "/one/two/three.png", "height": "50", "width": "100"},
        ),
    ],
)
def test_image_get_props(image: Image, expected_props):
    props = image.get_props()
    assert props == expected_props
