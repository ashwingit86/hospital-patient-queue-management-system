# Architecture

## Module layout

```mermaid
flowchart TD
    M[main.py<br/>menu / demo] --> H[hospital.py<br/>HospitalSystem]
    H --> P[patient.py<br/>Patient record]
    H --> Q[queue_ds.py<br/>LinkedQueue - routine]
    H --> PQ[priority_queue.py<br/>Heap - emergency/urgent]
    H --> S[searching.py<br/>binary / linear search]
    H --> SO[sorting.py<br/>merge / insertion / bubble]
```

## Flowchart: registering a patient

```mermaid
flowchart TD
    A([Start]) --> B[Enter name, age, severity, department]
    B --> C{Input valid?}
    C -- No --> D[Show error message] --> Z([Back to menu])
    C -- Yes --> E[Create Patient with next ID]
    E --> F[Append to patient list]
    F --> G{Severity 1 or 2?}
    G -- Yes --> H[Push into priority queue heap]
    G -- No --> I[Enqueue into routine FIFO queue]
    H --> Z
    I --> Z
```

## Flowchart: calling the next patient

```mermaid
flowchart TD
    A([Doctor is free]) --> B{Both queues empty?}
    B -- Yes --> C[No patients waiting] --> Z([End])
    B -- No --> D{Routine waiting AND<br/>priority queue empty OR<br/>5 priority patients in a row?}
    D -- Yes --> E[Dequeue from routine queue<br/>reset streak to 0]
    D -- No --> F[Pop from priority queue<br/>streak + 1 if routine is waiting]
    E --> G[Mark patient Served, record time]
    F --> G
    G --> H[Display patient] --> Z
```

## Data structure decisions

| Need | Structure chosen | Reason |
|---|---|---|
| Serve urgent cases first, FIFO among equals | Binary min-heap, key `(severity, id)` | O(log n) insert and remove |
| Serve routine cases in arrival order | Linked-list queue | O(1) enqueue and dequeue |
| Keep all patient details | List sorted by ID | Allows binary search and easy reporting |
| Find by ID | Binary search | O(log n) on the sorted list |
| Reports sorted by any field | Merge sort (default) | O(n log n), stable |

## Clock handling

`HospitalSystem` takes a `clock` function that returns the current time in minutes. The menu program uses the real clock. The demo and the unit tests use `SimulatedClock`, which lets time be advanced instantly so waiting times can be shown and tested without actually waiting.
