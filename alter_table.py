from backend.app.database import engine
from sqlalchemy import text

# Add dag_json column to workflow_defs if it doesn't exist
with engine.connect() as conn:
    conn.execute(
        text(
            """
            ALTER TABLE workflow_defs
            ADD COLUMN dag_json TEXT;
            """
        )
    )
    print("dag_json column added successfully.")
