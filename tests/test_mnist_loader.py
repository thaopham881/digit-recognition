"""Tests for loading MNIST IDX gzip files."""

import gzip
import struct

import pytest

from digitrecognition.mnist_loader import (
    load_mnist_images,
    load_mnist_labels,
)


def write_image_file(
    file_path,
    images: list[bytes],
    magic_number: int = 2051,
    rows: int = 28,
    columns: int = 28,
) -> None:
    """Create a small artificial MNIST image file for testing."""
    with gzip.open(file_path, "wb") as file:
        file.write(
            struct.pack(
                ">IIII",
                magic_number,
                len(images),
                rows,
                columns,
            )
        )

        for image in images:
            file.write(image)


def write_label_file(
    file_path,
    labels: list[int],
    magic_number: int = 2049,
) -> None:
    """Create a small artificial MNIST label file for testing."""
    with gzip.open(file_path, "wb") as file:
        file.write(
            struct.pack(
                ">II",
                magic_number,
                len(labels),
            )
        )
        file.write(bytes(labels))


def test_load_mnist_images(tmp_path):
    """Valid MNIST images should be loaded as 28 x 28 grids."""
    file_path = tmp_path / "images.gz"

    first_image = bytes([0] * (28 * 28))
    second_image = bytes([255] * (28 * 28))

    write_image_file(
        file_path,
        [first_image, second_image],
    )

    images = load_mnist_images(str(file_path))

    assert len(images) == 2
    assert len(images[0]) == 28
    assert len(images[0][0]) == 28
    assert images[0][0][0] == 0
    assert images[1][0][0] == 255


def test_image_limit_is_respected(tmp_path):
    """Image loading should support an optional limit."""
    file_path = tmp_path / "images.gz"

    images = [
        bytes([0] * (28 * 28)),
        bytes([100] * (28 * 28)),
        bytes([200] * (28 * 28)),
    ]

    write_image_file(file_path, images)

    loaded_images = load_mnist_images(
        str(file_path),
        limit=2,
    )

    assert len(loaded_images) == 2


def test_invalid_image_magic_number_raises_error(tmp_path):
    """An invalid image magic number should be rejected."""
    file_path = tmp_path / "images.gz"

    write_image_file(
        file_path,
        [bytes([0] * (28 * 28))],
        magic_number=9999,
    )

    with pytest.raises(ValueError):
        load_mnist_images(str(file_path))


def test_invalid_image_dimensions_raise_error(tmp_path):
    """MNIST image dimensions must be 28 x 28."""
    file_path = tmp_path / "images.gz"

    write_image_file(
        file_path,
        [],
        rows=27,
        columns=28,
    )

    with pytest.raises(ValueError):
        load_mnist_images(str(file_path))


def test_truncated_image_file_raises_error(tmp_path):
    """Incomplete image data should be rejected."""
    file_path = tmp_path / "images.gz"

    with gzip.open(file_path, "wb") as file:
        file.write(struct.pack(">IIII", 2051, 1, 28, 28))
        file.write(bytes([0] * 10))

    with pytest.raises(ValueError):
        load_mnist_images(str(file_path))


def test_invalid_image_limit_raises_error(tmp_path):
    """Image limit must be positive."""
    file_path = tmp_path / "images.gz"

    with pytest.raises(ValueError):
        load_mnist_images(
            str(file_path),
            limit=0,
        )


def test_load_mnist_labels(tmp_path):
    """Valid MNIST labels should be loaded correctly."""
    file_path = tmp_path / "labels.gz"

    write_label_file(
        file_path,
        [3, 7, 1],
    )

    labels = load_mnist_labels(str(file_path))

    assert labels == [3, 7, 1]


def test_label_limit_is_respected(tmp_path):
    """Label loading should support an optional limit."""
    file_path = tmp_path / "labels.gz"

    write_label_file(
        file_path,
        [1, 2, 3, 4],
    )

    labels = load_mnist_labels(
        str(file_path),
        limit=2,
    )

    assert labels == [1, 2]


def test_invalid_label_magic_number_raises_error(tmp_path):
    """An invalid label magic number should be rejected."""
    file_path = tmp_path / "labels.gz"

    write_label_file(
        file_path,
        [1],
        magic_number=9999,
    )

    with pytest.raises(ValueError):
        load_mnist_labels(str(file_path))


def test_truncated_label_file_raises_error(tmp_path):
    """Incomplete label data should be rejected."""
    file_path = tmp_path / "labels.gz"

    with gzip.open(file_path, "wb") as file:
        file.write(struct.pack(">II", 2049, 3))
        file.write(bytes([1]))

    with pytest.raises(ValueError):
        load_mnist_labels(str(file_path))


def test_invalid_label_limit_raises_error(tmp_path):
    """Label limit must be positive."""
    file_path = tmp_path / "labels.gz"

    with pytest.raises(ValueError):
        load_mnist_labels(
            str(file_path),
            limit=0,
        )