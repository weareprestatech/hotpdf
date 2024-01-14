from unittest.mock import patch

import pytest

from hotpdf import HotPdf
from hotpdf.data.classes import ElementDimension
from hotpdf.memory_map import MemoryMap
from hotpdf.utils import get_element_dimension


@pytest.fixture
def valid_file_name():
    return "tests/resources/PDF.pdf"


@pytest.fixture
def blank_file_name():
    return "tests/resources/blank.pdf"


@pytest.fixture
def multiple_pages_file_name():
    return "tests/resources/20pages.pdf"


@pytest.fixture
def non_existent_file_name():
    return "non_existent_file.pdf"


def test_load(valid_file_name):
    hot_pdf_object = HotPdf()
    hot_pdf_object.load(valid_file_name)


def test_full_text(valid_file_name):
    hot_pdf_object = HotPdf()
    hot_pdf_object.load(valid_file_name)
    pages = hot_pdf_object.pages
    # Not blank extraction
    assert len(pages[0].text()) > 1000


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
    assert extracted_text == WORD


def test_full_span_extraction(valid_file_name):
    WORD = "EXPERIENCE"
    # hotpdf should return the following span values
    FULL_SPAN_1 = "EXPERIENCE"
    FULL_SPAN_2 = "VOLUNTEER EXPERIENCE OR LEADERSHIP"

    hot_pdf_object = HotPdf()
    hot_pdf_object.load(valid_file_name)
    occurences = hot_pdf_object.find_text(WORD, take_span=True)

    # Only 1 page
    assert len(occurences) == 1
    # Should be page 0
    for page_num, _ in occurences.items():
        assert page_num == 0

    element_1 = get_element_dimension(occurences[0][0])
    element_2 = get_element_dimension(occurences[0][1])

    extracted_text_1 = hot_pdf_object.extract_text(
        x0=element_1.x0,
        y0=element_1.y0,
        x1=element_1.x1,
        y1=element_1.y1,
    )

    extracted_text_2 = hot_pdf_object.extract_text(
        x0=element_2.x0,
        y0=element_2.y0,
        x1=element_2.x1,
        y1=element_2.y1,
    )
    extracted_text_1 = extracted_text_1.strip("\n").strip()
    extracted_text_2 = extracted_text_2.strip("\n").strip()

    assert extracted_text_1 == FULL_SPAN_1
    assert extracted_text_2 == FULL_SPAN_2


def test_non_existent_file_path(non_existent_file_name):
    with pytest.raises(FileNotFoundError):
        hot_pdf_object = HotPdf()
        hot_pdf_object.load(non_existent_file_name)


def test_double_loading(valid_file_name):
    hot_pdf_object = HotPdf()
    hot_pdf_object.load(valid_file_name)
    with pytest.raises(Exception, match="A file is already loaded!"):
        hot_pdf_object.load(valid_file_name)


def test_blank_pdf(blank_file_name):
    hot_pdf_object = HotPdf()
    hot_pdf_object.load(blank_file_name)
    pages = hot_pdf_object.pages
    assert all([len(page.text().strip("\n").strip()) == 0 for page in pages])


def test_row_index_greater_than_rows_of_memory_map(valid_file_name):
    hot_pdf_object = HotPdf()
    hot_pdf_object.load(valid_file_name)
    pages = hot_pdf_object.pages
    pages[0].memory_map.get(row_idx=9999, column_idx=100) is not None
    assert pages[0].memory_map.get(row_idx=9999, column_idx=100) == ""


def test_col_index_greater_than_columns_of_memory_map(valid_file_name):
    hot_pdf_object = HotPdf()
    hot_pdf_object.load(valid_file_name)
    pages = hot_pdf_object.pages
    pages[0].memory_map.get(row_idx=100, column_idx=9999) is not None
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


def test_display_memory_map(valid_file_name):
    hot_pdf_object = HotPdf()
    hot_pdf_object.load(valid_file_name)
    pages = hot_pdf_object.pages
    pages[0].display_memory_map(save=False, filename="test.txt")


def test_get_spans(valid_file_name):
    INCOMPLETE_WORD = "EXPERIEN"
    NON_EXISTENT_WORD = "BLAH"
    # hotpdf should return the following span values
    FULL_SPAN_1 = "EXPERIENCE"
    FULL_SPAN_2 = "VOLUNTEER EXPERIENCE OR LEADERSHIP"

    hot_pdf_object = HotPdf()
    hot_pdf_object.load(valid_file_name)

    occurences = hot_pdf_object.find_text(INCOMPLETE_WORD)
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
            __full_spans_in_bbox_unsorted = hot_pdf_object.extract_spans(
                x0=element_dimension.x0,
                y0=element_dimension.y0,
                x1=element_dimension.x1,
                y1=element_dimension.y1 + 100,  # to simulate multi line extraction
                sort=False,
            )
            assert len(full_spans_in_bbox) == 1
            assert len(__full_spans_in_bbox_unsorted) > 1
            assert full_spans_in_bbox[0] in __full_spans_in_bbox_unsorted
            element_dimensions.append(get_element_dimension(full_spans_in_bbox[0]))

    span_1 = element_dimensions[0]
    span_2 = element_dimensions[1]

    text_1_extracted = hot_pdf_object.extract_text(x0=span_1.x0, y0=span_1.y0, x1=span_1.x1, y1=span_1.y1)
    text_2_extracted = hot_pdf_object.extract_text(x0=span_2.x0, y0=span_2.y0, x1=span_2.x1, y1=span_2.y1)
    assert text_1_extracted.strip("\n").strip() == FULL_SPAN_1, f"{text_1_extracted}, {FULL_SPAN_1}"
    assert text_2_extracted.strip("\n").strip() == FULL_SPAN_2, f"{text_2_extracted}, {FULL_SPAN_2}"

    # Test Non Existent Word
    occurences = hot_pdf_object.find_text(NON_EXISTENT_WORD)
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
            # Assert empty list returned
            assert full_spans_in_bbox == []


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


def test_no_spans_in_xml_file_extraction(valid_file_name):
    hot_pdf_object = HotPdf()
    with patch.object(MemoryMap, "_MemoryMap__get_page_spans") as get_page_spans:
        get_page_spans.return_value = None
        hot_pdf_object.load(valid_file_name)
        get_page_spans.assert_called_once()

        # No spans should be extracted
        spans = hot_pdf_object.extract_spans(0, 0, 1000, 1000)
        assert spans == []

        # Test extraction of word without span
        WORD = "DEGREE"
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
        assert extracted_text == WORD


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
