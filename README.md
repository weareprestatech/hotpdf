# hotpdf
Hot PDF

A faster alternative to libraries like pdfquery.

## Usage

```python
# USAGE
from hotpdf import HotPdf

hot_pdf = HotPdf(width=827, height=1170, precision=0.5)
hot_pdf.load("test.pdf")

# Find occurences of text in PDF - page wise
occurences = hot_pdf.find_text("Balance")
for page_num, occurence in occurences.items():
    print(page_num, "::::", occurence)

# Extract text from specific coordinates
# x0, x1, y0, y1 (Natural coordinates)
# y spans from 0 to height instead of inverted like other libraries
print(memory_map.extract_text_from_bbox(306, 345, 531, 532))

```


Will update later.
