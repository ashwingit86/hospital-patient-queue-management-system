"""FIFO Queue implemented from scratch with a singly linked list.

Used for ROUTINE patients: first to arrive is first to be called.
"""


class _Node:
    __slots__ = ("data", "next")

    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedQueue:
    def __init__(self):
        self.front = None   # dequeue happens here
        self.rear = None    # enqueue happens here
        self._size = 0

    def enqueue(self, item):
        """Add at the rear. O(1)."""
        node = _Node(item)
        if self.rear is None:
            self.front = self.rear = node
        else:
            self.rear.next = node
            self.rear = node
        self._size += 1

    def dequeue(self):
        """Remove and return the front item. O(1)."""
        if self.front is None:
            raise IndexError("dequeue from an empty queue")
        node = self.front
        self.front = node.next
        if self.front is None:
            self.rear = None
        self._size -= 1
        return node.data

    def peek(self):
        if self.front is None:
            raise IndexError("peek from an empty queue")
        return self.front.data

    def remove(self, predicate):
        """Remove the first item for which predicate(item) is True. O(n).

        Returns the removed item, or None if nothing matched.
        """
        prev, cur = None, self.front
        while cur is not None:
            if predicate(cur.data):
                if prev is None:
                    self.front = cur.next
                else:
                    prev.next = cur.next
                if cur is self.rear:
                    self.rear = prev
                self._size -= 1
                return cur.data
            prev, cur = cur, cur.next
        return None

    def is_empty(self):
        return self._size == 0

    def to_list(self):
        """Items from front to rear (does not modify the queue). O(n)."""
        out, cur = [], self.front
        while cur is not None:
            out.append(cur.data)
            cur = cur.next
        return out

    def __len__(self):
        return self._size

    def __iter__(self):
        return iter(self.to_list())
