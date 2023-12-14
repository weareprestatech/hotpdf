import pytest
from hotpdf import HotPdf
from hotpdf.utils import filter_adjacent_coords
from hotpdf.data.classes import HotCharacter
from hotpdf.sparse_matrix import SparseMatrix
import os


@pytest.fixture
def valid_file_name():
    return "tests/resources/PDF.pdf"


@pytest.fixture
def luca_mock_file_name():
    return "tests/resources/luca_mock.pdf"


def test_load_file(valid_file_name):
    hot_pdf_object = HotPdf(height=1170, width=827)
    hot_pdf_object.load(valid_file_name)


def test_element_dimensions_empty():
    assert filter_adjacent_coords("dummy", []) == []


def test_span_map_behaviours(valid_file_name):
    hot_pdf_object = HotPdf(height=1170, width=827)
    hot_pdf_object.load(valid_file_name)

    with pytest.raises(KeyError, match="Cannot set key as None"):
        hot_pdf_object.pages[0].span_map[None] = HotCharacter(
            value="c",
            x=0,
            y=0,
            x_end=10,
            span_id="x",
        )

    assert hot_pdf_object.pages[0].span_map["foo"] is None
    assert hot_pdf_object.pages[0].span_map.get_span("foo") is None
    assert hot_pdf_object.pages[0].span_map.get_span(None) is None


def test_memory_map_behaviour(valid_file_name):
    hot_pdf_object = HotPdf(height=1170, width=827)
    with pytest.raises(Exception, match="list index out of range"):
        hot_pdf_object.pages[0].text()
    hot_pdf_object.load(valid_file_name, drop_duplicate_spans=False)
    hot_pdf_object.pages[0].display_memory_map(save=True, filename="test.txt")
    assert os.path.exists("test.txt")
    os.remove("test.txt")


def test_sparse_matrix_insert_and_get():
    matrix = SparseMatrix(3, 3)
    matrix.insert("A", 0, 0)
    matrix.insert("B", 1, 1)
    matrix.insert("C", 2, 2)
    assert matrix.get(0, 0) == "A"
    assert matrix.get(1, 1) == "B"
    assert matrix.get(2, 2) == "C"

    # Test getting non-inserted values (should return empty string)
    assert matrix.get(0, 1) == ""
    assert matrix.get(1, 0) == ""
    assert matrix.get(2, 1) == ""


def test_sparse_matrix_getitem_and_setitem():
    matrix = SparseMatrix(3, 3)
    matrix[0, 0] = "A"
    matrix[1, 1] = "B"
    matrix[2, 2] = "C"
    assert matrix[0, 0] == "A"
    assert matrix[1, 1] == "B"
    assert matrix[2, 2] == "C"

    matrix[1, 1] = "D"
    assert matrix[1, 1] == "D"
    with pytest.raises(IndexError, match="Specified index is out of range"):
        matrix[-1, 0]
    with pytest.raises(IndexError):
        matrix[0, -1] = "Y"


def test_sparse_matrix_iterator():
    matrix = SparseMatrix(3, 3)
    matrix[0, 0] = "A"
    matrix[1, 1] = "B"
    matrix[2, 2] = "C"
    non_empty_values = list(matrix)
    expected_result = [((0, 0), "A"), ((1, 1), "B"), ((2, 2), "C")]
    assert non_empty_values == expected_result


def test_duplicate_spans_removed(luca_mock_file_name):
    hot_pdf_object_with_dup_span = HotPdf(height=1170, width=827)
    hot_pdf_object_with_dup_span.load(luca_mock_file_name, drop_duplicate_spans=False)

    hot_pdf_object = HotPdf(height=1170, width=827)
    hot_pdf_object.load(luca_mock_file_name)

    assert len(hot_pdf_object.pages[0].span_map) < len(
        hot_pdf_object_with_dup_span.pages[0].span_map
    )
