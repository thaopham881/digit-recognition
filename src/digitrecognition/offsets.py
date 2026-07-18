"""Generate coordinate offsets for nearest-point searches."""

from math import hypot


Offset = tuple[int, int, float]


def generate_offsets(search_size: int) -> list[Offset]:
    """Create offsets sorted by increasing Euclidean distance.

    The offsets cover a square area centred on the current pixel.

    Args:
        search_size: The width and height of the search area.
            It must be a positive odd number, such as 3, 5, or 11.

    Returns:
        A list containing row offset, column offset, and distance.

    Raises:
        ValueError: If search_size is not a positive odd number.
    """
    if search_size <= 0 or search_size % 2 == 0:
        raise ValueError("Search size must be a positive odd number.")

    radius = search_size // 2
    offsets: list[Offset] = []

    for row_offset in range(-radius, radius + 1):
        for column_offset in range(-radius, radius + 1):
            distance = hypot(row_offset, column_offset)

            offsets.append(
                (row_offset, column_offset, distance)
            )

    offsets.sort(
        key=lambda offset: (
            offset[2],
            offset[0],
            offset[1],
        )
    )

    return offsets