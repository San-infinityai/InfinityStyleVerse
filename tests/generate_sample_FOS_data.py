from dotenv import load_dotenv
from sqlalchemy import text
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import create_app
from backend.app.database import db
import random
from datetime import datetime, timedelta
from sqlalchemy import inspect

# Load environment variables
load_dotenv()

# Create Flask app context
app = create_app()
with app.app_context():
    engine = db.engine

    inspector = inspect(engine)

# Get columns for "runs"
print("Columns in runs:")
for column in inspector.get_columns("runs"):
    print(f"  {column['name']} ({column['type']})")

# Get columns for "run_steps"
print("\nColumns in run_steps:")
for column in inspector.get_columns("run_steps"):
    print(f"  {column['name']} ({column['type']})")

    # Clear existing data (optional, for fresh start)
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM run_steps"))
        connection.execute(text("DELETE FROM runs"))
        connection.commit()

    # Insert diverse sample data into runs
    with engine.connect() as connection:
        for i in range(200):  # Match the number of runs to steps
            run_id = i
            workflow_name = random.choice(["design_to_shop_v1", "price_update_v1"])
            status = random.choice(["completed", "failed"])
            created_at = datetime.now() - timedelta(minutes=random.randint(1, 200))
            connection.execute(
                text("""
                    INSERT INTO runs (id, workflow_name, status, created_at)
                    VALUES (:id, :workflow_name, :status, :created_at)
                """),
                {"id": run_id, "workflow_name": workflow_name, "status": status, "created_at": created_at}
            )
        connection.commit()
        print("Runs data inserted successfully!")

    # Insert diverse sample data into run_steps
    with engine.connect() as connection:
        for i in range(200):  # 200 rows for more variety
            run_id = i
            step_id = f"step_{random.randint(1, 10)}"
            step_type = random.choice(["model_call", "http_call", "join", "map"])
            status = random.choice(["succeeded", "failed"])
            # Vary latency from 500ms to 5000ms for realism
            base_latency_seconds = random.uniform(0.5, 5.0)
            started_at = datetime.now() - timedelta(minutes=random.randint(1, 200))
            ended_at = started_at + timedelta(seconds=base_latency_seconds)
            if i > 0 and i % 10 == 0:  # Simulate parallel groups every 10 runs
                step_id = f"step_parallel_{random.randint(1, 5)}"

            connection.execute(
                text("""
                    INSERT INTO run_steps (run_id, step_id, type, status, started_at, ended_at)
                    VALUES (:run_id, :step_id, :type, :status, :started_at, :ended_at)
                """),
                {"run_id": run_id, "step_id": step_id, "type": step_type, "status": status,
                 "started_at": started_at, "ended_at": ended_at}
            )
        connection.commit()
        print("Sample data inserted into run_steps successfully!")
