# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.3] 2025-07-30

- Improve `read_from_source()` to support an optional CWD parameter used to
  look for the OpenAPI spec. The OpenAPI plugin should supply that CWD relative
  to the current markdown file being processed. Markdown customarily uses
  paths relative to the document itself. Existing relative paths will not break,
  since this will attempt paths relative to both working directories, by
  @joewlambeth.

## [1.1.2] 2025-04-22

- Correct the contribs plugin to use the `--follow` option when obtaining
  contributors' information.

## [1.1.1] 2025-04-18 🌵

- Improve the `contribs` plugin to not pollute the logs with
  `dateutil.parser.ParseError` while working on a new file that is not
  committed in Git, yet.
- Add the possibility to enable and disable the `contribs` plugin by env
  variable, through plugin configuration. To use, specify the following
  setting:

```yaml
  - neoteroi.contribs:
      enabled_by_env: "GIT_CONTRIBS_ON"  # Use the name you wish here for the env var
```

- When `enabled_by_env` is not empty, the Git contributors plugin is only
  enabled if such variable exists and its value is a value in `{"1", "true"}`
  (case insensitive). This is useful to disable the plugin by default during
  local development, and enable it only during an automated build that builds
  the documentation for publishing. The rationale for this setting is that
  this plugin has an heavy impact on the build performance as it uses the Git
  CLI to obtain the list of contributors who worked on each page.
- Remove Python 3.8 from the build matrix, add 3.13.

## [1.1.0] 2024-08-10 🐢

- Improve the `cards` plugin to automatically use cards' titles for the `alt`
  property of their images, when `alt` is not specified.
  See [#63](https://github.com/Neoteroi/mkdocs-plugins/issues/63), reported by
  @Valerie-ts.

## [1.0.5] 2024-02-01 :mage:

- Show event description in Gantt diagrams, by @changbowen
- Add possibility to configure months time format in Gantt diagrams, by @yasamoka

## 2023-12-24

- Adds support for running tests using Python 3.12, and adds Python 3.12 to the
  build matrix. Note: only tests code did not support Python 3.12 because it
  used `pkg_resources`.

## [1.0.4] - 2023-07-28 :parasol_on_ground:

- Unpins the dependencies on `mkdocs` and `httpx`, to fix
  [#42](https://github.com/Neoteroi/mkdocs-plugins/issues/42).

## [1.0.3] - 2023-07-18 :cat:

- Adds support for icons in cards (by @Andy2003).
- Adds support for anchors with target="_blank" in cards.

## [1.0.2] - 2023-04-25

- Fixes detail in the `contribs` plugin: when the name is specified for a
  contributor by email address, it is used.
- Improves `pyproject.toml`.
- Adds `py.typed` files.

## [1.0.1] - 2023-04-25
- Improves the `contribs` plugin, adding the possibility to document
  contributors for a page also using `.txt` files close to `.md` files. This
  can be useful in several cases:
- - To document contributors who worked outside of Git, for example when providing
    pictures for the page, or written content provided to someone who is
    adding content to the MkDocs site.
- - To document contributors following a Git history re-write
- Improves the `contribs` plugin, adding the possibility to exclude files by
  glob patterns (fix #33).
- Improves the `contribs` plugin, adding the possibility to merge contributors
  by name, for scenarios when the same person commits using different names
  (Git reports different contributors in such cases) and it is preferred
  displaying information aggregated as single contributor.

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
