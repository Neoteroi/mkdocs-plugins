import os

import pkg_resources


def get_resource_file_path(file_name: str) -> str:
    return os.path.abspath(
        pkg_resources.resource_filename(__name__, os.path.join(".", "res", file_name))
    )


def collapse_str(value):
    return value.strip().replace("\n", "")


def equal_html(value1, value2):
    return collapse_str(value1) == collapse_str(value2)
