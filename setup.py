#!/usr/bin/env python3

from pathlib import Path
from setuptools import setup

directory = Path(__file__).resolve().parent
with open(directory / "README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="hotpdf",
    version="0.3.0",
    author="Krishnasis Mandal",
    author_email="krishnasis.mandal@prestatech.com",
    license="MIT",
    description="Fast PDF Data Extraction library",
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
    extras_require={
        "linting": [
            "pylint",
            "mypy",
            "typing-extensions",
            "pre-commit",
            "ruff",
        ],
        "testing": [
            "pytest",
            "pytest-xdist",
            "coverage",
        ],
        "profiling": ["memray"],
    },
    include_package_data=True,
)
