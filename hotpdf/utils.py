from copy import deepcopy


def find_neighbour_coord(anchor_coord, coords_array, max_distance):
    """
    Find a neighboring coordinate within a specified maximum distance.

    Args:
        anchor_coord (dict): The anchor (start) coordinate.
        coords_array (list): List of coordinates to search.
        max_distance (int): The maximum distance allowed from anchor.

    Returns:
        dict: The neighboring coordinate if found, else None.
    """
    for coord in coords_array:
        if (
            0 <= (coord["x"] - anchor_coord["x"]) <= max_distance + 5
            and anchor_coord["y"] == coord["y"]
        ):
            return coord


def filter_adjacent_coords(text, coords):
    """
    Filter adjacent coordinates based on the given text.

    Args:
        text (str): The text to filter by.
        coords (list): List of coordinates to filter.

    Returns:
        list: List of adjacent coordinate groups.
    """
    if not coords:
        return []

    max_len = len(text)
    adjacent_groups = []
    anchor_coords = coords[0]
    for anchor_coord in anchor_coords:
        neighbours = [anchor_coord]
        for idx, coords_j in enumerate(coords[1:]):
            neighbour_coord = find_neighbour_coord(
                anchor_coord, coords_j, ((idx + 1) * 6)
            )
            if neighbour_coord:
                neighbours.append(neighbour_coord)
        if len(neighbours) == max_len:
            adjacent_groups.append(deepcopy(neighbours))
        neighbours = []
    return adjacent_groups


def get_element_dimension(elem):
    """
    Get the dimensions of an element based on its coordinates.

    Args:
        elem (list): List of coordinates representing an element.

    Returns:
        dict: Dictionary containing the dimensions (x0, x1, y0, y1).
    """
    x0 = min(elem, key=lambda item: item["x"])["x"]
    x1 = max(elem, key=lambda item: item["x_end"])["x_end"]
    y0 = elem[0]["y"]
    y1 = elem[0]["y"]
    return dict(x0=x0, x1=x1, y0=y0, y1=y1)
