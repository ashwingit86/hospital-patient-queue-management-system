"""Patient record. One object per registered patient, stored in the master List."""

# Severity levels: a LOWER number means a HIGHER priority.
EMERGENCY, URGENT, ROUTINE = 1, 2, 3
SEVERITY_NAMES = {EMERGENCY: "Emergency", URGENT: "Urgent", ROUTINE: "Routine"}

# Patient status values
WAITING, SERVED, CANCELLED = "Waiting", "Served", "Cancelled"


class Patient:
    def __init__(self, pid, name, age, severity, department, arrival_time):
        self.pid = pid                    # integer ID, increases with every arrival
        self.name = name
        self.age = age
        self.severity = severity          # 1 = Emergency, 2 = Urgent, 3 = Routine
        self.department = department
        self.arrival_time = arrival_time  # in minutes (from the system clock)
        self.status = WAITING
        self.end_time = None              # set when served or cancelled

    @property
    def code(self):
        """Display ID such as P001."""
        return f"P{self.pid:03d}"

    @property
    def severity_name(self):
        return SEVERITY_NAMES[self.severity]

    def priority_key(self):
        """Heap ordering key: severity first, then arrival order.

        pid grows with every registration, so it doubles as the arrival
        order and acts as the FIFO tie-breaker between equal severities.
        """
        return (self.severity, self.pid)

    def wait_time(self, now):
        """Minutes waited so far (or total wait if already served/cancelled)."""
        end = self.end_time if self.end_time is not None else now
        return max(0.0, end - self.arrival_time)

    def __repr__(self):
        return f"Patient({self.code}, {self.name!r}, {self.severity_name}, {self.status})"
