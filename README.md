# Handwritten Digit Recognition

This project is being developed for the University of Helsinki Algorithms
Laboratory course.

The goal is to recognize handwritten digits using the k-nearest neighbours
algorithm and point-set distance measures. Grayscale images are converted into
coordinate lists and Boolean grids. The program then compares the shapes of
two digits by measuring nearest-point distances between their active pixels.

The core algorithms are implemented manually without using a ready-made
k-nearest-neighbours classifier or pre-built matrix distance operations.

## Current status

The project currently contains a working digit-classification pipeline using
artificial grayscale images.

Implemented functionality includes:

- converting grayscale images into coordinate lists and Boolean grids;
- generating coordinate offsets sorted by Euclidean distance;
- optimized nearest-point searching using a Boolean grid;
- exhaustive fallback searching using coordinate lists;
- directed average nearest-point distance calculation;
- directed sum nearest-point distance calculation;
- D22 point-set distance;
- D23 point-set distance;
- an unnormalized D23 variation;
- selecting the k nearest reference images;
- selecting the point-set distance measure used by k-nearest neighbours;
- majority voting with deterministic tie-breaking;
- a command-line demonstration using artificial images of digits 1 and 7;
- automated unit and integration tests;
- test-coverage tracking with pytest-cov;
- code-quality analysis with Pylint.

At the current stage:

- 48 automated tests pass;
- source-code test coverage is 100%;
- Pylint gives the project a score of 9.34 out of 10.

## Distance measures

The project currently implements three point-set distance measures.

### D22

D22 calculates the directed average nearest-point distance in both directions
between two point sets and returns the larger value.

### D23

D23 calculates the directed average nearest-point distance in both directions
and returns the average of the two values.

### Unnormalized D23

The unnormalized D23 variation uses directed sums instead of dividing the
nearest-point distance total by the number of source points.

The k-nearest-neighbours classifier can use any of these three distance
measures.

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

Run the current demonstration:

```bash
poetry run python demo.py
```

The demonstration asks the user to:

1. select an artificial test image representing digit 1 or 7;
2. select a value of `k` between 1 and 4.

It then displays the selected image, predicted label, and nearest reference
images with their distances.

The current demonstration uses D22 as its distance measure.

## Running the tests

Run all automated tests:

```bash
poetry run pytest
```

The current test suite contains 48 tests.

Run the tests with coverage:

```bash
poetry run pytest --cov=digitrecognition --cov-report=term-missing
```

The current source-code coverage is 100%.

Run the code-quality analysis:

```bash
poetry run pylint src/digitrecognition demo.py
```

The current Pylint score is 9.34 out of 10.

## Testing

The test suite includes unit and integration tests for:

- grayscale image conversion;
- threshold validation;
- Boolean-grid and coordinate-list representations;
- offset generation and ordering;
- optimized nearest-point searching;
- exhaustive nearest-point searching;
- agreement between optimized and exhaustive search;
- directed average distance;
- directed sum distance;
- D22;
- D23;
- the unnormalized D23 variation;
- k-nearest-neighbour selection;
- selectable distance measures;
- majority voting;
- deterministic tie-breaking;
- invalid input handling;
- the complete artificial classification pipeline.

Some tests use 28 × 28 artificial inputs to more closely represent the
dimensions of MNIST images.

These larger tests were added after peer-review feedback suggested using more
representative inputs in addition to small manually constructed examples.

## Current limitations

The current command-line demonstration uses small artificial 5 × 5 images
rather than the real MNIST dataset.

The current limitations include:

- real MNIST data has not yet been integrated;
- the demo currently includes only artificial representations of digits 1 and
  7;
- the demo does not yet allow the user to select the distance measure;
- classification accuracy has not yet been measured on MNIST;
- large-scale performance has not yet been measured;
- all calculated training distances are currently sorted even though only the
  `k` smallest distances are required.

The next major development step is MNIST integration and evaluation of the
different distance measures using real handwritten-digit images.

## Project structure

```text
digit-recognition/
├── data/
├── docs/
│   ├── implementation.md
│   ├── specification.md
│   ├── testing.md
│   ├── weekly_report_1.md
│   ├── weekly_report_2.md
│   ├── weekly_report_3.md
│   ├── weekly_report_4.md
│   └── weekly_report_5.md
├── src/
│   └── digitrecognition/
│       ├── image_representation.py
│       ├── knn.py
│       ├── nearest_point.py
│       ├── offsets.py
│       └── point_set_distance.py
├── tests/
│   ├── test_image_representation.py
│   ├── test_integration.py
│   ├── test_knn.py
│   ├── test_nearest_point.py
│   ├── test_offset.py
│   └── test_point_set_distance.py
├── demo.py
├── pyproject.toml
└── README.md
```

## Documentation

- [Specification document](docs/specification.md)
- [Implementation document](docs/implementation.md)
- [Testing document](docs/testing.md)
- [Weekly Report 1](docs/weekly_report_1.md)
- [Weekly Report 2](docs/weekly_report_2.md)
- [Weekly Report 3](docs/weekly_report_3.md)
- [Weekly Report 4](docs/weekly_report_4.md)
- [Weekly Report 5](docs/weekly_report_5.md)

## Peer review

The first peer review has been completed.

Peer-review feedback on this project suggested adding larger and more
representative tests. In response, additional 28 × 28 tests were added for
nearest-point searching and point-set distance calculations.

## Technologies

- Python 3.12
- Poetry
- pytest
- pytest-cov
- Pylint

## Next steps

The next planned development tasks are:

- integrate the MNIST dataset;
- convert real MNIST images into point-set representations;
- classify real handwritten digits;
- measure classification accuracy;
- compare D22, D23, and the unnormalized D23 variation;
- measure execution time on larger datasets;
- improve the command-line interface;
- prepare the project for the final demonstration.