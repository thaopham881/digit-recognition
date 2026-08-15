"""Tests for classifier evaluation."""

import pytest

from digitrecognition.evaluation import (
    evaluate_classifier,
    prepare_training_images,
)
from digitrecognition.offsets import generate_offsets


def test_prepare_training_images():
    """Grayscale images should be converted into labelled point sets."""
    images = [
        [
            [255, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ],
        [
            [0, 0, 0],
            [0, 255, 0],
            [0, 0, 0],
        ],
    ]
    labels = [1, 2]

    prepared = prepare_training_images(
        images,
        labels,
        threshold=128,
    )

    assert len(prepared) == 2

    first_label, first_points, first_grid = prepared[0]

    assert first_label == 1
    assert first_points == [(0, 0)]
    assert first_grid[0][0] is True


def test_prepare_training_images_requires_matching_labels():
    """Each training image must have a corresponding label."""
    images = [
        [
            [255, 0],
            [0, 0],
        ]
    ]

    with pytest.raises(ValueError):
        prepare_training_images(
            images,
            labels=[],
            threshold=128,
        )


def test_evaluate_classifier_correct_prediction():
    """Evaluation should count a correctly classified image."""
    training_images_raw = [
        [
            [255, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ],
        [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 255],
        ],
    ]
    training_labels = [1, 7]

    training_images = prepare_training_images(
        training_images_raw,
        training_labels,
        threshold=128,
    )

    test_images = [
        [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 255],
        ]
    ]

    correct, total, accuracy, elapsed = evaluate_classifier(
        test_images=test_images,
        test_labels=[7],
        training_images=training_images,
        threshold=128,
        k=1,
        offsets=generate_offsets(3),
    )

    assert correct == 1
    assert total == 1
    assert accuracy == pytest.approx(100.0)
    assert elapsed >= 0.0


def test_evaluate_classifier_requires_matching_labels():
    """Each test image must have a corresponding label."""
    with pytest.raises(ValueError):
        evaluate_classifier(
            test_images=[
                [
                    [255, 0],
                    [0, 0],
                ]
            ],
            test_labels=[],
            training_images=[],
            threshold=128,
            k=1,
            offsets=generate_offsets(3),
        )


def test_empty_test_set_has_zero_accuracy():
    """An empty test set should produce zero accuracy."""
    correct, total, accuracy, elapsed = evaluate_classifier(
        test_images=[],
        test_labels=[],
        training_images=[],
        threshold=128,
        k=1,
        offsets=generate_offsets(3),
    )

    assert correct == 0
    assert total == 0
    assert accuracy == 0.0
    assert elapsed >= 0.0