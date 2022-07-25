"""
Common utilities for the whole package.
"""
from dataclasses import fields, is_dataclass


def create_instance(cls, props, field_names=None):
    """
    Creates an instance of a given dataclass type, ignoring extra properties.
    """
    if not is_dataclass(cls):
        raise ValueError("The given type is not a dataclass")
    if field_names is None:
        field_names = {f.name for f in fields(cls)}
    return cls(**{k: v for k, v in props.items() if k in field_names})


def create_instances(cls, items):
    """
    Creates a list of instances of a given dataclass type, ignoring extra properties
    on single items.
    """
    field_names = {f.name for f in fields(cls)}
    return [create_instance(cls, item, field_names) for item in items]