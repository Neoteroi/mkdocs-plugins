import os
import re
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Tuple

from dateutil.parser import parse

from neoteroi.mkdocs.contribs.domain import ContributionsReader, Contributor


def _read_lines_strip_comments(file_path: Path):
    with open(str(file_path), mode="rt", encoding="utf8") as file:
        lines = file.readlines()
    lines = (re.sub("#.+$", "", x).strip() for x in lines)
    return [line for line in lines if line]


class TXTContributionsReader(ContributionsReader):
    """
    A ContributionsReader that can read contributors information described in .txt
    files.
    """

    _contrib_rx = re.compile(
        r"(?P<name>[^\<]+)<(?P<email>[^\>]+)>\s\((?P<count>[^\>]+)\)"
    )

    _last_mod_time_rx = re.compile(
        r"^\s*Last\smodified\stime:\s(?P<value>.+)$", re.IGNORECASE | re.MULTILINE
    )

    def _parse_value(self, value: str) -> Tuple[str, str, int]:
        match = self._contrib_rx.search(value)
        if match:
            values = match.groupdict()
            name = values["name"].strip()
            email = values["email"].strip()
            count = int(values["count"])
        else:
            name, email, count = ("", "", -1)
        return name, email, count

    def _get_txt_file_path(self, file_path: Path) -> Path:
        path_without_extension = os.path.splitext(file_path)[0]
        return Path(path_without_extension + ".contribs.txt")

    def _get_contributors_from_txt_file(self, file_path: Path) -> Iterable[Contributor]:
        for line in _read_lines_strip_comments(file_path):
            name, email, count = self._parse_value(line)
            if name and email:
                yield Contributor(name, email, count)

    def get_contributors(self, file_path: Path) -> List[Contributor]:
        """
        Obtains the list of contributors from a txt file with the given path.
        The file contents should look like:

        Charlie Brown <charlie.brown@peanuts.com> (3)

        Having each line with such pattern:

        Name <email> (Contributions Count)

        and supporting comments using hashes:
        # Example comment
        """
        txt_path = self._get_txt_file_path(file_path)

        if not txt_path.exists():
            return []

        return list(self._get_contributors_from_txt_file(txt_path))

    def get_last_modified_date(self, file_path: Path) -> datetime:
        """Reads the last commit date of a file."""
        txt_path = self._get_txt_file_path(file_path)

        if not txt_path.exists():
            raise FileNotFoundError()

        match = self._last_mod_time_rx.search(txt_path.read_text("utf8"))

        if match:
            return parse(match.groups()[0])

        return datetime.min
