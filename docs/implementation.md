# Implementation Document

## General structure

The program is divided into modules based on their responsibilities.

### `image_representation.py`

This module converts a grayscale image into two representations:

- a coordinate list containing the foreground pixels;
- a Boolean grid for quickly checking whether a coordinate contains a
  foreground pixel.

The coordinate list allows the algorithm to iterate only through active
pixels. The Boolean grid allows constant-time coordinate lookup during the
local nearest-point search.

### `offsets.py`

This module generates coordinate offsets inside a square local search area.

Each offset stores:

- a row displacement;
- a column displacement;
- its Euclidean distance from the centre.

The offsets are sorted in ascending order of distance and reused in multiple image comparisons.

### `nearest_point.py`

This module finds the nearest foreground point in a reference image.

The algorithm first checks nearby coordinates using the sorted offsets and the Boolean grid. If no foreground point is found inside the local area, it performs an exhaustive fallback search through the reference coordinate list.

### `point_set_distance.py`

This module calculates distances between complete point sets.

For every source point, it finds the nearest point in the reference image.
The nearest-point distances can either be averaged or summed depending on the selected distance measure. The calculation is performed in both directions.

The module currently implements the three required point-set distance
measures:

- D22 takes the larger of the two directed average nearest-point distances;
- D23 takes the average of the two directed average nearest-point distances;
- the unnormalized D23 variation uses directed sums instead of dividing each directed distance by the number of source points.

The earlier `symmetric_average_distance` function is retained as a
compatibility wrapper for D22.

### `knn.py`

This module implements k-nearest-neighbours classification.

The classifier can use D22, D23, or the unnormalized D23 variation as its distance measure. D22 is used by default.

The classifier:

1. compares a test image with every selected training image;
2. stores each distance and training label;
3. sorts the results by distance;
4. selects the first `k` neighbours;
5. predicts the label using majority voting.

Vote ties are resolved using total neighbour distance. The numerical label is used as a final deterministic tie-breaker.

The distance measure is selected using a string parameter. The currently supported values are:

- `d22`;
- `d23`;
- `d23_unnormalized`.

Unknown distance-measure names are rejected with a `ValueError`.

### `demo.py`

The current command-line demonstration uses artificial 5 × 5 images
representing digits 1 and 7.

The user selects a test image and a value of `k`. The program displays the image, predicted label, and nearest reference labels with their distances.

The demonstration currently uses the default D22 distance measure.

## Algorithm operation

For each foreground point in image A, the algorithm tries to find the nearest
foreground point in image B.

It first checks nearby positions according to the precomputed offsets. Since the offsets are sorted by distance, the first foreground point found is the nearest point inside the local search area.

If the local search does not find a point, the program compares the source point with every coordinate in the reference image. This fallback guarantees that a nearest point can still be found when no reference point is located inside the local search area.

The calculation is also performed from image B to image A because a
one-directional comparison may ignore additional points found in only one of the images.

### Directed average distance

For every point in the source point set, the nearest reference point is
located and its Euclidean distance is added to a total.

The total is then divided by the number of source points.

This directed average is used by D22 and D23.

### Directed sum distance

The unnormalized D23 variation uses the same nearest-point calculations but does not divide the total distance by the number of source points.

The result is therefore a directed sum rather than a directed average.

### D22

D22 calculates the directed average distance from A to B and from B to A.

The larger of these two directed values is returned.

### D23

D23 also calculates the directed average distance in both directions.

Instead of selecting the larger value, it returns the average of the two directed values.

### Unnormalized D23

The experimental D23 variation calculates directed sums instead of directed averages.

The two directed sums are then averaged.

## Time and space complexities

The following notation is used:

- `H × W`: image dimensions;
- `P`: number of active source points;
- `Q`: number of active reference points;
- `S`: number of offsets;
- `T`: number of training images.

### Image conversion

Every pixel is examined once.

- Time: `O(HW)`
- Space: `O(HW + P)`

### Offset generation

The program creates `S` offsets and sorts them.

- Time: `O(S log S)`
- Space: `O(S)`

The offset list is generated once and reused.

### Nearest-point search

The local search checks at most `S` offsets. If it fails, the fallback checks
all `Q` reference points.

- Local-search time: `O(S)`
- Worst-case time: `O(S + Q)`
- Additional space: `O(1)`

### Directed point-set distance

The nearest-point search is repeated for all `P` source points.

- Worst-case time: `O(P(S + Q))`
- Additional space: `O(1)`

The directed average and directed sum have the same asymptotic complexity because they perform the same nearest-point searches.

### Symmetric point-set comparison

D22, D23, and the unnormalized D23 variation all perform calculations in both
directions.

- Worst-case time: `O(P(S + Q) + Q(S + P))`

This can also be written as:

```text
O((P + Q)S + PQ)

### k-nearest-neighbours classification

One test image is compared with `T` training images. The current
implementation stores and sorts all calculated distances.

- Distance calculation: `O(T × point-set-distance cost)`
- Sorting: `O(T log T)`
- Stored distance list: `O(T)`

A future improvement could maintain only the `k` smallest distances using a
bounded heap.

## Correctness considerations

The sorted offset list ensures that the first foreground point found locally
has the smallest distance among the inspected positions.

If no foreground point is found inside the local search area, the exhaustive
fallback searches through all reference points.

The point-set comparison is performed in both directions to account for
additional points in either image.

D22, D23, and the unnormalized D23 variation are tested separately with
manually constructed point sets for which the expected results can be
calculated directly.

The k-nearest-neighbours tests also verify that D23 and the unnormalized D23
variation can be selected as the classifier's distance measure.

The classifier has explicit tie-breaking rules, which makes its result
deterministic.

## Current shortcomings

The current project has the following limitations:

- the demo uses artificial 5 × 5 images instead of MNIST;
- only digits 1 and 7 are included in the demo;
- real MNIST data has not yet been integrated;
- classification accuracy has not yet been measured on MNIST;
- large-scale performance has not yet been measured;
- the demo does not yet allow the user to select the distance measure;
- all training distances are sorted even though only the `k` smallest values
  are required.

## Possible improvements

Possible future improvements include:

- loading and preprocessing the MNIST dataset;
- comparing D22, D23, and the unnormalized D23 variation using
  classification accuracy and execution time;
- preprocessing training images only once;
- replacing complete sorting with a bounded heap;
- comparing different local search-area sizes;
- measuring classification accuracy and execution time on MNIST subsets;
- allowing the user to select the threshold, distance measure, image index,
  and dataset size.

## Testing and peer-review improvements

During Week 5, the first peer review suggested adding larger and more
representative test inputs.

In response, two new 28 × 28 tests were added.

One test compares the optimized nearest-point search with the exhaustive search on a larger grid containing several reference and query points.

Another test compares two larger point sets representing a simple shifted pattern and verifies the expected distance.

Additional tests were added for:

- D22;
- D23;
- the unnormalized D23 variation;
- selecting D23 in k-nearest-neighbours classification;
- selecting the unnormalized D23 variation;
- rejecting an unknown distance-measure name;
- error handling for empty point sets in the directed sum calculation.

At the current stage, the complete automated test suite contains 48 passing
tests.

The current test suite achieves 100% source-code coverage across all
implemented modules.

## Use of large language models

I used ChatGPT as an interactive tutor and programming assistant during the
project.

ChatGPT was used to:

- explain Python syntax and unfamiliar programming concepts;
- explain image representation, offset generation, nearest-point searching,
  point-set comparison, and k-nearest-neighbours classification;
- explain the differences between D22, D23, and the unnormalized D23
  variation;
- divide the weekly course requirements into smaller tasks;
- suggest initial drafts for some functions, tests, documentation, and the
  command-line demonstration;
- help interpret errors involving Poetry, imports, pytest, Git, coverage, and
  Pylint;
- review the wording and structure of documentation.

I manually added the code to the repository, ran it, examined the results, and tested the implementation. I used the explanations to understand the code instead of assuming that generated suggestions were automatically correct.

I remain responsible for the project's code, testing, documentation, and algorithmic decisions. The distance-measure definitions will also be checked against the original research article and the course material.

## Sources

- M.-P. Dubuisson and A. K. Jain, *A Modified Hausdorff Distance for Object
  Matching*, Proceedings of the 12th International Conference on Pattern
  Recognition, 1994.
- University of Helsinki Algorithms and AI Project course topic description.
- MNIST handwritten-digit dataset documentation, when MNIST integration is
  implemented.