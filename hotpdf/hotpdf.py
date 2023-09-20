from hotpdf.processor import get_document_xml
from hotpdf.memory_map import MemoryMap
from hotpdf.utils import filter_adjacent_coords, get_element_dimension
import math


class HotPdf:
    def __init__(
        self, height: int, width: int, precision: int = 1, extraction_tolerance: int = 4
    ):
        """
        Initialize the HotPdf class.

        Args:
            height (int): The height of the PDF pages.
            width (int): The width of the PDF pages.
            precision (int, optional): Precision parameter for loading. Defaults to 1.
            extraction_tolerance (int, optional): Tolerance value used during text extraction
                to adjust the bounding box for capturing text. Defaults to 4.
        """
        self.pages = []
        self.height = height
        self.width = width
        self.precision = precision
        self.extraction_tolerance = extraction_tolerance

    def load(self, pdf_file: str):
        """
        Load a PDF file into memory.

        Args:
            pdf_file (str): The path to the PDF file to be loaded.

        Raises:
            Exception: If a file is already loaded.
        """
        if len(self.pages) > 0:
            raise Exception("A file is already loaded!")
        document_xml = get_document_xml(pdf_file)
        for xml_page in document_xml:
            parsed_page = MemoryMap(
                width=self.width + 5, height=self.height + 5, precision=0.75
            )
            parsed_page.build_memory_map()
            parsed_page.load_memory_map(xml_page)
            self.pages.append(parsed_page)

    def find_text(self, query: str, pages: list[int] = [], validate: bool = True):
        """
        Find text within the loaded PDF pages.

        Args:
            query (str): The text to search for.
            pages (list[int], optional): List of page numbers to search. Defaults to [].
            validate (bool, optional): Double check the extracted bounding boxes with the query string.

        Returns:
            dict: A dictionary mapping page numbers to found text coordinates.
        """
        if len(pages) == 0:
            query_pages = {i: self.pages[i] for i in range(len(self.pages))}
        else:
            query_pages = {i: self.pages[i] for i in pages}

        found_page_map = {}

        for page_num in query_pages:
            found_page_map[page_num] = filter_adjacent_coords(
                *query_pages[page_num].find_text(query)
            )
        if not validate:
            return found_page_map

        final_found_page_map = {}
        for page_num in found_page_map.keys():
            coords = found_page_map[page_num]
            final_found_page_map[page_num] = []
            for coord in coords:
                span = get_element_dimension(coord)
                text = self.extract_text(
                    x0=span["x0"], x1=span["x1"], y0=span["y0"], y1=span["y1"]
                )
                if query in text:
                    final_found_page_map[page_num].append(coord)
        return final_found_page_map

    def extract_text(self, x0: int, y0: int, x1: int, y1: int, page: int = 0):
        """
        Extract text from a specified bounding box on a page.

        Args:
            x0 (int): The left x-coordinate of the bounding box.
            y0 (int): The bottom y-coordinate of the bounding box.
            x1 (int): The right x-coordinate of the bounding box.
            y1 (int): The top y-coordinate of the bounding box.
            page (int, optional): The page number. Defaults to 0.

        Returns:
            str: Extracted text within the bounding box.
        """
        page_to_search: MemoryMap = self.pages[page]
        x0 = max(0, math.floor(x0 - (1 / self.precision)))
        x1 = min(
            self.width + 1 / self.precision - 1,
            math.ceil(x1 + (1 / self.precision)) + self.extraction_tolerance,
        )
        extracted_text = page_to_search.extract_text_from_bbox(
            x0=math.floor(x0 - (1 / self.precision)),
            x1=math.ceil(x1 + (1 / self.precision)),
            y0=y0,
            y1=y1,
        )
        return extracted_text
