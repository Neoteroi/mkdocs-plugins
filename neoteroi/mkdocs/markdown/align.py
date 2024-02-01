"""
Objects to describe alignment of elements.
"""

import logging
from enum import Enum

logger = logging.getLogger("MARKDOWN")


class Alignment(Enum):
    CENTER = "center"
    LEFT = "left"
    RIGHT = "right"


def aligment_from_props(props):
    if props.get("center") is True:
        return Alignment.CENTER

    if props.get("left") is True:
        return Alignment.LEFT

    if props.get("right") is True:
        return Alignment.RIGHT

    return try_parse_align(props.get("align", "left"))


def try_parse_align(align: str):
    try:
        return Alignment(align)
    except ValueError:
        logger.exception(
            "Invalid timeline align property: %s; ignoring this attribute", align
        )
        return Alignment.LEFT
