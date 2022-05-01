"""
This package contains common utilities for markdown used across the various plugins
for Markdown.
"""
import re

from typing import Dict


_PROPS_RE = re.compile(
    r"""\s?((?P<name>[^\s\=]+)=(?P<quot>"|')(?P<value>[^\"\']+)(?P=quot))""",
    re.DOTALL | re.MULTILINE,
)


def parse_props(line: str) -> Dict[str, str]:
    """
    Parses a line describing properties, in this form:

    prop1="value1" prop2="value2"

    into a dictionary of names and values.
    """
    props = {}

    for match in _PROPS_RE.findall(line):
        props[match[1]] = match[3]

    return props
