"""Classify point-set images using k-nearest neighbours."""

from digitrecognition.image_representation import BooleanGrid, Point
from digitrecognition.offsets import Offset
from digitrecognition.point_set_distance import (
    d22_distance,
    d23_distance,
    d23_unnormalized_distance,
)


TrainingImage = tuple[int, list[Point], BooleanGrid]
Neighbour = tuple[float, int]


def find_k_nearest(
    test_points: list[Point],
    test_grid: BooleanGrid,
    training_images: list[TrainingImage],
    k: int,
    offsets: list[Offset],
    distance_measure: str = "d22",
) -> list[Neighbour]:
    """Find the k training images closest to a test image.

    Args:
        test_points: Active points from the test image.
        test_grid: Boolean representation of the test image.
        training_images: Labelled reference images. Each item contains
            a label, coordinate list, and Boolean grid.
        k: Number of nearest neighbours to return.
        offsets: Precomputed search offsets sorted by distance.
        distance_measure: Distance measure to use. Supported values are
            "d22", "d23", and "d23_unnormalized".

    Returns:
        A list containing distance-label pairs, ordered from nearest
        to farthest.

    Raises:
        ValueError: If k is invalid, the training set is empty, or the
            distance measure is unknown.
    """
    if not training_images:
        raise ValueError("Training image list cannot be empty.")

    if k <= 0:
        raise ValueError("k must be greater than zero.")

    if k > len(training_images):
        raise ValueError("k cannot exceed the number of training images.")

    distance_functions = {
        "d22": d22_distance,
        "d23": d23_distance,
        "d23_unnormalized": d23_unnormalized_distance,
    }

    if distance_measure not in distance_functions:
        raise ValueError("Unknown distance measure.")

    distance_function = distance_functions[distance_measure]

    neighbours: list[Neighbour] = []

    for label, training_points, training_grid in training_images:
        distance = distance_function(
            points_a=test_points,
            grid_a=test_grid,
            points_b=training_points,
            grid_b=training_grid,
            offsets=offsets,
        )

        neighbours.append((distance, label))

    neighbours.sort(key=lambda neighbour: (neighbour[0], neighbour[1]))

    return neighbours[:k]


def predict_label(neighbours: list[Neighbour]) -> int:
    """Predict a label using majority voting.

    If several labels receive the same number of votes, the label whose
    neighbours have the smallest total distance is selected.

    Args:
        neighbours: Distance-label pairs for the nearest images.

    Returns:
        The predicted digit label.

    Raises:
        ValueError: If the neighbour list is empty.
    """
    if not neighbours:
        raise ValueError("Neighbour list cannot be empty.")

    vote_counts: dict[int, int] = {}
    distance_totals: dict[int, float] = {}

    for distance, label in neighbours:
        vote_counts[label] = vote_counts.get(label, 0) + 1
        distance_totals[label] = distance_totals.get(label, 0.0) + distance

    return min(
        vote_counts,
        key=lambda label: (
            -vote_counts[label],
            distance_totals[label],
            label,
        ),
    )


def classify(
    test_points: list[Point],
    test_grid: BooleanGrid,
    training_images: list[TrainingImage],
    k: int,
    offsets: list[Offset],
    distance_measure: str = "d22",
) -> tuple[int, list[Neighbour]]:
    """Classify a test image and return its nearest neighbours.

    Args:
        test_points: Active points from the test image.
        test_grid: Boolean representation of the test image.
        training_images: Labelled reference images.
        k: Number of nearest neighbours.
        offsets: Precomputed search offsets sorted by distance.
        distance_measure: Distance measure to use. Supported values are
            "d22", "d23", and "d23_unnormalized".

    Returns:
        The predicted label and the selected nearest neighbours.
    """
    neighbours = find_k_nearest(
        test_points=test_points,
        test_grid=test_grid,
        training_images=training_images,
        k=k,
        offsets=offsets,
        distance_measure=distance_measure,
    )

    prediction = predict_label(neighbours)

    return prediction, neighbours