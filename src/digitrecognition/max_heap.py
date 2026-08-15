"""Fixed-size binary max-heap for nearest-neighbour candidates."""


HeapItem = tuple[float, int]


class KNearestHeap:
    """Keep the k smallest distance-label pairs in a binary max-heap."""

    def __init__(self, capacity: int):
        """Create an empty heap with a fixed maximum capacity.

        Args:
            capacity: Maximum number of items stored in the heap.

        Raises:
            ValueError: If capacity is not positive.
        """
        if capacity <= 0:
            raise ValueError("Heap capacity must be greater than zero.")

        self.capacity = capacity
        self._items: list[HeapItem] = []

    def __len__(self) -> int:
        """Return the number of items currently stored."""
        return len(self._items)

    def add(self, item: HeapItem) -> None:
        """Add an item if it belongs among the k smallest items.

        The root of the max-heap contains the worst currently retained
        neighbour. A new better neighbour replaces the root when the heap
        is already full.

        Args:
            item: A distance-label pair.
        """
        if len(self._items) < self.capacity:
            self._items.append(item)
            self._sift_up(len(self._items) - 1)
            return

        if self._is_better(item, self._items[0]):
            self._items[0] = item
            self._sift_down(0)

    def to_sorted_list(self) -> list[HeapItem]:
        """Return retained items ordered from nearest to farthest."""
        return sorted(
            self._items,
            key=lambda item: (item[0], item[1]),
        )

    @staticmethod
    def _is_worse(first: HeapItem, second: HeapItem) -> bool:
        """Return whether first should be higher in the max-heap."""
        if first[0] != second[0]:
            return first[0] > second[0]

        return first[1] > second[1]

    @staticmethod
    def _is_better(first: HeapItem, second: HeapItem) -> bool:
        """Return whether first is a better neighbour than second."""
        if first[0] != second[0]:
            return first[0] < second[0]

        return first[1] < second[1]

    def _sift_up(self, index: int) -> None:
        """Restore max-heap ordering after inserting an item."""
        while index > 0:
            parent_index = (index - 1) // 2

            if not self._is_worse(
                self._items[index],
                self._items[parent_index],
            ):
                break

            self._items[index], self._items[parent_index] = (
                self._items[parent_index],
                self._items[index],
            )

            index = parent_index

    def _sift_down(self, index: int) -> None:
        """Restore max-heap ordering after replacing the root."""
        size = len(self._items)

        while True:
            left_child = 2 * index + 1
            right_child = 2 * index + 2
            worst_index = index

            if (
                left_child < size
                and self._is_worse(
                    self._items[left_child],
                    self._items[worst_index],
                )
            ):
                worst_index = left_child

            if (
                right_child < size
                and self._is_worse(
                    self._items[right_child],
                    self._items[worst_index],
                )
            ):
                worst_index = right_child

            if worst_index == index:
                break

            self._items[index], self._items[worst_index] = (
                self._items[worst_index],
                self._items[index],
            )

            index = worst_index