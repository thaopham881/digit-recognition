"""Tests for k-nearest-neighbours classification."""

import pytest

from digitrecognition.knn import (
    classify,
    find_k_nearest,
    predict_label,
)
from digitrecognition.offsets import generate_offsets


def create_training_image(
    label: int,
    points: list[tuple[int, int]],
    height: int = 3,
    width: int = 3,
) -> tuple[int, list[tuple[int, int]], list[list[bool]]]:
    """Create a small labelled image for testing."""
    grid = [
        [False for _ in range(width)]
        for _ in range(height)
    ]

    for row, column in points:
        grid[row][column] = True

    return label, points, grid


def test_find_k_nearest_returns_images_in_distance_order():
    """Nearest training images should appear first."""
    test_points = [(1, 1)]
    test_grid = [
        [False, False, False],
        [False, True, False],
        [False, False, False],
    ]

    training_images = [
        create_training_image(7, [(1, 2)]),
        create_training_image(2, [(1, 1)]),
        create_training_image(4, [(2, 2)]),
    ]

    neighbours = find_k_nearest(
        test_points=test_points,
        test_grid=test_grid,
        training_images=training_images,
        k=2,
        offsets=generate_offsets(3),
    )

    assert neighbours == [
        (0.0, 2),
        (1.0, 7),
    ]


def test_predict_label_uses_majority_vote():
    """The label with the most votes should be selected."""
    neighbours = [
        (0.1, 3),
        (0.2, 3),
        (0.05, 8),
    ]

    prediction = predict_label(neighbours)

    assert prediction == 3


def test_predict_label_uses_distance_to_break_vote_tie():
    """The smaller total distance should break an equal vote."""
    neighbours = [
        (0.8, 1),
        (0.2, 2),
    ]

    prediction = predict_label(neighbours)

    assert prediction == 2


def test_predict_label_uses_smaller_label_as_final_tie_break():
    """The smaller label should win when votes and distances are equal."""
    neighbours = [
        (0.3, 7),
        (0.3, 4),
    ]

    prediction = predict_label(neighbours)

    assert prediction == 4


def test_empty_neighbour_list_raises_error():
    """Prediction requires at least one neighbour."""
    with pytest.raises(ValueError):
        predict_label([])


def test_empty_training_set_raises_error():
    """Nearest-neighbour searching requires training images."""
    with pytest.raises(ValueError):
        find_k_nearest(
            test_points=[(1, 1)],
            test_grid=[[True]],
            training_images=[],
            k=1,
            offsets=generate_offsets(3),
        )


def test_zero_k_raises_error():
    """The value of k must be greater than zero."""
    training_images = [
        create_training_image(1, [(1, 1)]),
    ]

    with pytest.raises(ValueError):
        find_k_nearest(
            test_points=[(1, 1)],
            test_grid=[
                [False, False, False],
                [False, True, False],
                [False, False, False],
            ],
            training_images=training_images,
            k=0,
            offsets=generate_offsets(3),
        )


def test_k_cannot_exceed_training_set_size():
    """There cannot be more neighbours than training images."""
    training_images = [
        create_training_image(1, [(1, 1)]),
    ]

    with pytest.raises(ValueError):
        find_k_nearest(
            test_points=[(1, 1)],
            test_grid=[
                [False, False, False],
                [False, True, False],
                [False, False, False],
            ],
            training_images=training_images,
            k=2,
            offsets=generate_offsets(3),
        )


def test_classify_returns_prediction_and_neighbours():
    """Classification should return both the label and nearest images."""
    test_points = [(1, 1)]
    test_grid = [
        [False, False, False],
        [False, True, False],
        [False, False, False],
    ]

    training_images = [
        create_training_image(5, [(1, 1)]),
        create_training_image(2, [(1, 2)]),
        create_training_image(9, [(2, 2)]),
    ]

    prediction, neighbours = classify(
        test_points=test_points,
        test_grid=test_grid,
        training_images=training_images,
        k=2,
        offsets=generate_offsets(3),
    )

    assert prediction == 5
    assert neighbours == [
        (0.0, 5),
        (1.0, 2),
    ]