"""Tests for nearest-point searching."""

import pytest

from digitrecognition.nearest_point import (
    full_search_distance,
    is_inside_grid,
    nearest_point_distance,
)
from digitrecognition.offsets import generate_offsets


def test_coordinate_inside_grid():
    """A valid coordinate should be inside the grid."""
    grid = [
        [False, False],
        [False, True],
    ]

    assert is_inside_grid(1, 1, grid) is True


def test_coordinate_outside_grid():
    """Invalid coordinates should be outside the grid."""
    grid = [
        [False, False],
        [False, True],
    ]

    assert is_inside_grid(-1, 0, grid) is False
    assert is_inside_grid(2, 0, grid) is False
    assert is_inside_grid(0, 2, grid) is False


def test_same_position_has_zero_distance():
    """A point at the same position should have distance zero."""
    reference_grid = [
        [False, False, False],
        [False, True, False],
        [False, False, False],
    ]
    reference_points = [(1, 1)]
    offsets = generate_offsets(3)

    distance = nearest_point_distance(
        point=(1, 1),
        reference_grid=reference_grid,
        reference_points=reference_points,
        offsets=offsets,
    )

    assert distance == 0.0


def test_adjacent_point_has_distance_one():
    """A neighbouring point should have distance one."""
    reference_grid = [
        [False, False, False],
        [False, False, True],
        [False, False, False],
    ]
    reference_points = [(1, 2)]
    offsets = generate_offsets(3)

    distance = nearest_point_distance(
        point=(1, 1),
        reference_grid=reference_grid,
        reference_points=reference_points,
        offsets=offsets,
    )

    assert distance == 1.0


def test_diagonal_point_has_correct_distance():
    """A diagonal point should have distance square root of two."""
    reference_grid = [
        [False, False, False],
        [False, False, False],
        [False, False, True],
    ]
    reference_points = [(2, 2)]
    offsets = generate_offsets(3)

    distance = nearest_point_distance(
        point=(1, 1),
        reference_grid=reference_grid,
        reference_points=reference_points,
        offsets=offsets,
    )

    assert distance == pytest.approx(2 ** 0.5)


def test_full_search_fallback_finds_distant_point():
    """The fallback should find a point outside the local search area."""
    reference_grid = [
        [False, False, False, False, False],
        [False, False, False, False, False],
        [False, False, False, False, False],
        [False, False, False, False, False],
        [False, False, False, False, True],
    ]
    reference_points = [(4, 4)]
    offsets = generate_offsets(3)

    distance = nearest_point_distance(
        point=(0, 0),
        reference_grid=reference_grid,
        reference_points=reference_points,
        offsets=offsets,
    )

    assert distance == pytest.approx(32 ** 0.5)


def test_full_search_returns_smallest_distance():
    """Full search should return the closest reference point."""
    reference_points = [
        (5, 5),
        (1, 2),
        (9, 9),
    ]

    distance = full_search_distance(
        point=(1, 1),
        reference_points=reference_points,
    )

    assert distance == 1.0
    
def test_empty_reference_points_raise_error():
    """An empty reference image should raise an error."""
    with pytest.raises(ValueError):
        full_search_distance((0, 0), [])


def test_empty_grid_is_outside():
    """A coordinate cannot be inside an empty grid."""
    assert is_inside_grid(0, 0, []) is False


def test_nearest_point_matches_full_search_on_larger_grid():
    """Optimized search should match exhaustive search on a 28x28 grid."""
    reference_points = [
        (2, 3),
        (5, 20),
        (10, 10),
        (14, 18),
        (20, 5),
        (25, 24),
    ]

    reference_grid = [
        [False for _ in range(28)]
        for _ in range(28)
    ]

    for row, column in reference_points:
        reference_grid[row][column] = True

    offsets = generate_offsets(11)

    test_points = [
        (0, 0),
        (4, 18),
        (11, 11),
        (18, 6),
        (27, 27),
    ]

    for point in test_points:
        optimized_distance = nearest_point_distance(
            point=point,
            reference_grid=reference_grid,
            reference_points=reference_points,
            offsets=offsets,
        )

        exhaustive_distance = full_search_distance(
            point=point,
            reference_points=reference_points,
        )

        assert optimized_distance == pytest.approx(exhaustive_distance)

def test_local_corner_point_does_not_hide_closer_outside_point():
    """Search should still return the globally nearest reference point."""
    grid = [[False for _ in range(15)] for _ in range(15)]

    # Query point is in the centre.
    query_point = (7, 7)

    # This point is inside an 11x11 local search square:
    # displacement (5, 5), distance sqrt(50) ≈ 7.07.
    grid[12][12] = True

    # This point is outside the local square but is actually closer:
    # displacement (6, 0), distance 6.
    grid[13][7] = True

    reference_points = [
        (12, 12),
        (13, 7),
    ]

    optimized_distance = nearest_point_distance(
        point=query_point,
        reference_grid=grid,
        reference_points=reference_points,
        offsets=generate_offsets(11),
    )

    exhaustive_distance = full_search_distance(
        point=query_point,
        reference_points=reference_points,
    )

    assert optimized_distance == pytest.approx(exhaustive_distance)
    assert optimized_distance == pytest.approx(6.0)