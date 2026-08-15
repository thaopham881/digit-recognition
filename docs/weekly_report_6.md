# Weekly Report 6

## Time spent

Approximately 16,75 hours.

## What did I do this week?

This week, I integrated the real MNIST handwritten-digit dataset into the project and completed the first end-to-end evaluation using genuine handwritten digit images.

I implemented an MNIST loader for the compressed IDX image and label files. The loader validates the file headers and dimensions and supports loading only a selected number of images and labels so that smaller experiments can be run during development.

I also added preprocessing functionality that converts the loaded grayscale MNIST images into the point-set and Boolean-grid representations already used by the classifier.

To evaluate the classifier, I implemented functionality for:

* preparing labelled training images;
* classifying test images;
* comparing predictions with the correct labels;
* calculating the number of correct predictions;
* calculating classification accuracy;
* measuring execution time.

I also improved the k-nearest-neighbours implementation. Previously, the classifier calculated every training-image distance, stored all results, and sorted the complete list even though only the `k` smallest distances were needed.

I replaced this with a fixed-size binary max-heap. The heap stores only the current `k` nearest candidates. When a better candidate is found, it replaces the worst candidate currently stored in the heap.

Finally, I added automated tests for the new MNIST, evaluation, and heap functionality and updated the project documentation.

## How has the program progressed?

The program can now classify real handwritten digits from MNIST instead of working only with artificial images.

The complete MNIST classification pipeline now performs the following steps:

1. load MNIST image and label files;
2. convert grayscale images into point-set and Boolean-grid representations;
3. generate coordinate offsets for nearest-point searching;
4. calculate point-set distances between a test image and training images;
5. retain the `k` nearest training images using a fixed-size max-heap;
6. perform majority voting;
7. predict the handwritten digit;
8. compare the prediction with the true label;
9. calculate classification accuracy.

I ran a small MNIST experiment using:

* 500 training images;
* 20 test images;
* threshold 128;
* `k = 3`;
* offset size 11;
* D22 distance.

The experiment produced:

```text
Correct predictions: 19/20
Accuracy: 95.00%
Elapsed time: 54.02 seconds
```

The 95% accuracy should not be interpreted as a reliable estimate of performance on the complete MNIST dataset because only 20 test images were used. However, the experiment demonstrates that the implemented algorithms can classify real handwritten digits.

The test suite now contains **72 automated tests**, and all tests pass.

The current source-code test coverage is **99%**.

The only uncovered statement is the direct script entry-point call in `mnist_experiment.py`. The implemented algorithmic functionality is covered by tests.

The current Pylint score is **9.56/10**.

## What did I learn this week?

I learned how the MNIST dataset is stored in IDX format and how image and label files can be parsed manually.

I also learned more about separating preprocessing from classification. Preparing the training images in advance avoids repeatedly converting the same grayscale training images every time a new test image is classified.

Implementing the binary max-heap helped me understand how a heap can be used to maintain only the best `k` candidates from a much larger sequence of values.

Previously, sorting all `T` training distances required approximately:

```text
O(T log T)
```

for neighbour ordering and required storing all `T` calculated distances.

With the fixed-size heap, neighbour maintenance instead requires approximately:

```text
O(T log k)
```

and only:

```text
O(k)
```

space for the retained neighbour candidates.

I also learned that this optimization does not solve the largest performance problem in the program. The classifier still needs to calculate the point-set distance between the test image and every selected training image. These distance calculations are much more expensive than maintaining the heap.

The real MNIST experiment made this performance limitation much clearer.

## What remains unclear or has been challenging?

The biggest challenge is still execution time.

The current experiment with only 500 training images and 20 test images took approximately 54 seconds. Using the complete MNIST training set of 60,000 images and a large number of test images would therefore be much more computationally expensive with the current point-set distance algorithm.

Another question is how the three implemented distance measures compare on real handwritten digits.

D22, D23, and unnormalized D23 are implemented and tested, but I have not yet performed a systematic comparison using the same MNIST training and test subsets.

The current experiment is also too small to draw strong conclusions about classification accuracy.

## What will I do next?

The main implementation goals of the project are now complete.

Next, I plan to:

* finalize the implementation, testing, and user documentation;
* make sure the README reflects the final state of the project;
* document the MNIST experiment and performance limitations;
* review the repository for outdated information;
* complete the second peer review;
* address any final peer-review feedback;
* run the complete tests, coverage analysis, and Pylint before submission;
* prepare the repository for final submission.

If time permits, I may also run small controlled experiments comparing D22, D23, and unnormalized D23, but this is secondary to completing the required documentation and final review.
