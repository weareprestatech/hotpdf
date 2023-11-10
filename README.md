# hotpdf
Hot PDF

A faster alternative to libraries like pdfquery.

## Usage

```python
# USAGE
from hotpdf import HotPdf

hot_pdf = HotPdf(width=827, height=1170, precision=0.5)
hot_pdf.load("test.pdf")

# Display in plain text representation
print(hot_pdf.pages[0].text())

# Display span of found text
occurences = hot_pdf.find_text("Auszahlungsbetrag")
print(occurences)

# Extract text based on bbox coordinates.
# Natural calculations, not inverted like other libs
print(hot_pdf.extract_text(x0=513, y0=760, x1=560, y1=766))

# Save page as txt file
hot_pdf.pages[0].display_memory_map(save=True, filename='krish.txt')


```


Will update later.
