# backend/app/tasks/python_fn.py
from backend.celery_app import celery_app
import time

@celery_app.task(
    bind=True,
    name="backend.app.tasks.python_fn.python_fn",
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=2,
    time_limit=30,
    soft_time_limit=25,
    queue="cpu",  # explicit CPU queue
)
def python_fn(self, x, y, operation="add", fn=None):
    """Small CPU-bound example; simulates heavier compute with sleep."""
    print(f"Running step '{fn}' with x={x}, y={y}, operation={operation}")
    time.sleep(3)  # simulate compute

    try:
        if operation == "add":
            result = x + y
        elif operation == "sub":
            result = x - y
        elif operation == "mul":
            result = x * y
        elif operation == "div":
            result = x / y if y != 0 else None
        else:
            return {"fn": fn, "error": f"Unsupported operation '{operation}'"}

        return {"fn": fn, "operation": operation, "x": x, "y": y, "result": result}
    except Exception as e:
        raise self.retry(exc=e)
