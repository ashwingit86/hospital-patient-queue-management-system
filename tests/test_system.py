"""Unit tests. Run from the project root:  python -m unittest discover -s tests -v"""

import os
import random
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.hospital import HospitalSystem, SimulatedClock
from src.patient import CANCELLED, SERVED, WAITING
from src.priority_queue import PriorityQueue
from src.queue_ds import LinkedQueue
from src.searching import binary_search, linear_search
from src.sorting import bubble_sort, insertion_sort, merge_sort


class TestLinkedQueue(unittest.TestCase):
    def test_fifo_order(self):
        q = LinkedQueue()
        for x in (1, 2, 3):
            q.enqueue(x)
        self.assertEqual([q.dequeue(), q.dequeue(), q.dequeue()], [1, 2, 3])
        self.assertTrue(q.is_empty())

    def test_empty_raises(self):
        with self.assertRaises(IndexError):
            LinkedQueue().dequeue()

    def test_remove_middle_front_rear(self):
        q = LinkedQueue()
        for x in range(1, 6):
            q.enqueue(x)
        self.assertEqual(q.remove(lambda v: v == 3), 3)   # middle
        self.assertEqual(q.remove(lambda v: v == 1), 1)   # front
        self.assertEqual(q.remove(lambda v: v == 5), 5)   # rear
        self.assertEqual(q.to_list(), [2, 4])
        q.enqueue(9)                                      # rear pointer still valid
        self.assertEqual(q.to_list(), [2, 4, 9])
        self.assertIsNone(q.remove(lambda v: v == 42))
        self.assertEqual(len(q), 3)


class TestPriorityQueue(unittest.TestCase):
    def test_pops_in_sorted_order(self):
        data = [random.randint(0, 100) for _ in range(200)]
        pq = PriorityQueue()
        for x in data:
            pq.push(x)
        self.assertEqual([pq.pop() for _ in range(len(data))], sorted(data))

    def test_remove_keeps_heap_valid(self):
        data = list(range(50))
        random.shuffle(data)
        pq = PriorityQueue()
        for x in data:
            pq.push(x)
        for victim in (0, 25, 49, 10):
            self.assertEqual(pq.remove(lambda v, t=victim: v == t), victim)
        expected = sorted(set(range(50)) - {0, 25, 49, 10})
        self.assertEqual([pq.pop() for _ in range(len(pq))], expected)

    def test_to_sorted_list_does_not_modify(self):
        pq = PriorityQueue()
        for x in (5, 1, 3):
            pq.push(x)
        self.assertEqual(pq.to_sorted_list(), [1, 3, 5])
        self.assertEqual(len(pq), 3)

    def test_empty_raises(self):
        with self.assertRaises(IndexError):
            PriorityQueue().pop()


class TestSearching(unittest.TestCase):
    def setUp(self):
        h = HospitalSystem()
        for i in range(1, 11):
            h.register(f"Person {i}", 30, 3)
        self.patients = h.patients

    def test_both_searches_find_every_id(self):
        for pid in range(1, 11):
            self.assertEqual(binary_search(self.patients, pid), pid - 1)
            self.assertEqual(linear_search(self.patients, pid), pid - 1)

    def test_missing_id(self):
        self.assertEqual(binary_search(self.patients, 99), -1)
        self.assertEqual(linear_search(self.patients, 0), -1)
        self.assertEqual(binary_search([], 1), -1)


class TestSorting(unittest.TestCase):
    def test_all_algorithms_match_builtin(self):
        data = [random.randint(-50, 50) for _ in range(120)]
        for algo in (bubble_sort, insertion_sort, merge_sort):
            self.assertEqual(algo(data), sorted(data))
            self.assertEqual(algo(data, reverse=True), sorted(data, reverse=True))

    def test_stability(self):
        data = [("a", 2), ("b", 1), ("c", 2), ("d", 1)]
        for algo in (bubble_sort, insertion_sort, merge_sort):
            self.assertEqual(algo(data, key=lambda t: t[1]),
                             [("b", 1), ("d", 1), ("a", 2), ("c", 2)])
            self.assertEqual(algo(data, key=lambda t: t[1], reverse=True),
                             [("a", 2), ("c", 2), ("b", 1), ("d", 1)])

    def test_empty_and_single(self):
        for algo in (bubble_sort, insertion_sort, merge_sort):
            self.assertEqual(algo([]), [])
            self.assertEqual(algo([7]), [7])


class TestHospitalSystem(unittest.TestCase):
    def setUp(self):
        self.clock = SimulatedClock()
        self.h = HospitalSystem(clock=self.clock)

    def test_emergency_served_before_routine(self):
        self.h.register("Routine One", 40, 3)
        self.h.register("Emergency One", 50, 1)
        self.assertEqual(self.h.call_next().name, "Emergency One")
        self.assertEqual(self.h.call_next().name, "Routine One")

    def test_emergency_before_urgent_and_fifo_on_ties(self):
        self.h.register("Urgent A", 30, 2)
        self.h.register("Emergency A", 30, 1)
        self.h.register("Urgent B", 30, 2)
        self.h.register("Emergency B", 30, 1)
        order = [self.h.call_next().name for _ in range(4)]
        self.assertEqual(order, ["Emergency A", "Emergency B", "Urgent A", "Urgent B"])

    def test_routine_is_fifo(self):
        for n in ("R1", "R2", "R3"):
            self.h.register(n, 20, 3)
        self.assertEqual([self.h.call_next().name for _ in range(3)], ["R1", "R2", "R3"])

    def test_call_next_when_empty(self):
        self.assertIsNone(self.h.call_next())

    def test_fairness_rule_prevents_starvation(self):
        self.h.register("Routine", 40, 3)
        for i in range(8):
            self.h.register(f"E{i}", 30, 1)
        names = [self.h.call_next().name for _ in range(9)]
        # 5 emergencies, then the routine patient gets a turn, then the rest
        self.assertEqual(names[5], "Routine")
        self.assertEqual(names[:5], ["E0", "E1", "E2", "E3", "E4"])

    def test_cancel_removes_from_queue(self):
        a = self.h.register("A", 30, 1)
        b = self.h.register("B", 30, 1)
        r = self.h.register("R", 30, 3)
        self.h.cancel(a.pid)
        self.h.cancel(r.pid)
        self.assertEqual(a.status, CANCELLED)
        self.assertEqual(self.h.call_next().name, "B")
        self.assertIsNone(self.h.call_next())
        with self.assertRaises(ValueError):
            self.h.cancel(b.pid)         # already served
        with self.assertRaises(LookupError):
            self.h.cancel(999)

    def test_find_and_parse_pid(self):
        p = self.h.register("Find Me", 22, 2)
        self.assertIs(self.h.find(self.h.parse_pid("P001")), p)
        self.assertIs(self.h.find(self.h.parse_pid("1")), p)
        self.assertIsNone(self.h.find(5))
        with self.assertRaises(ValueError):
            self.h.parse_pid("abc")

    def test_validation(self):
        bad = [("", 30, 1), ("X", "abc", 1), ("X", -1, 1), ("X", 200, 1),
               ("X", 30, 4), ("X", 30, "high")]
        for name, age, sev in bad:
            with self.assertRaises(ValueError):
                self.h.register(name, age, sev)
        self.assertEqual(len(self.h.patients), 0)

    def test_sorted_patients_every_algorithm(self):
        for name, sev in (("Zed", 3), ("Amy", 1), ("Bob", 2), ("Cat", 1)):
            self.h.register(name, 30, sev)
        for algo in ("merge", "insertion", "bubble"):
            self.assertEqual([p.name for p in self.h.sorted_patients("name", algo)],
                             ["Amy", "Bob", "Cat", "Zed"])
            self.assertEqual([p.name for p in self.h.sorted_patients("severity", algo)],
                             ["Amy", "Cat", "Bob", "Zed"])
            self.assertEqual([p.pid for p in self.h.sorted_patients("id", algo)], [1, 2, 3, 4])

    def test_wait_times_and_stats(self):
        self.h.register("First", 30, 3)      # arrives t=0
        self.clock.advance(10)
        self.h.register("Second", 30, 3)     # arrives t=10
        self.clock.advance(10)               # t=20
        served = self.h.call_next()          # First waited 20
        self.assertEqual(served.wait_time(self.clock()), 20)
        s = self.h.stats()
        self.assertEqual((s["registered"], s["served"], s["waiting"]), (2, 1, 1))
        self.assertEqual(s["avg_wait_served"], 20)
        self.assertEqual(s["longest_current_wait"], 10)
        longest_first = self.h.sorted_patients("wait")
        self.assertEqual(longest_first[0].name, "First")
        self.assertEqual(self.h.patients[1].status, WAITING)
        self.assertEqual(served.status, SERVED)


if __name__ == "__main__":
    unittest.main()
