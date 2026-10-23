"""Sorting algorithms (written from scratch, no built-in sort).

All three are STABLE (equal keys keep their original order), accept a key
function, and return a NEW sorted list. Use reverse=True for descending.
"""


def _out_of_order(a, b, reverse):
    """True if a should come AFTER b."""
    return a < b if reverse else a > b


def bubble_sort(items, key=lambda x: x, reverse=False):
    """Repeatedly swap neighbouring items. O(n^2) worst, O(n) if already sorted."""
    arr = list(items)
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if _out_of_order(key(arr[j]), key(arr[j + 1]), reverse):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def insertion_sort(items, key=lambda x: x, reverse=False):
    """Insert each item into the sorted part on its left. O(n^2), good for small lists."""
    arr = list(items)
    for i in range(1, len(arr)):
        current = arr[i]
        current_key = key(current)
        j = i - 1
        while j >= 0 and _out_of_order(key(arr[j]), current_key, reverse):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = current
    return arr


def merge_sort(items, key=lambda x: x, reverse=False):
    """Divide and conquer. O(n log n) always, O(n) extra space."""
    arr = list(items)
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key, reverse)
    right = merge_sort(arr[mid:], key, reverse)

    merged, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if _out_of_order(key(left[i]), key(right[j]), reverse):
            merged.append(right[j])
            j += 1
        else:                       # ties take from the left -> stable
            merged.append(left[i])
            i += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


ALGORITHMS = {
    "merge": merge_sort,
    "insertion": insertion_sort,
    "bubble": bubble_sort,
}
