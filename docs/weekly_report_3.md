# Weekly Report 3

## Time spent

Approximately 15,5 hours.

## What did I do this week?

This week, I continued developing the core functionality of the handwritten
digit recognition project.

I implemented point-set distance calculations. The program now finds the
nearest reference point for every point in a source image and calculates the
average nearest-point distance. It also calculates the distance in both
directions and combines the results into a symmetric distance value.

I implemented the first version of the k-nearest neighbours classifier. The
program compares a test image with labelled reference images, sorts the
reference images by distance, selects the k nearest images, and predicts the
label using majority voting.

Tie-breaking is handled using the total distance of the neighbours. If the
vote counts and total distances are equal, the smaller label is selected to
produce a deterministic result.

I also created a small command-line demonstration using artificial images of
the digits 1 and 7. The user can select a test image and a value of k. The
program displays the image, predicted label, nearest reference labels, and
their distances.

I added automated unit tests for the point-set distance and k-nearest
neighbours functions. I also created the initial testing document and used
Pylint to analyse code quality.

## How has the program progressed?

The project now has a small runnable classification pipeline.

The current pipeline performs the following steps:

1. converts a grayscale image into a coordinate list and Boolean grid;
2. generates sorted coordinate offsets;
3. finds nearest points efficiently;
4. calculates a distance between two point sets;
5. selects the k nearest labelled reference images;
6. predicts a label using majority voting;
7. displays the prediction and neighbour distances.

At the end of the week, all 36 automated tests pass. Source-code test coverage
is 100%.

Pylint currently gives the project a score of 9.49 out of 10.

The current demonstration uses small artificial images. Integration with the
MNIST dataset and the final required D22 and D23 distance measures remain to
be implemented.

## What did I learn this week?

I learned how a distance between complete point sets can be built from
nearest-point distances.

I also learned why the distance must be calculated in both directions. A
one-directional comparison may fail to account for additional points in one
of the images.

I learned how the k-nearest neighbours algorithm works in practice. The
algorithm does not train a separate model. Instead, it compares a test image
with labelled reference images and uses the labels of the nearest examples
to make a prediction.

I gained more experience with:

- Python type aliases and functions;
- sorting tuples with custom keys;
- dictionaries for vote counting;
- deterministic tie-breaking;
- command-line input;
- automated testing;
- test coverage;
- Pylint code-quality analysis.

## What was challenging?

The most challenging part was understanding how the individual nearest-point
distances should be combined into a complete image distance.

The current symmetric average distance is a temporary working measure for the
demonstration. I still need to study and implement the exact D22 and D23
formulas required by the project topic.

The current artificial data is small and easy to process. Performance will
become more challenging when the program compares MNIST test images with
thousands of reference images.

## What will I do next?

Next week, I plan to:

- study and implement the exact D22 and D23 point-set distance measures;
- add tests that distinguish the different distance measures;
- begin loading MNIST training and test images;
- convert MNIST images into coordinate lists and Boolean grids;
- classify a small MNIST subset before attempting the complete dataset;
- measure classification speed and accuracy;
- continue updating the documentation and tests.