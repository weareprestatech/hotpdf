import time
import tracemalloc

import pytest

from hotpdf import HotPdf


@pytest.fixture
def default_file_name():
    return "tests/resources/PDF.pdf"


@pytest.fixture
def multiple_pages_file_name():
    return "tests/resources/20pages.pdf"


@pytest.fixture
def luca_mock_file_name():
    return "tests/resources/luca_mock.pdf"


def test_benchmark_multiple_pages(multiple_pages_file_name):
    start_time = time.time()
    tracemalloc.start()
    hot_pdf_object = HotPdf()
    hot_pdf_object.load(multiple_pages_file_name)
    end_time = time.time()
    peak_memory = tracemalloc.get_traced_memory()[1] / (1024 * 1024)
    tracemalloc.stop()
    assert (end_time - start_time) < 2, "Benchmark time exceeded!"
    assert peak_memory < 15, "Benchmark memory usage exceeded!"


def test_luca_mock(luca_mock_file_name):
    start_time = time.time()
    tracemalloc.start()
    hot_pdf_object = HotPdf()
    hot_pdf_object.load(luca_mock_file_name)
    end_time = time.time()
    peak_memory = tracemalloc.get_traced_memory()[1] / (1024 * 1024)
    tracemalloc.stop()
    assert (end_time - start_time) < 2, "Benchmark time exceeded!"
    assert peak_memory < 12, "Benchmark memory usage exceeded!"


def test_default_file(default_file_name):
    start_time = time.time()
    tracemalloc.start()
    hot_pdf_object = HotPdf()
    hot_pdf_object.load(default_file_name)
    end_time = time.time()
    peak_memory = tracemalloc.get_traced_memory()[1] / (1024 * 1024)
    tracemalloc.stop()
    assert (end_time - start_time) < 2, "Benchmark time exceeded!"
    assert peak_memory < 0.6, "Benchmark memory usage exceeded!"
