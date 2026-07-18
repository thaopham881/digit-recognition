"""Tests for grayscale image conversion."""

import pytest

from digitrecognition.image_representation import create_point_set


def test_create_point_set_returns_correct_coordinates():
    """Active pixels should be stored as coordinates."""
    image = [
        [0, 100, 200],
        [20, 180, 255],
    ]

    coordinates, _ = create_point_set(image, threshold=128)

    assert coordinates == [(0, 2), (1, 1), (1, 2)]


def test_create_point_set_returns_correct_boolean_grid():
    """The Boolean grid should mark active pixels."""
    image = [
        [0, 100, 200],
        [20, 180, 255],
    ]

    _, boolean_grid = create_point_set(image, threshold=128)

    assert boolean_grid == [
        [False, False, True],
        [False, True, True],
    ]


def test_pixel_equal_to_threshold_is_active():
    """A pixel equal to the threshold should be active."""
    image = [[127, 128, 129]]

    coordinates, _ = create_point_set(image, threshold=128)

    assert coordinates == [(0, 1), (0, 2)]


def test_empty_image_returns_empty_results():
    """An empty image should produce empty representations."""
    coordinates, boolean_grid = create_point_set([], threshold=128)

    assert coordinates == []
    assert boolean_grid == []


def test_invalid_threshold_raises_error():
    """Threshold values must be between 0 and 255."""
    with pytest.raises(ValueError):
        create_point_set([[0, 255]], threshold=300)


def test_unequal_row_lengths_raise_error():
    """The image must be rectangular."""
    image = [
        [0, 100],
        [200],
    ]

    with pytest.raises(ValueError):
        create_point_set(image, threshold=128)