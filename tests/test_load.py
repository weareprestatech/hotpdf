import os
from unittest.mock import patch

import pytest
from pdfminer.pdfdocument import PDFPasswordIncorrect
from pdfminer.pdfparser import PDFSyntaxError

from hotpdf import HotPdf
from hotpdf.data.classes import ElementDimension
from hotpdf.memory_map import MemoryMap
from hotpdf.utils import get_element_dimension


def test_load(valid_file_name):
    hot_pdf_object = HotPdf()
    hot_pdf_object.load(valid_file_name)


def test_load_constructor(valid_file_name):
    hotpdf_obj = HotPdf(valid_file_name)
    assert len(hotpdf_obj.pages) > 0


def test_load_bytes(valid_file_name):
    with open(valid_file_name, "rb") as f:
        hot_pdf_object = HotPdf()
        hot_pdf_object.load(f)


def test_load_locked(locked_file_name):
    hot_pdf_object = HotPdf()
    hot_pdf_object.load(locked_file_name, password="hotpdfiscool")
    page = hot_pdf_object.extract_page_text(page=0)
    assert len(page) > 500


def test_load_locked_bytes(locked_file_name):
    hot_pdf_object = HotPdf()
    with open(locked_file_name, "rb") as f:
        hot_pdf_object.load(f, password="hotpdfiscool")
    page = hot_pdf_object.extract_page_text(page=0)
    assert len(page) > 500


def test_load_locked_wrong_psw(locked_file_name):
    hot_pdf_object = HotPdf()
    with pytest.raises(PDFPasswordIncorrect):
        hot_pdf_object.load(locked_file_name, password="defenitelythewrongpassword")


def test_load_locked_wrong_psw_bytes(locked_file_name):
    hot_pdf_object = HotPdf()
    with open(locked_file_name, "rb") as f, pytest.raises(PDFPasswordIncorrect):
        hot_pdf_object.load(f, password="defenitelythewrongpassword")


def test_load_locked_no_psw(locked_file_name):
    hot_pdf_object = HotPdf()
    with pytest.raises(PDFPasswordIncorrect):
        hot_pdf_object.load(locked_file_name)


def test_load_locked_no_psw_bytes(locked_file_name):
    hot_pdf_object = HotPdf()
    with open(locked_file_name, "rb") as f, pytest.raises(PDFPasswordIncorrect):
        hot_pdf_object.load(f)


def test_load_invalid(invalid_file_name):
    with pytest.raises(PDFSyntaxError):
        HotPdf(invalid_file_name)


def test_full_text(valid_file_name):
    hot_pdf_object = HotPdf()
    hot_pdf_object.load(valid_file_name)
    text_first_page = hot_pdf_object.extract_page_text(page=0)
    # Not blank extraction
    assert len(text_first_page) > 500


def test_full_text_bytes(valid_file_name):
    with open(valid_file_name, "rb") as f:
        hot_pdf_object = HotPdf()
        hot_pdf_object.load(f)
        text_first_page = hot_pdf_object.extract_page_text(page=0)
        # Not blank extraction
        assert len(text_first_page) > 500


def test_pages_length(valid_file_name):
    hot_pdf_object = HotPdf()
    hot_pdf_object.load(valid_file_name)
    pages = hot_pdf_object.pages
    assert len(pages) == 1


def test_extraction(valid_file_name):
    WORD = "DEGREE"
    hot_pdf_object = HotPdf()
    hot_pdf_object.load(valid_file_name)
    occurences = hot_pdf_object.find_text(WORD)
    assert len(occurences) == 1
    for page_num, _ in occurences.items():
        assert page_num == 0

    element = get_element_dimension(occurences[0][0])
    extracted_text = hot_pdf_object.extract_text(
        x0=element.x0,
        y0=element.y0,
        x1=element.x1,
        y1=element.y1,
    )
    extracted_text = extracted_text.strip("\n").strip()
    assert WORD in extracted_text


def test_full_span_extraction(valid_file_name):
    WORD = "EXPERIENCE"

    to_check = {
        "EXPERIENCE ": False,
        "VOLUNTEER EXPERIENCE OR LEADERSHIP": False,
    }

    hot_pdf_object = HotPdf()
    hot_pdf_object.load(valid_file_name)
    occurences = hot_pdf_object.find_text(WORD, take_span=True)

    # Only 1 page
    assert len(occurences) == 1
    # Should be page 0
    for page_num, _ in occurences.items():
        assert page_num == 0

    for occurence in occurences[0]:
        dimension = get_element_dimension(occurence)
        text_extracted = hot_pdf_object.extract_text(
            x0=dimension.x0,
            y0=dimension.y0,
            x1=dimension.x1,
            y1=dimension.y1,
        )
        if text_extracted in to_check:
            to_check[text_extracted] = True
    assert all([to_check.values()])


def test_full_span_extraction_sorted(valid_file_name):
    WORD = "EXPERIENCE"

    checks = [
        "EXPERIENCE",
        "VOLUNTEER EXPERIENCE OR LEADERSHIP",
    ]

    hot_pdf_object = HotPdf()
    hot_pdf_object.load(valid_file_name)
    occurences = hot_pdf_object.find_text(WORD, take_span=True, sort=True)

    # Only 1 page
    assert len(occurences) == 1
    # Should be page 0
    for page_num, _ in occurences.items():
        assert page_num == 0
    for i in range(len(checks)):
        occurence = occurences[0][i]
        dimension = get_element_dimension(occurence)
        text_extracted = hot_pdf_object.extract_text(
            x0=dimension.x0,
            y0=dimension.y0,
            x1=dimension.x1,
            y1=dimension.y1,
        )
        text_extracted = text_extracted.strip("\n").strip()
        assert text_extracted == checks[i]


def test_non_existent_file_path(non_existent_file_name):
    with pytest.raises(FileNotFoundError):
        hot_pdf_object = HotPdf()
        hot_pdf_object.load(non_existent_file_name)


def test_blank_pdf(blank_file_name):
    hot_pdf_object = HotPdf()
    hot_pdf_object.load(blank_file_name)
    len_pages = len(hot_pdf_object.pages)
    assert all([len(hot_pdf_object.extract_page_text(page=i).strip("\n").strip()) == 0 for i in range(len_pages)])


def test_row_index_greater_than_rows_of_memory_map(valid_file_name):
    hot_pdf_object = HotPdf()
    hot_pdf_object.load(valid_file_name)
    pages = hot_pdf_object.pages
    assert pages[0].memory_map.get(row_idx=9999, column_idx=100) is not None
    assert pages[0].memory_map.get(row_idx=9999, column_idx=100) == ""


def test_col_index_greater_than_columns_of_memory_map(valid_file_name):
    hot_pdf_object = HotPdf()
    hot_pdf_object.load(valid_file_name)
    pages = hot_pdf_object.pages
    assert pages[0].memory_map.get(row_idx=100, column_idx=9999) is not None
    assert pages[0].memory_map.get(row_idx=100, column_idx=9999) == ""


@pytest.mark.parametrize("page", [-1, -2, 99])
def test_invalid_page_number(valid_file_name, page):
    hot_pdf_object = HotPdf()
    hot_pdf_object.load(valid_file_name)

    with pytest.raises(ValueError, match="Invalid page number"):
        hot_pdf_object.find_text("Test", pages=[page])

    with pytest.raises(ValueError, match="Invalid page number"):
        hot_pdf_object.extract_text(x0=0, y0=1, x1=100, y1=5, page=page)


@pytest.mark.parametrize(
    "coordinates",
    [
        [-1, 0, 0, 0],
        [0, -1, 0, 0],
        [0, 0, -1, 0],
        [0, 0, 0, -1],
    ],
)
def test_extract_invalid_coordinates(valid_file_name, coordinates):
    hot_pdf_object = HotPdf()
    hot_pdf_object.load(valid_file_name)

    with pytest.raises(ValueError, match="Invalid coordinates"):
        hot_pdf_object.extract_text(x0=coordinates[0], y0=coordinates[1], x1=coordinates[2], y1=coordinates[3])


def test_get_spans(valid_file_name):
    INCOMPLETE_WORD = "EXPERIENCE"
    NON_EXISTENT_WORD = "BLAH"
    # hotpdf should return the following span values

    to_check = {
        "EXPERIENCE ": False,
        "VOLUNTEER EXPERIENCE OR LEADERSHIP": False,
    }
    hot_pdf_object = HotPdf()
    hot_pdf_object.load(valid_file_name)

    occurences = hot_pdf_object.find_text(INCOMPLETE_WORD, take_span=True)
    element_dimensions: list[ElementDimension] = []
    for _, page_num in enumerate(occurences):
        occurences_by_page = occurences[page_num]
        for occurence_by_page in occurences_by_page:
            element_dimension = get_element_dimension(occurence_by_page)
            full_spans_in_bbox = hot_pdf_object.extract_spans(
                x0=element_dimension.x0,
                y0=element_dimension.y0,
                x1=element_dimension.x1,
                y1=element_dimension.y1,
            )
            assert len(full_spans_in_bbox) == 1
            element_dimensions.append(full_spans_in_bbox[0].get_element_dimension())

    for span_dim in element_dimensions:
        text_extracted = hot_pdf_object.extract_text(x0=span_dim.x0, y0=span_dim.y0, x1=span_dim.x1, y1=span_dim.y1)
        if text_extracted in to_check:
            to_check[text_extracted] = True

    assert all([to_check.values()])

    # Test Non Existent Word
    occurences = hot_pdf_object.find_text(NON_EXISTENT_WORD)
    assert occurences == {0: []}


@pytest.mark.parametrize("first_page, last_page", [(1, 1), (1, 2)])
def test_extract_page_range(multiple_pages_file_name, first_page, last_page):
    hot_pdf_object = HotPdf()
    hot_pdf_object.load(multiple_pages_file_name, first_page=first_page, last_page=last_page)
    pages = hot_pdf_object.pages
    assert len(pages) == last_page - first_page + 1


@pytest.mark.parametrize("first_page, last_page", [(-1, 1), (20, 10)])
def test_extract_page_range_exception(multiple_pages_file_name, first_page, last_page):
    hot_pdf_object = HotPdf()
    with pytest.raises(ValueError, match="Invalid page range"):
        hot_pdf_object.load(multiple_pages_file_name, first_page=first_page, last_page=last_page)


def test_no_spans_in_xml_file_extract_spans(valid_file_name):
    hot_pdf_object = HotPdf()
    with patch.object(MemoryMap, "_MemoryMap__get_page_spans") as get_page_spans:
        hot_pdf_object.load(valid_file_name)
        get_page_spans.return_value = None
        # Test No spans
        assert (
            hot_pdf_object.extract_spans(
                x0=0,
                y0=0,
                x1=100,
                y1=100,
            )
            == []
        )


def test_find_text_multiple_pages(multiple_pages_file_name):
    hot_pdf_object = HotPdf()
    hot_pdf_object.load(multiple_pages_file_name)
    occurences = hot_pdf_object.find_text(query="God", pages=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    assert len(occurences) == 11


def test_find_spans_unique(valid_file_name):
    hot_pdf_object = HotPdf(valid_file_name)
    occurences = hot_pdf_object.find_text("EXPERIENCE")
    assert len(occurences[0]) == 2


def test_extract_spans(valid_file_name):
    hot_pdf_object = HotPdf()
    hot_pdf_object.load(valid_file_name)
    spans = hot_pdf_object.extract_spans(0, 0, 1000, 1000)
    to_check = {
        "PDF ": False,
        "THE BEST PDF PARSING LIBRARY TO EVER EXIST(DEBATABLE) ": False,
        "HOTPDF ": False,
    }
    all_text: str = ""
    for span in spans:
        span_text: str = span.to_text()
        if span_text in to_check:
            to_check[span_text] = True
        all_text += span_text
    assert all(to_check.values()), "Not all spans were extracted"
    assert len(all_text) == 608 if os.name == "nt" else 728


def test_span_has_no_characters(valid_file_name):
    hot_pdf_object = HotPdf()
    hot_pdf_object.load(valid_file_name)
    spans = hot_pdf_object.extract_spans(0, 0, 1000, 1000)
    span_1 = spans[0]
    assert span_1.get_element_dimension()
    span_1.characters = None
    with pytest.raises(ValueError, match="Span has no characters"):
        span_1.get_element_dimension()


def test_extract_spans_text(valid_file_name):
    hot_pdf_object = HotPdf()
    hot_pdf_object.load(valid_file_name)
    text = hot_pdf_object.extract_spans_text(0, 0, 1000, 1000)

    assert len(text) == 608 if os.name == "nt" else 728


def test_CONSISTENCY(valid_file_name):
    hot_pdf_object = HotPdf()
    hot_pdf_object.load(valid_file_name)
    page_text = hot_pdf_object.extract_page_text(0)
    bbox_text = hot_pdf_object.extract_text(0, 0, 1000, 1000)
    assert page_text == bbox_text


def test_load_pages_defined(multiple_pages_file_name):
    hotpdf_object = HotPdf()
    hotpdf_object.load(multiple_pages_file_name, first_page=1, last_page=1)
    assert len(hotpdf_object.pages) == 1

    hotpdf_object_1 = HotPdf(multiple_pages_file_name, first_page=1, last_page=3)
    assert len(hotpdf_object_1.pages) == 3
