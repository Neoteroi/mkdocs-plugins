from setuptools import setup


def readme():
    with open("README.md", mode="rt", encoding="utf8") as readme:
        return readme.read()


setup(
    name="neoteroi-mkdocs",
    version="1.0.0",
    description="Plugins for MkDocs and Python Markdown",
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/Neoteroi/mkdocs-plugins",
    author="RobertoPrevato",
    author_email="roberto.prevato@gmail.com",
    keywords="MkDocs OpenAPI Swagger Markdown plugins extensions documentation",
    license="MIT",
    packages=[
        "neoteroi.mkdocs.markdown",
        "neoteroi.mkdocs.markdown.data",
        "neoteroi.mkdocs.markdown.tables",
        "neoteroi.mkdocs.oad",
        "neoteroi.mkdocs.contribs",
        "neoteroi.mkdocs.spantable",
        "neoteroi.mkdocs.timeline",
        "neoteroi.mkdocs.cards",
        "neoteroi.mkdocs.projects",
        "neoteroi.mkdocs.projects.gantt",
    ],
    install_requires=[
        "essentials-openapi",
        "mkdocs~=1.4.0",
        "httpx<1",
        "click~=8.0.3",
        "Jinja2~=3.0.2",
        "rich~=12.2.0",
    ],
    entry_points={
        "mkdocs.plugins": [
            "neoteroi.mkdocsoad = neoteroi.mkdocs.oad:MkDocsOpenAPIDocumentationPlugin",
            "neoteroi.contribs = neoteroi.mkdocs.contribs:ContribsPlugin",
        ],
        "markdown.extensions": [
            "neoteroi.spantable = neoteroi.mkdocs.spantable:SpanTableExtension",
            "neoteroi.timeline = neoteroi.mkdocs.timeline:TimelineExtension",
            "neoteroi.cards = neoteroi.mkdocs.cards:CardsExtension",
            "neoteroi.projects = neoteroi.mkdocs.projects:ProjectsExtension",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
