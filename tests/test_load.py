import pytest
from hotpdf import HotPdf
from hotpdf.utils import get_element_dimension


@pytest.fixture
def file_name():
    return "tests/resources/PDF.pdf"


def test_load(file_name):
    hot_pdf_object = HotPdf(height=1170, width=827)
    hot_pdf_object.load(file_name)


def test_full_text(file_name):
    hot_pdf_object = HotPdf(height=1170, width=827)
    hot_pdf_object.load(file_name)
    pages = hot_pdf_object.pages
    # Not blank extraction
    assert len(pages[0].text()) > 1000


def test_pages_length(file_name):
    hot_pdf_object = HotPdf(height=1170, width=827)
    hot_pdf_object.load(file_name)
    pages = hot_pdf_object.pages
    assert len(pages) == 1


def test_pages_length(file_name):
    hot_pdf_object = HotPdf(height=1170, width=827)
    hot_pdf_object.load(file_name)
    pages = hot_pdf_object.pages
    assert len(pages) == 1


def test_test_extraction(file_name):
    WORD = "DEGREE"
    hot_pdf_object = HotPdf(height=1170, width=827)
    hot_pdf_object.load(file_name)
    occurences = hot_pdf_object.find_text(WORD)
    assert len(occurences) == 1
    for page_num, _ in occurences.items():
        assert page_num == 0

    element = get_element_dimension(occurences[0][0])
    extracted_text = hot_pdf_object.extract_text(
        x0=element["x0"],
        y0=element["y0"],
        x1=element["x1"],
        y1=element["y1"],
    )
    extracted_text = extracted_text.strip("\n").strip()
    assert extracted_text == WORD
