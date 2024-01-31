# hotpdf

[![Documentation Status](https://readthedocs.org/projects/hotpdf/badge/?version=latest)](https://hotpdf.readthedocs.io/en/latest/?badge=latest)
[![latest](https://github.com/weareprestatech/hotpdf/actions/workflows/python-publish.yml/badge.svg)](https://github.com/weareprestatech/hotpdf/actions/workflows/python-publish.yml)
[![build](https://github.com/weareprestatech/hotpdf/actions/workflows/build-badge.yml/badge.svg)](https://github.com/weareprestatech/hotpdf/actions/workflows/build-badge.yml)
[![Coverage Status](https://coveralls.io/repos/github/weareprestatech/hotpdf/badge.svg?branch=main)](https://coveralls.io/github/weareprestatech/hotpdf?branch=main)


This project was started as an internal project @ [Prestatech](http://prestatech.com/) to parse PDF files in a fast and memory efficient way to overcome the difficulties we were having while parsing big PDF files using libraries such as [pdfquery](https://github.com/jcushman/pdfquery).

hotpdf is a wrapper around [pdfminer.six](https://github.com/pdfminer/pdfminer.six) focusing on text extraction and text search operations on PDFs.

hotpdf can be used to find and extract text from PDFs.
Please [read the docs](https://hotpdf.readthedocs.io/en/latest/) to understand how the library can help you!

## Installation

The latest version of hotpdf can be installed directly from [PyPI](https://pypi.org/project/hotpdf/) with pip.

```bash
pip install hotpdf
```

## Local Setup

First install the dependencies required by hotpdf

```bash
python3 -m pip install -e .
```

### Contributing

You should install the [pre-commit](https://github.com/weareprestatech/hotpdf/blob/main/.pre-commit-config.yaml) hooks with `pre-commit install`. This will run the linter, mypy, and ruff formatting before each commit.

Rembember to run `pip install -e '.[dev]'` to install the extra dependencies for development.

For more examples of how to run the full test suite please refer to the [CI workflow](https://github.com/weareprestatech/hotpdf/blob/main/.github/workflows/test.yml).

We strive to keep the test coverage at 100%: if you want your contributions accepted please write tests for them :D

Some examples of running tests locally:

```bash
python3 -m pip install -e '.[dev]'               # install extra deps for testing
python3 -m pytest -n=auto tests/                      # run the test suite
# run tests with coverage
python3 -m pytest --cov-fail-under=98 -n=auto --cov=hotpdf --cov-report term-missing
```

### Documentation

We use [sphinx](https://www.sphinx-doc.org/en/master/) for generating our docs and host them on [readthedocs](https://readthedocs.org/)

Please update and add documentation if required, with your contributions.

Update the `.rst` files, rebuild them, and commit them along with your PRs.

```bash
cd docs
make clean
make html
```

This will generate the necessary documentation files. Once merged to `main` the docs will be updated automatically.

## Usage

**To view more detailed usage information, please [read the docs](https://hotpdf.readthedocs.io/en/latest/)**

Basic usage is as follows:

```python

from hotpdf import HotPdf

pdf_file_path = "test.pdf"

# Load pdf file into memory
hotpdf_document = HotPdf(pdf_file_path)

# Alternatively, you can also pass an opened pdf stream to be loaded
with open(pdf_file_path, "rb") as f:
   hotpdf_document_2 = HotPdf(f)

# Get number of pages
print(len(hotpdf_document.pages))

# Find text
text_occurences = hotpdf_document.find_text("foo")

# Find text and its full span
text_occurences_full_span = hotpdf_document.find_text("foo", take_span=True)

# Extract text in region
text_in_bbox = hotpdf_document.extract_text(
   x0=0,
   y0=0,
   x1=100,
   y1=10,
   page=0,
)

# Extract spans in region
spans_in_bbox = hotpdf_document.extract_spans(
   x0=0,
   y0=0,
   x1=100,
   y1=10,
   page=0,
)

# Extract spans text in region
spans_text_in_bbox = hotpdf_document.extract_spans_text(
   x0=0,
   y0=0,
   x1=100,
   y1=10,
   page=0,
)

# Extract full page text
full_page_text = hotpdf_document.extract_page_text(page=0)
```

## License

This project is licensed under the terms of the MIT license.

---
with ❤️ from the team @ [Prestatech GmbH](https://prestatech.com/)
