"""
This module contains methods to render the contributions stats.
"""

import xml.etree.ElementTree as etree
from dataclasses import dataclass
from datetime import datetime
from typing import List
from xml.etree.ElementTree import tostring as xml_to_str

from neoteroi.mkdocs.contribs.domain import Contributor


def _get_initials(value: str) -> str:
    return "".join([x[0].upper() for x in value.split(" ")][:2])


@dataclass
class ContribsViewOptions:
    contributors_label: str
    last_modified_label: str
    show_last_modified_time: bool
    show_contributors_title: bool
    time_format: str


def contribution_stats_to_element(
    contributors: List[Contributor],
    last_commit_date: datetime,
    options: ContribsViewOptions,
) -> etree.Element:
    element = etree.Element("div", {"class": "nt-contribs"})

    if options.show_last_modified_time:
        last_modified_time = etree.SubElement(
            element,
            "p",
            {"class": "nt-mod-time"},
        )
        if options.last_modified_label:
            last_modified_time.text = (
                f"{options.last_modified_label}: "
                f"{last_commit_date.strftime(options.time_format)}"
            )
        else:
            last_modified_time.text = last_commit_date.strftime(options.time_format)

    if options.show_contributors_title:
        contributors_title = etree.SubElement(
            element, "p", {"class": "nt-contributors-title"}
        )
        contributors_title.text = f"{options.contributors_label} ({len(contributors)})"

    contributors_parent = etree.SubElement(element, "div", {"class": "nt-contributors"})

    for i, contributor in enumerate(
        sorted(contributors, key=lambda item: item.count, reverse=True)
    ):
        props = {
            "class": "nt-contributor"
            + (f" {contributor.key}" if contributor.key else ""),
            "title": (
                f"{contributor.name} <{contributor.email}> ({contributor.count})"
            ),
        }

        if contributor.image:
            props.update(
                {
                    "class": "nt-contributor image",
                    "style": ("background-image: " f"url('{contributor.image}')"),
                }
            )
        props["class"] += f" nt-group-{i}"
        contrib_el = etree.SubElement(contributors_parent, "div", props)

        if not contributor.image:
            # display initials
            initials_el = etree.SubElement(contrib_el, "span", {"class": "nt-initials"})
            initials_el.text = _get_initials(contributor.name)
        else:
            etree.SubElement(contrib_el, "span", {"class": "nt-initials"})

    return element


def render_contribution_stats(
    contributors: List[Contributor],
    last_commit_date: datetime,
    options: ContribsViewOptions,
) -> str:
    return xml_to_str(
        contribution_stats_to_element(contributors, last_commit_date, options)
    ).decode("utf8")
