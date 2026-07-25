"""Calculate distances between point-set image representations."""

from digitrecognition.image_representation import BooleanGrid, Point
from digitrecognition.nearest_point import nearest_point_distance
from digitrecognition.offsets import Offset


def directed_average_distance(
    source_points: list[Point],
    reference_grid: BooleanGrid,
    reference_points: list[Point],
    offsets: list[Offset],
) -> float:
    """Calculate the average nearest-point distance from one set to another.

    For every point in the source set, the function finds the nearest point
    in the reference set. It then returns the average of those distances.

    Args:
        source_points: Active points from the source image.
        reference_grid: Boolean representation of the reference image.
        reference_points: Active points from the reference image.
        offsets: Precomputed search offsets sorted by distance.

    Returns:
        The average nearest-point distance from the source set to the
        reference set.

    Raises:
        ValueError: If either point set is empty.
    """
    if not source_points:
        raise ValueError("Source point set cannot be empty.")

    if not reference_points:
        raise ValueError("Reference point set cannot be empty.")

    total_distance = 0.0

    for point in source_points:
        total_distance += nearest_point_distance(
            point=point,
            reference_grid=reference_grid,
            reference_points=reference_points,
            offsets=offsets,
        )

    return total_distance / len(source_points)


def symmetric_average_distance(
    points_a: list[Point],
    grid_a: BooleanGrid,
    points_b: list[Point],
    grid_b: BooleanGrid,
    offsets: list[Offset],
) -> float:
    """Combine directed average distances in both directions.

    The function calculates the distance from A to B and from B to A.
    It returns the larger directed distance.

    Args:
        points_a: Active points from image A.
        grid_a: Boolean representation of image A.
        points_b: Active points from image B.
        grid_b: Boolean representation of image B.
        offsets: Precomputed search offsets sorted by distance.

    Returns:
        The larger of the two directed average distances.
    """
    distance_a_to_b = directed_average_distance(
        source_points=points_a,
        reference_grid=grid_b,
        reference_points=points_b,
        offsets=offsets,
    )

    distance_b_to_a = directed_average_distance(
        source_points=points_b,
        reference_grid=grid_a,
        reference_points=points_a,
        offsets=offsets,
    )

    return max(distance_a_to_b, distance_b_to_a)