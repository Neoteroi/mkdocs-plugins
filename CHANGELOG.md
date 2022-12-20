# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2022-12-20
- Adds the possibility to specify a `class` for the root HTML element of `cards`.
- Fixes a bug in the `contribs` plugin (adds a carriage return before the
  contribution fragment).
- Modifies the packages to group all extensions under `neoteroi.mkdocs` namespace.
- Replaces `setup.py` with `pyproject.toml`.

## [0.1.2] - 2022-10-04
- Corrects the pattern handling name and email for the `contribs` plugin.
- Adds tests for the `contribs` plugin.

## [0.1.1] - 2022-10-04
- Corrects bug in the `contribs` plugin, causing failures in certain CI/CD
  solutions and improves its safety and performance (removes `shell=True`!).
- Adds option to apply a class to specific contributors, for simpler styling.
- Minor improvements to styles.

## [0.0.9] - 2022-10-02
- Improves the `contributors` plugin:
- - Adds the possibility to exclude contributor information (for example to not display
    contributions from bots)
- - Adds the possibility to merge contributors' information
    for cases in which the same person commits using two different email addresses
- - Adds the possibility to display an element with the count of contributors
- Resolves a small issue in pip package resolution

## [0.0.8] - 2022-10-01
- Improves the Gantt extension:
- - now supports multiple periods in the same row
- - now supports activities using the start date from the previous activity (automatic dates)
- Adds a contributors plugin (`neoteroi.contribs`) to display contributors'
  information in each page, obtaining information from the Git repository at
  build time :star:

## [0.0.6] - 2022-08-11 :gem:
- Adds common classes to enable custom extensions reading configuration from:
- - YAML, JSON, or CSV embedded in the markdown source
- - YAML, JSON, or CSV fetched from a URL at build time (simple HTTP GET), with the
    option to define a custom fetcher for example for use cases that require
    authentication
- Adds the `Cards` extension, to render cards
- Adds the `Timeline` extension, to render timelines
- Adds the `Projects` extension, with a control to render `Gantt` diagrams :sparkles:
- Adds the link to the [documentation site](https://www.neoteroi.dev/mkdocs-plugins/)
- Drops support for Python 3.7 in the build pipeline (code might still work but is not ensured)

## [0.0.5] - 2022-05-08 :spades:
- Adds support for OAD specification organized in different files
  (fix https://github.com/Neoteroi/mkdocs-plugins/issues/5)
- Improves `mkdocsoad.css`

## [0.0.4] - 2022-05-04 :pill:
- Fixes a bug in `setup.py` (#4)
- Fixes entry_points related but (#7)

## [0.0.2] - 2022-05-01 :cake:

- Publishes the first extension for Python Markdown of the repository:
  `spantable`, custom Markdown table with support for `colspan` and `rowspan`
- Improves the support for Material for MkDocs themes in `mkdocsoad`

## [0.0.1] - 2022-04-20 :sparkles:

- First release with plugin for OpenAPI Documentation
