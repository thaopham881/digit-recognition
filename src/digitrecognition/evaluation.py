"""Evaluate the digit classifier on MNIST data."""

from time import perf_counter

from digitrecognition.image_representation import (
    BooleanGrid,
    GrayscaleImage,
    Point,
    create_point_set,
)
from digitrecognition.knn import TrainingImage, classify
from digitrecognition.offsets import Offset


PreparedImage = tuple[list[Point], BooleanGrid]


def prepare_training_images(
    images: list[GrayscaleImage],
    labels: list[int],
    threshold: int,
) -> list[TrainingImage]:
    """Convert grayscale training images into point-set representations.

    Args:
        images: Grayscale training images.
        labels: Digit labels corresponding to the images.
        threshold: Grayscale threshold for active pixels.

    Returns:
        Labelled point-set representations ready for k-NN classification.

    Raises:
        ValueError: If the numbers of images and labels do not match.
    """
    if len(images) != len(labels):
        raise ValueError("Images and labels must have the same length.")

    training_images: list[TrainingImage] = []

    for image, label in zip(images, labels):
        points, grid = create_point_set(
            image,
            threshold,
        )

        training_images.append(
            (label, points, grid)
        )

    return training_images


def evaluate_classifier(
    test_images: list[GrayscaleImage],
    test_labels: list[int],
    training_images: list[TrainingImage],
    threshold: int,
    k: int,
    offsets: list[Offset],
    distance_measure: str = "d22",
) -> tuple[int, int, float, float]:
    """Evaluate classification accuracy and running time.

    Args:
        test_images: Grayscale test images.
        test_labels: Correct labels for the test images.
        training_images: Preprocessed labelled training images.
        threshold: Grayscale threshold for active pixels.
        k: Number of nearest neighbours.
        offsets: Precomputed nearest-point search offsets.
        distance_measure: Point-set distance measure to use.

    Returns:
        A tuple containing:
        correct predictions,
        total predictions,
        accuracy percentage,
        elapsed time in seconds.

    Raises:
        ValueError: If the numbers of test images and labels do not match.
    """
    if len(test_images) != len(test_labels):
        raise ValueError("Test images and labels must have the same length.")

    correct = 0
    start_time = perf_counter()

    for image, true_label in zip(test_images, test_labels):
        test_points, test_grid = create_point_set(
            image,
            threshold,
        )

        prediction, _ = classify(
            test_points=test_points,
            test_grid=test_grid,
            training_images=training_images,
            k=k,
            offsets=offsets,
            distance_measure=distance_measure,
        )

        if prediction == true_label:
            correct += 1

    elapsed_time = perf_counter() - start_time
    total = len(test_images)

    if total == 0:
        accuracy = 0.0
    else:
        accuracy = 100.0 * correct / total

    return correct, total, accuracy, elapsed_time