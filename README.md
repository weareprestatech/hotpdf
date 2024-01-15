[![Documentation Status](https://readthedocs.org/projects/hotpdf/badge/?version=latest)](https://hotpdf.readthedocs.io/en/latest/?badge=latest)


# hotpdf

This project was started as an internal project @ [Prestatech](http://prestatech.com/) to parse PDF files in a fast and memory efficient way to overcome the difficulties we were having while parsing big PDF files using libraries such as [pdfquery](https://github.com/jcushman/pdfquery).

hotpdf can be used to find and extract text from PDFs.
Please [read the docs](https://hotpdf.readthedocs.io/en/latest/) to understand how the library can help you!

### Pre-requisites

1. **Ghostscript Installation:**
   hotpdf requires Ghostscript to be installed. Please install it on your system.

   [Download Ghostscript](https://www.ghostscript.com/).

### Contributing

You should install the [pre-commit](https://github.com/weareprestatech/hotpdf/blob/main/.pre-commit-config.yaml) hooks with `pre-commit install`. This will run the linter, mypy, and a subset of the tests on every commit.

For more examples of how to run the full test suite please refer to the [CI workflow](https://github.com/weareprestatech/hotpdf/blob/main/.github/workflows/test.yml).

We strive to keep the test coverage at 100%: if you want your contributions accepted please write tests for them :D

Some examples of running tests locally:

```bash
python3 -m pip install -e '.[testing]'               # install extra deps for testing
python3 -m pytest -n=auto test/                      # run the test suite
```

## Usage

#### To view more detailed usage information, please [read the docs](https://hotpdf.readthedocs.io/en/latest/)


Basic usage is as follows:
```python
from hotpdf import HotPdf

pdf_file_path = "test.pdf"

# Load pdf file into memory
hotpdf_document = HotPdf()
hotpdf_document.load(pdf_file_path)

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

# Extract text spans in region
spans_in_bbox = hotpdf_document.extract_spans(
   x0=0,
   y0=0,
   x1=100,
   y1=10,
   page=0,
)
```
For more granular function level documentation please check the docs.

## License
This project is licensed under the terms of the MIT license.

---
with ❤️ from the team @ [Prestatech GmbH](https://prestatech.com/)
