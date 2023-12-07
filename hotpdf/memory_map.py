import math
import xml.etree.cElementTree as ET
from .trie import Trie
from .span_map import SpanMap
from .data.classes import HotCharacter
from .sparse_matrix import SparseMatrix
from functools import lru_cache
from uuid import uuid4


class MemoryMap:
    def __init__(self, width: float = 0, height: float = 0, precision: float = 0.5):
        """
        Initialize the MemoryMap. 2D Matrix representation of a PDF Page.

        Args:
            width (float, optional): The width of the map. Defaults to 0.
            height (float, optional): The height of the map. Defaults to 0.
            precision (float, optional): The precision factor. Defaults to 0.5.
        """
        self.height = height
        self.width = width
        self.precision = precision
        self.rows = self.height // self.precision
        self.columns = self.width // self.precision
        self.text_trie = Trie()
        self.span_map = SpanMap()

    def build_memory_map(self) -> None:
        """
        Build the memory map based on width and height.
        The memory map is a SparseMatrix representation of the PDF.
        """
        self.memory_map = SparseMatrix(rows=self.rows, columns=self.columns)

    def text(self) -> str:
        """
        Get text of the memory map
        """
        memory_map_str = ""
        if hasattr(self, "memory_map"):
            for row in range(self.rows):
                for col in range(self.columns):
                    memory_map_str += self.memory_map.get(row_idx=row, column_idx=col)
                memory_map_str += "\n"
        else:
            raise Exception("Memory map not built yet!")

        return memory_map_str

    def display_memory_map(
        self, save: bool = False, filename: str = "memory_map.txt"
    ) -> None:
        """
        Display or save the memory map.

        Args:
            save (bool, optional): Whether to save to a file. Defaults to False.
            filename (str, optional): The filename to save the map. Defaults to "memory_map.txt".
        """
        memory_map_str = ""
        if hasattr(self, "memory_map"):
            memory_map_str = self.text()
        else:
            raise Exception("Memory map not built yet!")

        if save:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(memory_map_str)
        else:
            print(memory_map_str)

    def load_memory_map(self, page: ET.Element) -> None:
        """
        Load memory map data from an XML page.

        Args:
            page (str): The XML page data.
            format (str, optional): The format of the page. Defaults to "xml". (Unused)
        Returns:
            None
        """
        if not hasattr(self, "memory_map"):
            raise Exception("Memory map not built yet!")

        char_hot_characters = []
        spans = page.findall(".//span")
        chars: list = []
        if spans:
            for span in spans:
                span_id = str(uuid4())
                for char in span.findall(".//"):
                    char.set("span_id", span_id)
                    chars.append(char)
        else:
            chars = page.findall(".//char")

        for char in chars:
            char_bbox = char.attrib["bbox"]
            char_x0, char_y0, char_x1, _ = [
                float(char_coord) for char_coord in char_bbox.split()
            ]
            char_c = char.attrib["c"]
            char_span_id = char.attrib.get("span_id")
            cell_x = int(math.floor(char_x0))
            cell_y = int(math.floor(char_y0))
            hot_character = HotCharacter(
                value=char_c,
                x=cell_x,
                y=cell_y,
                x_end=char_x1,
                span_id=char_span_id,
            )
            if not 0 < cell_x < self.width or not 0 < cell_y < self.height:
                continue

            if self.memory_map.get(row_idx=cell_y, column_idx=cell_x) != "":
                cell_x += 1
                char_x1 += 1
            self.memory_map.insert(value=char_c, row_idx=cell_y, column_idx=cell_x)
            char_hot_characters.append(
                (
                    char_c,
                    hot_character,
                )
            )
        # Insert into Trie and Span Maps
        _hot_character: HotCharacter
        for char_c, _hot_character in char_hot_characters:
            self.text_trie.insert(char_c, _hot_character)
            self.span_map.insert(_hot_character.span_id, _hot_character)

    @lru_cache
    def extract_text_from_bbox(self, x0: float, x1: float, y0: float, y1: float) -> str:
        """
        Extract text within a specified bounding box.

        Args:
            x0 (float): Left x-coordinate of the bounding box.
            x1 (float): Right x-coordinate of the bounding box.
            y0 (float): Bottom y-coordinate of the bounding box.
            y1 (float): Top y-coordinate of the bounding box.

        Returns:
            str: Extracted text within the bounding box.
        """
        if not hasattr(self, "memory_map"):
            raise Exception("Memory map not built!")

        cell_x0 = int(math.floor(x0))
        cell_x1 = int(math.ceil(x1))
        cell_y0 = int(math.floor(y0))
        cell_y1 = int(math.ceil(y1))

        extracted_text = ""
        for row in range(cell_y0, cell_y1 + 1):
            if 0 <= row < self.rows:
                row_text = ""
                for col in range(cell_x0, cell_x1 + 1):
                    if 0 <= col < self.rows:
                        row_text += self.memory_map.get(row_idx=row, column_idx=col)
                if row_text:
                    extracted_text += row_text
                    extracted_text += "\n"

        return extracted_text

    @lru_cache
    def find_text(self, query):
        """
        Find text within the memory map.

        Args:
            query (str): The text to search for.

        Returns:
            list: List of found text coordinates.
        """
        found_text = self.text_trie.search_all(query)
        return found_text
