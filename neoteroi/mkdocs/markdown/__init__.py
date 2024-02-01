"""
This package contains common utilities for markdown used across the various plugins
for Markdown.
"""

import re
from typing import Dict, Tuple

_PROPS_RE = re.compile(
    r"""\s?((?P<name>[^\s\=]+)=(?P<quot>"|')(?P<value>[^\"\']+)(?P=quot))""",
    re.DOTALL | re.MULTILINE,
)


def parse_props(
    line: str, prefix: str = "", bool_attrs: bool = False
) -> Dict[str, str]:
    """
    Parses a line describing properties, in this form:

    prop1="value1" prop2="value2"

    It also parses boolean attributes, if bool_attrs is set to true:

    id="example" class="foo another" multiple

    into a dictionary of names and values. It accepts an optional prefix, to filter
    properties names.
    """
    props = {}

    for match in _PROPS_RE.findall(line):
        name: str = match[1]
        value: str = match[3]
        if prefix:
            if name.startswith(prefix):
                props[name[len(prefix) :]] = value
        else:
            props[name] = value

    if bool_attrs:
        for word in _PROPS_RE.sub("", line).split():
            if "=" in word:
                name, value = word.split("=")
                props[name] = value
            else:
                props[word] = True

    return props


def extract_props(line: str, prefix: str = "") -> Tuple[str, Dict[str, str]]:
    """
    Extracts properties like the `parse_props` function, but
    also returns the original line with properties removed.
    """
    props = parse_props(line, prefix)
    return _PROPS_RE.sub("", line).strip(), props
