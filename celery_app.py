# celery_app.py
from celery import Celery

celery_app = Celery(
    "workflow_engine",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)

# Make tasks known to the worker
import tasks
