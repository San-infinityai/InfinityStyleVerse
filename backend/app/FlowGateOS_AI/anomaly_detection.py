import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Loading the dataset
df = pd.read_csv(r"C:\Users\acer\Desktop\Infinity AI Work\InfinityStyleVerse\backend\app\FlowGateOS_AI\run_steps_sample_data.csv", parse_dates=['started_at', 'ended_at'])

# Definining the initial metrics
# Fallback rate - assuming 'failed' status indicates a fallback for now
df['is_fallback'] = df['status'].isin(['failed']).astype(int)

# Retry bursts - counting attempts > 0 as retries
df['retry_count'] = df['attempt'].apply(lambda x: max(0, x - 1)) 

# Worker heartbeat gaps - approximate as time difference between consecutive started_at for same run_id
df = df.sort_values(['started_at'])
df['heartbeat_gap'] = df['started_at'].diff().dt.total_seconds().fillna(0)
df = df.sort_values(['id'])

# Saving
df.to_csv('anomaly_data.csv', index=False)
print("Saved to anomaly_data.csv!")