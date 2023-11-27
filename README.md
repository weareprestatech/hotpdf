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

## Usage

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
#### find_text (string)
Returns the occurences where the string was found in page wise. (dict[list])
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

#### extract_text(x0, y0, x1, y1)
Returns the text in given bbox span (str)
```python
# Extract text from bbox
hot_pdf.extract_text(x0=513, y0=760, x1=560, y1=766)
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
pages[0].text(save=True, filename='test.txt')