"""Find the nearest point between point-set image representations."""

from math import hypot

from digitrecognition.image_representation import BooleanGrid, Point
from digitrecognition.offsets import Offset


def is_inside_grid(
    row: int,
    column: int,
    boolean_grid: BooleanGrid,
) -> bool:
    """Check whether a coordinate is inside the Boolean grid."""
    if not boolean_grid:
        return False

    return (
        0 <= row < len(boolean_grid)
        and 0 <= column < len(boolean_grid[0])
    )


def full_search_distance(
    point: Point,
    reference_points: list[Point],
) -> float:
    """Find the nearest reference point using an exhaustive search.

    This function checks the distance to every point in the reference image.
    It is used when the faster local search does not find a nearby point.

    Args:
        point: The point whose nearest neighbour is being searched for.
        reference_points: Active points from the reference image.

    Returns:
        The Euclidean distance to the nearest reference point.

    Raises:
        ValueError: If the reference image contains no active points.
    """
    if not reference_points:
        raise ValueError("Reference image contains no active points.")

    point_row, point_column = point
    smallest_distance = float("inf")

    for reference_row, reference_column in reference_points:
        distance = hypot(
            reference_row - point_row,
            reference_column - point_column,
        )

        if distance < smallest_distance:
            smallest_distance = distance

    return smallest_distance


def nearest_point_distance(
    point: Point,
    reference_grid: BooleanGrid,
    reference_points: list[Point],
    offsets: list[Offset],
) -> float:
    """Find the nearest point using local offsets and a full-search fallback.

    The function first checks nearby positions in the Boolean grid. The
    offsets must be sorted from the smallest distance to the largest.

    If no nearby point is found, the function performs an exhaustive search
    through the reference coordinate list.

    Args:
        point: The active point being compared.
        reference_grid: Boolean representation of the reference image.
        reference_points: Coordinate representation of the reference image.
        offsets: Precomputed offsets sorted by distance.

    Returns:
        The Euclidean distance to the nearest active reference point.
    """
    point_row, point_column = point

    for row_offset, column_offset, distance in offsets:
        candidate_row = point_row + row_offset
        candidate_column = point_column + column_offset

        if not is_inside_grid(
            candidate_row,
            candidate_column,
            reference_grid,
        ):
            continue

        if reference_grid[candidate_row][candidate_column]:
            return distance

    return full_search_distance(point, reference_points)