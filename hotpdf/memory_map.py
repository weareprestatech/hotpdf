import math
import xml.etree.cElementTree as ET
from functools import lru_cache
from hashlib import md5
from typing import Generator

from .data.classes import HotCharacter, PageResult
from .helpers.nanoid import generate_nano_id
from .span_map import SpanMap
from .sparse_matrix import SparseMatrix
from .trie import Trie


class MemoryMap:
    def __init__(self) -> None:
        """
        Initialize the MemoryMap. 2D Matrix representation of a PDF Page.

        Args:
            width (int): The width (max columns) of a page.
            height (int) The height (max rows) of a page.
        """
        self.text_trie = Trie()
        self.span_map = SpanMap()
        self.width: int = 0
        self.height: int = 0

    def build_memory_map(self) -> None:
        """
        Build the memory map based on width and height.
        The memory map is a SparseMatrix representation of the PDF.
        """
        self.memory_map = SparseMatrix()

    def __get_page_spans(self, page: ET.Element) -> Generator[ET.Element, None, None]:
        return page.iterfind(".//span")

    def __get_page_chars(self, page: ET.Element) -> Generator[ET.Element, None, None]:
        return page.iterfind(".//char")

    def __get_span_chars(self, spans: Generator[ET.Element, None, None], drop_duplicate_spans: bool) -> Generator[ET.Element, None, None]:
        seen_span_hashes: set[str] = set()
        for span in spans:
            span_id: str = generate_nano_id(size=10)
            span_hash: str = md5(f"{str(span.attrib)}|{str([_char.attrib for _char in span.iterfind('.//')])}".encode()).hexdigest()
            if drop_duplicate_spans:
                if span_hash in seen_span_hashes:
                    continue
                seen_span_hashes.add(span_hash)
            for char in span.iterfind(".//"):
                char.set("span_id", span_id)
                yield char

    def load_memory_map(self, page: ET.Element, drop_duplicate_spans: bool = True) -> None:
        """
        Load memory map data from an XML page.

        Args:
            page (str): The XML page data.
            drop_duplicate_spans (bool): Drop spans that are duplicates (example: on top of each other)
        Returns:
            None
        """
        char_hot_characters: list[tuple[str, HotCharacter]] = []
        spans: Generator[ET.Element, None, None] = self.__get_page_spans(page)
        chars: Generator[ET.Element, None, None]
        if spans:
            chars = self.__get_span_chars(
                spans=spans,
                drop_duplicate_spans=drop_duplicate_spans,
            )
        else:
            chars = self.__get_page_chars(page)
        for char in chars:
            char_bbox = char.attrib["bbox"]
            char_x0, char_y0, char_x1, char_y1 = map(float, char_bbox.split())
            if char_x0 < 0 or char_y0 < 0 or char_x1 < 0 or char_y1 < 0:
                continue
            char_c = char.attrib["c"]
            char_span_id = char.attrib.get("span_id")
            cell_x = math.floor(char_x0)
            cell_y = math.floor(char_y0)
            cell_x_end = math.ceil(char_x1)
            hot_character = HotCharacter(
                value=char_c,
                x=cell_x,
                y=cell_y,
                x_end=cell_x_end,
                span_id=char_span_id,
            )
            self.memory_map.insert(value=char_c, row_idx=cell_y, column_idx=cell_x)
            char_hot_characters.append((
                char_c,
                hot_character,
            ))
        # Insert into Trie and Span Maps
        _hot_character: HotCharacter
        for char_c, _hot_character in char_hot_characters:
            self.text_trie.insert(char_c, _hot_character)
            if _hot_character.span_id:
                self.span_map[_hot_character.span_id] = _hot_character
        self.width = self.memory_map.columns
        self.height = self.memory_map.rows

    @lru_cache
    def extract_text_from_bbox(self, x0: int, x1: int, y0: int, y1: int) -> str:
        """
        Extract text within a specified bounding box.

        Args:
            x0 (int): Left x-coordinate of the bounding box.
            x1 (int): Right x-coordinate of the bounding box.
            y0 (int): Bottom y-coordinate of the bounding box.
            y1 (int): Top y-coordinate of the bounding box.

        Returns:
            str: Extracted text within the bounding box.
        """
        extracted_text: str = ""
        for row in range(max(y0, 0), min(y1, self.memory_map.rows - 1) + 1):
            row_text: str = ""
            row_text = "".join([
                self.memory_map.get(row_idx=row, column_idx=col) for col in range(max(x0, 0), min(x1, self.memory_map.columns - 1) + 1)
            ])
            if row_text:
                extracted_text += row_text + "\n"

        return extracted_text

    @lru_cache
    def find_text(self, query: str) -> tuple[list[str], PageResult]:
        """
        Find text within the memory map.

        Args:
            query (str): The text to search for.

        Returns:
            list: List of found text coordinates.
        """
        found_text = self.text_trie.search_all(query)
        return found_text
