"""Hospital Patient Queue Management System - menu driven program.

Run:   python main.py           (interactive menu)
       python main.py --demo    (scripted demo with simulated time)
"""

import sys

from src.hospital import HospitalSystem, SimulatedClock
from src.patient import EMERGENCY, URGENT, SEVERITY_NAMES

SAMPLE_PATIENTS = [
    ("Ravi Kumar", 45, 3, "OPD"),
    ("Anita Sharma", 30, 2, "Medicine"),
    ("Suresh Patil", 62, 1, "Cardiology"),
    ("Meera Joshi", 25, 3, "ENT"),
    ("Imran Khan", 8, 1, "Pediatrics"),
    ("Kavita Rao", 52, 3, "OPD"),
    ("Dev Mehta", 37, 2, "Orthopedics"),
    ("Sunita Verma", 70, 3, "Medicine"),
]


# ---------------------------------------------------------------- display helpers
def format_table(patients, now):
    if not patients:
        return "  (none)"
    header = (f"{'ID':<6}{'Name':<18}{'Age':>4}  {'Severity':<10}"
              f"{'Department':<13}{'Status':<10}{'Wait(min)':>9}")
    lines = [header, "-" * len(header)]
    for p in patients:
        lines.append(f"{p.code:<6}{p.name[:17]:<18}{p.age:>4}  {p.severity_name:<10}"
                     f"{p.department[:12]:<13}{p.status:<10}{p.wait_time(now):>9.1f}")
    return "\n".join(lines)


def queue_name(patient):
    return "priority queue" if patient.severity in (EMERGENCY, URGENT) else "routine queue"


def show_queues(h):
    now = h.clock()
    print("\n=== PRIORITY QUEUE  (Emergency / Urgent - called first) ===")
    print(format_table(h.priority_list(), now))
    print("\n=== ROUTINE QUEUE  (FIFO - first come, first served) ===")
    print(format_table(h.routine_list(), now))


def show_stats(h):
    s = h.stats()
    print("\n=== STATISTICS ===")
    print(f"  Registered patients : {s['registered']}")
    print(f"  Waiting             : {s['waiting']} "
          f"(priority {s['priority_waiting']}, routine {s['routine_waiting']})")
    print(f"  Served              : {s['served']}")
    print(f"  Cancelled           : {s['cancelled']}")
    print(f"  Average wait (served): {s['avg_wait_served']:.1f} min")
    print(f"  Longest current wait : {s['longest_current_wait']:.1f} min")


# ---------------------------------------------------------------- menu actions
def action_register(h):
    name = input("Patient name: ")
    age = input("Age: ")
    print("Severity: 1 = Emergency, 2 = Urgent, 3 = Routine")
    severity = input("Severity (1-3): ")
    department = input("Department [General]: ")
    try:
        p = h.register(name, age, severity, department)
    except ValueError as error:
        print(f"  Error: {error}")
        return
    print(f"  Registered {p.name} as {p.code} ({p.severity_name}) -> added to the {queue_name(p)}.")


def action_call_next(h):
    p = h.call_next()
    if p is None:
        print("  No patients are waiting.")
    else:
        print(f"  Now calling: {p.code} - {p.name} ({p.severity_name}, {p.department}). "
              f"Waited {p.wait_time(h.clock()):.1f} min.")


def action_search(h):
    try:
        pid = h.parse_pid(input("Enter patient ID (e.g. P001): "))
    except ValueError as error:
        print(f"  Error: {error}")
        return
    p = h.find(pid)
    if p is None:
        print(f"  No patient found with ID P{pid:03d}.")
    else:
        print("  Patient found:")
        print(format_table([p], h.clock()))


def action_sort(h):
    print("Sort by: 1 = ID, 2 = Name, 3 = Severity, 4 = Waiting time (longest first)")
    field = {"1": "id", "2": "name", "3": "severity", "4": "wait"}.get(input("Choice: ").strip())
    print("Algorithm: 1 = Merge sort, 2 = Insertion sort, 3 = Bubble sort")
    algo = {"1": "merge", "2": "insertion", "3": "bubble"}.get(input("Choice: ").strip())
    if field is None or algo is None:
        print("  Invalid choice.")
        return
    print(f"\n  All patients sorted by {field} using {algo} sort:")
    print(format_table(h.sorted_patients(by=field, algorithm=algo), h.clock()))


def action_cancel(h):
    try:
        p = h.cancel(h.parse_pid(input("Enter patient ID to cancel: ")))
    except (ValueError, LookupError) as error:
        print(f"  Error: {error.args[0]}")
        return
    print(f"  Cancelled {p.code} - {p.name}.")


def action_sample(h):
    for name, age, severity, dept in SAMPLE_PATIENTS:
        h.register(name, age, severity, dept)
    print(f"  Loaded {len(SAMPLE_PATIENTS)} sample patients.")


MENU = """
==== HOSPITAL PATIENT QUEUE MANAGEMENT SYSTEM ====
 1. Register patient
 2. Call next patient
 3. Display waiting queues
 4. Search patient by ID
 5. Sort and display all patients
 6. Cancel a patient
 7. Statistics
 8. Load sample data
 0. Exit"""

ACTIONS = {
    "1": action_register,
    "2": action_call_next,
    "3": show_queues,
    "4": action_search,
    "5": action_sort,
    "6": action_cancel,
    "7": show_stats,
    "8": action_sample,
}


def run_menu():
    h = HospitalSystem()
    while True:
        print(MENU)
        try:
            choice = input("Enter choice: ").strip()
        except EOFError:
            print()
            break
        if choice == "0":
            print("Goodbye!")
            break
        action = ACTIONS.get(choice)
        if action is None:
            print("  Invalid choice, please enter a number from the menu.")
            continue
        try:
            action(h)
        except EOFError:
            print()
            break


# ---------------------------------------------------------------- scripted demo
def run_demo():
    clock = SimulatedClock()
    h = HospitalSystem(clock=clock)

    print("--- 1. Patients arrive (clock advances between arrivals) ---")
    for name, age, severity, dept in SAMPLE_PATIENTS:
        p = h.register(name, age, severity, dept)
        print(f"  t={clock():>4.0f} min  {p.code}  {p.name:<14} {p.severity_name:<9} -> {queue_name(p)}")
        clock.advance(3)

    show_queues(h)

    print("\n--- 2. Doctor calls patients (emergencies jump the queue) ---")
    for _ in range(5):
        clock.advance(4)
        p = h.call_next()
        print(f"  t={clock():>4.0f} min  called {p.code} {p.name:<14} {p.severity_name:<9} waited {p.wait_time(clock()):.1f} min")

    print("\n--- 3. Cancel P006 (Kavita Rao left the hospital) ---")
    print(f"  Cancelled {h.cancel(6).code}")

    print("\n--- 4. Search by patient ID ---")
    print(format_table([h.find(h.parse_pid('P004'))], clock()))
    print(f"  Search for P099 -> {h.find(99)}")

    print("\n--- 5. Remaining queues ---")
    show_queues(h)

    print("\n--- 6. All patients sorted by severity (merge sort) ---")
    print(format_table(h.sorted_patients(by="severity", algorithm="merge"), clock()))

    show_stats(h)


if __name__ == "__main__":
    if "--demo" in sys.argv:
        run_demo()
    else:
        run_menu()
