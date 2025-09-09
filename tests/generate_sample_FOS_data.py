from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import create_app
from backend.app.database import db
import random
from datetime import datetime, timedelta

load_dotenv()

app = create_app()
with app.app_context():
    engine = db.engine

    # Inserting sample data into run_steps
    with engine.connect() as connection:
        for i in range(100):  # Generating 100 sample rows
            run_id = f"run_{i:03d}"
            step_id = f"step_{random.randint(1, 5)}"
            step_type = random.choice(["model_call", "http_call", "join"])
            status = random.choice(["succeeded", "failed"])
            started_at = datetime.now() - timedelta(minutes=random.randint(1, 100))
            ended_at = started_at + timedelta(seconds=random.randint(10, 300))
            connection.execute(
                text("""
                    INSERT INTO run_steps (run_id, step_id, type, status, started_at, ended_at)
                    VALUES (:run_id, :step_id, :type, :status, :started_at, :ended_at)
                """),
                {"run_id": run_id, "step_id": step_id, "type": step_type, "status": status,
                 "started_at": started_at, "ended_at": ended_at}
            )
        connection.commit()
        print("Sample data inserted successfully!")