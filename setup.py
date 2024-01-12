# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from pathlib import Path
from pipenv_setup import pipfile_parser as parser

# Setup Pipfile parsing
project_dir = Path(__file__).parent
pipfile_path = project_dir.joinpath("Pipfile")
_, remote_packages = parser.get_default_packages(pipfile_path)
install_requires = [
    parser.format_remote_package(k, v)[1] for k, v in remote_packages.items()
]

version = "x.x"
with open("VERSION", "r") as version_file:
    version = str(version_file.read())

setup(
    name="hotpdf",
    version=version,
    author="Krishnasis Mandal",
    author_email="krishnasis.mandal@prestatech.com",
    packages=find_packages(exclude=("tests",)),
    url="https://dev.azure.com/prestacap/Prestatech-General/_git/hotpdf",
    license="MIT",
    description="Fast PDF Data Extraction library",
    keywords="",
    long_description=open("README.md").read(),
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3.11",
    ],
)
