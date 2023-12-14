# hotpdf
Hot PDF

A faster alternative to libraries like pdfquery.

## Pre-requisites
1. hotpdf requires ghostscript to be installed, so please install that beforehand on your system.
Get it from [here](https://www.ghostscript.com/).

## Contributing
1. Type & Lint Checks: We use `mypy` to check for types and maintain the code quality. Please run mypy locally as well before pushing to prevent the lint pipeline from failing. We also use `flake8` to do some basic linting.
```bash
pipenv run mypy hotpdf/ --check-untyped-defs
pipenv run mypy tests/ --check-untyped-defs
pipenv run flake8 hotpdf/ --ignore=E501,W503
```
2. Test Coverage: We also check our test coverage and aim to reach > 90% coverage. We use the `coverage` library for this.
```
pipenv run coverage run --omit="*/test*" -m pytest tests/
pipenv run coverage report -m
```

<br>

# Usage

```python
# Import
from hotpdf import HotPdf
```

### Loading
Initialising a HotPdf object
```python
# width = width of PDF
# height = height of PDF
# precision = sets the precision of loading data into memory. Set a value within 0 to 1.
# Less precision amounts to more data extraction but takes up more memory and processing time.
hotpdf = HotPdf(width=827, height=1170, precision=0.5)

# Load the file into memory
hot_pdf.load("test.pdf")
```

### Operations
#### load(str)
Loads the file in memory.
Params
- file_name (str): Path of the file to load
- drop_duplicate_spans (bool) (Optional): Drop duplicate text spans while loading in memroy (default: True)
- first_page (int) (Optional): Page to start loading from. (Default: 0) If nothing is specified, whole file is loaded
- last_page (int) (Optional): Last page to be loaded. (Default: 0) If nothing is specified, whole file is loaded.

#### find_text (string)
Returns the occurences where the string was found in page wise. (dict[list])
    
Params:
- query (str): The text that you are trying to search for
- pages (list) (Optional): List of pages you want to search in
- validate (bool) (Optional): Double check if the text extracted is the text you want to fetch
- take_span (bool) (Optional): Extract the whole span that the text is a child of.
```python
# Find occurences of word in the pdf
occurences = hot_pdf.find_text("Auszahlungsbetrag")
"""
Example
{
    page_num: [
        [
            {co-ordinates of char1}, {co-ordinates of char2}, .....
        ]
    ]
}
"""
```
To find the total span of the word, take the 'x' & y value of the first character and the 'x_end' & 'y_end' values of the last character 

#### extract_text(x0, y0, x1, y1, page)
Returns the text in given bbox span (str)
```python
# Extract text from bbox
hot_pdf.extract_text(x0=513, y0=760, x1=560, y1=766, page=0)
```

#### extract_spans(x0, y0, x1, y1, page)
Returns the spans that lie within the specified coordinates. Returns a list of spans.
```python
# Extract text from bbox
hot_pdf.extract_spans(x0=513, y0=760, x1=560, y1=766, page=0)
```


### Anatomy

#### MemoryMap
A memory map is the internal 2D matrix representation of a PDF page. The x values and y values in the matrix are positioned according to the bbox position.

- ? So now, how does precision affect HotPdf?
    
    In case there is a clash of character bboxes, precision makes sure that there's extra positions to put the character in. So, lower = better, but more memory and processing power is required for lower precisions.

 
#### page (MemoryMap)
You can access a page by accessing the hotpdf.pages object
```python
pages = hot_pdf.pages[0]

# Number of pages
num_pages = len(pages)

# View the text
pages[0].text()

# Save the text to a file to debug
pages[0].display_memory_map(save=True, filename="output.txt")