import pytest
from hotpdf import HotPdf
from hotpdf.utils import filter_adjacent_coords
from hotpdf.data.classes import HotCharacter
import os


@pytest.fixture
def valid_file_name():
    return "tests/resources/PDF.pdf"


def test_sparse_matrix(valid_file_name):
    hot_pdf_object = HotPdf(height=1170, width=827)
    hot_pdf_object.load(valid_file_name)


def test_element_dimensions_empty():
    assert filter_adjacent_coords("dummy", []) == []


def test_span_map_behaviours(valid_file_name):
    hot_pdf_object = HotPdf(height=1170, width=827)
    hot_pdf_object.load(valid_file_name)

    with pytest.raises(KeyError, match="Cannot set key as None"):
        hot_pdf_object.pages[0].span_map[None] = HotCharacter(
            value='c',
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
