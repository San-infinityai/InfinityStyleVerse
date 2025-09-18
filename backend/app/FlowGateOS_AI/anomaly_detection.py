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
#metrics = pd.read_csv(r"C:\Users\acer\Desktop\Infinity AI Work\InfinityStyleVerse\backend\app\FlowGateOS_AI\anomaly_metrics.csv", parse_dates=['hour'])

# Applying EWMA with a smoothing factor like 0.3 to each metric
#metrics['ewma_fallback'] = metrics['is_fallback'].ewm(alpha=0.3, adjust=False).mean()
#metrics['ewma_retry'] = metrics['retry_count'].ewm(alpha=0.3, adjust=False).mean()
#metrics['ewma_heartbeat'] = metrics['heartbeat_gap'].ewm(alpha=0.3, adjust=False).mean()

# Calculating rolling standard deviation and 3σ thresholds
#window_size = 3  # Using the last 3 hours 
#metrics['std_fallback'] = metrics['is_fallback'].rolling(window=window_size, min_periods=1).std().fillna(0)
#metrics['std_retry'] = metrics['retry_count'].rolling(window=window_size, min_periods=1).std().fillna(0)
#metrics['std_heartbeat'] = metrics['heartbeat_gap'].rolling(window=window_size, min_periods=1).std().fillna(0)

# Defining 3σ upper thresholds - anomalies above mean + 3σ
#metrics['threshold_fallback'] = metrics['ewma_fallback'] + 3 * metrics['std_fallback']
#metrics['threshold_retry'] = metrics['ewma_retry'] + 3 * metrics['std_retry']
#metrics['threshold_heartbeat'] = metrics['ewma_heartbeat'] + 3 * metrics['std_heartbeat']

# Detecting anomalies where the actual value exceeds threshold
#metrics['anomaly_fallback'] = metrics['is_fallback'] > metrics['threshold_fallback']
#metrics['anomaly_retry'] = metrics['retry_count'] > metrics['threshold_retry']
#metrics['anomaly_heartbeat'] = metrics['heartbeat_gap'] > metrics['threshold_heartbeat']

# Saving the results
#metrics.to_csv('anomaly_results.csv', index=False)
#print("Saved to anomaly_results.csv")



# Generating anomalies in the dataset and testing again!

#df = pd.read_csv(r"C:\Users\acer\Desktop\Infinity AI Work\InfinityStyleVerse\backend\app\FlowGateOS_AI\run_steps_sample_data.csv", parse_dates=['started_at', 'ended_at'])

# Simulating anomalies by entering extreme values
# Increasing fallback rate for one hour (For eg: 09:00:00)
#df.loc[df['started_at'].between('2025-09-11 09:00:00', '2025-09-11 09:59:59'), 'status'] = 'failed'
#df['is_fallback'] = df['status'].isin(['failed']).astype(int)

# Simulating retry burst for another hour (Eg: 08:00:00)
#df.loc[df['started_at'].between('2025-09-11 08:00:00', '2025-09-11 08:59:59'), 'attempt'] += 5  # Add 5 retries
#df['retry_count'] = df['attempt'].apply(lambda x: max(0, x - 1))

# Simulating heartbeat gap spike for another hour (Eg: 07:00:00)
#df.loc[df['started_at'].between('2025-09-11 07:00:00', '2025-09-11 07:59:59'), 'heartbeat_gap'] = 20.0  # Set to 20s

# Recalculating the aggregated metrics with anomalies
#df['hour'] = df['started_at'].dt.floor('1H')
#metrics = df.groupby('hour').agg({
#    'is_fallback': 'mean',
#    'retry_count': 'sum',
#    'heartbeat_gap': 'mean'
#}).reset_index()

# Applying EWMA and 3σ anomaly detection
#metrics['ewma_fallback'] = metrics['is_fallback'].ewm(alpha=0.3, adjust=False).mean()
#metrics['ewma_retry'] = metrics['retry_count'].ewm(alpha=0.3, adjust=False).mean()
#metrics['ewma_heartbeat'] = metrics['heartbeat_gap'].ewm(alpha=0.3, adjust=False).mean()

#window_size = 3
#metrics['std_fallback'] = metrics['is_fallback'].rolling(window=window_size, min_periods=1).std().fillna(0)
#metrics['std_retry'] = metrics['retry_count'].rolling(window=window_size, min_periods=1).std().fillna(0)
#metrics['std_heartbeat'] = metrics['heartbeat_gap'].rolling(window=window_size, min_periods=1).std().fillna(0)

#metrics['threshold_fallback'] = metrics['ewma_fallback'] + 3 * metrics['std_fallback']
#metrics['threshold_retry'] = metrics['ewma_retry'] + 3 * metrics['std_retry']
#metrics['threshold_heartbeat'] = metrics['ewma_heartbeat'] + 3 * metrics['std_heartbeat']

#metrics['anomaly_fallback'] = metrics['is_fallback'] > metrics['threshold_fallback']
#metrics['anomaly_retry'] = metrics['retry_count'] > metrics['threshold_retry']
#metrics['anomaly_heartbeat'] = metrics['heartbeat_gap'] > metrics['threshold_heartbeat']

# Saving the results with anomalies
#metrics.to_csv('anomaly_results_with_anomalies.csv', index=False)
#print("Saved to anomaly_results_with_anomalies.csv")



df = pd.read_csv(
    r"C:\Users\acer\Desktop\Infinity AI Work\InfinityStyleVerse\backend\app\FlowGateOS_AI\run_steps_sample_data.csv",
    parse_dates=['started_at', 'ended_at']
)

# Create fallback flag
df['is_fallback'] = np.where(df['status'] == 'failed', 1, 0)

# Extract hour for grouping
df['hour'] = df['started_at'].dt.floor('h')

# Aggregate metrics per hour
metrics = df.groupby('hour').agg({
    'is_fallback': 'sum',
    'retry_count': 'sum',
    'heartbeat_gap': 'mean'
}).reset_index()

# ----- Baseline metrics (normal hours only) -----
# Here you can filter a known baseline period. For demo I use the first N hours:
baseline_period = metrics['hour'] < metrics['hour'].min() + pd.Timedelta(hours=24)
baseline_metrics = metrics[baseline_period]

# EWMA (exponential weighted moving average)
window_size = 3
metrics['ewma_fallback'] = metrics['is_fallback'].ewm(span=window_size, adjust=False).mean()
metrics['ewma_retry'] = metrics['retry_count'].ewm(span=window_size, adjust=False).mean()
metrics['ewma_heartbeat'] = metrics['heartbeat_gap'].ewm(span=window_size, adjust=False).mean()

# ----- Rolling std from baseline only -----
baseline_std = baseline_metrics[['hour', 'is_fallback', 'retry_count', 'heartbeat_gap']].copy()
baseline_std['std_fallback'] = baseline_std['is_fallback'].rolling(window=window_size, min_periods=1).std().fillna(0)
baseline_std['std_retry'] = baseline_std['retry_count'].rolling(window=window_size, min_periods=1).std().fillna(0)
baseline_std['std_heartbeat'] = baseline_std['heartbeat_gap'].rolling(window=window_size, min_periods=1).std().fillna(0)

# Keep only std columns + hour
baseline_std = baseline_std[['hour','std_fallback','std_retry','std_heartbeat']]

# Merge into main metrics, forward-fill so later hours still use baseline std
metrics = metrics.merge(baseline_std, on='hour', how='left').ffill()

# Thresholds using baseline std
sigma = 3  # can tweak to 2 for more sensitivity
metrics['threshold_fallback'] = metrics['ewma_fallback'] + sigma * metrics['std_fallback']
metrics['threshold_retry'] = metrics['ewma_retry'] + sigma * metrics['std_retry']
metrics['threshold_heartbeat'] = metrics['ewma_heartbeat'] + sigma * metrics['std_heartbeat']

# Identify anomalies
metrics['anomaly_fallback'] = metrics['is_fallback'] > metrics['threshold_fallback']
metrics['anomaly_retry'] = metrics['retry_count'] > metrics['threshold_retry']
metrics['anomaly_heartbeat'] = metrics['heartbeat_gap'] > metrics['threshold_heartbeat']

# Optional: inspect anomalies
print(metrics[['hour','retry_count','threshold_retry','anomaly_retry']])