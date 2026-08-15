"""Load MNIST images and labels from IDX gzip files."""

import gzip
import struct


GrayscaleImage = list[list[int]]


def load_mnist_images(
    file_path: str,
    limit: int | None = None,
) -> list[GrayscaleImage]:
    """Load grayscale MNIST images from a compressed IDX file.

    Args:
        file_path: Path to the MNIST image .gz file.
        limit: Optional maximum number of images to load.

    Returns:
        A list of 28 x 28 grayscale images.

    Raises:
        ValueError: If the file does not contain MNIST image data or
            if limit is invalid.
    """
    if limit is not None and limit <= 0:
        raise ValueError("Limit must be greater than zero.")

    with gzip.open(file_path, "rb") as file:
        magic_number, image_count, rows, columns = struct.unpack(
            ">IIII",
            file.read(16),
        )

        if magic_number != 2051:
            raise ValueError("Invalid MNIST image file.")

        if rows != 28 or columns != 28:
            raise ValueError("Expected 28 x 28 MNIST images.")

        number_to_load = image_count

        if limit is not None:
            number_to_load = min(limit, image_count)

        images: list[GrayscaleImage] = []

        for _ in range(number_to_load):
            pixel_bytes = file.read(rows * columns)

            if len(pixel_bytes) != rows * columns:
                raise ValueError("MNIST image file ended unexpectedly.")

            image = [
                list(pixel_bytes[row * columns : (row + 1) * columns])
                for row in range(rows)
            ]

            images.append(image)

    return images


def load_mnist_labels(
    file_path: str,
    limit: int | None = None,
) -> list[int]:
    """Load MNIST labels from a compressed IDX file.

    Args:
        file_path: Path to the MNIST label .gz file.
        limit: Optional maximum number of labels to load.

    Returns:
        A list of digit labels.

    Raises:
        ValueError: If the file does not contain MNIST label data or
            if limit is invalid.
    """
    if limit is not None and limit <= 0:
        raise ValueError("Limit must be greater than zero.")

    with gzip.open(file_path, "rb") as file:
        magic_number, label_count = struct.unpack(
            ">II",
            file.read(8),
        )

        if magic_number != 2049:
            raise ValueError("Invalid MNIST label file.")

        number_to_load = label_count

        if limit is not None:
            number_to_load = min(limit, label_count)

        label_bytes = file.read(number_to_load)

        if len(label_bytes) != number_to_load:
            raise ValueError("MNIST label file ended unexpectedly.")

    return list(label_bytes)