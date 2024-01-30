from collections import defaultdict
from dataclasses import dataclass
from typing import Optional


@dataclass
class HotCharacter:
    """A hot character is a character on a page with certain attributes.

    Attributes:
        value (str): value value of the character.
        x (int): x position of the character - column number.
        y (int): y position of the character - row number.
        x_end (int): end x position of the character. x_end - x = width of character.
        span_id (str, Optional): hash of parent span the character lies in.
    """

    value: str
    x: int
    y: int
    x_end: int
    span_id: str


@dataclass
class ElementDimension:
    """ElementDimension is the dimension of an element in hotpdf.

    Attributes:
        x0 (int): starting x position of the element (column).
        y0 (int): starting y position of the element (row).
        x1 (int): end x position of the element (column). x1 - x0 = width.
        y1 (int): end y position of the element (row) y1 - y0 = height.
        span_id (str, Optional): hash of parent span the element lies in.
    """

    x0: int
    y0: int
    x1: int
    y1: int
    span_id: Optional[str] = None


@dataclass(init=True)
class Span:
    """A span is a group of characters that are close to each other.

    Attributes:
        characters (list[HotCharacter]): list of characters in the span.
        x0 (int): starting x position of the span (column).
        y0 (int): starting y position of the span (row).
        x_end (int): end x position of the span (column). x_end - x0 = width.
        span_id (str, Optional): hash of the span.
    """

    characters: list[HotCharacter]
    span_id: str

    def to_text(self) -> str:
        """Convert the span to text.

        Returns:
            str: text representation of the span.
        """
        return "".join([char.value for char in self.characters])

    def get_element_dimension(self) -> ElementDimension:
        """Get the element dimension of the span.

        Raises:
            ValueError: if the span has no characters.

        Returns:
            ElementDimension: _description_
        """
        if not self.characters:
            raise ValueError("Span has no characters")
        x0 = self.characters[0].x
        y0 = self.characters[0].y
        x1 = self.characters[-1].x_end
        y1 = y0
        return ElementDimension(x0, y0, x1, y1, self.span_id)


# All occurences of HotCharacters in a page
# A list[HotCharacter] is the representation of a word split into "HotCharacters"
# A list[list[HotCharacter]] is a list of multiple list[HotCharacter] found on a page
PageResult = list[list[HotCharacter]]

# Complete PageResult with Page Number as the index
SearchResult = defaultdict[int, PageResult]
