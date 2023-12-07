import pytest
from hotpdf import HotPdf
from hotpdf.utils import get_element_dimension


@pytest.fixture
def valid_file_name():
    return "tests/resources/PDF.pdf"


@pytest.fixture
def blank_file_name():
    return "tests/resources/blank.pdf"


@pytest.fixture
def non_existent_file_name():
    return "non_existent_file.pdf"


def test_load(valid_file_name):
    hot_pdf_object = HotPdf(height=1170, width=827)
    hot_pdf_object.load(valid_file_name)


def test_full_text(valid_file_name):
    hot_pdf_object = HotPdf(height=1170, width=827)
    hot_pdf_object.load(valid_file_name)
    pages = hot_pdf_object.pages
    # Not blank extraction
    assert len(pages[0].text()) > 1000


def test_pages_length(valid_file_name):
    hot_pdf_object = HotPdf(height=1170, width=827)
    hot_pdf_object.load(valid_file_name)
    pages = hot_pdf_object.pages
    assert len(pages) == 1


def test_pages_length(valid_file_name):
    hot_pdf_object = HotPdf(height=1170, width=827)
    hot_pdf_object.load(valid_file_name)
    pages = hot_pdf_object.pages
    assert len(pages) == 1


def test_extraction(valid_file_name):
    WORD = "DEGREE"
    hot_pdf_object = HotPdf(height=1170, width=827)
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

    hot_pdf_object = HotPdf(height=1170, width=827)
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
        hot_pdf_object = HotPdf(height=1170, width=827)
        hot_pdf_object.load(non_existent_file_name)


def test_double_loading(valid_file_name):
    hot_pdf_object = HotPdf(height=1170, width=827)
    hot_pdf_object.load(valid_file_name)
    with pytest.raises(Exception, match="A file is already loaded!"):
        hot_pdf_object.load(valid_file_name)


def test_blank_pdf(blank_file_name):
    hot_pdf_object = HotPdf(height=1170, width=827)
    hot_pdf_object.load(blank_file_name)
    pages = hot_pdf_object.pages
    assert all([len(page.text().strip("\n").strip()) == 0 for page in pages])


def test_row_index_out_of_range_memory_map(blank_file_name):
    hot_pdf_object = HotPdf(height=1170, width=827)
    hot_pdf_object.load(blank_file_name)
    pages = hot_pdf_object.pages
    with pytest.raises(IndexError, match="Specified index is out of range"):
        pages[0].memory_map.get(row_idx=9999, column_idx=100)


def test_col_index_out_of_range_memory_map(blank_file_name):
    hot_pdf_object = HotPdf(height=1170, width=827, precision=1)
    hot_pdf_object.load(blank_file_name)
    pages = hot_pdf_object.pages
    with pytest.raises(IndexError, match="Specified index is out of range"):
        pages[0].memory_map.get(row_idx=100, column_idx=9999)


# TODO: Implement Exceptions
@pytest.mark.skip("Not implemented yet")
def test_invalid_page_number(valid_file_name):
    hot_pdf_object = HotPdf(height=1170, width=827)
    hot_pdf_object.load(valid_file_name)

    with pytest.raises(ValueError, match="Invalid page number"):
        hot_pdf_object.find_text("Test", pages=[99])

    with pytest.raises(ValueError, match="Invalid page number"):
        hot_pdf_object.extract_text(x0=0, y0=1, x1=100, y1=5, page=99)


@pytest.mark.skip("Not implemented yet")
def test_extract_invalid_coordinates(valid_file_name):
    hot_pdf_object = HotPdf(height=1170, width=827)
    hot_pdf_object.load(valid_file_name)

    with pytest.raises(ValueError, match="Invalid coordinates"):
        hot_pdf_object.extract_text(x0=-5, y0=-5, x1=-5, y1=-5)
