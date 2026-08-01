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

The offsets are sorted in ascending order of distance and reused in multiple
image comparisons.

### `nearest_point.py`

This module finds the nearest foreground point in a reference image.

The algorithm first checks nearby coordinates using the sorted offsets and
the Boolean grid. If no foreground point is found inside the local area, it
performs an exhaustive fallback search through the reference coordinate list.

### `point_set_distance.py`

This module calculates distances between complete point sets.

For every source point, it finds the nearest point in the reference image and
calculates the average nearest-point distance. The calculation is performed
in both directions.

The current symmetric average distance is a working intermediate measure.
The final D22, D23, and D23-variation implementations will follow the exact
formulas in the original research article and course topic description.

### `knn.py`

This module implements k-nearest-neighbours classification.

The classifier:

1. compares a test image with every selected training image;
2. stores each distance and training label;
3. sorts the results by distance;
4. selects the first `k` neighbours;
5. predicts the label using majority voting.

Vote ties are resolved using total neighbour distance. The numerical label is
used as a final deterministic tie-breaker.

### `demo.py`

The current command-line demonstration uses artificial 5 × 5 images
representing digits 1 and 7.

The user selects a test image and a value of `k`. The program displays the
image, predicted label, and nearest reference labels with their distances.

## Algorithm operation

For each foreground point in image A, the algorithm tries to find the nearest
foreground point in image B.

It first checks nearby positions according to the precomputed offsets. Since
the offsets are sorted by distance, the first foreground point found is the
nearest point inside the local search area.

If the local search does not find a point, the program compares the source
point with every coordinate in the reference image. This fallback guarantees
correctness when the nearest point is outside the local area.

The calculation is also performed from image B to image A because a
one-directional comparison may ignore additional points found in only one of
the images.

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

### Symmetric point-set comparison

The calculation is performed in both directions.

- Worst-case time: `O(P(S + Q) + Q(S + P))`

This can also be written as:

```text
O((P + Q)S + PQ)
```

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

The exhaustive fallback guarantees that a nearest point is still found when
the local search area contains no foreground point.

The comparison is performed in both directions to account for additional
points in either image.

The classifier has explicit tie-breaking rules, which makes its result
deterministic.

## Current shortcomings

The current project has the following limitations:

- the demo uses artificial 5 × 5 images instead of MNIST;
- only digits 1 and 7 are included in the demo;
- the final D22, D23, and D23 variation are not yet complete;
- classification accuracy has not yet been measured on MNIST;
- large-scale performance has not yet been measured;
- all training distances are sorted even though only the `k` smallest values
  are required.

## Possible improvements

Possible future improvements include:

- loading and preprocessing the MNIST dataset;
- implementing and comparing all required distance measures;
- preprocessing training images only once;
- replacing complete sorting with a bounded heap;
- comparing different local search-area sizes;
- measuring classification accuracy and execution time on MNIST subsets;
- allowing the user to select the threshold, distance measure, image index,
  and dataset size.

## Use of large language models

I used ChatGPT, specifically GPT-5.6 Thinking, as an interactive tutor and
programming assistant during the project.

ChatGPT was used to:

- explain Python syntax and unfamiliar programming concepts;
- explain image representation, offset generation, nearest-point searching,
  point-set comparison, and k-nearest-neighbours classification;
- divide the weekly course requirements into smaller tasks;
- suggest initial drafts for some functions, tests, documentation, and the
  command-line demonstration;
- help interpret errors involving Poetry, imports, pytest, Git, coverage, and
  Pylint;
- review the wording and structure of documentation.

I manually added the code to the repository, ran it, examined the results,
and tested the implementation. I used the explanations to understand the
code instead of assuming that generated suggestions were automatically
correct.

I remain responsible for the project’s code, testing, documentation, and
algorithmic decisions. The final distance-measure definitions will be checked
against the original research article and the course material.

## Sources

- M.-P. Dubuisson and A. K. Jain, *A Modified Hausdorff Distance for Object
  Matching*, Proceedings of the 12th International Conference on Pattern
  Recognition, 1994.
- University of Helsinki Algorithms and AI Project course topic description.
- MNIST handwritten-digit dataset documentation, when MNIST integration is
  implemented.