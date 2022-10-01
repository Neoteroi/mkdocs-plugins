"""
This module provide a plugin that can be used to generate last modified time and
contributors list for each page, assuming that:

- the MkDocs site is built in a Git repository.
- the Git CLI can be used during the build.

"""
import logging
from datetime import datetime
from pathlib import Path
from typing import List

from mkdocs.config import config_options as c
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File
from mkdocs.structure.pages import Page

from neoteroi.contribs.domain import ContributionsReader, Contributor
from neoteroi.contribs.git import GitContributionsReader
from neoteroi.contribs.html import ContribsViewOptions, render_contribution_stats

logger = logging.getLogger("MARKDOWN")


class ContribsPlugin(BasePlugin):
    _contribs_reader: ContributionsReader
    config_scheme = (
        ("contributors_label", c.Type(str, default="Contributors")),
        ("last_modified_label", c.Type(str, default="Last modified on")),
        ("last_modified_time", c.Type(bool, default=True)),
        ("time_format", c.Type(str, default="%Y-%m-%d %H:%M:%S")),
        ("contributors", c.Type(list, default=[])),
    )

    def __init__(self) -> None:
        super().__init__()
        self._contribs_reader = GitContributionsReader()

    def _get_contributors(self, page_file: File) -> List[Contributor]:
        contributors = self._contribs_reader.get_contributors(
            Path("docs") / page_file.src_path
        )
        info = self.config.get("contributors")

        if not info:
            return contributors

        for contributor in contributors:
            contributor_info = next(
                (item for item in info if item.get("email") == contributor.email), None
            )
            if contributor_info:
                contributor.image = contributor_info.get("image")

        return contributors

    def _get_last_commit_date(self, page_file: File) -> datetime:
        return self._contribs_reader.get_last_commit_date(
            Path("docs") / page_file.src_path
        )

    def _set_contributors(self, markdown: str, page: Page) -> str:
        page_file = page.file
        last_commit_date = self._get_last_commit_date(page_file)
        contributors = self._get_contributors(page_file)
        return markdown + render_contribution_stats(
            contributors,
            last_commit_date,
            ContribsViewOptions(
                self.config["contributors_label"],
                self.config["last_modified_label"],
                self.config["last_modified_time"],
                self.config["time_format"],
            ),
        )

    def on_page_markdown(self, markdown, *args, **kwargs):
        try:
            markdown = self._set_contributors(markdown, kwargs["page"])
        except ValueError:
            logger.error(
                "Failed to display contributors list for page: %s",
                kwargs["page"].title,
            )
            pass
        return markdown
