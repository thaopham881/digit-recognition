# Specification Document

## 1. Programming language and peer-review languages

The project will be implemented in Python 3. Poetry will be used for dependency and project management.

I can confidently peer-review projects written in Python. I have some familiarity with other languages and tools, but not enough to confidently peer-review a complete algorithm project written in them.

## 2. Problem to be solved

The purpose of the project is to implement a program that recognizes handwritten digits from the MNIST dataset. The dataset contains grayscale images of handwritten digits from 0 to 9.

The program will classify an unknown test image by comparing it with labeled training images using the k-nearest neighbors algorithm. Instead of comparing the images as ordinary numerical matrices, each image will be converted into a set of foreground-pixel coordinates. The similarity between two images will then be measured using distance measures intended for point sets.

The main computational problem is that one test image may need to be compared with as many as 60,000 training images. The distance calculation must therefore avoid comparing every point in one image with every point in the other image whenever a nearer point can be found more efficiently.

## 3. Inputs and outputs

The program will receive the following inputs from the user:

- a grayscale threshold used to convert MNIST images into black-and-white images;
- the value of `k` used by the k-nearest neighbors classifier;
- the point-set distance measure to be used;
- one test-image index or a range of test images to classify;
- optionally, the size of the local nearest-point search area.

A pixel will be included in the point set when its grayscale value passes the selected threshold.

For an individual classification, the program will display:

- the test image;
- its actual label;
- its predicted label;
- the `k` nearest training images;
- the labels and distances of those neighboring images.

The program will also contain a performance-testing mode. It will measure classification accuracy and execution time using a configurable part of the test set. The goal is to test the complete set of 10,000 test images if this is computationally practical.

## 4. Algorithms and data structures

### 4.1 Image preprocessing

Each grayscale MNIST image will be converted into a binary image using the user-selected threshold.

Each thresholded image will be stored in two forms:

1. **Coordinate list:** a list of `(x, y)` coordinates for all foreground pixels.
2. **Boolean array:** a 28 × 28 Boolean representation that allows the program to check in constant time whether a particular coordinate contains a foreground pixel.

The coordinate list makes it unnecessary to iterate over background pixels. The Boolean array supports efficient membership checks during the nearest-point search.

### 4.2 Precomputed offset list

The program will precompute a list of coordinate offsets inside a configurable square search area, initially an 11 × 11 area.

Every entry will contain:

```text
(dx, dy, distance)
```

The entries will be sorted in ascending order by Euclidean distance. The first entries will therefore represent the same coordinate and its nearest surrounding coordinates.

The offset list will be generated once and reused during image comparisons.

### 4.3 Efficient nearest-point search

For every foreground point in image `A`, the program must find the nearest foreground point in image `B`.

The program will first scan the precomputed offsets in ascending distance order. For every offset, it will check the corresponding position in image `B`'s Boolean array. The first foreground pixel found is the nearest point inside the local search area.

Coordinates that fall outside the 28 × 28 image will be ignored.

If no foreground point is found within the local search area, the program will perform a fallback search. It will iterate through the complete coordinate list of image `B`, calculate the Euclidean distance to every point, and select the smallest distance.

The same search must also be performed in the opposite direction, from image `B` to image `A`.

### 4.4 Point-set distance measures

The project will implement point-set distance measures described in *A Modified Hausdorff Distance for Object Matching*.

The planned distance measures are:

- D22;
- D23;
- a D23 variation in which the `1/N` factor is removed from the `d6` subformula.

The exact formulas will follow the notation and definitions in the original article and the course topic description.

The different measures will be compared using classification accuracy and execution time.

### 4.5 k-nearest neighbors classification

For each test image, the program will:

1. calculate its point-set distance to every selected training image;
2. retain the `k` training images with the smallest distances;
3. count the labels among the `k` nearest images;
4. predict the label that occurs most often.

If two labels receive the same number of votes, the program will use the total or smallest distance of the tied neighbors as a tie-breaking rule. A deterministic final tie-breaking rule will also be added.

A bounded heap from Python's standard library may be used to retain the current `k` nearest neighbors efficiently. The classifier itself and all point-set distance calculations will be implemented as part of the project.

The program will not use a ready-made k-NN classifier, ready-made point-set distance implementation, or pre-built matrix operations for the central algorithm.

## 5. Expected time and space complexities

The following notation is used:

- `T` = number of training images;
- `Q` = number of test images being classified;
- `P` = number of pixels in an image;
- `a` = number of foreground points in image `A`;
- `b` = number of foreground points in image `B`;
- `S` = number of offsets in the local search area;
- `k` = number of nearest neighbors.

For MNIST, `P = 28 × 28 = 784`, but the complexity is described using variables so that the reason for the running time remains visible.

### Image preprocessing

Thresholding one image requires checking every pixel:

- Time: `O(P)`
- Space: `O(P)`

Preprocessing all training images requires:

- Time: `O(TP)`
- Space: `O(TP)`

### Offset generation

Generating and sorting `S` offsets requires:

- Time: `O(S log S)`
- Space: `O(S)`

This work is performed only once.

### Directed nearest-point distance

For every point in `A`, up to `S` local offsets may be checked.

If the local search fails, all `b` points in `B` must also be inspected. The worst-case time for the directed distance from `A` to `B` is therefore:

```text
O(a(S + b))
```

The search in both directions has the worst-case complexity:

```text
O(a(S + b) + b(S + a))
```

This can also be written as:

```text
O((a + b)S + ab)
```

The local search is expected to improve practical performance because corresponding pixels in similar digit images are often located close to one another. However, the fallback search is still required to guarantee that the actual nearest point is found.

### Classifying one test image

The test image is compared with `T` training images. Maintaining a bounded heap of `k` neighbors requires at most `O(log k)` work per training image.

The worst-case time is therefore:

```text
O(T((a + b)S + ab + log k))
```

Because the number of foreground points differs between images, `a` and `b` represent the compared images rather than fixed values.

### Performance testing

Classifying `Q` test images has the worst-case complexity:

```text
O(QT((a + b)S + ab + log k))
```

### Space complexity

The processed training images require:

```text
O(TP)
```

The offset list and the bounded neighbor heap require:

```text
O(S + k)
```

The total planned space complexity is therefore:

```text
O(TP + S + k)
```

If all processed test images are also kept in memory, their storage adds `O(QP)`.

## 6. Core of the project

The core of the project is the manual implementation and optimization of distance calculations between point sets representing handwritten digits.

The most important part is the nearest-point search that combines coordinate lists, Boolean arrays, distance-sorted offsets, and an exhaustive fallback search. The project will then use the implemented D22 and D23 point-set distance measures as the distance function of a k-nearest neighbors classifier.

The command-line interface, image display, dataset loading, and result presentation support the core algorithm but are not the main focus of the project.

## 7. Testing plan

Automated unit tests will be developed alongside the implementation.

The tests will cover at least:

- conversion of grayscale images into Boolean arrays and coordinate lists;
- generation and correct ordering of offsets;
- handling of image boundaries;
- nearest-point searches where a point is found locally;
- fallback searches where no point exists in the local area;
- point-set distance calculations using small manually constructed point sets;
- behavior with identical images;
- handling of empty or unusual point sets;
- selection of the `k` nearest neighbors;
- majority voting and tie-breaking;
- small end-to-end classification examples.

Test coverage will be measured using a Python coverage tool. Performance tests will compare local-search sizes and point-set distance measures using representative MNIST images.

The user interface itself does not need automated testing because the course requires testing of the program logic rather than the interface.

## 8. Planned program structure

The project is expected to include separate modules for:

- loading MNIST data;
- thresholding and image representation;
- offset generation;
- nearest-point searches;
- point-set distance measures;
- k-nearest neighbors classification;
- performance and accuracy measurement;
- command-line interaction and image display.

The exact structure may change as the implementation develops.

## 9. Study programme

Master’s Programme in Mathematics and Statistics.

## 10. Documentation language

English.
