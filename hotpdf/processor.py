import fitz
from fitz import Document, Page


def get_document_xml(file_path: str) -> list[str]:
    pages = []
    with open(file_path, "rb") as file:
        doc: Document = fitz.open(stream=file.read(), filetype="pdf")
        page: Page
        for page in doc:
            pages.append(page.get_text("xml"))
    return pages
