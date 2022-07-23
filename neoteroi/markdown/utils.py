"""
Common utilities for the whole package.
"""
from dataclasses import fields, is_dataclass


def create_instance(cls, props):
    """
    Creates an instance of a given dataclass type, ignoring extra properties.
    """
    if not is_dataclass(cls):
        raise ValueError("The given type is not a dataclass")
    class_fields = {f.name for f in fields(cls)}
    return cls(**{k: v for k, v in props.items() if k in class_fields})
