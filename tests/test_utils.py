from dataclasses import dataclass

import pytest

from neoteroi.mkdocs.markdown.utils import create_instance, create_instances


@dataclass
class Foo:
    id: int
    name: str


def test_create_instance():
    foo = create_instance(Foo, {"id": 1, "name": "Foo", "extra_to_ignore": False})

    assert isinstance(foo, Foo)
    assert foo.id == 1
    assert foo.name == "Foo"


def test_create_instances():
    foos = create_instances(
        Foo,
        [
            {"id": 1, "name": "Foo", "extra_to_ignore": False},
            {"id": 2, "name": "Foo 2", "extra_to_ignore": True},
        ],
    )

    assert isinstance(foos[0], Foo)
    assert foos[0].id == 1
    assert foos[0].name == "Foo"
    assert isinstance(foos[1], Foo)
    assert foos[1].id == 2
    assert foos[1].name == "Foo 2"


def test_create_instance_raises_for_non_dataclass():
    class NotDataclass:
        pass

    with pytest.raises(ValueError):
        create_instance(NotDataclass, {})
