# User Guide

## Overview

This program recognizes handwritten digits using k-nearest neighbours
and point-set distance measures.

Images from the MNIST dataset are converted from grayscale images into
point-set representations. The classifier compares a test image with
labelled training images and predicts the digit based on its nearest
neighbours.

The program supports the following distance measures:

- D22
- D23
- unnormalized D23

The project also includes a small MNIST experiment for testing the
classifier with real handwritten digit images.


## Requirements

The project requires:

- Python 3.12
- Poetry

Install the project dependencies from the project root with:

```bash
poetry install