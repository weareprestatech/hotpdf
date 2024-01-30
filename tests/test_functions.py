import shutil

import pytest

from hotpdf import HotPdf
from hotpdf.data.classes import ElementDimension as El
from hotpdf.data.classes import HotCharacter
from hotpdf.sparse_matrix import SparseMatrix
from hotpdf.utils import filter_adjacent_coords, intersect, to_text


def xml_copy_file_name(xml_file_name: str):
    shutil.copy(xml_file_name, f"{xml_file_name}_copy.xml")
    return f"{xml_file_name}_copy.xml"


def test_load_file(valid_file_name):
    hot_pdf_object = HotPdf()
    hot_pdf_object.load(valid_file_name)


def test_element_dimensions_empty():
    assert filter_adjacent_coords(["d", "u", "m", "m", "y"], []) == []


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
        matrix[0, -1]
    with pytest.warns(UserWarning, match="Index Error. Skipping insertion into SparseMatrix"):
        matrix[-1, 0] = "Y"

    with pytest.raises(IndexError, match="Specified index is out of range"):
        matrix.get(-1, 0)
    with pytest.warns(UserWarning, match="Index Error. Skipping insertion into SparseMatrix"):
        matrix.insert("Y", -1, 0)


def test_sparse_matrix_iterator():
    matrix = SparseMatrix(3, 3)
    matrix[0, 0] = "A"
    matrix[1, 1] = "B"
    matrix[2, 2] = "C"
    non_empty_values = list(matrix)
    expected_result = [((0, 0), "A"), ((1, 1), "B"), ((2, 2), "C")]
    assert non_empty_values == expected_result


@pytest.mark.parametrize(
    "bbox1, bbox2, expected",
    [
        (El(0, 0, 2, 2), El(3, 3, 5, 5), False),
        (El(0, 0, 2, 2), El(3, 3, 4, 4), False),
        (El(0, 0, 2, 2), El(3, 3, 5, 5), False),
        (El(1, 1, 4, 4), El(3, 2, 6, 5), True),
        (El(1, 1, 6, 6), El(2, 2, 5, 5), True),
        (El(0, 0, 4, 4), El(4, 0, 8, 4), True),
        (El(0, 0, 3, 3), El(3, 3, 6, 6), True),
        (El(2, 1, 5, 4), El(4, 0, 7, 3), True),
        (El(1, 2, 4, 5), El(0, 4, 3, 7), True),
        (El(0, 0, 3, 3), El(0, 0, 3, 3), True),
        (El(2, 0, 6, 4), El(4, 2, 8, 6), True),
    ],
)
def test_intersect(bbox1, bbox2, expected):
    assert intersect(bbox1, bbox2) == expected


@pytest.mark.parametrize(
    "hot_characters, expected",
    [
        ([HotCharacter(value="H", x=0, y=0, x_end=10, span_id="x")], "H"),
        (
            [
                HotCharacter(value="H", x=0, y=0, x_end=10, span_id="x"),
                HotCharacter(value="e", x=0, y=0, x_end=10, span_id="x"),
                HotCharacter(value="l", x=0, y=0, x_end=10, span_id="x"),
                HotCharacter(value="l", x=0, y=0, x_end=10, span_id="x"),
                HotCharacter(value="o", x=0, y=0, x_end=10, span_id="x"),
            ],
            "Hello",
        ),
        (
            [
                HotCharacter(value="H", x=0, y=0, x_end=10, span_id="x"),
                HotCharacter(value="e", x=0, y=0, x_end=10, span_id="x"),
                HotCharacter(value="l", x=0, y=0, x_end=10, span_id="x"),
                HotCharacter(value="l", x=0, y=0, x_end=10, span_id="x"),
                HotCharacter(value="o", x=0, y=0, x_end=10, span_id="x"),
                HotCharacter(value=" ", x=0, y=0, x_end=10, span_id="x"),
                HotCharacter(value="W", x=0, y=0, x_end=10, span_id="x"),
                HotCharacter(value="o", x=0, y=0, x_end=10, span_id="x"),
                HotCharacter(value="r", x=0, y=0, x_end=10, span_id="x"),
                HotCharacter(value="l", x=0, y=0, x_end=10, span_id="x"),
                HotCharacter(value="d", x=0, y=0, x_end=10, span_id="x"),
            ],
            "Hello World",
        ),
    ],
)
def test_to_text(hot_characters, expected):
    assert to_text(hot_characters) == expected


def test_invalid_page_number(valid_file_name):
    hotpdf_object = HotPdf()
    hotpdf_object.load(valid_file_name)
    with pytest.raises(ValueError, match="Invalid page number"):
        _ = hotpdf_object.extract_page_text(page=2)


def test_len_memory_map_magic_function(valid_file_name):
    hotpdf_object = HotPdf()
    hotpdf_object.load(valid_file_name)
    assert len(hotpdf_object.pages[0].span_map) > 10
