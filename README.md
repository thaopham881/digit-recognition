# Handwritten Digit Recognition

This project is being developed for the University of Helsinki Algorithms Laboratory course.

The goal is to recognize handwritten digits using the k-nearest neighbours algorithm and point-set distance measures. Grayscale images are converted into coordinate lists and Boolean grids. The program then compares the shapes of two digits by measuring nearest-point distances between their active pixels.

The core algorithms are implemented manually without using a ready-made k-nearest-neighbours classifier or pre-built matrix distance operations.

## Current status

The project contains a complete handwritten-digit classification pipeline that can be tested using both artificial images and real images from the MNIST dataset.

Implemented functionality includes:

* converting grayscale images into coordinate lists and Boolean grids;
* generating coordinate offsets sorted by Euclidean distance;
* optimized nearest-point searching using a Boolean grid;
* exhaustive fallback searching using coordinate lists;
* directed average nearest-point distance calculation;
* directed sum nearest-point distance calculation;
* D22 point-set distance;
* D23 point-set distance;
* an unnormalized D23 variation;
* selecting the point-set distance measure used by k-nearest neighbours;
* selecting the k nearest reference images;
* maintaining the k nearest neighbours using a binary max-heap;
* majority voting with deterministic tie-breaking;
* loading MNIST image and label files;
* converting MNIST images into point-set representations;
* evaluating classification predictions;
* running a small classification experiment using real MNIST images;
* a command-line demonstration using artificial images of digits 1 and 7;
* automated unit and integration tests;
* test-coverage tracking with pytest-cov;
* code-quality analysis with Pylint.

At the current stage:

* 72 automated tests pass;
* source-code test coverage is 99%;
* Pylint gives the project a score of 9.56 out of 10;
* a small MNIST experiment correctly classified 19 out of 20 test images, giving 95% accuracy.

## Distance measures

The project implements three point-set distance measures.

### D22

D22 calculates the directed average nearest-point distance in both directions between two point sets and returns the larger value.

### D23

D23 calculates the directed average nearest-point distance in both directions and returns the average of the two values.

### Unnormalized D23

The unnormalized D23 variation uses directed sums instead of dividing the nearest-point distance total by the number of source points.

The k-nearest-neighbours classifier can use any of these three distance measures.

The supported distance-measure names are:

```text
d22
d23
d23_unnormalized
```

D22 is currently used by default.

## Running the project

Install the dependencies:

```bash
poetry install
```

### Artificial digit demonstration

Run the original artificial-image demonstration with:

```bash
poetry run python demo.py
```

The demonstration asks the user to:

1. select an artificial test image representing digit 1 or 7;
2. select a value of `k` between 1 and 4.

It then displays the selected image, predicted label, and nearest reference images with their distances.

### MNIST experiment

Run the real MNIST experiment with:

```bash
poetry run python -m digitrecognition.mnist_experiment
```

The current default experiment uses:

* 500 training images;
* 20 test images;
* grayscale threshold 128;
* `k = 3`;
* offset size 11;
* D22 distance.

One experimental run produced:

```text
MNIST experiment results
------------------------
Training images: 500
Test images: 20
Threshold: 128
k: 3
Offset size: 11
Distance measure: d22
Correct predictions: 19/20
Accuracy: 95.00%
Elapsed time: 54.02 seconds
```

The exact running time may vary depending on the computer.

## Running the tests

Run all automated tests:

```bash
poetry run pytest
```

The current test suite contains 72 tests.

Run the tests with coverage:

```bash
poetry run pytest --cov=digitrecognition --cov-report=term-missing
```

The current source-code coverage is 99%.

The only currently uncovered statement is the script entry-point call in `mnist_experiment.py`; the implemented algorithms themselves are covered by the automated tests.

Run the code-quality analysis with:

```bash
poetry run pylint src tests
```

The current Pylint score is 9.56 out of 10.

## Testing

The test suite includes unit and integration tests for:

* grayscale image conversion;
* threshold validation;
* Boolean-grid and coordinate-list representations;
* offset generation and ordering;
* optimized nearest-point searching;
* exhaustive nearest-point searching;
* agreement between optimized and exhaustive search;
* directed average distance;
* directed sum distance;
* D22;
* D23;
* the unnormalized D23 variation;
* k-nearest-neighbour selection;
* binary max-heap operations;
* selectable distance measures;
* majority voting;
* deterministic tie-breaking;
* MNIST image and label loading;
* MNIST data preparation;
* classification evaluation;
* the MNIST experiment;
* invalid input handling;
* the complete artificial classification pipeline.

Some tests use 28 × 28 artificial inputs to more closely represent the dimensions of MNIST images.

These larger tests were added after peer-review feedback suggested using more representative inputs in addition to small manually constructed examples.

## MNIST evaluation

The project can now classify real handwritten digits from the MNIST dataset.

The current experiment intentionally uses a relatively small subset of MNIST because point-set distance calculation is computationally expensive.

For every test image, distances must be calculated against multiple training images. The classifier therefore uses a fixed-size binary max-heap to retain only the current `k` nearest neighbours instead of sorting every calculated distance.

With 500 training images and 20 test images, one experiment achieved:

* 19 correct predictions out of 20;
* 95% classification accuracy;
* approximately 54 seconds execution time.

This experiment demonstrates that the implemented point-set algorithms can be used to recognize real handwritten digit images. It is not intended to achieve state-of-the-art MNIST performance.

## Current limitations

The main current limitations are:

* point-set distance calculations are computationally expensive;
* the MNIST experiment currently uses only a small subset of the full dataset;
* D22, D23, and unnormalized D23 have not yet been systematically compared on larger MNIST experiments;
* large-scale performance using the complete MNIST dataset has not been evaluated;
* the artificial command-line demo includes only digits 1 and 7;
* the artificial demo does not allow the user to select the distance measure.

## Project structure

```text
digit-recognition/
├── data/
├── docs/
│   ├── implementation.md
│   ├── specification.md
│   ├── testing.md
│   ├── user_guide.md
│   ├── weekly_report_1.md
│   ├── weekly_report_2.md
│   ├── weekly_report_3.md
│   ├── weekly_report_4.md
│   └── weekly_report_5.md
├── src/
│   └── digitrecognition/
│       ├── __init__.py
│       ├── evaluation.py
│       ├── image_representation.py
│       ├── knn.py
│       ├── max_heap.py
│       ├── mnist_experiment.py
│       ├── mnist_loader.py
│       ├── nearest_point.py
│       ├── offsets.py
│       └── point_set_distance.py
├── tests/
│   ├── test_evaluation.py
│   ├── test_image_representation.py
│   ├── test_integration.py
│   ├── test_knn.py
│   ├── test_max_heap.py
│   ├── test_mnist_experiment.py
│   ├── test_mnist_loader.py
│   ├── test_nearest_point.py
│   ├── test_offset.py
│   └── test_point_set_distance.py
├── demo.py
├── pyproject.toml
└── README.md
```

## Documentation

* [Specification document](docs/specification.md)
* [Implementation document](docs/implementation.md)
* [Testing document](docs/testing.md)
* [User guide](docs/user_guide.md)
* [Weekly Report 1](docs/weekly_report_1.md)
* [Weekly Report 2](docs/weekly_report_2.md)
* [Weekly Report 3](docs/weekly_report_3.md)
* [Weekly Report 4](docs/weekly_report_4.md)
* [Weekly Report 5](docs/weekly_report_5.md)

## Peer review

The first peer review has been completed.

Peer-review feedback on this project suggested adding larger and more representative tests. In response, additional 28 × 28 tests were added for nearest-point searching and point-set distance calculations.

## Technologies

* Python 3.12
* Poetry
* pytest
* pytest-cov
* Pylint

## Next steps

The remaining development and documentation tasks include:

* document the MNIST integration and max-heap optimization;
* document the final testing results;
* compare the implemented distance measures where practical;
* document the performance limitations of the point-set approach;
* complete the Week 6 report;
* complete the final project documentation;
* prepare the repository for the final peer review and submission.
