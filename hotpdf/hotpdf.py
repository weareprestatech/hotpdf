import math
import os
from collections import defaultdict
from io import IOBase
from pathlib import PurePath
from typing import Optional, Union

from hotpdf import processor
from hotpdf.memory_map import MemoryMap
from hotpdf.utils import filter_adjacent_coords, intersect

from .data.classes import ElementDimension, HotCharacter, PageResult, SearchResult, Span


class HotPdf:
    def __init__(
        self,
        pdf_file: Union[PurePath, str, IOBase, None] = None,
        password: str = "",
        page_numbers: Optional[list[int]] = None,
        extraction_tolerance: int = 4,
        laparams: Optional[dict[str, Union[float, bool]]] = None,
    ) -> None:
        """Initialize the HotPdf class.

        Args:
            pdf_file (PurePath | str | IOBytes): The path to the PDF file to be loaded, or a bytes object.
            password (str, optional): Password to use to unlock the pdf
            page_numbers (list[int], optional): Pages to be loaded into memory. (0-indexed).
                If not provided, will load all pages (default).
            extraction_tolerance (int, optional): Tolerance value used during text extraction
                to adjust the bounding box for capturing text. Defaults to 4.

        Raises:
            ValueError: If the page range is invalid.
            FileNotFoundError: If the file is not found.
            PermissionError: If the file is encrypted or the password is wrong.
            RuntimeError: If an unkown error is generated by transfotmer.
        """
        self.pages: list[MemoryMap] = []
        self.extraction_tolerance: int = extraction_tolerance
        if pdf_file:
            self.load(pdf_file, password, page_numbers, laparams=laparams)

    def __check_file_exists(self, pdf_file: str) -> None:
        if not os.path.exists(pdf_file):
            raise FileNotFoundError(f"File {pdf_file} not found")

    def __check_coordinates(self, x0: int, y0: int, x1: int, y1: int) -> None:
        if x0 < 0 or x1 < 0 or y0 < 0 or y1 < 0:
            raise ValueError("Invalid coordinates")

    def __check_page_number(self, page: int) -> None:
        if page < 0 or page >= len(self.pages):
            raise ValueError("Invalid page number")

    def __check_page_numbers(self, pages: list[int]) -> None:
        for page in pages:
            self.__check_page_number(page)

    def __check_page_range(self, page_numbers: list[int]) -> None:
        if any(_page_num < 0 for _page_num in page_numbers):
            raise ValueError("Invalid page range")

    def __prechecks(self, pdf_file: Union[PurePath, str, IOBase], page_numbers: list[int]) -> None:
        if type(pdf_file) is str:
            self.__check_file_exists(pdf_file)
        self.__check_page_range(page_numbers)

    def load(
        self,
        pdf_file: Union[PurePath, str, IOBase],
        password: str = "",
        page_numbers: Optional[list[int]] = None,
        laparams: Optional[dict[str, Union[float, bool]]] = None,
    ) -> None:
        """Load a PDF file into memory.

        Args:
            pdf_file (str | Bytes): The path to the PDF file to be loaded, or a bytes object.
            password (str, optional): Password to use to unlock the pdf
            page_numbers (list[int], optional): Pages to be loaded into memory. (0-indexed).
                If not provided, will load all pages (default).
        Raises:
            Exception: If an unknown error is generated by pdfminer.
        """
        page_numbers = page_numbers or []
        self.__prechecks(pdf_file, page_numbers)
        try:
            self.pages = processor.process(pdf_file, password, page_numbers, laparams)
        except Exception as e:
            raise e

    def __extract_full_text_span(
        self,
        hot_characters: list[HotCharacter],
        page_num: int,
    ) -> Union[list[HotCharacter], None]:
        """Extract the full span of text that the given hot characters are a part of.

        Args:
            hot_characters (list[HotCharacter]): the list of hot characters to extract the span for.
            page_num (int): the page number of the hot characters.

        Returns:
            Union[list[HotCharacter], None]: the full span of text that the hot characters are a part of.
        """
        _span: Optional[Span] = None
        if hot_characters[0].span_id:
            _span = self.pages[page_num].span_map[hot_characters[0].span_id]
        return _span.characters if _span else None

    def find_text(
        self,
        query: str,
        pages: Optional[list[int]] = None,
        take_span: bool = False,
        sort: bool = True,
    ) -> SearchResult:
        """Find text within the loaded PDF pages.

        Args:
            query (str): The text to search for.
            pages (list[int], optional): List of page numbers to search.
            take_span (bool, optional): Take the full span of the text that it is a part of.
            sort (bool, Optional): Return elements sorted by their positions.
        Raises:
            ValueError: If the page number is invalid.

        Returns:
            SearchResult: A dictionary mapping page numbers to found text coordinates.
        """
        pages = pages or []

        self.__check_page_numbers(pages)

        query_pages = (
            {i: self.pages[i] for i in range(len(self.pages))} if len(pages) == 0 else {i: self.pages[i] for i in pages}
        )

        found_page_map = {}

        for page_num in query_pages:
            found_page_map[page_num] = filter_adjacent_coords(*query_pages[page_num].find_text(query))

        final_found_page_map: SearchResult = defaultdict(PageResult)

        for page_num in found_page_map:
            hot_character_page_occurences: PageResult = found_page_map[page_num]
            final_found_page_map[page_num] = []
            for hot_characters in hot_character_page_occurences:
                text = "".join(hc.value for hc in hot_characters)
                if query not in text:
                    continue
                full_span_dimension_hot_characters: Union[list[HotCharacter], None] = (
                    self.__extract_full_text_span(
                        hot_characters=hot_characters,
                        page_num=page_num,
                    )
                    if take_span
                    else None
                )
                chars_to_append = (
                    full_span_dimension_hot_characters
                    if (take_span and full_span_dimension_hot_characters)
                    else hot_characters
                )
                if chars_to_append and sort:
                    chars_to_append = sorted(chars_to_append, key=lambda ch: (ch.y, ch.x))
                final_found_page_map[page_num].append(chars_to_append)
        if sort:
            for _page in final_found_page_map:
                final_found_page_map[_page] = sorted(
                    final_found_page_map[_page], key=lambda element: (element[0].y, element[0].x)
                )
        return final_found_page_map

    def extract_spans(self, x0: int, y0: int, x1: int, y1: int, page: int = 0, sort: bool = True) -> list[Span]:
        """Extract spans that intersect with the given bounding box.

        Args:
            x0 (int): The left x-coordinate of the bounding box.
            y0 (int): The bottom y-coordinate of the bounding box.
            x1 (int): The right x-coordinate of the bounding box.
            y1 (int): The top y-coordinate of the bounding box.
            page (int, optional): The page number. Defaults to 0.
            sort (bool, optional): Sort the spans by their coordinates. Defaults to True.

        Raises:
            ValueError: If the coordinates are invalid.
            ValueError: If the page number is invalid.

        Returns:
            list[Span]: List of spans of hotcharacters that intersect with the given bounding box
        """
        spans: list[Span] = []

        self.__check_coordinates(x0, y0, x1, y1)
        self.__check_page_number(page)

        for _, span in self.pages[page].span_map.items():
            if intersect(ElementDimension(x0, y0, x1, y1, ""), span.get_element_dimension()):
                span.characters = sorted(span.characters, key=lambda ch: (ch.y, ch.x))
                spans.append(span)
                if sort:
                    spans = sorted(
                        spans, key=lambda span: (span.get_element_dimension().y0, span.get_element_dimension().x0)
                    )

        return spans

    def extract_text(
        self,
        x0: int,
        y0: int,
        x1: int,
        y1: int,
        page: int = 0,
    ) -> str:
        """Extract text from a specified bounding box on a page.

        Args:
            x0 (int): The left x-coordinate of the bounding box.
            y0 (int): The bottom y-coordinate of the bounding box.
            x1 (int): The right x-coordinate of the bounding box.
            y1 (int): The top y-coordinate of the bounding box.
            page (int): The page number. Defaults to 0.

        Raises:
            ValueError: If the coordinates are invalid.
            ValueError: If the page number is invalid.

        Returns:
            str: Extracted text within the bounding box.
        """
        self.__check_coordinates(x0, y0, x1, y1)
        self.__check_page_number(page)

        page_to_search: MemoryMap = self.pages[page]
        extracted_text = page_to_search.extract_text_from_bbox(
            x0=math.floor(x0),
            x1=math.ceil(x1 + self.extraction_tolerance),
            y0=y0,
            y1=y1,
        )
        return extracted_text

    def extract_page_text(
        self,
        page: int,
    ) -> str:
        """Extract text from a specified page.

        Args:
            page (int): The page number.

        Raises:
            ValueError: If the page number is invalid.

        Returns:
            str: Extracted text from the page.
        """
        self.__check_page_number(page)

        page_to_search: MemoryMap = self.pages[page]
        extracted_text = page_to_search.extract_text_from_bbox(
            x0=0,
            x1=page_to_search.width,
            y0=0,
            y1=page_to_search.height,
        )
        return extracted_text

    def extract_spans_text(
        self,
        x0: int,
        y0: int,
        x1: int,
        y1: int,
        page: int = 0,
    ) -> str:
        """Extract text from spans that intersect with the given bounding box.

        Args:
            x0 (int): The left x-coordinate of the bounding box.
            y0 (int): The bottom y-coordinate of the bounding box.
            x1 (int): The right x-coordinate of the bounding box.
            y1 (int): The top y-coordinate of the bounding box.
            page (int, optional): The page number. Defaults to 0.

        Raises:
            ValueError: If the coordinates are invalid.
            ValueError: If the page number is invalid.

        Returns:
            str: Extracted text that intersects with the bounding box.
        """
        self.__check_coordinates(x0, y0, x1, y1)
        self.__check_page_number(page)

        spans: list[Span] = self.extract_spans(x0, y0, x1, y1, page)
        extracted_text: list[str] = []

        for span in spans:
            extracted_text.append(span.to_text())
        return "".join(extracted_text)
