from setuptools import setup


def readme():
    with open("README.md", mode="rt", encoding="utf8") as readme:
        return readme.read()


setup(
    name="neoteroi-mkdocs",
    version="0.0.6",
    description="Plugins for MkDocs and Python Markdown",
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
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
        "neoteroi.spantable",
        "neoteroi.timeline",
        "neoteroi.cards",
        "neoteroi.projects",
        "neoteroi.projects.gantt",
    ],
    install_requires=["essentials-openapi[full]", "mkdocs~=1.3.1", "httpx~=0.22.0"],
    entry_points={
        "mkdocs.plugins": [
            "neoteroi.mkdocsoad = neoteroi.mkdocsoad:MkDocsOpenAPIDocumentationPlugin",
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
