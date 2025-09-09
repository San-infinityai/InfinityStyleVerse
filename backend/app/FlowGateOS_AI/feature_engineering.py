from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from backend.app import create_app
from backend.app.database import db
import pandas as pd
import numpy as np
from datetime import datetime

load_dotenv()

app = create_app()
with app.app_context():
    engine = db.engine

    # Querying the data from run_steps
    query = """
        SELECT run_id, step_id, type, status, started_at, ended_at
        FROM run_steps
    """
    df = pd.read_sql(query, engine)

    # Converting string timestamps to datetime
    df['started_at'] = pd.to_datetime(df['started_at'])
    df['ended_at'] = pd.to_datetime(df['ended_at'])

    # Calculating features
    df['latency_ms'] = (df['ended_at'] - df['started_at']).dt.total_seconds() * 1000  # Converting to milliseconds
    df['queue_time_ms'] = df.groupby('run_id')['started_at'].diff().dt.total_seconds().fillna(0) * 1000  # Time since the last step
    df['is_parallel'] = df['step_id'].str.contains('parallel').astype(int)  # Placeholder for parallel group detection
    df['sla_breach'] = (df['latency_ms'] > 2500).astype(int)  # Example SLA threshold from design_to_shop_v1

    # Aggregating historical means and variances per step type
    historical_stats = df.groupby('type').agg({
        'latency_ms': ['mean', 'var']
    }).reset_index()
    historical_stats.columns = ['type', 'mean_latency_ms', 'var_latency_ms']
    df = df.merge(historical_stats, on='type', how='left')

    # Saving to CSV for inspection
    df.to_csv('features.csv', index=False)
    print("Features extracted and saved to features.csv")