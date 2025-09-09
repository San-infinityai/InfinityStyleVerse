from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, inspect

load_dotenv()

# Creating database connection
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# Inspecting the database
inspector = inspect(engine)
print("Available tables:", inspector.get_table_names())

with engine.connect() as connection:
    print("Connection successful!")