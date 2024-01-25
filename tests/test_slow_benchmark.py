import pytest

from tests.test_benchmark import perform_memory_test, perform_speed_test


@pytest.mark.skip()
def test_speed_bible(bible_file_name):
    perform_speed_test(bible_file_name, 100)


@pytest.mark.skip()
def test_memory_bible(bible_file_name):
    perform_memory_test(bible_file_name, 1300)
