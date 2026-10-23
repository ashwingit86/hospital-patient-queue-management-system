"""Priority Queue implemented from scratch as a binary min-heap (array based).

The item with the SMALLEST key is served first. For patients the key is
(severity, pid), so Emergency (1) beats Urgent (2), and patients with the
same severity are served in arrival order.

Array layout: parent(i) = (i-1)//2, left(i) = 2i+1, right(i) = 2i+2
"""


class PriorityQueue:
    def __init__(self, key=lambda item: item):
        self._heap = []
        self._key = key

    # ---------- public operations ----------
    def push(self, item):
        """Insert an item. O(log n)."""
        self._heap.append(item)
        self._sift_up(len(self._heap) - 1)

    def pop(self):
        """Remove and return the highest-priority item. O(log n)."""
        if not self._heap:
            raise IndexError("pop from an empty priority queue")
        top = self._heap[0]
        last = self._heap.pop()
        if self._heap:
            self._heap[0] = last
            self._sift_down(0)
        return top

    def peek(self):
        """Look at the highest-priority item without removing it. O(1)."""
        if not self._heap:
            raise IndexError("peek from an empty priority queue")
        return self._heap[0]

    def remove(self, predicate):
        """Remove the first item matching predicate (e.g. a cancelled patient).

        O(n) to find it + O(log n) to repair the heap. Returns the item or None.
        """
        for index, item in enumerate(self._heap):
            if predicate(item):
                last = self._heap.pop()
                if index < len(self._heap):          # removed item was not the last one
                    self._heap[index] = last
                    parent = (index - 1) // 2
                    if index > 0 and self._key(last) < self._key(self._heap[parent]):
                        self._sift_up(index)
                    else:
                        self._sift_down(index)
                return item
        return None

    def to_sorted_list(self):
        """All items in service order, without changing the queue. O(n log n)."""
        copy = PriorityQueue(self._key)
        copy._heap = list(self._heap)
        out = []
        while copy._heap:
            out.append(copy.pop())
        return out

    def is_empty(self):
        return not self._heap

    def __len__(self):
        return len(self._heap)

    # ---------- heap maintenance ----------
    def _sift_up(self, i):
        heap, key = self._heap, self._key
        while i > 0:
            parent = (i - 1) // 2
            if key(heap[i]) < key(heap[parent]):
                heap[i], heap[parent] = heap[parent], heap[i]
                i = parent
            else:
                break

    def _sift_down(self, i):
        heap, key = self._heap, self._key
        n = len(heap)
        while True:
            smallest = i
            left, right = 2 * i + 1, 2 * i + 2
            if left < n and key(heap[left]) < key(heap[smallest]):
                smallest = left
            if right < n and key(heap[right]) < key(heap[smallest]):
                smallest = right
            if smallest == i:
                break
            heap[i], heap[smallest] = heap[smallest], heap[i]
            i = smallest
