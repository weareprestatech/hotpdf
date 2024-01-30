import time
import tracemalloc

import pytest

from hotpdf import HotPdf


def perform_speed_test(file_name, expected_processing_seconds):
    start_time = time.time()
    hot_pdf_object = HotPdf()
    hot_pdf_object.load(file_name)
    end_time = time.time()
    elapsed = end_time - start_time
    assert (elapsed) < expected_processing_seconds, "Benchmark time exceeded!"


@pytest.mark.skip(reason="Need to perform benchmarks first for pdfminer")
def perform_memory_test(file_name, expected_peak_memory):
    tracemalloc.start()
    hot_pdf_object = HotPdf()
    hot_pdf_object.load(file_name)
    peak_memory = tracemalloc.get_traced_memory()[1] / (1024 * 1024)
    tracemalloc.stop()
    assert peak_memory < expected_peak_memory, "Benchmark memory usage exceeded!"


def test_speed_benchmark_multiple_pages(multiple_pages_file_name):
    perform_speed_test(multiple_pages_file_name, 2.9)


def test_memory_benchmark_multiple_pages(multiple_pages_file_name):
    perform_memory_test(multiple_pages_file_name, 16)


def test_speed_luca_mock(mock_hotpdf_bank_file_name):
    perform_speed_test(mock_hotpdf_bank_file_name, 3.5)


def test_memory_luca_mock(mock_hotpdf_bank_file_name):
    perform_memory_test(mock_hotpdf_bank_file_name, 12.99)


def test_speed_default_file(valid_file_name):
    perform_speed_test(valid_file_name, 2.9)


@pytest.mark.skip(reason="Need to perform benchmarks first")
def test_memory_default_file(valid_file_name):
    perform_memory_test(valid_file_name, 1)
