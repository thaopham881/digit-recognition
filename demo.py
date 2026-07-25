"""Small command-line demonstration of digit classification."""

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


def display_image(boolean_grid: list[list[bool]]) -> None:
    """Print a Boolean image using visible text characters."""
    for row in boolean_grid:
        print(" ".join("#" if pixel else "." for pixel in row))


def prepare_training_image(
    label: int,
    image: list[list[int]],
    threshold: int,
) -> tuple[int, list[tuple[int, int]], list[list[bool]]]:
    """Convert a labelled grayscale image into training data."""
    points, grid = create_point_set(image, threshold)

    return label, points, grid


def read_choice(
    prompt: str,
    allowed_values: set[int],
) -> int:
    """Read an integer belonging to the allowed set."""
    while True:
        try:
            value = int(input(prompt))

            if value in allowed_values:
                return value

        except ValueError:
            pass

        allowed_text = ", ".join(
            str(value) for value in sorted(allowed_values)
        )
        print(f"Please enter one of these values: {allowed_text}")


def main() -> None:
    """Run a small digit-classification demonstration."""
    threshold = 128
    offsets = generate_offsets(5)

    training_images = [
        prepare_training_image(1, DIGIT_ONE_A, threshold),
        prepare_training_image(1, DIGIT_ONE_B, threshold),
        prepare_training_image(7, DIGIT_SEVEN_A, threshold),
        prepare_training_image(7, DIGIT_SEVEN_B, threshold),
    ]

    test_images = {
        1: TEST_ONE,
        7: TEST_SEVEN,
    }

    print("Handwritten digit recognition demonstration")
    print("------------------------------------------")
    print("This demonstration currently recognises digits 1 and 7.")
    print()

    selected_digit = read_choice(
        "Select a test image (1 or 7): ",
        {1, 7},
    )

    k = read_choice(
        "Choose k (1, 2, 3, or 4): ",
        {1, 2, 3, 4},
    )

    test_points, test_grid = create_point_set(
        test_images[selected_digit],
        threshold,
    )

    prediction, neighbours = classify(
        test_points=test_points,
        test_grid=test_grid,
        training_images=training_images,
        k=k,
        offsets=offsets,
    )

    print()
    print("Selected test image:")
    display_image(test_grid)

    print()
    print(f"Predicted label: {prediction}")
    print()
    print("Nearest reference images:")

    for position, (distance, label) in enumerate(
        neighbours,
        start=1,
    ):
        print(
            f"{position}. Label {label}, "
            f"distance {distance:.3f}"
        )


if __name__ == "__main__":
    main()