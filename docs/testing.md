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

## Test coverage

Test coverage is measured using pytest-cov.

The coverage report can be generated with:

```bash
poetry run pytest --cov=digitrecognition --cov-report=term-missing