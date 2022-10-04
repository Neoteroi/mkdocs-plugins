from setuptools import setup


def readme():
    with open("README.md", mode="rt", encoding="utf8") as readme:
        return readme.read()


setup(
    name="neoteroi-mkdocs",
    version="0.1.2",
    description="Plugins for MkDocs and Python Markdown",
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/Neoteroi/mkdocs-plugins",
    author="RobertoPrevato",
    author_email="roberto.prevato@gmail.com",
    keywords="MkDocs OpenAPI Swagger Markdown plugins extensions documentation",
    license="MIT",
    packages=[
        "neoteroi.markdown",
        "neoteroi.markdown.data",
        "neoteroi.markdown.tables",
        "neoteroi.mkdocsoad",
        "neoteroi.contribs",
        "neoteroi.spantable",
        "neoteroi.timeline",
        "neoteroi.cards",
        "neoteroi.projects",
        "neoteroi.projects.gantt",
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
            "neoteroi.mkdocsoad = neoteroi.mkdocsoad:MkDocsOpenAPIDocumentationPlugin",
            "neoteroi.contribs = neoteroi.contribs:ContribsPlugin",
        ],
        "markdown.extensions": [
            "neoteroi.spantable = neoteroi.spantable:SpanTableExtension",
            "neoteroi.timeline = neoteroi.timeline:TimelineExtension",
            "neoteroi.cards = neoteroi.cards:CardsExtension",
            "neoteroi.projects = neoteroi.projects:ProjectsExtension",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
