from hotpdf.processor import get_document_xml
from hotpdf.memory_map import MemoryMap
from hotpdf.utils import filter_adjacent_coords


class HotPdf:
    def __init__(self, height: int, width: int, precision: int = 1):
        self.pages = []
        self.height = height
        self.width = width
        self.precision = precision

    def load(self, pdf_file: str):
        if len(self.pages) > 0:
            raise Exception("File already loaded!")
        document_xml = get_document_xml(pdf_file)
        for xml_page in document_xml:
            parsed_page = MemoryMap(
                width=self.width + 5, height=self.height + 5, precision=0.75
            )
            parsed_page.build_memory_map()
            parsed_page.load_memory_map(xml_page)
            self.pages.append(parsed_page)

    def find_text(self, query: str, pages: list[int] = []):
        if len(pages) == 0:
            query_pages = {i: self.pages[i] for i in range(len(self.pages))}
        else:
            query_pages = {i: self.pages[i] for i in pages}

        found_page_map = {}
        for page_num in query_pages:
            found_page_map[page_num] = filter_adjacent_coords(
                *query_pages[page_num].find_text(query)
            )
        return found_page_map

    def extract_text(self, x0: int, y0: int, x1: int, y1: int, page: int = 0):
        page_to_search: MemoryMap = self.pages[page]
        extracted_text = page_to_search.extract_text_from_bbox(
            x0=x0, x1=x1, y0=y0, y1=y1
        )
        return extracted_text
