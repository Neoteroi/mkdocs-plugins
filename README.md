![Build](https://github.com/Neoteroi/mkdocs-plugins/workflows/Build/badge.svg)
[![pypi](https://img.shields.io/pypi/v/neoteroi-mkdocs.svg)](https://pypi.python.org/pypi/neoteroi-mkdocs)
[![versions](https://img.shields.io/pypi/pyversions/neoteroi-mkdocs.svg)](https://github.com/neoteroi/mkdocs-plugins)
[![license](https://img.shields.io/github/license/neoteroi/mkdocs-plugins.svg)](https://github.com/neoteroi/mkdocs-plugins/blob/main/LICENSE)
[![codecov](https://codecov.io/gh/Neoteroi/mkdocs-plugins/branch/main/graph/badge.svg)](https://codecov.io/gh/Neoteroi/mkdocs-plugins)

# Plugins for MkDocs and Python Markdown

```bash
pip install neoteroi-mkdocs
```

This package includes the following plugins and extensions:

| Name                      | Description                                               | Type                       |
| :------------------------ | :-------------------------------------------------------- | :------------------------- |
| [`mkdocsoad`](#mkdocsoad) | Generates documentation from OpenAPI specification files. | MkDocs plugin.             |
| [`spantable`](#spantable) | Tables supporting colspan and rowspan.                    | Python Markdown extension. |

## MkDocsOAD

Plugin for MkDocs to generate human readable documentation from [OpenAPI
Documentation](https://swagger.io/specification/) **Version 3** (also known as
Swagger documentation).

How to use:

1. Install using `pip install neoteroi-mkdocs`
2. Configure this plugin in the MkDocs configuration file:

```yaml
plugins:
  - search
  - neoteroi.mkdocsoad
```

3. Configure a source in your Markdown file, for example having a `swagger.json`
   file in your `docs` folder:

```markdown
[OAD(./docs/swagger.json)]
```

The plugin fetches the contents from the OpenAPI Specification source,
generates Markdown using [essentials-openapi](https://github.com/Neoteroi/essentials-openapi),
then writes them in the markdown file.

Example result:

![Example result](https://gist.githubusercontent.com/RobertoPrevato/38a0598b515a2f7257c614938843b99b/raw/06e157c4f49e27a7e488d72d36d199194e28e952/oad-example-1.png)

### Recommended: enable PyMDown and extra CSS

This plugin was designed to generate Markdown for sites that use [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
and three extensions from [PyMdown extensions](https://facelessuser.github.io/pymdown-extensions/).
To achieve the best results, it is recommended to enable PyMdown extensions.

1. Install [PyMdown extensions](https://facelessuser.github.io/pymdown-extensions/)
   using `pip install pymdown-extensions`
2. Configure the following PyMdown markdown extensions in the MkDocs
   configuration file:

```yaml
markdown_extensions:
  - pymdownx.details
  - pymdownx.superfences
  - pymdownx.tabbed:
      alternate_style: true
```

Enable PyMdown integration this way:

```yaml
plugins:
  - search
  - neoteroi.mkdocsoad:
      use_pymdownx: true
```

Download a local copy of the provided [`mkdocsoad.css`
file](https://github.com/Neoteroi/mkdocs-plugins/blob/main/neoteroi/mkdocsoad/resources/mkdocsoad.css)
and configure it as extra file in your MkDocs configuration:

```yaml
extra_css:
  - css/mkdocsoad.css
```

### Supported sources for OpenAPI Documentation

| Source                         | Example                                                     |
| :----------------------------- | :---------------------------------------------------------- |
| YAML file                      | `[OAD(./docs/swagger.yaml)]`                                |
| JSON file                      | `[OAD(./docs/swagger.json)]`                                |
| URL returning YAML on HTTP GET | `[OAD(https://example-domain.net/swagger/v1/swagger.yaml)]` |
| URL returning JSON on HTTP GET | `[OAD(https://example-domain.net/swagger/v1/swagger.json)]` |

---

![Example result](https://gist.githubusercontent.com/RobertoPrevato/38a0598b515a2f7257c614938843b99b/raw/06e157c4f49e27a7e488d72d36d199194e28e952/oad-example-2.png)

## SpanTable

Extension for Python Markdown to support tables with `colspan` and `rowspan`,
including automatic handling of span value, support for captions, and table
classes.

How to use:

1. Configure the extension in the MkDocs configuration file:

```yaml
markdown_extensions:
  - neoteroi.spantable
```

2. Write a Markdown table like in the following example, use `@span`
   placeholders for automatic handling of colspan and rowspan depending on
   adjacent empty cells (separator lines are ignored):

```
::spantable:: caption="Offices by country" class="offices-by-country"

| Country      | Address                                                  |
| ------------ | -------------------------------------------------------- |
| France @span | 8 Rue St Ferréol - 92190 City: Meudon (Île-de-France)    |
|              | 50 boulevard Amiral Courbet - 94310 Orly (Île-de-France) |
|              | ...                                                      |
|              | ...                                                      |
| Italy @span  | Str. S. Maurizio, 12, 10072 Caselle torinese TO          |
|              | S.S. Torino-Asti - 10026 Santena (TO)                    |
|              | ...                                                      |
| Poland @span | al. Jana Pawła II 22, 00-133 Warszawa                    |
|              | plac Trzech Krzyży 4/6, 00-535 Warszawa                  |
|              | ...                                                      |
|              | ...                                                      |

::end-spantable::
```

Produces an output like the following:

![SpanTable example 1](https://gist.githubusercontent.com/RobertoPrevato/38a0598b515a2f7257c614938843b99b/raw/6df659decb605cf9d1f6166a8ae5cc6a0ba897bb/spantable-example-01b.png)

_Note: caption and class are not required._

### SpanTable options

| Option          | Description                                                                                                               |
| :-------------- | :------------------------------------------------------------------------------------------------------------------------ |
| @span           | Applies colspan and rowspan automatically to expand the cell to all adjacent cells (colspan has precedence over rowspan). |
| @span=x         | colspan=x                                                                                                                 |
| @span=x:y       | colspan=x; rowspan=y;                                                                                                     |
| @class="value"  | Adds an HTML _class_ to any cell, to simplify styling (optional).                                                         |
| caption="value" | Adds a _caption_ element with the given value to the table (optional).                                                    |
| class="value"   | Adds a _class_ to the _table_ element with the given value (optional).                                                    |

In the following example, the cells with `Italy` and `France` both get
`colspan="2" rowspan="3"` because they have empty adjacent cells growing one
column and two rows:

```
::spantable:: caption="Life Expectancy By Current Age" class="foo"

| Italy @span   |       | 40 @span      |       | 20 @span      |       |
| ------------- | ----- | ------------- | ----- | ------------- | ----- |
|               |       | Men           | Women | Men           | Women |
|               |       | 78            | 82    | 77            | 81    |
| Poland @span  |       | 40 @span      |       | 20 @span      |       |
| ------------- | ----- | ------------- | ----- | ------------- | ----- |
|               |       | Men           | Women | Men           | Women |
|               |       | 78            | 82    | 77            | 81    |

::end-spantable::
```

Produces an output like the following:

![SpanTable example 2](https://gist.githubusercontent.com/RobertoPrevato/38a0598b515a2f7257c614938843b99b/raw/6df659decb605cf9d1f6166a8ae5cc6a0ba897bb/spantable-example-02b.png)

### Styling

Download a local copy of the provided [`spantable.css`
file](https://github.com/Neoteroi/mkdocs-plugins/blob/main/neoteroi/spantable/resources/spantable.css)
and configure it as extra file in your MkDocs configuration:

```yaml
extra_css:
  - css/spantable.css
```
