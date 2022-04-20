import os

import pkg_resources


def get_resource_file_path(file_name: str) -> str:
    return pkg_resources.resource_filename(
        __name__, os.path.join(".", "res", file_name)
    )
