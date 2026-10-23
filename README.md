# 🏥 Hospital Patient Queue Management System

A menu-driven console application that manages patients waiting for consultation in a hospital. Emergency cases are called before routine ones, and every core feature is built on a **data structure written from scratch** (no built-in `heapq`, `queue`, `sorted()` or `.sort()`).

Written in **Python 3.8+** with no external dependencies.

---

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [DSA Topics Used](#dsa-topics-used)
- [Project Structure](#project-structure)
- [How to Run](#how-to-run)
- [Menu Options](#menu-options)
- [Sample Output](#sample-output)
- [Running Tests](#running-tests)
- [Design Decisions](#design-decisions)
- [Scope Note and Future Work](#scope-note-and-future-work)

---

## Project Overview

Patients register with a name, age, severity and department. Severity decides which queue they join:

| Severity | Level | Goes to |
|---|---|---|
| 1 | Emergency | Priority Queue (heap) |
| 2 | Urgent | Priority Queue (heap) |
| 3 | Routine | FIFO Queue (linked list) |

When the doctor is free, the system calls the next patient: the priority queue is served first (Emergency before Urgent, and first-come-first-served within the same severity), then the routine queue. A **fairness rule** guarantees that after 5 consecutive priority patients, one waiting routine patient is called, so routine patients never starve.

---

## DSA Topics Used

| # | Topic | Feature | Implementation | File | Complexity |
|---|---|---|---|---|---|
| 1 | **Queue (FIFO)** | Keeps the order of routine patients waiting for consultation | Singly linked list with front and rear pointers | `src/queue_ds.py` | Enqueue O(1), Dequeue O(1), Remove O(n) |
| 2 | **Priority Queue** | Emergency and urgent cases get higher priority than routine cases | Array-based binary min-heap on key `(severity, patient ID)` | `src/priority_queue.py` | Push O(log n), Pop O(log n), Peek O(1), Remove O(n) |
| 3 | **List** | Stores every patient's details | Python list of `Patient` objects, always sorted by ID | `src/patient.py`, `src/hospital.py` | Append O(1) |
| 4 | **Searching** | Find a patient by patient ID | Binary search on the ID-sorted list (linear search also provided for comparison) | `src/searching.py` | Binary O(log n), Linear O(n) |
| 5 | **Sorting** | Display all patients by ID, name, severity or waiting time | Merge sort, insertion sort and bubble sort, all stable | `src/sorting.py` | Merge O(n log n), Insertion O(n²), Bubble O(n²) |

### How the structures work together

```
register() ─► Patient added to the LIST (sorted by ID)
                 │
                 ├─ Emergency / Urgent ─► PRIORITY QUEUE (heap)
                 └─ Routine            ─► FIFO QUEUE (linked list)

call_next() ─► priority queue first  (fairness rule lets a routine patient in after 5)
find(id)    ─► BINARY SEARCH on the list
sorted_patients() ─► MERGE / INSERTION / BUBBLE SORT on the list
```

### Key code: heap ordering

```python
def priority_key(self):
    return (self.severity, self.pid)   # lower severity number = more urgent; pid breaks ties (FIFO)
```

The heap always keeps the patient with the smallest key at index 0, so `pop()` returns the most urgent patient in O(log n).

---

## Project Structure

```
hospital-patient-queue-management-system/
├── src/
│   ├── __init__.py
│   ├── patient.py          # Patient record + severity constants        (List item)
│   ├── queue_ds.py         # FIFO queue using a linked list             (Queue)
│   ├── priority_queue.py   # Binary min-heap                            (Priority Queue)
│   ├── searching.py        # Linear + binary search                     (Searching)
│   ├── sorting.py          # Bubble, insertion and merge sort           (Sorting)
│   └── hospital.py         # HospitalSystem: combines everything
├── tests/
│   └── test_system.py      # 22 unit tests
├── docs/
│   ├── SYLLABUS.md         # DSA concept -> feature -> file mapping + viva answers
│   └── ARCHITECTURE.md     # Flowcharts and design decisions
├── main.py                 # Menu-driven program (and --demo mode)
├── README.md
└── .gitignore
```

---

## How to Run

**Requirements:** Python 3.8 or newer (`python --version`). Nothing else to install.

```bash
# 1. Clone the repository
git clone https://github.com/ashwingit86/hospital-patient-queue-management-system.git
cd hospital-patient-queue-management-system

# 2. Start the program
python main.py

# 3. (Optional) Run the scripted demo with simulated time
python main.py --demo
```

On Windows, if `python` is not found, use `py main.py`.

**Quick start inside the program:** choose option `8` to load 8 sample patients, then `3` to view the queues and `2` to call the next patient.

---

## Menu Options

| Option | Action |
|---|---|
| 1 | Register a patient (name, age, severity, department) |
| 2 | Call the next patient for consultation |
| 3 | Display the priority queue and the routine queue |
| 4 | Search for a patient by ID (accepts `P001`, `p1` or `1`) |
| 5 | Sort and display all patients (by ID, name, severity or waiting time, using the algorithm you pick) |
| 6 | Cancel a waiting patient |
| 7 | Statistics (served, waiting, cancelled, average wait) |
| 8 | Load sample data |
| 0 | Exit |

Invalid input (empty name, non-numeric age, severity outside 1 to 3, unknown ID) is handled with an error message and never crashes the program.

---

## Sample Output

Output of `python main.py --demo` (time is simulated, so waits are shown in minutes):

```
--- 1. Patients arrive (clock advances between arrivals) ---
  t=   0 min  P001  Ravi Kumar     Routine   -> routine queue
  t=   3 min  P002  Anita Sharma   Urgent    -> priority queue
  t=   6 min  P003  Suresh Patil   Emergency -> priority queue
  t=   9 min  P004  Meera Joshi    Routine   -> routine queue
  t=  12 min  P005  Imran Khan     Emergency -> priority queue
  t=  15 min  P006  Kavita Rao     Routine   -> routine queue
  t=  18 min  P007  Dev Mehta      Urgent    -> priority queue
  t=  21 min  P008  Sunita Verma   Routine   -> routine queue

=== PRIORITY QUEUE  (Emergency / Urgent - called first) ===
ID    Name               Age  Severity  Department   Status    Wait(min)
------------------------------------------------------------------------
P003  Suresh Patil        62  Emergency Cardiology   Waiting        18.0
P005  Imran Khan           8  Emergency Pediatrics   Waiting        12.0
P002  Anita Sharma        30  Urgent    Medicine     Waiting        21.0
P007  Dev Mehta           37  Urgent    Orthopedics  Waiting         6.0

=== ROUTINE QUEUE  (FIFO - first come, first served) ===
ID    Name               Age  Severity  Department   Status    Wait(min)
------------------------------------------------------------------------
P001  Ravi Kumar          45  Routine   OPD          Waiting        24.0
P004  Meera Joshi         25  Routine   ENT          Waiting        15.0
P006  Kavita Rao          52  Routine   OPD          Waiting         9.0
P008  Sunita Verma        70  Routine   Medicine     Waiting         3.0

--- 2. Doctor calls patients (emergencies jump the queue) ---
  t=  28 min  called P003 Suresh Patil   Emergency waited 22.0 min
  t=  32 min  called P005 Imran Khan     Emergency waited 20.0 min
  t=  36 min  called P002 Anita Sharma   Urgent    waited 33.0 min
  t=  40 min  called P007 Dev Mehta      Urgent    waited 22.0 min
  t=  44 min  called P001 Ravi Kumar     Routine   waited 44.0 min
```

Notice that routine patient P001 arrived first, yet all four emergency/urgent patients are called before them, and within each severity the earlier arrival goes first.

---

## Running Tests

```bash
python -m unittest discover -s tests -v
```

The 22 tests cover: FIFO order, heap ordering and removal, binary and linear search (found and missing IDs), all three sorting algorithms (correctness and stability), emergency-before-routine, tie-breaking, the fairness rule, cancellation, input validation and wait-time statistics.

---

## Design Decisions

- **Why a priority queue instead of a plain queue?** A plain queue serves strictly by arrival, so a critical patient could wait behind many routine ones. A heap serves the most urgent first in O(log n).
- **Why also keep a FIFO queue for routine patients?** Routine patients all have equal priority, so arrival order is exactly right, and a linked-list queue does it in O(1).
- **Why binary search?** Patient IDs are assigned in increasing order and appended, so the master list is always sorted by ID. Binary search is O(log n) instead of O(n).
- **Why write sorting ourselves?** To demonstrate the algorithms. All three are stable, so patients with equal keys keep their original order.
- **Fairness rule:** after `FAIRNESS_LIMIT = 5` consecutive priority patients, one routine patient is called (only counted while a routine patient is actually waiting).

---

## Scope Note and Future Work

This project covers queues, priority queues, lists, searching and sorting. It does **not** include:

- Saving data to a file or database (records exist only while the program runs).
- Multiple doctors or per-department queues.
- A graphical or web interface.

Possible extensions: file persistence (JSON/CSV), one priority queue per department, an "undo last call" feature using a stack, and a hash map index for O(1) lookup by ID.
