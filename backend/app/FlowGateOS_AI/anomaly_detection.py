import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Loading the dataset
#df = pd.read_csv(r"C:\Users\acer\Desktop\Infinity AI Work\InfinityStyleVerse\backend\app\FlowGateOS_AI\run_steps_sample_data.csv", parse_dates=['started_at', 'ended_at'])

# Definining the initial metrics
# Fallback rate - assuming 'failed' status indicates a fallback for now
#df['is_fallback'] = df['status'].isin(['failed']).astype(int)

# Retry bursts - counting attempts > 0 as retries
#df['retry_count'] = df['attempt'].apply(lambda x: max(0, x - 1)) 

# Worker heartbeat gaps -randomly assigning values between 1 and 15s
#df['heartbeat_gap'] = np.random.uniform(1, 15, size=len(df))

# Saving
#df.to_csv('anomaly_data.csv', index=False)
#print("Saved to anomaly_data.csv!")



# Loading the dataset with anomaly data
df = pd.read_csv(r"C:\Users\acer\Desktop\Infinity AI Work\InfinityStyleVerse\backend\app\FlowGateOS_AI\anomaly_data.csv", parse_dates=['started_at', 'ended_at'])

df = df.sort_values('started_at')

# Aggregating metrics by 1-hour windows
df['hour'] = df['started_at'].dt.floor('1H')
metrics = df.groupby('hour').agg({
    'is_fallback': 'mean',    # Proportion of fallbacks per hour
    'retry_count': 'sum',     # Total retries per hour
    'heartbeat_gap': 'mean'   # Average heartbeat gap per hour
}).reset_index()

# Saving
metrics.to_csv('anomaly_metrics.csv', index=False)
print("Saved to anomaly_metrics.csv")