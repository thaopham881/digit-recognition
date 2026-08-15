# Testing Document

## Testing approach

The project uses automated unit and integration tests implemented with pytest.

Tests are developed alongside the program code. Small manually constructed images and point sets are used where possible so that expected results can be calculated independently.

Larger 28 × 28 artificial inputs are also used to test the algorithms with image dimensions similar to MNIST.

During Week 6, the test suite was extended to cover:

* the fixed-size binary max-heap;
* loading MNIST images;
* loading MNIST labels;
* invalid MNIST files;
* MNIST preprocessing;
* classification evaluation;
* the MNIST experiment;
* the updated heap-based k-nearest-neighbour implementation.

The complete test suite currently contains **72 tests**.

All 72 tests pass.

## Running the tests

Run the complete test suite with:

```bash
poetry run pytest
```

The current result is:

```text
72 passed
```

Run the tests with coverage using:

```bash
poetry run pytest --cov=digitrecognition --cov-report=term-missing
```

The current source-code coverage is **99%**.

The only uncovered statement is the direct script entry-point call in `mnist_experiment.py`:

```python
if __name__ == "__main__":
    main()
```

The algorithmic implementation itself is covered by the automated tests.

## Current test distribution

The current tests are divided approximately as follows:

| Test file                      |  Tests |
| ------------------------------ | -----: |
| `test_evaluation.py`           |      5 |
| `test_image_representation.py` |      6 |
| `test_integration.py`          |      2 |
| `test_knn.py`                  |     12 |
| `test_max_heap.py`             |      6 |
| `test_mnist_experiment.py`     |      1 |
| `test_mnist_loader.py`         |     11 |
| `test_nearest_point.py`        |     11 |
| `test_offset.py`               |      6 |
| `test_point_set_distance.py`   |     12 |
| **Total**                      | **72** |

## Image representation tests

The image-representation tests verify that grayscale images are correctly converted into:

* coordinate lists;
* Boolean grids.

The tests cover:

* active and inactive pixels;
* pixels equal to the selected threshold;
* empty images;
* thresholds outside the range 0–255;
* images whose rows have unequal lengths.

These tests verify the preprocessing step used before point-set distance calculations.

## Offset generation tests

The offset tests verify that coordinate offsets are generated correctly for the local nearest-point search.

The tests verify:

* the expected number of offsets;
* the centre coordinate has distance zero;
* the centre is checked first;
* offsets are sorted by increasing Euclidean distance;
* diagonal distances are calculated correctly;
* invalid search sizes are rejected.

The ordering is important because the nearest-point search examines candidate positions from shortest to longest distance.

## Nearest-point search tests

The nearest-point tests verify both the optimized local search and the exhaustive reference search.

The tests cover points:

* at exactly the same coordinate;
* horizontally or vertically adjacent;
* diagonally adjacent;
* farther away from the source coordinate;
* outside the local search area.

The tests also verify:

* coordinate boundary checking;
* empty-reference handling;
* exhaustive fallback behaviour;
* agreement between optimized and exhaustive search in representative cases.

During Week 5, a larger 28 × 28 test was added after peer-review feedback.

The larger test contains multiple reference and query points. Results from the optimized search are compared with results from the exhaustive implementation.

This provides a stronger correctness check with image-sized inputs rather than relying only on very small examples.

## Point-set distance tests

The point-set distance tests use manually constructed point sets whose expected values can be calculated directly.

The tests cover:

* identical point sets;
* shifted point sets;
* directed average nearest-point distance;
* directed sum nearest-point distance;
* empty point-set validation;
* D22;
* D23;
* unnormalized D23;
* the compatibility wrapper for D22.

For example, consider:

```text
A = [(0, 0), (0, 1)]
B = [(0, 0)]
```

The directed average from A to B is `0.5`.

The directed average from B to A is `0.0`.

Therefore:

```text
D22 = max(0.5, 0.0) = 0.5
D23 = (0.5 + 0.0) / 2 = 0.25
```

The unnormalized variation uses the directed sums instead.

A 28 × 28 point-set test was also added during Week 5. The second point set is shifted horizontally by one pixel, allowing an expected D22 value of `1.0` to be verified on a more representative input.

## K-nearest-neighbours tests

The k-nearest-neighbour tests verify both neighbour selection and classification.

The tests cover:

* returning exactly `k` neighbours;
* ordering neighbours from nearest to farthest;
* majority voting;
* vote ties;
* total-distance tie-breaking;
* final numerical-label tie-breaking;
* invalid `k`;
* empty training sets;
* empty neighbour lists;
* complete prediction;
* selecting D22;
* selecting D23;
* selecting unnormalized D23;
* rejecting an unknown distance-measure name.

During Week 6, k-nearest-neighbour selection was changed from storing all distances and sorting them to maintaining only the current `k` nearest candidates in a max-heap.

Tests verify that this change preserves the expected classification behaviour.

## Max-heap tests

The fixed-size max-heap has its own unit tests.

These verify that:

* a new heap is empty;
* items can be inserted until capacity is reached;
* only the `k` smallest distances are retained;
* a worse candidate is ignored when the heap is already full;
* equal distances use the smaller numerical label deterministically;
* invalid heap capacity raises a `ValueError`.

Testing the heap separately is important because it is now an algorithmic component of the k-nearest-neighbour implementation.

## MNIST loader tests

The MNIST loader tests verify the loading of compressed IDX image and label files.

The tests create small artificial IDX files so that behaviour can be checked without depending on the complete external MNIST dataset.

The tests cover:

* correctly loading image files;
* correctly loading label files;
* limiting the number of loaded items;
* invalid limits;
* incorrect image magic numbers;
* incorrect label magic numbers;
* invalid image dimensions;
* incomplete image data;
* incomplete label data;
* malformed files.

This verifies that the program detects invalid MNIST input instead of silently accepting corrupted data.

## Evaluation tests

The evaluation tests cover the functions that prepare training images and evaluate predictions.

The tests verify that:

* grayscale training images are converted into the required point-set representations;
* labels remain associated with their corresponding images;
* multiple images can be prepared;
* predictions are compared with their expected labels;
* the number of correct predictions and calculated accuracy are returned correctly.

These tests use small controlled examples rather than running the complete MNIST experiment.

This keeps the automated tests fast and deterministic.

## MNIST experiment test

The MNIST experiment has a separate test that verifies the experiment command's overall control flow.

The test checks that the experiment:

* loads the required data;
* prepares training images;
* runs evaluation;
* reports the resulting statistics.

The test does not repeatedly perform the full 500-training-image experiment because that experiment takes approximately one minute on the development computer.

Instead, the expensive components are replaced with controlled test values so that the command can be tested quickly.

## Integration testing

The project also contains integration tests for the complete artificial-image classification pipeline.

These tests begin with grayscale image data and perform the following steps together:

1. convert the images into coordinate lists and Boolean grids;
2. generate nearest-point search offsets;
3. calculate point-set distances;
4. find the k nearest labelled images;
5. perform majority voting;
6. return the predicted digit.

The tests use artificial examples representing digits 1 and 7.

They verify that the complete pipeline correctly classifies both examples and returns the expected neighbours.

These tests differ from individual unit tests because several modules are exercised together.

## Real MNIST experiment

In addition to the automated tests, the program has been run manually on real MNIST data.

The experiment was executed with:

```text
Training images: 500
Test images: 20
Threshold: 128
k: 3
Offset size: 11
Distance measure: d22
```

The result was:

```text
Correct predictions: 19/20
Accuracy: 95.00%
Elapsed time: 54.02 seconds
```

This is not treated as an automated accuracy test.

The sample of only 20 test images is too small to establish reliable general MNIST accuracy, and the experiment is relatively slow.

Instead, it demonstrates that the complete implementation can process and classify genuine MNIST images successfully.

## Coverage

Coverage is measured using pytest-cov.

The current coverage result is:

```text
Name                                           Cover
----------------------------------------------------
src/digitrecognition/__init__.py                100%
src/digitrecognition/evaluation.py              100%
src/digitrecognition/image_representation.py    100%
src/digitrecognition/knn.py                     100%
src/digitrecognition/max_heap.py                100%
src/digitrecognition/mnist_experiment.py         98%
src/digitrecognition/mnist_loader.py            100%
src/digitrecognition/nearest_point.py            100%
src/digitrecognition/offsets.py                  100%
src/digitrecognition/point_set_distance.py       100%
----------------------------------------------------
TOTAL                                             99%
```

The uncovered line in `mnist_experiment.py` is the script entry point used when the program is executed directly as a module.

The underlying `main` functionality is tested.

## Code quality

Pylint is used in addition to the automated tests.

It can be run with:

```bash
poetry run pylint src tests
```

The current Pylint score is:

```text
9.56/10
```

Pylint is not a correctness test, but it helps identify code-quality, formatting, and maintainability issues.

## Peer-review response

The first peer review suggested that the project should include more representative test inputs.

Earlier tests relied heavily on very small point sets and grids because their expected values were easy to calculate manually.

In response, larger 28 × 28 tests were added during Week 5.

These tests more closely resemble MNIST image dimensions while still keeping the expected behaviour controlled.

The feedback demonstrated that high code coverage alone does not guarantee that test inputs are representative.

## Current testing limitations

The current tests provide strong coverage of the implemented code, but some limitations remain.

The main limitations are:

* the full 60,000-image MNIST training set is not used during automated testing;
* classification accuracy has only been demonstrated on a small experiment;
* performance is not tested automatically because timing results depend on the computer;
* D22, D23, and unnormalized D23 have not been systematically compared on large real-MNIST samples;
* additional randomized comparisons between optimized and exhaustive nearest-point searching could provide further validation.

Despite these limitations, the test suite covers all main algorithmic components individually as well as the complete classification pipeline.
