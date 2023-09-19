import fitz
from fitz import Document, Page


def get_document_xml(file_path: str) -> list[str]:
    """
    Extracts XML representation of text content from a PDF document.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        list[str]: A list of XML strings, one for each page in the PDF.
    """
    pages = []
    with open(file_path, "rb") as file:
        doc: Document = fitz.open(stream=file.read(), filetype="pdf")
        for page in doc:
            pages.append(page.get_text("xml"))
    return pages
