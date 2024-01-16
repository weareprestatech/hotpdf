import time

import pytest

from hotpdf import HotPdf


@pytest.fixture
def multiple_pages_file_name():
    return "tests/resources/20pages.pdf"


@pytest.fixture
def luca_mock_file_name():
    return "tests/resources/luca_mock.pdf"


def test_benchmark_multiple_pages(multiple_pages_file_name):
    start_time = time.time()
    hot_pdf_object = HotPdf()
    hot_pdf_object.load(multiple_pages_file_name)
    assert (time.time() - start_time) < 2, "Benchmark time exceeded!"


def test_luca_mock(luca_mock_file_name):
    start_time = time.time()
    hot_pdf_object = HotPdf()
    hot_pdf_object.load(luca_mock_file_name)
    assert (time.time() - start_time) < 3, "Benchmark time exceeded!"
