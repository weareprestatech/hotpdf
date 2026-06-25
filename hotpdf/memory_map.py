from __future__ import annotations

import math
from collections import defaultdict
from collections.abc import Generator
from uuid import UUID, uuid4

from pdfminer.layout import LTAnno, LTChar, LTComponent, LTFigure, LTPage, LTText, LTTextContainer, LTTextLine

from .data.classes import HotCharacter, PageResult
from .span_map import SpanMap
from .sparse_matrix import SparseMatrix
from .trie import Trie


class MemoryMap:
    def __init__(self) -> None:
        """Initialize the MemoryMap. 2D Matrix representation of a PDF Page.

        Args:
            width (int): The width of a page.
            height (int) The height of a page.
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
        self.char_x_end: dict[tuple[int, int], int] = {}

    def __reverse_page_objs(self, page_objs: list[LTComponent]) -> Generator[LTComponent, None, None]:
        yield from reversed(page_objs)

    def __extract_from_ltfigure(self, lt_figure_obj: LTFigure) -> Generator[LTTextLine | LTChar, None, None]:
        for element in lt_figure_obj:
            if isinstance(element, (LTTextLine, LTChar)):
                yield element
            elif isinstance(element, LTTextContainer):
                element_stack = self.__reverse_page_objs(list(element))
                yield from (em for em in element_stack if isinstance(em, LTTextLine))

    def __get_page_spans(self, page: LTPage) -> Generator[LTTextLine | LTChar, None, None]:
        element_stack = self.__reverse_page_objs(page._objs)
        for obj in element_stack:
            if isinstance(obj, LTTextLine):
                yield obj
            elif isinstance(obj, (LTTextContainer)):
                element_stack = self.__reverse_page_objs(list(obj))
                yield from (em for em in element_stack if isinstance(em, LTTextLine))
            elif isinstance(obj, (LTFigure)):
                yield from self.__extract_from_ltfigure(obj)

    def __get_right_shifted_hot_character(self, hot_character: HotCharacter, shift: int) -> HotCharacter:
        """Shift a hotcharacter on the x-coordinate

        Args:
            hot_character (HotCharacter): HotCharacter object to be shifted
            shift (int): shift offset on the x-coordinate

        Returns:
            HotCharacter: HotCharacter object with new coords
        """
        hot_character.x += shift
        hot_character.x_end += shift
        return hot_character

    def load_memory_map(
        self,
        page: LTPage,
        include_annotation_spaces: bool = False,
        preserve_pdfminer_coordinates: bool = False,
    ) -> None:
        """Load memory map data from an XML page.

        Args:
            page (str): LTPage Element returned by pdfminer
            include_annotation_spaces (bool, optional): Add annotation spaces to the memory map.
            preserve_pdfminer_coordinates(bool, optional): Preserve pdfminer y-coordinate values.
        Returns:
            None
        """
        char_hot_characters: list[HotCharacter] = []
        page_components: Generator[LTTextLine | LTChar, None, None] = self.__get_page_spans(page)
        line_shift: defaultdict[int, int] = defaultdict(int)
        for component in page_components:
            span_id = uuid4()
            prev_char_inserted = False
            if isinstance(component, LTChar):
                x0 = round(component.x0)
                x1 = round(component.x1)
                y0 = round(component.y0) if preserve_pdfminer_coordinates else round(page.height - component.y0)
                char_hot_characters.extend(
                    self.__get_hot_characters_of(
                        value=component.get_text(),
                        x=x0,
                        y=y0,
                        x_end=x1,
                        span_id=span_id,
                    )
                )
                continue
            for character in component:
                if (
                    include_annotation_spaces
                    and isinstance(character, LTAnno)
                    and (character._text == " ")
                    and prev_char_inserted
                ):
                    _elem_width: int = 1
                    space_char: HotCharacter = self.__get_hot_character_of(
                        value=" ", x=x0, y=y0, x_end=x0 + _elem_width, span_id=span_id, is_anno=True
                    )
                    char_hot_characters.append(
                        space_char,
                    )
                    prev_char_inserted = False
                elif (
                    isinstance(character, (LTChar, LTText))
                    and (
                        hasattr(character, "x0")
                        and hasattr(character, "x1")
                        and hasattr(character, "y0")
                        and hasattr(character, "y1")
                    )
                    and not isinstance(character, LTAnno)
                ):
                    char_c = character.get_text()
                    x0 = round(character.x0)
                    x1 = round(character.x1)
                    y0 = round(component.y0) if preserve_pdfminer_coordinates else round(page.height - component.y0)
                    char_hot_characters.extend(
                        self.__get_hot_characters_of(
                            value=char_c,
                            x=x0,
                            y=y0,
                            x_end=x1,
                            span_id=span_id,
                        )
                    )
                    prev_char_inserted = char_c != " "
        # Insert into Trie and Span Maps
        last_inserted_x_y: tuple[int, int] = (-1, -1)
        for i in range(len(char_hot_characters)):
            _current_character: HotCharacter = char_hot_characters[i]
            # Determine if annotation spaces should be added
            if include_annotation_spaces and i > 0 and i < len(char_hot_characters) - 1:
                prev_char: HotCharacter = char_hot_characters[i - 1]
                next_char: HotCharacter = char_hot_characters[i + 1]
                # Anno and non-anno characters should not be overlapping
                if _current_character.is_anno and next_char.x - prev_char.x <= 0:
                    continue

            # Prevent characters from overlapping
            if (last_inserted_x_y[0] > 0 and last_inserted_x_y[1] > 0) and (
                _current_character.x == last_inserted_x_y[0] and _current_character.y == last_inserted_x_y[1]
            ):
                line_shift[_current_character.y] += 1
            last_inserted_x_y = (_current_character.x, _current_character.y)
            _current_character = self.__get_right_shifted_hot_character(
                _current_character, line_shift[_current_character.y]
            )

            self.__insert_hotcharacter_to_memory(_current_character)
        self.width = math.ceil(page.width)
        self.height = math.ceil(page.height)

    def __insert_hotcharacter_to_memory(
        self,
        hot_character: HotCharacter,
    ) -> None:
        """Insert hotcharacter into memory map & trie"""
        if hot_character.value == "":
            return None
        self.memory_map.insert(value=hot_character.value, row_idx=hot_character.y, column_idx=hot_character.x)
        self.char_x_end[(hot_character.y, hot_character.x)] = hot_character.x_end
        self.text_trie.insert(word=hot_character.value, hot_character=hot_character)
        if hot_character.span_id:
            self.span_map[hot_character.span_id] = hot_character

    def __get_hot_character_of(
        self,
        value: str,
        x: int,
        y: int,
        x_end: int,
        span_id: UUID,
        is_anno: bool = False,
    ) -> HotCharacter:
        """Insert element into memory map.

        Args:
            value (str): Value of the object to be inserted.
            x (int): column index (x0-coordinate) of the element.
            y (int): row index (y0-coordinate) of the element.
            x_end (int): end column index (x1-coordinate) of element. x_end - x = width of element.
            span_id (UUID): id of parent span.

        Returns:
            HotCharacter: HotCharacter object of the whitespace.
        """
        return HotCharacter(
            value=value,
            x=x,
            y=y,
            x_end=x_end,
            span_id=span_id,
            is_anno=is_anno,
        )

    def __get_hot_characters_of(
        self,
        value: str,
        x: int,
        y: int,
        x_end: int,
        span_id: UUID,
        is_anno: bool = False,
    ) -> list[HotCharacter]:
        # pdfminer emits ligatures (e.g. "fi", "ffi") as a single glyph. The trie matches the
        # query one char at a time, so an un-split ligature makes find_text miss any text crossing
        # it. Split into single chars with proportional x so trie/find_text see real characters.
        if len(value) <= 1:
            return [self.__get_hot_character_of(value=value, x=x, y=y, x_end=x_end, span_id=span_id, is_anno=is_anno)]

        n = len(value)
        width = x_end - x
        return [
            self.__get_hot_character_of(
                value=char,
                x=round(x + width * i / n),
                y=y,
                x_end=round(x + width * (i + 1) / n),
                span_id=span_id,
                is_anno=is_anno,
            )
            for i, char in enumerate(value)
        ]

    def __render_lines(self, cells: list[tuple[int, int, int, str]], space_gap: int) -> str:
        """Render cells top-to-bottom, one grid row per line, with gap-based spacing."""
        by_row: dict[int, list[tuple[int, int, str]]] = defaultdict(list)
        for row, col, x_end, char in cells:
            by_row[row].append((col, x_end, char))

        lines: list[str] = []
        for row in sorted(by_row):
            parts: list[str] = []
            prev_x_end: int | None = None
            for col, x_end, char in sorted(by_row[row]):
                gap_break = prev_x_end is not None and col - prev_x_end > space_gap
                if gap_break and char != " " and parts and parts[-1] != " ":
                    parts.append(" ")
                parts.append(char)
                prev_x_end = x_end
            if parts:
                lines.append("".join(parts))

        return "\n".join(lines)

    @staticmethod
    def __widest_empty_run(occupied: set[int], lo: int, hi: int, min_gap: int) -> int | None:
        """Return the start column/row of the widest empty run >= min_gap within [lo, hi], else None."""
        best_len = 0
        best_start: int | None = None
        run_len = 0
        run_start: int | None = None
        for i in range(lo, hi + 1):
            if i in occupied:
                if run_len > best_len:
                    best_len, best_start = run_len, run_start
                run_len = 0
                run_start = None
            else:
                if run_start is None:
                    run_start = i
                run_len += 1
        if run_len > best_len:
            best_len, best_start = run_len, run_start

        return best_start if best_len >= min_gap else None

    def __xy_cut(self, cells: list[tuple[int, int, int, str]], gap_x: int, gap_y: int, space_gap: int) -> str:
        """Recursive XY-cut: split the region at its widest gutter, read blocks in order."""
        if not cells:
            return ""

        min_x = min(c[1] for c in cells)
        max_x = max(c[2] for c in cells)
        min_y = min(c[0] for c in cells)
        max_y = max(c[0] for c in cells)
        cols_used: set[int] = set()
        rows_used: set[int] = set()
        for row, col, x_end, _ in cells:
            cols_used.update(range(col, x_end + 1))
            rows_used.add(row)

        v_cut = self.__widest_empty_run(cols_used, min_x, max_x, gap_x)
        h_cut = self.__widest_empty_run(rows_used, min_y, max_y, gap_y)
        if v_cut is None and h_cut is None:
            return self.__render_lines(cells, space_gap)

        # Prefer the vertical cut (column split) when present; it preserves reading order of rows.
        if v_cut is not None and (h_cut is None or v_cut >= h_cut):
            left = [c for c in cells if c[2] < v_cut]
            right = [c for c in cells if c[2] >= v_cut]
            return self.__xy_cut(left, gap_x, gap_y, space_gap) + "\n" + self.__xy_cut(right, gap_x, gap_y, space_gap)

        top = [c for c in cells if c[0] < h_cut]
        bottom = [c for c in cells if c[0] >= h_cut]
        return self.__xy_cut(top, gap_x, gap_y, space_gap) + "\n" + self.__xy_cut(bottom, gap_x, gap_y, space_gap)

    def extract_text_from_bbox(
        self,
        x0: int,
        x1: int,
        y0: int,
        y1: int,
        space_gap: int = 2,
        segment: bool = False,
        segment_gap_x: int = 12,
        segment_gap_y: int = 6,
    ) -> str:
        """Extract text within a specified bounding box.

        Args:
            x0 (int): Left x-coordinate of the bounding box.
            x1 (int): Right x-coordinate of the bounding box.
            y0 (int): Bottom y-coordinate of the bounding box.
            y1 (int): Top y-coordinate of the bounding box.
            space_gap (int): Insert a space when the horizontal gap between a glyph's end and the
                next glyph's start exceeds this many columns. Separate text groups (form fields,
                table cells) carry no explicit space character, so the gap is the only signal.
            segment (bool): Group text into layout blocks via recursive XY-cut before reading, so
                side-by-side columns (e.g. a left-margin label next to a table) are not interleaved
                row by row. Best-effort; dense forms may over-segment. Defaults to False.
            segment_gap_x (int): Minimum empty-column run treated as a vertical gutter when segment.
            segment_gap_y (int): Minimum empty-row run treated as a horizontal gutter when segment.

        Returns:
            str: Extracted text within the bounding box.
        """
        col_lo = max(x0, 0)
        col_hi = min(x1, self.memory_map.columns - 1)
        row_lo = max(y0, 0)
        row_hi = min(y1, self.memory_map.rows - 1)
        cells: list[tuple[int, int, int, str]] = []
        for row in range(row_lo, row_hi + 1):
            for col in range(col_lo, col_hi + 1):
                char = self.memory_map.get(row_idx=row, column_idx=col)
                if char:
                    cells.append((row, col, self.char_x_end.get((row, col), col + 1), char))

        if segment:
            extracted_text = self.__xy_cut(cells, segment_gap_x, segment_gap_y, space_gap)
            extracted_text = "\n".join(line for line in extracted_text.split("\n") if line)
            extracted_text = extracted_text + "\n" if extracted_text else ""
        else:
            extracted_text = self.__render_lines(cells, space_gap)
            extracted_text = extracted_text + "\n" if extracted_text else ""

        return extracted_text

    def find_text(self, query: str, case_sensitive: bool = True) -> tuple[list[str], PageResult]:
        """Find text within the memory map.

        Args:
            query (str): The text to search for.
            case_sensitive (bool): Whether the search should be case-sensitive. Defaults to True.

        Returns:
            list: List of found text coordinates.
        """
        found_text = self.text_trie.search_all(query, case_sensitive=case_sensitive)
        return found_text
