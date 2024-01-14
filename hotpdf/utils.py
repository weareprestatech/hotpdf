import math
from copy import deepcopy
from typing import Union

from .data.classes import ElementDimension, HotCharacter, PageResult


def find_neighbour_coord(
    reference_character: HotCharacter,
    hot_characters: list[HotCharacter],
    max_distance: int = 5,
    span_tolerance: int = 5,
) -> Union[HotCharacter, None]:
    """
    Find a neighbouring coordinate within a specified maximum distance.

    Args:
        reference_coord (HotCharacter): Previous char instance.
        hot_characters (list[HotCharacter]): List of character instances to search through.
        max_distance (int): Maximum distance between reference coordinate and target coordinate.
        span_tolerance (int): Additional distance to consider if text lies in the same span.

    Returns:
        HotCharacter: The neighbouring HotCharacter if found, else None.
    """
    for hot_character in hot_characters:
        if (
            0
            <= (hot_character.x - reference_character.x_end)
            <= (
                (max_distance + span_tolerance)
                if hot_character.span_id == reference_character.span_id and (hot_character.span_id and reference_character.span_id)
                else max_distance
            )
            and reference_character.y == hot_character.y
        ):
            return hot_character
    return None


def filter_adjacent_coords(text: list[str], page_hot_character_occurences: PageResult) -> PageResult:
    """
    Filter adjacent coordinates based on the given text.

    Args:
        text (str): The text to filter by.
        page_hot_character_occurences (list): List of coordinates to filter by page

    Returns:
        PageResult: List of adjacent groups of HotCharacters on a page.
    """
    if not page_hot_character_occurences:
        return []

    max_len = len(text)
    adjacent_groups = []

    anchor_hot_character_instances = page_hot_character_occurences[0]

    for anchor_hot_character in anchor_hot_character_instances:
        neighbours = [anchor_hot_character]
        reference_hot_character = anchor_hot_character
        for _, coords_j in enumerate(page_hot_character_occurences[1:]):
            neighbour_hot_character = find_neighbour_coord(
                reference_character=reference_hot_character,
                hot_characters=coords_j,
            )
            if neighbour_hot_character:
                neighbours.append(neighbour_hot_character)
                reference_hot_character = neighbour_hot_character
        if len(neighbours) == max_len:
            adjacent_groups.append(deepcopy(neighbours))
        neighbours = []
    return adjacent_groups


def get_element_dimension(elem: list[HotCharacter]) -> ElementDimension:
    """
    Get the dimensions of an element based on its coordinates.

    Args:
        elem (list): List of coordinates representing an element.

    Returns:
        ElementDimension: ElementDimension object containing the dimensions (x0, x1, y0, y1, span_id).
    """
    x0 = math.floor(min(elem, key=lambda item: item.x).x)
    x1 = math.ceil(max(elem, key=lambda item: item.x_end).x_end)
    y0 = math.floor(elem[0].y)
    y1 = math.ceil(elem[0].y)
    span = elem[0].span_id
    return ElementDimension(x0=x0, x1=x1, y0=y0, y1=y1, span_id=span)


def intersect(bbox1: tuple[int, int, int, int], bbox2: tuple[int, int, int, int]) -> bool:
    """
    Check if two bounding boxes intersect.

    Args:
        bbox1 (tuple): Bounding box 1. (x0, y0, x1, y1)
        bbox2 (tuple): Bounding box 2. (x0, y0, x1, y1)

    Returns:
        bool: True if the bounding boxes intersect, else False.
    """
    return not (bbox2[0] > bbox1[2] or bbox2[2] < bbox1[0] or bbox2[1] > bbox1[3] or bbox2[3] < bbox1[1])
