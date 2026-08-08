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

def directed_sum_distance(
    source_points: list[Point],
    reference_grid: BooleanGrid,
    reference_points: list[Point],
    offsets: list[Offset],
) -> float:
    """Calculate the sum of nearest-point distances from one set to another.

    Unlike directed_average_distance, this function does not divide the
    total by the number of source points.

    Args:
        source_points: Active points from the source image.
        reference_grid: Boolean representation of the reference image.
        reference_points: Active points from the reference image.
        offsets: Precomputed search offsets sorted by distance.

    Returns:
        The sum of nearest-point distances from the source set to the
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

    return total_distance


def d22_distance(
    points_a: list[Point],
    grid_a: BooleanGrid,
    points_b: list[Point],
    grid_b: BooleanGrid,
    offsets: list[Offset],
) -> float:
    """Calculate the D22 distance between two point sets.

    D22 is the larger of the two directed average nearest-point
    distances: A to B and B to A.

    Args:
        points_a: Active points from image A.
        grid_a: Boolean representation of image A.
        points_b: Active points from image B.
        grid_b: Boolean representation of image B.
        offsets: Precomputed search offsets sorted by distance.

    Returns:
        The D22 distance between the two point sets.
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

def d23_distance(
    points_a: list[Point],
    grid_a: BooleanGrid,
    points_b: list[Point],
    grid_b: BooleanGrid,
    offsets: list[Offset],
) -> float:
    """Calculate the D23 distance between two point sets.

    D23 is the average of the two directed average nearest-point
    distances: A to B and B to A.

    Args:
        points_a: Active points from image A.
        grid_a: Boolean representation of image A.
        points_b: Active points from image B.
        grid_b: Boolean representation of image B.
        offsets: Precomputed search offsets sorted by distance.

    Returns:
        The D23 distance between the two point sets.
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

    return (distance_a_to_b + distance_b_to_a) / 2

def d23_unnormalized_distance(
    points_a: list[Point],
    grid_a: BooleanGrid,
    points_b: list[Point],
    grid_b: BooleanGrid,
    offsets: list[Offset],
) -> float:
    """Calculate D23 without normalizing the directed distances.

    The nearest-point distances are summed in both directions instead
    of being divided by the number of source points. The two directed
    sums are then averaged.

    Args:
        points_a: Active points from image A.
        grid_a: Boolean representation of image A.
        points_b: Active points from image B.
        grid_b: Boolean representation of image B.
        offsets: Precomputed search offsets sorted by distance.

    Returns:
        The unnormalized D23 distance between the two point sets.
    """
    distance_a_to_b = directed_sum_distance(
        source_points=points_a,
        reference_grid=grid_b,
        reference_points=points_b,
        offsets=offsets,
    )

    distance_b_to_a = directed_sum_distance(
        source_points=points_b,
        reference_grid=grid_a,
        reference_points=points_a,
        offsets=offsets,
    )

    return (distance_a_to_b + distance_b_to_a) / 2

def symmetric_average_distance(
    points_a: list[Point],
    grid_a: BooleanGrid,
    points_b: list[Point],
    grid_b: BooleanGrid,
    offsets: list[Offset],
) -> float:
    """Return the D22 distance using the earlier function name."""
    return d22_distance(
        points_a=points_a,
        grid_a=grid_a,
        points_b=points_b,
        grid_b=grid_b,
        offsets=offsets,
    )