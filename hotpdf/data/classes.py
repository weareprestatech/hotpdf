from dataclasses import dataclass
from typing import Optional
from collections import defaultdict


@dataclass
class HotCharacter:
    """
    A hot character is a character on a page with certain attributes.
    value (str): value value of the character.
    x (int): x position of the character - column number.
    y (int): y position of the character - row number.
    x_end (int): end x position of the character. x_end - x = width of character.
    span_id (Optional)(str): hash of parent span the character lies in.
    """

    value: str
    x: int
    y: int
    x_end: float
    span_id: Optional[str] = None


@dataclass
class ElementDimension:
    """
    ElementDimension is the dimension of an element in hotpdf
    x0 (int): starting x position of the element (column).
    y0 (int): starting y position of the element (row).
    x1 (int): end x position of the element (column). x1 - x0 = width.
    y1 (int): end y position of the element (row) y1 - y0 = height.
    span_id (Optional)(str): hash of parent span the element lies in.
    """

    x0: int
    y0: int
    x1: int
    y1: int
    span_id: Optional[str] = None


# All occurences of HotCharacters in a page
# A list[HotCharacter] is the representation of a word split into "HotCharacters"
# A list[list[HotCharacter]] is a list of multiple list[HotCharacter] found on a page
PageResult = list[list[HotCharacter]]

# Complete PageResult with Page Number as the index
SearchResult = defaultdict[int, PageResult]
