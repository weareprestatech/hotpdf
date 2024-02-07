import logging
from io import IOBase
from pathlib import PurePath
from typing import Optional, Union

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

from hotpdf.memory_map import MemoryMap

logging.getLogger("pdfminer").setLevel(logging.ERROR)


def __process(
    source: Union[PurePath, str, IOBase],
    password: str = "",
    page_numbers: Optional[list[int]] = None,
    laparams: Optional[dict[str, Union[float, bool]]] = None,
    include_annotation_spaces: bool = False,
) -> list[MemoryMap]:
    pages: list[MemoryMap] = []
    page_numbers = sorted(page_numbers) if page_numbers else []

    file = open(source, "rb") if not isinstance(source, IOBase) else source  # noqa: SIM115

    laparams_obj = LAParams(**laparams if laparams else {})
    parser = PDFParser(file)
    encoded_password = password.encode() if password else b""
    doc = PDFDocument(parser, password=encoded_password)
    rsrcmgr = PDFResourceManager()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams_obj)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for page_number, page in enumerate(PDFPage.create_pages(doc), start=0):
        if not page_numbers or page_number in page_numbers:
            interpreter.process_page(page)
            page_layout = device.get_result()
            parsed_page: MemoryMap = MemoryMap()
            parsed_page.build_memory_map()
            parsed_page.load_memory_map(page=page_layout, include_annotation_spaces=include_annotation_spaces)
            pages.append(parsed_page)

    if not isinstance(source, IOBase):
        file.close()
    return pages


def process(
    source: Union[PurePath, str, IOBase],
    password: str = "",
    page_numbers: Optional[list[int]] = None,
    laparams: Optional[dict[str, Union[float, bool]]] = None,
    include_annotation_spaces: bool = False,
) -> list[MemoryMap]:
    return __process(
        source=source,
        password=password,
        page_numbers=page_numbers,
        laparams=laparams,
        include_annotation_spaces=include_annotation_spaces,
    )
