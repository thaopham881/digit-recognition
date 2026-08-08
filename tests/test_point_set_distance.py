"""Tests for point-set distance calculations."""

import pytest

from digitrecognition.point_set_distance import (
    directed_average_distance,
    symmetric_average_distance,
)
from digitrecognition.offsets import generate_offsets


def test_identical_point_sets_have_zero_directed_distance():
    """Identical point sets should have distance zero."""
    points = [(0, 0), (1, 1)]
    grid = [
        [True, False],
        [False, True],
    ]
    offsets = generate_offsets(3)

    distance = directed_average_distance(
        source_points=points,
        reference_grid=grid,
        reference_points=points,
        offsets=offsets,
    )

    assert distance == 0.0


def test_shifted_single_points_have_distance_one():
    """Points one position apart should have distance one."""
    points_a = [(0, 0)]
    points_b = [(0, 1)]

    grid_b = [
        [False, True],
    ]

    offsets = generate_offsets(3)

    distance = directed_average_distance(
        source_points=points_a,
        reference_grid=grid_b,
        reference_points=points_b,
        offsets=offsets,
    )

    assert distance == 1.0


def test_directed_distance_uses_average():
    """The function should average all nearest-point distances."""
    points_a = [(0, 0), (0, 1)]
    points_b = [(0, 0)]

    grid_b = [
        [True, False],
    ]

    offsets = generate_offsets(3)

    distance = directed_average_distance(
        source_points=points_a,
        reference_grid=grid_b,
        reference_points=points_b,
        offsets=offsets,
    )

    assert distance == 0.5


def test_symmetric_distance_uses_larger_direction():
    """The symmetric result should use the larger directed value."""
    points_a = [(0, 0), (0, 1)]
    grid_a = [
        [True, True],
    ]

    points_b = [(0, 0)]
    grid_b = [
        [True, False],
    ]

    offsets = generate_offsets(3)

    distance = symmetric_average_distance(
        points_a=points_a,
        grid_a=grid_a,
        points_b=points_b,
        grid_b=grid_b,
        offsets=offsets,
    )

    assert distance == 0.5


def test_empty_source_point_set_raises_error():
    """A directed distance requires at least one source point."""
    with pytest.raises(ValueError):
        directed_average_distance(
            source_points=[],
            reference_grid=[[True]],
            reference_points=[(0, 0)],
            offsets=generate_offsets(3),
        )


def test_empty_reference_point_set_raises_error():
    """A directed distance requires at least one reference point."""
    with pytest.raises(ValueError):
        directed_average_distance(
            source_points=[(0, 0)],
            reference_grid=[[False]],
            reference_points=[],
            offsets=generate_offsets(3),
        )
def test_symmetric_distance_on_larger_28x28_point_sets():
    """Larger shifted point sets should have the expected distance."""
    points_a = [
        (6, 13),
        (7, 13),
        (8, 13),
        (9, 13),
        (10, 13),
        (11, 13),
        (12, 13),
        (13, 13),
        (14, 13),
        (15, 13),
    ]