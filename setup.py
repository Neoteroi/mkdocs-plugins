from setuptools import setup


def readme():
    with open("README.md", mode="rt", encoding="utf8") as readme:
        return readme.read()


setup(
    name="neoteroi-mkdocs",
    version="0.0.1",
    description="Plugins for MkDocs",
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
    keywords="MkDocs OpenAPI Swagger Markdown plugin documentation",
    license="MIT",
    packages=["neoteroi.mkdocsoad"],
    install_requires=["essentials-openapi[full]", "mkdocs"],
    entry_points={
        "mkdocs.plugins": [
            "neoteroi.mkdocsoad = neoteroi.mkdocsoad:MkDocsOpenAPIDocumentationPlugin",
        ]
    },
    include_package_data=True,
    zip_safe=False,
)
