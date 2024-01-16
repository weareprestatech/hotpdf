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
def mock_hotpdf_bank_file_name():
    return "tests/resources/hotpdf_bank.pdf"


def perform_speed_test(file_name, expected_processing_seconds):
    start_time = time.time()
    hot_pdf_object = HotPdf()
    hot_pdf_object.load(file_name)
    end_time = time.time()
    assert (end_time - start_time) < expected_processing_seconds, "Benchmark time exceeded!"


def perform_memory_test(file_name, expected_peak_memory):
    tracemalloc.start()
    hot_pdf_object = HotPdf()
    hot_pdf_object.load(file_name)
    peak_memory = tracemalloc.get_traced_memory()[1] / (1024 * 1024)
    tracemalloc.stop()
    assert peak_memory < expected_peak_memory, "Benchmark memory usage exceeded!"


def test_speed_benchmark_multiple_pages(multiple_pages_file_name):
    perform_speed_test(multiple_pages_file_name, 4)


def test_memory_benchmark_multiple_pages(multiple_pages_file_name):
    perform_memory_test(multiple_pages_file_name, 15.5)


def test_speed_luca_mock(mock_hotpdf_bank_file_name):
    perform_speed_test(mock_hotpdf_bank_file_name, 3)


def test_memory_luca_mock(mock_hotpdf_bank_file_name):
    perform_memory_test(mock_hotpdf_bank_file_name, 12.5)


def test_speed_default_file(default_file_name):
    perform_speed_test(default_file_name, 2.5)


def test_memory_default_file(default_file_name):
    perform_memory_test(default_file_name, 1)
