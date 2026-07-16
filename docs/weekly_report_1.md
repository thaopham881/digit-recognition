# Weekly Report 1

## What did I do this week?

This week, I familiarised myself with the course requirements and reviewed the suggested project topics.

My original topic was considered too narrow, so I discussed an alternative topic with the course assistant. Based on the feedback, I changed my project topic to handwritten digit recognition using the k-nearest neighbors algorithm and point-set distance measures.

I also:

* created the GitHub repository;
* prepared the initial Python project structure;
* configured the project for dependency management;
* wrote the first version of the specification document;
* planned the main algorithms and data structures required for the project.

## How has the program progressed?

The project is currently in the planning and setup stage.

The repository, initial directory structure, and project documentation have been created. The scope of the project has also been approved by the course assistant.

The main digit-recognition algorithm has not yet been implemented. However, I now have a clearer plan for how the program should represent images and calculate distances between them.

## What did I learn this week?

I learned more about how the MNIST handwritten digit dataset can be used for image classification.

I also learned that the grayscale images will first be converted into black-and-white images using a threshold. Each image can then be stored both as:

* a list of coordinates representing black pixels;
* a Boolean array that allows fast checks of whether a pixel is black.

I learned the general idea of using precomputed coordinate offsets to find nearby pixels more efficiently. I also became more familiar with GitHub repositories, Markdown documentation, and the structure of a Python project.

## What remains unclear or has been challenging?

The point-set distance measures, particularly D22 and D23, are still new to me. I need to study their formulas carefully before implementing them.

I am also unsure how fast the complete classification process will be when every test image must be compared with up to 60,000 training images. Performance will therefore be an important challenge during the project.

## What will I do next?

Next week, I plan to:

* study the D22 and D23 point-set distance measures in more detail;
* create the first Python modules for image processing;
* implement the generation of distance-sorted coordinate offsets;
* begin converting sample images into coordinate lists and Boolean arrays;
* write the first automated unit tests;
* start tracking test coverage;
* commit and push progress to GitHub regularly.

## Hours spent

Approximately 13 hours.
