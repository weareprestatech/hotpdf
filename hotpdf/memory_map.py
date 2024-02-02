import math
from collections.abc import Generator

from pdfminer.layout import LTAnno, LTChar, LTComponent, LTPage, LTText, LTTextContainer, LTTextLine

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

    def __reverse_page_objs(self, page_objs: list[LTComponent]) -> Generator[LTComponent, None, None]:
        yield from reversed(page_objs)

    def __get_page_spans(self, page: LTPage) -> Generator[LTTextLine, None, None]:
        element_stack = self.__reverse_page_objs(page._objs)
        for obj in element_stack:
            if isinstance(obj, LTTextLine):
                yield obj
            elif isinstance(obj, LTTextContainer):
                element_stack = self.__reverse_page_objs(list(obj))
                yield from (em for em in element_stack if isinstance(em, LTTextLine))

    def load_memory_map(self, page: LTPage) -> None:
        """Load memory map data from an XML page.

        Args:
            page (str): LTPage Element returned by pdfminer

        Returns:
            None
        """
        char_hot_characters: list[tuple[str, HotCharacter]] = []
        spans: Generator[LTTextLine, None, None] = self.__get_page_spans(page)
        for span in spans:
            span_id = generate_nano_id(size=10)
            prev_char_inserted = False
            for character in span:
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
                    hot_character: HotCharacter = self.__insert_element(
                        value=char_c, x=x0, y=y0, x_end=x1, span_id=span_id
                    )
                    char_hot_characters.append((
                        char_c,
                        hot_character,
                    ))
                    prev_char_inserted = char_c != " "
                elif isinstance(character, LTAnno) and (character._text == " ") and prev_char_inserted:
                    _elem_width: int = 1
                    space_char: HotCharacter = self.__insert_element(
                        value=" ", x=x0, y=y0, x_end=x0 + _elem_width, span_id=span_id
                    )
                    char_hot_characters.append((
                        " ",
                        space_char,
                    ))
                    prev_char_inserted = False

        # Insert into Trie and Span Maps
        _hot_character: HotCharacter
        for char_c, _hot_character in char_hot_characters:
            self.text_trie.insert(char_c, _hot_character)
            if _hot_character.span_id:
                self.span_map[_hot_character.span_id] = _hot_character
        self.width = math.ceil(page.width)
        self.height = math.ceil(page.height)

    def __insert_element(self, value: str, x: int, y: int, x_end: int, span_id: str) -> HotCharacter:
        """Insert element into memory map.

        Args:
            value (str): Value of the object to be inserted.
            x (int): row index (y0-coordinate) of the element.
            y (int): column index (x0-coordinate) of the element.
            x_end (int): end column index (x1-coordinate) of element. x_end - x = width of element.
            span_id (str): id of parent span.

        Returns:
            HotCharacter: HotCharacter object of the whitespace.
        """
        self.memory_map.insert(value=value, row_idx=y, column_idx=x)
        return HotCharacter(
            value=value,
            x=x,
            y=y,
            x_end=x_end,
            span_id=span_id,
        )

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
            row_text = "".join(
                self.memory_map.get(row_idx=row, column_idx=col)
                for col in range(max(x0, 0), min(x1, self.memory_map.columns - 1) + 1)
            )
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
