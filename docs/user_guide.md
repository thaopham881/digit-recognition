# User Guide

## Overview

This program recognizes handwritten digits using k-nearest neighbours and point-set distance measures.

Images from the MNIST dataset are converted from grayscale images into point-set representations. The classifier compares a test image with labelled training images and predicts the digit based on its nearest neighbours.

The program supports the following distance measures:

* D22
* D23
* unnormalized D23

The project also includes a small MNIST experiment for testing the classifier with real handwritten digit images.

## Requirements

The project requires:

* Python 3.12
* Poetry

## Installation

Clone the repository and move to the project directory.

Install the project dependencies from the project root with:

```bash
poetry install
```

## Running the MNIST experiment

Run the real MNIST experiment with:

```bash
poetry run python -m digitrecognition.mnist_experiment
```

The experiment loads a subset of the MNIST dataset, converts the images into point-set representations, and classifies the test images using k-nearest neighbours.

The default experiment settings are:

* 500 training images
* 20 test images
* threshold 128
* k = 3
* offset size 11
* D22 distance measure

After the experiment finishes, the program prints the number of correct predictions, classification accuracy, and elapsed running time.

One example run produced:

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

The experiment uses only a small subset of MNIST because the implemented point-set distance calculations are computationally expensive.

## Running the artificial demonstration

The project also contains a small command-line demonstration using artificial digit images.

Run it with:

```bash
poetry run python demo.py
```

The demonstration asks the user to select:

1. an artificial test image representing digit 1 or 7;
2. a value of `k` between 1 and 4.

The program then displays the selected image, predicted label, and nearest reference images with their distances.

## Running the tests

Run all automated tests with:

```bash
poetry run pytest
```

The current test suite contains 72 tests.

To run the tests and measure test coverage:

```bash
poetry run pytest --cov=digitrecognition --cov-report=term-missing
```

The current source-code coverage is 99%.

## Code quality

Run Pylint with:

```bash
poetry run pylint src tests
```

The current Pylint score is 9.56 out of 10.

## How the recognition works

The recognition process consists of the following main steps:

1. A grayscale image is converted into a coordinate list and Boolean grid using a selected threshold.
2. Coordinate offsets are generated for nearest-point searching.
3. The distance between a test image and each training image is calculated using a point-set distance measure.
4. A fixed-size binary max-heap retains only the current `k` nearest training images.
5. The labels of the nearest neighbours are used in majority voting.
6. The winning label becomes the predicted handwritten digit.

## Supported distance measures

The classifier currently supports:

```text
d22
d23
d23_unnormalized
```

D22 is used by default.

### D22

D22 calculates the directed average nearest-point distance in both directions between two point sets and returns the larger value.

### D23

D23 calculates the directed average nearest-point distance in both directions and returns the average of the two values.

### Unnormalized D23

The unnormalized D23 variation uses directed sums instead of directed averages.

## MNIST data

The project reads MNIST image and label data from compressed IDX files.

The MNIST loader validates:

* file magic numbers;
* image dimensions;
* the requested item limit;
* whether the file contains enough data.

The experiment supports loading only a selected number of images and labels, which makes smaller experiments possible.

## Limitations

The main limitation is execution time.

Point-set distance calculations require many nearest-point searches. Each test image must also be compared with every selected training image.

The binary max-heap improves neighbour selection because the classifier stores only the current `k` nearest candidates instead of sorting all training-image distances. However, it does not remove the main cost of calculating the point-set distances themselves.

For this reason, the included MNIST experiment uses only a relatively small subset of the complete dataset.

The current 95% accuracy result is based on only 20 test images and should therefore be treated as a demonstration rather than a reliable estimate of overall MNIST classification accuracy.
