"""Searching algorithms (written from scratch). Both return an index, or -1."""


def linear_search(patients, pid):
    """Check every element one by one. O(n). Works on any list."""
    for index, patient in enumerate(patients):
        if patient.pid == pid:
            return index
    return -1


def binary_search(patients, pid):
    """Halve the search range each step. O(log n).

    Requires the list to be sorted by pid. The master patient list always is,
    because IDs are assigned in increasing order and patients are appended.
    """
    low, high = 0, len(patients) - 1
    while low <= high:
        mid = (low + high) // 2
        if patients[mid].pid == pid:
            return mid
        if patients[mid].pid < pid:
            low = mid + 1
        else:
            high = mid - 1
    return -1
