![Build](https://github.com/Neoteroi/mkdocs-plugins/workflows/Build/badge.svg)
[![pypi](https://img.shields.io/pypi/v/neoteroi-mkdocs.svg)](https://pypi.python.org/pypi/neoteroi-mkdocs)
[![versions](https://img.shields.io/pypi/pyversions/neoteroi-mkdocs.svg)](https://github.com/neoteroi/mkdocs-plugins)
[![license](https://img.shields.io/github/license/neoteroi/mkdocs-plugins.svg)](https://github.com/neoteroi/mkdocs-plugins/blob/main/LICENSE)
[![codecov](https://codecov.io/gh/Neoteroi/mkdocs-plugins/branch/main/graph/badge.svg)](https://codecov.io/gh/Neoteroi/mkdocs-plugins)

# Plugins for MkDocs

```bash
pip install neoteroi-mkdocs
```

## MkDocsOAD

Plugin for MkDocs to generate human readable documentation from [OpenAPI
Documentation](https://swagger.io/specification/) **Version 3** (also known as
Swagger documentation).

How to use:

1. Install using `pip install neoteroi-mkdocs`
2. Configure this plugin in the MkDocs configuration file:

```yaml
plugins:
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

This plugin has been originally designed to generate Markdown that makes use of three
extensions from [PyMdown extensions](https://facelessuser.github.io/pymdown-extensions/).
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
  - neoteroi.mkdocsoad:
      use_pymdownx: true
```

Download a local copy of the provided `extra.css` file and configure it as extra
file in your MkDocs configuration:

```yaml
extra_css:
  - css/extra.css
```

### Supported sources for OpenAPI Documentation

| Source                         | Example                                                     |
| ------------------------------ | ----------------------------------------------------------- |
| YAML file                      | `[OAD(./docs/swagger.yaml)]`                                |
| JSON file                      | `[OAD(./docs/swagger.json)]`                                |
| URL returning YAML on HTTP GET | `[OAD(https://example-domain.net/swagger/v1/swagger.yaml)]` |
| URL returning JSON on HTTP GET | `[OAD(https://example-domain.net/swagger/v1/swagger.json)]` |

---

![Example result](https://gist.githubusercontent.com/RobertoPrevato/38a0598b515a2f7257c614938843b99b/raw/06e157c4f49e27a7e488d72d36d199194e28e952/oad-example-2.png)
