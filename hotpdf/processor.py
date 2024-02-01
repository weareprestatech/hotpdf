import logging
from io import IOBase
from pathlib import PurePath
from typing import Union

from pdfminer.high_level import extract_pages

from hotpdf.memory_map import MemoryMap

logging.getLogger("pdfminer").setLevel(logging.ERROR)


def __process(
    source: Union[PurePath, str, IOBase],
    password: str = "",
    first_page: int = 0,
    last_page: int = 0,
) -> list[MemoryMap]:
    pages: list[MemoryMap] = []
    page_numbers = None if first_page == 0 and last_page == 0 else list(range(first_page - 1, last_page))
    hl_page_layouts = extract_pages(source, password=password, page_numbers=page_numbers, caching=False)
    for page_layout in hl_page_layouts:
        parsed_page: MemoryMap = MemoryMap()
        parsed_page.build_memory_map()
        parsed_page.load_memory_map(page=page_layout)
        pages.append(parsed_page)
    return pages


def process(
    source: Union[PurePath, str, IOBase],
    password: str = "",
    first_page: int = 0,
    last_page: int = 0,
) -> list[MemoryMap]:
    return __process(
        source=source,
        password=password,
        first_page=first_page,
        last_page=last_page,
    )
