# Testing Document

## Testing approach

The project uses automated unit tests implemented with pytest.

Tests are developed alongside the program code. The tests use small and
representative artificial images and point sets so that the expected results
can be calculated manually.

The tests currently cover:

- conversion of grayscale images into coordinate lists and Boolean grids;
- validation of grayscale thresholds and image dimensions;
- generation of coordinate offsets;
- ordering of offsets by Euclidean distance;
- optimized nearest-point searches;
- exhaustive nearest-point fallback searches;
- symmetric point-set distance calculations;
- selection of the k nearest reference images;
- majority voting and tie-breaking in k-nearest neighbours classification;
- invalid and empty input handling.

## Image representation tests

The image representation tests verify that active pixels are correctly stored
in both the coordinate list and the Boolean grid.

The tests also cover:

- pixels equal to the selected threshold;
- empty images;
- thresholds outside the range 0–255;
- images whose rows have unequal lengths.

## Offset generation tests

The offset tests verify that a square search area contains the correct number
of offsets.

They also verify that:

- the centre position has distance zero and is checked first;
- the offsets are sorted by increasing Euclidean distance;
- diagonal distances are calculated correctly;
- even, zero, and otherwise invalid search sizes are rejected.

## Nearest-point search tests

The nearest-point tests verify that the algorithm finds points:

- at the same coordinate;
- at horizontally or vertically adjacent coordinates;
- at diagonal coordinates;
- outside the precomputed local search area.

The distant-point case verifies that the exhaustive coordinate-list fallback
is used when the local Boolean-grid search does not find a point.

The tests also verify coordinate boundary checking and empty reference-point
handling.

## Point-set distance tests

The point-set distance tests use small manually constructed point sets.

They verify that:

- identical point sets have distance zero;
- shifted points produce the expected Euclidean distance;
- nearest-point distances are averaged correctly;
- the larger directed average is selected by the current symmetric distance;
- empty point sets are rejected.

The current symmetric average distance is an initial working distance measure.
The final project will later include the required D22 and D23 distance
measures.

## K-nearest neighbours tests

The k-nearest neighbours tests verify that:

- reference images are sorted from nearest to farthest;
- only the requested number of neighbours is returned;
- total neighbour distance is used to resolve a vote tie;
- the smaller label is used as a final deterministic tie-breaker;
- invalid values of k are rejected;
- empty training and neighbour lists are rejected;
- the complete classification function returns both the predicted label and
  the selected neighbours.

## Integration testing

In addition to unit tests, the project contains integration tests that verify
the complete classification pipeline.

The integration tests begin with grayscale image data and execute the
following steps together:

1. convert the grayscale images into coordinate lists and Boolean grids;
2. generate the sorted local-search offsets;
3. calculate point-set distances;
4. find the k nearest labelled reference images;
5. perform majority voting;
6. return the predicted digit label.

The tests use two artificial test images representing digits 1 and 7. Each
test image is classified against a small training set containing two examples
of digit 1 and two examples of digit 7.

The test for digit 1 verifies that:

- the predicted label is 1;
- exactly three neighbours are returned when `k = 3`;
- the neighbours are ordered by increasing distance.

The test for digit 7 verifies the same behaviour and expects the predicted
label to be 7.

The integration tests can be run separately with:

```bash
poetry run pytest tests/test_integration.py -v
```

At the end of Week 4, both integration tests pass successfully.

These tests differ from the individual unit tests because they exercise
multiple program modules together, from grayscale image conversion to the
final classification result.

## Test coverage

Test coverage is measured using pytest-cov.

The coverage report can be generated with:

```bash
poetry run pytest --cov=digitrecognition --cov-report=term-missing
```

At the end of Week 4, the project contains 38 automated tests. All 38 tests
pass successfully.

The source-code test coverage is 100%.

The coverage percentage does not guarantee that the program is completely
free of errors. It confirms that every executable source-code line is
executed by at least one test. Representative unit and integration tests are
therefore also used to verify the actual behaviour of the algorithms.

## Code-quality analysis

Pylint is used to analyse source-code quality.

It can be run with:

```bash
poetry run pylint src/digitrecognition demo.py
```

At the end of Week 4, Pylint gives the project a score of 9.49 out of 10.

The remaining warnings currently concern missing final newlines and similar
argument-passing code. These warnings do not affect the correctness of the
implemented algorithms.

## Current testing limitations

The current tests use small artificial images rather than genuine MNIST
images.

The integration tests currently cover only artificial representations of
digits 1 and 7. Testing with realistic MNIST images, classification-accuracy
measurement, and large-scale performance testing remain future work.

The current symmetric average distance is an intermediate working distance
measure. Tests for the final D22 and D23 measures will be added when those
measures are implemented.