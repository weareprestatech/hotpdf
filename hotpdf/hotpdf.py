import math
import os
import xml.etree.ElementTree as ET
from collections import defaultdict
from typing import Optional, Union

from hotpdf import processor
from hotpdf.memory_map import MemoryMap
from hotpdf.utils import filter_adjacent_coords, get_element_dimension, intersect

from .data.classes import ElementDimension, HotCharacter, PageResult, SearchResult, Span


class HotPdf:
    def __init__(
        self,
        extraction_tolerance: int = 4,
    ) -> None:
        """Initialize the HotPdf class.

        Args:
            extraction_tolerance (int, optional): Tolerance value used during text extraction
                to adjust the bounding box for capturing text. Defaults to 4.
        """
        self.pages: list[MemoryMap] = []
        self.extraction_tolerance: int = extraction_tolerance
        self.xml_file_path: Optional[str] = None

    def __delete_xml_file(self) -> None:
        if self.xml_file_path and os.path.exists(self.xml_file_path):
            os.remove(self.xml_file_path)

    def __check_file_exists(self, pdf_file: str) -> None:
        if not os.path.exists(pdf_file):
            raise FileNotFoundError(f"File {pdf_file} not found")

    def __check_coordinates(self, x0: int, y0: int, x1: int, y1: int) -> None:
        if x0 < 0 or x1 < 0 or y0 < 0 or y1 < 0:
            raise ValueError("Invalid coordinates")

    def __check_page_number(self, page: int) -> None:
        if page < 0 or page >= len(self.pages):
            raise ValueError("Invalid page number")

    def __check_page_range(self, first_page: int, last_page: int) -> None:
        if first_page > last_page or first_page < 0 or last_page < 0:
            raise ValueError("Invalid page range")

    def __prechecks(self, pdf_file: str, first_page: int, last_page: int) -> None:
        self.__check_file_exists(pdf_file)
        self.__check_page_range(first_page, last_page)

    def load(
        self,
        pdf_file: str,
        drop_duplicate_spans: bool = True,
        first_page: int = 0,
        last_page: int = 0,
    ) -> None:
        """Load a PDF file into memory.

        Args:
            pdf_file (str): The path to the PDF file to be loaded.
            drop_duplicate_spans (bool, optional): Drop duplicate spans when loading. Defaults to True.
            first_page (int, optional): The first page to load. Defaults to 0.
            last_page (int, optional): The last page to load. Defaults to 0.

        Raises:
            ValueError: If the page range is invalid.
            FileNotFoundError: If the file is not found.
        """
        self.__prechecks(pdf_file, first_page, last_page)
        self.xml_file_path = processor.generate_xml_file(pdf_file, first_page, last_page)
        tree_iterator = ET.iterparse(self.xml_file_path, events=("start", "end"))
        event: str
        root: ET.Element
        event, root = next(tree_iterator)

        element: ET.Element
        for event, element in tree_iterator:
            if event == "end" and element.tag == "page":
                parsed_page: MemoryMap = MemoryMap()
                parsed_page.build_memory_map()
                parsed_page.load_memory_map(page=element, drop_duplicate_spans=drop_duplicate_spans)
                self.pages.append(parsed_page)
                element.clear()
            root.clear()
        self.__delete_xml_file()

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
        validate: bool = True,
        take_span: bool = False,
    ) -> SearchResult:
        """Find text within the loaded PDF pages.

        Args:
            query (str): The text to search for.
            pages (list[int], optional): List of page numbers to search.
            validate (bool, optional): Double check the extracted bounding boxes with the query string.
            take_span (bool, optional): Take the full span of the text that it is a part of.

        Raises:
            ValueError: If the page number is invalid.

        Returns:
            SearchResult: A dictionary mapping page numbers to found text coordinates.
        """
        if pages is None:
            pages = []

        for page in pages:
            self.__check_page_number(page)

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
                element_dimension = get_element_dimension(hot_characters)
                text = self.extract_text(
                    x0=element_dimension.x0,
                    y0=element_dimension.y0,
                    x1=element_dimension.x1,
                    y1=element_dimension.y1,
                    page=page_num,
                )
                if (query in text) or not validate:
                    if take_span:
                        full_span_dimension_hot_characters = self.__extract_full_text_span(
                            hot_characters=hot_characters,
                            page_num=page_num,
                        )
                    final_found_page_map[page_num].append(
                        full_span_dimension_hot_characters
                        if (take_span and full_span_dimension_hot_characters)
                        else hot_characters
                    )

        return final_found_page_map

    def extract_spans(
        self,
        x0: int,
        y0: int,
        x1: int,
        y1: int,
        page: int = 0,
    ) -> list[Span]:
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
            if intersect(ElementDimension(x0, y0, x1, y1), span.get_element_dimension()):
                spans.append(span)
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
            # TODO: This will be span.to_text() in the next release
            extracted_text.append(span.to_text())
        return "".join(extracted_text)
