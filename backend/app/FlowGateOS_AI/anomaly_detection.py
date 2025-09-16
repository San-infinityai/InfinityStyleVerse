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
#df = pd.read_csv(r"C:\Users\acer\Desktop\Infinity AI Work\InfinityStyleVerse\backend\app\FlowGateOS_AI\anomaly_data.csv", parse_dates=['started_at', 'ended_at'])

#df = df.sort_values('started_at')

# Aggregating metrics by 1-hour windows
#df['hour'] = df['started_at'].dt.floor('1H')
#metrics = df.groupby('hour').agg({
#    'is_fallback': 'mean',    # Proportion of fallbacks per hour
#    'retry_count': 'sum',     # Total retries per hour
#    'heartbeat_gap': 'mean'   # Average heartbeat gap per hour
#}).reset_index()

# Saving
#metrics.to_csv('anomaly_metrics.csv', index=False)
#print("Saved to anomaly_metrics.csv")



# Loading the metrics
metrics = pd.read_csv(r"C:\Users\acer\Desktop\Infinity AI Work\InfinityStyleVerse\backend\app\FlowGateOS_AI\anomaly_metrics.csv", parse_dates=['hour'])

# Applying EWMA with a smoothing factor like 0.3 to each metric
metrics['ewma_fallback'] = metrics['is_fallback'].ewm(alpha=0.3, adjust=False).mean()
metrics['ewma_retry'] = metrics['retry_count'].ewm(alpha=0.3, adjust=False).mean()
metrics['ewma_heartbeat'] = metrics['heartbeat_gap'].ewm(alpha=0.3, adjust=False).mean()

# Calculating rolling standard deviation and 3σ thresholds
window_size = 3  # Using the last 3 hours 
metrics['std_fallback'] = metrics['is_fallback'].rolling(window=window_size, min_periods=1).std().fillna(0)
metrics['std_retry'] = metrics['retry_count'].rolling(window=window_size, min_periods=1).std().fillna(0)
metrics['std_heartbeat'] = metrics['heartbeat_gap'].rolling(window=window_size, min_periods=1).std().fillna(0)

# Defining 3σ upper thresholds - anomalies above mean + 3σ
metrics['threshold_fallback'] = metrics['ewma_fallback'] + 3 * metrics['std_fallback']
metrics['threshold_retry'] = metrics['ewma_retry'] + 3 * metrics['std_retry']
metrics['threshold_heartbeat'] = metrics['ewma_heartbeat'] + 3 * metrics['std_heartbeat']

# Detecting anomalies where the actual value exceeds threshold
metrics['anomaly_fallback'] = metrics['is_fallback'] > metrics['threshold_fallback']
metrics['anomaly_retry'] = metrics['retry_count'] > metrics['threshold_retry']
metrics['anomaly_heartbeat'] = metrics['heartbeat_gap'] > metrics['threshold_heartbeat']

# Saving the results
metrics.to_csv('anomaly_results.csv', index=False)
print("Saved to anomaly_results.csv")