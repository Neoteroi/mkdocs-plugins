"""
This module provide a plugin that can be used to generate Markdown
from OpenAPI Documentation files, using essentials-openapi

    https://github.com/Neoteroi/essentials-openapi

The markdown requires by default

neoteroi.mkdocs.oad
"""

import re

from mkdocs.config.config_options import Type
from mkdocs.plugins import BasePlugin
from openapidocs.mk.v3 import OpenAPIV3DocumentationHandler
from openapidocs.utils.source import read_from_source


class MkDocsOpenAPIDocumentationPlugin(BasePlugin):
    config_scheme = (("use_pymdownx", Type(bool, default=False)),)

    rx = re.compile(r"\[OAD\(([^\)]+)\)\]")

    def _get_style(self) -> str:
        return "MKDOCS" if self.config.get("use_pymdownx", False) else "MARKDOWN"

    def _replacer(self, match) -> str:
        source = match.group(1).strip("'\"")
        data = read_from_source(source)

        handler = OpenAPIV3DocumentationHandler(
            data, style=self._get_style(), source=source
        )
        return handler.write()

    def on_page_markdown(self, markdown, *args, **kwargs):
        """
        Replaces the tag [OAD(...)] in markdown with markdown generated from an
        OpenAPI Documentation, using essentials-openapi

        https://github.com/Neoteroi/essentials-openapi
        """
        if "[OAD(" in markdown:
            return self.rx.sub(self._replacer, markdown)
        return markdown
