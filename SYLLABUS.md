# DSA Syllabus Mapping

Every data structure and algorithm below is implemented from scratch in this project.

## Topic to feature to file

| # | DSA topic | Feature in the app | Source file | Key function(s) |
|---|---|---|---|---|
| 1 | Queue (FIFO), linked list | Routine patients wait in arrival order | `src/queue_ds.py` | `enqueue`, `dequeue`, `remove` |
| 2 | Priority queue, binary heap | Emergency and urgent patients are called first | `src/priority_queue.py` | `push`, `pop`, `_sift_up`, `_sift_down`, `remove` |
| 3 | List | Master record of every patient | `src/hospital.py`, `src/patient.py` | `HospitalSystem.patients` |
| 4 | Searching | Find a patient by ID | `src/searching.py` | `binary_search`, `linear_search` |
| 5 | Sorting | Sorted patient reports | `src/sorting.py` | `merge_sort`, `insertion_sort`, `bubble_sort` |

## Complexity table

| Operation | Structure / algorithm | Time | Space |
|---|---|---|---|
| Register routine patient | Linked-list queue `enqueue` | O(1) | O(1) |
| Register emergency/urgent patient | Heap `push` | O(log n) | O(1) |
| Call next patient | Heap `pop` or queue `dequeue` | O(log n) / O(1) | O(1) |
| Cancel a patient | Search in queue/heap, then repair | O(n) | O(1) |
| Search by ID | Binary search | O(log n) | O(1) |
| Search by ID (alternative) | Linear search | O(n) | O(1) |
| Show priority queue in order | Pop all from a copy of the heap | O(n log n) | O(n) |
| Sort all patients | Merge sort | O(n log n) | O(n) |
| Sort all patients | Insertion / bubble sort | O(n²) (best case O(n)) | O(1) beyond the copy |

## Likely viva questions and answers

**1. Why did you use a heap for emergencies?**
A heap gives the highest-priority item in O(1) and removes it in O(log n). Scanning an unsorted list for the most urgent patient would cost O(n) every time.

**2. How do you handle two patients with the same severity?**
The heap key is the tuple `(severity, patient ID)`. IDs increase with arrival, so the earlier arrival has the smaller key and is served first (FIFO within a severity).

**3. Why is the heap an array and not a tree with pointers?**
In a complete binary tree the parent of index `i` is `(i-1)//2` and its children are `2i+1` and `2i+2`, so no pointers are needed. It is compact and cache-friendly.

**4. Why does binary search work on your patient list?**
IDs are assigned in increasing order and patients are only appended, so the list is always sorted by ID. Binary search needs a sorted list.

**5. What is the difference between your three sorting algorithms?**
Merge sort splits the list, sorts each half and merges them: O(n log n) always. Insertion sort grows a sorted prefix: O(n²), fast on nearly-sorted data. Bubble sort swaps neighbours repeatedly: O(n²). All three are stable.

**6. What does stable mean, and why does it matter here?**
Equal keys keep their original relative order. When sorting by severity, patients of the same severity stay in arrival order.

**7. What is starvation, and how do you prevent it?**
If emergencies keep arriving, routine patients could wait forever. After 5 consecutive priority patients, the system calls one waiting routine patient.

**8. How does cancelling a patient from the heap work?**
Find the item (O(n)), replace it with the last element, then sift it up or down to restore the heap property (O(log n)).

**9. Why a linked list for the queue and not a Python list?**
`list.pop(0)` is O(n) because every element shifts. A linked list with front and rear pointers makes both enqueue and dequeue O(1).

**10. What are the limitations?**
Data is not saved to disk, there is a single doctor, and cancelling needs an O(n) search. A hash map from ID to its position would make cancelling faster.
