# Weekly Report 5

## Time spent

Approximately 12.5 hours.

## What did I do this week?

This week, I continued developing the point-set distance measures used by the handwritten digit classifier.

I implemented the D22 and D23 distance measures. D22 calculates the directed average nearest-point distance in both directions between two point sets and returns the larger value. D23 calculates the same two directed average distances but returns their average.

I also implemented an unnormalized variation of D23. This version uses the sums of the nearest-point distances instead of dividing them by the number of source points.

The k-nearest-neighbours classifier was updated so that the distance measure can be selected instead of always using one fixed distance calculation. The currently supported choices are D22, D23, and unnormalized D23.

I also worked on the feedback from the first peer review. The reviewer suggested that the project should include larger and more representative test inputs instead of relying mainly on very small artificial examples. In response, I added tests using 28 × 28 inputs, which are closer to the dimensions of real MNIST images.

I updated the README and testing-related documentation to describe the new distance measures, the additional tests, and the current state of the project.

## How has the program progressed?

The program now contains the main distance measures planned for the project.

The classification pipeline can:

1. convert grayscale images into coordinate lists and Boolean grids;
2. generate sorted coordinate offsets;
3. search for the nearest active point;
4. calculate directed nearest-point distances;
5. calculate D22, D23, or unnormalized D23 distances between point sets;
6. compare a test image with labelled reference images;
7. select the k nearest reference images;
8. perform majority voting to predict the digit label.

The classifier can now use different point-set distance measures without changing the overall k-nearest-neighbours algorithm.

At the end of the week, all 48 automated tests pass successfully and source-code test coverage is 100%.

The project also received a Pylint score of 9.34 out of 10.

The larger 28 × 28 tests provide more realistic input sizes and help verify that the nearest-point and point-set-distance implementations also work with image dimensions similar to MNIST.

## What did I learn this week?

I learned more about how different point-set distance measures can be constructed from directed nearest-point distances.

In particular, I learned that D22 and D23 use the same directed distance calculations but combine the two directions differently. D22 uses the larger directed average, while D23 averages the two directed averages.

Implementing the unnormalized D23 variation also helped me understand how normalization by the number of points affects a distance measure.

I also learned more about designing representative tests. Small manually constructed examples are useful because their expected results can be calculated easily, but larger inputs are important for checking whether the implementation behaves correctly with data closer to the real problem.

The peer-review feedback was useful because it showed that high test coverage alone does not necessarily mean that the test data is representative.

## What remains unclear or has been challenging?

The biggest remaining challenge is computational performance when moving from artificial images to real MNIST data.

The point-set distance calculation requires many nearest-point searches. When one test image is compared against hundreds or thousands of training images, the number of distance calculations becomes large.

The current k-nearest-neighbours implementation also calculates the distance to every reference image and sorts the resulting distances even though only the k smallest values are needed. This may become inefficient when using a larger MNIST training set.

Another remaining challenge is determining how the different distance measures perform with genuine handwritten digits. The algorithms are implemented and tested, but their classification accuracy has not yet been measured using real MNIST data.

## What will I do next?

Next week, I plan to:

* integrate the real MNIST dataset into the project;
* implement loading of MNIST image and label files;
* convert genuine MNIST images into the existing point-set representation;
* classify a small subset of real handwritten digits;
* measure classification accuracy and execution time;
* improve the selection of the k nearest neighbours so that all distances do not need to be fully sorted;
* add automated tests for the MNIST loading and evaluation functionality;
* update the implementation, testing, and user documentation;
* prepare the project for the final peer review and submission.
