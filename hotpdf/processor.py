import logging
from io import IOBase
from pathlib import PurePath
from typing import Optional, Union

from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams

from hotpdf.memory_map import MemoryMap

logging.getLogger("pdfminer").setLevel(logging.ERROR)


def __make_custom_laparams_object(
    laparams: Optional[dict[str, Union[float, bool]]] = None,
) -> Union[LAParams, None]:
    if not laparams:
        return None
    laparams_obj: LAParams = LAParams()
    for key in laparams:
        if hasattr(laparams_obj, key):
            laparams_obj.__setattr__(key, laparams[key])
    return laparams_obj


def __supress_pdfminer_logs() -> None:
    logging.getLogger("pdfminer").setLevel(logging.ERROR)


def __process(
    source: Union[PurePath, str, IOBase],
    password: str = "",
    page_numbers: Optional[list[int]] = None,
    laparams: Optional[dict[str, Union[float, bool]]] = None,
    include_annotation_spaces: bool = False,
    preserve_pdfminer_coordinates: bool = False,
) -> list[MemoryMap]:
    pages: list[MemoryMap] = []
    __supress_pdfminer_logs()
    page_numbers = sorted(page_numbers) if page_numbers else []
    laparams_obj = __make_custom_laparams_object(laparams)

    hl_page_layouts = extract_pages(
        source, password=password, page_numbers=page_numbers, caching=True, laparams=laparams_obj
    )
    for page_layout in hl_page_layouts:
        parsed_page: MemoryMap = MemoryMap()
        parsed_page.build_memory_map()
        parsed_page.load_memory_map(
            page=page_layout,
            include_annotation_spaces=include_annotation_spaces,
            preserve_pdfminer_coordinates=preserve_pdfminer_coordinates,
        )
        pages.append(parsed_page)
    return pages


def process(
    source: Union[PurePath, str, IOBase],
    password: str = "",
    page_numbers: Optional[list[int]] = None,
    laparams: Optional[dict[str, Union[float, bool]]] = None,
    include_annotation_spaces: bool = False,
    preserve_pdfminer_coordinates: bool = False,
) -> list[MemoryMap]:
    return __process(
        source=source,
        password=password,
        page_numbers=page_numbers,
        laparams=laparams,
        include_annotation_spaces=include_annotation_spaces,
        preserve_pdfminer_coordinates=preserve_pdfminer_coordinates,
    )
