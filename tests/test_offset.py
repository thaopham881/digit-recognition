"""Tests for coordinate offset generation."""

import pytest

from digitrecognition.offsets import generate_offsets


def test_three_by_three_area_contains_nine_offsets():
    """A 3 × 3 search area should contain nine offsets."""
    offsets = generate_offsets(3)

    assert len(offsets) == 9


def test_first_offset_is_the_centre():
    """The current pixel should be checked first."""
    offsets = generate_offsets(3)

    assert offsets[0] == (0, 0, 0.0)


def test_offsets_are_sorted_by_distance():
    """Distances should be ordered from smallest to largest."""
    offsets = generate_offsets(5)
    distances = [offset[2] for offset in offsets]

    assert distances == sorted(distances)


def test_diagonal_offset_has_correct_distance():
    """A diagonal neighbour should have distance square root of two."""
    offsets = generate_offsets(3)

    diagonal_distance = next(
        distance
        for row, column, distance in offsets
        if row == 1 and column == 1
    )

    assert diagonal_distance == pytest.approx(2 ** 0.5)


def test_even_search_size_raises_error():
    """A search area must have an odd size."""
    with pytest.raises(ValueError):
        generate_offsets(4)


def test_zero_search_size_raises_error():
    """A search area must be larger than zero."""
    with pytest.raises(ValueError):
        generate_offsets(0)