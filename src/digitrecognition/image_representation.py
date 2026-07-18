"""Convert grayscale images into point-set representations."""


Point = tuple[int, int]
GrayscaleImage = list[list[int]]
BooleanGrid = list[list[bool]]


def create_point_set(
    image: GrayscaleImage,
    threshold: int,
) -> tuple[list[Point], BooleanGrid]:
    """Convert an image into coordinates and a Boolean grid.

    Pixels whose values are at least the threshold are treated as
    active pixels belonging to the handwritten digit.

    Args:
        image: A rectangular two-dimensional grayscale image.
        threshold: A grayscale threshold between 0 and 255.

    Returns:
        A coordinate list and a Boolean grid.

    Raises:
        ValueError: If the threshold is invalid or the image is not rectangular.
    """
    if not 0 <= threshold <= 255:
        raise ValueError("Threshold must be between 0 and 255.")

    if not image:
        return [], []

    width = len(image[0])

    if any(len(row) != width for row in image):
        raise ValueError("All image rows must have the same length.")

    coordinates: list[Point] = []
    boolean_grid: BooleanGrid = []

    for row_index, row in enumerate(image):
        boolean_row: list[bool] = []

        for column_index, pixel_value in enumerate(row):
            is_active = pixel_value >= threshold
            boolean_row.append(is_active)

            if is_active:
                coordinates.append((row_index, column_index))

        boolean_grid.append(boolean_row)

    return coordinates, boolean_grid