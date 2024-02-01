"""
This module provides controls for projects information.

neoteroi.projects

MIT License
Copyright (c) 2022 to present, Roberto Prevato
"""

from markdown import Extension

from .gantt import register_extension


class ProjectsExtension(Extension):
    config = {
        "priority": [12, "The priority to be configured for the extension."],
    }

    def extendMarkdown(self, md):
        md.registerExtension(self)
        register_extension(md, self.getConfig("priority"))
