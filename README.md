[![Test CI](https://github.com/weareprestatech/hotpdf/actions/workflows/python-app.yml/badge.svg)](https://github.com/weareprestatech/hotpdf/actions/workflows/python-app.yml)

# hotpdf

This project was started as an internal project @ [Prestatech](http://prestatech.com/) to parse PDF files in a fast and memory efficient way to overcome the difficulties we were having while parsing big PDF files using libraries such as [pdfquery](https://github.com/jcushman/pdfquery).

hotpdf can be used to find and extract text from PDFs.

[Read the docs](https://stdocs.z6.web.core.windows.net/hotpdf/index.html)

### Pre-requisites

1. **Ghostscript Installation:**
   hotpdf requires Ghostscript to be installed. Please install it on your system.

   [Download Ghostscript](https://www.ghostscript.com/).

### Contributing

1. **Type & Lint Checks:**
   - Use `mypy` to check for types and maintain code quality.
   - Run mypy locally before pushing to prevent lint pipeline failures.
   - hotpdf/ folder should have **strict** mypy type checking
   - Use `flake8` for basic linting.

    ```bash
    pipenv run mypy hotpdf/ --check-untyped-defs --strict
    pipenv run mypy tests/ --check-untyped-defs
    pipenv run flake8 hotpdf/ --ignore=E501,W503
    ```

2. **Test Coverage:**
   - Check test coverage with the `coverage` library.
   - Aim for 100% test coverage.

    ```bash
    pipenv run coverage run --omit="*/test*" -m pytest tests/
    pipenv run coverage report -m --fail-under=100 -m
    ```

## Usage
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
text_occurences = hotpdf_document.find_text("word")

# Find text and its full span
text_occurences_full_span = hotpdf_document.find_text("word", take_span=True)

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

## Comprehensive Documentation

`hotpdf` is comprehensively documented within code for easy understanding. You can use any tool to view the documentation.
You can use an inbuilt tool like `pydoc` to view the documentation.

However we can also generate a better looking documentation using tools like [pdoc3](https://pypi.org/project/pdoc3/).

### View documentation

``` bash
pipenv run python -m pdoc --http localhost:8081 hotpdf/
```

This will start the documentation server on `localhost:8081`

[View documentation](https://stdocs.z6.web.core.windows.net/hotpdf/index.html)


## License
This project is licensed under the terms of the MIT license.

---
with ❤️ from the team @ [Prestatech GmbH](https://prestatech.com/)