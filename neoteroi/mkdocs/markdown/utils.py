"""
Common utilities for the whole package.
"""

from dataclasses import fields, is_dataclass

_FIELDS = {}


def _get_fields(cls):
    try:
        return _FIELDS[cls]
    except KeyError:
        _FIELDS[cls] = {f.name for f in fields(cls)}
        return _FIELDS[cls]


def _norm_key(key: str) -> str:
    return key.replace("-", "_").lower()


def create_instance(cls, props, field_names=None):
    """
    Creates an instance of a given dataclass type, ignoring extra properties.
    """
    if not is_dataclass(cls):
        raise ValueError("The given type is not a dataclass")
    if field_names is None:
        field_names = _get_fields(cls)
    return cls(
        **{_norm_key(k): v for k, v in props.items() if _norm_key(k) in field_names}
    )


def create_instances(cls, items):
    """
    Creates a list of instances of a given dataclass type, ignoring extra properties
    on single items.
    """
    field_names = _get_fields(cls)
    return [create_instance(cls, item, field_names) for item in items]
