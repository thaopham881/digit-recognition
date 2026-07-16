# Specification Document

## Programming language

The project will be implemented in Python.

## Project topic

Stock Price Pattern Similarity Search Using Dynamic Time Warping.

## Problem to be solved

The program will compare historical stock price movements and identify periods with patterns similar to a selected query period.

The purpose is not to predict future stock prices. The purpose is to implement and study an algorithm for measuring similarity between time-series sequences.

## Inputs

The program will receive historical stock price data from CSV files.

The data will contain:

- dates
- closing prices

The user will select:

- the stock price period used as the query pattern
- the length of the comparison windows
- the number of similar patterns to return

## Outputs

The program will return historical stock price windows ranked according to their similarity to the selected query pattern.

Each result will include:

- the corresponding historical period
- its Dynamic Time Warping distance
- its similarity ranking

## Algorithms and data structures

The main algorithm will be Dynamic Time Warping, abbreviated as DTW.

Dynamic Time Warping uses dynamic programming to compare two time-series sequences. It can identify similar patterns even when movements do not occur at exactly the same speed.

The program will also use a sliding-window search to compare a query pattern with multiple historical periods.

## Expected time complexity

For two sequences with lengths n and m, the expected time complexity of the basic Dynamic Time Warping implementation is:

O(n × m)

If all comparison windows have length w and there are k historical windows, the expected search complexity is approximately:

O(k × w²)

## Expected space complexity

A complete Dynamic Time Warping matrix has an expected space complexity of:

O(n × m)

A possible improvement would be a memory-optimized implementation.

## Core of the project

The core of the project is the implementation of the Dynamic Time Warping algorithm and its use in searching historical stock price data for similar patterns.

Stock data loading, visualization, and the user interface are supporting functionality rather than the core of the project.

## Sources

Sources concerning Dynamic Time Warping, time-series similarity, algorithm complexity, and software testing will be added during development.

## Study programme

Master's Degree in the Master's Programme in Mathematics and Statistics 

## Documentation language

English