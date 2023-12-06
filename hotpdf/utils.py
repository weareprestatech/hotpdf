from copy import deepcopy
from .data.classes import HotCharacter


def find_neighbour_coord(
    reference_character: HotCharacter,
    hot_characters: list[HotCharacter],
    max_distance: int = 5,
    span_tolerance: int = 5,
):
    """
    Find a neighbouring coordinate within a specified maximum distance.

    Args:
        reference_coord (HotCharacter): Previous char instance.
        hot_characters (list[HotCharacter]): List of character instances to search through.
        max_distance (int): Maximum distance between reference coordinate and target coordinate.
        span_tolerance (int): Additional distance to consider if text lies in the same span.

    Returns:
        dict: The neighbouring coordinate if found, else None.
    """
    for hot_character in hot_characters:
        # Character end must not be > max_distance than the pre-neighbour
        # But - if it's in the same span: add 5pts to the max_distance
        if (
            0
            <= (hot_character.x - reference_character.x_end)
            <= (
                (max_distance + span_tolerance)
                if hot_character.span_id == reference_character.span_id
                and (hot_character.span_id and reference_character.span_id)
                else max_distance
            )
            and reference_character.y == hot_character.y
        ):
            return hot_character


def filter_adjacent_coords(text: str, hot_characters: list[HotCharacter]):
    """
    Filter adjacent coordinates based on the given text.

    Args:
        text (str): The text to filter by.
        coords (list): List of coordinates to filter.

    Returns:
        list: List of adjacent coordinate groups.
    """
    if not hot_characters:
        return []

    max_len = len(text)
    adjacent_groups = []

    anchor_hot_character_instances = hot_characters[0]

    for anchor_hot_character in anchor_hot_character_instances:
        neighbours = [anchor_hot_character]
        reference_hot_character = anchor_hot_character
        for _, coords_j in enumerate(hot_characters[1:]):
            neighbour_hot_character = find_neighbour_coord(
                reference_hot_character, coords_j
            )
            if neighbour_hot_character:
                neighbours.append(neighbour_hot_character)
                reference_hot_character = neighbour_hot_character
        if len(neighbours) == max_len:
            adjacent_groups.append(deepcopy(neighbours))
        neighbours = []
    return adjacent_groups


def get_element_dimension(elem: list[HotCharacter]):
    """
    Get the dimensions of an element based on its coordinates.

    Args:
        elem (list): List of coordinates representing an element.

    Returns:
        dict: Dictionary containing the dimensions (x0, x1, y0, y1).
    """
    x0 = min(elem, key=lambda item: item.x).x
    x1 = max(elem, key=lambda item: item.x_end).x_end
    y0 = elem[0].y
    y1 = elem[0].y
    return dict(x0=x0, x1=x1, y0=y0, y1=y1)
