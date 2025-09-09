# backend/app/metrics.py
from prometheus_client import Counter, Histogram

# Count how many tasks are started and failed
TASKS_STARTED = Counter("tasks_started_total", "Total tasks started", ["name"])
TASKS_FAILED  = Counter("tasks_failed_total", "Total tasks failed", ["name"])

# Measure task duration in seconds
TASKS_TIME = Histogram("task_duration_seconds", "Task execution duration", ["name"])
