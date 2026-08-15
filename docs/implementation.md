# Implementation Document

## General structure

The program is divided into modules according to their responsibilities.

### `image_representation.py`

This module converts a grayscale image into two representations:

* a coordinate list containing the active foreground pixels;
* a Boolean grid for quickly checking whether a coordinate contains an active pixel.

Pixels whose grayscale value is at least the selected threshold are considered active.

The coordinate list allows the distance algorithms to iterate only through active pixels. The Boolean grid allows constant-time coordinate lookup during local nearest-point searching.

### `offsets.py`

This module generates coordinate offsets for the local nearest-point search.

Each offset contains:

* a row displacement;
* a column displacement;
* its Euclidean distance from the centre point.

The offsets are sorted in ascending order of Euclidean distance. They can therefore be generated once and reused during many image comparisons.

### `nearest_point.py`

This module searches for the nearest active point in a reference image.

For a source coordinate, the algorithm first checks positions using the precomputed offsets and the Boolean grid. Since the offsets are ordered by distance, the first active point found is the nearest point among the positions included in the local search area.

If no active reference point is found inside the local search area, the program performs an exhaustive fallback search through the complete reference coordinate list.

The exhaustive search is also implemented separately and is used in tests as a reference method.

### `point_set_distance.py`

This module calculates distances between complete point sets.

For every active point in one image, the nearest active point in the other image is determined. These nearest-point distances can either be averaged or summed.

The calculation is performed in both directions because a one-directional comparison could ignore points that exist only in one of the images.

The module implements three point-set distance measures:

* D22;
* D23;
* unnormalized D23.

#### D22

D22 calculates the directed average nearest-point distance from image A to image B and from image B to image A.

The larger of the two directed averages is returned.

#### D23

D23 also calculates the directed average nearest-point distance in both directions.

Instead of returning the larger value, D23 returns the average of the two directed values.

#### Unnormalized D23

The unnormalized D23 variation uses directed sums instead of directed averages.

The nearest-point distances are therefore not divided by the number of source points before the two directions are combined.

The earlier `symmetric_average_distance` function is retained as a compatibility wrapper for D22.

### `max_heap.py`

This module implements a fixed-size binary max-heap used by the k-nearest-neighbours algorithm.

The heap stores at most `k` distance-label pairs.

The root of the heap contains the worst, meaning the most distant, neighbour currently retained.

While the training images are processed:

1. new candidates are inserted normally while the heap contains fewer than `k` items;
2. once the heap is full, a new candidate is compared with the root;
3. if the new candidate is better than the current worst neighbour, it replaces the root;
4. the heap property is restored using a sift-down operation.

This means that the classifier does not need to store and sort the distances of every training image.

When classification is complete, the retained `k` neighbours are returned in nearest-to-farthest order.

Distance is the primary comparison value. The label is used as a deterministic tie-breaker when two candidates have equal distances.

### `knn.py`

This module implements k-nearest-neighbours classification.

The classifier can use any of the following point-set distance measures:

```text
d22
d23
d23_unnormalized
```

D22 is used by default.

For one test image, the classifier:

1. compares the test image with each training image;
2. calculates the selected point-set distance;
3. adds the distance-label pair to the fixed-size max-heap;
4. retains only the current `k` nearest candidates;
5. performs majority voting using those neighbours.

The classifier validates that:

* the training set is not empty;
* `k` is greater than zero;
* `k` does not exceed the number of training images;
* the requested distance measure exists.

Unknown distance-measure names cause a `ValueError`.

### Majority voting

After the `k` nearest neighbours have been selected, their labels are counted.

The label receiving the largest number of votes is selected.

If multiple labels receive the same number of votes, the total neighbour distance for each tied label is compared. The label with the smaller total distance is preferred.

If a tie still remains, the numerically smaller label is selected.

These rules make classification deterministic.

### `mnist_loader.py`

This module loads real MNIST data from compressed IDX files.

The MNIST image loader:

* reads the IDX header;
* validates the image-file magic number;
* checks that the images are 28 × 28 pixels;
* reads grayscale pixel values;
* converts each image into a two-dimensional Python list.

The label loader similarly reads and validates the corresponding label file.

Both loaders support an optional `limit` argument. This makes it possible to use a small subset of MNIST instead of loading the entire dataset during development and evaluation.

Invalid file formats, invalid limits, and unexpectedly incomplete files are rejected with exceptions.

### `evaluation.py`

This module contains functionality used for evaluating the classifier on MNIST.

`prepare_training_images` converts grayscale training images into the point-set and Boolean-grid representations used by the classifier.

Preprocessing the training images before evaluation avoids converting the same training image repeatedly for every test image.

`evaluate_classifier`:

1. converts each test image into the point-set representation;
2. classifies the image using k-nearest neighbours;
3. compares the predicted label with the correct MNIST label;
4. counts correct predictions;
5. calculates classification accuracy;
6. measures total classification time.

The function returns the number of correct predictions, number of test images, accuracy percentage, and elapsed time.

### `mnist_experiment.py`

This module provides a small experiment using real MNIST handwritten digits.

The current default settings are:

* 500 training images;
* 20 test images;
* threshold 128;
* `k = 3`;
* offset size 11;
* D22 distance measure.

The experiment:

1. loads MNIST training and test data;
2. preprocesses the training images;
3. generates the nearest-point search offsets;
4. classifies the selected test images;
5. prints accuracy and execution time.

One run of the current configuration produced:

```text
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

This experiment is intended to demonstrate that the implemented algorithms work with genuine handwritten digits. It is not intended to achieve state-of-the-art MNIST accuracy or performance.

### `demo.py`

The original command-line demonstration uses small artificial 5 × 5 images representing digits 1 and 7.

The user selects a test image and a value of `k`. The demonstration then displays the image, predicted label, and nearest reference images.

This demonstration remains useful for manually inspecting the behaviour of the classification pipeline with very small inputs.

## Algorithm operation

The complete real-image classification process can be described as follows.

### 1. Image conversion

A 28 × 28 MNIST grayscale image is converted into:

* a list of active coordinates;
* a Boolean grid.

The selected threshold determines which pixels belong to the handwritten digit.

### 2. Offset generation

A list of coordinate offsets is generated and sorted according to Euclidean distance.

The same offset list can be reused during many nearest-point searches.

### 3. Nearest-point searching

For every active source point, the algorithm searches the reference image for an active point.

The local search checks the precomputed offsets first.

If no point is found in the configured local search area, an exhaustive search through the reference coordinate list is performed.

### 4. Point-set distance

Nearest-point searches are repeated for all points in a source image.

Depending on the selected distance measure, the resulting nearest-point distances are averaged or summed.

The process is performed in both directions between the two images.

The two directed results are then combined according to D22, D23, or the unnormalized D23 definition.

### 5. k-nearest-neighbour selection

The test image is compared with every selected training image.

Instead of storing every calculated distance, a binary max-heap with capacity `k` retains only the current best candidates.

After all training images have been processed, the heap contains the `k` nearest training images.

### 6. Prediction

The labels of the nearest neighbours are passed to the majority-voting function.

The winning label becomes the predicted handwritten digit.

## Time and space complexities

The following notation is used:

* `H × W`: image dimensions;
* `P`: number of active points in the source image;
* `Q`: number of active points in the reference image;
* `S`: number of local-search offsets;
* `T`: number of training images;
* `k`: number of nearest neighbours.

### Image conversion

Every pixel is examined once.

* Time: `O(HW)`
* Space: `O(HW + P)`

For MNIST, `H = W = 28`.

### Offset generation

The program creates `S` offsets and sorts them.

* Time: `O(S log S)`
* Space: `O(S)`

The offsets are generated once and reused.

### Nearest-point search

The local search checks at most `S` offsets.

If no point is found locally, the fallback search examines all `Q` reference points.

* Local-search time: `O(S)`
* Worst-case time: `O(S + Q)`
* Additional space: `O(1)`

### Directed point-set distance

The nearest-point search is repeated for all `P` source points.

* Worst-case time: `O(P(S + Q))`
* Additional space: `O(1)`

Directed average and directed sum calculations have the same asymptotic complexity because they perform the same nearest-point searches.

### Symmetric point-set comparison

D22, D23, and unnormalized D23 calculate distances in both directions.

The worst-case time is therefore:

```text
O(P(S + Q) + Q(S + P))
```

which can also be written as:

```text
O((P + Q)S + PQ)
```

### Binary max-heap

The heap contains at most `k` items.

Insertion or replacement can require moving an item through the height of the heap.

* Heap update: `O(log k)` worst case
* Heap space: `O(k)`
* Final ordering of retained neighbours: `O(k log k)`

### k-nearest-neighbours classification

A test image must still be compared with all `T` selected training images because the classifier needs their distances.

The point-set distance calculations therefore remain the dominant cost.

Ignoring the distance calculation itself, maintaining the nearest neighbours requires approximately:

```text
O(T log k)
```

rather than sorting all `T` calculated distances using:

```text
O(T log T)
```

The heap requires:

```text
O(k)
```

storage for neighbour candidates rather than an `O(T)` list of all calculated distances.

The complete classification cost can be expressed as:

```text
O(T × point-set-distance cost + T log k)
```

plus `O(k log k)` for ordering the final retained neighbours.

## Correctness considerations

The program contains both optimized/local and exhaustive nearest-point search functionality.

The sorted offset list ensures that the first active point encountered is the nearest point among the coordinates included in the local search window.

If the local search finds no active point, exhaustive fallback searches all reference coordinates and therefore finds the nearest available reference point.

The limited local search area is an optimization choice. When a point is found locally, positions outside that configured area are not examined. The size of the offset area therefore represents a trade-off between execution time and the extent of the search.

Point-set calculations are performed in both directions so that differences in either image affect the result.

D22, D23, and unnormalized D23 are tested with manually constructed inputs for which expected values can be calculated independently.

The k-nearest-neighbour implementation is tested separately from the distance algorithms.

The binary max-heap is also tested directly to verify:

* insertion;
* fixed capacity;
* replacement of the current worst candidate;
* ordering;
* equal-distance behaviour;
* invalid capacity handling.

MNIST loading and evaluation functionality have separate automated tests.

## Testing and peer-review improvements

During Week 5, peer-review feedback suggested using larger and more representative test inputs.

In response, 28 × 28 artificial inputs were added to tests for nearest-point searching and point-set distance calculations.

These inputs more closely resemble the dimensions of MNIST images while still allowing the expected behaviour to be controlled.

During Week 6, additional tests were added for:

* the binary max-heap;
* MNIST image loading;
* MNIST label loading;
* invalid MNIST data;
* preprocessing training images;
* classification evaluation;
* the MNIST experiment;
* the updated heap-based k-nearest-neighbour implementation.

At the current stage, the complete automated test suite contains 72 passing tests.

The test suite achieves 99% source-code coverage.

The only currently uncovered source statement is the direct script entry-point call in `mnist_experiment.py`. The implemented algorithmic modules are covered by the tests.

Pylint currently gives the project a score of 9.56 out of 10.

## MNIST evaluation

Real MNIST data has now been integrated into the project.

A small experiment was selected because the point-set comparison algorithm is computationally expensive.

Using:

* 500 training images;
* 20 test images;
* threshold 128;
* `k = 3`;
* an 11 × 11 offset area;
* D22;

the classifier correctly predicted 19 of the 20 test images.

This corresponds to an accuracy of 95%.

The experiment took approximately 54 seconds on the development computer.

Because only 20 test examples were used, the 95% result should be treated as a small demonstration rather than a reliable estimate of general MNIST accuracy.

A larger evaluation would provide a more reliable accuracy estimate but would require considerably more execution time with the current distance algorithm.

## Current shortcomings

The main current limitations are:

* point-set distance calculations are computationally expensive;
* classification still requires a point-set comparison against every selected training image;
* only a small subset of MNIST has been evaluated;
* the current 95% accuracy result is based on only 20 test images;
* D22, D23, and unnormalized D23 have not yet been systematically compared on larger MNIST subsets;
* the local nearest-point search uses a limited search area before falling back to exhaustive search only when no local point is found;
* the artificial command-line demo includes only digits 1 and 7;
* the artificial demo does not allow the distance measure to be selected interactively.

The max-heap improves neighbour selection, but it does not remove the main computational cost: calculating the point-set distance between the test image and every training image.

## Possible improvements

Possible future improvements include:

* evaluating larger MNIST subsets;
* comparing D22, D23, and unnormalized D23 using the same training and test sets;
* comparing different values of `k`;
* comparing different grayscale thresholds;
* comparing different local search-area sizes;
* measuring how the heap implementation affects performance as the number of training images increases;
* improving or replacing the local nearest-point search while preserving correctness and efficiency;
* adding command-line parameters for experiment settings;
* allowing the artificial demonstration to select the distance measure;
* performing more systematic performance measurements.

## Use of large language models

I used ChatGPT as an interactive tutor and programming assistant during the project.

ChatGPT was used to:

* explain Python syntax and unfamiliar programming concepts;
* explain image representation, offset generation, nearest-point searching, point-set comparison, and k-nearest-neighbours classification;
* explain the differences between D22, D23, and the unnormalized D23 variation;
* explain binary heaps and how a fixed-size max-heap can retain the `k` smallest distances;
* help divide weekly course requirements into smaller tasks;
* suggest initial drafts for some functions, tests, and documentation;
* help interpret errors involving Poetry, imports, pytest, Git, coverage, and Pylint;
* help with MNIST loading and evaluation structure;
* review the wording and structure of documentation.

I manually added and reviewed the code in the repository, ran the program and tests, examined the results, and used the explanations to understand the implementation.

I remain responsible for the project's code, testing, documentation, and algorithmic decisions.

## Sources

* M.-P. Dubuisson and A. K. Jain, *A Modified Hausdorff Distance for Object Matching*, Proceedings of the 12th International Conference on Pattern Recognition, 1994.
* University of Helsinki Algorithms and AI Project course material.
* MNIST handwritten-digit dataset.
