# Weekly Report 2

## Time spent

Approximately 14.5 hours.

## What did I do this week?

This week, I began implementing the core functionality of the handwritten digit recognition project.

I implemented a function that converts a grayscale image into two representations: a coordinate list of active pixels and a Boolean array showing the locations of those pixels. The grayscale threshold is provided as a parameter.

I also implemented the generation of coordinate offsets within a square search area. The offsets are stored together with their Euclidean distances and sorted in ascending order of distance.

In addition, I implemented the first version of the nearest-point search. The algorithm first searches the Boolean array using the sorted offsets. If no point is found within the local search area, it uses an exhaustive fallback search through the reference image's coordinate list.

I documented the new functions using docstrings and added unit tests alongside the implementation. I also installed and used pytest-cov to track test coverage.

## How has the program progressed?

The project has progressed from the planning and setup stage into the implementation stage.

The program does not yet classify complete MNIST images, but several components of the core point-set comparison algorithm are now implemented. It can create the required image representations, generate sorted search offsets, and find the nearest point using both an optimized local search and an exhaustive fallback.

At the end of the week, all 21 automated tests pass successfully. The current test coverage is 100%.

## What did I learn this week?

I learned how a grayscale image can be represented as both a coordinate list and a Boolean array. The coordinate list makes it possible to iterate through active pixels, while the Boolean array makes it possible to check whether a particular coordinate contains an active pixel efficiently.

I also learned how precomputed coordinate offsets can be sorted by Euclidean distance and used to search nearby image positions in nearest-first order.

I gained more experience with Python type hints, docstrings, pytest unit tests, exception testing, approximate floating-point comparisons, Poetry, and test-coverage measurement.

## What was challenging?

The most challenging part was understanding how the nearest-point search works and how the Boolean array and coordinate list are used together.

Setting up Poetry and ensuring that the project could be imported correctly during testing also required some troubleshooting.

The complete calculation of distance between two point sets still needs to be implemented.

## What will I do next?

Next week, I plan to:

- implement the complete distance calculation between two point sets;
- compare the distance from image A to image B and from image B to image A;
- add unit tests for image-to-image distance calculations;
- begin loading and processing a small subset of MNIST images;
- continue documenting the code and tracking test coverage.