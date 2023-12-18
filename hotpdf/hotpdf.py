from hotpdf.processor import generate_xml_file
from hotpdf.memory_map import MemoryMap
from hotpdf.utils import filter_adjacent_coords, get_element_dimension
from .data.classes import HotCharacter
import math
import xml.etree.cElementTree as ET
import os
import gc
from typing import Optional, Union


class HotPdf:
    def __init__(
        self,
        height: int,
        width: int,
        precision: float = 0.75,
        extraction_tolerance: int = 4,
    ):
        """
        Initialize the HotPdf class.

        Args:
            height (int): The height of the PDF pages.
            width (int): The width of the PDF pages.
            precision (float, optional): Precision parameter for loading. Defaults to 1.
            extraction_tolerance (int, optional): Tolerance value used during text extraction
                to adjust the bounding box for capturing text. Defaults to 4.
        """
        self.pages: list[MemoryMap] = []
        self.height: int = height
        self.width: int = width
        self.precision: float = precision
        self.extraction_tolerance: int = extraction_tolerance
        self.xml_file_path: Optional[str] = None

    def __del__(self):
        if self.xml_file_path:
            os.remove(self.xml_file_path)

    def __check_file_exists(self, pdf_file: str):
        if not os.path.exists(pdf_file):
            raise FileNotFoundError(f"File {pdf_file} not found")

    def __check_file_already_loaded(self):
        if len(self.pages) > 0:
            raise Exception("A file is already loaded!")

    def __check_coordinates(self, x0: int, y0: int, x1: int, y1: int):
        if x0 < 0 or x1 < 0 or y0 < 0 or y1 < 0:
            raise ValueError("Invalid coordinates")
        if x0 > self.width or x1 > self.width or y0 > self.height or y1 > self.height:
            raise ValueError("Invalid coordinates")

    def __check_page_number(self, page: int):
        if page < 0 or page >= len(self.pages):
            raise ValueError("Invalid page number")

    def __check_page_range(self, first_page: int, last_page: int):
        if first_page > last_page or first_page < 0 or last_page < 0:
            raise ValueError("Invalid page range")

    def prechecks(self, pdf_file: str, first_page: int, last_page: int):
        self.__check_file_exists(pdf_file)
        self.__check_file_already_loaded()
        self.__check_page_range(first_page, last_page)

    def load(
        self,
        pdf_file: str,
        drop_duplicate_spans: bool = True,
        first_page: int = 0,
        last_page: int = 0,
    ):
        """
        Load a PDF file into memory.

        Args:
            pdf_file (str): The path to the PDF file to be loaded.
            drop_duplicate_spans (bool, optional): Drop duplicate spans when loading. Defaults to True.
            first_page (int, optional): The first page to load. Defaults to 0.
            last_page (int, optional): The last page to load. Defaults to 0.
        Raises:
            Exception: If a file is already loaded.
            ValueError: If the page range is invalid.
            FileNotFoundError: If the file is not found.
        """
        self.prechecks(pdf_file, first_page, last_page)
        self.xml_file_path = generate_xml_file(pdf_file, first_page, last_page)
        xml_object = ET.parse(self.xml_file_path)
        for xml_page in xml_object.findall(".//page"):
            parsed_page = MemoryMap(
                width=self.width + self.extraction_tolerance + 1,
                height=self.height + self.extraction_tolerance + 1,
                precision=self.precision,
            )
            parsed_page.build_memory_map()
            parsed_page.load_memory_map(
                page=xml_page, drop_duplicate_spans=drop_duplicate_spans
            )
            self.pages.append(parsed_page)
        del xml_object
        gc.collect()

    def extract_full_text_span(
        self,
        hot_characters: list[HotCharacter],
        page_num: int,
    ) -> Union[list[HotCharacter], None]:
        """
        Find text and all text in it's parent span.
        Args:
            query (str): The text to search for.
            pages (list[int], optional): List of page numbers to search. Defaults to [].
            validate (bool, optional): Double check the extracted bounding boxes with the query string.
        Returns:
            dict: A dictionary mapping page numbers to found text coordinates.
        """
        full_span = None
        if hot_characters[0].span_id:
            full_span = self.pages[page_num].span_map[hot_characters[0].span_id]
        return full_span

    def find_text(
        self,
        query: str,
        pages: list[int] = [],
        validate: bool = True,
        take_span: bool = False,
    ) -> dict[int, list[list[HotCharacter]]]:
        """
        Find text within the loaded PDF pages.

        Args:
            query (str): The text to search for.
            pages (list[int], optional): List of page numbers to search. Defaults to [].
            validate (bool, optional): Double check the extracted bounding boxes with the query string.
            take_span (bool, optional): Take the full span of the text that it is a part of.
        Raises:
            ValueError: If the page number is invalid.
        Returns:
            dict: A dictionary mapping page numbers to found text coordinates.
        """
        for page in pages:
            self.__check_page_number(page)

        if len(pages) == 0:
            query_pages = {i: self.pages[i] for i in range(len(self.pages))}
        else:
            query_pages = {i: self.pages[i] for i in pages}

        found_page_map = {}

        for page_num in query_pages:
            found_page_map[page_num] = filter_adjacent_coords(
                *query_pages[page_num].find_text(query)
            )

        final_found_page_map: dict = {}
        for page_num in found_page_map.keys():
            hot_character_page_occurences: list[list[HotCharacter]] = found_page_map[
                page_num
            ]
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
                        full_span_dimension_hot_characters = (
                            self.extract_full_text_span(
                                hot_characters=hot_characters,
                                page_num=page_num,
                            )
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
        sort: bool = True,
    ) -> list[list[HotCharacter]]:
        """
        Extract spans that exist within the specified bbox
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
            list: List of spans of hotcharacters that exist within the given bboxes
        """
        if len(self.pages[page].span_map) == 0:
            raise Exception("No spans exist on this page")

        text_in_bbox = self.extract_text(
            x0=x0,
            y0=y0,
            x1=x1,
            y1=y1,
            page=page,
        )
        if y1 != y0:
            text_in_bbox = list(map(str.strip, text_in_bbox.split("\n")))
            text_in_bbox = [_text for _text in text_in_bbox if _text]
        else:
            text_in_bbox = text_in_bbox.strip().strip("\n")
            text_in_bbox = [text_in_bbox]

        spans: list = []
        appended_spans: set = set()
        all_hot_characters_in_page: list[HotCharacter] = []

        for part_text in text_in_bbox:
            occurences_text_in_bbox = self.find_text(query=part_text, pages=[page])

            for _, page_num in enumerate(occurences_text_in_bbox):
                for hot_character_list in occurences_text_in_bbox[page_num]:
                    for hot_character in hot_character_list:
                        all_hot_characters_in_page.append(hot_character)
        if sort:
            all_hot_characters_in_page = sorted(
                all_hot_characters_in_page,
                key=lambda hot_character: (hot_character.y, hot_character.x),
            )
        for hot_character in all_hot_characters_in_page:
            if not hot_character.span_id:
                continue
            if hot_character.span_id in appended_spans or not (
                hot_character.y >= y0 and hot_character.y <= y1
            ):
                continue
            spans.append(self.pages[page].span_map[hot_character.span_id])
            appended_spans.add(hot_character.span_id)
        return spans

    def extract_text(
        self,
        x0: int,
        y0: int,
        x1: int,
        y1: int,
        page: int = 0,
    ):
        """
        Extract text from a specified bounding box on a page.

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
        x0 = max(0, math.floor(x0 - (1 / self.precision)))
        x1 = min(
            math.ceil(self.width + 1 / self.precision - 1),
            math.ceil(x1 + (1 / self.precision)) + self.extraction_tolerance,
        )
        extracted_text = page_to_search.extract_text_from_bbox(
            x0=math.floor(x0 - (1 / self.precision)),
            x1=math.ceil(x1 + (1 / self.precision)),
            y0=y0,
            y1=y1,
        )
        return extracted_text
