import math
from collections.abc import Generator
from hashlib import md5
from typing import Any

from pdfminer.layout import LTChar, LTPage, LTText, LTTextContainer, LTTextLine

from .data.classes import HotCharacter, PageResult
from .helpers.nanoid import generate_nano_id
from .span_map import SpanMap
from .sparse_matrix import SparseMatrix
from .trie import Trie


class MemoryMap:
    def __init__(self) -> None:
        """Initialize the MemoryMap. 2D Matrix representation of a PDF Page.

        Args:
            width (int): The width (max columns) of a page.
            height (int) The height (max rows) of a page.
        """
        self.text_trie = Trie()
        self.span_map = SpanMap()
        self.width: int = 0
        self.height: int = 0

    def build_memory_map(self) -> None:
        """Build the memory map based on width and height.

        The memory map is a SparseMatrix representation of the PDF.
        """
        self.memory_map = SparseMatrix()

    def __get_page_spans(self, page: LTPage) -> Generator[LTTextContainer[Any], None, None]:
        for element in page:
            if isinstance(element, LTTextContainer):
                yield element

    def load_memory_map(self, page: LTPage, drop_duplicate_spans: bool = True) -> None:
        """Load memory map data from an XML page.

        Args:
            page (str): The XML page data.
            drop_duplicate_spans (bool): Drop spans that are duplicates (example: on top of each other)

        Returns:
            None
        """
        char_hot_characters: list[tuple[str, HotCharacter]] = []
        spans: Generator[LTTextContainer[Any], None, None] = self.__get_page_spans(page)
        seen_span_hashes: list[str] = []
        if not spans:
            return
        for span in spans:
            span_hash = md5(str(seen_span_hashes).encode(), usedforsecurity=False).hexdigest()
            if span_hash in seen_span_hashes:
                continue
            seen_span_hashes.append(span_hash)
            span_id = generate_nano_id(size=10)
            for line in span:
                if not isinstance(line, LTTextLine):
                    continue
                for character in line:
                    if isinstance(character, (LTChar, LTText)) and (
                        hasattr(character, "x0")
                        and hasattr(character, "x1")
                        and hasattr(character, "y0")
                        and hasattr(character, "y1")
                    ):
                        char_c = character.get_text()
                        x0 = round(character.x0)
                        x1 = round(character.x1)
                        y0 = round(page.height - character.y0)
                        hot_character = HotCharacter(
                            value=char_c,
                            x=x0,
                            y=y0,
                            x_end=x1,
                            span_id=span_id,
                        )
                        self.memory_map.insert(value=char_c, row_idx=y0, column_idx=x0)
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
        self.width = math.ceil(page.width)
        self.height = math.ceil(page.height)

    def extract_text_from_bbox(self, x0: int, x1: int, y0: int, y1: int) -> str:
        """Extract text within a specified bounding box.

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
                self.memory_map.get(row_idx=row, column_idx=col)
                for col in range(max(x0, 0), min(x1, self.memory_map.columns - 1) + 1)
            ])
            if row_text:
                extracted_text += row_text + "\n"

        return extracted_text

    def find_text(self, query: str) -> tuple[list[str], PageResult]:
        """Find text within the memory map.

        Args:
            query (str): The text to search for.

        Returns:
            list: List of found text coordinates.
        """
        found_text = self.text_trie.search_all(query)
        return found_text
