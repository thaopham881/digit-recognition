"""Integration tests for the complete classification pipeline."""

from digitrecognition.image_representation import create_point_set
from digitrecognition.knn import classify
from digitrecognition.offsets import generate_offsets


DIGIT_ONE_A = [
    [0, 255, 0, 0, 0],
    [255, 255, 0, 0, 0],
    [0, 255, 0, 0, 0],
    [0, 255, 0, 0, 0],
    [255, 255, 255, 0, 0],
]

DIGIT_ONE_B = [
    [0, 0, 255, 0, 0],
    [0, 255, 255, 0, 0],
    [0, 0, 255, 0, 0],
    [0, 0, 255, 0, 0],
    [0, 255, 255, 255, 0],
]

DIGIT_SEVEN_A = [
    [255, 255, 255, 255, 0],
    [0, 0, 0, 255, 0],
    [0, 0, 255, 0, 0],
    [0, 255, 0, 0, 0],
    [0, 255, 0, 0, 0],
]

DIGIT_SEVEN_B = [
    [0, 255, 255, 255, 255],
    [0, 0, 0, 255, 0],
    [0, 0, 255, 0, 0],
    [0, 255, 0, 0, 0],
    [0, 255, 0, 0, 0],
]

TEST_ONE = [
    [0, 255, 0, 0, 0],
    [0, 255, 0, 0, 0],
    [0, 255, 0, 0, 0],
    [0, 255, 0, 0, 0],
    [0, 255, 255, 0, 0],
]

TEST_SEVEN = [
    [255, 255, 255, 255, 0],
    [0, 0, 0, 255, 0],
    [0, 0, 255, 0, 0],
    [0, 255, 0, 0, 0],
    [255, 0, 0, 0, 0],
]


def prepare_training_image(
    label: int,
    image: list[list[int]],
    threshold: int,
) -> tuple[int, list[tuple[int, int]], list[list[bool]]]:
    """Convert an image into the format expected by the classifier."""
    points, grid = create_point_set(image, threshold)

    return label, points, grid


def create_training_set(
    threshold: int,
) -> list[tuple[int, list[tuple[int, int]], list[list[bool]]]]:
    """Create a small labelled training set."""
    return [
        prepare_training_image(1, DIGIT_ONE_A, threshold),
        prepare_training_image(1, DIGIT_ONE_B, threshold),
        prepare_training_image(7, DIGIT_SEVEN_A, threshold),
        prepare_training_image(7, DIGIT_SEVEN_B, threshold),
    ]


def test_complete_pipeline_classifies_digit_one():
    """The complete pipeline should classify the artificial digit one."""
    threshold = 128
    test_points, test_grid = create_point_set(TEST_ONE, threshold)

    prediction, neighbours = classify(
        test_points=test_points,
        test_grid=test_grid,
        training_images=create_training_set(threshold),
        k=3,
        offsets=generate_offsets(5),
    )

    assert prediction == 1
    assert len(neighbours) == 3
    assert neighbours == sorted(neighbours)


def test_complete_pipeline_classifies_digit_seven():
    """The complete pipeline should classify the artificial digit seven."""
    threshold = 128
    test_points, test_grid = create_point_set(TEST_SEVEN, threshold)

    prediction, neighbours = classify(
        test_points=test_points,
        test_grid=test_grid,
        training_images=create_training_set(threshold),
        k=3,
        offsets=generate_offsets(5),
    )

    assert prediction == 7
    assert len(neighbours) == 3
    assert neighbours == sorted(neighbours)