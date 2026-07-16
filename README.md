# Handwritten Digit Recognition

This project is being developed for the University of Helsinki Algorithms Laboratory course.

The program will recognize handwritten digits from the MNIST dataset using the k-nearest neighbors algorithm and point-set distance measures.

Each grayscale image will be converted into a black-and-white image using a selected threshold. The black pixels will be represented as coordinate lists and Boolean arrays. The program will compare test images with training images using the D22 and D23 point-set distance measures.

The main algorithms and distance calculations will be implemented manually without using a ready-made k-nearest neighbors classifier or pre-built matrix operations.

## Current status

The project is currently in the planning and setup stage.

The repository structure, specification document, and first weekly report have been created. Implementation of the core algorithms will begin during Week 2.

## Documentation

- [Specification document](docs/specification.md)
- [Weekly Report 1](docs/weekly_report_1.md)

## Project structure

```text
digit-recognition/
├── data/
├── docs/
├── src/
│   └── digitrecognition/
├── tests/
├── .gitignore
└── README.md
