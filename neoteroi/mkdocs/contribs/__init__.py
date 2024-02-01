"""
This module provide a plugin that can be used to generate last modified time and
contributors list for each page, assuming that:

- the MkDocs site is built in a Git repository.
- the Git CLI can be used during the build.

"""

import logging
from datetime import datetime
from fnmatch import fnmatch
from pathlib import Path
from subprocess import CalledProcessError
from typing import List

from mkdocs.config import config_options as c
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File
from mkdocs.structure.pages import Page

from neoteroi.mkdocs.contribs.domain import ContributionsReader, Contributor
from neoteroi.mkdocs.contribs.git import GitContributionsReader
from neoteroi.mkdocs.contribs.html import ContribsViewOptions, render_contribution_stats
from neoteroi.mkdocs.contribs.txt import TXTContributionsReader

logger = logging.getLogger("MARKDOWN")


class DefaultContributionsReader(ContributionsReader):
    """
    Supports both contributors obtained from Git history and from configuration files.
    """

    def __init__(self) -> None:
        super().__init__()
        self._git_reader = GitContributionsReader()
        self._txt_reader = TXTContributionsReader()

    def get_contributors(self, file_path: Path) -> List[Contributor]:
        git_history_contributors = self._git_reader.get_contributors(file_path)
        configured_contributors = self._txt_reader.get_contributors(file_path)
        return list(
            {
                item.email: item
                for item in configured_contributors + git_history_contributors
            }.values()
        )

    def get_last_modified_date(self, file_path: Path) -> datetime:
        return self._git_reader.get_last_modified_date(file_path)


class ContribsPlugin(BasePlugin):
    _contribs_reader: ContributionsReader
    config_scheme = (
        ("contributors_label", c.Type(str, default="Contributors")),
        ("last_modified_label", c.Type(str, default="Last modified on")),
        ("time_format", c.Type(str, default="%Y-%m-%d %H:%M:%S")),
        ("contributors", c.Type(list, default=[])),
        ("show_last_modified_time", c.Type(bool, default=True)),
        ("show_contributors_title", c.Type(bool, default=False)),
        ("exclude", c.Type(list, default=[])),
    )

    def __init__(self) -> None:
        super().__init__()
        self._contribs_reader = DefaultContributionsReader()

    def _merge_contributor_by_email(
        self,
        contributors: List[Contributor],
        contributor: Contributor,
        contributor_info: dict,
    ) -> bool:
        """
        Handles an optional "merge_with" property in the contributor info object
        (from configuration), returning true if the given contributor (from repo
        information) should be discarded (its commits count was merged with another
        one).
        """
        assert contributor.email == contributor_info.get(
            "email"
        ), "The contributor info object must match the contributor object."
        merge_with = contributor_info.get("merge_with")

        if merge_with:
            parent = next(
                (item for item in contributors if item.email == merge_with),
                None,
            )
            if parent:
                parent.count += contributor.count
                return True

        return False

    def _get_contributors(self, page_file: File) -> List[Contributor]:
        results = []
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
                contributor.key = contributor_info.get("key")

                if contributor_info.get("ignore"):
                    # ignore the contributor's information (can be useful for bots)
                    continue

                if (
                    "name" in contributor_info
                    and contributor_info["name"] != contributor.name
                ):
                    parent = next(
                        (
                            other
                            for other in contributors
                            if other.name == contributor_info["name"]
                        ),
                        None,
                    )
                    if parent:
                        parent.count += contributor.count
                        continue
                    else:
                        # use configured name
                        contributor.name = contributor_info["name"]

                # should contributor information be merged with another object?
                if self._merge_contributor_by_email(
                    contributors, contributor, contributor_info
                ):
                    # skip this item as it was merged with another one
                    continue

            results.append(contributor)

        return results

    def _get_last_commit_date(self, page_file: File) -> datetime:
        return self._contribs_reader.get_last_modified_date(
            Path("docs") / page_file.src_path
        )

    def _set_contributors(self, markdown: str, page: Page) -> str:
        page_file = page.file
        last_commit_date = self._get_last_commit_date(page_file)
        contributors = self._get_contributors(page_file)
        return (
            markdown
            + "\n\n"
            + render_contribution_stats(
                contributors,
                last_commit_date,
                ContribsViewOptions(
                    self.config["contributors_label"],
                    self.config["last_modified_label"],
                    self.config["show_last_modified_time"],
                    self.config["show_contributors_title"],
                    self.config["time_format"],
                ),
            )
        )

    def _is_ignored_page(self, page: Page) -> bool:
        if not self.config.get("exclude"):
            return False

        return any(
            fnmatch(page.file.src_path, ignored_pattern)
            for ignored_pattern in self.config["exclude"]
        )

    def on_page_markdown(self, markdown, *args, **kwargs):
        if self._is_ignored_page(kwargs["page"]):
            return markdown
        try:
            markdown = self._set_contributors(markdown, kwargs["page"])
        except (CalledProcessError, ValueError) as operation_error:
            logger.error(
                "Failed to display contributors list for page: %s",
                kwargs["page"].title,
                exc_info=operation_error,
            )
            pass
        return markdown
