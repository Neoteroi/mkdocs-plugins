import os
import pprint

import pkg_resources


def get_resource_file_path(file_name: str) -> str:
    return os.path.abspath(
        pkg_resources.resource_filename(__name__, os.path.join(".", "res", file_name))
    )


def get_resource_file_contents(file_name: str) -> str:
    with open(get_resource_file_path(file_name), "rt", encoding="utf8") as source_file:
        return source_file.read()


def collapse_str(value):
    return value.strip().replace("\n", "")


def equal_html(value1, value2):
    return collapse_str(value1) == collapse_str(value2)


def debug_pprint(data, file_name: str = "__file_out.py"):
    with open(file_name, "wt", encoding="utf8") as f:
        f.write(pprint.pformat(data, width=89))


def debug_write(text: str, file_name: str = "__file_out.html"):
    with open(file_name, "wt", encoding="utf8") as f:
        f.write(text)
