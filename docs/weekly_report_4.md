# Weekly Report 4

## Time spent

Approximately 11,5 hours.

## What did I do this week?

This week, I prepared the project for the first peer review.

I updated the main README so that another student can understand the purpose
of the project, install its dependencies, run the demonstration, execute the
tests, and find the project documentation.

I began writing the implementation document. The document currently explains the structure of the program, the responsibilities of the different modules, the operation of the nearest-point search, the current time and space complexities, known limitations, possible future improvements, and my use of ChatGPT during the project.

I also added integration tests for the complete classification pipeline. The integration tests begin with grayscale image data and execute image conversion, offset generation, point-set comparison, k-nearest-neighbour selection, majority voting, and final label prediction.

The integration tests classify artificial test images of digits 1 and 7
against a small labelled training set.

I updated the testing document to describe the integration tests, their input data, their expected results, and the commands required to reproduce them.

## How has the program progressed?

The project is now easier for another student to run and review.

The current program contains a complete small-scale classification pipeline:

1. grayscale images are converted into coordinate lists and Boolean grids;
2. local search offsets are generated and sorted by distance;
3. nearest foreground points are found;
4. complete point-set distances are calculated;
5. the k nearest labelled reference images are selected;
6. majority voting produces the predicted label;
7. the result and neighbour distances can be observed through the
   command-line demonstration.

At the end of the week, all 38 automated tests pass successfully. The
source-code test coverage is 100%.

The project also has two integration tests in addition to the existing unit tests.

The implementation document has been started, and the README now links the available project documentation.

## What did I learn this week?

I learned the difference between a unit test and an integration test.

A unit test normally checks one small function in isolation. The integration tests added this week verify that several modules work correctly together, from the initial grayscale input to the final predicted label.

I also learned more about documenting a program’s architecture and analysing time and space complexity using Big-O notation.

Writing the implementation document helped me understand how the coordinate list, Boolean grid, offset list, nearest-point search, point-set distance, and k-nearest-neighbours classifier are connected.

I also learned how to prepare a repository so that another developer can install, run, test, and review it.

## What remains unclear or has been challenging?

The most difficult remaining issue is the exact implementation of the
required D22 and D23 point-set distance measures.

The current symmetric average distance is a working intermediate measure, but it is not yet the complete final implementation described in the project scope.

Another challenge is moving from the current artificial 5 × 5 images to
genuine MNIST images. The final program must process considerably larger amounts of image data, so execution time may become an important issue.

The current integration tests use only artificial representations of digits 1 and 7. Realistic MNIST testing and classification-accuracy measurement have not yet begun.

## What will I do next?

Next week, I plan to:

- complete the first peer-review assignment received through Labtool;
- study and implement the exact required point-set distance measures;
- begin loading and converting genuine MNIST images;
- classify a small MNIST subset before attempting larger datasets;
- add tests for the final distance measures;
- measure classification accuracy and execution time;
- update the implementation and testing documents;
- review and respond to feedback received on my own project.