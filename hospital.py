"""HospitalSystem: ties the data structures together.

 List            -> self.patients          (every patient record, sorted by ID)
 Priority Queue  -> self.priority_queue    (Emergency + Urgent, heap)
 Queue           -> self.routine_queue     (Routine, FIFO linked list)
 Searching       -> find()                 (binary search by patient ID)
 Sorting         -> sorted_patients()      (merge / insertion / bubble sort)
"""

import time

from .patient import (EMERGENCY, URGENT, ROUTINE, SEVERITY_NAMES,
                      WAITING, SERVED, CANCELLED, Patient)
from .priority_queue import PriorityQueue
from .queue_ds import LinkedQueue
from .searching import binary_search
from .sorting import ALGORITHMS


def real_clock():
    """Current time in minutes."""
    return time.time() / 60.0


class SimulatedClock:
    """Manual clock so demos and tests can 'advance' time without waiting."""

    def __init__(self, start=0.0):
        self.now = float(start)

    def advance(self, minutes):
        self.now += minutes

    def __call__(self):
        return self.now


class HospitalSystem:
    # After this many consecutive Emergency/Urgent patients, one waiting
    # Routine patient is called. This prevents starvation of routine patients.
    FAIRNESS_LIMIT = 5

    def __init__(self, clock=None):
        self.clock = clock or real_clock
        self.patients = []                                           # List
        self.priority_queue = PriorityQueue(key=lambda p: p.priority_key())
        self.routine_queue = LinkedQueue()
        self._next_id = 1
        self._priority_streak = 0

    # ---------------- registration ----------------
    def register(self, name, age, severity, department="General"):
        name = str(name).strip()
        if not name:
            raise ValueError("Name cannot be empty.")
        try:
            age = int(age)
        except (TypeError, ValueError):
            raise ValueError("Age must be a whole number.")
        if not 0 <= age <= 120:
            raise ValueError("Age must be between 0 and 120.")
        try:
            severity = int(severity)
        except (TypeError, ValueError):
            severity = None
        if severity not in SEVERITY_NAMES:
            raise ValueError("Severity must be 1 (Emergency), 2 (Urgent) or 3 (Routine).")
        department = str(department).strip() or "General"

        patient = Patient(self._next_id, name, age, severity, department, self.clock())
        self._next_id += 1
        self.patients.append(patient)            # stays sorted by pid
        if severity in (EMERGENCY, URGENT):
            self.priority_queue.push(patient)    # O(log n)
        else:
            self.routine_queue.enqueue(patient)  # O(1)
        return patient

    # ---------------- serving ----------------
    def call_next(self):
        """Call the next patient for consultation. Returns the Patient or None."""
        has_priority = not self.priority_queue.is_empty()
        has_routine = not self.routine_queue.is_empty()
        if not has_priority and not has_routine:
            return None

        take_routine = has_routine and (not has_priority or
                                        self._priority_streak >= self.FAIRNESS_LIMIT)
        if take_routine:
            patient = self.routine_queue.dequeue()
            self._priority_streak = 0
        else:
            patient = self.priority_queue.pop()
            if has_routine:                      # only count when someone is being made to wait
                self._priority_streak += 1

        patient.status = SERVED
        patient.end_time = self.clock()
        return patient

    def cancel(self, pid):
        """Remove a waiting patient from the queues."""
        patient = self.find(pid)
        if patient is None:
            raise LookupError(f"No patient with ID {pid}.")
        if patient.status != WAITING:
            raise ValueError(f"{patient.code} is already {patient.status.lower()}.")
        if patient.severity in (EMERGENCY, URGENT):
            self.priority_queue.remove(lambda p: p.pid == pid)
        else:
            self.routine_queue.remove(lambda p: p.pid == pid)
        patient.status = CANCELLED
        patient.end_time = self.clock()
        return patient

    # ---------------- searching ----------------
    def find(self, pid):
        """Binary search by patient ID. Returns the Patient or None. O(log n)."""
        index = binary_search(self.patients, pid)
        return self.patients[index] if index != -1 else None

    @staticmethod
    def parse_pid(text):
        """Accepts 'P001', 'p1' or '1'."""
        t = str(text).strip().upper()
        if t.startswith("P"):
            t = t[1:]
        if not t.isdigit():
            raise ValueError("Invalid patient ID. Use a format like P001 or 1.")
        return int(t)

    # ---------------- views ----------------
    def priority_list(self):
        """Emergency/Urgent patients in the order they will be called."""
        return self.priority_queue.to_sorted_list()

    def routine_list(self):
        """Routine patients, front of the queue first."""
        return self.routine_queue.to_list()

    def sorted_patients(self, by="id", algorithm="merge", reverse=None):
        """All patients sorted by: id | name | severity | wait (longest first)."""
        now = self.clock()
        keys = {
            "id": lambda p: p.pid,
            "name": lambda p: p.name.lower(),
            "severity": lambda p: (p.severity, p.pid),
            "wait": lambda p: p.wait_time(now),
        }
        if by not in keys:
            raise ValueError(f"Unknown sort field: {by}")
        if algorithm not in ALGORITHMS:
            raise ValueError(f"Unknown algorithm: {algorithm}")
        if reverse is None:
            reverse = (by == "wait")             # longest wait first by default
        return ALGORITHMS[algorithm](self.patients, key=keys[by], reverse=reverse)

    def stats(self):
        now = self.clock()
        served = [p for p in self.patients if p.status == SERVED]
        waiting = [p for p in self.patients if p.status == WAITING]
        cancelled = [p for p in self.patients if p.status == CANCELLED]
        avg_wait = sum(p.wait_time(now) for p in served) / len(served) if served else 0.0
        longest = max((p.wait_time(now) for p in waiting), default=0.0)
        return {
            "registered": len(self.patients),
            "waiting": len(waiting),
            "served": len(served),
            "cancelled": len(cancelled),
            "priority_waiting": len(self.priority_queue),
            "routine_waiting": len(self.routine_queue),
            "avg_wait_served": avg_wait,
            "longest_current_wait": longest,
        }
