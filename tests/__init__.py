import os
import pprint

import pkg_resources


def get_resource_file_path(file_name: str) -> str:
    return os.path.abspath(
        pkg_resources.resource_filename(__name__, os.path.join(".", "res", file_name))
    )


def collapse_str(value):
    return value.strip().replace("\n", "")


def equal_html(value1, value2):
    return collapse_str(value1) == collapse_str(value2)


def debug_pprint(data, file_name: str = "__file_out.py"):
    with open(file_name, "wt", encoding="utf8") as f:
        f.write(pprint.pformat(data, width=89))
