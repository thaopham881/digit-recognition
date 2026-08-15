"""Run a small accuracy experiment on the real MNIST dataset."""

from pathlib import Path

from digitrecognition.evaluation import (
    evaluate_classifier,
    prepare_training_images,
)
from digitrecognition.mnist_loader import (
    load_mnist_images,
    load_mnist_labels,
)
from digitrecognition.offsets import generate_offsets


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIRECTORY = PROJECT_ROOT / "data"

TRAIN_IMAGES_FILE = DATA_DIRECTORY / "train-images-idx3-ubyte.gz"
TRAIN_LABELS_FILE = DATA_DIRECTORY / "train-labels-idx1-ubyte.gz"
TEST_IMAGES_FILE = DATA_DIRECTORY / "t10k-images-idx3-ubyte.gz"
TEST_LABELS_FILE = DATA_DIRECTORY / "t10k-labels-idx1-ubyte.gz"


def main() -> None:
    """Load MNIST data and evaluate the classifier."""
    training_limit = 500
    test_limit = 20
    threshold = 128
    k = 3
    offset_size = 11
    distance_measure = "d22"

    print("Loading MNIST data...")

    training_images_raw = load_mnist_images(
        str(TRAIN_IMAGES_FILE),
        limit=training_limit,
    )
    training_labels = load_mnist_labels(
        str(TRAIN_LABELS_FILE),
        limit=training_limit,
    )

    test_images = load_mnist_images(
        str(TEST_IMAGES_FILE),
        limit=test_limit,
    )
    test_labels = load_mnist_labels(
        str(TEST_LABELS_FILE),
        limit=test_limit,
    )

    print("Preparing training images...")

    training_images = prepare_training_images(
        images=training_images_raw,
        labels=training_labels,
        threshold=threshold,
    )

    offsets = generate_offsets(offset_size)

    print("Running classification...")
    print()

    correct, total, accuracy, elapsed = evaluate_classifier(
        test_images=test_images,
        test_labels=test_labels,
        training_images=training_images,
        threshold=threshold,
        k=k,
        offsets=offsets,
        distance_measure=distance_measure,
    )

    print("MNIST experiment results")
    print("------------------------")
    print(f"Training images: {len(training_images)}")
    print(f"Test images: {total}")
    print(f"Threshold: {threshold}")
    print(f"k: {k}")
    print(f"Offset size: {offset_size}")
    print(f"Distance measure: {distance_measure}")
    print(f"Correct predictions: {correct}/{total}")
    print(f"Accuracy: {accuracy:.2f}%")
    print(f"Elapsed time: {elapsed:.2f} seconds")


if __name__ == "__main__":
    main()