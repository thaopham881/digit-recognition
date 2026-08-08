# Testing Document

## Testing approach

The project uses automated unit and integration tests implemented with pytest.

Tests are developed alongside the program code. Most tests use small,
manually constructed images and point sets so that the expected results can be calculated directly. Larger 28 × 28 artificial inputs are also used to provide more representative tests of image-sized data.

The tests currently cover:

- conversion of grayscale images into coordinate lists and Boolean grids;
- validation of grayscale thresholds and image dimensions;
- generation of coordinate offsets;
- ordering of offsets by Euclidean distance;
- optimized nearest-point searches;
- exhaustive nearest-point fallback searches;
- directed point-set distance calculations;
- D22 distance calculations;
- D23 distance calculations;
- the unnormalized D23 variation;
- selection of the k nearest reference images;
- selection of different point-set distance measures in k-nearest neighbours;
- majority voting and tie-breaking in k-nearest neighbours classification;
- invalid and empty input handling;
- integration of the main classification components.

## Image representation tests

The image representation tests verify that active pixels are correctly stored in both the coordinate list and the Boolean grid.

The tests also cover:

- pixels equal to the selected threshold;
- empty images;
- thresholds outside the range 0–255;
- images whose rows have unequal lengths.

These tests verify that grayscale input is converted into the point-set
representations required by the later distance calculations.

## Offset generation tests

The offset tests verify that a square search area contains the correct number of offsets.

They also verify that:

- the centre position has distance zero and is checked first;
- the offsets are sorted by increasing Euclidean distance;
- diagonal distances are calculated correctly;
- even, zero, and otherwise invalid search sizes are rejected.

The offset ordering is important because the nearest-point algorithm examines
local candidate positions in increasing order of Euclidean distance.

## Nearest-point search tests

The nearest-point tests verify that the algorithm finds points:

- at the same coordinate;
- at horizontally or vertically adjacent coordinates;
- at diagonal coordinates;
- outside the precomputed local search area.

The distant-point case verifies that the exhaustive coordinate-list fallback is used when the local Boolean-grid search does not find a point.

The tests also verify:

- coordinate boundary checking;
- empty reference-point handling;
- agreement between the optimized search and exhaustive search.

During Week 5, a larger 28 × 28 test case was added in response to
peer-review feedback.

The test contains several reference points distributed across the grid and several query points. For every query point, the result of
`nearest_point_distance` is compared with the result of
`full_search_distance`.

This provides a stronger correctness check because the optimized algorithm must produce the same result as the simple exhaustive reference implementation on a more representative image-sized input.

## Point-set distance tests

The point-set distance tests use manually constructed point sets whose
expected distances can be calculated directly.

The tests verify that:

- identical point sets have distance zero;
- shifted points produce the expected Euclidean distance;
- directed nearest-point distances are averaged correctly;
- empty point sets are rejected;
- D22 selects the larger of the two directed average distances;
- D23 averages the two directed average distances;
- the unnormalized D23 variation uses directed sums instead of directed
  averages.

For example, one test uses the following point sets:

```text
A = [(0, 0), (0, 1)]
B = [(0, 0)]
```

The directed average distance from A to B is `0.5`, while the directed
average distance from B to A is `0.0`.

Therefore:

```text
D22 = max(0.5, 0.0) = 0.5
D23 = (0.5 + 0.0) / 2 = 0.25
```

For the unnormalized D23 variation, the directed sums are used instead. The test therefore expects a value of `0.5`.

A larger point-set test was also added during Week 5. It uses two 28 × 28 point sets containing ten active pixels. The second point set is shifted one pixel horizontally from the first, so the expected D22 distance is `1.0`.

These larger tests were added after the first peer review suggested testing the algorithms with more representative inputs instead of relying only on very small hand-built examples.

The earlier `symmetric_average_distance` function is also tested through its role as a compatibility wrapper for D22.

## K-nearest neighbours tests

The k-nearest neighbours tests verify that:

- reference images are sorted from nearest to farthest;
- only the requested number of neighbours is returned;
- majority voting selects the most common label;
- total neighbour distance is used to resolve a vote tie;
- the smaller numerical label is used as a final deterministic tie-breaker;
- invalid values of `k` are rejected;
- an empty training-image list is rejected;
- an empty neighbour list is rejected;
- the complete classification function returns both the predicted label and the selected neighbours.

During Week 5, the classifier was extended so that the distance measure can be selected.

Additional tests verify that:

- D23 can be selected by `find_k_nearest`;
- the unnormalized D23 variation can be selected by `find_k_nearest`;
- an unknown distance-measure name raises a `ValueError`.

For the D23 selection test, a manually constructed example has an expected
distance of `0.25`.

For the unnormalized D23 selection test, the same point sets produce an
expected distance of `0.5`.

These tests verify that the k-nearest neighbours implementation does not only contain the distance functions separately, but can actually use the selected distance function during classification.

## Integration testing

In addition to unit tests, the project contains integration tests that verify the complete classification pipeline.

The integration tests begin with grayscale image data and execute the
following steps together:

1. convert the grayscale images into coordinate lists and Boolean grids;
2. generate the sorted local-search offsets;
3. calculate point-set distances;
4. find the k nearest labelled reference images;
5. perform majority voting;
6. return the predicted digit label.

The tests use two artificial test images representing digits 1 and 7. Each test image is classified against a small training set containing two examples of digit 1 and two examples of digit 7.

The test for digit 1 verifies that:

- the predicted label is 1;
- exactly three neighbours are returned when `k = 3`;
- the neighbours are ordered by increasing distance.

The test for digit 7 verifies the same behaviour and expects the predicted label to be 7.

The integration tests currently use the default D22 distance measure.

The integration tests can be run separately with:

```bash
poetry run pytest tests/test_integration.py -v
```

These tests differ from the individual unit tests because they exercise
multiple program modules together, from grayscale image conversion to the final classification result.

## Test count

After the Week 5 additions, the project contains 46 automated tests.

The complete test suite can be run with:

```bash
poetry run pytest
```

The current test suite result is:

```text
46 passed
```

The Week 5 additions include:

- a larger 28 × 28 nearest-point test comparing optimized and exhaustive
  search;
- a larger 28 × 28 point-set distance test;
- a D22-specific test;
- a D23-specific test;
- an unnormalized D23 test;
- a test selecting D23 in k-nearest neighbours;
- a test selecting the unnormalized D23 variation;
- a test rejecting an unknown distance-measure name.

## Test coverage

Test coverage is measured using pytest-cov.

The coverage report can be generated with:

```bash
poetry run pytest --cov=digitrecognition --cov-report=term-missing
```

Earlier coverage measurements reached 100% source-code coverage.

Because new D22, D23, and distance-selection code was added during Week 5, the coverage command should be run again after these changes to confirm the current final coverage percentage.

Coverage alone does not guarantee that the program is completely free of errors. It only measures whether executable lines have been exercised by the tests. For this reason, tests with manually known expected results, representative 28 × 28 inputs, and integration tests are also used to verify the actual behaviour of the algorithms.

## Code-quality analysis

Pylint is used to analyse source-code quality.

It can be run with:

```bash
poetry run pylint src/digitrecognition demo.py
```

Pylint is used together with the automated tests to identify code-quality
issues that do not necessarily cause test failures.

A final Pylint run will be performed after the remaining Week 5 changes.

## Peer-review feedback

The first peer review reported that the project was structured clearly,
documented well, and that the existing tests passed successfully.

The reviewer also suggested adding tests with larger or more representative
inputs because many of the original tests used small hand-built examples.

This feedback was addressed during Week 5 by adding:

- a 28 × 28 nearest-point search test;
- a 28 × 28 point-set distance test.

The new tests preserve manually verifiable behaviour while using input sizes that are more representative of the 28 × 28 MNIST images that will later be processed by the program.

## Current testing limitations

The current tests still use artificial images and point sets rather than genuine MNIST images.

Some tests now use 28 × 28 inputs matching the dimensions of MNIST images, but real MNIST data has not yet been integrated into the test suite.

The integration tests currently cover only artificial representations of digits 1 and 7.

The following testing tasks therefore remain:

- testing preprocessing with genuine MNIST images;
- testing classification with all digit classes from 0 to 9;
- measuring classification accuracy;
- comparing the accuracy of D22, D23, and the unnormalized D23 variation;
- measuring execution time on larger MNIST subsets;
- investigating performance when many reference images are used.

These tests will be added as MNIST integration and performance evaluation are implemented.