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

The project currently contains a small working digit-classification pipeline.

Implemented functionality includes:

- converting grayscale images into coordinate lists and Boolean grids;
- generating coordinate offsets sorted by Euclidean distance;
- optimized nearest-point searching using a Boolean grid;
- exhaustive fallback searching using coordinate lists;
- directed and symmetric point-set distance calculations;
- selecting the k nearest reference images;
- majority voting with deterministic tie-breaking;
- a command-line demonstration using artificial images of digits 1 and 7;
- automated unit tests and test-coverage tracking.

At the end of Week 3:

- 36 automated tests pass;
- source-code test coverage is 100%;
- Pylint gives the project a score of 9.49 out of 10.

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
2. select a value of k between 1 and 4.

It then displays the selected image, predicted label, and nearest reference
images with their distances.

## Running the tests

Run all automated tests:

```bash
poetry run pytest
```

Run the tests with coverage:

```bash
poetry run pytest --cov=digitrecognition --cov-report=term-missing
```

Run the code-quality analysis:

```bash
poetry run pylint src/digitrecognition demo.py
```

## Current limitations

The current command-line demonstration uses small artificial 5 × 5 images
rather than the complete MNIST dataset.

The current symmetric average distance is a working intermediate distance
measure. The exact required D22 and D23 point-set distance measures still need
to be completed.

MNIST integration, classification-accuracy measurement, and large-scale
performance testing also remain under development.

## Project structure

```text
digit-recognition/
├── data/
├── docs/
│   ├── specification.md
│   ├── testing.md
│   ├── weekly_report_1.md
│   ├── weekly_report_2.md
│   └── weekly_report_3.md
├── src/
│   └── digitrecognition/
│       ├── image_representation.py
│       ├── knn.py
│       ├── nearest_point.py
│       ├── offsets.py
│       └── point_set_distance.py
├── tests/
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

## Technologies

- Python 3.12
- Poetry
- pytest
- pytest-cov
- Pylint