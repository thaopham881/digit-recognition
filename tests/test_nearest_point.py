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