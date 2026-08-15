"""Tests for the fixed-size k-nearest-neighbour max-heap."""

import pytest

from digitrecognition.max_heap import KNearestHeap


def test_new_heap_is_empty():
    """A new heap should contain no items."""
    heap = KNearestHeap(capacity=3)

    assert len(heap) == 0
    assert heap.to_sorted_list() == []


def test_heap_accepts_items_until_capacity():
    """Items should be stored while the heap is not full."""
    heap = KNearestHeap(capacity=3)

    heap.add((3.0, 3))
    heap.add((1.0, 1))
    heap.add((2.0, 2))

    assert len(heap) == 3
    assert heap.to_sorted_list() == [
        (1.0, 1),
        (2.0, 2),
        (3.0, 3),
    ]


def test_heap_keeps_only_k_smallest_distances():
    """A full heap should discard worse neighbours."""
    heap = KNearestHeap(capacity=3)

    heap.add((5.0, 5))
    heap.add((2.0, 2))
    heap.add((8.0, 8))
    heap.add((1.0, 1))
    heap.add((4.0, 4))

    assert heap.to_sorted_list() == [
        (1.0, 1),
        (2.0, 2),
        (4.0, 4),
    ]


def test_worse_item_is_ignored_when_heap_is_full():
    """An item worse than all retained neighbours should be ignored."""
    heap = KNearestHeap(capacity=2)

    heap.add((1.0, 1))
    heap.add((2.0, 2))
    heap.add((10.0, 9))

    assert heap.to_sorted_list() == [
        (1.0, 1),
        (2.0, 2),
    ]


def test_smaller_label_wins_when_distances_are_equal():
    """Equal distances should prefer the smaller numerical label."""
    heap = KNearestHeap(capacity=2)

    heap.add((1.0, 7))
    heap.add((1.0, 5))
    heap.add((1.0, 2))

    assert heap.to_sorted_list() == [
        (1.0, 2),
        (1.0, 5),
    ]


def test_invalid_capacity_raises_error():
    """Heap capacity must be positive."""
    with pytest.raises(ValueError):
        KNearestHeap(capacity=0)