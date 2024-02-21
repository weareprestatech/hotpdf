from hotpdf import HotPdf
from hotpdf.encodings.types import EncodingTypes

pdf_file_path = "test.pdf"

# Load pdf file into memory
hotpdf_document = HotPdf(pdf_file_path)

# Alternatively, you can also pass an opened pdf stream to be loaded
with open(pdf_file_path, "rb") as f:
    hotpdf_document_2 = HotPdf(f)

# Sometimes pdfminer will not replace (cid:x) values properly
# In that case pass EncodingTypes

hotpdf_cid_removal_object = HotPdf(f, cid_overwrite_charset=EncodingTypes.LATIN)

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
