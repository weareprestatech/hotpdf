import pytest


@pytest.fixture()
def valid_file_name():
    return "tests/resources/PDF.pdf"


@pytest.fixture()
def blank_file_name():
    return "tests/resources/blank.pdf"


@pytest.fixture()
def multiple_pages_file_name():
    return "tests/resources/20pages.pdf"


@pytest.fixture()
def non_existent_file_name():
    return "non_existent_file.pdf"


@pytest.fixture()
def locked_file_name():
    return "tests/resources/PDF_locked.pdf"


@pytest.fixture()
def invalid_file_name():
    return "tests/resources/invalid_file.txt"


@pytest.fixture()
def bible_file_name():
    return "tests/resources/bible.pdf"


@pytest.fixture()
def mock_hotpdf_bank_file_name():
    return "tests/resources/hotpdf_bank.pdf"
